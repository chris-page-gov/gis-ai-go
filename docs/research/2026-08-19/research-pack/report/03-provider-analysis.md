# Provider analysis: one canonical query model, many preserved authorities

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## Provider integration rule

**Recommendation.** Give clients a coherent canonical selection/result envelope, but preserve provider-native identifiers, fields, source URI, version, licence, update time, error code and query parameters. A canonical model is a convenience layer, not authority over OS, ONS, Nomis, LandIS or HMLR semantics.

## Provider matrix

| Provider lane | Authority/scope | Access | Authentication | Rights and cache position | Recommended integration |
| --- | --- | --- | --- | --- | --- |
| Ordnance Survey | National mapping agency for Great Britain; Great Britain; product-specific | open, PSGA, commercial | Project API key or OAuth 2 client credentials for supported APIs; not user-delegated OAuth | Product and customer agreement specific Must be evaluated per product and entitlement; derived-data constraints may apply | Server-side adapter and credential broker; separate protected caches; preserve native identifiers and version metadata |
| ONS Data API | Official statistics publisher; UK statistics; dataset-specific | open | Public access for open endpoints | Open Government Licence where stated Respect dataset terms and API fair use; prefer frozen metadata and bulk data where appropriate | OKF for discovery; live validation at execution; version-bound observation retrieval |
| ONS Geography and Open Geography Portal | Official statistical geography authority for England and Wales, with UK products where published; England and Wales plus UK-wide products depending on dataset | open | Public | Product-specific ONS/OS/Royal Mail rights; not all geography products have identical rights Record rights per product and vintage | Versioned boundary/code cache with temporal identifier graph and source-native fields |
| Nomis | ONS labour market and census dissemination service; UK; dataset-specific | open | Public; optional API credentials for higher limits | Dataset/source specific, usually OGL with attribution Respect API limits and dataset terms | Discovery through OKF; deterministic query builder; preserve exact dimension order and code lists |
| LandIS | Cranfield University soil information service; England and Wales; product-specific | open, commercial-or-restricted where record terms require | Public for open-access portal; product-specific conditions may remain | Read and enforce each record licence; do not infer one blanket licence from “open access” A local open cache is justified only for explicitly licensed downloadable products and with provenance/scale caveats | Harvest records into OKF and OGC Records crosswalk; cache only licence-confirmed products; expose uncertainty |
| HM Land Registry open publications | Official land registration authority for England and Wales; England and Wales | open | Public for open products | OGL plus additional Royal Mail/OS conditions for some address fields Retain record-level rights and attribution; do not generalise all HMLR data as open | Use as public worked example with explicit legal/fitness warnings and rights metadata |
| HM Land Registry protected and paid services | Official land registration authority for England and Wales; England and Wales | commercial, protected-service | Account, contract and service credentials | Contract, statutory fee and permitted-use specific No caching or redistribution beyond explicit contract and legal authority | Metadata discovery only in first phases; no protected transaction implementation until legal, security and service agreements are complete |

## Ordnance Survey

**Verified fact.** Relevant OS Data Hub OAuth uses a client-credentials flow. The provider token represents a project/workload, not the end user. Replacing a browser-visible key with that token does not create delegated human authority. [S-OS-AUTH] [S-OS-OAUTH-GUIDE]

The platform must authenticate and authorise the human, organisation, agent, host and workload itself, then choose an organisation-owned OS credential under policy. OS OpenData, PSGA and commercial products must be classified separately; caches and derived outputs require product-specific licence evidence. Product end-of-life and NGD migration events belong in the source ledger and capability lifecycle. [S-OS-EOL] [S-OS-NGD] [S-OS-LICENSING]

## ONS Data, ONS Geography and Nomis

These are three lanes:

- ONS Data API: dataset/version/dimension/observation semantics;
- ONS Geography/Open Geography Portal: boundaries, lookups, names/codes, vintages and source-rights variations;
- Nomis: dataset-specific code lists, geography types, suppression and selection limits.

The ONS OKF work demonstrates a sound boundary: static metadata discovers and prepares a non-executing selection plan; a downstream live service validates the current dataset/version/dimensions before retrieving observations. [S-OKF-ONS]

## LandIS

**Verified fact.** The current public portal and OGC API – Records interface support machine-readable discovery. [S-LANDIS] [S-LANDIS-RECORDS]

**Recommendation.** Harvest records and source evidence into OKF. Cache only products whose individual licences permit it. Every soil result must preserve product, survey date, scale, uncertainty, interpreted/raw status and fitness-for-purpose warning. “Open access” is not a sufficient machine policy by itself.

## HMLR worked example

The current HMLR OKF repository is a metadata-only proof of concept and deliberately excludes title registers, plans, searches, personal data, paid documents and credentials. That is the right Stage 1 boundary. [S-OKF-HMLR]

A safe journey is:

1. search/facet HMLR datasets and services in the public OKF pack;
2. inspect authority, rights, freshness, relationships and warnings in a data card;
3. discover that Price Paid Data can answer transaction-price questions but does not prove ownership or exact boundary;
4. identify ONS geography/statistics or LandIS soil enrichment where the licences and semantics permit;
5. create a non-executing selection plan;
6. run a bounded deterministic open query;
7. return source versions, licences, transformations, freshness and policy evidence.

Title ownership, official copies, Business Gateway and licensed bulk products remain metadata-only/deferred until legal, contractual, identity and security prerequisites exist. [S-HMLR-PPD] [S-HMLR-BG]

## UK-wide geography warning

ONS Geography is not a universal UK geography authority for every product. Scotland and Northern Ireland have distinct authorities and products. The provider registry must express geographic jurisdiction and avoid silently projecting England/Wales assumptions across the UK.
