import assert from "node:assert/strict";
import { mkdtemp, mkdir, rm, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { resolve } from "node:path";
import test from "node:test";

import {
  inventoryRegularTree,
  parseCatalogueChecksums,
} from "../../scripts/build-boundary.mjs";
import {
  REQUIRED_WEBMCP_CSP,
  verifyDistributionHtml,
} from "../../scripts/html-boundary.mjs";

const htmlOptions = {
  javascriptPath: "assets/application.js",
  stylesheetPath: "assets/application.css",
};

function productionHtml({ csp = REQUIRED_WEBMCP_CSP, script = "./assets/application.js" } = {}) {
  return `<!doctype html>
<html lang="en-GB">
  <head>
    <meta http-equiv="Content-Security-Policy" content="${csp}">
    <link rel="icon" href="./favicon.svg" type="image/svg+xml">
    <script type="module" src="${script}"></script>
    <link rel="stylesheet" href="./assets/application.css">
  </head>
  <body><form action="./" method="get"></form></body>
</html>`;
}

test("accepts a regular bounded tree and rejects symbolic links", async () => {
  const root = await mkdtemp(resolve(tmpdir(), "gis-ai-go-webmcp-build-"));
  try {
    await mkdir(resolve(root, "nested"));
    await writeFile(resolve(root, "nested", "file.txt"), "safe\n");
    assert.deepEqual(await inventoryRegularTree(root, "test tree"), {
      directories: ["nested"],
      files: ["nested/file.txt"],
    });
    await symlink(resolve(root, "nested", "file.txt"), resolve(root, "linked.txt"));
    await assert.rejects(
      inventoryRegularTree(root, "test tree"),
      /must not contain a symbolic link/,
    );
  } finally {
    await rm(root, { recursive: true, force: true });
  }
});

test("accepts sorted checksum paths and rejects traversal or duplicates", () => {
  const a = "a".repeat(64);
  const b = "b".repeat(64);
  assert.deepEqual(parseCatalogueChecksums(`${a}  a.json\n${b}  nested/b.json\n`), [
    { digest: a, path: "a.json" },
    { digest: b, path: "nested/b.json" },
  ]);
  assert.throws(() => parseCatalogueChecksums(`${a}  ../escape.json\n`), /Unsafe/);
  assert.throws(
    () => parseCatalogueChecksums(`${a}  a.json\n${b}  a.json\n`),
    /unique and sorted/,
  );
});

test("validates the effective CSP and exact generated active assets", () => {
  assert.doesNotThrow(() => verifyDistributionHtml(productionHtml(), htmlOptions));

  const decoy = productionHtml({ csp: "default-src * 'unsafe-inline'" }).replace(
    "</head>",
    `<!-- ${REQUIRED_WEBMCP_CSP} --></head>`,
  );
  assert.throws(
    () => verifyDistributionHtml(decoy, htmlOptions),
    /Content Security Policy has drifted/,
  );

  const protocolRelative = productionHtml().replace(
    'src="./assets/application.js"',
    "src='//attacker.invalid/payload.js'",
  );
  assert.throws(
    () => verifyDistributionHtml(protocolRelative, htmlOptions),
    /must reference exactly/,
  );

  const extraScript = productionHtml().replace(
    "</head>",
    '<script type="module" src="./assets/application.js"></script></head>',
  );
  assert.throws(() => verifyDistributionHtml(extraScript, htmlOptions), /one script element/);
});
