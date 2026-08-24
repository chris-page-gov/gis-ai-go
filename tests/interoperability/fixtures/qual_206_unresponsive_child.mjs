import { mkdirSync, writeFileSync, writeSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";

const stateDirectory = join(tmpdir(), "state-that-requires-parent-cleanup");
mkdirSync(stateDirectory, { recursive: true });
writeFileSync(join(stateDirectory, "marker"), "unresponsive child state\n", "utf8");

process.on("SIGTERM", () => {
  // Deliberately ignore graceful termination to exercise the SIGKILL path.
});
process.stdin.resume();
setInterval(() => {}, 60_000);
writeSync(3, `${JSON.stringify({ event: "ready" })}\n`, undefined, "utf8");
