# Find a term without changing its meaning

Owner request: 21 October 2026. Tracking: [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
This additive OKF+ discovery method adds no provider executor, account entitlement,
hosted tool or private-data publication. The product owner owns its scope; offline
build and test contracts enforce its implementation boundary.

A reader can know a concept by its expanded name, abbreviation, code, field name,
another language or a historical spelling. Discovery should expose the retained
forms and their sources. A search match must not become an identity assertion,
a valid join or an executable API field alias.

## Authored source and generated discovery

Markdown with JSON-shaped YAML-LD front matter remains the authored boundary.
The normal offline build produces `term-discovery.json`, advertises it through
the descriptor's `termDiscovery` entry point and includes it in build checksums.
Every entry binds its originating record by SHA-256, source references, review
state, temporal evidence and update metadata. Every lexical occurrence includes
a JSON Pointer into that exact record.

| Form | What is retained | What is not inferred |
| --- | --- | --- |
| Record title, native identifier and IRI | Original identity and title fields | That a title is a concept identifier |
| SKOS preferred, alternative and hidden labels | Literal, declared language and source position | Missing language, translation or equality with another concept |
| SKOS notation | Native value and declared datatype | That a bare code has meaning outside its scheme |
| Qualified lexical form | Text, kind, source and source-stated or project-search authority | That a friendly search phrase is an official synonym |
| Native NGD field | Owner field IRI, spelling and schema position | Interchangeability across feature types or schema versions |
| Native enum or constant | Value, JSON type, order and nested subschema position | A missing definition, unit or mapping to another product |
| Native documentation label | Table and row position, duplicates and exact whitespace | A stable concept IRI, API enum identity or uniqueness |
| Semantic vocabulary term | Full and compact IRI, usage and definition source | Ontology certification, inference or a fetched definition |

Search normalisation uses Unicode NFKC, case folding and surrounding-whitespace
removal only. Original values remain intact. Number, boolean, null, absent field,
empty text and whitespace-only text remain distinct. Repeated labels and multiple
candidate meanings stay visible; search returns the matching form and pointer.

Only recognised JSON Schema subschema positions are traversed for enums and
constants. Property names such as `enum`, examples, defaults and custom annotation
objects are not interpreted as schema keywords. No `$ref` is fetched.
Retained collection schema, queryable and API contract contexts are indexed as
well as field nodes. Repeated constraints keep their distinct source positions;
occurrence counts are not counts of unique categories or concepts.

## Qualified search forms in YAML-LD

This synthetic project-owned extension represents an authored search aid, not a
supplier assertion or cross-scheme mapping:

```json
{
  "okfp:lexicalForm": [{
    "@id": "https://example.org/synthetic-concept/lexical-form/1",
    "@type": "okfp:LexicalForm",
    "rdf:value": {"@value": "small census area", "@language": "en-GB"},
    "okfp:formKind": "search-variant",
    "okfp:authority": "project-search-variant",
    "prov:wasDerivedFrom": [{"@id": "https://example.org/synthetic-source"}]
  }]
}
```

Use source-stated forms only when exact spelling and role are supported. Keep
synonyms, abbreviations, alternative spellings, historical labels, language forms,
native fields and codes separately typed. Deprecated labels need edition and
applicability evidence; finding one does not revive it. Missing release, reference,
collection, effective or metadata-modification dates remain unknown. A release
date and an earlier reference date need not conflict.

The build requires the closed authored lexical-form schema before reading any
records and validates each qualified form against it. The generated discovery
index has its own required schema. Syntax checks do not certify the meaning of
a label or the strength of its evidence.

SKOS `exactMatch` is a strong, transitive concept mapping, not a lexical alias.
`closeMatch`, broader/narrower relations, field bindings, identifier correlations
and `owl:sameAs` have different meanings. This method creates none from matching
text. See the [SKOS reference](https://www.w3.org/TR/skos-reference/) and
[OKF+ profile](../../okf-plus/profile/README.md).

## Local use and limits

After the normal build:

```sh
uv run --locked python scripts/okf_plus/term_discovery.py \
  --index artifacts/okf-plus/bundle/term-discovery.json --query UPRN --limit 20
```

The dedicated machine index can exceed the small-knowledge card ceiling; it is
not sent wholesale to the demo or an assistant. The CLI admits a regular input
of at most 256 MiB, bounds the actual read and rejects changes during that read.
Queries are at most 500 characters and return at most 100 lexical occurrences,
with total matches and truncation explicit. It makes no network requests and
loads no remote context. Consumers must treat text as inert evidence and apply
their own source and navigation policy to links.

Coverage means complete traversal of recognised structures in retained validated
records. It does not mean all geospatial vocabularies, editions, supplier codes
or possible phrases. Unretained lists, unreviewed translations, arbitrary prose
and unrecognised opaque structures remain gaps. A parent record's definition is
not a definition of every enum value in it.

The learning interface uses a smaller authored glossary with source links,
plain-English definitions, scoped aliases and task-specific safeguards. The
large index provides access to source-native material; it does not replace that
glossary, statistical interpretation or original documentation.

The [dated vocabulary investigation](../research/2026-10-21/CONTROLLED_VOCABULARIES.md)
records the scheme families, national and edition differences, native-list
inventory and unresolved external scope. The
[compact learning registry](../../okf-plus/profile/learning-vocabulary.json)
links the selected explanation terms to their authored records and definition
sources. These two views have different denominators.

## Assurance

Synthetic tests reconstruct source positions and cover language, datatype,
typed enum values, duplicates, whitespace, qualified forms, ambiguous matches,
opaque JSON, schema-keyword positions, bounded reads and checksum/descriptor
integration. Full-corpus counts are dated build observations, not manually
maintained assertions. Consumer comprehension and human task completion remain
separate evaluation work. No live provider or semantic-equivalence acceptance
is claimed by this increment.
