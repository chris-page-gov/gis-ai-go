declare const safeNavigableHrefBrand: unique symbol;

/** A URL value that has passed the Explorer's navigation policy. */
export type SafeNavigableHref = string & {
  readonly [safeNavigableHrefBrand]: true;
};

const FORBIDDEN_CODE_POINT =
  /[\u0000-\u001f\u007f\u061c\u200e\u200f\u202a-\u202e\u2066-\u2069]/u;
const SCHEME = /^[a-z][a-z0-9+.-]*:/iu;
const ENCODED_SEPARATOR = /%(?:2f|5c)/iu;

function repeatedlyDecode(value: string): string | null {
  let current = value;
  for (let index = 0; index < 4; index += 1) {
    let decoded: string;
    try {
      decoded = decodeURIComponent(current);
    } catch {
      return null;
    }
    if (decoded === current) {
      return decoded;
    }
    current = decoded;
  }
  return null;
}

function hasTraversal(value: string): boolean {
  const path = value.split(/[?#]/u, 1)[0] ?? "";
  const decoded = repeatedlyDecode(path);
  if (decoded === null) {
    return true;
  }
  return decoded.replaceAll("\\", "/").split("/").some((part) => part === "..");
}

/**
 * Return a branded href when it can be used for navigation.
 *
 * Absolute destinations must use HTTPS. Relative destinations must remain on the
 * base origin and must not contain credentials, protocol-relative syntax or path
 * traversal. HTTP is tolerated only when it results from resolving a relative URL
 * against a local development base; an explicitly supplied HTTP URL is rejected.
 */
export function safeNavigableHref(
  value: string,
  base: string | URL,
): SafeNavigableHref | null {
  if (
    value.length === 0 ||
    value.length > 2_048 ||
    value !== value.trim() ||
    FORBIDDEN_CODE_POINT.test(value) ||
    value.startsWith("/") ||
    value.includes("\\") ||
    ENCODED_SEPARATOR.test(value) ||
    hasTraversal(value)
  ) {
    return null;
  }

  let baseUrl: URL;
  let resolved: URL;
  try {
    baseUrl = base instanceof URL ? new URL(base.href) : new URL(base);
    resolved = new URL(value, baseUrl);
  } catch {
    return null;
  }

  if (!new Set(["http:", "https:"]).has(baseUrl.protocol)) {
    return null;
  }
  if (resolved.username || resolved.password) {
    return null;
  }

  const absolute = SCHEME.test(value);
  if (absolute) {
    if (resolved.protocol !== "https:") {
      return null;
    }
  } else {
    const deploymentBase = new URL("./", baseUrl);
    if (
      resolved.origin !== deploymentBase.origin ||
      !resolved.pathname.startsWith(deploymentBase.pathname)
    ) {
      return null;
    }
  }

  if (resolved.protocol !== "https:" && resolved.origin !== baseUrl.origin) {
    return null;
  }
  return value as SafeNavigableHref;
}

export function isSafeNavigableHref(value: string, base: string | URL): boolean {
  return safeNavigableHref(value, base) !== null;
}
