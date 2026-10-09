import { defineConfig } from "vite";
export default defineConfig(({ mode }) => ({
  base: "./",
  build: { assetsInlineLimit: 0, sourcemap: false, outDir: mode === "gcp" ? "dist/gcp" : mode === "hosted" ? "dist-hosted" : mode === "experience-offline" ? "dist/experience-offline" : "dist",
    rollupOptions: { input: mode === "experience-offline" ? { experience: "experience.html" } : { main: "index.html", experience: "experience.html" } } },
  plugins: mode === "hosted" || mode === "gcp" ? [{
    name: "web216-hosted-edition",
    transformIndexHtml(html: string, context) {
      if (context.filename.endsWith("experience.html")) return html;
      const replacements = [
        ["Experimental · local", mode === "gcp" ? "Experimental · private GCP" : "Experimental · private Site"],
        ["This local experiment retrieves two ONS CPIH observations.", "This private experiment retrieves two captured ONS CPIH observations."],
        ["No embedded AI, external account or public MCP service.", mode === "gcp"
          ? "No embedded AI or public MCP service. Access requires the approved private connection."
          : "No embedded AI or public MCP service. Access uses this Site's existing private audience."],
      ] as const;
      for (const [before, after] of replacements) {
        if (html.split(before).length !== 2) throw new Error("Hosted edition requires an exact, unique boundary label.");
        html = html.replace(before, after);
      }
      return html;
    },
  }] : [],
}));
