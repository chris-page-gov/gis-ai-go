import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

import {
  WEBMCP_GENERATED_MARKER,
  inventoryRegularTree,
  verifyChecksummedCatalogue,
} from "./build-boundary.mjs";
import { verifyDistributionHtml } from "./html-boundary.mjs";

const appRoot = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const distRoot = resolve(appRoot, "dist");
const catalogueRoot = resolve(distRoot, "catalogue");
const tree = await inventoryRegularTree(distRoot, "WebMCP Explorer distribution");
const checksums = await verifyChecksummedCatalogue(catalogueRoot, {
  ignoredFiles: [".webmcp-explorer-generated"],
});
const marker = await readFile(resolve(catalogueRoot, ".webmcp-explorer-generated"), "utf8");
if (marker !== WEBMCP_GENERATED_MARKER) {
  throw new Error("WebMCP Explorer distribution catalogue marker is invalid");
}

const javascript = tree.files.filter((path) => /^assets\/[^/]+\.js$/u.test(path));
const stylesheets = tree.files.filter((path) => /^assets\/[^/]+\.css$/u.test(path));
if (javascript.length !== 1 || stylesheets.length !== 1) {
  throw new Error(
    `Expected one JavaScript and one CSS asset; javascript=${javascript.join(",")}; ` +
      `stylesheets=${stylesheets.join(",")}`,
  );
}
if (tree.files.some((path) => path.endsWith(".map"))) {
  throw new Error("WebMCP Explorer distribution must not contain source maps");
}

const expected = [
  "favicon.svg",
  "index.html",
  ...javascript,
  ...stylesheets,
  "catalogue/.webmcp-explorer-generated",
  "catalogue/CHECKSUMS.sha256",
  ...checksums.map(({ path }) => `catalogue/${path}`),
].sort();
const actual = [...tree.files].sort();
if (actual.join("\n") !== expected.join("\n")) {
  throw new Error(
    `WebMCP Explorer distribution differs from the allowlist; ` +
      `expected=${expected.join(",")}; actual=${actual.join(",")}`,
  );
}

const html = await readFile(resolve(distRoot, "index.html"), "utf8");
verifyDistributionHtml(html, {
  javascriptPath: javascript[0],
  stylesheetPath: stylesheets[0],
});

console.log(
  `Verified WebMCP Explorer distribution: ${tree.files.length} regular files, ` +
    `${checksums.length} checksum-bound catalogue files.`,
);
