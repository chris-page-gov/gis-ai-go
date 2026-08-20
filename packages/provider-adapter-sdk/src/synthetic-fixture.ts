import {
  CANONICAL_DOMAINS,
  canonicalDigest,
  canonicalJsonBytes,
  canonicalJsonClone,
  type CanonicalDigest,
} from "@gis-ai-go/evidence";

import { ProviderAdapterFault, normaliseAdapterError } from "./contract.js";
import {
  ADAPTER_OPERATIONS,
  type AdapterDescription,
  type AdapterHealth,
  type AdapterLifecycle,
  type NormalisedAdapterError,
  type ProviderAdapter,
  type ProviderAdapterEstimate,
  type ProviderAdapterProvenance,
  type ProviderAdapterQuery,
  type ProviderAdapterResult,
  type ProviderRights,
} from "./types.js";

const ADAPTER_ID = "gis-ai-go.synthetic-statistics";
const ADAPTER_VERSION = "1";
const PROVIDER_ID = "fixture.statistics";
const DATASET_ID = "population-count";
const EDITION = "2026";
const VERSION = "1";
const VERSION_URI =
  "urn:gis-ai-go:fixture:provider:fixture.statistics:datasets:population-count:editions:2026:versions:1";
const DIMENSION_ORDER = Object.freeze(["time", "geography", "measure"] as const);

const DEFAULT_LIFECYCLE: AdapterLifecycle = Object.freeze({
  discovery: "suspended",
  invocation: "suspended",
  reason: "Fixture activation must be explicit in tests.",
});

const RIGHTS: ProviderRights = canonicalJsonClone({
  state: "project-synthetic",
  licence: "MIT",
  licenceUri: "https://opensource.org/license/mit",
  attribution: "GIS AI GO synthetic fixture; not official statistics.",
  obligations: [
    "Keep the result labelled as synthetic.",
    "Do not attribute fixture values to an external provider.",
  ],
  exceptions: [],
  evidenceUris: ["https://github.com/chris-page-gov/gis-ai-go/blob/main/LICENSE"],
  reviewedAt: "2026-08-20T00:00:00Z",
});

const PROVIDER_VERSION = canonicalJsonClone({
  providerId: PROVIDER_ID,
  datasetId: DATASET_ID,
  edition: EDITION,
  version: VERSION,
  versionUri: VERSION_URI,
  sourceDate: "2026-08-20",
  dimensionOrder: DIMENSION_ORDER,
});

const PROVENANCE: ProviderAdapterProvenance = canonicalJsonClone({
  providerVersion: PROVIDER_VERSION,
  adapter: { id: ADAPTER_ID, version: ADAPTER_VERSION },
  transformations: ["exact-fixture-key-lookup.v1", "rfc8785-canonical-json.v1"],
  synthetic: true,
});

const ROWS: Readonly<Record<string, string>> = Object.freeze({
  "2026|FIXTURE-EW|population": "1000",
  "2026|FIXTURE-SC|population": "500",
});

function recordAt(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  return value as Record<string, unknown>;
}

function exactKeys(record: Record<string, unknown>, expected: readonly string[]): void {
  const actual = Object.keys(record).sort();
  const wanted = [...expected].sort();
  if (actual.length !== wanted.length || actual.some((key, index) => key !== wanted[index])) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
}

function boundedString(value: unknown, maximum = 128): string {
  if (typeof value !== "string" || value.length < 1 || value.length > maximum) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  return value;
}

function parseLifecycle(input: unknown): AdapterLifecycle {
  let detached: unknown;
  try {
    detached = canonicalJsonClone(input);
  } catch {
    throw new TypeError("Adapter lifecycle must be canonical JSON");
  }
  const lifecycle = recordAt(detached);
  exactKeys(lifecycle, ["discovery", "invocation", "reason"]);
  if (
    !["active", "suspended"].includes(String(lifecycle.discovery)) ||
    !["active", "suspended"].includes(String(lifecycle.invocation))
  ) {
    throw new TypeError("Adapter lifecycle planes must be active or suspended");
  }
  const reason = boundedString(lifecycle.reason, 512);
  return canonicalJsonClone({
    discovery: lifecycle.discovery as AdapterLifecycle["discovery"],
    invocation: lifecycle.invocation as AdapterLifecycle["invocation"],
    reason,
  });
}

function parseQuery(input: unknown): ProviderAdapterQuery {
  let detached: unknown;
  try {
    detached = canonicalJsonClone(input);
  } catch {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  const request = recordAt(detached);
  exactKeys(request, ["dataset", "selections"]);

  const dataset = recordAt(request.dataset);
  exactKeys(dataset, ["edition", "id", "version"]);
  const datasetId = boundedString(dataset.id);
  const edition = boundedString(dataset.edition);
  const version = boundedString(dataset.version);
  if (datasetId !== DATASET_ID || edition !== EDITION) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  if (version !== VERSION) {
    throw new ProviderAdapterFault("STALE_PROVIDER_VERSION");
  }

  if (!Array.isArray(request.selections) || request.selections.length !== DIMENSION_ORDER.length) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  const selections = request.selections.map((candidate, index) => {
    const selection = recordAt(candidate);
    exactKeys(selection, ["dimension", "option"]);
    const dimension = boundedString(selection.dimension);
    const option = boundedString(selection.option);
    if (dimension !== DIMENSION_ORDER[index]) {
      throw new ProviderAdapterFault("INVALID_REQUEST");
    }
    return { dimension, option };
  });

  return canonicalJsonClone({
    dataset: { id: datasetId, edition, version },
    selections,
  });
}

function resultFor(query: ProviderAdapterQuery): ProviderAdapterResult {
  const key = query.selections.map(({ option }) => option).join("|");
  const value = ROWS[key];
  if (value === undefined) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  return canonicalJsonClone({
    schema: "gis-ai-go.provider-adapter-result.v1",
    provider: { id: PROVIDER_ID, adapterId: ADAPTER_ID },
    dataset: {
      id: DATASET_ID,
      edition: EDITION,
      version: VERSION,
      versionUri: VERSION_URI,
    },
    dimensions: query.selections,
    observations: [{ value, unit: "synthetic persons" }],
    rights: RIGHTS,
    provenance: PROVENANCE,
  });
}

export class SyntheticFixtureAdapter implements ProviderAdapter {
  public readonly operations = ADAPTER_OPERATIONS;
  readonly #lifecycle: AdapterLifecycle;

  public constructor(lifecycle: AdapterLifecycle = DEFAULT_LIFECYCLE) {
    this.#lifecycle = parseLifecycle(lifecycle);
  }

  public describe(): AdapterDescription {
    if (this.#lifecycle.discovery !== "active") {
      throw new ProviderAdapterFault("ADAPTER_DISCOVERY_SUSPENDED");
    }
    return canonicalJsonClone({
      adapterId: ADAPTER_ID,
      adapterVersion: ADAPTER_VERSION,
      name: "GIS AI GO deterministic statistics fixture",
      operations: ADAPTER_OPERATIONS,
      lifecycle: this.#lifecycle,
      providerVersion: PROVIDER_VERSION,
      egress: {
        mode: "none",
        reason: "The frozen synthetic adapter performs no network request.",
      },
    });
  }

  public health(): AdapterHealth {
    return canonicalJsonClone({
      adapterId: ADAPTER_ID,
      discovery: this.#lifecycle.discovery,
      invocation: this.#lifecycle.invocation,
      network: "not-used",
    });
  }

  public estimate(request: unknown): ProviderAdapterEstimate {
    this.#assertInvocation();
    const result = resultFor(parseQuery(request));
    return canonicalJsonClone({
      observations: result.observations.length,
      canonicalResponseBytes: canonicalJsonBytes(result).byteLength,
      confidence: "exact",
    });
  }

  public execute(request: unknown): ProviderAdapterResult {
    this.#assertInvocation();
    return resultFor(parseQuery(request));
  }

  public normalise_error(error: unknown): NormalisedAdapterError {
    return normaliseAdapterError(error);
  }

  public licence_evidence(): ProviderRights {
    return canonicalJsonClone(RIGHTS);
  }

  public provenance(): ProviderAdapterProvenance {
    return canonicalJsonClone(PROVENANCE);
  }

  #assertInvocation(): void {
    if (this.#lifecycle.invocation !== "active") {
      throw new ProviderAdapterFault("ADAPTER_INVOCATION_SUSPENDED");
    }
  }
}

export function serialiseProviderAdapterResult(result: ProviderAdapterResult): Uint8Array {
  return canonicalJsonBytes(result);
}

export function digestProviderAdapterResult(
  result: ProviderAdapterResult,
): CanonicalDigest<typeof CANONICAL_DOMAINS.providerAdapterResult> {
  return canonicalDigest(CANONICAL_DOMAINS.providerAdapterResult, result);
}

export function createSyntheticFixtureAdapter(
  lifecycle: AdapterLifecycle = DEFAULT_LIFECYCLE,
): SyntheticFixtureAdapter {
  return new SyntheticFixtureAdapter(lifecycle);
}
