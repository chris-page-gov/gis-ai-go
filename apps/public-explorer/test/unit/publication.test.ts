import { createHash } from "node:crypto";
import { describe, expect, it } from "vitest";

import { verifyPayloadBytes, verifyPayloadManifest } from "../fixtures/publication";

function digest(value: Uint8Array | string): string {
  return createHash("sha256").update(value).digest("hex");
}

function fixture(): { payload: Record<string, unknown>; script: Uint8Array } {
  const script = new TextEncoder().encode("console.log('accepted');\n");
  const files = [
    { path: ".nojekyll", bytes: 0, sha256: digest(new Uint8Array()) },
    { path: "assets/app.js", bytes: script.byteLength, sha256: digest(script) },
  ];
  const ledger = files.map((entry) => `${entry.sha256}  ${entry.path}\n`).join("");
  return {
    payload: { fileCount: files.length, files, rootSha256: digest(ledger) },
    script,
  };
}

describe("public payload verification", () => {
  it("accepts the exact checksum-rooted manifest and payload bytes", () => {
    const { payload, script } = fixture();
    const entries = verifyPayloadManifest(payload, String(payload.rootSha256));
    verifyPayloadBytes(entries[0]!, new Uint8Array());
    verifyPayloadBytes(entries[1]!, script);
  });

  it("rejects changed public bytes even when the accepted manifest is unchanged", () => {
    const { payload } = fixture();
    const entries = verifyPayloadManifest(payload, String(payload.rootSha256));
    const altered = new TextEncoder().encode("console.log('altered');\n");
    expect(() => verifyPayloadBytes(entries[1]!, altered)).toThrow(/differs from the accepted manifest/u);
  });

  it("rejects a rewritten manifest inventory that retains the accepted root", () => {
    const { payload } = fixture();
    const altered = structuredClone(payload);
    const files = altered.files as Array<Record<string, unknown>>;
    files[1]!.sha256 = digest("altered");
    expect(() => verifyPayloadManifest(altered, String(payload.rootSha256))).toThrow(
      /does not reproduce the accepted payload root/u,
    );
  });
});
