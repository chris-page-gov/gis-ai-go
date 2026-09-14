import { defineConfig } from "vite";
export default defineConfig(({ mode }) => ({
  base: "./",
  build: { assetsInlineLimit: 0, sourcemap: false, outDir: mode === "hosted" ? "dist-hosted" : "dist" },
  plugins: mode === "hosted" ? [{
    name: "web216-hosted-edition",
    transformIndexHtml(html: string) {
      const replacements = [
        ["Experimental · local", "Experimental · private Site"],
        ["This local experiment retrieves two ONS CPIH observations.", "This private experiment retrieves two captured ONS CPIH observations."],
        ["No embedded AI, external account or public MCP service.", "No embedded AI or public MCP service. Access uses this Site's existing private audience."],
      ] as const;
      for (const [before, after] of replacements) {
        if (html.split(before).length !== 2) throw new Error("Hosted edition requires an exact, unique boundary label.");
        html = html.replace(before, after);
      }
      return html;
    },
  }] : [],
}));
