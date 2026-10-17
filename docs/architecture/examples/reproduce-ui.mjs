// Run from the repository root: node docs/architecture/examples/reproduce-ui.mjs
// Read-only reproductions for UI-01 and UI-02 using installed Vite/jsdom modules.
// Expected observations describe review baseline 97bc4563; later fixes may differ.
import { createRequire } from "node:module";
import { resolve } from "node:path";

const appRoot = resolve("apps/public-explorer");
const require = createRequire(`${appRoot}/package.json`);
const { createServer } = await import(require.resolve("vite"));
const { JSDOM } = require("jsdom");
const server = await createServer({
  root: appRoot,
  configFile: false,
  server: { middlewareMode: true, hmr: false, ws: false },
  appType: "custom",
});
let dom;
try {
  const { parseCatalogue, deriveGraph } = await server.ssrLoadModule("@gis-ai-go/contracts");
  const state = await server.ssrLoadModule("/src/state.ts");
  const fixture = await server.ssrLoadModule("/test/unit/fixtures.ts");
  const graph = await server.ssrLoadModule("/src/views/graph.ts");
  const bundle = parseCatalogue(fixture.validCatalogueFixture());
  const canonical = state.canonicaliseState({
    ...state.createDefaultExplorerState(bundle), query: "𐐀".repeat(101),
  }, bundle);
  const url = state.serialiseExplorerUrl(canonical, "https://example.test/", bundle);
  console.log(JSON.stringify({
    case: "Unicode query roundtrip",
    canonicalCodePoints: [...canonical.query].length,
    canonicalUtf16Units: canonical.query.length,
    parsedQuery: state.parseExplorerUrl(url, bundle).query,
  }));

  dom = new JSDOM('<main id="root"><a id="nav" href="#view">Graph</a></main>');
  globalThis.document = dom.window.document;
  globalThis.Node = dom.window.Node;
  document.getElementById("nav").focus();
  const rendered = graph.renderGraphView(
    deriveGraph(bundle.records, bundle.records.map((record) => record.id)),
    bundle.records,
    { hrefForRecord: () => "#record", selectRecord: () => {} },
  );
  document.getElementById("root").replaceChildren(rendered);
  const heading = document.getElementById("view-heading-graph");
  heading.focus();
  console.log(JSON.stringify({
    case: "Actual graph renderer focus", target: heading.id,
    tabindexAttribute: heading.getAttribute("tabindex"),
    activeElement: document.activeElement.tagName,
  }));
} finally {
  delete globalThis.document;
  delete globalThis.Node;
  dom?.window.close();
  await server.close();
}
