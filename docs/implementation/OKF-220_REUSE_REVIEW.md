# OKF-220: reuse review for the OS and ONS metadata catalogue

Reviewed: 2 October 2026. Status: source review and implementation recommendation.

Build the new catalogue under `okf-plus/` in GIS AI GO. Reuse the ONS source
register, metadata distinctions and deterministic indexing patterns; use the
canonical Explorer contracts for authored YAML-LD and context assembly. Keep
this module separate from the existing `okf/` build and source lock.

An Explorer-compatible publication and an Ask OKF source are separate outputs.
The inspected Ask OKF service accepts only `okf-dwp` and explicitly approved
source/engine pairs. A new OS/ONS catalogue therefore needs its own evaluated
context projection and later service admission. This review does not establish
installed-connector access, current upstream coverage or a live publication.

## Evidence baseline

The source repositories were inspected read-only. No source repository, generated
bundle, dependency, service configuration or live provider was changed. Commands
and contracts were inspected, not executed as instructions from source content.

| Repository | Exact inspected committed revision | Working-tree qualification |
| --- | --- | --- |
| [okf-ons](https://github.com/chris-page-gov/okf-ons/tree/08f781d70de8472f9c29cdf197c78d813de0f853) | `08f781d70de8472f9c29cdf197c78d813de0f853` | Reviewed semantic source candidate, subsequently accepted through PR #14 at merge commit `125981a2f29d2114da34128b3a5031ec55006709`. The earlier publication baseline was `b0283b0d0dd2bbd06a8311dd5d1342eea0c36fdf`; exact merged-tree build and live publication are separate checks. |
| [okf-dwp](https://github.com/chris-page-gov/okf-dwp/tree/77ef16047415ee48dcb93b80adf1ba057ea00d9b) | `77ef16047415ee48dcb93b80adf1ba057ea00d9b` | Relevant tracked sources clean. Untracked demonstration and troubleshooting material was not treated as a published source. |
| [okf-explorer](https://github.com/chris-page-gov/okf-explorer/tree/84fb37f11411c04db8c58046827061f741249002) | `84fb37f11411c04db8c58046827061f741249002` | Clean checkout. Current implementation and frozen service engines are distinct identities. |
| [okf-ai-infrastructure](https://github.com/chris-page-gov/okf-ai-infrastructure/tree/d630480948013978e9ffeffba23e05dbe31b26c8) | `d630480948013978e9ffeffba23e05dbe31b26c8` | Broad uncommitted semantic migration affects source and generated files. Use the committed Markdown authoring example only; prefer Explorer for the canonical profile. |

This is not a complete repository security audit or a fresh build of those
repositories. Statements below concern the inspected files and revisions.
Historical upstream URLs in them were not re-fetched during this review.

The initial ONS publication pin advanced from
`4aa41c71dd570ceccb661768af95c4d69f49162b` to
`b0283b0d0dd2bbd06a8311dd5d1342eea0c36fdf` after a read-only committed-tree
check. The separately reviewed semantic candidate is now accepted: a read-only
GitHub check confirmed [PR #14](https://github.com/chris-page-gov/okf-ons/pull/14)
merged at 07:56 UTC on 2 October 2026, with merge commit
`125981a2f29d2114da34128b3a5031ec55006709`. The inspected candidate and accepted
merge retain separate identities; this review does not claim a fresh build or
live acceptance of the merge commit.

## Useful ONS material

The pinned ONS repository already provides a metadata-only catalogue, a local
network-free MCP broker and independent discovery evaluations. It is a better
starting point than a new unbounded scrape. Reuse source-native identities and
field provenance; retain separate representations across source surfaces.

| Material at the pinned ONS revision | Reuse in `okf-plus/` | Boundary |
| --- | --- | --- |
| `source/source-register.json`; `docs/scope-and-denominator.md` | Source lane register, declared denominator, pagination/stopping evidence, omissions, exclusions, aliases and tombstones. | Completeness applies only to measured registered lanes at a named snapshot. Counts from different surfaces are not unique statistical-product counts. |
| `source/metadata-enrichment-2026-07-21-r6/snapshot.json` and its four named metadata files | Hash-bound historical bootstrap: 337 ONS Data API, 1,617 Nomis, 3,035 Open Geography and 108 Explore Local Statistics records; 5,097 representations in total. | These are July metadata snapshots, not current observations or proof of October completeness. ELS is a pinned application projection, not a stable live API. |
| `src/okf_ons/model.py`; `docs/metadata-model.md` | Identity construction, provenance, dimension distinctions, strict Nomis FREQ/TIME interpretation, metadata evidence states. | Do not carry the common record's OGL default across to OS or other sources. Licence evidence needs a source-specific rule; unresolved rights remain unresolved. |
| `src/okf_ons/search.py`; `tests/test_search.py` | Deterministic tokenisation, weighted fields, native identifier lookup, filter postings and bounded result chunks. | `okf-static-search.v2` is a Search contract, not an Ask OKF context manifest. Search ranking is not evidence sufficiency. |
| `src/okf_ons/metadata_gaps.py`; `evaluation/metadata-completeness/stopping-audit.json` | Applicable-field denominator, missing/conflicted evidence, measured acquisition yield and explicit stopping reasons. | The July audit measured evidence availability, not statistical accuracy. Its 68.7% applicable-field completeness is historical and does not establish a new catalogue's quality. |
| `src/okf_ons/mcp_broker.py`; `docs/mcp-selection-contract.md` | Exact source/version selection, snapshot/record digests and explicit unresolved options. | Plans are non-executing and non-authorising. Historical MCP-Geo bindings are not automatically supported Sites tools. |
| `evaluation/gold-queries.json`; `evaluation/ai-client/tasks.json`, `expected.json` and `personas-and-journeys.json` | Existing question patterns, contrast cases and expected source identities. | Re-evaluate against the new corpus and engine; historical client scores do not transfer. |
| `docs/provider-datapacks.md`; `source/okf-publication.json` | Distinguish frozen snapshot facts from dated external-provider reviews, with digest and snapshot parity. | `reviewed-reference-not-live-validated` remains dated reference evidence; no verification event or freshness deadline is invented. |

The committed coverage ledger explicitly leaves ONS website dataset pages,
release calendar and releases, QMI, time-series pages and data.gov.uk
reconciliation as planned lanes. They have no implemented denominator and do
not contribute to full coverage. These are useful next acquisition targets for
the user's feed, update and date-range questions.

The July stopping audit still records missing revision status for all 5,097
records, missing methodology for 4,887, missing frequency for 3,083 and missing
applicable time coverage for 371. These figures are evidence of unresolved
metadata, not a reason to infer values from titles or request observation data.
The stable demonstrator snapshot and the enriched r6 snapshot also have
different identities: choose and bind one input explicitly in each build.

The ONS semantic implementation first reviewed at
`65295ab90ccf587d64fe06a3d304b27cf04d9fe8` now adds `okf.semantic.json`,
`src/okf_ons/semantic.py`, `src/okf_ons/schema_validation.py`, assertion schema
files and whole-graph parity validation. The candidate was inspected directly
from Git objects, without consuming working-tree bytes. At inspection its
branch was `codex/semantic-assertion-publication`; acceptance was not yet
observed. The later PR #14 merge establishes source acceptance, while live
publication remains outside this review.

### Accepted ONS contracts and immediate reuse

At the earlier publication baseline, `okf.publication.json` uses
`okf-repository-publication-contract.v1`. It declares authored/generated
boundaries, source-to-publication dependency planes, command identities and
exact assured-byte promotion. `scripts/check_publication_contract.py` checks
local path references, unique identities and an acyclic plane graph. Reuse this
contract shape for GIS-owned lifecycle declarations; its command strings remain
untrusted declarations, and its validator does not establish browser or semantic
acceptance. ONS still records no committed generated baseline and separately
leaves exact-commit browser verification unproved.

That baseline's semantic declaration points to
`source/ontology-crosswalk.json`, whose 30 canonical field mappings distinguish
direct, structural, broader, conditional and process mappings. It is useful
reviewed design evidence, not a replacement executable source schema. In
particular:

- `dct:temporal` represents reference-period evidence; release, modification and
  geographic vintage retain separate meanings.
- `dct:accrualPeriodicity` needs cadence evidence. A source-native statistical
  frequency dimension does not supply that evidence by itself.
- `dct:spatial`, `locn:Geometry` and `schema:spatialCoverage` apply only when
  supported by the described geography and representation.
- `prov:Entity`, `prov:Activity`, `prov:Agent`, `prov:wasDerivedFrom` and
  `prov:hadPrimarySource` express different provenance roles. Preserve exact
  captured identifiers and locators beside these relationships.
- `dcat:DatasetSeries`, `dcat:inSeries`, version/succession predicates and
  `skos:exactMatch` require explicit source evidence; similar titles do not
  establish them.

Keep these established terms aligned with the GIS model. Use GIS extension
terms for evidence status, rights admission and native period-code extrema
where the crosswalk supplies no exact equivalent. The accepted ONS semantic
compiler now provides a reviewed reference for choosing a tested adapter or
shared producer deliberately. The current local producer remains necessary
for the OS-specific schema inventory and captured October evidence.

### Accepted semantic source reviewed during the owner's merge

The immutable candidate supplies a useful implementation reference rather than
a replacement for the entire GIS producer:

| Candidate contract or function | Reuse decision |
| --- | --- |
| `okf.semantic.json` | Reuse the explicit authoritative-input, generated-output, local-context and relationship-contract declarations. Its conformance label is a producer declaration; separate validation and consumer evidence are still required. |
| `profiles/bundle-wiki/v1/` and `v1.vendor-lock.json` | The same canonical 16-file Explorer profile and immutable release lock already recommended here. Vendor that profile once; do not create a second GIS-specific copy under the canonical identity. |
| `src/okf_ons/semantic.py:compile_relationships` | Supports only `alternative`, `cross-source-alternative` and `cross-source-representation` with ONS record shapes and source-specific rules. A shared adapter would need deliberate translation of GIS routes, native source evidence, rights and relation kinds. Do not call it for OS field relationships without a new reviewed rule. |
| `semantic_assertion`, `add_direct_triples`, `validate_semantic_projection` | Reuse the one-source projection and exact triple/count parity pattern. Direction, predicates and endpoints must remain identical across runtime rows, direct triples and reified assertions. |
| `src/okf_ons/schema_validation.py` | Digest-pinned, offline validation for its accepted JSON Schema keyword subset, rejecting unsupported keywords and remote references. GIS already has `jsonschema`; reuse the canonical schema and provenance lock instead of copying a second general validator. |
| `src/okf_ons/build.py` semantic shards and `data/semantic/manifest.json` | Useful scale pattern: deterministic compressed entity/assertion shards with semantic validation, count and digest bindings. This semantic graph manifest is still distinct from an Ask OKF context corpus. |

The candidate deliberately labels similarity as inferred discovery and marks
statistical equivalence false. Shared declared table-code relationships are
normalised correspondence, not identity. Its evidence time fallback explicitly
labels publication time when source retrieval is not evidenced. GIS has exact
capture times and should retain them rather than invoke that fallback. The
candidate does not change the installed Ask OKF allowlist or supply new live
provider authority. Its committed tests were reviewed but not executed as part
of this bounded source review.

A subsequent committed-tree check found candidate head
`08f781d70de8472f9c29cdf197c78d813de0f853`, published on
`origin/codex/semantic-assertion-publication`. Its difference from the reviewed
compiler commit comprises documentation, publication/semantic declarations and
tests; the compiler and schema validator are unchanged. At that inspection,
`origin/main` remained `b0283b0d0dd2bbd06a8311dd5d1342eea0c36fdf`. The subsequent
confirmed PR #14 merge at `125981a2f29d2114da34128b3a5031ec55006709` accepts
this reviewed source candidate. It does not transfer ONS test results to the
GIS implementation or establish hosted Ask OKF admission.

## Authored source and semantic contracts

Use Markdown with one YAML-LD frontmatter document for the new authored records.
The evidence for this structure is Explorer's
[`profiles/bundle-wiki/v1/index.md`](https://github.com/chris-page-gov/okf-explorer/blob/84fb37f11411c04db8c58046827061f741249002/profiles/bundle-wiki/v1/index.md)
and `docs/okf-0.2-yaml-ld-semantic-authoring.md`. The small OKF 0.2 core and the
additive Bundle Wiki profile are different conformance claims.

- Declare `okf_version: "0.2"` at the module's root index. Keep the core `type`
  and profile `@type` meanings distinct. Provide absolute semantic `@id` values,
  safe local routes, title, description, lifecycle status, `generated` and
  concrete `sources`.
- Resolve only pinned local JSON-LD contexts. Parse UTF-8 YAML 1.2 safely;
  reject duplicate keys, multiple documents, cycles, non-string mapping keys
  and non-finite numbers. Quote dates. Build offline without remote context or
  schema loading.
- If claiming the canonical Bundle Wiki v1 URI, vendor its exact 16-file
  profile and adjacent `v1.vendor-lock.json`. The accepted vendor lock names
  Explorer release `v0.6.0`, commit
  `4bb7b92a64b7ba69bde9b1e86786217338cd166d`, tree
  `d26ae9a818041ff74c469e653ec714632ddbfc2a`. Do not edit those bytes under the
  same canonical `$id`; use a separate GIS extension schema and namespace.
- Declare authored inputs, generated outputs, limitations and build/check
  tooling in a module semantic contract. It is a discoverability control file,
  not evidence that every conformance or publication gate passed. The root
  publication lifecycle can reference the module without changing `okf/`.
- Treat ordinary Markdown links as navigation or `dcterms:references`.
  Material relationships need explicit source, predicate, target, assertion
  identity, direction, authority, evidence, rights and scope. Similarity and
  cross-source correspondence do not imply equivalence.
- Generate direct triples, reified assertions and runtime rows from the same
  source; validate every assertion and their identity/count parity. Keep
  official, normalised, inferred and model-derived claims distinct. Human
  verification requires a recorded event; deterministic generation alone does
  not justify `verified`.

Explorer's `scripts/okf_semantic.py`, `scripts/reconcile_okf_repositories.py`
and canonical profile schemas are the useful reference implementations. The
committed infrastructure repository's `standards/openapi.md` demonstrates a
small source-backed Markdown record, but its older profile mirror and inferred
viewer relationship descriptions should not be adopted as current semantic
authority. Its uncommitted migration is expressly excluded from this baseline.

The DWP producer offers a richer provenance pattern:
`knowledge/full-dmg/international/intl-dla-mobility-classification.yamlld`
retains source and extraction hashes, acquisition time, exact locators,
interpretation status and unresolved review. Its `domain-profile/navigation/`
keeps mention-based discovery separate from applicability. Reuse that
separation, not its legal corpus or source-specific extraction pipeline.

## Searchable metadata model

Define source-backed fields before widening acquisition. At minimum the module
needs the following distinct claims; each carries a value or explicit evidence
state, source locator, source hash, observation time and derivation rule.

| Claim | Recommended treatment |
| --- | --- |
| Identity | Provider, source surface, native identifier, canonical resource, record kind and separate version/edition/collection identities. Never derive identity from title alone. |
| Authority and rights | Source publisher, surface operator and independent bundle publisher; metadata rights separate from data rights, API authentication, PSGA entitlement and hosting/AI-recipient permission. |
| Temporal evidence | Separate acquisition time, metadata modification, release date, announced next release, revision event, dataset reference period, available observation-period extent and geography effective date/vintage. Preserve precision and source time zone. |
| Frequency | Separate statistical/reference frequency, publication cadence, metadata refresh schedule and feature change/update frequency. Nomis FREQ does not establish publication cadence. Unknown or multiple options remain explicit. |
| Feeds and change discovery | Explicit advertised feed/calendar/change endpoint, format, relation, documented scope and last observed availability. A URL or promised schedule does not prove a working subscription, complete history or automatic refresh. |
| Schema | Official schema/queryables/OpenAPI URL, dialect/version, captured digest, feature/property types, required/nullable/enumerated fields, CRS and units, linked validation finding. Schema version, collection version and feature version are separate. |
| Coverage | Provider-lane denominator, discovered/retained/excluded/unexplained counts, geographic scope, grain, vintage, population/measure/unit, date range, completeness basis and stopping reason. |
| Access plan | Advertised API/download formats and required dimensions; live validation and policy status separate from discoverability. Metadata presence must not imply a callable Sites tool. |

Index these fields directly and provide plain-language discovery descriptions
with their evidence state. For example, “Which datasets are updated monthly?”
must distinguish a source-declared monthly release from monthly observations.
“What years are available?” must not use geography vintage as the answer.
Keep raw source values alongside normalised fields, and preserve conflicting
source observations rather than selecting one silently.

The current [NGD validation](SITES-218_NGD_VALIDATION.md) demonstrates why schema
findings belong in this catalogue: official public schema metadata can contain
contradictory required-field spelling, while feature version information uses
source-native date fields. A captured schema is not a claim that all licensed
features have been validated. No protected feature values are needed here.

## Explorer and Ask OKF integration

Explorer's ordinary Search can consume the generated small bundle or
large-corpus projection. Ask requires an additional declared source:

1. Begin with a bounded `okf-context-index.v1` for reviewed catalogue questions.
   Generate records, directed assertions and scoped requirements from the same
   authored metadata. Advertise it with an exact digest through
   `entrypoints.context_assembly` in the Explorer descriptor.
2. For broad lexical discovery, add a separately tested
   `okf-context-corpus.v3` and `entrypoints.context_corpus`, including bounded
   record, discovery-card, posting and relationship shards. ONS static-search
   manifests cannot be renamed to this format. An invalid advertised corpus
   must fail closed, not silently fall back to a smaller index.
3. Use Explorer's `profiles/context-assembly/v1/` schemas and
   `apps/okf-explorer/src/lib/context/{index.ts,types.ts,corpus.ts,corpusV3.ts}`
   as pinned contracts. The closed context schemas require a deliberate
   projection; arbitrary catalogue frontmatter cannot be passed through as
   unknown fields. Evidence records retain whole text, hashes, locators,
   authority, rights, access and scope.
4. Evaluate the direct engine against frozen bytes before any service change.
   Report source identity, engine identity, snapshot, input/index digest,
   question, budget, context identity, omissions and requirements. Preserve
   `insufficient` or `conflicting` when facts are missing or inconsistent.
5. Prepare a proposed new logical bundle identifier, immutable source revision,
   descriptor/index/manifest digests and compatible engine pair for Ask OKF
   admission. Do not claim that this step is already supported remotely.

The exact local service implementation is in Explorer's
[`services/ask-okf-mcp/`](https://github.com/chris-page-gov/okf-explorer/tree/84fb37f11411c04db8c58046827061f741249002/services/ask-okf-mcp):
`src/contracts.ts` fixes the input bundle to `okf-dwp`; `src/registry.ts` pins
approved manifests and versions; `src/bundles.ts` selects those sources;
`src/engines.ts` approves exact source/engine pairs and statically imports frozen
assemblers. The current default DWP source is
`7eeded763042ddd0070f4fed834c6074149e8e2f`, paired with engine source
`d6930bbcddaab616deec002d9e6efff6e3aae953`; the current Explorer checkout is a
different revision. `ARCHITECTURE.md` documents these separate identities.

A later, separately authorised upstream integration would add the new bundle
to those contracts and registry, bind reviewed source/engine bytes, preserve
existing DWP replays, and verify direct-engine, full structured/text MCP package,
compact continuation and actual installed-client parity. Public source retrieval
must remain allowlisted, hash-checked and redirect-rejecting. Registering a
bundle in Explorer or deploying static files does not perform this service
admission. Do not relabel an independent GIS metadata search tool as the
installed Ask OKF connector.

## DWP retrieval lessons and required evaluation

The previously investigated DWP failure is a historical diagnosis, not a new
live reproduction in this review. The ordinary-language question found the
qualifying passage F1123 but missed the timing passage A4361, which ranked
535th with only 16 lexical candidates admitted. Larger context budgets did not
recover a candidate outside that shortlist. The generic `rate` alias also
activated unrelated material and exhausted a separate 64-file allowance.

Current source inspection confirms the relevant mechanisms still exist:
`corpus.ts` declares 24 query tokens, 16 candidates and 64 files; `corpusV3.ts`
reserves bounded places for verified multiword discovery routes before lexical
candidates; DWP's `domain-profile/staff-semantic/concepts.yamlld` still contains
the broad `rate` alias. This does not establish that every present-day query
reproduces the old failure. DWP's `domain-profile/evidence-connect/profile.json`
and `scripts/build_evidence_connect.py` demonstrate source-bound discovery
wording and scope patterns that can be tested without promoting discovery
cards into source evidence.

For OS/ONS, avoid universal aliases such as “area”, “rate”, “latest” or “update”
that route an entire question to one product. Use provider-, subject- and
task-scoped descriptions. Add questions about evidence dependencies, including
schema version, geography vintage, observation range and release cadence,
rather than only exact catalogue titles.

Acceptance should include:

- Exact native identifier, ordinary-language wording, paraphrases and withheld
  questions across each represented source lane.
- Contrasts: release cadence versus observation frequency; effective geography
  date versus data period; metadata permission versus data access; product versus
  feature version; code lookup versus polygon containment; similar statistical
  products without an equivalence claim.
- Questions requiring more than one record, with explicit directed routes and
  independently defined evidence requirements. Requirement records are checks,
  never hidden retrieval seeds.
- Unknown, stale, conflicting, rights-unresolved and unsupported-live-call cases.
  Missing evidence must not become a negative claim about the real world.
- Rank, candidate, hydration and path metrics separately: relevant source rank,
  admitted candidate count, fetched files/bytes, selected evidence, required
  path retention, unresolved terms and budget omissions. Increasing byte limits
  alone is not a retrieval repair.
- Exact canonical-package replay, digest mismatch and stale-context rejection;
  independent Search, direct-engine, MCP transport and installed-client results.
  No model or Voice acceptance is inferred from local tests.

## Recommended delivery split and checks

| Workstream | Proposed owned paths in GIS AI GO | Acceptance |
| --- | --- | --- |
| Source census and acquisition | `okf-plus/source-register.*`, source locks and acquisition adapters | Bounded source-specific metadata requests; exact digests and scope; no observations, licensed values or credentials; unexplained omissions visible. |
| Authoring and semantics | `okf-plus/records/`, local contexts, extension schemas and semantic contract | One safe YAML-LD document per record; identity/route uniqueness; typed temporal and rights claims; all assertions validated; no invented verification. |
| Deterministic producer | `okf-plus/scripts/`, generated projections and checksums | Offline repeatability; source/output lockstep; canonical profile bytes; direct/runtime/reified parity and bounded manifests. |
| Discovery and context | Search projection, context index/corpus and consumer adapter | Independent contract tests; ordinary-language and negative-control corpus; complete package parity and explicit omissions. |
| Publication and service admission | Module runbook, integration proposal and root-owned lifecycle wiring | Canonical GIS CI; later exact publication/browser and connector acceptance; preserve existing `okf/`, DWP and release gates. |

Start with the historical ONS bootstrap explicitly labelled as such plus the
already reviewed OS public metadata/schema evidence. Add a current bounded
source census to establish fresh denominators, prioritising release, cadence,
feed and schema gaps. Publish coverage and gaps alongside search from the first
increment. The build must distinguish a broad but dated inventory from freshly
verified fields, rather than replacing the whole snapshot date with its build
time.

Run the affected GIS checks and mandatory canonical CI for implementation.
Use focused semantic and context checks from the pinned contracts; do not run
every sibling repository's publication pipeline merely to reuse a format.
Upstream producer acceptance, new source acquisition, live publication and Ask
OKF service admission each retain their own evidence and authority boundary.
