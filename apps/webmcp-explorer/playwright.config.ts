import { defineConfig } from "@playwright/test";

const port = Number(process.env.WEBMCP_EXPLORER_PREVIEW_PORT ?? "4183");
const origin = `http://127.0.0.1:${port}`;

export default defineConfig({
  testDir: "./test/browser",
  outputDir: "./test-results",
  fullyParallel: false,
  forbidOnly: Boolean(process.env.CI),
  retries: process.env.CI ? 1 : 0,
  ...(process.env.CI ? { workers: 1 } : {}),
  reporter: process.env.CI ? "github" : "list",
  timeout: 30_000,
  expect: { timeout: 5_000 },
  use: {
    baseURL: `${origin}/`,
    channel: "chrome",
    locale: "en-GB",
    timezoneId: "Europe/London",
    colorScheme: "light",
    screenshot: "only-on-failure",
    trace: "retain-on-failure",
    video: "off",
  },
  webServer: {
    command: `pnpm exec vite preview --host 127.0.0.1 --port ${port} --strictPort`,
    reuseExistingServer: false,
    timeout: 60_000,
    url: `${origin}/`,
  },
});
