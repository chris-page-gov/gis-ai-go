# Explore a classification without losing its context

Tracking: [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).
Owner request: 21 October 2026. This increment closes selected list traversal,
not the whole vocabulary domain. It adds no network executor or hosted API.

The Reference pane lets a reader choose a scheme, search a code or label, and
inspect its source, native fields, dates and remaining gaps. A classification is
a set of categories used for a stated purpose. A code has meaning within that
scheme and edition; the same text in another scheme is not automatically the
same category.

## Three separate questions

1. **Have all entries in this selected list been retained?** The expected and
   retained entry counts answer this only when the complete input was processed
   and independently reconstructed.
2. **Are those entries explained?** A label is not necessarily a definition.
   Missing definitions, empty source text and unavailable historical guidance
   remain distinguishable. An explanatory document from an earlier edition does
   not silently define a later list.
3. **Can this code be joined to another product?** Equal codes or labels establish
   a comparison result, not semantic equivalence, product adoption or a valid
   geographic join. Dataset, dimension, population and edition evidence is needed.

AddressBase and NGD address classifications should therefore be compared as
separate source lists. For Census and Nomis, preserve the variable dictionary,
dataset, dimension, category set, statistical population and totals separately.
The dictionary's not-applicable code and an API total can legitimately differ.
Do not sum a total with its component categories or infer personal attributes
from an area classification.

## Reviewed input and YAML-LD

The closed [browser contract](../../okf-plus/schemas/classification-browser.schema.json)
binds every entry to one scheme, one source hash and a source locator. Original
native fields remain in the entry. Source-stated aliases and project search
variants are separately qualified. A missing date is unknown; retrieval time is
not publication, reference or validity time. Hierarchy values are displayed only
when supplied by the reviewed source projection, never derived from code length.
The source title and locator identify what was hashed: for example, an archive's
CSV member or an HTTP response body. A landing-page link with a member hash is
not represented as a checksum of that landing page's HTTP response.

The offline [exporter](../../scripts/okf_plus/classification_release.py) validates
counts, identities, sources and structural limits, then writes one small
Markdown/YAML-LD knowledge card per entry, a checksum manifest, the browser payload
and an existing-format term-discovery index. `skos:notation`, preferred labels and
qualified lexical forms are searchable without creating `sameAs`, `exactMatch`
or a provider query alias. Each card preserves the complete native entry and
the scheme's explicit scope and gaps. Codes shared by different schemes or
entries remain distinct identities.
Uncoded explanatory rows remain documentation records, not additional coded
concepts; their original null, empty or whitespace code is preserved.
The identities also bind the source snapshot hashes, so an unknown supplier
edition cannot silently merge two different captured lists.

```sh
uv run --locked python scripts/okf_plus/classification_release.py \
  --input /private/location/reviewed-classifications.json \
  --output /private/location/new-export
```

Use an existing private parent directory and a new output name. The exporter
refuses overwrite, links and special input files, bounds the input to 16 MiB and
each concept card to 16 KiB, and emits `COMPLETE.json` only after writing the
listed files. A partial failed output is preserved without a completion marker.
The generated index can be larger than a card; query it with the existing bounded
[term-discovery method](GEOSPATIAL_TERM_DISCOVERY.md).

This is a reviewed-input projection, not an arbitrary supplier parser. Structural
validation cannot prove that the input's source interpretation is correct.
Independent source reconstruction and source-specific rights review remain
required. Source bytes, private lists, local paths, models and capture receipts
do not belong in the public repository. The example fixtures are synthetic.

## Learning and remaining acceptance

Use the property journey to introduce address classifications, then the Census
journey to introduce population and category sets. Just-in-time help should
explain a selected code alongside its scheme, without requiring the reader to
read the whole dictionary first. A source definition or source label must remain
distinguishable from authored teaching guidance.

The [family matrix](../research/2026-10-21/VOCABULARY_FAMILY_MATRIX.md) retains the
larger denominator. Complete authoritative releases, all definitions, translations,
deprecations, cross-scheme mappings and national variants remain separate gaps.
Automated reconstruction and interface checks do not establish human learning,
assistive-technology acceptance or full domain coverage.
