import assert from "node:assert/strict";
import test from "node:test";

import {
  inspectHtmlDocument,
  REQUIRED_CSP,
  requireExactCsp,
  requireExactInventory,
} from "../../scripts/dist-policy.mjs";

function htmlWith({ csp = `content="${REQUIRED_CSP}"`, script = 'src="assets/app.js"' } = {}) {
  return `<!doctype html><html lang="en-GB"><head>` +
    `<meta name="viewport" content="width=device-width">` +
    `<meta http-equiv="Content-Security-Policy" ${csp}>` +
    `</head><body><script ${script}></script></body></html>`;
}

test("inspects the browser-parsed HTML document", () => {
  assert.deepEqual(inspectHtmlDocument(htmlWith()), ["assets/app.js"]);
});

test("does not accept data attributes as policy or script attributes", () => {
  assert.throws(
    () =>
      inspectHtmlDocument(
        '<!doctype html><html lang="en-GB"><head>' +
          '<meta name="viewport" content="width=device-width">' +
          `<meta data-http-equiv="Content-Security-Policy" data-content="${REQUIRED_CSP}">` +
          '</head><body><script data-src="assets/app.js">alert(1)</script></body></html>',
      ),
    /exactly one Content Security Policy/u,
  );
});

test("rejects an unquoted weak policy before the exact duplicate", () => {
  assert.throws(
    () =>
      inspectHtmlDocument(
        htmlWith({ csp: `content=upgrade-insecure-requests content="${REQUIRED_CSP}"` }),
      ),
    /directive set differs/u,
  );
});

test("rejects an unquoted external script source", () => {
  assert.throws(
    () => inspectHtmlDocument(htmlWith({ script: "src=https://attacker.invalid/payload.js" })),
    /non-relative asset URL/u,
  );
});

test("accepts the exact Explorer Content Security Policy", () => {
  assert.doesNotThrow(() => requireExactCsp(REQUIRED_CSP));
});

test("rejects duplicate Content Security Policy directives", () => {
  assert.throws(
    () => requireExactCsp(`${REQUIRED_CSP}; img-src https:`),
    /duplicate directive: img-src/u,
  );
});

test("rejects a weaker Content Security Policy directive", () => {
  assert.throws(
    () => requireExactCsp(REQUIRED_CSP.replace("img-src 'self'", "img-src *")),
    /img-src must be exactly/u,
  );
});

test("rejects default-src self as an alternative", () => {
  assert.throws(
    () => requireExactCsp(REQUIRED_CSP.replace("default-src 'none'", "default-src 'self'")),
    /default-src must be exactly/u,
  );
});

test("rejects an omitted Content Security Policy directive", () => {
  assert.throws(
    () => requireExactCsp(REQUIRED_CSP.replace("; worker-src 'none'", "")),
    /missing=worker-src/u,
  );
});

test("rejects an extra Content Security Policy directive", () => {
  assert.throws(
    () => requireExactCsp(`${REQUIRED_CSP}; child-src 'none'`),
    /extra=child-src/u,
  );
});

test("rejects an arbitrary extra distribution file", () => {
  assert.throws(
    () =>
      requireExactInventory(
        ["index.html", "favicon.svg", "assets/app.js", "debug.txt"],
        ["index.html", "favicon.svg", "assets/app.js"],
      ),
    /extra=debug\.txt/u,
  );
});

test("accepts the exact distribution inventory independent of ordering", () => {
  assert.doesNotThrow(() =>
    requireExactInventory(
      ["index.html", "assets/app.js", "favicon.svg"],
      ["favicon.svg", "index.html", "assets/app.js"],
    ),
  );
});
