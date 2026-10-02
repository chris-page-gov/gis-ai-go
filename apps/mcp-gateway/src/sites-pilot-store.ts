/** Separate experimental Sites store. Never reads or migrates the captured-CPIH store. */
import { createHash } from "node:crypto";
import { canonicalJson } from "@gis-ai-go/evidence/web216-pure";
import type { Web216D1Database } from "@gis-ai-go/evidence/web216-pure";

export const SITES_PILOT_SCHEMA = "gis-ai-go.sites-pilot-evidence.v1";
export const SITES_PILOT_MAX_RECEIPTS = 128;
export const SITES_PILOT_MAX_RESULT_BYTES = 65_536;
export const SITES_PILOT_PROVIDERS = ["os-names", "os-open-data", "ons-cpih", "ons-geography"] as const;
export type PilotProvider = typeof SITES_PILOT_PROVIDERS[number];
export const SITES_PILOT_SQL = Object.freeze({
  schema: [
    `CREATE TABLE IF NOT EXISTS sites_pilot_allowance_v1 (
      provider TEXT PRIMARY KEY, enabled INTEGER NOT NULL CHECK(enabled IN (0,1)),
      used INTEGER NOT NULL CHECK(used >= 0), maximum INTEGER NOT NULL CHECK(maximum BETWEEN 1 AND 200),
      window_start INTEGER NOT NULL, window_used INTEGER NOT NULL CHECK(window_used >= 0))`,
    `CREATE TABLE IF NOT EXISTS sites_pilot_receipts_v1 (
      receipt_id TEXT PRIMARY KEY, created_at TEXT NOT NULL, result_json TEXT NOT NULL
      CHECK(length(CAST(result_json AS BLOB)) <= 65536))`,
  ],
  admit: `UPDATE sites_pilot_allowance_v1 SET used = used + 1,
    window_used = CASE WHEN window_start <= ? THEN 1 ELSE window_used + 1 END,
    window_start = CASE WHEN window_start <= ? THEN ? ELSE window_start END
    WHERE provider = ? AND enabled = 1 AND used < maximum
      AND (window_start <= ? OR window_used < 20)
      AND (SELECT COUNT(*) FROM sites_pilot_receipts_v1) < 128 RETURNING used`,
  insert: `INSERT INTO sites_pilot_receipts_v1 (receipt_id, created_at, result_json)
    SELECT ?, ?, ? WHERE (SELECT COUNT(*) FROM sites_pilot_receipts_v1) < 128
    ON CONFLICT(receipt_id) DO NOTHING RETURNING receipt_id`,
  read: `SELECT result_json FROM sites_pilot_receipts_v1 WHERE receipt_id = ?`,
});
export class SitesPilotStoreError extends Error {
  constructor(public readonly code: "allowance-denied" | "store-unavailable" | "store-full" | "not-found" | "corrupt-evidence") {
    super(code); this.name = "SitesPilotStoreError";
  }
}
export interface PilotEvidence {
  schema: typeof SITES_PILOT_SCHEMA;
  created_at: string;
  software_revision: string;
  parameters_sha256: string;
  data_sha256: string;
  provider_egress: boolean;
  persistence: "d1-append-only-application-contract";
  attestation: "not-attested";
  rollback_protection: "requires-independent-checkpoint";
  receipt_id: string;
}
export interface PilotResult {
  schema: "gis-ai-go.sites-pilot-result.v1";
  tool: string;
  data: Record<string, unknown>;
  evidence: PilotEvidence;
}
export interface PilotStore {
  admit(provider: PilotProvider, now: number): Promise<void>;
  append(result: PilotResult): Promise<void>;
  inspect(receiptId: string): Promise<PilotResult>;
}
export const pilotHash = (value: unknown): string => createHash("sha256").update(canonicalJson(value)).digest("hex");
export function makePilotResult(tool: string, parameters: unknown, data: Record<string, unknown>, revision: string,
  now: Date, providerEgress: boolean): PilotResult {
  if (!/^[0-9a-f]{40}$/.test(revision) || !/^sites_[a-z_]+$/.test(tool)) throw new TypeError("Invalid pilot identity");
  const core: Omit<PilotEvidence, "receipt_id"> = { schema: SITES_PILOT_SCHEMA, created_at: now.toISOString(), software_revision: revision,
    parameters_sha256: pilotHash(parameters), data_sha256: pilotHash(data), provider_egress: providerEgress,
    persistence: "d1-append-only-application-contract" as const, attestation: "not-attested" as const,
    rollback_protection: "requires-independent-checkpoint" as const };
  const receipt_id = `sites-pilot:sha256:${pilotHash({ tool, ...core })}`;
  const result: PilotResult = { schema: "gis-ai-go.sites-pilot-result.v1", tool, data, evidence: { ...core, receipt_id } };
  if (Buffer.byteLength(canonicalJson(result)) > SITES_PILOT_MAX_RESULT_BYTES) throw new RangeError("Pilot result exceeds bound");
  return result;
}
export function verifyPilotResult(value: unknown): value is PilotResult {
  try {
    const result = value as PilotResult;
    const exact = (object: unknown, keys: string[]): boolean => object !== null && typeof object === "object"
      && !Array.isArray(object) && Object.keys(object).sort().join("|") === keys.sort().join("|");
    if (!exact(result, ["schema", "tool", "data", "evidence"]) || !exact(result.evidence,
      ["schema", "created_at", "software_revision", "parameters_sha256", "data_sha256", "provider_egress",
        "persistence", "attestation", "rollback_protection", "receipt_id"])) return false;
    if (result.schema !== "gis-ai-go.sites-pilot-result.v1" || !/^sites_[a-z_]+$/.test(result.tool)
      || result.data === null || typeof result.data !== "object" || Array.isArray(result.data)) return false;
    const { receipt_id, ...core } = result.evidence;
    return core.schema === SITES_PILOT_SCHEMA && /^[0-9a-f]{40}$/.test(core.software_revision)
      && /^[0-9a-f]{64}$/.test(core.parameters_sha256) && typeof core.provider_egress === "boolean"
      && new Date(core.created_at).toISOString() === core.created_at && core.persistence === "d1-append-only-application-contract"
      && core.attestation === "not-attested" && core.rollback_protection === "requires-independent-checkpoint"
      && core.data_sha256 === pilotHash(result.data)
      && receipt_id === `sites-pilot:sha256:${pilotHash({ tool: result.tool, ...core })}`
      && Buffer.byteLength(canonicalJson(result)) <= SITES_PILOT_MAX_RESULT_BYTES;
  } catch { return false; }
}
export function createSitesPilotStore(database: Web216D1Database): PilotStore {
  return {
    async admit(provider, now) {
      if (!SITES_PILOT_PROVIDERS.includes(provider) || !Number.isSafeInteger(now) || now < 0) throw new TypeError("Invalid admission");
      try {
        const row = await database.prepare(SITES_PILOT_SQL.admit).bind(now - 60_000, now - 60_000, now,
          provider, now - 60_000).first<{ used: number }>();
        if (row === null) throw new SitesPilotStoreError("allowance-denied");
      } catch (error) {
        if (error instanceof SitesPilotStoreError) throw error;
        throw new SitesPilotStoreError("store-unavailable");
      }
    },
    async append(result) {
      if (!verifyPilotResult(result)) throw new SitesPilotStoreError("corrupt-evidence");
      try {
        const row = await database.prepare(SITES_PILOT_SQL.insert).bind(result.evidence.receipt_id,
          result.evidence.created_at, canonicalJson(result)).first<{ receipt_id: string }>();
        if (row === null) throw new SitesPilotStoreError("store-full");
        const readBack = await this.inspect(result.evidence.receipt_id);
        if (canonicalJson(readBack) !== canonicalJson(result)) throw new SitesPilotStoreError("corrupt-evidence");
      } catch (error) {
        if (error instanceof SitesPilotStoreError) throw error;
        throw new SitesPilotStoreError("store-unavailable");
      }
    },
    async inspect(receiptId) {
      if (!/^sites-pilot:sha256:[0-9a-f]{64}$/.test(receiptId)) throw new TypeError("Invalid receipt identifier");
      try {
        const row = await database.prepare(SITES_PILOT_SQL.read).bind(receiptId).first<{ result_json: string }>();
        if (row === null) throw new SitesPilotStoreError("not-found");
        if (Buffer.byteLength(row.result_json) > SITES_PILOT_MAX_RESULT_BYTES) throw new SitesPilotStoreError("corrupt-evidence");
        const value: unknown = JSON.parse(row.result_json);
        if (!verifyPilotResult(value) || value.evidence.receipt_id !== receiptId) throw new SitesPilotStoreError("corrupt-evidence");
        return value;
      } catch (error) {
        if (error instanceof SitesPilotStoreError) throw error;
        throw new SitesPilotStoreError("store-unavailable");
      }
    },
  };
}
