# Controlled vocabularies and learning terms

Reviewed on 21 October 2026. This is a scoped research and implementation proposal, not a complete inventory of every vocabulary used in UK geospatial or statistical work. It contains 46 authored learning terms, 33 source-family or scheme summaries and a separate, reproducible inventory of recognised structures in the retained repository corpus. Definitions are concise project paraphrases. No provider payload, account information, credential, execution permission or new entitlement is included.

The immediate recommendation is to keep five things distinct: a scheme and its release; an identified concept or code; a lexical form; a native field binding; and a relationship assertion. The same word may participate in all five without making them interchangeable. The UI can explain and search these records now while retaining their source and uncertainty.

The [family matrix](VOCABULARY_FAMILY_MATRIX.md) lists all 33 investigated families,
their recorded versions, source-review depth and remaining work in one table.

The later [selected-list follow-up](CLASSIFICATION_RELEASE_FINDINGS.md) closes bounded address and Census lists and records source discrepancies. Earlier statements below about lists not yet fetched describe the initial investigation, not the later capture.

## What the retained inventory covers

`vocabulary-retained-scope.json` records the dated source inventory. The baseline contained 30,833 Markdown records at commit `c1d16db0aabeb613505536e6af9bdb02f84b9bfb`. The inspected record/profile paths were unchanged from the earlier inspected `d7fa5048bccecd0be7e630f96a2f378721aa5b91`. Every record frontmatter was parsed with duplicate-key and non-finite-number refusal, and every recognised structure was visited. The reproducible inventory method emits exact record IDs, repository-relative paths, record hashes and JSON pointers into a chosen local output directory. Large generated inventories are not committed.

| Retained structure | Count | Meaning and limit |
| --- | ---: | --- |
| NGD navigation code-list URLs | 221 | Individually enumerated routes; a navigation entry does not prove full current content |
| NGD field enum nodes | 1,249 | 20,732 value occurrences across schema/queryable contexts; repeated constraints are not distinct concepts |
| Other OS API contract enum nodes | 119 | Finite operation/parameter constraints, kept separate from NGD business-field vocabularies |
| Documentation native-label tables | 237 | 6,067 retained rows; page/table/row identity and omissions remain significant |
| ONS code-list catalogue entries | 83 | Each native ID and advertised self/edition route; subordinate editions and codes were not all traversed |
| Nomis native SDMX component references | 19,724 | 10,028 distinct native list IDs; dimension, attribute and time roles retained |
| Existing projected Nomis code-list routes | 8,405 | Project-generated route references are inventoried, not newly endorsed as live endpoint syntax |
| Nomis retained time-code lists | 1,617 | 13,814 native rows; available periods are not proof of populated observations or continuity |
| ONS retained version-dimension references | 1,059 | Exact definition and version contexts; category closure is separate |
| ONS population-type records | 39 | Population definitions do not enumerate every subordinate variable or category |

There are 32,532 recognised structural nodes and 9,134 unique advertised or projected controlled-list URLs. These totals have different units and must not be added into a “number of vocabularies”. The external denominator remains unknown. Exact recognised path/key rules are in [`vocabulary_inventory.py`](../../../scripts/okf_plus/vocabulary_inventory.py); unrecognised prose, new provider pages and externally linked lists remain outside that closed scope.

The complete route inventory includes AddressBase code/enumeration navigation and all retained ONS/Nomis list references. The native ONS entries include `sic`, `sic-unofficial`, `soc`, `sex`, `sexual-orientation`, `speak-welsh`, geography and measure families. Dataset-specific Nomis identifiers additionally expose ethnicity, religion, age, disability, qualifications, employment, household and other Census dimensions. These are discovery links, not permission to infer an individual’s characteristics or to merge categories with similar labels. No additional category payloads were fetched.

## Current source checks and important differences

Each registry source records whether its official page was opened and its returned text reviewed, only a search-result extract was reviewed, or a pinned project file was read. No response-byte hash or complete-document preservation is invented for web-tool views. The 2 October retained corpus and 21 October documentation review have separate dates. A source’s edition, effective date, operational adoption, metadata modification and our review date are separate roles.

- [SIC 2026](https://www.ons.gov.uk/methodology/classificationsandstandards/ukstandardindustrialclassificationofeconomicactivities/uksic2026revisionprocess) illustrates why the roles matter: ONS gives an effective date of 14 April 2026 but says the framework is not yet operational across ONS systems, with earliest planned use in the 2031 Blue Book. Existing SIC 2007-based statistics cannot be silently relabelled. Full code tables and correlation mappings remain a separate task.
- [SOC 2020](https://www.ons.gov.uk/methodology/classificationsandstandards/standardoccupationalclassificationsoc/soc2020) separates classification structure, job-title coding index and NS-SEC. A coding-index search expression is not automatically an alternative concept label or an equivalence to an older SOC/ISCO code.
- The [Census ethnic-group dictionary](https://www.ons.gov.uk/census/census2021dictionary/variablesbytopic/ethnicgroupnationalidentitylanguageandreligionvariablescensus2021/ethnicgroup) distinguishes the question, derived variable, classification and category. Different grouped/detailed classifications, applicability and not-applicable codes need their own bindings. Religion and other retained topic references still need their exact dictionaries; this review does not treat category names as universal across nations or Census editions.
- [AddressBase classification](https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/addressbase-fundamentals/classification-scheme) has product-specific depth and a source-stated update of 17 January 2025. Its complete release was not downloaded. Shared examples in [NGD classification documentation](https://docs.os.uk/osngd/code-lists/code-lists-overview/addressclassificationcodevalue) do not establish full release equivalence. A product epoch, feature-schema version and classification release need separate fields.
- England/Wales [RUC 2021](https://www.ons.gov.uk/methodology/geography/geographicalproducts/ruralurbanclassifications/2021ruralurbanclassification), [Scottish 2022 urban/rural classification](https://www.gov.scot/publications/scottish-government-urban-rural-classification-2022/pages/overview/) and [Northern Ireland settlement classifications](https://www.nisra.gov.uk/support/geography/urban-rural-classification) are distinct. NI’s described 2005/2015 settlement products must not be filled with E/W or Scottish codes. Complete national lookup and successor coverage is not established.
- OAC, English IMD, WIMD, SIMD and NIMDM retain nation, edition, geography and hierarchy/domain. Rank is neither a quantity of deprivation nor an individual characteristic. The WIMD series’ October 2026 children’s analysis is not itself a new classification edition.
- NGD has documented case and version changes, such as positional-accuracy labels. Preserve native spelling and edition; case-folding is a search operation, not a source correction. Access Level’s “Surface Level” needs its field context. A compound `buildinguse` representation has its own rule and is not a new fused concept.
- Linked Identifiers edges preserve method, direction, source/target type and version. They are neither lexical synonyms nor `owl:sameAs`. Method-specific relationships must not become transitive identity, building classification, road access or containment claims.

## Proposed representation

The current project record shape already permits prefixed fields, has pinned context prefixes for RDF, SKOS and PROV, and preserves native evidence. The proposed lexical extension is closed by [`lexical-form.schema.json`](../../../okf-plus/schemas/lexical-form.schema.json); the schema constrains syntax only and does not prove semantic correctness.

Use `skos:prefLabel` for the authored display label, with its language. Put genuinely source-stated abbreviations in `skos:altLabel` only when they denote the same scoped concept. Preserve each qualified form separately with `rdf:value`, `okfp:formKind`, `okfp:authority` and one or more `prov:wasDerivedFrom` URLs. Unknown language is absent on the RDF literal and `null` in the UI registry; it is not guessed from the surrounding English page. Project search variants use `okfp:authority: project-search-variant`, never a promoted synonym relation. Every qualified form is also present in the Markdown body for ordinary retrieval.

A native field name, code/notation, URI, language tag, historical label and abbreviation are different form kinds. Keep code identity scoped to scheme, release and owner field where appropriate. A lexical collision should return multiple labelled candidates. Neither normalised search text nor shared native spelling creates `skos:exactMatch`, `owl:sameAs` or `owl:equivalentClass`. SKOS exactMatch is a strong, transitive cross-scheme mapping and needs separately reviewed evidence. No such mapping is emitted here.

SKOS-XL is a candidate when labels themselves require identities/history; adopting it needs a pinned context/profile change. DCAT describes catalogue resources, PROV describes derivation, OWL expresses formal semantics, and SOSA/SSN models observations. Their presence does not make every dataset row an observation, every code a concept or every diagram an ontology. GeoSPARQL, CRS and unit vocabularies likewise require exact versions and field bindings. QUDT is a candidate source with no release pin or automatic unit conversion admitted.

For a future governed scheme record, require publisher, scheme identity, release identifier (or explicit unknown), jurisdiction, native language/notation, publication/effective/adoption dates with role labels, deprecation/replacement evidence and exact source locators. For a mapping assertion, additionally require both identities/editions, relation kind, direction, method, reviewer and scope. Keep these separate from the simple glossary fixture; do not fabricate missing metadata to satisfy a form.

## Implementation and validation

The [compact registry](../../../okf-plus/profile/learning-vocabulary.json) links all
46 terms to their actual Markdown records. Forty authored draft records are new;
six additions reuse the existing UPRN, USRN, TOID, geodetic datum, coordinate
reference system and unit-of-measure identities. Their original definitions,
scope assertions and Markdown prose remain intact. The new forms are appended as
source-qualified learning information, without new equivalence assertions.

The complete current corpus has 30,873 records after adding those forty concepts.
Schema-aware inventory corrected the initial research count by one: the
`Queryable.properties.enum` property describes an enum-valued field but is not
itself a JSON Schema enum constraint. API contract enum nodes are therefore 119,
not 120. NGD counts remain unchanged. The walker follows known subschema keyword
positions and leaves examples, defaults, custom annotations and remote references
opaque. A property called `enum` or `const` is a property name; only a constraint
inside its schema is counted.

Owner: the OKF+ maintainers. This is an offline metadata method, with no provider
executor, credential use or network access. Its input is the existing strict
JSON-shaped Markdown corpus; its output is a generated summary, source inventory,
recognised nodes and retained routes. Source text cannot authorise requests or
promote lexical matches into identity. Output is written only to a new directory;
existing output is refused. Unrecognised external vocabulary scope remains open.

Reproduce the inventory from the repository root:

```sh
python -m scripts.okf_plus.vocabulary_inventory --repo . --output /tmp/okf-vocabulary-inventory
```

The output directory must not already exist. Generated inventory files are local
review artefacts, not required publication inputs. The compact dated summary here
records the scope and counts, including the distinction between before and after
the authored additions.

Focused tests cover real record-schema validation, the closed lexical-form
contract, unknown language, source-reference closure, Markdown discoverability,
schema annotations, misleading property names, nested subschemas and source-row
multiplicity. They do not certify the meaning of every external category.
Canonical build assurance, semantic review, source drift and publication remain
separate checks. The new project terms are `okfp:LexicalForm`, `okfp:lexicalForm`,
`okfp:formKind` and `okfp:authority`; the existing project namespace resolves them,
while their use is governed by the closed lexical schema rather than a new remote
context. SKOS-XL adoption would still need a separately reviewed profile change.
