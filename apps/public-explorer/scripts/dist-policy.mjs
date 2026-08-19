import { JSDOM } from "jsdom";

const EXPECTED_CSP_DIRECTIVES = Object.freeze([
  ["default-src", "'none'"],
  ["script-src", "'self'"],
  ["style-src", "'self'"],
  ["img-src", "'self'"],
  ["font-src", "'self'"],
  ["connect-src", "'self'"],
  ["media-src", "'none'"],
  ["object-src", "'none'"],
  ["frame-src", "'none'"],
  ["worker-src", "'none'"],
  ["manifest-src", "'self'"],
  ["base-uri", "'none'"],
  ["form-action", "'none'"],
]);

function parseCsp(value) {
  const directives = new Map();
  for (const part of value
    .split(";")
    .map((item) => item.trim())
    .filter(Boolean)) {
    const [rawDirective, ...tokens] = part.split(/\s+/u);
    const directive = rawDirective.toLowerCase();
    if (directives.has(directive)) {
      throw new Error(`Content Security Policy contains duplicate directive: ${directive}`);
    }
    directives.set(directive, tokens.join(" "));
  }
  return directives;
}

export function requireExactCsp(value) {
  const actual = parseCsp(value);
  const expected = new Map(EXPECTED_CSP_DIRECTIVES);
  const missing = [...expected.keys()].filter((directive) => !actual.has(directive));
  const extra = [...actual.keys()].filter((directive) => !expected.has(directive));
  if (missing.length > 0 || extra.length > 0) {
    throw new Error(
      `Content Security Policy directive set differs from the required policy; ` +
        `missing=${missing.join(",") || "none"}; extra=${extra.join(",") || "none"}`,
    );
  }
  for (const [directive, requiredValue] of expected) {
    const actualValue = actual.get(directive);
    if (actualValue !== requiredValue) {
      throw new Error(
        `Content Security Policy ${directive} must be exactly: ${requiredValue}; ` +
          `found: ${actualValue || "<empty>"}`,
      );
    }
  }
}

export function inspectHtmlDocument(html) {
  const { document, Node } = new JSDOM(html).window;
  if (document.documentElement.getAttribute("lang") !== "en-GB") {
    throw new Error("Explorer index must declare lang=en-GB");
  }
  if (!document.head.querySelector('meta[name="viewport"]')) {
    throw new Error("Explorer index must declare a viewport");
  }

  const cspElements = [...document.head.querySelectorAll("meta")].filter(
    (element) =>
      element.getAttribute("http-equiv")?.toLowerCase() === "content-security-policy",
  );
  if (cspElements.length !== 1 || !cspElements[0].getAttribute("content")) {
    throw new Error("Explorer index must contain exactly one Content Security Policy meta element");
  }
  const [cspElement] = cspElements;
  requireExactCsp(cspElement.getAttribute("content"));

  const firstScript = document.querySelector("script");
  if (
    firstScript &&
    !(cspElement.compareDocumentPosition(firstScript) & Node.DOCUMENT_POSITION_FOLLOWING)
  ) {
    throw new Error("Content Security Policy must precede executable scripts");
  }
  const inlineScripts = [...document.querySelectorAll("script")].filter(
    (element) => !element.hasAttribute("src") && element.textContent.trim(),
  );
  if (inlineScripts.length > 0) {
    throw new Error("Explorer index must not contain inline executable scripts");
  }

  const references = [];
  for (const element of document.querySelectorAll("[src], [href]")) {
    for (const name of ["src", "href"]) {
      const value = element.getAttribute(name);
      if (!value || value.startsWith("#")) continue;
      if (/^(?:[a-z][a-z0-9+.-]*:|\/\/|\/)/iu.test(value)) {
        throw new Error(`Built HTML contains a non-relative asset URL: ${value}`);
      }
      references.push(value);
    }
  }
  return references;
}

export function requireExactInventory(actualFiles, expectedFiles) {
  const actual = [...new Set(actualFiles)].sort();
  const expected = [...new Set(expectedFiles)].sort();
  const missing = expected.filter((path) => !actual.includes(path));
  const extra = actual.filter((path) => !expected.includes(path));
  if (missing.length > 0 || extra.length > 0) {
    throw new Error(
      `Distribution inventory differs from the required publication; ` +
        `missing=${missing.join(",") || "none"}; extra=${extra.join(",") || "none"}`,
    );
  }
}

export const REQUIRED_CSP = EXPECTED_CSP_DIRECTIVES
  .map(([directive, value]) => `${directive} ${value}`)
  .join("; ");
