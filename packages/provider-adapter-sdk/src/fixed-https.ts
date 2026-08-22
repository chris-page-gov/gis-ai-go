import { Resolver } from "node:dns/promises";
import { request as httpsRequest } from "node:https";
import { BlockList, isIP, type LookupFunction } from "node:net";
import { performance } from "node:perf_hooks";
import type { TLSSocket } from "node:tls";
import { types as utilTypes } from "node:util";

import { assertFixedEgressTarget } from "./contract.js";
import type { FixedEgressPolicy } from "./types.js";

const MAX_HEADER_BYTES = 16_384;
const MAX_HEADER_COUNT = 64;
const NODE_HTTP_PARSER_ERROR_CODE = /^HPE_[A-Z0-9_]+$/u;
const NODE_NETWORK_ERROR_CODES = new Set([
  "EADDRNOTAVAIL",
  "EAI_AGAIN",
  "ECONNABORTED",
  "ECONNREFUSED",
  "ECONNRESET",
  "EHOSTDOWN",
  "EHOSTUNREACH",
  "ENETDOWN",
  "ENETUNREACH",
  "ENOTFOUND",
  "EPIPE",
  "ETIMEDOUT",
  "CERT_HAS_EXPIRED",
  "CERT_NOT_YET_VALID",
  "DEPTH_ZERO_SELF_SIGNED_CERT",
  "ERR_TLS_CERT_ALTNAME_INVALID",
  "SELF_SIGNED_CERT_IN_CHAIN",
  "UNABLE_TO_GET_ISSUER_CERT",
  "UNABLE_TO_GET_ISSUER_CERT_LOCALLY",
  "UNABLE_TO_VERIFY_LEAF_SIGNATURE",
]);
const FIXED_HTTPS_FAILURE_KINDS = new Set<FixedHttpsFailureKind>([
  "aborted",
  "connect-timeout",
  "invalid-response-framing",
  "invalid-response-headers",
  "network",
  "response-timeout",
  "response-too-large",
  "unclassified",
  "unsafe-address",
]);
const FIXED_HTTPS_TRANSPORT_ERRORS = new WeakSet<object>();

const BLOCKED_ADDRESSES = new BlockList();
for (const [address, prefix] of [
  ["0.0.0.0", 8],
  ["10.0.0.0", 8],
  ["100.64.0.0", 10],
  ["127.0.0.0", 8],
  ["169.254.0.0", 16],
  ["172.16.0.0", 12],
  ["192.0.0.0", 24],
  ["192.0.2.0", 24],
  ["192.31.196.0", 24],
  ["192.52.193.0", 24],
  ["192.88.99.0", 24],
  ["192.168.0.0", 16],
  ["192.175.48.0", 24],
  ["198.18.0.0", 15],
  ["198.51.100.0", 24],
  ["203.0.113.0", 24],
  ["224.0.0.0", 4],
  ["240.0.0.0", 4],
] as const) {
  BLOCKED_ADDRESSES.addSubnet(address, prefix, "ipv4");
}
for (const [address, prefix] of [
  ["::", 128],
  ["::1", 128],
  ["64:ff9b::", 96],
  ["64:ff9b:1::", 48],
  ["100::", 64],
  ["2001::", 32],
  ["2001:2::", 48],
  ["2001:3::", 32],
  ["2001:4:112::", 48],
  ["2001:10::", 28],
  ["2001:20::", 28],
  ["2001:30::", 28],
  ["2001:db8::", 32],
  ["2002::", 16],
  ["2620:4f:8000::", 48],
  ["3fff::", 20],
  ["5f00::", 16],
  ["fc00::", 7],
  ["fe80::", 10],
  ["ff00::", 8],
] as const) {
  BLOCKED_ADDRESSES.addSubnet(address, prefix, "ipv6");
}

export type FixedHttpsFailureKind =
  | "aborted"
  | "connect-timeout"
  | "invalid-response-framing"
  | "invalid-response-headers"
  | "network"
  | "response-timeout"
  | "response-too-large"
  | "unclassified"
  | "unsafe-address";

export class FixedHttpsTransportError extends Error {
  public readonly kind: FixedHttpsFailureKind;

  public constructor(kind: FixedHttpsFailureKind) {
    super("The fixed provider HTTPS request failed");
    this.name = "FixedHttpsTransportError";
    this.kind = kind;
  }
}

function makeFixedHttpsTransportError(
  kind: FixedHttpsFailureKind,
): FixedHttpsTransportError {
  const error = Object.freeze(new FixedHttpsTransportError(kind));
  FIXED_HTTPS_TRANSPORT_ERRORS.add(error);
  return error;
}

/** Read an exact base-class error kind without invoking caller-controlled traps. */
export function fixedHttpsTransportErrorKind(
  value: unknown,
): FixedHttpsFailureKind | null {
  if (typeof value !== "object" || value === null || utilTypes.isProxy(value)) return null;
  try {
    if (Object.getPrototypeOf(value) !== FixedHttpsTransportError.prototype) return null;
    const descriptor = Object.getOwnPropertyDescriptor(value, "kind");
    return descriptor !== undefined &&
      "value" in descriptor &&
      typeof descriptor.value === "string" &&
      FIXED_HTTPS_FAILURE_KINDS.has(descriptor.value as FixedHttpsFailureKind)
      ? descriptor.value as FixedHttpsFailureKind
      : null;
  } catch {
    return null;
  }
}

/** Recognise only transport errors created by this module's private factory. */
export function isExactFixedHttpsTransportError(
  value: unknown,
): value is FixedHttpsTransportError {
  return typeof value === "object" &&
    value !== null &&
    !utilTypes.isProxy(value) &&
    FIXED_HTTPS_TRANSPORT_ERRORS.has(value);
}

/** Keep provider-controlled HTTP parser failures out of the network outage class. */
export function normaliseFixedHttpsRequestError(error: unknown): FixedHttpsTransportError {
  if (typeof error !== "object" || error === null) {
    return makeFixedHttpsTransportError("unclassified");
  }
  if (utilTypes.isProxy(error)) return makeFixedHttpsTransportError("unclassified");
  if (isExactFixedHttpsTransportError(error)) return error;
  let codeDescriptor: PropertyDescriptor | undefined;
  try {
    codeDescriptor = Object.getOwnPropertyDescriptor(error, "code");
  } catch {
    return makeFixedHttpsTransportError("unclassified");
  }
  const code = codeDescriptor !== undefined && "value" in codeDescriptor
    ? codeDescriptor.value
    : undefined;
  if (typeof code !== "string") return makeFixedHttpsTransportError("unclassified");
  if (NODE_HTTP_PARSER_ERROR_CODE.test(code)) {
    return makeFixedHttpsTransportError("invalid-response-framing");
  }
  return NODE_NETWORK_ERROR_CODES.has(code) || /^(?:ERR_TLS_|ERR_SSL_)/u.test(code)
    ? makeFixedHttpsTransportError("network")
    : makeFixedHttpsTransportError("unclassified");
}

function normaliseFixedHttpsResponseError(error: unknown): FixedHttpsTransportError {
  // Once response headers have been accepted, an ordinary socket/parser error
  // means the provider response is incomplete. Preserve only module-owned
  // abort, timeout and size failures; never relabel premature EOF as network.
  return isExactFixedHttpsTransportError(error)
    ? error
    : makeFixedHttpsTransportError("invalid-response-framing");
}

export interface FixedHttpsTelemetry {
  readonly dnsMs: number;
  readonly resolvedAddressCount: number;
  readonly selectedAddressFamily: 4 | 6;
  readonly connectMs: number;
  readonly responseMs: number;
  readonly totalMs: number;
  readonly compressedBytes: number;
  readonly tlsProtocol: string | null;
  readonly tlsCipher: string | null;
}

export interface FixedHttpsResponse {
  readonly status: number;
  readonly headers: Readonly<Record<string, string>>;
  readonly body: Uint8Array;
  readonly telemetry: FixedHttpsTelemetry;
}

export interface FixedHttpsRequest {
  readonly policy: FixedEgressPolicy;
  readonly url: string;
  readonly signal?: AbortSignal;
}

export type FixedHttpsTransport = (request: FixedHttpsRequest) => Promise<FixedHttpsResponse>;

interface ResolvedAddress {
  readonly address: string;
  readonly family: 4 | 6;
}

/** Reject all local, private, documentation, transition, multicast and reserved IP space. */
export function assertPublicProviderAddress(address: string, family: number): void {
  const observedFamily = isIP(address);
  if (observedFamily !== family || (family !== 4 && family !== 6)) {
    throw makeFixedHttpsTransportError("unsafe-address");
  }
  if (family === 6 && !/^[23]/u.test(address)) {
    throw makeFixedHttpsTransportError("unsafe-address");
  }
  if (BLOCKED_ADDRESSES.check(address, family === 4 ? "ipv4" : "ipv6")) {
    throw makeFixedHttpsTransportError("unsafe-address");
  }
}

function roundedMilliseconds(value: number): number {
  return Math.max(0, Math.round(value * 1_000) / 1_000);
}

function abortError(): FixedHttpsTransportError {
  return makeFixedHttpsTransportError("aborted");
}

function isAborted(signal: AbortSignal | undefined): boolean {
  return signal?.aborted === true;
}

async function resolvePublicAddresses(
  hostname: string,
  timeoutMs: number,
  signal: AbortSignal | undefined,
): Promise<readonly ResolvedAddress[]> {
  if (isAborted(signal)) throw abortError();
  const resolver = new Resolver();
  let timer: ReturnType<typeof setTimeout> | undefined;
  let abortListener: (() => void) | undefined;
  const timeout = new Promise<never>((_resolve, reject) => {
    timer = setTimeout(() => {
      reject(makeFixedHttpsTransportError("connect-timeout"));
      resolver.cancel();
    }, timeoutMs);
    if (signal !== undefined) {
      abortListener = () => {
        reject(abortError());
        resolver.cancel();
      };
      signal.addEventListener("abort", abortListener, { once: true });
    }
  });
  if (isAborted(signal)) {
    if (timer !== undefined) clearTimeout(timer);
    if (abortListener !== undefined) signal?.removeEventListener("abort", abortListener);
    resolver.cancel();
    throw abortError();
  }
  try {
    const resolution = Promise.allSettled([
      resolver.resolve4(hostname),
      resolver.resolve6(hostname),
    ]);
    const results = await Promise.race([resolution, timeout]);
    const records = results.flatMap((result, index): ResolvedAddress[] =>
      result.status === "fulfilled"
        ? result.value.map((address) => ({ address, family: index === 0 ? 4 : 6 }))
        : [],
    );
    if (records.length === 0) {
      const failures = results
        .filter((result): result is PromiseRejectedResult => result.status === "rejected")
        .map((result) => normaliseFixedHttpsRequestError(result.reason));
      throw failures.length > 0 && failures.every((failure) => failure.kind === "network")
        ? makeFixedHttpsTransportError("network")
        : makeFixedHttpsTransportError("unclassified");
    }
    const addresses = records.map(({ address, family }) => {
      assertPublicProviderAddress(address, family);
      return { address, family };
    });
    return Object.freeze(
      addresses.sort((left, right) => {
        if (left.family !== right.family) return left.family - right.family;
        return left.address < right.address ? -1 : left.address > right.address ? 1 : 0;
      }),
    );
  } catch (error) {
    if (isExactFixedHttpsTransportError(error)) throw error;
    throw makeFixedHttpsTransportError("unclassified");
  } finally {
    if (timer !== undefined) clearTimeout(timer);
    if (abortListener !== undefined) signal?.removeEventListener("abort", abortListener);
  }
}

function normaliseHeaders(rawHeaders: readonly string[]): Readonly<Record<string, string>> {
  if (rawHeaders.length % 2 !== 0 || rawHeaders.length / 2 > MAX_HEADER_COUNT) {
    throw makeFixedHttpsTransportError("invalid-response-headers");
  }
  const result: Record<string, string> = Object.create(null) as Record<string, string>;
  for (let index = 0; index < rawHeaders.length; index += 2) {
    const name = rawHeaders[index]?.toLowerCase();
    const value = rawHeaders[index + 1];
    if (name === undefined || value === undefined) {
      throw makeFixedHttpsTransportError("invalid-response-headers");
    }
    result[name] = result[name] === undefined ? value : `${result[name]},${value}`;
  }
  return Object.freeze(result);
}

/**
 * Perform one credential-free, redirect-free HTTPS request pinned to one DNS
 * answer that was validated immediately before connection. No proxy environment
 * variables or provider-returned links are consulted.
 */
export async function fixedHttpsGet(input: FixedHttpsRequest): Promise<FixedHttpsResponse> {
  const target = assertFixedEgressTarget(input.policy, {
    method: "GET",
    url: input.url,
    redirectCount: 0,
  });
  const started = performance.now();
  const dnsStarted = performance.now();
  const addresses = await resolvePublicAddresses(
    target.hostname,
    input.policy.connectTimeoutMs,
    input.signal,
  );
  const dnsCompleted = performance.now();
  const selected = addresses[0]!;
  const remainingConnectMs = input.policy.connectTimeoutMs - (dnsCompleted - started);
  if (remainingConnectMs <= 0) throw makeFixedHttpsTransportError("connect-timeout");

  return await new Promise<FixedHttpsResponse>((resolve, reject) => {
    let settled = false;
    let responseStarted = false;
    let connectedAt: number | undefined;
    let connectTimer: ReturnType<typeof setTimeout> | undefined;
    let responseTimer: ReturnType<typeof setTimeout> | undefined;
    let tlsProtocol: string | null = null;
    let tlsCipher: string | null = null;

    const finish = (error: FixedHttpsTransportError | null, result?: FixedHttpsResponse): void => {
      if (settled) return;
      settled = true;
      if (connectTimer !== undefined) clearTimeout(connectTimer);
      if (responseTimer !== undefined) clearTimeout(responseTimer);
      input.signal?.removeEventListener("abort", onAbort);
      if (error !== null) reject(error);
      else resolve(result!);
    };

    const lookup: LookupFunction = (_hostname, _options, callback) => {
      callback(null, selected.address, selected.family);
    };
    const request = httpsRequest(
      {
        protocol: "https:",
        hostname: target.hostname,
        port: "443",
        path: `${target.pathname}${target.search}`,
        method: "GET",
        agent: false,
        family: selected.family,
        lookup,
        servername: target.hostname,
        rejectUnauthorized: true,
        minVersion: "TLSv1.2",
        maxVersion: "TLSv1.3",
        maxHeaderSize: MAX_HEADER_BYTES,
        headers: {
          Accept: "application/json",
          "Accept-Encoding": "gzip",
          Connection: "close",
          "User-Agent": "gis-ai-go-ons-data-api-adapter/1",
        },
      },
      (response) => {
        responseStarted = true;
        const chunks: Buffer[] = [];
        let compressedBytes = 0;
        response.on("data", (chunk: Buffer | Uint8Array | string) => {
          const bytes = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
          compressedBytes += bytes.byteLength;
          if (compressedBytes > input.policy.maxCompressedBytes) {
            response.destroy(makeFixedHttpsTransportError("response-too-large"));
            return;
          }
          chunks.push(bytes);
        });
        response.once("error", (error: Error) => {
          finish(normaliseFixedHttpsResponseError(error));
        });
        response.once("end", () => {
          if (response.complete !== true) {
            finish(makeFixedHttpsTransportError("invalid-response-framing"));
            return;
          }
          let headers: Readonly<Record<string, string>>;
          try {
            headers = normaliseHeaders(response.rawHeaders);
          } catch (error) {
            finish(
              isExactFixedHttpsTransportError(error)
                ? error
                : makeFixedHttpsTransportError("unclassified"),
            );
            return;
          }
          const completed = performance.now();
          const connected = connectedAt ?? started;
          finish(null, {
            status: response.statusCode ?? 0,
            headers,
            body: Buffer.concat(chunks, compressedBytes),
            telemetry: Object.freeze({
              dnsMs: roundedMilliseconds(dnsCompleted - dnsStarted),
              resolvedAddressCount: addresses.length,
              selectedAddressFamily: selected.family,
              connectMs: roundedMilliseconds(connected - dnsCompleted),
              responseMs: roundedMilliseconds(completed - connected),
              totalMs: roundedMilliseconds(completed - started),
              compressedBytes,
              tlsProtocol,
              tlsCipher,
            }),
          });
        });
      },
    );
    request.maxHeadersCount = MAX_HEADER_COUNT;

    const onAbort = (): void => {
      request.destroy(abortError());
      finish(abortError());
    };
    if (input.signal?.aborted === true) {
      onAbort();
      return;
    }
    input.signal?.addEventListener("abort", onAbort, { once: true });

    connectTimer = setTimeout(() => {
      request.destroy(makeFixedHttpsTransportError("connect-timeout"));
      finish(makeFixedHttpsTransportError("connect-timeout"));
    }, remainingConnectMs);

    request.once("socket", (socket) => {
      const tlsSocket = socket as TLSSocket;
      tlsSocket.once("secureConnect", () => {
        const remoteAddress = tlsSocket.remoteAddress;
        const pinned = new BlockList();
        pinned.addAddress(selected.address, selected.family === 4 ? "ipv4" : "ipv6");
        if (
          tlsSocket.authorized !== true ||
          remoteAddress === undefined ||
          !pinned.check(remoteAddress, selected.family === 4 ? "ipv4" : "ipv6")
        ) {
          request.destroy(makeFixedHttpsTransportError("unsafe-address"));
          finish(makeFixedHttpsTransportError("unsafe-address"));
          return;
        }
        connectedAt = performance.now();
        if (connectTimer !== undefined) clearTimeout(connectTimer);
        tlsProtocol = tlsSocket.getProtocol();
        try {
          tlsCipher = tlsSocket.getCipher().name;
        } catch {
          tlsCipher = null;
        }
        responseTimer = setTimeout(() => {
          request.destroy(makeFixedHttpsTransportError("response-timeout"));
          finish(makeFixedHttpsTransportError("response-timeout"));
        }, input.policy.responseTimeoutMs);
      });
    });
    request.once("error", (error: Error) => {
      finish(
        responseStarted
          ? normaliseFixedHttpsResponseError(error)
          : normaliseFixedHttpsRequestError(error),
      );
    });
    request.end();
  });
}
