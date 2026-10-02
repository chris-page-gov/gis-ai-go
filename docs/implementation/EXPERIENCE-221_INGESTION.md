# EXPERIENCE-221: files, folders and web addresses

Date: 2 October 2026. Owner: GIS AI GO product owner. Status: local implementation;
hosted deployment and unaided user acceptance are separate evidence gates.

The first working intake slice helps someone understand what they have brought
and what can happen next. The user need is “I have something useful; help me use
it”, without requiring the person to name a format or collect known companions
by hand when a folder or ZIP already contains them.

## What works in this increment

[`packages/experience-intake`](../../packages/experience-intake/README.md) is a
dependency-free, deterministic module. The browser passes descriptors for files
the user selected. Small complete text inputs receive a real structural preview.
Selected folder members are grouped automatically by directory and filename stem.
A bounded ZIP inventory inspects actual local and central headers and discovers
matching Shapefile components without extracting their contents. Multiple
Shapefiles remain separate groups, even when names repeat in different folders.

| Input | Implemented result | Example need and presentation | Plain-language learning summary |
| --- | --- | --- | --- |
| GeoJSON or geographic JSON | Strict JSON and bounded geometry structure, feature count, geometry types, field names and coordinate bounds | “Show what places this file describes.” Summary card and fields, ready for a separate reviewed map renderer | A point marks a place, a line follows a path, and an area has a boundary. Coordinates tell a map where each one goes. |
| CSV or TSV | Actual quoted-cell parsing, row/column counts, first eight rows, omitted-row count | “What does this table contain?” Accessible table, with no guessed heading or location columns | A table puts related facts in rows. Check what each column means before comparing its numbers. |
| Plain text or Markdown | Text length, line count and first 1,200 code units, visibly truncated | “Explain this note.” Plain-text evidence card | Words in a file are evidence to read, not orders for the assistant to obey. |
| Shapefile files or folder selection | Same-stem companion discovery; required `.shp`, `.shx`, `.dbf` and separate `.prj`/`.cpg` checks | “I dropped a folder; find the map inside.” Dataset group and exact missing companions | A Shapefile is a kit. One part holds shapes, another finds them, and another holds their facts. |
| Local ZIP | Bounded actual member inventory, header agreement, automatic companion groups, missing-parts report | “Here is the download ZIP.” Groups for all discovered datasets and an explicit unverified-content note | A ZIP is a bag of files. We can look at its list before opening any of the files inside. |
| Component or folder URL | Address classification; candidate same-stem Shapefile sibling addresses when unsigned; no fetch | “This link is one part; find the rest.” Proposed addresses, clearly unverified | A link points to a place on the web. It does not prove we can open the file or use its contents. |
| GeoPackage, GeoParquet and other binary GIS formats | Name-based classification and specific next steps | “Which layer or shape column should I use?” Planned layer/column picker, not a false import success | One file can hold several layers. Choose the layer that answers your question. |
| Spreadsheets, presentations, documents and images | Name-based classification and format-specific guidance | “Use this chart or spreadsheet.” Planned sheet/slide/page picker with source anchors | A chart picture is not the underlying table. Hidden sheets, notes and footnotes may change its meaning. |

The initial format catalogue also recognises raster/scientific grids, KML/GML/GPX,
FlatGeobuf, point clouds, CAD, map tiles, GIS projects, geodatabase folders and
common archive extensions. **Recognition is not conversion.** An unknown format
gets a useful request for the creating application or an open-format export.
There is no “any spatial file” completeness claim.

## Stable interface contract

`planIntake({files, urls?})` returns `experience-intake.v1`. Each item has a stable
ID, format, status, summary, short `jit` explanation, next steps, findings and
source references. Optional `preview` contains actual local observations;
optional `companionSuggestions` contains proposed sibling addresses only.
`inspectZipArchive(name, bytes)` returns the same shape with `evidence.archive`.

Item statuses are `preview-ready`, `needs-input`, `planned-only` or `blocked`.
The caller must display the status and limitations alongside the attractive
preview. A complete set of Shapefile *names* remains `planned-only` until a
reviewed reader validates and converts the binary contents. ZIP inspection never
sets `contentExtracted` or `crcVerified` to true.

The [request schema](../../packages/experience-intake/schema/request.v1.schema.json)
and [result schema](../../packages/experience-intake/schema/result.v1.schema.json)
describe the closed JSON forms. Binary ZIP bytes are an in-process parameter,
not base64 in MCP arguments. Runtime validation additionally enforces matching
basenames, relative paths and UTF-8 byte budgets.

Limits are explicit: 64 selected files, eight addresses, 20 MiB per descriptor or
ZIP, 50 MiB per selection, complete text previews up to 256 KiB each and 1 MiB in
total. GeoJSON has bounded nesting/JSON values, at most 2,000 features and 10,000
positions. Tables have at most 2,001 rows, 64 columns and 4,096 characters per cell.
The GeoJSON profile is intentionally narrower than RFC 7946: empty coordinate
arrays, more than three coordinate values and legacy `crs` declarations require
further input. It does not check topology, winding, overlaps or positional
accuracy. Bounds are raw coordinate minima/maxima, not a date-line-aware extent.

ZIP inventory supports stored and deflated members and ordinary data descriptors.
It limits all entries, including folders, to 64; declared expanded contents to
50 MiB; individual members to 20 MiB; and expansion to 100:1. It refuses encrypted,
multipart or ZIP64 records, unsupported filename encodings, symlinks, duplicate
or ambiguous paths, traversal, inconsistent headers, overlapping ranges and
unexplained prefixes or gaps. These are inventory checks, not proof that an
untrusted compressed stream will decompress to its declared size. No stream is
decompressed in this increment; every future extractor must enforce actual byte
and CPU limits independently.

## Policy, threat and evidence boundaries

The `local-intake-preview-v1` policy permits local in-memory inspection of
user-selected material. It permits zero network requests, uploads, persistent
files, provider calls, model calls or content execution. No licence decision is
inferred from a file extension or an owner's ability to open a file. The caller
must clear references when the user removes a selection or ends the session.
The module itself owns no persistent store and does not log input.

| Threat or misunderstanding | Implemented boundary | Further gate |
| --- | --- | --- |
| A document tells the assistant to ignore rules | Content remains plain untrusted strings; no instructions execute | Every later model prompt and tool boundary must retain that separation |
| Script/HTML or spreadsheet formula runs in a preview | No execution or rendered markup; caller must use text nodes | Browser integration tests must prove safe rendering |
| ZIP bomb, traversal or hidden extra files | Header, names, entry, size and ratio checks; no extraction | Sandboxed extractor with actual decompressed-byte, time, memory and checksum checks |
| ZIP member `.shp` looks complete but contains invalid data | Companion names and content validity are separate states | Cross-check geometry/index/table counts, types and encoding before conversion |
| URL fetch reaches a private service or leaks credentials | This module never performs DNS or HTTP; local/IP/credentialled forms refused | Approved downloader must validate DNS and every redirect, media type, quota and access authority |
| A signed link is copied to other paths | Query-bearing URLs do not produce sibling suggestions; display hides query/fragment | Provider-specific signed-link semantics must be respected |
| Coordinates are assigned the wrong CRS | Legacy GeoJSON CRS declarations are refused; no reprojection or guessed CSV locations | Source-backed CRS, axis order, units, epoch and deterministic transformation |
| File names or row data expose personal information | No persistence or telemetry; selection is not a sharing decision | Explicit scope/retention/recipient policy before uploading or sending to an AI service |
| An extension or green preview is mistaken for full support | Status and limitations accompany every item | Capability catalogue and end-to-end acceptance must agree |

The returned `evidence` is a deterministic local structural observation. It is
**not** a signed or durable receipt, authenticated source, content hash, rights
determination or import certificate. Durable processing receipts belong to the
later governed ingest workflow. Raw input must not be added to public repository
fixtures or evaluation logs.

## User journeys and next increments

1. **Bring it:** drop/select files, select a folder where the browser supports it,
   or paste an address. File selection stays usable by keyboard. Unsupported
   directory APIs fall back to multi-file selection or ZIP.
2. **Understand it:** show what was actually found, all dataset groups, what can
   be previewed and the next useful action. The JIT explanation stays beside the
   result. Do not make beginners translate a filename into a technical workflow.
3. **Choose meaning:** select layer/sheet/page, heading row, date, units, source,
   rights and location columns. A future importer must capture those choices in
   its receipt; the present preview never invents them.
4. **Use it:** a governed renderer or computation consumes typed validated data.
   Voice should request the same typed action and show the resulting component,
   with keyboard/text alternatives and an undo route. Spoken confirmation cannot
   replace a missing data permission or licence.

Next priorities are a bounded reviewed Shapefile reader and archive extraction;
GeoPackage table/layer/schema inspection; Parquet footer and GeoParquet metadata
inspection; spreadsheet sheet extraction; then source-anchored document and
presentation extraction. Raster and scientific data require band, unit,
resolution, missing-value and CRS choices. GIS project files and virtual rasters
need external-reference controls. Full importers require pinned parsers,
sandboxed execution, fuzz/hostile fixtures, memory/CPU limits, provenance and
governed receipts before activation. GDAL's driver list is a design reference,
not evidence that its readers are installed or safe to invoke here.

For an event with teenagers, begin with the three synthetic examples shipped
with this package and facilitator-controlled files. Ask learners to explain one
finding and one uncertainty. Testing participant accounts, hosted access and
real personal files are separate decisions; the event date/ages/access mode must
be confirmed in the overall experience plan.

## Verification and sources

`pnpm --filter @gis-ai-go/experience-intake run test` builds the package and runs
19 focused tests, including real synthetic stored/deflated ZIPs and malicious
header/path cases. Passing these checks establishes the implemented local
contract; it does not establish hosted browser, Voice or independent-client
acceptance. The overall EXPERIENCE-221 work owns those integration checks.

Primary specifications inspected on 2 October 2026:

- [GeoJSON RFC 7946, August 2016](https://datatracker.ietf.org/doc/html/rfc7946):
  geometry structure and longitude/latitude order.
- [CSV RFC 4180, October 2005](https://datatracker.ietf.org/doc/html/rfc4180):
  quoted cells and optional headings; the preview also accepts LF line endings.
- [Esri Shapefile companion documentation](https://desktop.arcgis.com/en/arcmap/latest/manage-data/shapefiles/shapefile-file-extensions.htm):
  mandatory companions and optional coordinate-system/text-encoding files.
- [PKWARE APPNOTE 6.3.10, 1 November 2022](https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT):
  the ZIP records used by the bounded inventory implementation.
- [GeoPackage 1.4.0](https://www.geopackage.org/spec140/index.html) and
  [GeoParquet 1.1.0](https://geoparquet.org/releases/v1.1.0/): planned metadata
  readers; a missing GeoParquet CRS and an explicitly null CRS have different
  meanings and must not be conflated.
- [OGC GeoTIFF](https://www.ogc.org/standards/geotiff/) and
  [KML](https://www.ogc.org/standards/kml/): format-specific roadmap references.
- [GDAL vector drivers](https://gdal.org/en/stable/drivers/vector/index.html) and
  [raster drivers](https://gdal.org/en/stable/drivers/raster/index.html): broad
  format discovery only; no GDAL installation or invocation is added.
