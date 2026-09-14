# WEB-216 X04 and X05: geography and storage

Protocol date: 14 September 2026. These are bounded development experiments under
[WEB-216](WEB-216_PUBLIC_DATA_WORKBENCH.md), not production geography processing,
a complete dataset build or a hosting benchmark.

## X04: what exactly does a place-to-statistic join mean?

The proposed first geographic story is a staff analyst finding the Census area
containing a named place's representative point, then inspecting that area's
occupancy statistics. That is not a claim about the whole named settlement or an
individual household.

The [OS Open Names feature specification](https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/os-open-names/os-open-names-technical-specification/feature-type/namedplace)
provides identifiers, alternative names and language labels, local type and a
British National Grid representative point. Its settlement bounding box is not an
exact settlement boundary. Some administrative context can use the nearest area;
do not turn that text or a context URI into a verified containment join. Exact
package headers, identifiers and release metadata still need to be bound at ingest.

The candidate [ONS MSOA 2021 full-resolution boundary release](https://www.data.gov.uk/dataset/b9d6e8eb-95a8-4a32-832f-e8a746252f43/middle-layer-super-output-areas-december-2021-boundaries-ew-bfc-v7)
covers England and Wales at Census day and is clipped to mean high water. Its
published catalogue describes V7's Welsh-name addition. This is a source candidate,
not evidence that its payload has already been downloaded or validated. A 2026
named point joined to a 2021 area must retain the two different vintages.

ONS [geography licence guidance](https://www.ons.gov.uk/methodology/geography/licences)
requires source attribution and recognises third-party rights. Licence URLs in a
record do not decide rights automatically. The first experiment excludes protected
address data and Northern Ireland postcode products. GB place-name coverage does
not make an England-and-Wales statistic UK-wide.

The [ONS observation guide](https://developer.ons.gov.uk/observations/) describes
a Census-specific response route and area selection, different from the maintained
time-series and CMD routes. TS053 occupancy is a candidate measure, but the exact
current version, area support, categories, missing-value semantics and payload
remain to be checked. Neither the English nor Welsh version-4 publication page
could be retrieved in this inspection; do not infer an API success from that gap.

### Executable synthetic contract

The [pure contract](../../scripts/web216_geography_contract.py) and
[invented fixtures](../../tests/fixtures/web216/geography-join-cases.json) exercise
the failure rules without downloading provider data:

- exact declared CRS and geography vintage; no automatic transformation or repair;
- strictly inside exactly one supported simple polygon;
- edge or overlap is ambiguous; no match is unsupported; never substitute nearest;
- join statistics through the declared identifier, not a name or display label;
- require the complete expected category set and reject duplicate dimension tuples;
- retain source/rights evidence as untrusted descriptive material, not permission.

The polygons, identifiers, coordinates and counts are synthetic. One simple
exterior ring without holes and bounded integer coordinates is a deliberately
restricted test model, not a new GIS
engine suitable for real MSOA geometry. Full-resolution production joins need an
appropriately verified geometry implementation, exact source payloads and coverage
checks. No spatial language model calculation is used.

```bash
python3 -m unittest tests.test_web216_geography_contract -v
```

## X05: which local storage layout is proportionate?

Use the same 339-record pinned comparison corpus as
[X01/X02/X06](WEB-216_EXPERIMENTS.md). Compare:

1. one canonical static JSON record array;
2. local standard-library SQLite, with separate metadata/details tables and
   primary-key identifier lookup;
3. deterministic JSON partitions selected by a record-identifier digest prefix.

Reconstruct the entire original record set from every layout and require equal
canonical content. Rebuild the existing ranking function from each reconstruction
and require identical full ranked identifier lists for all five development
queries. This measures storage correctness, not a new SQL search algorithm or
independent relevance evaluation.

Measure exact persisted file bytes, then at most five identifier samples across
three cold/warm repetitions per layout. Cold means a fresh application reader or
connection, including initialisation; operating-system caches remain uncontrolled.
Warm means repeating that identifier immediately on the same reader. SQLite page
I/O is unknown here, not zero. Static/partition initial application reads are not
compressed HTTP transfer. Record failures, code/input/configuration/output hashes,
UTC times, environment and the precise selected sample identifiers.

```bash
python3 -m unittest tests.test_web216_storage_experiment -v
python3 scripts/web216_storage_experiment.py \
  --corpus <pinned-comparison-corpus.json> \
  --output <fresh-experiment-directory> --repeats 3
```

Local SQLite is not Sites D1. JSON partitions are not Parquet, a columnar query
engine or a measured object-store deployment. Hosting latency, billing, residency,
concurrency and resource limits remain unmeasured. Do not add a database dependency
or claim an optimum on the strength of this small local experiment. The measured
result and provisional implementation choice belong in the
[development journal](../chronicle/WEB-216_JOURNAL.md).
