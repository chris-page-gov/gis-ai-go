import { JSDOM } from "jsdom";

export const REQUIRED_WEBMCP_CSP =
  "default-src 'none'; script-src 'self'; style-src 'self'; img-src 'self'; " +
  "font-src 'self'; connect-src 'self'; media-src 'none'; object-src 'none'; " +
  "frame-src 'none'; worker-src 'none'; manifest-src 'self'; base-uri 'none'; " +
  "form-action 'self'";

const VALIDATION_ORIGIN = new URL("https://webmcp-explorer.invalid/");
const AUTOMATIC_RESOURCE_SELECTOR = [
  "script",
  "link",
  "img",
  "iframe",
  "audio",
  "video",
  "source",
  "track",
  "embed",
  "object",
  "input[type='image']",
  "svg image",
].join(",");

function exactRelativeAsset(element, attribute, expectedPath, label) {
  const raw = element.getAttribute(attribute);
  const expected = `./${expectedPath}`;
  if (raw !== expected) {
    throw new Error(`${label} must reference exactly ${expected}; found ${raw ?? "missing"}`);
  }
  const resolved = new URL(raw, VALIDATION_ORIGIN);
  if (
    resolved.origin !== VALIDATION_ORIGIN.origin ||
    resolved.pathname !== `/${expectedPath}` ||
    resolved.search ||
    resolved.hash ||
    resolved.username ||
    resolved.password
  ) {
    throw new Error(`${label} does not resolve to the exact same-origin build asset`);
  }
}

/** Verify the security-relevant semantics of the generated HTML document. */
export function verifyDistributionHtml(html, { javascriptPath, stylesheetPath }) {
  const dom = new JSDOM(html, {
    contentType: "text/html",
    url: VALIDATION_ORIGIN.href,
  });
  try {
    const { document, Node } = dom.window;
    if (document.querySelector("base") !== null) {
      throw new Error("WebMCP Explorer distribution must not contain a base element");
    }

    const httpEquiv = [...document.querySelectorAll("meta[http-equiv]")];
    const csp = httpEquiv.filter(
      (element) => element.getAttribute("http-equiv")?.toLowerCase() === "content-security-policy",
    );
    if (httpEquiv.length !== 1 || csp.length !== 1) {
      throw new Error("WebMCP Explorer distribution must contain exactly one CSP meta element");
    }
    const cspElement = csp[0];
    if (cspElement.parentElement !== document.head) {
      throw new Error("WebMCP Explorer CSP meta element must be inside head");
    }
    if (cspElement.getAttribute("content") !== REQUIRED_WEBMCP_CSP) {
      throw new Error("WebMCP Explorer distribution Content Security Policy has drifted");
    }

    const automaticResources = [...document.querySelectorAll(AUTOMATIC_RESOURCE_SELECTOR)];
    if (
      automaticResources.some(
        (element) =>
          (cspElement.compareDocumentPosition(element) & Node.DOCUMENT_POSITION_FOLLOWING) === 0,
      )
    ) {
      throw new Error("WebMCP Explorer CSP must precede every automatic resource element");
    }

    const scripts = [...document.querySelectorAll("script")];
    if (scripts.length !== 1) {
      throw new Error(`Expected one script element; found ${scripts.length}`);
    }
    const script = scripts[0];
    if (script.getAttribute("type") !== "module" || script.textContent?.trim()) {
      throw new Error("WebMCP Explorer script must be an external module with no inline content");
    }
    exactRelativeAsset(script, "src", javascriptPath, "WebMCP Explorer script");

    const links = [...document.querySelectorAll("link")];
    const stylesheets = links.filter((element) =>
      element.relList.contains("stylesheet"),
    );
    const icons = links.filter((element) => element.relList.contains("icon"));
    if (links.length !== 2 || stylesheets.length !== 1 || icons.length !== 1) {
      throw new Error(
        `Expected one stylesheet link and one icon link; found ${links.length} link elements`,
      );
    }
    exactRelativeAsset(
      stylesheets[0],
      "href",
      stylesheetPath,
      "WebMCP Explorer stylesheet",
    );
    exactRelativeAsset(icons[0], "href", "favicon.svg", "WebMCP Explorer icon");

    for (const element of document.querySelectorAll("*")) {
      const hasInlineHandler = [...element.attributes].some((attribute) =>
        attribute.name.toLowerCase().startsWith("on"),
      );
      if (hasInlineHandler) {
        throw new Error("WebMCP Explorer distribution must not contain inline event handlers");
      }
    }
  } finally {
    dom.window.close();
  }
}
