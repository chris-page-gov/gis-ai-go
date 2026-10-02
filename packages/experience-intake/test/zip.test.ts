import { test } from "node:test";
import assert from "node:assert/strict";
import { deflateRawSync } from "node:zlib";
import { inspectZipArchive, planIntake } from "../src/index.js";

interface Member { name: string; text?: string; deflate?: boolean; descriptor?: boolean; flags?: number; attributes?: number; expandedOverride?: number; extra?: Buffer }
function crc32(bytes: Uint8Array): number {
  let crc = 0xffffffff;
  for (const value of bytes) {
    crc ^= value;
    for (let bit = 0; bit < 8; bit += 1) crc = crc & 1 ? 0xedb88320 ^ (crc >>> 1) : crc >>> 1;
  }
  return (crc ^ 0xffffffff) >>> 0;
}
function archive(members: Member[]): Buffer {
  const locals: Buffer[] = []; const centres: Buffer[] = []; let offset = 0;
  for (const member of members) {
    const name = Buffer.from(member.name); const raw = Buffer.from(member.text ?? "synthetic");
    const compressed = member.deflate ? deflateRawSync(raw) : raw; const method = member.deflate ? 8 : 0;
    const flags = member.flags ?? (0x0800 | (member.descriptor ? 8 : 0)); const crc = crc32(raw);
    const expanded = member.expandedOverride ?? raw.length; const extra = member.extra ?? Buffer.alloc(0);
    const local = Buffer.alloc(30); local.writeUInt32LE(0x04034b50); local.writeUInt16LE(20, 4);
    local.writeUInt16LE(flags, 6); local.writeUInt16LE(method, 8);
    if (!member.descriptor) { local.writeUInt32LE(crc, 14); local.writeUInt32LE(compressed.length, 18); local.writeUInt32LE(expanded, 22); }
    local.writeUInt16LE(name.length, 26); local.writeUInt16LE(extra.length, 28);
    const descriptor = Buffer.alloc(member.descriptor ? 16 : 0);
    if (member.descriptor) { descriptor.writeUInt32LE(0x08074b50); descriptor.writeUInt32LE(crc, 4); descriptor.writeUInt32LE(compressed.length, 8); descriptor.writeUInt32LE(expanded, 12); }
    const localRecord = Buffer.concat([local, name, extra, compressed, descriptor]);
    locals.push(localRecord);
    const central = Buffer.alloc(46); central.writeUInt32LE(0x02014b50); central.writeUInt16LE(0x0314, 4); central.writeUInt16LE(20, 6);
    central.writeUInt16LE(flags, 8); central.writeUInt16LE(method, 10); central.writeUInt32LE(crc, 16);
    central.writeUInt32LE(compressed.length, 20); central.writeUInt32LE(expanded, 24);
    central.writeUInt16LE(name.length, 28); central.writeUInt16LE(extra.length, 30);
    central.writeUInt32LE(member.attributes ?? 0, 38); central.writeUInt32LE(offset, 42);
    centres.push(Buffer.concat([central, name, extra])); offset += localRecord.length;
  }
  const directory = Buffer.concat(centres); const end = Buffer.alloc(22);
  end.writeUInt32LE(0x06054b50); end.writeUInt16LE(members.length, 8); end.writeUInt16LE(members.length, 10);
  end.writeUInt32LE(directory.length, 12); end.writeUInt32LE(offset, 16);
  return Buffer.concat([...locals, directory, end]);
}

test("a real ZIP inventory automatically discovers multiple Shapefile sets without extraction", () => {
  const bytes = archive([
    ...["shp", "shx", "dbf", "prj"].map(ext => ({ name: `one/places.${ext}`, deflate: true })),
    { name: "two/places.shp", descriptor: true, deflate: true }, { name: "README.txt" },
  ]);
  const result = inspectZipArchive("maps.zip", bytes);
  assert.equal(result.status, "attention"); assert.equal(result.items.length, 3);
  const groups = result.items.filter(item => item.format === "shapefile");
  assert.equal(groups.length, 2); assert.equal(groups[0]!.status, "planned-only");
  assert(!groups[0]!.issues.some(issue => issue.code === "missing-shapefile-companions"));
  assert(groups[1]!.issues.some(issue => issue.code === "missing-shapefile-companions"));
  assert.equal(result.evidence.archive?.memberCount, 6);
  assert.equal(result.evidence.archive?.contentExtracted, false); assert.equal(result.evidence.archive?.crcVerified, false);
  assert.equal(result.policy.networkRequests, 0);
  assert(result.issues.some(issue => issue.code === "zip-inventory-only"));
});

test("ZIP parser supports empty archives, explicit folders and exact ArrayBuffer slices", () => {
  assert.equal(inspectZipArchive("empty.zip", archive([])).status, "empty");
  const bytes = archive([{ name: "set/", text: "" }, { name: "set/place.shp" }]);
  const buffer = bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength) as ArrayBuffer;
  assert.equal(inspectZipArchive("set.zip", buffer).items[0]!.format, "shapefile");
});

test("unsafe paths, duplicate names, symlinks, encryption, ZIP64 and excessive expansion are refused", () => {
  const candidates: Member[][] = [
    [{ name: "../place.shp" }], [{ name: "/place.shp" }], [{ name: "C:\\place.shp" }], [{ name: "folder//place.shp" }],
    [{ name: "folder./place.shp" }], [{ name: "place.shp" }, { name: "PLACE.SHP" }],
    [{ name: "link.shp", attributes: (0xa1ff << 16) >>> 0 }], [{ name: "place.shp", flags: 0x0801 }],
    [{ name: "place.shp", deflate: true, expandedOverride: 3_000_000 }],
    [{ name: "place.shp", extra: Buffer.from([1, 0, 0, 0]) }],
    Array.from({ length: 65 }, (_, i) => ({ name: `${i}.txt` })),
    [{ name: "folder/", text: "bad directory data" }],
    [{ name: "folder" }, { name: "folder/place.shp" }],
  ];
  for (const members of candidates) {
    const result = inspectZipArchive("unsafe.zip", archive(members));
    assert.equal(result.status, "blocked", members[0]?.name); assert.equal(result.items.length, 0);
    assert.equal(result.issues[0]!.code, "zip-inspection-refused");
  }
});

test("central and local header disagreements, overlap, truncation and multipart ZIPs fail closed", () => {
  const corruptions: ((bytes: Buffer, central: number) => void)[] = [
    bytes => bytes.writeUInt32LE(0, 0),
    bytes => bytes.writeUInt16LE(8, 8),
    bytes => { bytes[30] = 120; },
    bytes => bytes.writeUInt32LE(99, 18),
    (bytes, central) => bytes.writeUInt32LE(1, central + 42),
    (bytes, central) => bytes.writeUInt32LE(0xffffffff, central + 20),
    bytes => bytes.writeUInt16LE(1, bytes.length - 18),
  ];
  for (const corrupt of corruptions) {
    const bytes = archive([{ name: "place.shp" }]); const central = bytes.readUInt32LE(bytes.length - 6);
    corrupt(bytes, central); assert.equal(inspectZipArchive("bad.zip", bytes).status, "blocked");
  }
  const truncated = archive([{ name: "place.shp" }]).subarray(0, -1);
  assert.equal(inspectZipArchive("bad.zip", truncated).status, "blocked");
  const descriptor = archive([{ name: "place.shp", descriptor: true }]);
  const central = descriptor.readUInt32LE(descriptor.length - 6); descriptor.writeUInt32LE(3, central - 4);
  assert.equal(inspectZipArchive("bad.zip", descriptor).status, "blocked");
});

test("remote Shapefile companion suggestions are explicit and never transfer signed query tokens", () => {
  const result = planIntake({ files: [], urls: ["https://example.org/data/places.shp", "https://example.org/data/places.shp?signature=private"] });
  assert.deepEqual(result.items[0]!.companionSuggestions, ["shp", "shx", "dbf", "prj", "cpg"].map(ext => `https://example.org/data/places.${ext}`));
  assert.equal(result.items[1]!.companionSuggestions, undefined);
  assert.equal(result.policy.networkRequests, 0);
});
