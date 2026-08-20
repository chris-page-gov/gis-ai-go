import { createHash } from "node:crypto";

export type PublicationPayloadEntry = {
  path: string;
  bytes: number;
  sha256: string;
};

const SHA256 = /^[0-9a-f]{64}$/u;
const ENTRY_KEYS = ["bytes", "path", "sha256"];
const PAYLOAD_KEYS = ["fileCount", "files", "rootSha256"];

function sha256(value: Uint8Array | string): string {
  return createHash("sha256").update(value).digest("hex");
}

function object(value: unknown, label: string): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) {
    throw new Error(`${label} must be an object`);
  }
  return value as Record<string, unknown>;
}

function exactKeys(value: Record<string, unknown>, expected: string[], label: string): void {
  const actual = Object.keys(value).sort();
  if (actual.join("\n") !== expected.join("\n")) {
    throw new Error(`${label} has unexpected fields`);
  }
}

function safePath(value: unknown): string {
  if (typeof value !== "string" || !value || value.startsWith("/") || value.includes("\\")) {
    throw new Error("publication payload path is unsafe");
  }
  const parts = value.split("/");
  if (parts.some((part) => !part || part === "." || part === ".." || part.includes("\0"))) {
    throw new Error("publication payload path is unsafe");
  }
  return value;
}

function utf8Compare(left: string, right: string): number {
  return Buffer.compare(Buffer.from(left, "utf8"), Buffer.from(right, "utf8"));
}

export function encodedPublicationPath(path: string): string {
  return path.split("/").map((part) => encodeURIComponent(part)).join("/");
}

export function verifyPayloadManifest(
  value: unknown,
  expectedRootSha256: string,
): PublicationPayloadEntry[] {
  if (!SHA256.test(expectedRootSha256)) throw new Error("expected payload root is invalid");
  const payload = object(value, "manifest payload");
  exactKeys(payload, PAYLOAD_KEYS, "manifest payload");
  if (!Array.isArray(payload.files) || payload.files.length === 0) {
    throw new Error("manifest payload files must be a non-empty array");
  }

  const entries = payload.files.map((raw, index) => {
    const entry = object(raw, `manifest payload file ${index}`);
    exactKeys(entry, ENTRY_KEYS, `manifest payload file ${index}`);
    const path = safePath(entry.path);
    if (!Number.isSafeInteger(entry.bytes) || Number(entry.bytes) < 0) {
      throw new Error(`manifest payload byte count is invalid: ${path}`);
    }
    if (typeof entry.sha256 !== "string" || !SHA256.test(entry.sha256)) {
      throw new Error(`manifest payload digest is invalid: ${path}`);
    }
    return { path, bytes: Number(entry.bytes), sha256: entry.sha256 };
  });

  const sorted = [...entries].sort((left, right) => utf8Compare(left.path, right.path));
  if (entries.map((entry) => entry.path).join("\n") !== sorted.map((entry) => entry.path).join("\n")) {
    throw new Error("manifest payload paths must use canonical UTF-8 order");
  }
  if (new Set(entries.map((entry) => entry.path)).size !== entries.length) {
    throw new Error("manifest payload paths must be unique");
  }
  if (payload.fileCount !== entries.length) {
    throw new Error("manifest payload file count does not match its inventory");
  }

  const noJekyll = entries.find((entry) => entry.path === ".nojekyll");
  if (!noJekyll || noJekyll.bytes !== 0 || noJekyll.sha256 !== sha256(new Uint8Array())) {
    throw new Error("manifest payload must bind the empty .nojekyll control file");
  }
  const ledger = entries
    .map((entry) => `${entry.sha256}  ${entry.path}\n`)
    .join("");
  const actualRoot = sha256(ledger);
  if (payload.rootSha256 !== expectedRootSha256 || actualRoot !== expectedRootSha256) {
    throw new Error("manifest payload inventory does not reproduce the accepted payload root");
  }
  return entries;
}

export function verifyPayloadBytes(entry: PublicationPayloadEntry, value: Uint8Array): void {
  if (value.byteLength !== entry.bytes || sha256(value) !== entry.sha256) {
    throw new Error(`public payload differs from the accepted manifest: ${entry.path}`);
  }
}
