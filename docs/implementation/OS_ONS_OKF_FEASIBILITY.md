# OS and ONS to OKF: feasibility and indicative effort

Date: 2 October 2026. Status: proposal only. This note activates no roadmap
stage, procurement, data ingestion or spending authority. It is separate from
the current [private Sites pilot](SITES-218_PRIVATE_MCP_PILOT.md).

## Feasibility decision

An OKF representation of OS and ONS specifications, catalogues, schemas, concepts
and permitted access routes is feasible. Importing Swagger alone would not
produce a complete or reliable knowledge framework. API contracts describe
operations and data shapes; source catalogues, field definitions, code lists,
versions, geography semantics, rights and operating constraints need additional
modelling and validation. There is no verified complete inventory of both
organisations in this proposal, so neither complete coverage nor a fixed total
cost is established.

The recommended first scope is a source-backed metadata and capability layer.
It would help select the right dataset and explain an answer's limits, then route
an admitted query to a governed adapter. Loading every OS feature and ONS
observation into OKF would be a separate data-platform programme, with different
volume, update, retention, rights and query-performance requirements.

## What the official sources provide

| Source family | Useful input to OKF | What remains to establish |
| --- | --- | --- |
| OS API specifications | Operations, parameters, response structures, authentication and service-specific constraints across maps, features, search and utilities. | Enumerate the actual services and available machine-readable definitions; one API specification is not the entire OS catalogue. [OS API documentation](https://docs.os.uk/os-apis) |
| OS Downloads catalogue | OpenData product metadata and release/download references; separately authenticated data-package routes. | Bound catalogue traversal, preserve product/version identifiers and distinguish discovering a download from acquiring its contents. [Downloads specification](https://docs.os.uk/os-apis/accessing-os-apis/os-downloads-api/technical-specification) |
| OS NGD schema and queryables | Feature-type fields, relationships, schema versions and the attributes actually admitted for filtering. | Preserve the collection and schema version; a field existing in the data schema does not imply it is queryable or that every feature type is available through each delivery route. [NGD discovery](https://docs.os.uk/osngd/getting-started/access-the-os-ngd-api), [queryables](https://docs.os.uk/osngd/getting-started/access-the-os-ngd-api/os-ngd-api-features/technical-specification/queryables), [example Building schema](https://docs.os.uk/osngd/data-structure/buildings/building-features/building) |
| ONS Developer Hub and API catalogues | Dataset, edition, version, dimensions/options, observation and filtering concepts, plus endpoint-specific guidance. | Inventory the distinct API families and live coverage; preserve revisions, units and geography scope. The hub warns that beta interfaces can change. [Developer Hub](https://developer.ons.gov.uk/), [dataset reference](https://developer.ons.gov.uk/dataset/) |
| ONS `dp-dataset-api` Swagger | Machine-readable dataset-service paths, models and parameter definitions. The source distinguishes public reads from private publication operations. | Pin an exact source revision and compare it with the public deployed API; do not expose every repository operation as a callable MCP tool. This repository does not represent all ONS services. [Official Swagger source](https://github.com/ONSdigital/dp-dataset-api/blob/develop/swagger.yaml) |
| Geography products and source documentation | Release-specific geography definitions, identifiers, lookup and boundary metadata. | Reconcile these with statistical datasets rather than assuming that a shared place name or general API search proves a valid join. [ONS geography catalogue](https://geoportal.statistics.gov.uk/) |

The inference from these sources is that specification-assisted ingestion is
practical, while complete semantic coverage requires curation. The assessment
has not downloaded every specification, enumerated every product or tested every
endpoint. Before implementation, record source URLs, exact revisions or content
digests, retrieval time and unresolved coverage gaps. Follow endpoint retirement
notices rather than treating a retained Swagger file as proof of current service
availability. [ONS retirement guidance](https://developer.ons.gov.uk/retirement/)

## Proposed representation and validation

Use reviewed authored records for each provider, product/dataset, release,
collection, field, code list, geography, operation and licence. Preserve native
identifiers and source citations. Add explicit relations such as “served by”,
“has edition”, “has dimension”, “uses code list” and “supersedes”; do not infer
equivalence from similar labels. Generated search indexes or JSON-LD would remain
projections of those reviewed records, following the repository's existing
source/generated boundary.

Keep data availability, technical reachability, licence eligibility and admitted
MCP execution as different facts. Discovery must not activate a provider. Every
executable route still needs a closed schema, owner, threat and policy assessment,
request bounds, evidence receipt and meaningful tests. The separately authorised
PSGA/NGD validation supplies evidence for its scoped decision; it does not grant
bulk ingestion or universal third-party use.

For an OS feature, retain collection/schema version, native identifier, geometry
meaning and CRS. For an ONS observation, retain dataset/edition/version,
dimensions, geography code/vintage, time and unit. A representative place point,
administrative boundary and statistical best-fit lookup are different things.
The first release should evaluate source selection, valid joins, ambiguity,
withdrawn products, unsupported dimensions, missing rights and refusal behaviour
using a reviewed representative question set.

## Indicative effort and cost

These are planning estimates, not measured delivery forecasts, supplier quotes
or DWP-derived benchmarks. They assume an experienced engineer with geospatial
and semantic-modelling support, reuse of the existing repository, accessible
documentation and prompt review decisions. The totals are **cumulative**, so the
rows must not be added together.

| Cumulative outcome | Indicative person-days | Labour at an illustrative £800 per day |
| --- | ---: | ---: |
| Bounded inventory and proof of mapping: enumerate agreed source families, inspect representative specifications/catalogues, identify rights and coverage gaps, and produce a revised delivery plan | 3–5 | £2,400–£4,000 |
| Curated metadata pilot: ingest the agreed inventory into reviewed OKF records, add provenance/version handling and a small discovery evaluation | 15–25 | £12,000–£20,000 |
| Broader governed service for an agreed set of questions: validated semantic joins, approved adapters, rights/policy tests, refresh operations, evidence and deployment assurance | 40–70 | £32,000–£56,000 |

The estimates exclude VAT, paid datasets or API transactions, hosting/storage,
model charges, commercial licence/legal work, procurement delays and ongoing
operations. They do not price a copy of all OS and ONS raw records. No expenditure
is authorised by the illustrative rate or these totals.

A full cost requires the inventory first: counts of services, specifications,
products, collections, schema versions, fields, code lists and dataset dimensions;
expected change rates; selected questions and joins; rights/review workload;
service objectives; deployment/recovery requirements; and any retained data volume.
Some catalogue routes can be automated, but manual ambiguity and rights decisions
will materially affect effort. Re-estimate against that measured inventory before
committing a delivery budget or completeness claim.

## Proposed next decision

If this work is selected later, accept the bounded inventory output first and
choose the smallest useful set of questions and sources. Keep the existing Sites
pilot as a source of implementation and evaluation evidence, without treating its
six tools as complete OS/ONS coverage. Neither the inventory nor the wider build
has been activated by this proposal.
