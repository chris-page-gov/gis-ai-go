import { defineConfig } from "@playwright/test";

function requireEnvironment(name: string): string {
  const value = process.env[name]?.trim();
  if (!value) throw new Error(`${name} is required for public deployment assurance`);
  return value;
}

const publicBaseUrl = new URL(requireEnvironment("PUBLIC_BASE_URL"));
if (publicBaseUrl.username || publicBaseUrl.password || publicBaseUrl.search || publicBaseUrl.hash) {
  throw new Error("PUBLIC_BASE_URL must not contain credentials, a query or a fragment");
}
if (!publicBaseUrl.pathname.endsWith("/")) {
  throw new Error("PUBLIC_BASE_URL must end with a slash");
}
const loopback = publicBaseUrl.hostname === "127.0.0.1" || publicBaseUrl.hostname === "localhost";
if (publicBaseUrl.protocol !== "https:" && !(loopback && publicBaseUrl.protocol === "http:")) {
  throw new Error("PUBLIC_BASE_URL must use HTTPS except for a loopback validation server");
}

for (const [name, length] of [
  ["EXPECTED_SOURCE_COMMIT", 40],
  ["EXPECTED_ARCHIVE_SHA256", 64],
  ["EXPECTED_OKF_CONTENT_ROOT", 64],
  ["EXPECTED_PAYLOAD_ROOT", 64],
  ["EXPECTED_PUBLIC_CHECKSUMS_SHA256", 64],
] as const) {
  if (!new RegExp(`^[0-9a-f]{${length}}$`, "u").test(requireEnvironment(name))) {
    throw new Error(`${name} must be a lower-case ${length}-character hexadecimal value`);
  }
}
requireEnvironment("EXPECTED_VERSION");

export default defineConfig({
  testDir: "./test/browser",
  testMatch: "public-deployment.spec.ts",
  outputDir: "./test-results/public",
  fullyParallel: false,
  forbidOnly: true,
  retries: 1,
  workers: 1,
  reporter: process.env.CI ? "github" : "list",
  timeout: 45_000,
  expect: { timeout: 10_000 },
  use: {
    baseURL: publicBaseUrl.href,
    channel: "chrome",
    locale: "en-GB",
    timezoneId: "Europe/London",
    colorScheme: "light",
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
    video: "off",
  },
});
