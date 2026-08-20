import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import {
  cp,
  mkdtemp,
  mkdir,
  open,
  readFile,
  realpath,
  rm,
  stat,
  symlink,
  truncate,
  unlink,
  writeFile,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";

import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";

const SOURCE_CATALOGUE = fileURLToPath(
  new URL("../../../../artifacts/okf/", import.meta.url),
);

async function withCatalogueCopy(run: (root: string) => Promise<void>): Promise<void> {
  const temporaryBase = await realpath(tmpdir());
  const workspace = await mkdtemp(join(temporaryBase, "gis-ai-go-catalogue-"));
  const root = join(workspace, "okf");
  await cp(SOURCE_CATALOGUE, root, { recursive: true });
  try {
    await run(root);
  } finally {
    await rm(workspace, { recursive: true, force: true });
  }
}

function digest(bytes: Uint8Array): string {
  return createHash("sha256").update(bytes).digest("hex");
}

async function refreshLedgerDigest(root: string, relativePath: string): Promise<void> {
  const checksumPath = join(root, "CHECKSUMS.sha256");
  const replacement = digest(await readFile(join(root, relativePath)));
  const rows = (await readFile(checksumPath, "utf8"))
    .trimEnd()
    .split("\n")
    .map((row) => (row.endsWith(`  ${relativePath}`) ? `${replacement}  ${relativePath}` : row));
  await writeFile(checksumPath, `${rows.join("\n")}\n`, "utf8");
}

test("loads the checksum-verified catalogue as a deeply immutable snapshot", async () => {
  const snapshot = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
    now: new Date("2026-08-20T12:00:00Z"),
  });

  assert.equal(
    snapshot.bundle.id,
    "https://chris-page-gov.github.io/gis-ai-go/id/bundle/public-discovery",
  );
  assert.equal(snapshot.recordsById.size, snapshot.recordCount);
  assert.equal(snapshot.recordsById.get("LR-Q003")?.id, "LR-Q003");
  assert.match(snapshot.contentRootSha256, /^[0-9a-f]{64}$/u);
  assert.match(snapshot.manifestSha256, /^[0-9a-f]{64}$/u);
  assert.equal(snapshot.stale, false);
  assert.equal(snapshot.stalenessWarning, null);
  assert.deepEqual(snapshot.warnings, []);
  assert.equal(Object.isFrozen(snapshot), true);
  assert.equal(Object.isFrozen(snapshot.bundle), true);
  assert.equal(Object.isFrozen(snapshot.bundle.records), true);
  assert.equal(Object.isFrozen(snapshot.bundle.records[0]?.details), true);
  assert.equal("set" in snapshot.recordsById, false);
  assert.throws(() => {
    (snapshot.bundle.records as unknown as CatalogueRecordMutation[]).push({ id: "rogue" });
  }, TypeError);
});

interface CatalogueRecordMutation {
  readonly id: string;
}

test("returns one explicit warning after the catalogue freshness boundary", async () => {
  const snapshot = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
    now: new Date("2026-11-20T00:00:00Z"),
  });
  assert.equal(snapshot.stale, true);
  assert.match(snapshot.stalenessWarning ?? "", /governed snapshot, not current source authority/u);
  assert.deepEqual(snapshot.warnings, [snapshot.stalenessWarning]);
  assert.equal(Object.isFrozen(snapshot.warnings), true);
});

test("rejects checksum corruption", async () => {
  await withCatalogueCopy(async (root) => {
    const bundlePath = join(root, "okf-bundle.json");
    await writeFile(bundlePath, Buffer.concat([await readFile(bundlePath), Buffer.from("\n")]));
    await assert.rejects(loadCatalogueSnapshot(root), /checksum mismatch for okf-bundle\.json/u);
  });
});

test("rejects both unexpected and missing inventory entries", async (t) => {
  await t.test("unexpected file", async () => {
    await withCatalogueCopy(async (root) => {
      await writeFile(join(root, "unexpected.txt"), "not governed\n", "utf8");
      await assert.rejects(loadCatalogueSnapshot(root), /missing or unexpected files/u);
    });
  });
  await t.test("missing file", async () => {
    await withCatalogueCopy(async (root) => {
      await unlink(join(root, "index.md"));
      await assert.rejects(loadCatalogueSnapshot(root), /missing or unexpected files/u);
    });
  });
});

test("streams and rejects an oversized single-directory inventory", async () => {
  await withCatalogueCopy(async (root) => {
    const oversizedDirectory = join(root, "oversized");
    await mkdir(oversizedDirectory);
    for (let index = 0; index < 1_100; index += 1) {
      await mkdir(join(oversizedDirectory, `entry-${index.toString().padStart(4, "0")}`));
    }

    await assert.rejects(
      loadCatalogueSnapshot(root),
      /catalogue inventory exceeds 1000 directories/u,
    );
  });
});

test("rejects same-inode growth with an exact-length bounded read", async () => {
  await withCatalogueCopy(async (root) => {
    const markerPath = join(root, ".okf-generated");
    const markerBefore = await stat(markerPath);
    const markerSize = markerBefore.size;
    const probe = await open(markerPath, "r");

    type BoundedRead = (
      this: { readonly fd: number },
      buffer: Buffer,
      offset: number,
      length: number,
      position: number,
    ) => Promise<{ bytesRead: number; buffer: Buffer }>;
    const fileHandlePrototype = Object.getPrototypeOf(probe) as { read: BoundedRead };
    const originalRead = fileHandlePrototype.read;
    await probe.close();

    let growthInjected = false;
    let requestedLength: number | undefined;
    let bufferLength: number | undefined;
    fileHandlePrototype.read = async function (buffer, offset, length, position) {
      if (!growthInjected) {
        growthInjected = true;
        requestedLength = length;
        bufferLength = buffer.byteLength;
        await truncate(markerPath, markerSize + 8 * 1024 * 1024);
      }
      return originalRead.call(this, buffer, offset, length, position);
    };

    try {
      await assert.rejects(
        loadCatalogueSnapshot(root),
        /catalogue inventory changed while it was being verified/u,
      );
    } finally {
      fileHandlePrototype.read = originalRead;
    }

    assert.equal(growthInjected, true);
    assert.equal(requestedLength, markerSize + 1);
    assert.equal(bufferLength, markerSize + 1);
    const markerAfter = await stat(markerPath);
    assert.equal(markerAfter.ino, markerBefore.ino);
    assert.equal(markerAfter.size, markerSize + 8 * 1024 * 1024);
  });
});

test("rejects symbolic links in the root path and inventory", async (t) => {
  await t.test("root alias", async () => {
    await withCatalogueCopy(async (root) => {
      const alias = join(dirname(root), "catalogue-alias");
      await symlink(root, alias, "dir");
      await assert.rejects(
        loadCatalogueSnapshot(alias),
        /root and its ancestors must not be symbolic links/u,
      );
    });
  });
  await t.test("inventory entry", async () => {
    await withCatalogueCopy(async (root) => {
      const indexPath = join(root, "index.md");
      await unlink(indexPath);
      await symlink("THIRD_PARTY.md", indexPath, "file");
      await assert.rejects(loadCatalogueSnapshot(root), /inventory contains a symbolic link/u);
    });
  });
});

test("rejects a checksum-valid receipt whose manifest cross-link is false", async () => {
  await withCatalogueCopy(async (root) => {
    const receiptPath = join(root, "build-receipt.json");
    const receipt = JSON.parse(await readFile(receiptPath, "utf8")) as Record<string, unknown>;
    receipt.manifestSha256 = "0".repeat(64);
    await writeFile(receiptPath, `${JSON.stringify(receipt, null, 2)}\n`, "utf8");
    await refreshLedgerDigest(root, "build-receipt.json");

    await assert.rejects(
      loadCatalogueSnapshot(root),
      /manifestSha256 does not match manifest\.json/u,
    );
  });
});
