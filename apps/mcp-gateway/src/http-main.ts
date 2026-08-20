import { resolve } from "node:path";

import { loadCatalogueSnapshot } from "./catalogue-snapshot.js";
import { createGatewayNodeServer } from "./http-server.js";

const HOST = "127.0.0.1";
const PORT = 8_787;
async function main(): Promise<void> {
  const catalogueRoot = resolve(process.argv[2] ?? "../../artifacts/okf");
  const snapshot = await loadCatalogueSnapshot(catalogueRoot);
  const server = createGatewayNodeServer(snapshot);

  server.listen(PORT, HOST, () => {
    process.stdout.write(
      `GIS AI GO blocked gateway candidate listening on http://${HOST}:${PORT}\n`,
    );
  });

  let stopping = false;
  const stop = (): void => {
    if (stopping) return;
    stopping = true;
    void server.closeGateway().catch(() => {
      process.exitCode = 1;
    });
  };
  process.once("SIGINT", stop);
  process.once("SIGTERM", stop);
}

await main();
