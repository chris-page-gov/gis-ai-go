# Local intake planner

This dependency-free package explains user-selected files and web addresses. It
previews small GeoJSON, CSV, TSV and plain-text files in memory, groups Shapefile
companions from selected folders, and inventories bounded local ZIP archives to
find their companion sets automatically. Other formats receive honest next steps.
It does not upload, extract archives, fetch web addresses, execute content or import
features into a provider or database.

```ts
import { planIntake, canPreviewText, inspectZipArchive } from "@gis-ai-go/experience-intake";

const plan = planIntake({
  files: [{ name: "visits.csv", size: 21, text: "place,count\nExample,3" }],
  urls: ["https://example.org/maps/places.shp"],
});

// In a browser, check selection-wide bounds before reading anything.
// Only read a complete File.text() when canPreviewText(file.name, file.size).
// A selected ZIP <= 20 MiB can be read with File.arrayBuffer() and passed to:
// inspectZipArchive(file.name, bytes).
```

`planIntake` accepts untrusted input and enforces a closed descriptor contract.
`canPreviewText` is a convenience check, not a replacement for batch limits.
`inspectZipArchive` accepts a local byte buffer and returns the same result shape.
All return values are data: render strings with text nodes, never `innerHTML`,
Markdown execution or automatic links. URLs with a query or fragment have those
components hidden. Unsigned Shapefile URLs can include clearly labelled candidate
sibling addresses; their existence is not claimed and they are not fetched.

See the [implementation and threat record](../../docs/implementation/EXPERIENCE-221_INGESTION.md),
[request schema](schema/request.v1.schema.json),
[result schema](schema/result.v1.schema.json) and [TypeScript contract](src/types.ts).

## Examples and tests

The three files in `examples/` are synthetic, public training examples. Counts,
place labels and coordinates are invented and must not be used as observations
about real people or places. ZIP tests construct real stored/deflated archives
locally, containing synthetic companion bytes. Those bytes are not presented as
valid map features.

```sh
pnpm --filter @gis-ai-go/experience-intake run test
```

The tests exercise ambiguity, malformed input, geometry structure, coordinates,
quoted table cells, omitted preview rows, untrusted text, folder boundaries,
automatic archive companion discovery and hostile ZIP/URL cases. The strict JSON
parser is a local copy of the existing provider parser so this package does not
pull provider or network capabilities into the browser. Changes to either parser
require reviewing the duplicate-key, nesting and numeric boundary tests.
