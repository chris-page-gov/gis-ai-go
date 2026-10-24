"""Candidate bounded ZIP/gzip GML processing. No network, execution or disposal."""
from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import time
import unicodedata
import xml.etree.ElementTree as ET
import zipfile

from . import gml_profile as g

SCHEMA = "gis-ai-go.gml-selected-archive.v1"
OS_PRODUCT_NAMESPACE = "http://namespaces.os.uk/product/1.0"
OS_TRANSACTION_ACTIONS = {"insert", "replace", "delete"}
OS_NAMESPACES = {
    "http://www.ordnancesurvey.co.uk/xml/namespaces/osgb",
    "http://www.ordnancesurvey.co.uk/xml/namespaces/osgb/1.0",
}
DIRECT_OS_FEATURES = {
    "TopographicArea", "TopographicLine", "TopographicPoint", "CartographicText",
    "CartographicSymbol", "DepartedFeature", "RoadLink", "RoadNode", "PathLink",
    "PathNode", "Road", "Path", "ConnectingLink", "ConnectingNode",
}


@dataclass(frozen=True)
class ArchiveLimits:
    max_expanded_bytes: int = 256 * 1024 * 1024
    max_member_bytes: int = 128 * 1024 * 1024
    max_members: int = 10_000
    max_raw_bytes: int = 256 * 1024 * 1024
    max_wall_seconds: int = 600
    max_documentation_bytes: int = 2 * 1024 * 1024
    max_sequence_items: int = 20_000

    def validate(self):
        if any(type(v) is not int or v < 1 for v in self.__dict__.values()):
            raise g.Rejected("Archive limits must be positive integers")


def json_pointer(value, pointer):
    if not isinstance(pointer, str) or (pointer and not pointer.startswith("/")):
        raise g.Rejected("Invalid selection evidence pointer")
    for raw in pointer.split("/")[1:]:
        if re.search(r"~(?![01])", raw):
            raise g.Rejected("Invalid selection evidence pointer")
        part = raw.replace("~1", "/").replace("~0", "~")
        try:
            value = value[int(part)] if isinstance(value, list) and part.isdecimal() else value[part]
        except (KeyError, IndexError, TypeError, ValueError):
            raise g.Rejected("Selection evidence pointer is unresolved") from None
    return value


def hash_file(path, limit, deadline):
    path = g.no_links(path)
    descriptor = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    digest, md5, size = hashlib.sha256(), hashlib.md5(), 0
    with os.fdopen(descriptor, "rb") as stream:
        before = os.fstat(stream.fileno())
        if not stat.S_ISREG(before.st_mode) or before.st_size > limit:
            raise g.Rejected("Raw payload type or byte ceiling refused")
        while chunk := stream.read(65536):
            deadline()
            size += len(chunk)
            if size > limit:
                raise g.Rejected("Raw payload byte ceiling exceeded")
            digest.update(chunk)
            md5.update(chunk)
        after = os.fstat(stream.fileno())
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
            after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
        raise g.Rejected("Raw input changed during verification")
    return {"bytes": size, "sha256": digest.hexdigest(), "md5": md5.hexdigest()}


def checked_receipt(receipt_path, payload, limit, deadline):
    raw = g.bounded_read(receipt_path, 2 * 1024 * 1024)
    receipt = json.loads(raw)
    allowed = {"schema", "payload", "selection", "selectionEvidence", "classifications"}
    if not isinstance(receipt, dict) or not set(receipt) <= allowed:
        raise g.Rejected("Acquisition descriptor fields are closed")
    if receipt.get("schema", SCHEMA) != SCHEMA:
        raise g.Rejected("Unknown acquisition descriptor schema")
    declared = receipt["payload"]
    if not isinstance(declared, dict) or not set(declared) <= {"file", "bytes", "sha256", "md5"}:
        raise g.Rejected("Invalid payload descriptor")
    if type(declared.get("bytes")) is not int or declared["bytes"] < 1 or not g.HASH.fullmatch(declared.get("sha256", "")):
        raise g.Rejected("Invalid payload digest or byte count")
    if declared.get("file"):
        specified = Path(declared["file"])
        if not specified.is_absolute():
            specified = Path(receipt_path).parent / specified
        if g.no_links(specified) != g.no_links(payload):
            raise g.Rejected("Payload descriptor does not match selected input")
    actual = hash_file(payload, limit, deadline)
    if actual["bytes"] != declared["bytes"] or actual["sha256"] != declared["sha256"]:
        raise g.Rejected("Raw payload checksum or size mismatch")
    if declared.get("md5") is not None and declared["md5"].lower() != actual["md5"]:
        raise g.Rejected("Raw payload MD5 mismatch")
    selection = receipt["selection"]
    if (not isinstance(selection, dict) or set(selection) != {"id", "deliveryMode"} or
            any(not isinstance(v, str) or not v or len(v) > 256 for v in selection.values())):
        raise g.Rejected("Invalid selected source mode")
    evidence = receipt["selectionEvidence"]
    if not isinstance(evidence, dict) or set(evidence) != {"file", "sha256", "jsonPointer"}:
        raise g.Rejected("Selection needs hash-bound source evidence")
    evidence_path = Path(evidence["file"])
    if not evidence_path.is_absolute():
        evidence_path = Path(receipt_path).parent / evidence_path
    evidence_raw = g.bounded_read(evidence_path, 2 * 1024 * 1024)
    if g.sha(evidence_raw) != evidence["sha256"]:
        raise g.Rejected("Selection evidence checksum mismatch")
    observed = json_pointer(json.loads(evidence_raw), evidence["jsonPointer"])
    if not isinstance(observed, dict) or any(observed.get(k) != v for k, v in selection.items()):
        raise g.Rejected("Selection evidence does not bind the selected mode")
    mode = {"FULL": "FULL", "Full": "FULL", "COU": "COU", "COU_FEATURES": "COU"}.get(
        selection["deliveryMode"], "unknown")
    bound = {"sha256": evidence["sha256"], "jsonPointer": evidence["jsonPointer"],
             "nativeDeliveryMode": selection["deliveryMode"], "labelNormalisedTo": mode,
             "normalisationStatus": "source-label-candidate",
             "evidenceBytesVerified": True, "meaningIndependentlyValidated": False}
    native_version = observed.get("productVersion")
    version_evidence = {"status": "not-established"}
    if isinstance(native_version, str) and 0 < len(native_version) <= 1024:
        version_evidence = {"status": "source-declared-candidate", "nativeProductVersion": native_version,
                            "sourceSha256": evidence["sha256"],
                            "jsonPointer": evidence["jsonPointer"] + "/productVersion",
                            "versionSemanticsIndependentlyValidated": False}
    return {"descriptorSha256": g.sha(raw), "payload": actual,
            "selection": selection, "mode": mode, "modeEvidence": bound,
            "versionEvidence": version_evidence,
            "classifications": receipt.get("classifications", [])}


def safe_zip_inventory(archive, limits):
    entries = archive.infolist()
    if not entries or len(entries) > limits.max_members:
        raise g.Rejected("ZIP member count is empty or exceeds ceiling")
    nodes, explicit, total, result = {}, set(), 0, []
    for item in entries:
        name = item.filename
        if (not name or "\x00" in item.orig_filename or "\\" in name or
                name.startswith("/") or any(ord(c) < 32 for c in name)):
            raise g.Rejected("Unsafe ZIP member path")
        directory = item.is_dir()
        clean = name[:-1] if directory else name
        parts = clean.split("/")
        if any(part in {"", ".", ".."} or ":" in part or part.endswith((" ", ".")) for part in parts):
            raise g.Rejected("Unsafe ZIP member component")
        if len(name.encode()) > 4096 or len(parts) > 128:
            raise g.Rejected("ZIP path ceiling exceeded")
        if name in explicit:
            raise g.Rejected("Duplicate ZIP member path")
        explicit.add(name)
        mode = (item.external_attr >> 16) & 0xFFFF
        file_type = stat.S_IFMT(mode)
        expected = stat.S_IFDIR if directory else stat.S_IFREG
        if file_type not in (0, expected) or item.flag_bits & 1:
            raise g.Rejected("ZIP links, special types or encryption are refused")
        if (item.external_attr & 0x10) and not directory:
            raise g.Rejected("Contradictory ZIP directory attributes")
        if directory and item.file_size:
            raise g.Rejected("ZIP directory has payload bytes")
        if directory and item.CRC:
            raise g.Rejected("ZIP directory CRC is inconsistent")
        for i in range(1, len(parts) + 1):
            spelling = "/".join(parts[:i])
            key = unicodedata.normalize("NFC", spelling).casefold()
            kind = "directory" if i < len(parts) or directory else "file"
            prior = nodes.get(key)
            if prior and (prior["spelling"] != spelling or prior["kind"] != kind):
                raise g.Rejected("ZIP case, Unicode or implicit-directory collision")
            nodes[key] = {"spelling": spelling, "kind": kind}
        if not directory:
            if item.file_size < 0 or item.file_size > limits.max_member_bytes:
                raise g.Rejected("ZIP member expanded byte ceiling exceeded")
            total += item.file_size
            if total > limits.max_expanded_bytes:
                raise g.Rejected("ZIP expanded byte ceiling exceeded")
        result.append(item)
    return result


def split_tag(tag):
    if tag.startswith("{"):
        uri, local = tag[1:].split("}", 1)
        return uri, local
    return "", tag


def feature_count(path, deadline):
    """Independent ElementTree pass after Expat acceptance; no feature values."""
    stack, counts, membership, unclassified = [], Counter(), Counter(), Counter()
    total, root_children = 0, Counter()
    action_counts, action_children = Counter(), {}
    for event, element in ET.iterparse(path, events=("start", "end")):
        deadline()
        if event == "start":
            total += 1
            uri, local = split_tag(element.tag)
            if stack:
                parent_uri, parent_local = split_tag(stack[-1].tag)
                product_transaction = split_tag(stack[0].tag) == (OS_PRODUCT_NAMESPACE, "Transaction")
                if len(stack) == 1:
                    root_children[element.tag] += 1
                    if product_transaction and uri == OS_PRODUCT_NAMESPACE and local in OS_TRANSACTION_ACTIONS:
                        action_counts[element.tag] += 1
                if (len(stack) == 2 and product_transaction and parent_uri == OS_PRODUCT_NAMESPACE and
                        parent_local in OS_TRANSACTION_ACTIONS):
                    action_children.setdefault(stack[-1].tag, Counter())[element.tag] += 1
                generic = parent_uri in g.GML and parent_local in {"featureMember", "featureMembers"}
                os_member = parent_uri in OS_NAMESPACES and (
                    parent_local in {"featureMember", "featureMembers"} or parent_local.endswith("Member"))
                if generic or os_member:
                    counts[element.tag] += 1
                    membership[stack[-1].tag] += 1
                elif len(stack) == 1 and uri in OS_NAMESPACES and local in DIRECT_OS_FEATURES:
                    counts[element.tag] += 1
                    membership["direct-os-feature-child"] += 1
            stack.append(element)
        else:
            uri, local = split_tag(element.tag)
            is_transaction_action = (len(stack) == 2 and split_tag(stack[0].tag) ==
                                     (OS_PRODUCT_NAMESPACE, "Transaction") and uri == OS_PRODUCT_NAMESPACE and
                                     local in OS_TRANSACTION_ACTIONS)
            if len(stack) == 2 and not is_transaction_action and local not in {"boundedBy", "description", "name", "metaDataProperty",
                                               "featureMember", "featureMembers"}:
                if not ((uri in OS_NAMESPACES and (local.endswith("Member") or local in DIRECT_OS_FEATURES))):
                    unclassified[element.tag] += 1
            stack.pop()
            element.clear()
    return {"method": "independent-ElementTree-membership-pass.v1", "elementsTraversed": total,
            "featureElements": sum(counts.values()), "featureElementQNames": dict(counts),
            "membershipRoutes": dict(membership), "rootChildQNames": dict(root_children),
            "transactionActionCounts": dict(action_counts),
            "transactionActionChildElements": sum(sum(rows.values()) for rows in action_children.values()),
            "transactionActionChildQNames": {action: dict(rows) for action, rows in action_children.items()},
            "transactionCountMeaning": "exact OS product Transaction actions and direct child candidates; not validated features",
            "unclassifiedRootChildQNames": dict(unclassified), "conversionSuccess": False,
            "schemaValidated": False, "nativeFeatureCountSemantics": "candidate-membership-count",
            "limitations": ["Feature references without local child elements are not resolved or counted.",
                           "FULL/COU relationships, removed features and baseline application are not validated.",
                           "A feature-element count is not conversion success or product completeness.",
                           "Transaction action children are counted separately; empty actions and delete/reference semantics remain unresolved."]}


def process(receipt_path, payload, work_dir, output, *, limits=ArchiveLimits()):
    limits.validate()
    started = time.monotonic()

    def deadline():
        if time.monotonic() - started > limits.max_wall_seconds:
            raise g.Rejected("Archive wall ceiling exceeded")

    receipt_path, payload = g.no_links(receipt_path), g.no_links(payload)
    work_dir, output = g.no_links(work_dir), g.no_links(output)
    if work_dir == output or work_dir.is_relative_to(output) or output.is_relative_to(work_dir):
        raise g.Rejected("Transient work and retained output must be separate")
    if any(p.exists() or not p.parent.is_dir() for p in (work_dir, output)):
        raise g.Rejected("Fresh work/output directories with existing parents are required")
    admitted = checked_receipt(receipt_path, payload, limits.max_raw_bytes, deadline)
    with payload.open("rb") as stream:
        magic = stream.read(4)
    archive_type = "zip" if magic[:2] == b"PK" else "gzip" if magic[:2] == b"\x1f\x8b" else None
    if archive_type is None:
        raise g.Rejected("Only ZIP or gzip magic is admitted")
    classifications = {}
    for item in admitted["classifications"]:
        if (not isinstance(item, dict) or set(item) != {"path", "kind", "sha256"} or
                item["kind"] not in {"documentation", "schema"} or
                not isinstance(item["path"], str) or not g.HASH.fullmatch(item.get("sha256", "")) or
                item["path"] in classifications):
            raise g.Rejected("Invalid explicit non-XML member classification")
        classifications[item["path"]] = item
    archive, inventory = None, None
    if archive_type == "zip":
        archive = zipfile.ZipFile(payload)
        try:
            inventory = safe_zip_inventory(archive, limits)
        except Exception:
            archive.close()
            raise
    work_dir.mkdir(mode=0o700)
    output.mkdir(mode=0o700)
    (output / "profiles").mkdir(mode=0o700)
    expanded, extracted, profiles, used_classifications = 0, [], [], set()

    def persist_json(path, value):
        raw = g.canonical(value)
        if len(raw) > g.MAX_OUTPUT:
            raise g.Rejected("Completion metadata exceeds 16 KiB")
        descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(raw)
            stream.flush()
            os.fsync(stream.fileno())
        g.sync_directory(path.parent)

    def copy_member(source, label, layer, declared_size=None):
        nonlocal expanded
        deadline()
        if len(extracted) >= limits.max_members:
            raise g.Rejected("Expanded member count ceiling exceeded")
        index = len(extracted)
        target = work_dir / f"member-{index:05d}.bin"
        digest, size = hashlib.sha256(), 0
        descriptor = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(descriptor, "wb") as out:
            while raw := source.read(65536):
                deadline()
                size += len(raw)
                expanded += len(raw)
                if size > limits.max_member_bytes or expanded > limits.max_expanded_bytes:
                    raise g.Rejected("Expanded member byte ceiling exceeded")
                digest.update(raw)
                out.write(raw)
            out.flush()
            os.fsync(out.fileno())
        if declared_size is not None and size != declared_size:
            raise g.Rejected("ZIP member byte count mismatch")
        row = {"index": index, "memberPath": label, "layer": layer, "bytes": size,
               "sha256": digest.hexdigest(), "transientFile": target.name}
        extracted.append(row)
        return target, row

    def classify_and_profile(target, row):
        deadline()
        with target.open("rb") as stream:
            first = stream.read(128)
        if first.startswith(b"\x1f\x8b"):
            if row["layer"] != "zip":
                raise g.Rejected("Only one gzip layer inside ZIP is admitted")
            with gzip.open(target, "rb") as source:
                child, child_row = copy_member(source, row["memberPath"] + "::gzip", "gzip-in-zip")
            row["processing"] = "gzip-container-fully-verified"
            row["gzipTrailerVerified"] = True
            classify_and_profile(child, child_row)
            return
        # XML parsing, rather than a file extension, establishes XML acceptance.
        xml_like = first.lstrip().startswith(b"<") or first.startswith(
            (b"\xef\xbb\xbf", b"\xff\xfe", b"\xfe\xff", b"\x00<"))
        if not xml_like:
            classification = classifications.get(row["memberPath"])
            if not classification or classification["sha256"] != row["sha256"]:
                raise g.Rejected("Non-XML member lacks explicit hash-bound classification")
            if row["bytes"] > limits.max_documentation_bytes:
                raise g.Rejected("Retained documentation/schema byte ceiling exceeded")
            try:
                g.bounded_read(target, limits.max_documentation_bytes).decode("utf-8")
            except UnicodeDecodeError:
                raise g.Rejected("Classified documentation/schema is not UTF-8") from None
            row["processing"] = "retained-bounded-" + classification["kind"]
            row["retentionVerified"] = True
            used_classifications.add(row["memberPath"])
            return
        remaining = int(limits.max_wall_seconds - (time.monotonic() - started))
        if remaining < 1:
            raise g.Rejected("Archive wall ceiling exceeded")
        snapshot = g.profile(target, limits=g.Limits(
            max_bytes=limits.max_member_bytes, max_wall_seconds=remaining,
            max_sequence_items=limits.max_sequence_items),
            mode=admitted["mode"], mode_evidence=admitted["modeEvidence"])
        if snapshot["inputSha256"] != row["sha256"] or snapshot["counts"]["inputBytes"] != row["bytes"]:
            raise g.Rejected("Profile input binding mismatch")
        snapshot["versionEvidence"] = admitted["versionEvidence"]
        independently_counted = feature_count(target, deadline)
        if independently_counted["elementsTraversed"] != snapshot["counts"]["elements"]:
            raise g.Rejected("Independent XML traversal count disagrees")
        profile_path = output / "profiles" / f"member-{row['index']:05d}"
        maps = g.mapping_candidates([], snapshot, work_dir)
        result = g.export_bundle(profile_path, snapshot, maps)
        if result["sourceSha256"] != row["sha256"]:
            raise g.Rejected("Verified profile source binding mismatch")
        root_raw = g.bounded_read(profile_path / "root.json", g.MAX_OUTPUT)
        profiles.append({"memberIndex": row["index"], "profilePath": profile_path.relative_to(output).as_posix(),
                         "rootSha256": g.sha(root_raw), "files": result["files"],
                         "maximumFileBytes": result["maxFileBytes"],
                         "independentFeatureCount": independently_counted})
        row["processing"] = "complete-structural-profile-verified"
        row["conversionSuccess"] = False

    try:
        if archive_type == "zip":
            for entry in inventory:
                deadline()
                if entry.is_dir():
                    if len(extracted) >= limits.max_members:
                        raise g.Rejected("Expanded member count ceiling exceeded")
                    extracted.append({"index": len(extracted), "memberPath": entry.filename,
                                      "layer": "zip", "type": "directory", "bytes": 0,
                                      "sha256": g.sha(b""), "processing": "directory-only"})
                    continue
                with archive.open(entry, "r") as member:
                    target, row = copy_member(member, entry.filename, "zip", entry.file_size)
                row.update(crc32=f"{entry.CRC:08x}", crcVerified=True,
                           compressedBytes=entry.compress_size)
                classify_and_profile(target, row)
        else:
            # gzip.open verifies CRC, size trailer and all concatenated members.
            # Header filenames are deliberately not trusted as filesystem paths.
            with gzip.open(payload, "rb") as member:
                target, row = copy_member(member, "gzip-payload", "gzip")
            row["gzipTrailerVerified"] = True
            classify_and_profile(target, row)
        if used_classifications != set(classifications):
            raise g.Rejected("Unused explicit member classification")
        # Re-read the original archive after processing; detect changed source.
        final_raw = hash_file(payload, limits.max_raw_bytes, deadline)
        if final_raw != admitted["payload"]:
            raise g.Rejected("Raw payload changed during processing")
        summary = {
            "schema": "gis-ai-go.gml-archive-profile.candidate.v1",
            "scanComplete": True, "inputSha256": admitted["payload"]["sha256"],
            "archiveType": archive_type, "selection": admitted["selection"],
            "selectionEvidence": admitted["modeEvidence"],
            "versionEvidence": admitted["versionEvidence"],
            "acquisitionDescriptorSha256": admitted["descriptorSha256"],
            "rawPayload": admitted["payload"], "expandedBytesCounted": expanded,
            "limits": limits.__dict__, "members": extracted, "profiles": profiles,
            "rawPayloadDisposed": False, "transientMembersDisposed": False,
            "conversionSuccess": False, "schemaMappingComplete": False,
            "completeProcessingMeaning": "all admitted members structurally processed or explicitly retained",
            "limitations": ["No network, executable invocation, conversion or raw disposal.",
                           "XSD dependency closure and source/target mapping completeness remain separate.",
                           "One selected archive is not full product, PSGA or national coverage.",
                           "gzip CRC/trailer integrity does not independently authenticate source origin.",
                           "gzip header filenames are ignored; concatenated streams parse as one XML document."]}
        maps = {"schema": "gis-ai-go.gml-archive-mapping-status.v1",
                "inputSha256": summary["inputSha256"], "candidates": [],
                "status": "unassessed", "conversionExecuted": False}
        g.export_bundle(output / "summary", summary, maps)
        verification = verify_archive(output, work_dir)
        root_raw = g.bounded_read(output / "summary" / "root.json", g.MAX_OUTPUT)
        persist_json(output / "complete.json", {
            "schema": "gis-ai-go.gml-archive-completion.candidate.v1",
            "complete": True, "summaryRootSha256": g.sha(root_raw),
            "inputSha256": summary["inputSha256"], "conversionSuccess": False,
            "rawPayloadDisposed": False, "schemaMappingComplete": False})
        return verification
    except Exception as error:
        persist_json(output / "failure.json", {
            "schema": "gis-ai-go.gml-archive-failure.candidate.v1", "complete": False,
            "errorType": type(error).__name__, "message": str(error) if isinstance(error, g.Rejected) else "Processing failed",
            "membersFinished": len(extracted), "expandedBytesCounted": expanded,
            "rawPayloadDisposed": False, "transientMembersDisposed": False})
        raise
    finally:
        if archive is not None:
            archive.close()


def verify_archive(output, work_dir, require_completion=False):
    output, work_dir = g.no_links(output), g.no_links(work_dir)
    result = g.verify_bundle(output / "summary")
    summary = result["documents"]["profile"]
    if summary.get("schema") != "gis-ai-go.gml-archive-profile.candidate.v1":
        raise g.Rejected("Unsupported archive profile")
    if any(summary.get(key) is not False for key in
           ("rawPayloadDisposed", "transientMembersDisposed", "conversionSuccess", "schemaMappingComplete")):
        raise g.Rejected("Archive summary overstates processing authority")
    if len(summary["members"]) > summary["limits"]["max_members"]:
        raise g.Rejected("Retained member count exceeds admitted ceiling")
    deadline = lambda: None
    for member in summary["members"]:
        if member.get("type") == "directory":
            continue
        name = member["transientFile"]
        if not re.fullmatch(r"member-[0-9]{5}\.bin", name):
            raise g.Rejected("Unsafe retained transient reference")
        actual = hash_file(work_dir / name, summary["limits"]["max_member_bytes"], deadline)
        if any(actual[k] != member[k] for k in ("bytes", "sha256")):
            raise g.Rejected("Retained transient member integrity mismatch")
    for child in summary["profiles"]:
        path = child["profilePath"]
        if not re.fullmatch(r"profiles/member-[0-9]{5}", path):
            raise g.Rejected("Unsafe retained profile reference")
        raw = g.bounded_read(output / path / "root.json", g.MAX_OUTPUT)
        if g.sha(raw) != child["rootSha256"]:
            raise g.Rejected("Profile root checksum mismatch")
        verified = g.verify_bundle(output / path)
        member = summary["members"][child["memberIndex"]]
        if verified["sourceSha256"] != member["sha256"]:
            raise g.Rejected("Profile member binding mismatch")
    if require_completion:
        marker = json.loads(g.bounded_read(output / "complete.json", g.MAX_OUTPUT))
        root_hash = g.sha(g.bounded_read(output / "summary" / "root.json", g.MAX_OUTPUT))
        expected_keys = {"schema", "complete", "summaryRootSha256", "inputSha256",
                         "conversionSuccess", "rawPayloadDisposed", "schemaMappingComplete"}
        if (not isinstance(marker, dict) or set(marker) != expected_keys or
                marker.get("schema") != "gis-ai-go.gml-archive-completion.candidate.v1" or
                any(marker.get(key) is not False for key in
                    ("conversionSuccess", "rawPayloadDisposed", "schemaMappingComplete")) or
                marker.get("complete") is not True or marker["summaryRootSha256"] != root_hash or
                marker["inputSha256"] != summary["inputSha256"]):
            raise g.Rejected("Archive completion marker mismatch")
        if (output / "failure.json").exists():
            raise g.Rejected("Archive retains a failed processing record")
    return {"status": "verified", "inputSha256": summary["inputSha256"],
            "archiveMembersIncludingNested": len(summary["members"]),
            "xmlProfiles": len(summary["profiles"]),
            "independentFeatureElements": sum(p["independentFeatureCount"]["featureElements"]
                                             for p in summary["profiles"]),
            "independentTransactionActionChildren": sum(
                p["independentFeatureCount"]["transactionActionChildElements"] for p in summary["profiles"]),
            "rawPayloadDisposed": False, "conversionSuccess": False,
            "schemaMappingComplete": False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--payload", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--max-sequence-items", type=int, default=ArchiveLimits.max_sequence_items,
                        help="explicit per-element order-item ceiling; default 20000")
    args = parser.parse_args()
    if args.max_sequence_items < 1:
        parser.error("--max-sequence-items must be a positive integer")
    print(json.dumps(process(args.receipt, args.payload, args.work_dir, args.output,
                            limits=ArchiveLimits(max_sequence_items=args.max_sequence_items))))


if __name__ == "__main__":
    main()
