import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

import type { StdioServerHandle } from "@modelcontextprotocol/server/stdio";

import { createCatalogueApplication } from "./catalogue-application.js";
import { loadCatalogueSnapshot } from "./catalogue-snapshot.js";
import { gatewayMetadata } from "./metadata.js";
import { startCatalogueStdio } from "./mcp-stdio.js";

/**
 * Start the protocol-clean process entry. Tool and resource activation comes
 * only from the frozen application activation document.
 */
export async function runCatalogueStdioMain(
  catalogueRootArgument?: string,
): Promise<StdioServerHandle> {
  const catalogueRoot = resolve(catalogueRootArgument ?? "../../artifacts/okf");
  const snapshot = await loadCatalogueSnapshot(catalogueRoot);
  const application = createCatalogueApplication(snapshot, {
    software: {
      name: "gis-ai-go-mcp-gateway",
      version: gatewayMetadata.version,
      revision: snapshot.revision,
    },
  });
  return startCatalogueStdio({ application, snapshot });
}

const entryPath = process.argv[1];
if (
  entryPath !== undefined &&
  import.meta.url === pathToFileURL(resolve(entryPath)).href
) {
  try {
    await runCatalogueStdioMain(process.argv[2]);
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown startup failure";
    process.stderr.write(`GIS AI GO MCP STDIO startup failed: ${message}\n`);
    process.exitCode = 1;
  }
}
