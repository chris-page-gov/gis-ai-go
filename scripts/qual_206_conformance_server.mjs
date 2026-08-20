import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";

import { createCatalogueApplication } from
  "../apps/mcp-gateway/dist/src/catalogue-application.js";
import { loadCatalogueSnapshot } from
  "../apps/mcp-gateway/dist/src/catalogue-snapshot.js";
import { startCatalogueStdio } from "../apps/mcp-gateway/dist/src/mcp-stdio.js";

const ENABLE_FLAG = "GIS_AI_GO_QUAL_206_CONFORMANCE";
const SOURCE_COMMIT_VARIABLE = "GIS_AI_GO_QUAL_206_SOURCE_COMMIT";
const FIXED_SNAPSHOT_TIME = new Date("2026-08-20T12:00:00Z");
const FIXED_RECEIPT_TIME = new Date("2026-08-20T12:34:56Z");
const STABLE_SEMVER = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$/u;
const FULL_COMMIT = /^[0-9a-f]{40}$/u;

if (process.env[ENABLE_FLAG] !== "1") {
  throw new Error(
    `Refusing to expose the QUAL-206 conformance surface without ${ENABLE_FLAG}=1`,
  );
}

const sourceCommit = process.env[SOURCE_COMMIT_VARIABLE] ?? "";
if (!FULL_COMMIT.test(sourceCommit)) {
  throw new Error(`${SOURCE_COMMIT_VARIABLE} must be a full lowercase Git commit`);
}

const catalogueRoot = fileURLToPath(new URL("../artifacts/okf/", import.meta.url));
const version = (await readFile(new URL("../VERSION", import.meta.url), "utf8")).trim();
if (!STABLE_SEMVER.test(version)) {
  throw new Error("VERSION must contain a stable semantic version");
}

const snapshot = await loadCatalogueSnapshot(catalogueRoot, {
  now: FIXED_SNAPSHOT_TIME,
});
const application = createCatalogueApplication(snapshot, {
  software: {
    name: "gis-ai-go-mcp-gateway",
    version,
    revision: sourceCommit,
  },
  now: () => FIXED_RECEIPT_TIME,
});

const handle = startCatalogueStdio({
  application,
  snapshot,
  enabledOperations: ["catalogue.describe", "catalogue.search"],
  enabledResources: ["catalogue.public", "catalogue.record"],
});

let closing = false;
async function close() {
  if (closing) return;
  closing = true;
  await handle.close();
}

process.once("SIGINT", () => void close());
process.once("SIGTERM", () => void close());
