"""Bounded, provider-free GML structural profiling candidate, version 1.

No network, schema resolution, conversion, feature-value retention or raw disposal.
XML metadata is untrusted evidence. A complete scan covers only the selected file.
"""
from __future__ import annotations

import argparse
import base64
from collections import Counter
from dataclasses import dataclass, field
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import time
from urllib.parse import urlsplit
from xml.parsers import expat

VERSION = "gis-ai-go.gml-structural-profile.candidate.v1"
XSI = "http://www.w3.org/2001/XMLSchema-instance"
XLINK = "http://www.w3.org/1999/xlink"
GML = {"http://www.opengis.net/gml", "http://www.opengis.net/gml/3.2"}
MAX_OUTPUT = 16384
HASH = re.compile(r"[0-9a-f]{64}")
FILE = re.compile(r"[0-9a-f]{64}\.json")


class Rejected(ValueError):
    """A bounded, non-reflective failure; source contents stay private."""


def canonical(value):
    return (json.dumps(value, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"), allow_nan=False) + "\n").encode("utf-8")


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def no_links(path):
    path = Path(os.path.abspath(path))
    if any(part.is_symlink() for part in (path, *path.parents)):
        raise Rejected("Symbolic links are refused")
    return path


def bounded_read(path, limit):
    path = no_links(path)
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "rb") as stream:
        if not stat.S_ISREG(os.fstat(stream.fileno()).st_mode):
            raise Rejected("Input must be a regular file")
        raw = stream.read(limit + 1)
    if len(raw) > limit:
        raise Rejected("Metadata byte ceiling exceeded")
    return raw


def inert_reference(value):
    """Preserve metadata locators, without following them or retaining secrets."""
    if not isinstance(value, str) or not value or len(value.encode()) > 2048:
        raise Rejected("Invalid metadata reference")
    if any(ord(c) < 32 or c.isspace() for c in value):
        raise Rejected("Invalid metadata reference")
    parsed = urlsplit(value)
    if parsed.username or parsed.password or parsed.query:
        raise Rejected("Credential-bearing or query-bearing metadata reference")
    if parsed.scheme and parsed.scheme not in {"http", "https", "urn"}:
        raise Rejected("Unsupported inert metadata scheme")
    if not parsed.scheme and (value.startswith(("/", "\\")) or ".." in value.split("/")):
        raise Rejected("Unsafe relative metadata reference")
    return value


def name_parts(name):
    parts = name.rsplit("}", 1)
    return (parts[0], parts[1]) if len(parts) == 2 else ("", name)


def qname(name):
    uri, local = name_parts(name)
    if len(name.encode()) > 1024 or not local or "{" in uri or "}" in uri:
        raise Rejected("XML name ceiling exceeded")
    if uri:
        inert_reference(uri)
    return "Q{" + uri + "}" + local


@dataclass(frozen=True)
class Limits:
    max_bytes: int = 64 * 1024 * 1024
    max_depth: int = 128
    max_elements: int = 1_000_000
    max_attributes: int = 2_000_000
    max_paths: int = 20_000
    max_patterns: int = 50_000
    max_sequence_items: int = 20_000
    max_metadata_values: int = 256
    max_structure_bytes: int = 32 * 1024 * 1024
    max_wall_seconds: int = 300

    def validate(self):
        for value in self.__dict__.values():
            if type(value) is not int or value < 1:
                raise Rejected("Limits must be positive integers")


@dataclass
class Frame:
    path: str
    nil: str
    attributes: list
    children: Counter = field(default_factory=Counter)
    sequence: list = field(default_factory=list)
    text_chars: int = 0
    text_nonblank: bool = False


def profile(source, *, limits=Limits(), mode="unknown", mode_evidence=None):
    limits.validate()
    if mode not in {"FULL", "COU", "unknown"}:
        raise Rejected("Invalid selected delivery mode")
    if mode != "unknown" and mode_evidence is None:
        raise Rejected("Known delivery mode requires checked evidence")
    started = time.monotonic()
    source = no_links(source)
    paths, attributes, patterns = {}, {}, {}
    frames, root_namespaces, schema_locations = [], [], []
    counters = Counter()
    digest = hashlib.sha256()
    parser = expat.ParserCreate(namespace_separator="}")
    parser.ordered_attributes = True
    parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)

    def reject_xml(*_args):
        raise Rejected("DTDs and entity declarations are forbidden")

    parser.StartDoctypeDeclHandler = reject_xml
    parser.EntityDeclHandler = reject_xml
    parser.UnparsedEntityDeclHandler = reject_xml
    parser.ExternalEntityRefHandler = reject_xml

    def deadline():
        if time.monotonic() - started > limits.max_wall_seconds:
            raise Rejected("Wall ceiling exceeded")

    def start_namespace(prefix, uri):
        if not frames:
            if len(root_namespaces) >= 256:
                raise Rejected("Namespace declaration ceiling exceeded")
            root_namespaces.append({"prefix": prefix or "", "uri": inert_reference(uri) if uri else ""})

    parser.StartNamespaceDeclHandler = start_namespace

    def observe_metadata(row, local, uri, value):
        permitted = local in {"srsName", "srsDimension", "dimension", "axisLabels",
                              "uomLabels", "uom", "codeSpace"} and (not uri or uri in GML)
        if not permitted:
            return
        if len(value.encode()) > 2048:
            raise Rejected("Semantic attribute ceiling exceeded")
        if local in {"srsName", "codeSpace", "uom"}:
            # Legacy OS GML2 uses this exact opaque CRS label. Preserve it as
            # source metadata only: no URI fetching or EPSG equivalence is implied.
            if not (local == "srsName" and value == "osgb:BNG"):
                inert_reference(value)
        elif local in {"srsDimension", "dimension"}:
            if not re.fullmatch(r"[1-9][0-9]{0,2}", value):
                raise Rejected("Invalid dimension metadata")
        elif not re.fullmatch(r"[A-Za-z0-9_.:+/-]+(?: [A-Za-z0-9_.:+/-]+)*", value):
            raise Rejected("Invalid axis or unit metadata")
        values = row["semanticValues"]
        values[value] = values.get(value, 0) + 1
        if len(values) > limits.max_metadata_values:
            raise Rejected("Semantic metadata cardinality ceiling exceeded")

    def start(name, attrs):
        deadline()
        counters["elements"] += 1
        if counters["elements"] > limits.max_elements:
            raise Rejected("Element ceiling exceeded")
        if len(frames) + 1 > limits.max_depth:
            raise Rejected("Depth ceiling exceeded")
        native = qname(name)
        path = (frames[-1].path if frames else "") + "/" + native
        if path not in paths:
            if len(paths) + len(attributes) >= limits.max_paths:
                raise Rejected("Distinct XPath ceiling exceeded")
            counters["structureBytes"] += len(path.encode())
            if counters["structureBytes"] > limits.max_structure_bytes:
                raise Rejected("Structural metadata byte ceiling exceeded")
            paths[path] = {"xpath": path, "qname": native,
                          "parentXpath": frames[-1].path if frames else None, "occurrences": 0,
                          "parentInstancesPresent": 0, "nilStates": Counter(),
                          "contentStates": Counter(), "childCardinality": {},
                          "patterns": Counter()}
        row = paths[path]
        row["occurrences"] += 1
        if frames:
            parent = frames[-1]
            parent.children[native] += 1
            parent.sequence.append({"element": native})
            if len(parent.sequence) > limits.max_sequence_items:
                raise Rejected("Per-element order sequence ceiling exceeded")
        nil, attr_order = "not-declared", []
        for i in range(0, len(attrs), 2):
            counters["attributes"] += 1
            if counters["attributes"] > limits.max_attributes:
                raise Rejected("Attribute ceiling exceeded")
            raw_name, value = attrs[i:i + 2]
            attr_name = qname(raw_name)
            uri, local = name_parts(raw_name)
            attr_order.append(attr_name)
            attr_path = path + "/@" + attr_name
            if attr_path not in attributes:
                if len(paths) + len(attributes) >= limits.max_paths:
                    raise Rejected("Distinct XPath ceiling exceeded")
                counters["structureBytes"] += len(attr_path.encode())
                if counters["structureBytes"] > limits.max_structure_bytes:
                    raise Rejected("Structural metadata byte ceiling exceeded")
            item = attributes.setdefault(attr_path, {
                "xpath": attr_path, "qname": attr_name, "ownerXpath": path, "occurrences": 0,
                "valueStates": Counter(), "semanticValues": {}, "referenceKinds": Counter()})
            item["occurrences"] += 1
            item["valueStates"]["empty" if value == "" else "whitespace" if not value.strip() else "nonempty-redacted"] += 1
            if uri == XSI and local == "nil":
                nil = "true" if value in {"true", "1"} else "false" if value in {"false", "0"} else "invalid"
            elif uri == XLINK and local == "href":
                kind = "fragment" if value.startswith("#") else "absolute" if urlsplit(value).scheme else "relative"
                item["referenceKinds"][kind] += 1
            if not frames and uri == XSI and local in {"schemaLocation", "noNamespaceSchemaLocation"}:
                tokens = value.split()
                if len(tokens) > 128 or (local == "schemaLocation" and len(tokens) % 2):
                    raise Rejected("Invalid root schema locator pairs")
                if local == "noNamespaceSchemaLocation" and len(tokens) != 1:
                    raise Rejected("Invalid root schema locator")
                schema_locations.append({"attribute": attr_name,
                                         "tokens": [inert_reference(token) for token in tokens],
                                         "retrieved": False})
            observe_metadata(item, local, uri, value)
        frames.append(Frame(path, nil, attr_order))
        counters["maxDepth"] = max(counters["maxDepth"], len(frames))

    def text(value):
        if frames and value:
            current = frames[-1]
            current.text_chars += len(value)
            current.text_nonblank = current.text_nonblank or bool(value.strip())
            if current.sequence and "text" in current.sequence[-1]:
                token = current.sequence[-1]
                token["text"] = token["text"] or bool(value.strip())
            else:
                current.sequence.append({"text": bool(value.strip())})
            if len(current.sequence) > limits.max_sequence_items:
                raise Rejected("Per-element order sequence ceiling exceeded")

    def end(_name):
        current = frames.pop()
        row = paths[current.path]
        row["nilStates"][current.nil] += 1
        state = ("mixed-content-redacted" if current.children and current.text_nonblank else
                 "children" if current.children else "text-redacted" if current.text_nonblank else
                 "whitespace-only" if current.text_chars else "empty")
        row["contentStates"][state] += 1
        for child, count in current.children.items():
            child_path = current.path + "/" + child
            paths[child_path]["parentInstancesPresent"] += 1
            histogram = row["childCardinality"].setdefault(child, Counter())
            histogram[str(count)] += 1
        pattern = {"attributeOrder": current.attributes, "contentOrder": current.sequence}
        pattern_raw = canonical(pattern)
        identity = sha(pattern_raw)
        if identity not in patterns and len(patterns) >= limits.max_patterns:
            raise Rejected("Structural pattern ceiling exceeded")
        if identity not in patterns:
            counters["structureBytes"] += len(pattern_raw)
            if counters["structureBytes"] > limits.max_structure_bytes:
                raise Rejected("Structural metadata byte ceiling exceeded")
        patterns[identity] = pattern
        row["patterns"][identity] += 1

    parser.StartElementHandler = start
    parser.CharacterDataHandler = text
    parser.EndElementHandler = end
    descriptor = os.open(source, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(descriptor, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode):
            raise Rejected("Input must be a regular file")
        if before.st_size > limits.max_bytes:
            raise Rejected("Input byte ceiling exceeded")
        try:
            while raw := stream.read(65536):
                deadline()
                counters["inputBytes"] += len(raw)
                if counters["inputBytes"] > limits.max_bytes:
                    raise Rejected("Input byte ceiling exceeded")
                digest.update(raw)
                parser.Parse(raw, False)
            parser.Parse(b"", True)
        except expat.ExpatError:
            raise Rejected("Malformed XML; no complete profile") from None
        after = os.fstat(stream.fileno())
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
            after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
        raise Rejected("Input changed during processing")
    if counters["inputBytes"] != before.st_size or not paths or frames:
        raise Rejected("Incomplete XML input")
    for path, row in paths.items():
        parent = row["parentXpath"]
        denominator = paths[parent]["occurrences"] if parent else 1
        row["parentInstances"] = denominator
        row["absentParentInstances"] = denominator - row["parentInstancesPresent"] if parent else 0
        row["absenceMeaning"] = "not-seen-in-selected-parent-instances; not-schema-requiredness"
        for child, histogram in row["childCardinality"].items():
            histogram["0"] = row["occurrences"] - sum(histogram.values())
    for row in attributes.values():
        row["ownerInstances"] = paths[row["ownerXpath"]]["occurrences"]
        row["absentOwnerInstances"] = row["ownerInstances"] - row["occurrences"]
    return {
        "schema": VERSION, "scanComplete": True, "providerUniverseComplete": False,
        "inputSha256": digest.hexdigest(), "counts": dict(counters),
        "deliveryMode": {"selected": mode, "evidence": mode_evidence,
                         "inferredFromFilename": False, "couAppliedToBaseline": False},
        "rootNamespaces": root_namespaces, "rootSchemaLocations": schema_locations,
        "limits": limits.__dict__, "elements": list(paths.values()),
        "attributes": list(attributes.values()), "structuralPatterns": patterns,
        "limitations": [
            "One complete selected XML file; not complete archive, product or national coverage.",
            "No XSD validation, schema fetching, conversion, geometry computation or reference resolution.",
            "Namespace-qualified Q{} paths are XPath 3.1 EQNames; prefix spelling is not field identity.",
            "Attribute order and element/text order are source syntax, not asserted XSD semantics.",
            "Whitespace and non-whitespace text states are retained; text and feature attribute values are redacted.",
            "Comments, processing instructions and exact lexical XML are not retained.",
            "Absent states concern observed parent instances; undeclared/unseen schema fields remain unknown.",
            "COU is recorded but no baseline merge or completeness assertion is performed.",
            "Source bytes are retained; this method never disposes of raw payloads."
        ]}


def checked_evidence(spec, base):
    if not isinstance(spec, dict) or set(spec) != {"file", "sha256", "lineStart", "lineEnd"}:
        raise Rejected("Evidence needs an exact local file, digest and line interval")
    filename = spec["file"]
    if not isinstance(filename, str) or Path(filename).is_absolute() or ".." in Path(filename).parts:
        raise Rejected("Evidence path must stay within the supplied evidence directory")
    source = no_links(Path(base) / filename)
    if not source.is_relative_to(no_links(base)):
        raise Rejected("Evidence path escapes its root")
    raw = bounded_read(source, 2 * 1024 * 1024)
    if sha(raw) != spec["sha256"]:
        raise Rejected("Evidence checksum mismatch")
    try:
        lines = raw.decode("utf-8").splitlines()
    except UnicodeDecodeError:
        raise Rejected("Mapping evidence must be UTF-8 text") from None
    first, last = spec["lineStart"], spec["lineEnd"]
    if (type(first) is not int or type(last) is not int or
            not 1 <= first <= last <= len(lines) or not any(lines[first - 1:last])):
        raise Rejected("Evidence line interval is invalid")
    return {"sha256": spec["sha256"], "lineStart": first, "lineEnd": last,
            "evidenceBytesVerified": True, "meaningIndependentlyValidated": False}


def mapping_candidates(specs, snapshot, evidence_root):
    known = {row["xpath"] for row in snapshot["elements"] + snapshot["attributes"]}
    candidates = []
    for spec in specs:
        expected = {"sourceXpath", "productVersion", "targetFormat", "targetField",
                    "conversionLosses", "evidence"}
        if not isinstance(spec, dict) or set(spec) != expected:
            raise Rejected("Mapping candidate fields are closed")
        if spec["sourceXpath"] not in known:
            raise Rejected("Mapping source XPath was not observed")
        if spec["targetFormat"] not in {"GeoJSON", "GeoPackage", "CSV", "Shapefile", "GML", "unmapped"}:
            raise Rejected("Unsupported candidate target format")
        for key in ("productVersion", "targetField"):
            if not isinstance(spec[key], str) or not spec[key] or len(spec[key]) > 1024:
                raise Rejected("Invalid candidate target or product version")
        if not isinstance(spec["conversionLosses"], list) or len(spec["conversionLosses"]) > 64:
            raise Rejected("Invalid conversion loss candidates")
        if any(not isinstance(item, str) or len(item) > 2048 for item in spec["conversionLosses"]):
            raise Rejected("Conversion loss annotation ceiling exceeded")
        evidence = checked_evidence(spec["evidence"], evidence_root)
        candidates.append({**{k: v for k, v in spec.items() if k != "evidence"},
                           "evidence": evidence, "status": "source-backed-candidate",
                           "equivalence": "not-established", "conversionExecuted": False})
    return {"schema": "gis-ai-go.gml-format-mapping-candidates.v1",
            "inputSha256": snapshot["inputSha256"], "candidates": candidates,
            "missingMappingMeaning": "unassessed; not evidence of equivalence or absence",
            "automaticallyInventedMappings": 0}


def sync_directory(path):
    descriptor = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def export_bundle(output, snapshot, mappings):
    """Create a new private directory; root.json is the final completion marker.

    Every file is <=16 KiB. Interrupted output is incomplete, never overwritten.
    Exact canonical documents reconstruct through checksummed content-addressed
    parts and bounded manifest trees. No raw source bytes enter this bundle.
    """
    output = no_links(output)
    if output.exists():
        raise Rejected("Output exists; preserve it")
    if not output.parent.is_dir():
        raise Rejected("Create the private output parent first")
    output.mkdir(mode=0o700)

    def write(name, raw):
        if len(raw) > MAX_OUTPUT:
            raise Rejected("Output file exceeds 16 KiB")
        descriptor = os.open(output / name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        return {"file": name, "sha256": sha(raw), "bytes": len(raw)}

    def object_file(value):
        raw = canonical(value)
        name = sha(raw) + ".json"
        if (output / name).exists():
            if bounded_read(output / name, MAX_OUTPUT) != raw:
                raise Rejected("Content-addressed output collision")
            return {"file": name, "sha256": sha(raw), "bytes": len(raw)}
        return write(name, raw)

    def document(value):
        raw = canonical(value)
        parts = []
        for offset in range(0, len(raw), 8192):
            chunk = raw[offset:offset + 8192]
            parts.append(object_file({"schema": "gml-profile-part.v1", "offset": offset,
                                      "data": base64.b64encode(chunk).decode(),
                                      "rawSha256": sha(chunk)}))
        level = parts
        while len(level) > 48:
            level = [object_file({"schema": "gml-profile-manifest.v1",
                                  "children": level[i:i + 48]})
                     for i in range(0, len(level), 48)]
        top = object_file({"schema": "gml-profile-manifest.v1", "children": level})
        return {"root": top, "sha256": sha(raw), "bytes": len(raw)}

    cards = []
    for kind, rows in (("element", snapshot.get("elements", [])),
                       ("attribute", snapshot.get("attributes", []))):
        for row in rows:
            native_path = row["xpath"]
            identity = "urn:sha256:" + snapshot["inputSha256"] + ":field:" + sha(native_path.encode())
            card = {
                "@context": {"@vocab": "urn:gis-ai-go:gml-structural-candidate:",
                             "prov": "http://www.w3.org/ns/prov#"},
                "@id": identity, "@type": "NativeGmlStructuralFieldCandidate",
                "nativeXpath": native_path, "qname": row["qname"], "kind": kind,
                "sourceSha256": snapshot["inputSha256"],
                "prov:wasDerivedFrom": {"@id": "urn:sha256:" + snapshot["inputSha256"]},
                "deliveryModeEvidence": snapshot.get("deliveryMode", {"selected": "unknown"}),
                "versionEvidence": snapshot.get("versionEvidence", {"status": "not-established"}),
                "occurrences": row["occurrences"],
                "structuralPatternCount": len(row.get("patterns", {})),
                "patternResolution": "hash keys resolve against the reconstructed profile structuralPatterns",
                "conversionSuccess": False, "schemaValidated": False,
                "details": row}
            if len(canonical(card)) > MAX_OUTPUT:
                card.pop("details")
                card["detailsReference"] = document(row)
                card["oversizeHandling"] = "lossless per-field parts; no discarded native field metadata"
            if len(canonical(card)) > MAX_OUTPUT:
                raise Rejected("Bounded navigational field card exceeds ceiling")
            reference = object_file(card)
            cards.append({"nativeXpath": native_path, "qname": row["qname"],
                          "kind": kind, "fieldIdentity": identity, "card": reference})
    index = {"schema": "gis-ai-go.gml-native-field-card-index.v1",
             "inputSha256": snapshot["inputSha256"], "fieldCount": len(cards),
             "maxCardBytes": MAX_OUTPUT, "fields": cards}
    documents = {key: document(value) for key, value in
                 (("profile", snapshot), ("mappingCandidates", mappings),
                  ("fieldCardIndex", index))}
    sync_directory(output)
    write("candidate-root.json", canonical({"schema": "gml-profile-bundle.v1", "complete": True,
                                 "sourceSha256": snapshot["inputSha256"], "documents": documents}))
    sync_directory(output)
    # Verify the entire candidate before publishing the completion marker.
    verify_bundle(output, root_name="candidate-root.json")
    os.link(output / "candidate-root.json", output / "root.json")
    (output / "candidate-root.json").unlink()
    sync_directory(output)
    return verify_bundle(output)


def verify_bundle(output, *, root_name="root.json"):
    output = no_links(output)
    if root_name not in {"root.json", "candidate-root.json"}:
        raise Rejected("Unsupported bundle marker")
    root = json.loads(bounded_read(output / root_name, MAX_OUTPUT))
    if root.get("schema") != "gml-profile-bundle.v1" or root.get("complete") is not True:
        raise Rejected("Missing complete bundle marker")
    visited = {root_name}
    work = Counter()

    def object_value(reference, ancestry):
        work["references"] += 1
        if work["references"] > 50_000:
            raise Rejected("Manifest reference ceiling exceeded")
        name = reference["file"]
        if not FILE.fullmatch(name) or name in ancestry:
            raise Rejected("Unsafe or cyclic manifest reference")
        raw = bounded_read(output / name, MAX_OUTPUT)
        if sha(raw) != reference["sha256"] or len(raw) != reference["bytes"] or name != sha(raw) + ".json":
            raise Rejected("Bundle file checksum mismatch")
        visited.add(name)
        return name, json.loads(raw)

    def node(reference, ancestry):
        name, value = object_value(reference, ancestry)
        if value.get("schema") == "gml-profile-manifest.v1":
            if not 1 <= len(value["children"]) <= 48 or len(ancestry) >= 16:
                raise Rejected("Manifest bounds exceeded")
            return [part for child in value["children"] for part in node(child, ancestry | {name})]
        if value.get("schema") != "gml-profile-part.v1":
            raise Rejected("Unknown bundle object")
        decoded = base64.b64decode(value["data"], validate=True)
        if sha(decoded) != value["rawSha256"] or len(decoded) > 8192:
            raise Rejected("Part checksum mismatch")
        work["decodedBytes"] += len(decoded)
        if work["decodedBytes"] > 128 * 1024 * 1024:
            raise Rejected("Reconstruction byte ceiling exceeded")
        return [(value["offset"], decoded)]

    def reconstructed(descriptor):
        parts = node(descriptor["root"], set())
        result = bytearray()
        for offset, raw in parts:
            if offset != len(result):
                raise Rejected("Part order or offset mismatch")
            result.extend(raw)
        if len(result) != descriptor["bytes"] or sha(result) != descriptor["sha256"]:
            raise Rejected("Reconstructed document mismatch")
        return json.loads(result)

    decoded_documents = {name: reconstructed(descriptor)
                         for name, descriptor in root["documents"].items()}
    if set(decoded_documents) != {"profile", "mappingCandidates", "fieldCardIndex"}:
        raise Rejected("Missing profile, mapping or field-card document")
    if any(value["inputSha256"] != root["sourceSha256"] for value in decoded_documents.values()):
        raise Rejected("Source binding mismatch")
    if decoded_documents["profile"].get("scanComplete") is not True:
        raise Rejected("Profile is incomplete")
    snapshot = decoded_documents["profile"]
    expected_fields = {row["xpath"]: row for row in
                       snapshot.get("elements", []) + snapshot.get("attributes", [])}
    index = decoded_documents["fieldCardIndex"]
    if index["fieldCount"] != len(index["fields"]) or index["fieldCount"] != len(expected_fields):
        raise Rejected("Field-card denominator mismatch")
    seen_fields = set()
    for entry in index["fields"]:
        native = entry["nativeXpath"]
        if native not in expected_fields or native in seen_fields:
            raise Rejected("Unbound or duplicate field card")
        seen_fields.add(native)
        _, card = object_value(entry["card"], set())
        expected_id = "urn:sha256:" + root["sourceSha256"] + ":field:" + sha(native.encode())
        if (card.get("@id") != expected_id or entry["fieldIdentity"] != expected_id or
                card.get("sourceSha256") != root["sourceSha256"] or card.get("nativeXpath") != native or
                card.get("qname") != expected_fields[native]["qname"]):
            raise Rejected("Field-card source identity mismatch")
        expected_row = expected_fields[native]
        expected_kind = "attribute" if "ownerXpath" in expected_row else "element"
        if (card.get("@type") != "NativeGmlStructuralFieldCandidate" or
                card.get("kind") != expected_kind or entry.get("kind") != expected_kind or
                entry.get("qname") != expected_row["qname"] or
                card.get("occurrences") != expected_row["occurrences"] or
                card.get("structuralPatternCount") != len(expected_row.get("patterns", {})) or
                card.get("deliveryModeEvidence") != snapshot.get("deliveryMode", {"selected": "unknown"}) or
                card.get("versionEvidence") != snapshot.get("versionEvidence", {"status": "not-established"}) or
                card.get("prov:wasDerivedFrom") != {"@id": "urn:sha256:" + root["sourceSha256"]} or
                card.get("conversionSuccess") is not False or card.get("schemaValidated") is not False):
            raise Rejected("Field-card evidence or candidate claim mismatch")
        details = reconstructed(card["detailsReference"]) if "detailsReference" in card else card.get("details")
        if details != expected_fields[native]:
            raise Rejected("Field-card details differ from the complete profile")
    actual = set()
    for entry in output.iterdir():
        actual.add(entry.name)
        if len(actual) > 50_000:
            raise Rejected("Output file count ceiling exceeded")
    if actual != visited:
        raise Rejected("Unindexed or missing output file")
    if any(not p.is_file() or p.is_symlink() or p.stat().st_size > MAX_OUTPUT for p in output.iterdir()):
        raise Rejected("Unsafe output file")
    return {"status": "verified", "files": len(visited), "maxFileBytes": max(
        p.stat().st_size for p in output.iterdir()), "sourceSha256": root["sourceSha256"],
        "documents": decoded_documents}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-bytes", type=int, default=Limits.max_bytes)
    parser.add_argument("--max-elements", type=int, default=Limits.max_elements)
    parser.add_argument("--max-depth", type=int, default=Limits.max_depth)
    parser.add_argument("--max-wall-seconds", type=int, default=Limits.max_wall_seconds)
    parser.add_argument("--mode", choices=("FULL", "COU", "unknown"), default="unknown")
    parser.add_argument("--mode-evidence", type=Path)
    parser.add_argument("--mappings", type=Path)
    args = parser.parse_args()
    evidence = None
    if args.mode_evidence:
        evidence = checked_evidence(json.loads(bounded_read(args.mode_evidence, 65536)),
                                    args.mode_evidence.parent)
    snapshot = profile(args.source, limits=Limits(max_bytes=args.max_bytes,
                       max_elements=args.max_elements, max_depth=args.max_depth,
                       max_wall_seconds=args.max_wall_seconds),
                       mode=args.mode, mode_evidence=evidence)
    mappings = mapping_candidates(
        json.loads(bounded_read(args.mappings, 2 * 1024 * 1024)) if args.mappings else [],
        snapshot, args.mappings.parent if args.mappings else args.source.parent)
    result = export_bundle(args.output, snapshot, mappings)
    print(json.dumps({key: value for key, value in result.items() if key != "documents"}))


if __name__ == "__main__":
    main()
