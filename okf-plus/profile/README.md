# OKF+ metadata and schema profile

OKF+ is an additive, project-owned OKF 0.2 profile for OS, ONS and geospatial
knowledge. It is a candidate extension, not a replacement standard or a claim
that the upstream Explorer/Ask OKF service has accepted it.

Records use Markdown with JSON-shaped YAML-LD front matter. JSON is a strict
subset of YAML 1.2; the deliberately narrow parser rejects duplicate keys,
non-finite numbers, executable tags and multiple documents. The context URI
resolves to the bundled `context.jsonld` during offline compilation; the build
never fetches a context or follows a schema reference.

The [standards register](standards.json) describes applicable vocabularies and
mapping purposes. Namespaces are not certifications. Dataset, service, document,
concept and schema-field identities remain distinct. Native schema enum values
and source code-list identifiers are retained without inventing cross-source
`owl:sameAs` relationships. Semantic relations are explicit; ordinary prose links
are navigation and do not establish domain assertions.

The builder emits `vocabulary-usage.json`, bound to the same revision and input
digest as the bundle and included in its checksums. It expands the pinned local
context's aliases and prefixes in the record graph, then counts predicate
occurrences, class references, object references and typed-literal datatypes
separately for each declared namespace and term. It reports unused registered
terms and prefixes, additional used terms and unregistered namespace use.
Context declarations, subject identifiers, ordinary text and opaque `@json`
contents are excluded. A property occurrence counts once per node even if its
value is an array; each class reference also counts its implicit `rdf:type`.
The report is an offline usage inventory, not a general JSON-LD processor,
entailment check, ontology-conformance result or semantic certification. The
register's `mappingReview` records that reporting method, not a completed human
review. A declared but unused ontology remains visibly unused.

The OKF literal fields `status` and `type` retain their existing values and map to
the local predicates `okfp:lifecycleStatus` and `okfp:recordType`. Formal classes
remain in `@type`. The ADMS mapping is deliberately not admitted:
[`adms:status`](https://www.w3.org/TR/vocab-adms/#adms-status) expects a SKOS concept
resource, while local `draft`/`stable`/`deprecated` labels do not identify reviewed
external concepts. The profile does not invent those identifiers or treat an
internal record-kind label as a `dcterms:type` resource. The cited ADMS source is
the retired W3C Note; the register does not claim a current SEMIC version.

## Source and generated material

`source/` contains captured, normalised factual metadata and receipts. Full raw
responses remain in ignored local acquisition evidence. Named contacts, account
handles, credentials and observation/feature payloads are excluded from the
public projection. A response digest identifies the original response; the
normalised-record digest identifies the retained factual projection. They are
different evidence objects.

NGD documentation code-list labels use the bounded
`os-documentation-native-label-table.v1` structure: explicit columns
`sourceRow` and `nativeText`, with rows retaining the exact decoded text,
including meaningful whitespace and duplicate values. The enclosing source
page, table ordinal and row locate each label. Only reviewed code-list routes
and `Label`/`Definition` or `Label`/`Description` header shapes admit these
values. Narrative definitions remain private. A retained native label is not
an inferred API code/enum, a unique concept identity or evidence of cross-list
equivalence. Each table reports source, retained and omitted label-row counts.

The explicit importer writes source-backed `records/` Markdown. Its mappings
and the captured snapshots are authoritative for machine-imported records;
separately authored concepts remain separate and are never overwritten by a
catalogue refresh. The offline builder reads the Markdown to produce bundles,
search and coverage. Do not hand-edit generated artefacts.

A source record is not independently human-reviewed merely because parsing or
schema checks pass. Imported records say `normalised` and `not-human-reviewed`.
Authored interpretation must state its source and review boundary. Every material
result retains sources, rights, temporal evidence, release routes and limitations.

## Temporal and update evidence

Keep these separate: retrieval time; metadata modification; publication/release;
next announced release; data reference period; available native observation-period
options; feature validity; geography vintage; classification adoption.

`update.frequency` is a declared publication/update cadence. Nomis `FREQ` is a
statistical dimension and is not used as release cadence. `temporal` describes
its explicit evidence kind. Missing extents stay unknown. Open ends do not prove
continuous coverage, and period-code minima/maxima do not prove populated cells.
Do not derive a date range from a title, metadata timestamp or first-release date.

Recognised explicit cadence labels retain the reviewed SDMX frequency-code IRI.
Other source-stated labels use an anonymous `dcterms:Frequency` node with
`rdfs:label`, preserving the original label and source-field evidence in `update`.
This keeps [`dcterms:accrualPeriodicity`](https://www.dublincore.org/specifications/dublin-core/dcmi-terms/#http://purl.org/dc/terms/accrualPeriodicity)
resource-valued without inventing a code or converting the label into a schedule.

Imported Nomis `details.timeOptionsTable` uses the lossless
`gis-ai-go.native-time-table.v1` projection: explicit columns `value`,
`description` and `revisionMetadata`, with revision columns `title` and `value`.
Values and numeric types are retained. A null description cell denotes an absent
key; an empty object denotes a present, empty description. The source snapshot
retains the original objects. `compact_time_metadata` and
`expand_time_metadata` in the model prove round-trip equality. This removes
repeated field names so complete records fit the pinned consumer's evidence-unit
limit; it drops no periods or revision fields and does not raise that limit.

Release catalogues and feeds are searchable links with documented scope. A recent
RSS feed is a discovery signal, not a complete release archive or a running
subscription. Refreshes use bounded capture and explicit source diffs; no
recurring schedule is created by this profile.

## Assurance and access boundary

Catalogue, metadata, schema, field, concept and query-evaluation coverage have
separate denominators. The report must expose unknown denominators, failed
requests, changed counts, omitted source fields and unexplained exclusions.
Source-schema contradictions remain visible; never silently repair an official
schema while claiming byte identity or provider conformance.

No metadata record admits a live provider invocation. Metadata rights, described
resource rights, authentication, entitlement, hosting permission and current
technical availability are separate facts. The model introduces no geospatial
calculation or statistical answer generated by an LLM.
