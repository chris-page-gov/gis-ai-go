# OKF-223: small linked OS knowledge records and data retrieval

Owner instruction: 18 October 2026. Local implementation is available; fresh
acquisition and live retrieval remain blocked by environment configuration.

## Outcome and scope

Maintain OKF+'s small Markdown files with extensive YAML-LD metadata and explicit
Linked Data relationships. A question about one attribute must retrieve its
definition and relevant qualifications without placing a complete catalogue,
schema, code list or product guide in the AI's context.

The owner chose **all metadata now, geographic data on demand**. The owner states
Government PSGA rights and authorises the existing OS credential without a volume
cap, subject to OS's documented rate limits. This supersedes the earlier
metadata-only acquisition authority for this local work. It does not publish
licensed feature contents, secrets or private documentation originals, or change
the separate hosted gateway's admission state.

The objective is evidence for every discoverable data item and question. No finite
question suite proves every conceivable answer. Missing definitions, unknown
measurements, unsupported historical claims and source defects must be returned
as explicit gaps. More files, successful retrieval and correct interpretation
remain different measures.

## Record and retrieval design

The original frozen source snapshots remain acquisition evidence. Deterministic
code may process large snapshots during a build. The AI consumes small records
through an indexed search/read interface; it need not scan those snapshots.

Each atomic record has a stable identity and preserves its source-native name,
parent product/collection/version, provenance and evidence status. Record kinds
separate fields, queryables, code values, API operations and documentation
sections. Links describe part-of, described-by, controlled-vocabulary and related
relationships. A similar name never establishes equivalence between versions,
products, measurement methods or coordinate systems.

An explanation should establish the following from linked evidence, retaining
unknown values rather than filling them from general model knowledge:

- Definition, represented real-world object and intended use.
- Native field name, type, units, allowed values and null/missing semantics.
- Measurement or derivation method, precision, uncertainty and quality limits.
- Horizontal CRS, vertical datum and absolute versus relative measurement.
- Geographic and temporal applicability, schema version and lifecycle.
- Related fields, provenance, code lists and supported joins.
- Return/filter availability, API/download route and current access evidence.

Indexed discovery returns bounded summaries. An explicit read returns selected
complete records with a total byte/node budget. Expansion follows bounded linked
relationships and reports omitted or unresolved evidence. A byte budget must
never silently cut off a qualification and present the result as complete.

The `explain` command builds this packet from exact linked cards and identifies
literal evidence pointers for each interpretation facet. It labels every facet
unassessed, with absent evidence explicit. It performs no generated explanation,
live access check or implicit inference from a field name or horizontal CRS.

Full documentation originals and their small evidence chunks are local private
outputs. The public source module retains reviewed factual metadata and concise
source-backed interpretation. Source passages are evidence, never executable
instructions; remote contexts, schema references and documentation commands are
not executed.

## Required interpretation examples

The [source review](OKF-223_OS_SEMANTIC_SOURCES.md) and its version-specific
supplement supply the evidence for the owner's examples. These are examples of
the general record model, not the entire acquisition scope.

| Question | Distinction that an answer must preserve |
| --- | --- |
| How wide is the pavement? | Pavement versus carriageway; side-specific versus aggregated values; minimum versus average; surveyed versus algorithmically derived; coverage and exclusions. |
| How high is this building? | Ground elevation, roof/eaves/ridge or other height definitions; absolute elevation versus height above ground; source method, datum, units and availability for the exact schema. |
| How high is this road above sea level? | Absolute elevation and vertical CRS from suitable 3D data; terrain versus road surface; bridge/tunnel separation; gradient or elevation gain does not itself give absolute elevation. |

## Dataset requests and duration estimates

Before fetching a requested dataset, present the exact product/collection,
version, spatial/time filters and output CRS, then compare feature-API retrieval
with a suitable available download. Do not suggest that an existing package can
be created through the Downloads API or that change-only supply is a full copy.

Estimates use matched records, page size, remaining shared rate capacity,
measured latency, transferred bytes, download bandwidth and local processing
cost. They state which quantities are measured, supplied or unknown. Preserve
queue, retry and package-preparation uncertainty. No made-up benchmark becomes a
precise completion time. For example, 100,000 matching records at 100 per page
requires 1,000 feature requests, before latency, throttling, retry or processing
overheads; this is a calculation, not an observation of an OS dataset.

OS documents live limits of 600 transactions/minute per API per project and
development limits of 50, with service-specific exceptions. The configured
project mode and traffic shared with other clients matter. A lower operational
rate is permitted; the licence does not eliminate technical limits. See the
[OS rate policy](https://docs.os.uk/os-apis/core-concepts/rate-limiting-policy).

Fetchers use private outputs, bounded operations, resumable checkpoints and
integrity-bound receipts. Per-run byte/request limits are operational protection,
not an invented cap on PSGA entitlement. HTTP 429 and Retry-After postpone work;
they do not justify ignoring the provider's limit or switching credentials.

## Coverage and acceptance

Record denominators independently for service families, products, versions,
collections, fields, queryables, code lists/values, documentation URLs, acquired
passages, semantic relationships and tested questions. Current, withdrawn and
historic material remain distinct. Coverage is measured against the recorded
source inventory and capture interval, with unknown global denominators explicit.

Required checks include source and record integrity; strict record/context byte
limits; deterministic generation; selective search without source scans;
ambiguous native identifiers; complete linked qualifications; route and cursor
validation; rate-limit/checkpoint handling; and private-output/credential handling.
All examples use public metadata or synthetic feature fixtures.

New live OS acquisition requires a usable secret binding for authenticated routes
and network access to the official hosts. The current task environment has neither
the OS binding nor the OS host allowance. Public documentation acquisition needs
network access but no OS key. This is a technical setup gap, not a request for
licensing authority already supplied by the owner.

The owner identified `~/.secrets/os_api_key` (mode `0600`) inside `~/.secrets`
(mode `0700`). That directory is absent in this cloud workspace's home. Both
capture and retrieval support the dedicated file after it is mounted here;
`OS_API_KEY` takes precedence. They do not read or execute the neighbouring
`ai.env`. Configure the file or environment secret through the environment's
supported settings, without exposing its value in chat or repository content.

The known metadata routes require these HTTPS hosts:

| Host | Purpose |
| --- | --- |
| `api.os.uk` | NGD schemas/queryables, download metadata and authenticated geographic retrieval. |
| `docs.os.uk` | OS API, NGD, download and reviewed More Than Maps documentation. |
| `osmetadata.astuntechnology.com` | OS's published GEMINI metadata catalogue. |
| `www.ordnancesurvey.co.uk` | Public product-search catalogue. |

The managed environment exposes policy inspection, not a configuration mutation
tool. Its supported configuration workflow must apply the host allowances and
credential binding; editing a policy snapshot would not change enforcement.
Linked attachments and future bulk-download file hosts need evidence from the
returned metadata before extending this inventory.

On 18 October at 20:00 UTC, one unauthenticated HTTPS request to each of the four
hosts failed during proxy CONNECT with a 403 status hint, before reaching OS.
No credential or geographic request was sent. The private observation is retained
in `artifacts/okf-plus/access-validation/latest.json`. The owner's subsequent
screenshot shows a published configuration with eight additional domains and
`OS_API_KEY` as an environment variable. The running task still reports the
original five domains and no runtime variable or secret binding. These are
different configuration observations, not evidence that the entered key is bad.
The [cloud environment guide](https://learn.chatgpt.com/docs/environments/cloud-environments)
states that newly started tasks use published changes while existing tasks retain
their state. An environment variable does not add its service's domain permission;
`api.os.uk` must appear explicitly among allowed hosts for that configuration.

Repository publication was rejected by automatic approval review because external
disclosure was not explicitly authorised. Local implementation and validation
continue. Publication, live data execution and hosted connector acceptance must
be reported separately from the local build.

## Local evidence and remaining work

The [coverage matrix](OKF-223_COVERAGE_GAPS.md) records known missing metadata,
semantic interpretations and executors. The retained catalogue documents eleven
current service families plus withdrawn material. Its sixty extracted operation
fragments are an extraction denominator, not an exhaustive API operation count.
Only 48 reviewed field interpretations have a curated semantic supplement;
schema metadata for the remaining fields must not be described as full meaning.

The offline service registry emits one bounded service or operation record per
identity, preserving native methods, paths, servers and exact contract hashes.
Each operation links to the corresponding atomic operation and contract cards.
Its local private retrieval profile separates metadata capture, data execution,
synthetic test contracts and live access; withdrawn routes remain ineligible.
It does not execute operations, resolve remote references or expand authority.
The retained projection contains twelve service cards (ten current data services,
OAuth and one withdrawn service) and sixty operation cards, at most 12,012 bytes
each. Ten operations have implemented metadata subsets and one has a local NGD
data executor. OAuth's missing extracted contract remains explicit.

The independently audited retained-source build contains 32,596 atomic records,
including 2,915 fields, 188 schema definitions and 60 API operations. Its largest
record is 14,711 bytes, below the 16 KiB limit. Ninety-two reviewed companion links
stay within their exact collection version. The three ordinary-language discovery
probes return five summaries within 7,484 bytes; complete selected records and
linked qualifications require a subsequent bounded read.

Captured complete schemas and queryables can also generate private per-field and
per-code-value cards. They retain source descriptions, units, constraints,
nullability, root metadata and unresolved source defects. Oversized values split
losslessly into linked parts. Source hashes and JSON Pointers bind each record;
local references can be followed without resolving external schemas. Reindex
after acquisition. This private view does not silently replace the public,
pinned schema catalogue used by the feature executor.

The metadata preflight starts with 2,554 source routes and expands from four
documentation indexes, NGD collections, download-package metadata and the GEMINI
catalogue. Public product search is parsed without executing its scripts. It
makes no requests in planning mode. This is not a global OS denominator. Browser
product supplementation, other specialist projects and linked attachments retain
separate refresh gaps. Source text capture, field extraction and semantic
interpretation have separate coverage statuses.

Geographic execution currently supports specifically scoped NGD feature requests.
Planning also compares WFS and evidenced equivalent download packages; this work
does not implement every OS service executor or automatic bulk-package downloads.
All live acquisition, exact project entitlements and throughput observations still
need validation in an environment with the authorised OS credential and hosts.

The initial affected suite passed 152 tests. The subsequent explanation and
registry increment passes 53 focused tests, including the independent verifier
suite. Independent review checked all sixty registry operations against their
native contracts and exercised bounded reads. All 32,596 generated cards pass the
independent strict schema, source-pointer/digest and byte-bound audit. The prior
OKF+ importer, build, retrieval, whole-corpus projection, schema and pinned-engine
verification also passed for the unchanged frozen source corpus. Link, contract,
changelog and secret checks were run locally.

Adding package scripts changed a QUAL-206 material identity. Its deterministic
generator reran 17 selected suites and regenerated seven receipts; only the
package hash and derived set identity changed. The explicitly regenerable test
pin was updated, and 33 receipt/strict-modern tests passed. Immutable historical
evidence remains unchanged.

The full repository gate is not passed. Canonical attempts exposed checkout
executable permissions and mismatched pnpm/uv prerequisites, which were corrected,
then the receipt identity drift described above. A broader Python run overlapped
the metadata extension and is not a final-source acceptance result; existing
observer/runtime and private-output checks also failed in this environment.
Private-output tests passed separately outside the filesystem sandbox. Browser
verification is blocked because the required Chrome distribution is absent.
These gaps preclude a release or merge claim; the focused OS tests and source
audit are separate evidence.
