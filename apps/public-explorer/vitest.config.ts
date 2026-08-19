import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    environment: "jsdom",
    include: ["test/unit/**/*.test.ts", "test/component/**/*.test.ts"],
  },
});
