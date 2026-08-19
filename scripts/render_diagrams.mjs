#!/usr/bin/env node

import { createHash } from "node:crypto";
import { mkdir, readFile, readdir, writeFile } from "node:fs/promises";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import { instance } from "@viz-js/viz";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const sourceDirectory = join(root, "architecture", "source", "dot");
const packageMetadata = JSON.parse(await readFile(join(root, "package.json"), "utf8"));
const rendererPackageVersion = packageMetadata.devDependencies["@viz-js/viz"];
const expectedSources = [
  "components.dot",
  "containers.dot",
  "context.dot",
  "delegated-agent-sequence.dot",
  "evidence-flow.dot",
  "open-tier-sequence.dot",
  "protected-tier-sequence.dot",
  "six-control-spine.dot",
  "webmcp-sequence.dot",
];

function outputArgument(argv) {
  const index = argv.indexOf("--output");
  if (index === -1 || !argv[index + 1]) {
    throw new Error("Usage: render_diagrams.mjs --output <directory>");
  }
  return resolve(root, argv[index + 1]);
}

const outputDirectory = outputArgument(process.argv.slice(2));
const viz = await instance();
const sources = (await readdir(sourceDirectory))
  .filter((name) => name.endsWith(".dot"))
  .sort();

if (JSON.stringify(sources) !== JSON.stringify(expectedSources)) {
  throw new Error(
    `DOT source inventory mismatch: expected ${expectedSources.join(", ")}; ` +
      `found ${sources.join(", ") || "none"}`,
  );
}

await mkdir(outputDirectory, { recursive: true });
const manifest = [];

for (const name of sources) {
  const source = await readFile(join(sourceDirectory, name), "utf8");
  const result = viz.render(source, { engine: "dot", format: "svg" });
  if (result.status !== "success") {
    throw new Error(`${name}: ${result.errors.map((error) => error.message).join("; ")}`);
  }
  const svg = `${result.output.trimEnd()}\n`;
  const repeated = viz.render(source, { engine: "dot", format: "svg" });
  if (repeated.status !== "success" || `${repeated.output.trimEnd()}\n` !== svg) {
    throw new Error(`${name}: repeated render was not byte-for-byte deterministic`);
  }
  const outputName = name.replace(/\.dot$/, ".svg");
  await writeFile(join(outputDirectory, outputName), svg, "utf8");
  manifest.push({
    source: `architecture/source/dot/${name}`,
    output: outputName,
    sha256: createHash("sha256").update(svg).digest("hex"),
  });
}

const receipt = {
  renderer: "@viz-js/viz",
  rendererPackageVersion,
  graphvizVersion: viz.graphvizVersion,
  deterministicRepeat: true,
  diagrams: manifest,
};
await writeFile(
  join(outputDirectory, "manifest.json"),
  `${JSON.stringify(receipt, null, 2)}\n`,
  "utf8",
);
console.log(
  `Rendered ${manifest.length} diagrams with @viz-js/viz ${rendererPackageVersion} ` +
    `(Graphviz ${viz.graphvizVersion}); ` +
    `wrote checksums to ${join(outputDirectory, "manifest.json")}.`,
);
