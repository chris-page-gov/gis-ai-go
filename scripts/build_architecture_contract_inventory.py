#!/usr/bin/env python3
"""Build a reproducible, source-linked contract register from one Git commit.

This is a documentation inventory, not a validator or a reachability proof. Literal
references and declarations are retained as evidence; they are not called runtime
validation unless the reviewed narrative establishes that relationship.
"""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "97bc45635a91064cd78f06bf0848ad7636f05439"
GIT_URL = "https://github.com/chris-page-gov/gis-ai-go/blob/"
TEXT_SUFFIXES = {".ts", ".tsx", ".py", ".mjs", ".js", ".json", ".sql", ".yaml", ".yml"}


def git(*args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=ROOT)


def read_sources(commit: str) -> dict[str, str]:
    paths = git("ls-tree", "-r", "--name-only", commit).decode().splitlines()
    selected = [p for p in paths if Path(p).suffix in TEXT_SUFFIXES
                and not p.startswith(("docs/", "okf-plus/records/", "okf-plus/snapshots/"))
                and p != "pnpm-lock.yaml"]
    # One batch process reads immutable blobs. Concurrent worktree edits cannot
    # silently change either an inventory entry or its Git line reference.
    process = subprocess.run(["git", "cat-file", "--batch"], cwd=ROOT,
                             input="".join(f"{commit}:{p}\n" for p in selected).encode(),
                             stdout=subprocess.PIPE, check=True)
    output = process.stdout
    position = 0
    sources: dict[str, str] = {}
    for path in selected:
        end = output.index(b"\n", position)
        size = int(output[position:end].split()[-1])
        position = end + 1
        blob = output[position:position + size]
        position += size + 1
        try:
            sources[path] = blob.decode("utf-8")
        except UnicodeDecodeError:
            continue
    return sources


def location(commit: str, path: str, line: int = 1) -> dict:
    return {"path": path, "line": line,
            "git_url": f"{GIT_URL}{commit}/{quote(path, safe='/')}#L{line}"}


def kind(path: str) -> str:
    if "/test/" in path or "/tests/" in path or path.startswith("tests/"):
        return "test-or-fixture"
    if "fixture" in path or "example" in path:
        return "example-or-fixture"
    if path.startswith("schemas/") or "/schemas/" in path or "/schema/" in path:
        return "schema-reference"
    if path.startswith("scripts/"):
        return "build-or-assurance-code"
    if "/src/" in path:
        return "runtime-source"
    return "configuration-or-evidence"


def provenance(path: str) -> str:
    return "pinned-vendored-dependency" if path.startswith("okf-plus/vendor/") else "project-authored"


def lifecycle(path: str) -> str:
    name = Path(path).name
    if path.startswith("okf-plus/vendor/"):
        return "vendored-profile"
    if path.startswith("okf-plus/"):
        return "metadata-build"
    if path.startswith("packages/experience-intake/"):
        return "local-experimental"
    if name in {"authority-context.schema.json", "policy-decision.schema.json",
                "provider.schema.json", "tool-profile.schema.json", "workflow-profile.schema.json",
                "decision.schema.json"}:
        return "promoted-governance-definition"
    if name == "evidence-inspect-operation-result.schema.json":
        return "retained-compatibility"
    if name.startswith(("deployment-", "deployed-", "remote-https-")):
        return "planned-deployment-assurance"
    if name.startswith(("qual-206-", "gateway-", "local-edition-", "provider-live-probe",
                        "provider-adapter-preflight", "sites-mcp-evaluation")):
        return "assurance"
    if name.startswith(("evidence-checkpoint-", "evidence-external-", "evidence-filesystem-")):
        return "operator-local"
    if name.startswith("execution-"):
        return "private-synthetic"
    if name == "okf-publication-bundle.schema.json":
        return "metadata-build"
    return "local-candidate-runtime"


def strings(value, key: str):
    if isinstance(value, dict):
        for name, child in value.items():
            if name == key and isinstance(child, str):
                yield child
            yield from strings(child, key)
    elif isinstance(value, list):
        for child in value:
            yield from strings(child, key)


def build(commit: str) -> dict:
    sources = read_sources(commit)
    schema_paths = [p for p in sources if p.endswith(".schema.json")]
    references = defaultdict(list)
    schemas = []
    tokens = defaultdict(set)
    for path in schema_paths:
        schema = json.loads(sources[path])
        candidates = {Path(path).name, schema.get("$id", "")}
        candidates.update(s for s in strings(schema.get("properties", {}).get("schema", {}), "const"))
        for token in candidates - {""}:
            tokens[token].add(path)
    matcher = re.compile("|".join(re.escape(token) for token in sorted(tokens, key=len, reverse=True)))
    markers = ("schema", "gis-ai-go", "okf-")
    # The bulk metadata snapshots contain millions of lines with no contract
    # identity. Keep the full scan, but avoid a large alternation on those lines.
    # Fail explicitly if a future identity escapes the fast prefilter.
    if any(not any(marker in token for marker in markers) for token in tokens):
        raise ValueError("A schema identity needs a new reference prefilter marker")
    for path, source in sources.items():
        for number, line in enumerate(source.splitlines(), 1):
            if not any(marker in line for marker in markers):
                continue
            matched = set()
            for match in matcher.finditer(line):
                matched.update(tokens[match.group()])
            for schema_path in sorted(matched - {path}):
                references[schema_path].append({**location(commit, path, number), "kind": kind(path)})
    for path in sorted(schema_paths):
        schema = json.loads(sources[path])
        evidence = references[path]
        schemas.append({"id": schema.get("$id"), "title": schema.get("title", Path(path).name),
                        "description": schema.get("description", ""), "dialect": schema.get("$schema"),
                        "lifecycle": lifecycle(path), "provenance": provenance(path), "source": location(commit, path),
                        "source_sha256": hashlib.sha256(sources[path].encode()).hexdigest(),
                        "type": schema.get("type", "composition-or-constant"),
                        "required": schema.get("required", []),
                        "additional_properties": schema.get("additionalProperties", "unspecified"),
                        "refs": sorted(set(strings(schema, "$ref"))),
                        "literal_references": evidence,
                        "reference_counts": dict(sorted(Counter(r["kind"] for r in evidence).items())),
                        "generic_catalogue_validator": location(commit, "scripts/validate_contracts.py", 182)
                        if path.startswith("schemas/") else None})
    declarations = []
    for path, source in sorted(sources.items()):
        if "/src/" not in path or Path(path).suffix not in {".ts", ".tsx"}:
            continue
        for match in re.finditer(r"^export\s+(?:declare\s+)?(interface|type)\s+(\w+)", source, re.M):
            declarations.append({"symbol": match[2], "kind": "typescript-" + match[1],
                                 "provenance": provenance(path),
                                 "source": location(commit, path, source.count("\n", 0, match.start()) + 1),
                                 "enforcement": "compile-time-only; see runtime boundary narrative"})
    dataclasses = []
    for path, source in sorted(sources.items()):
        if not path.endswith(".py") or kind(path) in {"test-or-fixture", "example-or-fixture"}:
            continue
        if "@dataclass" not in source:
            continue
        tree = ast.parse(source, filename=path)
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and any(
                "dataclass" in ast.unparse(d) for d in node.decorator_list
            ):
                dataclasses.append({"symbol": node.name, "source": location(commit, path, node.lineno),
                                    "purpose": ast.get_docstring(node) or "Internal typed state or result carrier; inspect callers.",
                                    "enforcement": "dataclass fields do not validate untrusted input"})
    embedded = []
    for path, source in sorted(sources.items()):
        if "/src/" not in path or Path(path).suffix not in {".ts", ".tsx"}:
            continue
        for number, line in enumerate(source.splitlines(), 1):
            if re.search(r"(?:const\s+\w*(?:SCHEMAS|INPUTS|Schema)\b|inputSchema\s*:|schema:\s*closed\()", line):
                embedded.append({"source": location(commit, path, number), "provenance": provenance(path),
                                 "declaration": line.strip(),
                                 "status": "schema definition or registration reference; not independently proven validation"})
    template_path = "apps/mcp-gateway/openapi/catalogue-api.openapi.json"
    template = json.loads(sources[template_path])
    openapi = {"source": location(commit, template_path), "version": template["openapi"],
               "routes": [{"path": route, "method": method, "operation_id": op.get("operationId")}
                          for route, methods in template.get("paths", {}).items()
                          for method, op in methods.items() if method in {"get", "post", "put", "delete"}],
               "projection": location(commit, "apps/mcp-gateway/src/openapi.ts", 51),
               "private_execution_projection": location(commit, "services/geo-execution/src/gis_ai_go_execution/http.py", 65)}
    digest_path = "schemas/qual-206-exact-five-tool-schema-digests.v1.json"
    sql_path = "sites/private-pilot/drizzle/0001_sites_pilot.sql"
    authored_declarations = sum(d["provenance"] == "project-authored" for d in declarations)
    vendored_declaring_modules = {d["source"]["path"] for d in declarations
                                 if d["provenance"] == "pinned-vendored-dependency"}
    vendored_source_files = sum(provenance(path) == "pinned-vendored-dependency"
                                and "/src/" in path and Path(path).suffix in {".ts", ".tsx"}
                                for path in sources)
    return {"inventory_version": 1, "baseline_commit": commit,
            "method": "Immutable Git blobs; all maintained *.schema.json files outside preserved research; literal name/id/discriminator references; exported TypeScript interface/type declarations in project-authored and pinned-vendored src, with provenance; non-test Python dataclasses; embedded schema declarations/registrations; separately listed SQL constraints and schema-digest reference data. Literal use is not execution reachability.",
            "coverage": {"scanned_text_files": len(sources), "json_schemas": len(schemas),
                         "root_json_schemas": sum(s["source"]["path"].startswith("schemas/") for s in schemas),
                         "typescript_declarations": len(declarations), "python_dataclasses": len(dataclasses),
                         "typescript_authored_declarations": authored_declarations,
                         "typescript_vendored_declarations": len(declarations) - authored_declarations,
                         "typescript_vendored_declaring_modules": len(vendored_declaring_modules),
                         "typescript_vendored_source_files": vendored_source_files,
                         "embedded_schema_sites": len(embedded)},
            "schemas": schemas, "openapi": openapi,
            "non_schema_contract_assets": [{"source": location(commit, digest_path),
                                            "kind": "schema-digest-reference-data",
                                            "purpose": "Pinned advertised-tool schema digests; data used by conformance checks, not JSON Schema."},
                                           {"source": location(commit, sql_path, 2), "kind": "sql-storage-constraints",
                                            "source_sha256": hashlib.sha256(sources[sql_path].encode()).hexdigest(),
                                            "purpose": "Private pilot tables: provider primary key; enabled in {0,1}; non-negative used/window_used; maximum between 1 and 200; receipt primary key and result JSON at most 65,536 stored bytes. Reapplying seeds uses ON CONFLICT DO NOTHING. Atomic admission code separately enforces used < maximum and receipt/rate ceilings.",
                                            "related_contracts": [location(commit, "sites/private-pilot/db/sites-pilot-schema.ts", 6),
                                                                  location(commit, "apps/mcp-gateway/src/sites-pilot-store.ts", 11),
                                                                  location(commit, "apps/mcp-gateway/src/sites-pilot-store.ts", 21)]}],
            "typescript_declarations": declarations, "python_dataclasses": dataclasses,
            "embedded_schema_sites": embedded}


def link(loc: dict, label: str | None = None) -> str:
    return f"[{label or loc['path'] + ':' + str(loc['line'])}]({loc['git_url']})"


def markdown(inventory: dict) -> str:
    counts = inventory["coverage"]
    output = ["# Contract register", "", f"Baseline: `{inventory['baseline_commit']}`.", "",
              "Generated by `python scripts/build_architecture_contract_inventory.py`. "
              "Read [Contracts explained](CONTRACTS.md) for usage, validators and examples. "
              "[contracts.json](contracts.json) contains every literal reference and declaration; "
              "the tables below show one representative reference per category to stay readable.", "",
              f"Coverage: **{counts['root_json_schemas']} root JSON Schemas**, "
              f"**{counts['json_schemas'] - counts['root_json_schemas']} package/metadata/vendor JSON Schemas**, "
              f"**{counts['typescript_declarations']} exported TypeScript interface/type declarations**, "
              f"split into **{counts['typescript_authored_declarations']} project-authored** and "
              f"**{counts['typescript_vendored_declarations']} pinned-vendored dependency declarations**, "
              f"**{counts['python_dataclasses']} non-test Python dataclasses**, "
              f"**{counts['embedded_schema_sites']} embedded schema/registration sites**, and the two OpenAPI projections.", "",
              "Classification is reviewed purpose, not a deployment assertion. `local-candidate-runtime` means "
              "the contract belongs to an implemented local/candidate boundary; public registration is a separate gate. "
              "`assurance` and `planned-deployment-assurance` validate documents, not the truth of a claimed observation. "
              "`promoted-governance-definition` preserves research-derived governance metadata, not public identity authority. "
              "`retained-compatibility` is deliberately kept for older representations. "
              "A reference to a schema can be a producer, consumer, publication or validator; lexical matching alone "
              "does not distinguish these. Runtime references below are therefore candidates with line evidence. "
              "All root schemas also receive generic meta-schema checks in "
              + link(location(inventory['baseline_commit'], 'scripts/validate_contracts.py', 182)) + ". "
              "No direct runtime reference does not mean dead code: external consumers, generic loaders and "
              "offline validators can consume a contract. Preserved research-pack copies are excluded from maintained counts.", "",
              "## JSON Schema contracts", ""]
    groups = defaultdict(list)
    for schema in inventory["schemas"]:
        groups[schema["lifecycle"]].append(schema)
    for group, schemas in sorted(groups.items()):
        output += [f"### {group} ({len(schemas)})", "", "| Contract and purpose | Producer/consumer reference candidates | Assurance or example evidence |", "|---|---|---|"]
        for schema in schemas:
            refs = schema["literal_references"]
            first = {}
            for ref in refs:
                first.setdefault(ref["kind"], ref)
            runtime = first.get("runtime-source")
            candidates = [first[k] for k in ("build-or-assurance-code", "test-or-fixture", "example-or-fixture", "schema-reference", "configuration-or-evidence") if k in first]
            purpose = (schema["description"] or schema["title"]).replace("|", "\\|").replace("\n", " ")
            identifier = f"`{schema['id']}`" if schema['id'] else "No `$id`; standalone local descriptor."
            output.append(f"| {link(schema['source'], Path(schema['source']['path']).name)}<br>{identifier}<br>{purpose} | "
                          + (link(runtime) if runtime else "No direct runtime-source literal reference found.")
                          + " | " + ("<br>".join(link(r) for r in candidates) if candidates else
                                     ("Only generic catalogue validation found; inspect before retirement."
                                      if schema['generic_catalogue_validator'] else
                                      "No literal reference found; no generic validation established for this path.")) + " |")
        output.append("")
    output += ["## OpenAPI and non-schema assets", "", "| Contract | Role |", "|---|---|",
               f"| {link(inventory['openapi']['source'])} | OpenAPI {inventory['openapi']['version']} template. The published operation subset is projected by the selected assembly. |",
               f"| {link(inventory['openapi']['projection'])} | Loads canonical root schemas and assembles the public/candidate OpenAPI and MCP shapes. |",
               f"| {link(inventory['openapi']['private_execution_projection'])} | Separately builds the private synthetic execution OpenAPI document. |"]
    for asset in inventory["non_schema_contract_assets"]:
        output.append(f"| {link(asset['source'])} | {asset['purpose']} |")
        for related in asset.get("related_contracts", []):
            output.append(f"| {link(related)} | Related typed table declaration, runtime table construction or atomic admission contract for the pilot SQL asset. |")
    output += ["", "## Embedded runtime schema definitions and registrations", "",
               "These are source-level contract sites outside the root schema directory. Repeated registration sites "
               "are included so the caller can follow the actual projection. A registration does not itself prove semantic validation.", "",
               "| Site | Provenance | Definition or registration |", "|---|---|---|"]
    for site in inventory["embedded_schema_sites"]:
        declaration = site["declaration"].replace("|", "\\|").replace("`", "'")
        output.append(f"| {link(site['source'])} | {site['provenance']} | `{declaration}` |")
    output += ["", "## Exported TypeScript type contracts", "",
               "Every exported `interface` and `type` declaration in project-authored and pinned-vendored `src` files is listed, grouped by module and labelled by provenance. "
               f"The {counts['typescript_vendored_declarations']} vendored declarations occur in "
               f"{counts['typescript_vendored_declaring_modules']} declaring modules within the "
               f"{counts['typescript_vendored_source_files']}-file pinned TypeScript dependency snapshot; "
               "they describe dependency contracts and are not project-authored implementation. "
               "Aliases and internal options are included to avoid equating the schema directory with the complete contract surface. "
               "These declarations constrain checked TypeScript callers; they disappear from emitted JavaScript and do not validate JSON.", "",
               "| Module | Provenance | Type declarations (each links to its definition) |", "|---|---|---|"]
    by_module = defaultdict(list)
    for declaration in inventory["typescript_declarations"]:
        by_module[declaration["source"]["path"]].append(declaration)
    for module, declarations in by_module.items():
        output.append(f"| `{module}` | {provenance(module)} | " + ", ".join(link(d["source"], d["symbol"]) for d in declarations) + " |")
    output += ["", "## Python dataclass contracts", "",
               "Dataclasses describe internal state and typed result/error carriers. They do not enforce annotations "
               "on runtime input; the boundary validators supply that enforcement.", "",
               "| Declaration | Purpose |", "|---|---|"]
    for item in inventory["python_dataclasses"]:
        purpose = item["purpose"].replace("\n", " ").replace("|", "\\|")
        output.append(f"| {link(item['source'], item['symbol'])} | {purpose} |")
    return "\n".join(output) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", default=BASELINE)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    commit = git("rev-parse", "--verify", f"{args.commit}^{{commit}}").decode().strip()
    inventory = build(commit)
    outputs = {ROOT / "docs/architecture/contracts.json": json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
               ROOT / "docs/architecture/CONTRACT_REGISTER.md": markdown(inventory)}
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                raise SystemExit(f"Inventory differs: {path.relative_to(ROOT)}")
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
    print(json.dumps(inventory["coverage"], sort_keys=True))


if __name__ == "__main__":
    main()
