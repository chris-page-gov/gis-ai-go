import { describe, expect, it } from "vitest";

import { isSafeNavigableHref, safeNavigableHref } from "../../src/links.js";

const BASE = "https://example.test/gis-ai-go/index.html";

describe("navigable link policy", () => {
  it("allows HTTPS destinations and deployment-relative paths", () => {
    expect(safeNavigableHref("https://www.gov.uk/guidance/example", BASE)).toBe(
      "https://www.gov.uk/guidance/example",
    );
    expect(isSafeNavigableHref("catalogue/okf-bundle.json", BASE)).toBe(true);
    expect(isSafeNavigableHref("./records/example", BASE)).toBe(true);
    expect(isSafeNavigableHref("?view=graph#record=example", BASE)).toBe(true);
  });

  it("rejects same-origin relative links outside the deployment base", () => {
    expect(isSafeNavigableHref("../outside.html", BASE)).toBe(false);
    expect(isSafeNavigableHref("/outside.html", BASE)).toBe(false);
    expect(isSafeNavigableHref("/gis-ai-go/catalogue/okf-bundle.json", BASE)).toBe(false);
    expect(isSafeNavigableHref("%252e%252e/outside.html", BASE)).toBe(false);
  });

  it.each([
    "http://example.test/unsafe",
    "javascript:alert(1)",
    "data:text/html,unsafe",
    "file:///tmp/unsafe",
    "//example.test/unsafe",
    "https://user:password@example.test/",
    " https://example.test/",
    "https://example.test/a%2fb",
    "https://example.test/\u202eunsafe",
  ])("rejects %s", (value) => {
    expect(isSafeNavigableHref(value, BASE)).toBe(false);
  });
});
