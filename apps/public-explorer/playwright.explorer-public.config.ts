import { defineConfig } from "@playwright/test";

const value = process.env.PUBLIC_BASE_URL?.trim();
if (!value) throw new Error("PUBLIC_BASE_URL is required for Explorer publication assurance");
const base = new URL(value);
const loopback = base.hostname === "127.0.0.1" || base.hostname === "localhost";
if (
  (base.protocol !== "https:" && !(loopback && base.protocol === "http:")) ||
  base.pathname !== "/gis-ai-go/" ||
  base.username || base.password || base.search || base.hash
) {
  throw new Error("PUBLIC_BASE_URL must be a credential-free HTTPS /gis-ai-go/ URL, or loopback HTTP");
}
if (!loopback && base.href !== "https://chris-page-gov.github.io/gis-ai-go/") {
  throw new Error("public verification must use the exact canonical GIS URL");
}
if (!/^[0-9a-f]{40}$/u.test(process.env.EXPECTED_SOURCE_COMMIT ?? "")) {
  throw new Error("EXPECTED_SOURCE_COMMIT must be the accepted full commit");
}

export default defineConfig({
  testDir: "./test/browser",
  testMatch: "explorer-publication.spec.ts",
  outputDir: "./test-results/explorer-public/browser",
  fullyParallel: false,
  forbidOnly: true,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: [
    process.env.CI ? ["github"] : ["list"],
    ["json", { outputFile: "./test-results/explorer-public/browser-results.json" }],
  ],
  globalTimeout: 10 * 60_000,
  timeout: 120_000,
  expect: { timeout: 15_000 },
  use: {
    baseURL: base.href,
    ...(process.env.EXPLORER_CHROME_EXECUTABLE
      ? { launchOptions: { executablePath: process.env.EXPLORER_CHROME_EXECUTABLE } }
      : { channel: "chrome" }),
    locale: "en-GB",
    timezoneId: "Europe/London",
    colorScheme: "light",
    viewport: { width: 1440, height: 1000 },
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
    video: "off",
  },
});
