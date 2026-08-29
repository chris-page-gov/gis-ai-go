import { isIP } from "node:net";

const PUBLIC_DNS_HOSTNAME =
  /^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z](?:[a-z0-9-]{0,61}[a-z0-9])?$/u;
const DISALLOWED_PUBLIC_HOSTNAME_SUFFIXES = Object.freeze([
  ".alt",
  ".arpa",
  ".example",
  ".invalid",
  ".internal",
  ".local",
  ".localhost",
  ".onion",
  ".test",
] as const);

export interface PublicHttpsOrigin {
  readonly origin: string;
  readonly hostname: string;
}

/** Parse one exact HTTPS origin with a DNS-form hostname, without DNS or TLS discovery. */
export function parsePublicHttpsOrigin(rawOrigin: unknown): PublicHttpsOrigin {
  if (typeof rawOrigin !== "string" || rawOrigin.length === 0 || rawOrigin.length > 255) {
    throw new Error("The gateway public HTTPS origin is invalid");
  }

  let parsed: URL;
  try {
    parsed = new URL(rawOrigin);
  } catch {
    throw new Error("The gateway public HTTPS origin is invalid");
  }
  const hostname = parsed.hostname;
  if (
    parsed.protocol !== "https:" ||
    parsed.origin !== rawOrigin ||
    parsed.pathname !== "/" ||
    parsed.search !== "" ||
    parsed.hash !== "" ||
    parsed.username !== "" ||
    parsed.password !== "" ||
    parsed.port !== "" ||
    hostname !== hostname.toLowerCase() ||
    isIP(hostname) !== 0 ||
    !PUBLIC_DNS_HOSTNAME.test(hostname) ||
    DISALLOWED_PUBLIC_HOSTNAME_SUFFIXES.some((suffix) => hostname.endsWith(suffix))
  ) {
    throw new Error("The gateway public HTTPS origin is invalid");
  }
  return Object.freeze({ origin: rawOrigin, hostname });
}
