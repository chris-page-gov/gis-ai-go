# Dependency security disposition, 17 October 2026

Status: source repair locally verified; canonical CI, hosted
publication and GitHub alert closure remain separate gates. Tracking:
[issue #142](https://github.com/chris-page-gov/gis-ai-go/issues/142).

The implementation starts from repository commit
`ca09c5630bf41798e4c8b04632e7a855efcfede0`. The owner has chosen completion of the
existing private Sites teaching exemplar first. The full exact-five gateway port
remains a later milestone with unchanged release requirements.

## Advisory evidence and minimum replacements

The pinned `pnpm 10.33.2 audit --json` command reported 14 advisories: five high,
six moderate and three low. The [complete before report](evidence/dependency-audit-2026-10-17.before.json)
retains the registry's advisory text, affected ranges and dependency paths. The
same command after the replacements returned zero advisories in its
[complete after report](evidence/dependency-audit-2026-10-17.after.json).
No advisory was suppressed or ignored. GitHub's separate 16-alert notification is
not the same data source or result; its current state still needs readback after
the repair reaches the default branch.

| Package and old version | Exact replacement | Advisory and affected condition |
| --- | --- | --- |
| Hono `4.13.5` | `4.13.7` | [GHSA-hxh3-vqpv-xpqv](https://github.com/advisories/GHSA-hxh3-vqpv-xpqv): plain strings rendered through affected JSX boundary/server-rendering paths can become HTML. |
| Undici `8.10.0` | `8.10.2` | Eleven advisories covering WebSocket/retry/decompression denial of service, cache isolation and cookie disclosure, TLS options in `BalancedPool`, and response handling. Exact identifiers and conditions are in the retained report. |
| source-map-js `1.2.1` | `1.2.2` | [GHSA-68fv-2mgg-jv7q](https://github.com/advisories/GHSA-68fv-2mgg-jv7q): hostile indexed source-map section offsets can block the event loop. |
| MCP client `2.0.0` | `2.2.0`, with its core `2.2.0` | [GHSA-6qxp-vccf-f47h](https://github.com/advisories/GHSA-6qxp-vccf-f47h): configured OAuth clients could send existing credentials to an authorization server selected by an untrusted MCP server. |

The public npm registry returned these exact versions, integrity values and Node
engine requirements. The lockfile records the package integrities. All admit the
repository's Node `24.19.0`; no SDK server, Node adapter, jsdom, Vite or Node runtime
upgrade is needed for this bounded patch. Hono's existing exact override changes;
`jsdom>undici` has a targeted override; source-map-js is pinned for both css-tree
and PostCSS; both direct MCP client declarations change to `2.2.0`.

## Actual source exposure

- **Hono is production-installed in the Node gateway dependency closure.** The
  `@modelcontextprotocol/node`/`@hono/node-server` dependency path retains it in
  the production deployment. The maintained ingress uses the SDK's Node bridge;
  no authored Hono JSX rendering was identified. This narrows the known advisory
  path, but does not remove affected installed bytes. A fresh OCI build and scan
  are still required to verify the resulting image.
- **The MCP client is shipped browser code.** The
  [workbench manifest](../../apps/public-data-workbench/package.json#L16) declares
  it as a production dependency; [the browser client](../../apps/public-data-workbench/src/mcp-client.ts#L1)
  imports it and configures a bounded fetch transport. The gateway also uses the
  client in development and evaluation. No authored `authProvider`, `withOAuth`,
  `fetchToken` or credential-provider configuration was found in these paths.
  The affected OAuth workflow is therefore not configured by the inspected code;
  this is not a claim that all OAuth library code is absent from emitted assets.
  Rebuilding and republishing the hosted workbench is necessary before claiming
  that the active Site serves the patched client.
- **Undici and source-map-js are development/build dependencies here.** All three
  frontends use jsdom for tests; Explorer HTML/build boundary checks also use it.
  The inspected authored JSDOM construction does not enable scripts or external
  resources. jsdom nevertheless implements fetch-related and WebSocket behaviour
  using Undici. source-map-js is also reached through Vite's PostCSS tooling.
  Development classification is not an exemption from patching these packages.
- **The private six-tool Worker server has a separate graph.** Its package uses
  the SDK server's Workers shim rather than the Node adapter. The server and
  `@modelcontextprotocol/node` remain `2.0.0`; the patched client has a separate
  core `2.2.0` dependency. No claim is made about the complete private Site/Vinext
  dependency closure without its recovered source and lockfile.
- **Node's bundled Undici is separate.** Updating the npm `undici` package does
  not replace the implementation used by Node's native `fetch`. Existing exact
  runtime-image scans and Node advisory review remain applicable.

The MCP advisory also requires correct issuer binding if OAuth is introduced:
bundled credential providers need `expectedIssuer`; persisted/pre-registered
credentials must retain their `issuer`. The package upgrade does not authorise
new authentication flows or convert a private test token into owner OAuth.

## Resolver result and evidence compatibility

The 2 October Dependabot logs in issue #142 reported Hono/Undici updates as
impossible and showed both pnpm `10.33.2` and a later helper using `11.25.0`.
The current repair used **only `10.33.2`**, successfully resolving the four
minimum fixed versions and completing a frozen-lock installation with dependency
scripts disabled. The old Hono override explicitly held the affected version;
jsdom's Undici range already admitted the patch. The successful current resolver
run establishes a working pinned route, not the historical updater's root cause.

The historical protocol matrix and its original `2.0.0` client observation remain
unchanged. Current package/lock assertions separately require `2.2.0`. The Sites
evaluation harness checks its actual installed client and reports `2.2.0`; its
unchanged v1 report shape permits only the historical `2.0.0` and current `2.2.0`
identifiers. Tests require the current value and reject an unadmitted version.
The local Worker probe now names client and server SDK versions separately.
Current local qualification receipts were regenerated by executing their selected
suites. Only the package/source-lock hashes and derived identities changed;
assertions, outcomes and boundaries are unchanged. This does not extend historical
host attestations. The updated third-party notice is bound by both the OKF source
lock and the current gateway-image receipt contract.

## Verification and remaining gates

The local checks passed:

| Check | Observed result and limit |
| --- | --- |
| Locked installation and registry audit | pnpm `10.33.2`, frozen lockfile and disabled dependency scripts; 14 advisories before, zero after. |
| Builds and types | Complete workspace build/typechecks and final Explorer/WebMCP/workbench builds, including hosted workbench, passed with client `2.2.0` and server `2.0.0`. |
| Gateway runtime | 352 maintained tests exercised; 351 passed on the first run. One unchanged launcher-mode assertion failed because this worktree's restrictive creation mask produced `0700` for Git's `100755` files. Restoring the intended `0755` launcher modes made that one test pass; no assertion or runtime source was changed. |
| Sites evaluation | All 22 evaluator/native-mount tests passed, including the three supported protocol revisions and current/historical report-version validation. No hosted provider was called. |
| Frontend unit/build boundaries | 102 Vitest tests (51 Explorer, seven WebMCP, 44 workbench) and 26 Node build-policy tests passed. |
| Interoperability | The maintained two Node invocations completed with 76 passes and 14 existing macOS-specific skips on Linux. Five local-edition client tests also passed. |
| Contracts and evidence | All 136 repository-boundary, protocol-matrix, strict-evidence, local-receipt and gateway-image contract tests passed after the final notice binding and receipt refresh. Root contract validation accepted 102 schemas/153 records and rejected ten forbidden selection mutations. |
| SBOM | Generated 170 components, including client/core `2.2.0`, separate server core `2.0.0`, and the patched Hono/Undici/source-map-js packages. |

The first protocol-matrix run detected a pre-existing comment-only source-binding
drift in `reconciliation-index.ts`. The preceding integration repair was applied
before the successful 51-test run. Updating the third-party notice then required
refreshing its two current source pins and regenerating the current local receipts.
Earlier failures remain part of this record; historical matrices and previous host
observations retain their original identities. Independent review found no
actionable functional issue. Its final notice/receipt review independently
recomputed the changed identities and confirmed that assertions, outcomes, limits
and historical evidence remained unchanged.

Documentation checks resolved 1,293 local Markdown links, 183 research hashes,
two ledger snapshots and 71 source identifiers, and validated 115 changelog
fragments. The baseline secret and machine-path scan checked 32,284 text files
without a match. The final diff passed whitespace checks.

Canonical repository, image, independent derivation, provenance and CodeQL checks
must pass for the final candidate. Current registry audit success does not replace
those controls. The updated Sites source/build helper remains unavailable, so a
new private Site build/publication and native installed-client call remain pending.
Existing version-8 observations prove only their own source and configuration.

Retained report SHA-256 values:

- Before: `bd628a0cecab5966d47aee7908605cf2a839ba9eca982fb57983637614b646df`.
- After: `a8a7a974183836dac9cc62194a0be09cb15c2244ff5554370bd3695d964008c6`.
