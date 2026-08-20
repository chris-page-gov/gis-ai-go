import type {
  AdapterErrorCode,
  FixedEgressPolicy,
  NormalisedAdapterError,
} from "./types.js";

const QUERY_VALUE = /^[A-Za-z0-9](?:[A-Za-z0-9._~-]{0,126}[A-Za-z0-9])?$/u;
const QUERY_NAME = /^[A-Za-z][A-Za-z0-9._~-]{0,127}$/u;

const SAFE_MESSAGES: Readonly<Record<AdapterErrorCode, string>> = Object.freeze({
  ADAPTER_DISCOVERY_SUSPENDED: "The provider adapter is suspended for discovery.",
  ADAPTER_INVOCATION_SUSPENDED: "The provider adapter is suspended for invocation.",
  INCOMPATIBLE_OPERATION: "The provider adapter does not support this operation.",
  INVALID_REQUEST: "The provider adapter rejected the request.",
  MALFORMED_PROVIDER_RESPONSE: "The provider returned a response that failed validation.",
  PROVIDER_OUTAGE: "The provider is unavailable.",
  PROVIDER_RATE_LIMITED: "The provider rate limit was reached.",
  PROVIDER_TIMEOUT: "The provider request exceeded its deadline.",
  RIGHTS_UNKNOWN: "The provider record has no accepted rights evidence.",
  STALE_PROVIDER_VERSION: "The requested provider version is not the reviewed version.",
});

export class ProviderAdapterFault extends Error {
  public readonly code: AdapterErrorCode;
  public readonly retryable: boolean;
  public readonly providerStatus: number | null;

  public constructor(
    code: AdapterErrorCode,
    options: { readonly retryable?: boolean; readonly providerStatus?: number | null } = {},
  ) {
    super(SAFE_MESSAGES[code]);
    this.name = "ProviderAdapterFault";
    this.code = code;
    this.retryable = options.retryable ?? false;
    this.providerStatus = options.providerStatus ?? null;
  }
}

export function normaliseAdapterError(error: unknown): NormalisedAdapterError {
  try {
    if (error instanceof ProviderAdapterFault) {
      const code = error.code;
      if (Object.hasOwn(SAFE_MESSAGES, code)) {
        return Object.freeze({
          code,
          message: SAFE_MESSAGES[code],
          providerStatus: error.providerStatus,
          retryable: error.retryable,
        });
      }
    }
  } catch {
    // A hostile thrown proxy is treated as an opaque provider failure below.
  }

  let abort = false;
  try {
    abort = error instanceof Error && error.name === "AbortError";
  } catch {
    abort = false;
  }
  const code: AdapterErrorCode = abort ? "PROVIDER_TIMEOUT" : "PROVIDER_OUTAGE";
  return Object.freeze({
    code,
    message: SAFE_MESSAGES[code],
    providerStatus: null,
    retryable: true,
  });
}

function validateFixedPolicy(policy: FixedEgressPolicy): URL {
  let origin: URL;
  try {
    origin = new URL(policy.origin);
  } catch {
    throw new TypeError("Fixed egress origin must be an absolute URL");
  }
  if (
    origin.protocol !== "https:" ||
    origin.username !== "" ||
    origin.password !== "" ||
    origin.port !== "" ||
    origin.pathname !== "/" ||
    origin.search !== "" ||
    origin.hash !== ""
  ) {
    throw new TypeError("Fixed egress origin must be a credential-free HTTPS origin");
  }
  if (
    policy.allowCallerUrl !== false ||
    policy.allowCredentials !== false ||
    policy.maxRedirects !== 0 ||
    policy.method !== "GET"
  ) {
    throw new TypeError("Fixed egress policy must reject caller URLs, credentials and redirects");
  }
  const boundedInteger = (value: number, minimum: number, maximum: number): boolean =>
    Number.isSafeInteger(value) && value >= minimum && value <= maximum;
  if (
    !boundedInteger(policy.connectTimeoutMs, 100, 10_000) ||
    !boundedInteger(policy.responseTimeoutMs, 100, 30_000) ||
    !boundedInteger(policy.maxCompressedBytes, 1_024, 1_048_576) ||
    !boundedInteger(policy.maxDecompressedBytes, policy.maxCompressedBytes, 4_194_304) ||
    !boundedInteger(policy.maxAttempts, 1, 3) ||
    !boundedInteger(policy.maxRetryAfterSeconds, 0, 60) ||
    policy.routes.length < 1 ||
    policy.routes.length > 10
  ) {
    throw new TypeError("Fixed egress limits must use the reviewed closed bounds");
  }
  const paths = new Set<string>();
  for (const route of policy.routes) {
    let routeUrl: URL;
    try {
      routeUrl = new URL(route.path, origin);
    } catch {
      throw new TypeError("Fixed egress route must be a valid absolute path");
    }
    const queryNames = route.queryParameters.map(({ name }) => name);
    const expectedRawQuery = route.queryParameters
      .map(({ name, value }) => `${name}=${value}`)
      .join("&");
    if (
      routeUrl.origin !== origin.origin ||
      routeUrl.pathname !== route.path ||
      routeUrl.search !== "" ||
      routeUrl.hash !== "" ||
      paths.has(route.path) ||
      route.queryParameters.length > 20 ||
      route.canonicalRawQuery.length > 4_096 ||
      new Set(queryNames).size !== queryNames.length ||
      route.queryParameters.some(
        ({ name, value }) => !QUERY_NAME.test(name) || !QUERY_VALUE.test(value),
      ) ||
      route.canonicalRawQuery !== expectedRawQuery
    ) {
      throw new TypeError("Fixed egress routes and query values must be exact and unique");
    }
    paths.add(route.path);
  }
  if (
    policy.retryableStatuses.length < 1 ||
    policy.retryableStatuses.length > 8 ||
    new Set(policy.retryableStatuses).size !== policy.retryableStatuses.length ||
    policy.retryableStatuses.some((status) => ![429, 502, 503, 504].includes(status))
  ) {
    throw new TypeError("Fixed egress retry statuses must use the reviewed closed set");
  }
  return origin;
}

/**
 * Validate an internally constructed provider request against an exact allowlist.
 * Application callers must supply typed identifiers, never this URL.
 */
export function assertFixedEgressTarget(
  policy: FixedEgressPolicy,
  candidate: { readonly method: string; readonly url: string; readonly redirectCount: number },
): URL {
  const origin = validateFixedPolicy(policy);
  if (candidate.method !== policy.method || candidate.redirectCount !== 0) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }

  let target: URL;
  try {
    target = new URL(candidate.url);
  } catch {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  if (
    target.origin !== origin.origin ||
    target.protocol !== "https:" ||
    target.username !== "" ||
    target.password !== "" ||
    target.port !== "" ||
    target.hash !== ""
  ) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }

  const route = policy.routes.find(({ path }) => path === target.pathname);
  if (route === undefined) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }

  const queryMarker = candidate.url.indexOf("?");
  const observedRawQuery = queryMarker === -1 ? null : candidate.url.slice(queryMarker + 1);
  const expectedRawQuery = route.canonicalRawQuery === "" ? null : route.canonicalRawQuery;
  if (observedRawQuery !== expectedRawQuery) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }

  const observedParameters = [...target.searchParams];
  if (
    observedParameters.length !== route.queryParameters.length ||
    observedParameters.some(
      ([name, value], index) =>
        name !== route.queryParameters[index]?.name ||
        value !== route.queryParameters[index]?.value,
    )
  ) {
    throw new ProviderAdapterFault("INVALID_REQUEST");
  }
  return new URL(target.href);
}
