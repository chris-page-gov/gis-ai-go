/** Firestore strong-read + conditional atomic snapshot store. No local-file durability. */
import {
  canonicalJson, createWeb216D1SnapshotStore, WEB216_D1_SQL,
  type Web216D1Database, type Web216D1Statement, type Web216TransactionalSnapshot,
  type Web216TransactionalMaterial,
} from "@gis-ai-go/evidence/web216-pure";

export interface GcpAtomicDocument {
  readonly version: string;
  readonly fields: Readonly<Record<string, string>>;
}
export interface GcpAtomicDocumentStore {
  /** Firestore reads are strongly consistent; null is definite absence. */
  read(id: string): Promise<GcpAtomicDocument | null>;
  /** All fields commit together, only if the exact updateTime (or absence) still holds. */
  compareAndSet(id: string, expectedVersion: string | null, fields: Readonly<Record<string, string>>): Promise<boolean>;
}
export interface GcpFirestoreConfig {
  readonly projectId: string;
  readonly databaseId: string;
  readonly collection: string;
}
const MAX_DOCUMENT_BYTES = 900_000; // Firestore's 1 MiB ceiling includes field/name overhead.
function safeConfig(config: GcpFirestoreConfig): void {
  if (!/^[a-z][a-z0-9-]{4,61}[a-z0-9]$/u.test(config.projectId) ||
      !/^(?:\(default\)|[a-z][a-z0-9-]{3,62})$/u.test(config.databaseId) ||
      !/^[a-zA-Z][a-zA-Z0-9_-]{0,63}$/u.test(config.collection)) throw Error("Invalid Firestore configuration");
}
async function boundedJson(response: Response): Promise<Record<string, unknown>> {
  const body = response.body?.getReader(); if (!body) throw Error("Missing Firestore response");
  let size = 0; const chunks: Uint8Array[] = [];
  for (;;) { const part = await body.read(); if (part.done) break; size += part.value.byteLength;
    if (size > 1_100_000) { void body.cancel(); throw Error("Firestore response exceeds limit"); } chunks.push(part.value); }
  const value: unknown = JSON.parse(Buffer.concat(chunks).toString("utf8"));
  if (!value || typeof value !== "object" || Array.isArray(value)) throw Error("Malformed Firestore response");
  return value as Record<string, unknown>;
}
/** Runtime authentication uses short-lived metadata credentials. No service-account key or supplied bearer env. */
export function createGcpMetadataAccessToken(options: { readonly fetch?: typeof fetch; readonly now?: () => number } = {}) {
  const fetcher = options.fetch ?? fetch; const now = options.now ?? Date.now;
  let token: string | undefined; let until = 0;
  return async () => {
    if (token && now() < until) return token;
    const response = await fetcher("http://metadata.google.internal/computeMetadata/v1/instance/service-accounts/default/token", {
      headers: { "Metadata-Flavor": "Google" }, redirect: "error", signal: AbortSignal.timeout(3_000),
    });
    if (!response.ok || response.headers.get("metadata-flavor") !== "Google") throw Error("Runtime credentials unavailable");
    const value = await boundedJson(response);
    if (typeof value.access_token !== "string" || value.access_token.length > 8_192 || value.token_type !== "Bearer" ||
        !Number.isSafeInteger(value.expires_in) || (value.expires_in as number) < 60) throw Error("Invalid runtime credentials");
    token = value.access_token; until = now() + ((value.expires_in as number) - 30) * 1_000; return token;
  };
}
/** Strong reads and Firestore commit updateTime preconditions implement a one-document transaction. */
export function createGcpFirestoreRestStore(config: GcpFirestoreConfig, options: {
  readonly fetch?: typeof fetch; readonly accessToken?: () => Promise<string>;
} = {}): GcpAtomicDocumentStore {
  safeConfig(config);
  const fetcher = options.fetch ?? fetch; const credential = options.accessToken ?? createGcpMetadataAccessToken({ fetch: fetcher });
  const database = `projects/${config.projectId}/databases/${config.databaseId}`;
  const root = `${database}/documents/${config.collection}`;
  function document(id: string) { if (!/^[0-9a-f]{64}$/u.test(id)) throw Error("Invalid evidence scope"); return `${root}/${id}`; }
  async function request(url: string, init: RequestInit = {}) {
    const response = await fetcher(url, { ...init, redirect: "error", signal: AbortSignal.timeout(8_000),
      headers: { "content-type": "application/json", authorization: `Bearer ${await credential()}` } });
    return response;
  }
  return Object.freeze({
    read: async (id: string): Promise<GcpAtomicDocument | null> => {
      const name = document(id); const response = await request(`https://firestore.googleapis.com/v1/${name}`);
      if (response.status === 404) return null;
      if (!response.ok) throw Error("Firestore read unavailable");
      const value = await boundedJson(response);
      if (value.name !== name || typeof value.updateTime !== "string" || !value.fields ||
          typeof value.fields !== "object" || Array.isArray(value.fields)) throw Error("Corrupt Firestore document");
      const fields: Record<string, string> = {};
      for (const [key, field] of Object.entries(value.fields as Record<string, unknown>)) {
        if (!field || typeof field !== "object" || Array.isArray(field) ||
            Object.keys(field).join(",") !== "stringValue" || typeof (field as { stringValue: unknown }).stringValue !== "string") throw Error("Corrupt Firestore field");
        fields[key] = (field as { stringValue: string }).stringValue;
      }
      return Object.freeze({ version: value.updateTime, fields: Object.freeze(fields) });
    },
    compareAndSet: async (id: string, expectedVersion: string | null, fields: Readonly<Record<string, string>>) => {
      if (Buffer.byteLength(canonicalJson(fields)) > MAX_DOCUMENT_BYTES) throw Error("Firestore snapshot capacity exceeded");
      const name = document(id);
      const body = { writes: [{ update: { name, fields: Object.fromEntries(Object.entries(fields).map(([key, value]) => [key, { stringValue: value }])) },
        currentDocument: expectedVersion === null ? { exists: false } : { updateTime: expectedVersion } }] };
      const response = await request(`https://firestore.googleapis.com/v1/${database}/documents:commit`, { method: "POST", body: JSON.stringify(body) });
      if (!response.ok) {
        if ([400, 409, 412].includes(response.status)) {
          const failure = await boundedJson(response);
          const status = (failure.error as { status?: unknown } | undefined)?.status;
          if (status === "FAILED_PRECONDITION" || status === "ALREADY_EXISTS" || status === "ABORTED") return false;
        }
        throw Error("Firestore commit outcome uncertain");
      }
      const value = await boundedJson(response);
      if (!Array.isArray(value.writeResults) || value.writeResults.length !== 1 || typeof value.commitTime !== "string") throw Error("Firestore commit acknowledgement invalid");
      return true;
    },
  });
}

/** A closed compatibility adapter reuses the maintained CPIH application and exact receipt/chain contracts.
 * It accepts only its three published statements; it executes no SQL and has no D1/Workers dependency.
 * Snapshot CAS atomically publishes the key claim, immutable receipt, event and head. */
export function createGcpFirestoreCpihStore(options: {
  readonly backend: GcpAtomicDocumentStore; readonly principalScope: string;
  readonly initialSnapshot: Web216TransactionalSnapshot;
  readonly material: Omit<Web216TransactionalMaterial, "expectedCheckpointId">;
}) {
  if (!/^[0-9a-f]{64}$/u.test(options.principalScope)) throw Error("Invalid scoped evidence store");
  const fieldsFor = (snapshotJson: string, storeId: string, checkpointId: string, sequence: number) => ({
    schema: "gis-ai-go.gcp-firestore-cpih.v1", principal_scope: options.principalScope,
    snapshot_json: snapshotJson, store_id: storeId, checkpoint_id: checkpointId, sequence: String(sequence),
  });
  async function read() {
    const doc = await options.backend.read(options.principalScope);
    if (doc === null) return null;
    if (Object.keys(doc.fields).sort().join(",") !== "checkpoint_id,principal_scope,schema,sequence,snapshot_json,store_id" ||
        doc.fields.schema !== "gis-ai-go.gcp-firestore-cpih.v1" || doc.fields.principal_scope !== options.principalScope ||
        !/^(?:0|[1-9]\d{0,2})$/u.test(doc.fields.sequence ?? "") || Buffer.byteLength(doc.fields.snapshot_json ?? "") > MAX_DOCUMENT_BYTES) throw Error("Scoped evidence corruption");
    return doc;
  }
  const database: Web216D1Database = { prepare: (sql: string): Web216D1Statement => {
    if (!(Object.values(WEB216_D1_SQL) as string[]).includes(sql)) throw Error("Unexpected evidence statement");
    const statement = (values: readonly unknown[]): Web216D1Statement => ({
      bind: (...bound) => statement(bound),
      first: async <T>() => {
        if (sql !== WEB216_D1_SQL.read || values.length !== 0) throw Error("Unexpected evidence read");
        const doc = await read(); if (doc === null) return null;
        return { singleton: 1, store_id: doc.fields.store_id, checkpoint_id: doc.fields.checkpoint_id,
          sequence: Number(doc.fields.sequence), snapshot_json: doc.fields.snapshot_json,
          snapshot_bytes: Buffer.byteLength(doc.fields.snapshot_json!), row_count: 1 } as T;
      },
      run: async () => {
        if (sql === WEB216_D1_SQL.insert && values.length === 3) {
          const [storeId, checkpointId, encoded] = values as [string, string, string];
          const committed = await options.backend.compareAndSet(options.principalScope, null, fieldsFor(encoded, storeId, checkpointId, 0));
          return { success: true, meta: { changes: committed ? 1 : 0 } };
        }
        if (sql !== WEB216_D1_SQL.update || values.length !== 6) throw Error("Unexpected evidence write");
        const [encoded, checkpoint, sequence, expectedStore, expectedHead, expectedSequence] = values as [string, string, number, string, string, number];
        const previous = await read();
        if (previous === null || previous.fields.store_id !== expectedStore || previous.fields.checkpoint_id !== expectedHead ||
            Number(previous.fields.sequence) !== expectedSequence) return { success: true, meta: { changes: 0 } };
        const committed = await options.backend.compareAndSet(options.principalScope, previous.version,
          fieldsFor(encoded, expectedStore, checkpoint, sequence));
        return { success: true, meta: { changes: committed ? 1 : 0 } };
      },
    });
    return statement([]);
  } };
  return createWeb216D1SnapshotStore({ database, initialSnapshot: options.initialSnapshot, material: options.material });
}
