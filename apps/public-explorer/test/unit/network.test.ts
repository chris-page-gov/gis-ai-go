import { describe, expect, it } from "vitest";

import { isRequestFromConfiguredOrigin } from "../fixtures/network";

describe("browser request origin assurance", () => {
  const baseURL = "http://127.0.0.1:4173/";

  it("allows the configured origin", () => {
    expect(isRequestFromConfiguredOrigin("http://127.0.0.1:4173/assets/app.js", baseURL)).toBe(
      true,
    );
  });

  it("rejects a different port on the same host", () => {
    expect(isRequestFromConfiguredOrigin("http://127.0.0.1:43117/track", baseURL)).toBe(false);
  });

  it("rejects a localhost alias and a different scheme", () => {
    expect(isRequestFromConfiguredOrigin("http://localhost:4173/track", baseURL)).toBe(false);
    expect(isRequestFromConfiguredOrigin("https://127.0.0.1:4173/track", baseURL)).toBe(false);
  });
});
