import { INTAKE_LIMITS, planIntake } from "./index.js";
import type { IntakeFile, IntakePlan } from "./types.js";

const CENTRAL = 0x02014b50;
const LOCAL = 0x04034b50;
const END = 0x06054b50;
const DESCRIPTOR = 0x08074b50;
const UTF8 = new TextDecoder("utf-8", { fatal: true });
function fail(message: string): never { throw new Error(message); }

/** Inventory only: inspect headers and discover companions without decompression. */
export function inspectZipArchive(name: string, input: ArrayBuffer | Uint8Array): IntakePlan {
  const blocked = (message: string): IntakePlan => {
    const plan = planIntake({ files: [] });
    plan.status = "blocked";
    plan.issues.push({ code: "zip-inspection-refused", severity: "error", message });
    return plan;
  };
  if (typeof name !== "string" || !name.toLowerCase().endsWith(".zip") || /[/\\\u0000-\u001f]/u.test(name) || name.length > 255) return blocked("Select a local file with a .zip name.");
  if (!(input instanceof ArrayBuffer) && !(input instanceof Uint8Array)) return blocked("Provide the selected ZIP bytes, not a path or web address.");
  const data = input instanceof Uint8Array ? input : new Uint8Array(input);
  if (data.byteLength > INTAKE_LIMITS.fileBytes || data.byteLength < 22) return blocked("The ZIP must be complete and no larger than 20 MiB.");
  const view = new DataView(data.buffer, data.byteOffset, data.byteLength);
  const u16 = (offset: number): number => view.getUint16(offset, true);
  const u32 = (offset: number): number => view.getUint32(offset, true);
  const slice = (offset: number, length: number): Uint8Array => {
    if (offset < 0 || length < 0 || offset + length > data.byteLength) fail("A ZIP header points outside the selected file.");
    return data.subarray(offset, offset + length);
  };
  const sameBytes = (a: Uint8Array, b: Uint8Array): boolean => a.length === b.length && a.every((value, index) => b[index] === value);
  const extras = (start: number, length: number): void => {
    const end = start + length;
    while (start < end) {
      if (start + 4 > end) fail("A ZIP extra field is incomplete.");
      const type = u16(start); const size = u16(start + 2); start += 4;
      if ([0x0001, 0x0017, 0x9901].includes(type)) fail("ZIP64 and encrypted ZIP members need a separate reviewed reader.");
      // Alternate Unicode paths can disagree with the actual member name.
      if (type === 0x7075) fail("Alternate ZIP filename encodings need a separate reviewed reader.");
      if (start + size > end) fail("A ZIP extra field extends past its header.");
      start += size;
    }
  };
  try {
    let end = -1;
    for (let offset = data.length - 22; offset >= Math.max(0, data.length - 65_557); offset -= 1) {
      if (u32(offset) === END && offset + 22 + u16(offset + 20) === data.length) { end = offset; break; }
    }
    if (end < 0) fail("A complete ZIP end record was not found. Download the complete archive first.");
    if (u16(end + 4) !== 0 || u16(end + 6) !== 0 || u16(end + 8) !== u16(end + 10)) fail("Multipart ZIP archives are outside this preview profile.");
    const count = u16(end + 10); const centralSize = u32(end + 12); const centralStart = u32(end + 16);
    if (count === 0xffff || centralSize === 0xffffffff || centralStart === 0xffffffff) fail("ZIP64 archives are outside this preview profile.");
    if (count > INTAKE_LIMITS.files) fail("The ZIP inventory is limited to 64 entries, including folders.");
    if (centralStart + centralSize !== end || centralStart > end) fail("The ZIP central directory does not match the selected file.");
    let cursor = centralStart; let expanded = 0;
    const files: IntakeFile[] = [];
    const names = new Set<string>();
    const fileNames = new Set<string>();
    const extents: { start: number; end: number }[] = [];
    for (let index = 0; index < count; index += 1) {
      if (cursor + 46 > end || u32(cursor) !== CENTRAL) fail("A ZIP member header is missing or incomplete.");
      const flags = u16(cursor + 8); const method = u16(cursor + 10); const crc = u32(cursor + 16);
      const compressedSize = u32(cursor + 20); const expandedSize = u32(cursor + 24);
      const nameLength = u16(cursor + 28); const extraLength = u16(cursor + 30); const commentLength = u16(cursor + 32);
      const attributes = u32(cursor + 38); const localStart = u32(cursor + 42);
      const centralEnd = cursor + 46 + nameLength + extraLength + commentLength;
      if (centralEnd > end || !nameLength) fail("A ZIP filename or member record is incomplete.");
      if (flags & ~0x080e) fail("Encrypted or unsupported ZIP flags are outside this preview profile.");
      if (![0, 8].includes(method)) fail("Only stored and deflated ZIP members can be inventoried by this profile.");
      if (u16(cursor + 34) !== 0 || [compressedSize, expandedSize, localStart].includes(0xffffffff)) fail("Multipart and ZIP64 members are outside this preview profile.");
      if ((attributes >>> 16 & 0xf000) === 0xa000) fail("ZIP symbolic links are refused.");
      const nameBytes = slice(cursor + 46, nameLength);
      if (!(flags & 0x0800) && nameBytes.some(byte => byte > 127)) fail("Non-UTF-8 ZIP filenames need a separate reviewed reader.");
      const path = UTF8.decode(nameBytes);
      const directory = path.endsWith("/");
      const normal = directory ? path.slice(0, -1) : path;
      if (!normal || normal.length > 1_024 || /[\\:\u0000-\u001f\u007f]/u.test(normal) || normal.startsWith("/")
        || normal.split("/").some(part => !part || part === "." || part === ".." || /[. ]$/u.test(part))) fail("A ZIP member has an unsafe absolute, traversal or ambiguous filename.");
      const key = normal.normalize("NFC").toLowerCase();
      if (names.has(key)) fail("Duplicate or case-conflicting ZIP member names are refused.");
      names.add(key);
      if (!directory) fileNames.add(key);
      if (expandedSize > INTAKE_LIMITS.fileBytes) fail("An expanded ZIP member exceeds the 20 MiB member limit.");
      expanded += expandedSize;
      if (expanded > INTAKE_LIMITS.totalBytes) fail("The ZIP declares more than 50 MiB of expanded data.");
      if (expandedSize > Math.max(1, compressedSize) * 100) fail("A ZIP member expands by more than the permitted 100:1 ratio.");
      if (method === 0 && compressedSize !== expandedSize) fail("A stored ZIP member has inconsistent sizes.");
      if (directory && (compressedSize || expandedSize)) fail("A ZIP folder unexpectedly contains data.");
      extras(cursor + 46 + nameLength, extraLength);
      if (localStart + 30 > centralStart || u32(localStart) !== LOCAL) fail("A ZIP local header is missing or overlaps its directory.");
      if (u16(localStart + 6) !== flags || u16(localStart + 8) !== method) fail("ZIP local and central flags or compression methods disagree.");
      const localNameLength = u16(localStart + 26); const localExtraLength = u16(localStart + 28);
      const payloadStart = localStart + 30 + localNameLength + localExtraLength;
      if (payloadStart > centralStart || !sameBytes(nameBytes, slice(localStart + 30, localNameLength))) fail("ZIP local and central filenames disagree.");
      extras(localStart + 30 + localNameLength, localExtraLength);
      let memberEnd = payloadStart + compressedSize;
      if (memberEnd > centralStart) fail("A ZIP member overlaps the central directory.");
      const localCrc = u32(localStart + 14); const localCompressed = u32(localStart + 18); const localExpanded = u32(localStart + 22);
      if (flags & 0x0008) {
        if ((localCrc !== 0 && localCrc !== crc) || (localCompressed !== 0 && localCompressed !== compressedSize)
          || (localExpanded !== 0 && localExpanded !== expandedSize)) fail("A ZIP local size or checksum declaration disagrees with its directory.");
        if (memberEnd + 12 > centralStart) fail("A ZIP data descriptor is incomplete.");
        if (u32(memberEnd) === DESCRIPTOR) memberEnd += 4;
        if (memberEnd + 12 > centralStart || u32(memberEnd) !== crc || u32(memberEnd + 4) !== compressedSize || u32(memberEnd + 8) !== expandedSize) fail("A ZIP data descriptor disagrees with its directory.");
        memberEnd += 12;
      } else if (localCrc !== crc || localCompressed !== compressedSize || localExpanded !== expandedSize) fail("ZIP local and central sizes or checksum declarations disagree.");
      extents.push({ start: localStart, end: memberEnd });
      if (!directory) files.push({ name: normal.split("/").at(-1)!, relativePath: normal, size: expandedSize });
      cursor = centralEnd;
    }
    if (cursor !== end) fail("Unexpected extra records occur in the ZIP central directory.");
    for (const path of names) {
      const parts = path.split("/");
      for (let count = 1; count < parts.length; count += 1) {
        if (fileNames.has(parts.slice(0, count).join("/"))) fail("A ZIP path uses another file as a folder.");
      }
    }
    extents.sort((a, b) => a.start - b.start);
    let next = 0;
    for (const extent of extents) {
      if (extent.start !== next) fail("ZIP members overlap or contain an unexplained gap or executable prefix.");
      next = extent.end;
    }
    if (next !== centralStart) fail("The ZIP contains an unexplained gap before its directory.");
    const result = planIntake({ files });
    if (result.status === "blocked") return result;
    result.evidence.archive = { format: "zip", compressedBytes: data.byteLength, memberCount: count,
      declaredExpandedBytes: expanded, contentExtracted: false, crcVerified: false };
    result.issues.push({ code: "zip-inventory-only", severity: "information", message:
      `${count} ZIP entries inspected locally. Matching Shapefile companions were grouped automatically. No file was extracted; checksums, compressed content and map features remain unverified.` });
    return result;
  } catch (error) { return blocked(error instanceof Error ? error.message : "The ZIP could not be inventoried safely."); }
}
