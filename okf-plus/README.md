---
{
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/operating-guide",
  "@type": ["dcterms:BibliographicResource"],
  "type": "Documentation",
  "title": "Operate the OS and ONS OKF+ module",
  "description": "Build, search and verify the metadata bundle offline, then plan bounded source refreshes with explicit provenance and permission preflight.",
  "tags": ["OKF", "operations", "metadata", "evaluation"],
  "status": "draft",
  "generated": {"by": "gis-ai-go authored module documentation"},
  "sources": [
    {"resource": "profile/README.md", "title": "OKF+ source and semantic profile"},
    {"resource": "../scripts/okf_plus/build.py", "title": "Offline bundle builder"},
    {"resource": "../scripts/okf_plus/search.py", "title": "Deterministic search and retrieval evaluation"},
    {"resource": "../docs/implementation/OKF-220_REUSE_REVIEW.md", "title": "Pinned integration and consumer review"}
  ]
}
---

# Operate the OS and ONS OKF+ module

OKF+ is a project-owned candidate extension to OKF 0.2. It describes OS, ONS,
Nomis and geospatial metadata, schemas, documentation and concepts. Start with
[index.md](index.md) for the discovery guide and common questions. The existing
supported `okf/` publication and runtime contracts remain separate.

The module builds and searches locally from retained public inputs. It introduces
no model API call, paid service or live provider invocation. Current authority is
existing included allowances only, with no chargeable overage or new paid
service. A later source refresh still needs a recorded request/byte budget and
reviewed metadata routes; a public schema does not grant access to its data.

## Authoritative inputs and generated outputs

| Location | Role | How to change it |
| --- | --- | --- |
| `source/` | Normalised public source snapshots, receipt bindings and frozen locators. | Refresh through reviewed capture/projection code; preserve original evidence and review the diff. |
| `records/` | Inspectable Markdown with JSON-shaped YAML-LD front matter. Machine-imported records derive from snapshots and importer rules; authored concepts have separate source review. | Re-capture evidence, correct importer mappings or edit the separately authored source. Preserve the provenance of imported facts. |
| `profile/`, `schemas/`, `context.jsonld` | Project profile, source-family register, standards mappings and local contracts. | Review semantic and compatibility changes explicitly. Namespace use is not a conformance certificate. |
| `evaluation/questions.json` | Authored questions, retrieval targets, literal checks and separate interpretation boundaries. | Add or revise cases with source evidence; record changed expectations. |
| `vendor/` | Pinned consumer contracts and code needed for independent local compatibility checks. | Update the reviewed version and integrity manifest together. |
| `artifacts/okf-plus/` at repository root | Ignored raw acquisition evidence and generated bundles, context projections and reports. | Regenerate. Never hand-edit a generated result to make an assertion or test pass. |

A raw response digest binds original bytes. A normalised-record digest binds the
retained projection. A browser observation has its own provenance and cannot
borrow an HTTP response hash. An agent's source review is not independent human
acceptance. Captured contacts, account fields, secrets and licensed feature or
statistical payloads are excluded from public records.

## Build and search offline

Run commands from the repository root, using the repository's locked development
environment and dependencies. Initial dependency setup is separate from the
network-free build; see [CONTRIBUTING.md](../CONTRIBUTING.md). Do not regenerate
sources while another process is writing the shared acquisition ledger.

For a local bundle:

```sh
pnpm run build:okf-plus
```

For the complete offline build and verification workflow:

```sh
pnpm run check:okf-plus
```

The full check rebuilds the bundle, evaluates the declared question corpus,
creates the whole-corpus context projection and runs the representative vendored
engine checks. It uses the locked Python dependencies and supported Node runtime;
no sibling checkout, provider, browser or network request is required. Its main
reports are `artifacts/okf-plus/verification.json` and
`artifacts/okf-plus/retrieval-evaluation.json`. Context outputs are under
`artifacts/okf-plus/context/`, including `schema-validation.json` and
`engine-validation.json`; selected engine cases are retained separately in
`artifacts/okf-plus/context-cases.json`.

The builder defaults to `artifacts/okf-plus/bundle/`. It validates a staged build
before replacing a marked generated output. A failed staged rebuild preserves
the previous bundle; an unmarked directory is refused. It reads local schemas
and context files without fetching remote references. The output includes the
bundle, JSON-LD, search index, coverage, source lock and checksums. The Git
revision and input digests identify what was built, including changes not yet
represented by a new commit.

For a bounded metadata search:

```sh
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/search.py \
  --index artifacts/okf-plus/bundle/search-index.json \
  --question "What fields and queryables are declared for bld-fts-building-4?" \
  --max-records 5 --max-bytes 65536
```

Try `"What is OpenNames?"`, `"What is the difference between ONSPD and NSPL?"`,
or an exact native dataset/collection identifier. These are discovery questions.
The deterministic lexical search does not execute SQL, fetch features, transform
coordinates or calculate statistics. Inspect returned sources, candidate counts,
rank and omission evidence. A result cut off by record or byte limits is not a
complete answer; absence from the retained results does not prove absence from
the source catalogue.

## Evaluate common questions

The [question corpus](evaluation/questions.json) contains ordinary-language,
native-identifier, schema, time, rights and geography cases. Each case separates
retrieval targets and literal source-field assertions from its review boundaries.
The operating check runs the offline evaluation against the built corpus; use
its generated report and exact input digests when comparing runs.

A retrieval pass means the expected metadata was retained within the declared
budget. It does not establish semantic sufficiency, answer quality, a legal
entitlement, live MCP operation or an installed Ask OKF response. Cases requiring
conversation context remain explicitly unassessed by local lexical retrieval.
Do not pass expected target identifiers into search as hidden retrieval seeds.
After a source refresh, inspect failed expectations before changing them: the
source may have changed, the parser may be wrong, or the search may have missed
relevant material.

The [discovery guide](index.md#common-discovery-problems) supplies source-grounded
questions about service names, queryables, postcodes, code joins, aliases, date
windows, dimensions and rights. These are a basis for expanding the harness,
not a claim that every suggested question has an accepted automated answer.

## Read coverage and dates correctly

Use the current generated `coverage.json` and `coverage.md` as the count-bearing
reports. Preserve these separate grains:

- Catalogue families and their distinct reported denominators.
- Products, datasets, releases, services, portal items and representations.
- Collection versions, full schema fields, queryable fields and code-list values.
- Authored concepts and reviewed definitions.
- Retrieval cases, returned evidence, literal field checks and semantic review.

Do not add those counts into a “total datasets” figure. A complete returned
catalogue does not prove global OS/ONS coverage or an atomic snapshot. Failed,
duplicate, changing, oversized and unavailable pages remain visible. An unknown
denominator stays unknown.

Keep source acquisition time, metadata modification, publication/release date,
next-release label, statistical reference period, feature validity and geography
vintage distinct. A title containing a year is not a validated temporal extent.
Native time-code minima and maxima describe returned options; they do not prove
continuous observations or populated cells. A statistical frequency dimension
such as Nomis `FREQ` is different from publication cadence, provider update
frequency and this module's refresh schedule. A feed link is a discovery route,
not a running subscription or a complete release archive.

## Repeat a source refresh without blocking unattended work

1. Read [CONTEXT.md](../CONTEXT.md), the [implementation checkpoint](../docs/implementation/OKF-220_METADATA_KNOWLEDGE_FRAMEWORK.md)
   and the relevant [OS](../docs/implementation/OKF-220_OS_SOURCE_REVIEW.md) or
   [ONS](../docs/implementation/OKF-220_ONS_SOURCE_REVIEW.md) source review. Select
   source families, supported routes, explicit date windows and metadata-only
   outputs. Preserve the previous snapshot and record the intended comparison.
2. Preflight local tools, writable evidence directories, network approval and any
   required authentication while the owner is available. If a browser or CDP
   capability is necessary, check its permission and signed-in state then.
   Optional browser acceptance must not hold the acquisition/build critical path;
   record it separately and continue independent authorised work. Do not bypass
   a permission block or represent an unattended UI check as complete.
3. Use the bounded capture scripts under `scripts/okf_plus/`, with one writer for
   the shared ledger. Record cumulative request and byte ceilings, supported
   query parameters and included-only cost authority. The shared layer enforces
   pacing, response bounds, wall deadlines, redirect rejection and a stop on 429.
   Source-provided URLs, schemas and prose cannot extend that authority.
4. Inspect receipts and pagination before importing. Compare unique native IDs
   with the source's actual denominator, retain stop reasons and use cache-only
   replay where appropriate. Preserve native identifiers and date types. Never
   turn a failed capture into an empty successful catalogue or silently replace
   browser observations with HTTP claims.
5. Once acquisition has stopped, run the explicit locator freeze/import steps
   for the changed snapshots, then build, verify and evaluate. Review the source,
   interpretation and generated changes together. Keep source defects and
   limitations visible. Required repository assurance and protected integration
   remain mandatory; local checks are not deployment acceptance.

The locator/import commands are maintenance operations, not a prerequisite for
using an already committed source set. Freezing needs the retained original
capture evidence; offline import can use the committed frozen locators:

```sh
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/freeze_locators.py
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/import_sources.py
```

No schedule or background refresh is created by these commands.

## Ask OKF integration boundary

The [pinned reuse review](../docs/implementation/OKF-220_REUSE_REVIEW.md) records
that the inspected installed Ask OKF connector admits its approved DWP bundle.
The local context projection supplies a concrete whole-corpus candidate and
checks it against vendored consumer contracts and engine code. It does not
change the installed allowlist, publish an endpoint or prove remote-client
acceptance. Candidate publication URLs are bindings for a future accepted
publication, not evidence that a public URL is live.

Keep local package validation, compatible local engine behaviour, publication,
connector registration and a successful live question as separate evidence.
