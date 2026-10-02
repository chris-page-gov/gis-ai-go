import { previewGeoJson, previewTable, previewText } from "./previews.js";
import type { IntakeFile, IntakeFormat, IntakeItem, IntakeIssue, IntakePlan, IntakeRequest } from "./types.js";
export type * from "./types.js";
export { inspectZipArchive } from "./zip.js";

export const INTAKE_LIMITS = Object.freeze({ files: 64, urls: 8, fileBytes: 20 * 1_024 * 1_024,
  totalBytes: 50 * 1_024 * 1_024, previewBytes: 256 * 1_024, totalPreviewBytes: 1_024 * 1_024 });
const bytes = (value: string): number => new TextEncoder().encode(value).byteLength;
const issue = (code: string, message: string, severity: IntakeIssue["severity"] = "warning"): IntakeIssue => ({ code, severity, message });
const record = (value: unknown): value is Record<string, unknown> => typeof value === "object" && value !== null && !Array.isArray(value);
const extension = (name: string): string => name.toLowerCase().split(".").at(-1) ?? "";
const SHAPE = new Set(["shp", "shx", "dbf", "prj", "cpg", "sbn", "sbx", "fbn", "fbx", "ain", "aih", "ixs", "mxs", "atx", "qix"]);
const SOURCES = {
  geojson: "https://datatracker.ietf.org/doc/html/rfc7946",
  csv: "https://datatracker.ietf.org/doc/html/rfc4180",
  shape: "https://desktop.arcgis.com/en/arcmap/latest/manage-data/shapefiles/shapefile-file-extensions.htm",
  gpkg: "https://www.geopackage.org/spec140/index.html",
  parquet: "https://geoparquet.org/releases/v1.1.0/",
  tiff: "https://www.ogc.org/standards/geotiff/",
  kml: "https://www.ogc.org/standards/kml/",
};

/** A filename hint alone never proves format, rights or safe content. */
export function classifyFile(name: string): IntakeFormat {
  const ext = extension(name);
  if (SHAPE.has(ext) || name.toLowerCase().endsWith(".shp.xml")) return "shapefile";
  if (/(?:^|\/)\w[^/]*\.gdb(?:\/|$)/iu.test(name)) return "geodatabase-candidate";
  if (ext === "geojson") return "geojson";
  if (ext === "json") return "json";
  if (ext === "csv" || ext === "tsv") return ext;
  if (["txt", "md", "log"].includes(ext)) return "text";
  if (ext === "gpkg") return "geopackage";
  if (["geoparquet", "parquet"].includes(ext)) return "geoparquet-candidate";
  if (["tif", "tiff", "cog", "asc", "img", "vrt", "nc", "hdf", "h5", "grib", "grb"].includes(ext)) return "raster-candidate";
  if (["kml", "gml", "gpx", "fgb", "wkt", "wkb", "topojson", "mvt", "pbf", "mbtiles", "pmtiles", "las", "laz", "dxf", "dwg", "tab", "mif", "mid", "qgs", "qgz", "lyr", "lyrx", "aprx"].includes(ext)) return "gis-document";
  if (["zip", "kmz", "gz", "tgz", "tar", "7z", "rar"].includes(ext)) return "archive";
  if (["xls", "xlsx", "xlsm", "xlsb", "ods", "numbers"].includes(ext)) return "spreadsheet";
  if (["ppt", "pptx", "pptm", "odp", "key"].includes(ext)) return "presentation";
  if (["pdf", "doc", "docx", "docm", "odt", "rtf", "html", "htm"].includes(ext)) return "document";
  if (["png", "jpg", "jpeg", "webp", "svg", "heic"].includes(ext)) return "image";
  return "unknown";
}

export function canPreviewText(name: string, size: number): boolean {
  return Number.isSafeInteger(size) && size >= 0 && size <= INTAKE_LIMITS.previewBytes
    && ["geojson", "json", "csv", "tsv", "text"].includes(classifyFile(name));
}

const DESCRIPTIONS: Record<IntakeFormat, { summary: string; jit: string; nextSteps: string[]; sourceRefs: string[] }> = {
  geojson: { summary: "A possible map-data file that can be checked locally.", jit: "GeoJSON stores points, lines and areas with facts about them. Its first coordinate is longitude: how far east or west a place is.", nextSteps: ["Preview a small file, then check who made it and what you may use it for."], sourceRefs: [SOURCES.geojson] },
  json: { summary: "A JSON file; it may or may not contain geographic data.", jit: "JSON is a way to label and group information. A .json name does not tell us whether it contains a map.", nextSteps: ["Try the geographic structure check; other JSON needs a defined schema."], sourceRefs: [SOURCES.geojson] },
  csv: { summary: "A plain-text table that can be previewed locally.", jit: "CSV stores rows of facts separated by commas. A column heading tells you what each fact means.", nextSteps: ["Check the heading row, dates, units and any location columns before using this table."], sourceRefs: [SOURCES.csv] },
  tsv: { summary: "A plain-text table separated by tabs.", jit: "TSV works like CSV, but a tab separates each cell instead of a comma.", nextSteps: ["Check the heading row and tell us which columns matter."], sourceRefs: [SOURCES.csv] },
  text: { summary: "Plain text can be previewed as evidence without following its instructions.", jit: "A text file holds words. Those words may describe a place, but we still need evidence before placing it on a map.", nextSteps: ["Read the short preview and identify its source, date and the question it helps answer."], sourceRefs: [] },
  shapefile: { summary: "A Shapefile is a set of matching files that must travel together.", jit: "A Shapefile is like a small kit: .shp holds shapes, .shx finds them and .dbf holds their facts. The .prj file helps explain their map coordinates.", nextSteps: ["Select the matching files together, or make a ZIP containing them. Conversion is not available in this preview."], sourceRefs: [SOURCES.shape] },
  geopackage: { summary: "A possible GeoPackage; binary inspection and import are not implemented.", jit: "A GeoPackage is one container that can hold several map layers and tables. A layer is one set of related map objects.", nextSteps: ["Use a reviewed importer to list its layers and coordinate systems; choose one layer before conversion."], sourceRefs: [SOURCES.gpkg] },
  "geoparquet-candidate": { summary: "A Parquet filename does not prove that it is GeoParquet.", jit: "Parquet packs large tables efficiently. GeoParquet adds information explaining which columns hold map shapes and how their coordinates work.", nextSteps: ["Inspect the Parquet footer and geo metadata with a reviewed reader before selecting rows or geometry columns."], sourceRefs: [SOURCES.parquet] },
  "raster-candidate": { summary: "A possible raster or scientific grid; decoding is not implemented.", jit: "A raster is a grid of small cells, like picture pixels. Each cell may hold a colour, height, temperature or another measurement.", nextSteps: ["Identify its coordinate system, bands, units, missing values and size before decoding."], sourceRefs: ["https://gdal.org/en/stable/drivers/raster/index.html"] },
  "gis-document": { summary: "A GIS format or project file has been recognised by name only.", jit: "A GIS file may contain shapes, a point cloud, map tiles or instructions for arranging a map. A project file often points to other files it needs.", nextSteps: ["Keep accompanying files together and use a reviewed format-specific reader. External links remain disabled."], sourceRefs: ["https://gdal.org/en/stable/drivers/vector/index.html"] },
  "geodatabase-candidate": { summary: "A possible geodatabase folder; none of its database files have been opened.", jit: "A geodatabase folder is a group of files that work together as a map database. One file alone is usually not useful.", nextSteps: ["Preserve the whole folder and obtain a reviewed database reader before selecting a layer."], sourceRefs: [] },
  archive: { summary: "An archive name is recognised; its file list is checked when a local ZIP is selected.", jit: "A ZIP or other archive is a bag of files. A small bag can expand into a huge amount of data, so its file list and sizes need checks first.", nextSteps: ["Select a local ZIP for bounded inspection and automatic Shapefile companion discovery. Other archive formats need a reviewed reader."], sourceRefs: ["https://pkware.cachefly.net/webdocs/casestudies/APPNOTE.TXT"] },
  spreadsheet: { summary: "A spreadsheet is recognised but sheet extraction is not implemented.", jit: "A spreadsheet can contain many sheets, formulas and hidden cells. A value on screen may be the result of a formula rather than stored data.", nextSteps: ["Export one reviewed sheet as UTF-8 CSV for this preview. Check hidden or personal information first; macros and formulas will not run."], sourceRefs: [] },
  presentation: { summary: "A presentation is recognised but slide extraction is not implemented.", jit: "Slides may contain charts, images and speaker notes. A chart picture does not contain all the numbers needed to check it.", nextSteps: ["Provide the source table or a plain-text extract with slide references; preserve image, chart and note provenance for a future reader."], sourceRefs: [] },
  document: { summary: "A document is recognised but document extraction is not implemented.", jit: "A document may mix words, scanned pages and tables. Copying words out can lose important headings, footnotes or table structure.", nextSteps: ["Provide a short plain-text extract and its page references, or wait for a reviewed document reader. Embedded links and code remain disabled."], sourceRefs: [] },
  image: { summary: "An image is recognised but location, metadata and text extraction are not implemented.", jit: "A map picture shows what someone drew. It does not automatically tell us the real-world coordinates of each pixel.", nextSteps: ["Provide a source and licence. A future image reader must check private metadata and map alignment before use."], sourceRefs: [] },
  "url-folder": { summary: "This address looks like a folder; no directory listing has been requested.", jit: "A web folder address is a signpost, not a list of its contents. The website decides whether you can see or download the files.", nextSteps: ["Provide an explicit file list or download link. Permission and safe downloading need a separate connector."], sourceRefs: [] },
  unknown: { summary: "This format is not recognised by the current intake planner.", jit: "A filename is only a label. We need to know what made the file before choosing a reader safely.", nextSteps: ["Tell us the creating application and data format, or export a small GeoJSON, CSV or plain-text example."], sourceRefs: [] },
};

function item(id: string, label: string, inputKind: IntakeItem["inputKind"], format: IntakeFormat): IntakeItem {
  const description = DESCRIPTIONS[format];
  return { id, label, inputKind, format, status: "planned-only", summary: description.summary, jit: description.jit,
    nextSteps: [...description.nextSteps], issues: [], sourceRefs: [...description.sourceRefs] };
}

function validPath(value: string): boolean {
  return value.length > 0 && value.length <= 1_024 && !/[\u0000-\u001f\u007f\\:]/u.test(value)
    && !value.startsWith("/") && value.split("/").every(part => part !== "" && part !== "." && part !== "..");
}

function validateRequest(input: unknown): input is IntakeRequest {
  if (!record(input) || Object.keys(input).some(key => !["files", "urls"].includes(key)) || !Array.isArray(input.files)
    || input.files.length > INTAKE_LIMITS.files || (input.urls !== undefined && (!Array.isArray(input.urls) || input.urls.length > INTAKE_LIMITS.urls))) return false;
  return input.files.every(file => record(file) && Object.keys(file).every(key => ["name", "size", "relativePath", "text"].includes(key))
    && typeof file.name === "string" && file.name.length > 0 && file.name.length <= 255
    && !/[\u0000-\u001f\u007f/\\:]/u.test(file.name) && ![".", ".."].includes(file.name)
    && typeof file.size === "number" && Number.isSafeInteger(file.size) && file.size >= 0
    && (file.relativePath === undefined || (typeof file.relativePath === "string" && validPath(file.relativePath) && file.relativePath.split("/").at(-1) === file.name))
    && (file.text === undefined || typeof file.text === "string"))
    && (input.urls === undefined || input.urls.every(url => typeof url === "string" && url.length > 0 && url.length <= 2_048));
}

function planFile(file: IntakeFile, id: string): IntakeItem {
  const candidate = item(id, file.name, "file", classifyFile(file.relativePath ?? file.name));
  if (file.size > INTAKE_LIMITS.fileBytes) {
    candidate.status = "blocked";
    candidate.issues.push(issue("file-size-limit", "This file exceeds the 20 MiB planning limit. Make a smaller, reviewed extract.", "error"));
    return candidate;
  }
  if (file.text !== undefined && (bytes(file.text) > INTAKE_LIMITS.previewBytes || file.size > INTAKE_LIMITS.previewBytes)) {
    candidate.status = "blocked";
    candidate.issues.push(issue("preview-size-limit", "Only complete files up to 256 KiB can be previewed. A truncated extract must be saved as a separate file.", "error"));
    return candidate;
  }
  if (!["geojson", "json", "csv", "tsv", "text"].includes(candidate.format)) return candidate;
  if (file.text === undefined) {
    candidate.status = "needs-input";
    candidate.issues.push(issue("contents-not-provided", file.size > INTAKE_LIMITS.previewBytes
      ? "This file is too large for the 256 KiB preview. Select a smaller complete example."
      : "The name was checked, but no file contents were provided to the local preview."));
    return candidate;
  }
  try {
    candidate.preview = candidate.format === "csv" || candidate.format === "tsv"
      ? previewTable(file.text, candidate.format === "csv" ? "," : "\t")
      : candidate.format === "text" ? previewText(file.text) : previewGeoJson(file.text);
    if (candidate.format === "json") candidate.format = "geojson";
    candidate.status = "preview-ready";
    candidate.summary = candidate.preview.summary;
    candidate.issues.push(issue("local-preview-only", "This file stays in the caller's memory. Its rights, accuracy and suitability have not been established.", "information"));
  } catch (error) {
    candidate.status = "needs-input";
    candidate.issues.push(issue("preview-rejected", error instanceof Error ? error.message : "The local structure check failed."));
  }
  return candidate;
}

function shapeGroup(files: IntakeFile[], id: string): IntakeItem {
  const primary = files.find(file => extension(file.name) === "shp") ?? files[0]!;
  const candidate = item(id, primary.name, "file-group", "shapefile");
  const extensions = files.map(file => extension(file.name));
  const missing = ["shp", "shx", "dbf"].filter(ext => !extensions.includes(ext));
  candidate.summary = `${files.length} matching Shapefile companion names checked; their binary contents are unopened.`;
  if (missing.length) {
    candidate.status = "needs-input";
    candidate.issues.push(issue("missing-shapefile-companions", `Add the matching ${missing.map(ext => `.${ext}`).join(", ")} file${missing.length === 1 ? "" : "s"} from the same folder.`));
  }
  if (!extensions.includes("prj")) candidate.issues.push(issue("unknown-crs", "No .prj file was selected. Ask the source which coordinate system it uses; never guess from the numbers."));
  if (!extensions.includes("cpg")) candidate.issues.push(issue("unknown-text-encoding", "No .cpg file was selected. Text encoding must be checked when the table is read."));
  if (extensions.some((ext, index) => extensions.indexOf(ext) !== index)) {
    candidate.status = "needs-input";
    candidate.issues.push(issue("duplicate-companion", "More than one matching companion has the same extension. Choose one consistent export."));
  }
  if (files.some(file => file.size > INTAKE_LIMITS.fileBytes)) {
    candidate.status = "blocked";
    candidate.issues.push(issue("file-size-limit", "A companion exceeds the 20 MiB planning limit. Use a smaller reviewed dataset.", "error"));
  }
  candidate.nextSteps = [missing.length ? "Select the complete matching set together." : "The mandatory companion names are present; a reviewed binary reader must still check their contents.",
    "Confirm the coordinate system, source, licence and date before conversion. No map features have been imported."];
  return candidate;
}

function planUrl(raw: string, id: string): IntakeItem {
  const candidate = item(id, "Web address", "url", "unknown");
  let url: URL;
  try { url = new URL(raw); } catch {
    candidate.status = "blocked"; candidate.issues.push(issue("invalid-url", "Use a complete HTTPS address.", "error")); return candidate;
  }
  const host = url.hostname.toLowerCase();
  if (url.protocol !== "https:" || url.username || url.password || url.port && url.port !== "443"
    || host === "localhost" || host.endsWith(".localhost") || host.endsWith(".local") || !host.includes(".")
    || /^[\d.]+$/u.test(host) || host.includes(":")) {
    candidate.status = "blocked"; candidate.issues.push(issue("url-policy", "Use a public HTTPS address without a password, special port or local network address. Nothing has been fetched.", "error")); return candidate;
  }
  // Show no path, query or fragment: these may contain secrets, names or signed download tokens.
  candidate.label = `https://${host}/…`;
  const isFolder = url.pathname.endsWith("/");
  let path: string;
  try { path = decodeURIComponent(url.pathname); } catch { path = url.pathname; }
  candidate.format = isFolder ? "url-folder" : classifyFile(path);
  const description = DESCRIPTIONS[candidate.format];
  candidate.summary = "Address recognised only; no request, permission check or download has happened.";
  candidate.jit = description.jit;
  candidate.sourceRefs = [...description.sourceRefs];
  candidate.status = "needs-input";
  candidate.nextSteps = [...description.nextSteps, "Use a future approved connector with explicit access, size and redirect checks, or select a permitted local file now."];
  candidate.issues.push(issue("url-not-fetched", "A public-looking name is not proof of public access or a safe network destination. No DNS, redirect or content checks have run."));
  if (url.search || url.hash) candidate.issues.push(issue("url-components-hidden", "The query and fragment are hidden because they may contain access tokens or private information."));
  if (candidate.format === "shapefile") {
    candidate.issues.push(issue("remote-companions-unknown", "Matching companion addresses are suggested, but their existence and access have not been checked."));
    // Signed queries may authorise one object only. Never copy them to sibling addresses.
    if (!url.search && !url.hash) {
      const stem = url.pathname.replace(/\.shp\.xml$/iu, ".shp").replace(/\.[^/.]+$/u, "");
      candidate.companionSuggestions = ["shp", "shx", "dbf", "prj", "cpg"].map(ext => `${url.origin}${stem}.${ext}`);
      candidate.nextSteps.unshift("These same-name companion addresses can be checked by a future approved downloader; selecting a local ZIP finds its actual companions now.");
    }
  }
  return candidate;
}

/** Pure, deterministic and synchronous. Never reads paths, fetches URLs or saves data. */
export function planIntake(input: unknown): IntakePlan {
  const plan: IntakePlan = {
    schemaVersion: "experience-intake.v1", status: "empty", items: [], issues: [],
    policy: { owner: "GIS AI GO product owner", profile: "local-intake-preview-v1", networkRequests: 0, persistedFiles: 0,
      executesContent: false, sharing: "local-preview-only" },
    evidence: { level: "local-structural-observation", fileCount: 0, declaredBytes: 0, suppliedTextBytes: 0, urlCount: 0,
      limitation: "No durable receipt, source authentication, rights determination, content hash, upload, conversion or data import is claimed." },
  };
  if (!validateRequest(input)) {
    plan.status = "blocked";
    plan.issues.push(issue("invalid-request", "Select up to 64 files with safe names and relative folder paths, and up to 8 web addresses. Unknown fields and invalid sizes are refused.", "error"));
    return plan;
  }
  plan.evidence.fileCount = input.files.length;
  plan.evidence.urlCount = input.urls?.length ?? 0;
  plan.evidence.declaredBytes = input.files.reduce((total, file) => total + file.size, 0);
  // Bound string lengths before encoding, so oversized content is not copied into another buffer.
  if (input.files.some(file => (file.text?.length ?? 0) > INTAKE_LIMITS.previewBytes)) {
    plan.status = "blocked"; plan.issues.push(issue("preview-size-limit", "A supplied text file exceeds the 256 KiB preview limit.", "error")); return plan;
  }
  plan.evidence.suppliedTextBytes = input.files.reduce((total, file) => total + (file.text === undefined ? 0 : bytes(file.text)), 0);
  if (plan.evidence.declaredBytes > INTAKE_LIMITS.totalBytes || plan.evidence.suppliedTextBytes > INTAKE_LIMITS.totalPreviewBytes) {
    plan.status = "blocked"; plan.issues.push(issue("batch-size-limit", "Select at most 50 MiB of file descriptors and 1 MiB of preview text in one batch.", "error")); return plan;
  }
  const groups = new Map<string, IntakeFile[]>();
  input.files.forEach((file, index) => {
    const path = file.relativePath ?? file.name;
    if (classifyFile(path) !== "shapefile") { plan.items.push(planFile(file, `file-${index + 1}`)); return; }
    const key = path.replace(/\.shp\.xml$/iu, ".shp").replace(/\.[^.]+$/u, "").toLowerCase();
    const group = groups.get(key) ?? []; group.push(file); groups.set(key, group);
  });
  for (const [index, group] of [...groups.values()].entries()) plan.items.push(shapeGroup(group, `shape-${index + 1}`));
  input.urls?.forEach((url, index) => plan.items.push(planUrl(url, `url-${index + 1}`)));
  plan.status = plan.items.length === 0 ? "empty" : plan.items.every(candidate => candidate.status === "preview-ready") ? "ready"
    : plan.items.every(candidate => candidate.status === "blocked") ? "blocked" : "attention";
  return plan;
}
