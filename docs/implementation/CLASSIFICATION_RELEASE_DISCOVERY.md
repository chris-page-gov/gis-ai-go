# Explore a classification without losing its context

For long reference entries, expand **Limits for this entry's scheme** or
**Other occurrences of this code** when needed. Definitions and source links
remain available without expanding either section. The comparison count is
visible while folded; equal code text does not establish equivalent concepts.

When exploring access to a site, introduce direction, mechanism and restrictions
before following an identifier. A site's primary-building UPRN does not enumerate
every address on the site. When reading a map label, check whether a field measures
the text's rendering height or a physical building: these answer different questions.
The [dated findings](../research/2026-10-21/CLASSIFICATION_RELEASE_FINDINGS.md)
record the selected Sites and VectorMap source distinctions and open dependencies.

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
Optional [label-origin metadata](../../examples/geography-task-experience/LABEL-ORIGIN.md)
distinguishes exact source labels from project display fallbacks. An explicit
fallback remains a readable record title but emits neither `skos:prefLabel` nor
`rdfs:label`. Its title occurrence carries an origin marker in discovery; no
supplier alias or source-native lexical form is inferred. Native code, absent or
null value, language evidence and exact source pointer remain available. Legacy
payloads retain their earlier behaviour, not retrospective source attestation.

Uncoded explanatory rows remain documentation records, not additional coded
concepts; their original null, empty or whitespace code is preserved.
The identities also bind the source snapshot hashes, so an unknown supplier
edition cannot silently merge two different captured lists.

A repeated mnemonic can identify different tables on different source pages.
Retain the page, named table and snapshot identity before suggesting a join.
Similarly, a native child-count annotation need not describe the same relation
as an explicit parent-code field: overlapping statistical aggregates may require
separate membership evidence. Preserve both declarations and the unresolved
interpretation. Source `DisplayName` text may be exposed as a qualified
alternative label; it does not create an alias for a provider request parameter.

For OAC and rural/urban domains, keep native hierarchy-label columns and national
variants separate. A guide's complete set of names is not a proved dictionary for
another product's field. In the Census journey, introduce the statistical unit
(for example, households or persons) before asking the reader to compare codes.

```sh
uv run --locked python scripts/okf_plus/classification_release.py \
  --input /private/location/reviewed-classifications.json \
  --output /private/location/new-export \
  --source-revision REVIEWED_PRODUCER_COMMIT
```

Replace `REVIEWED_PRODUCER_COMMIT` with the exact reviewed 40-character lowercase
Git commit for the producer source. The exporter records it as the discovery
index revision and `producerSourceRevision` in its receipt. The payload remains
separately bound by its original and canonical SHA-256 values. Syntax validation
does not establish that a supplied commit is authentic, clean or reviewed: the
caller must bind the executed source and its acceptance evidence. The exporter
does not invent a commit from a payload hash or run Git/provider commands.

Every generated record and the complete discovery index must pass their canonical
schemas before any output directory is created. A native empty label remains valid
in the source/UI projection but cannot satisfy the record schema’s non-empty title;
export refuses it rather than inventing a title or losing the empty string. Earlier exports used a non-Git revision sentinel
that did not satisfy that schema; those historical files remain unchanged and
must not be described as passing this new admission. Existing callers must now
supply the explicit producer revision. Legacy label interpretation is unchanged.

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

A useful next activity is to compare the same code in two schemes, then explain
why matching text is insufficient. For representative point codes, read the full
source definition, including any alternatives, before describing accuracy. For
age or occupation, identify the population, reference date and comparison limits
before choosing a chart. For economic activity, check whether rows are totals,
components or overlapping categories before summing them. These are authored
learning prompts, not assessed learning outcomes.

Complete selected documentation also needs a field-level gap record. A name in a
summary table may lack a definition section; an empty CSV/GML mapping cell does
not prove that the other format lacks the property. Keep source tables, native
schemas, observed headers and tested conversions as separate evidence. Preserve
GML-only metadata and change-delivery requirements rather than silently dropping
them when proposing another format.

The [family matrix](../research/2026-10-21/VOCABULARY_FAMILY_MATRIX.md) retains the
larger denominator. Complete authoritative releases, all definitions, translations,
deprecations, cross-scheme mappings and national variants remain separate gaps.
Automated reconstruction and interface checks do not establish human learning,
assistive-technology acceptance or full domain coverage.
