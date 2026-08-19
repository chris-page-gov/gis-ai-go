import assert from "node:assert/strict";
import { mkdtemp, mkdir, rm, symlink, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import test from "node:test";

import {
  EXPLORER_GENERATED_MARKER,
  assertPreparedPublicInventory,
  assertSafeBuildRoots,
} from "../../scripts/build-boundary.mjs";

const DIGEST = "0".repeat(64);

async function temporaryTree(run) {
  const root = await mkdtemp(join(tmpdir(), "gis-ai-go-build-boundary-"));
  try {
    await run(root);
  } finally {
    await rm(root, { force: true, recursive: true });
  }
}

async function validTree(root) {
  const publicRoot = join(root, "public");
  const distRoot = join(root, "dist");
  const catalogueRoot = join(publicRoot, "catalogue");
  await mkdir(catalogueRoot, { recursive: true });
  await mkdir(distRoot, { recursive: true });
  await writeFile(join(publicRoot, "favicon.svg"), "<svg xmlns=\"http://www.w3.org/2000/svg\"/>\n");
  await writeFile(join(catalogueRoot, ".explorer-generated"), EXPLORER_GENERATED_MARKER);
  await writeFile(join(catalogueRoot, "CHECKSUMS.sha256"), `${DIGEST}  record.json\n`);
  await writeFile(join(catalogueRoot, "record.json"), "{}\n");
  return { publicRoot, distRoot };
}

test("rejects a symbolic link anywhere in the public input", async () => {
  await temporaryTree(async (root) => {
    const { publicRoot, distRoot } = await validTree(root);
    const benignFile = join(root, "benign-local-file.txt");
    await writeFile(benignFile, "harmless validation value\n");
    await symlink(benignFile, join(publicRoot, "linked-local-file.txt"));

    await assert.rejects(
      assertSafeBuildRoots({ publicRoot, distRoot }),
      /public directory must not contain a symbolic link: linked-local-file\.txt/u,
    );
  });
});

test("rejects an arbitrary extra regular file in the prepared public input", async () => {
  await temporaryTree(async (root) => {
    const { publicRoot, distRoot } = await validTree(root);
    await writeFile(join(publicRoot, "unexpected.txt"), "not allowlisted\n");

    await assert.rejects(
      assertPreparedPublicInventory({ publicRoot, distRoot }),
      /public inventory differs from the generated allowlist/u,
    );
  });
});

test("rejects a distribution root that is itself a symbolic link", async () => {
  await temporaryTree(async (root) => {
    const { publicRoot, distRoot } = await validTree(root);
    const linkedDirectory = join(root, "linked-distribution");
    await rm(distRoot, { recursive: true });
    await mkdir(linkedDirectory);
    await symlink(linkedDirectory, distRoot, "dir");

    await assert.rejects(
      assertSafeBuildRoots({ publicRoot, distRoot }),
      /distribution directory root must not be a symbolic link/u,
    );
  });
});

test("accepts the exact regular prepared-public inventory", async () => {
  await temporaryTree(async (root) => {
    const { publicRoot, distRoot } = await validTree(root);

    assert.deepEqual(await assertPreparedPublicInventory({ publicRoot, distRoot }), [
      "catalogue/.explorer-generated",
      "catalogue/CHECKSUMS.sha256",
      "catalogue/record.json",
      "favicon.svg",
    ]);
  });
});
