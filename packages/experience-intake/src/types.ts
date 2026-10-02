/** User-selected descriptors only. No path is opened and no URL is fetched. */
export interface IntakeFile {
  name: string;
  size: number;
  relativePath?: string;
  text?: string;
}

export interface IntakeRequest {
  files: IntakeFile[];
  urls?: string[];
}

export type IntakeFormat = "geojson" | "json" | "csv" | "tsv" | "text" | "shapefile"
  | "geopackage" | "geoparquet-candidate" | "raster-candidate" | "gis-document"
  | "geodatabase-candidate" | "archive" | "spreadsheet" | "presentation" | "document"
  | "image" | "url-folder" | "unknown";
export type IntakeStatus = "preview-ready" | "needs-input" | "planned-only" | "blocked";
export interface IntakeIssue { code: string; severity: "information" | "warning" | "error"; message: string }
export interface IntakePreview {
  kind: "geojson" | "table" | "text";
  /** These are local structural observations, never a completeness or safety certificate. */
  summary: string;
  featureCount?: number;
  geometryTypes?: string[];
  coordinateCount?: number;
  nullGeometryCount?: number;
  bounds?: [number, number, number, number];
  fieldNames?: string[];
  fieldNamesOmitted?: number;
  rowCount?: number;
  columnCount?: number;
  rows?: string[][];
  rowsOmitted?: number;
  headerAssumption?: string;
  characterCount?: number;
  lineCount?: number;
  excerpt?: string;
  excerptTruncated?: boolean;
  crs?: string;
  limitations: string[];
}
export interface IntakeItem {
  id: string;
  label: string;
  inputKind: "file" | "file-group" | "url";
  format: IntakeFormat;
  status: IntakeStatus;
  summary: string;
  jit: string;
  nextSteps: string[];
  issues: IntakeIssue[];
  sourceRefs: string[];
  /** Explicit candidate sibling addresses only, not discovered or fetched files. */
  companionSuggestions?: string[];
  preview?: IntakePreview;
}
export interface IntakePlan {
  schemaVersion: "experience-intake.v1";
  status: "empty" | "ready" | "attention" | "blocked";
  items: IntakeItem[];
  issues: IntakeIssue[];
  policy: {
    owner: "GIS AI GO product owner";
    profile: "local-intake-preview-v1";
    networkRequests: 0;
    persistedFiles: 0;
    executesContent: false;
    sharing: "local-preview-only";
  };
  evidence: {
    level: "local-structural-observation";
    fileCount: number;
    declaredBytes: number;
    suppliedTextBytes: number;
    urlCount: number;
    limitation: string;
    archive?: {
      format: "zip";
      compressedBytes: number;
      memberCount: number;
      declaredExpandedBytes: number;
      contentExtracted: false;
      crcVerified: false;
    };
  };
}
