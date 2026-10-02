---
{
  "okf_version": "0.2",
  "@context": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/context.jsonld",
  "@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/id/catalogue",
  "@type": ["dcat:Catalog"],
  "type": "Knowledge Bundle",
  "title": "OS, ONS and geospatial OKF+",
  "description": "Source-backed discovery of public metadata, schemas, documentation and geospatial concepts, with explicit provenance, coverage and access boundaries.",
  "tags": ["OKF", "Ordnance Survey", "ONS", "geospatial", "metadata", "schema", "provenance"],
  "status": "draft",
  "generated": {"by": "gis-ai-go authored module documentation"},
  "sources": [
    {"resource": "../docs/implementation/OKF-220_METADATA_KNOWLEDGE_FRAMEWORK.md", "title": "Authorised scope and implementation checkpoint"},
    {"resource": "../docs/implementation/OKF-220_OS_SOURCE_REVIEW.md", "title": "OS source review"},
    {"resource": "../docs/implementation/OKF-220_ONS_SOURCE_REVIEW.md", "title": "ONS source review"},
    {"resource": "profile/README.md", "title": "Project-owned OKF+ profile"}
  ],
  "dcterms:conformsTo": {"@id": "https://chris-page-gov.github.io/gis-ai-go/okf-plus/profile/v1"}
}
---

# OS, ONS and geospatial OKF+

Use this knowledge bundle to find candidate sources, inspect their identifiers
and schemas, and understand the evidence needed for a defensible query or join.
It contains metadata and interpretation boundaries. It does not supply current
statistical observations, geographic features, provider entitlement or a live
API connection.

Start with the [operating guide](README.md) for building, searching, evaluation
and refresh. The [profile](profile/README.md) explains source and generated
material, semantics and access boundaries. The [implementation checkpoint](../docs/implementation/OKF-220_METADATA_KNOWLEDGE_FRAMEWORK.md)
records current acceptance and gaps. Read generated coverage from the build for
current counts; the directory size is not a count of unique datasets.

## Find the right evidence

| Need | Starting point | Check before using the result |
| --- | --- | --- |
| OS product, API, NGD collection or field | [OS source review](../docs/implementation/OKF-220_OS_SOURCE_REVIEW.md) and [source-family register](profile/source-families.json) | Product versus service; collection/schema version; queryable versus returned field; retirement and rights. |
| ONS, Nomis or Census source | [ONS source review](../docs/implementation/OKF-220_ONS_SOURCE_REVIEW.md) | Native dataset, edition and version; statistical population; dimensions, units, reference period and revision. |
| Geography, identifier or method | [Geography vintage](records/geospatial-concepts/geography-vintage.md), [geography lookup](records/geospatial-concepts/geography-lookup.md), [concept scheme](profile/standards.json) | Code scheme, geographic level, vintage, exact/best-fit method and correspondence direction. |
| Repeatable discovery checks | [Question corpus](evaluation/questions.json) and the [operating guide](README.md#evaluate-common-questions) | Retrieval, literal field checks and semantic review are different assessments. |

## Common discovery problems

These prompts are derived from official guidance and the source reviews. They
are not findings about support volumes or a claim that all users have the same
problems. The examples describe metadata discovery, not executed data queries.

| Question or difficulty | What to establish | Source and example |
| --- | --- | --- |
| “OS Features” sounds like “NGD Features”. | Preserve the service name, protocol and versioned collection. The WFS Features service and NGD Features have different coverage. | [OS API FAQs](https://docs.os.uk/os-apis/core-concepts/faqs). Search `bld-fts-building-4` rather than treating “buildings” as a complete query contract. |
| A schema field exists, but filtering fails. | A returned property and a queryable property are separate declarations. Inspect the exact collection's queryables and preserve source-schema defects. | [NGD queryables](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/queryables). Ask “What fields and queryables are declared for bld-fts-building-4?” |
| An NGD tile omits an attribute. | A visualisation tile can expose a subset of the source feature attributes. Do not infer that the underlying source lacks the attribute. | [OS API FAQs](https://docs.os.uk/os-apis/core-concepts/faqs). Select the relevant feature/schema evidence before promising a richer response. |
| An older schema appears to imply historical data. | Schema version, feature validity, delivery date and available historical supply are different. A maintained older schema may receive current data. | [NGD versioning](https://docs.os.uk/osngd/getting-started/os-ngd-fundamentals/data-schema-versioning) and [temporal filtering](https://docs.os.uk/osngd/getting-started/downloading-with-os-select+build/getting-started-with-data-packages/getting-started-with-temporal-filtering). Ask separately for the schema version and the required as-of date. |
| A place name or acronym produces several matches. | A search alias is a discovery aid, not a join key. Retain each returned native identifier, geographic level, publisher and vintage; use official correspondence rather than title similarity. | [ONS names, codes and lookups](https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups). “Warwick” needs a named geography and release before a code join. |
| A postcode is used as an exact boundary lookup. | ONSPD uses postcode-point allocation; NSPL uses Output Area best fit for higher geographies. Neither proves every address lies in the assigned area. | [ONS postcode products](https://www.ons.gov.uk/methodology/geography/geographicalproducts/postcodeproducts). Choose the product and allocation method before joining to a statistical geography. |
| Old and new area codes fail to join. | Preserve live/terminated status, effective geography and relationship type. A successor code does not make historical observations directly comparable. | [Code History Database](https://www.ons.gov.uk/methodology/geography/geographicalproducts/namescodesandlookups/codehistorydatabasechd). Inspect the relevant lookup, vintage and direction. |
| UPRN, USRN and TOID are treated as interchangeable. | They identify different kinds of thing. An explicit relationship can support a join; it does not establish identity, address availability or common rights. | [Government identifier guidance](https://www.gov.uk/government/publications/open-standards-for-government/identifying-property-and-street-information) and [OS UPRN explanation](https://www.ordnancesurvey.co.uk/public/unique-property-reference-numbers). Ask for the relationship source and its version. |
| A recent release is assumed to contain recent observations. | Keep release windows separate from statistical reference periods and geography/classification vintages. Period-code extrema do not prove populated observations or continuity. | [ONS dataset metadata](https://developer.ons.gov.uk/dataset/) and [release search](https://developer.ons.gov.uk/search/search-releases/). Specify both “published during this window” and “measuring these periods”. |
| A statistical question names only a topic. | Select dataset, edition/version, measure, unit, geography, population and all required dimensions. A Nomis frequency dimension is not a release schedule. | [Nomis API guide](https://www.nomisweb.co.uk/api/v01/help) and [ONS population definitions](https://developer.ons.gov.uk/population-types/). “Employment in Warwick” still needs period, population and measure. |
| Every possible Census dimension combination is assumed available. | Metadata describes a query space. Disclosure controls and product design can restrict combinations or geographic detail. | [ONS multivariate products](https://www.ons.gov.uk/census/aboutcensus/censusproducts/multivariatedata). Inspect the appropriate population and categorisation before proposing a query. |
| Public documentation is mistaken for permission to fetch data. | Keep metadata rights, data licence, authentication, entitlement, provider availability and hosting/AI-recipient permission separate. A specification can document private or write operations. | [OS source review rights boundary](../docs/implementation/OKF-220_OS_SOURCE_REVIEW.md) and [project context](../CONTEXT.md). Discover a protected NGD schema without treating it as an authorised feature request. |

An answer should identify its source record and revision, state the relevant
limits and expose missing evidence. Search ranking alone does not establish
that a source can answer the question. If a join, historical window, licence or
calculation is not evidenced, retain the gap instead of inventing a relationship
or deriving a result from a title.
