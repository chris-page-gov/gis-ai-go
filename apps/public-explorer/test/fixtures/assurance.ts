import { expect, test as base } from "@playwright/test";

import { isRequestFromConfiguredOrigin } from "./network";

type AssuranceFixtures = { browserAssurance: void };

export const test = base.extend<AssuranceFixtures>({
  browserAssurance: [
    async ({ baseURL, page }, use, testInfo) => {
      if (!baseURL) throw new Error("Browser assurance requires a configured baseURL");
      const failures: string[] = [];
      const externalRequests: string[] = [];
      page.on("console", (message) => {
        if (message.type() === "error") failures.push(`console: ${message.text()}`);
      });
      page.on("pageerror", (error) => failures.push(`pageerror: ${error.message}`));
      page.on("requestfailed", (request) => {
        failures.push(`requestfailed: ${request.method()} ${request.url()}`);
      });
      page.on("response", (response) => {
        if (response.status() >= 400) failures.push(`response ${response.status()}: ${response.url()}`);
      });
      page.on("request", (request) => {
        if (!isRequestFromConfiguredOrigin(request.url(), baseURL)) {
          externalRequests.push(`${request.method()} ${request.url()}`);
        }
      });
      await page.addInitScript(() => {
        Reflect.deleteProperty(globalThis, "webMCP");
        Reflect.deleteProperty(globalThis, "modelContext");
        try {
          Object.defineProperty(navigator, "modelContext", {
            configurable: true,
            value: undefined,
          });
        } catch {
          // An absent or non-configurable experimental API is a valid no-WebMCP state.
        }
      });
      await use();
      if (failures.length || externalRequests.length) {
        await testInfo.attach("browser-assurance-errors", {
          body: [...failures, ...externalRequests.map((value) => `external: ${value}`)].join("\n"),
          contentType: "text/plain",
        });
      }
      expect(externalRequests, "the static Explorer must use its configured origin only").toEqual(
        [],
      );
      expect(failures, "the browser console and request lifecycle must stay clean").toEqual([]);
    },
    { auto: true },
  ],
});

export { expect };
