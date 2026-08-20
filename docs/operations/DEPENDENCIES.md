# Dependency baseline

All installed dependencies are exact in `pnpm-lock.yaml` or `uv.lock`.

| Surface | Version or constraint | Purpose |
| --- | --- | --- |
| Node.js | `24.19.0` LTS baseline; engine `>=24.19.0` | TypeScript build and tests |
| pnpm | `10.33.2` | JavaScript workspace and lock |
| TypeScript | `7.0.2` | Strict type checking |
| `@types/node` | `24.13.3` | Node.js 24 types |
| `@modelcontextprotocol/server` | `2.0.0` | MCP 2026-07-28 server and transports |
| `@modelcontextprotocol/node` | `2.0.0` | Streaming Node HTTP adapter |
| `@modelcontextprotocol/client` | `2.0.0` | Development-only conformance client |
| `@viz-js/viz` | `3.29.0` | Lockfile-pinned WebAssembly Graphviz renderer |
| Vite | `8.2.1` | Static Explorer build and local preview only |
| Vitest | `4.1.11` | Explorer unit and component assurance |
| jsdom | `30.0.1` | Standards-based HTML parsing in build-policy and component tests |
| Playwright | `1.62.1` | Real-browser Explorer acceptance using runner Chrome |
| axe-core Playwright integration | `4.13.0` | Automated WCAG 2.2 A and AA checks |
| Python | `>=3.12` | Portable deterministic service and assurance scripts |
| uv | `0.12.2` | Python workspace and lock |
| jsonschema | `4.26.0` | Draft 2020-12 OKF, schema and fixture validation |

The three MCP packages are the exact split v2 packages; the deprecated monolithic
`@modelcontextprotocol/sdk` package and legacy server package are not permitted.
`@modelcontextprotocol/node` brings its pinned Node adapter dependencies, including
`@hono/node-server` and `hono`, through the lockfile. They are transport
implementation details, not an additional application framework selected by GIS AI
GO. The gateway enforces its own exact Host and Origin allow-lists; MCP applies them
before body receipt. The client package is not a gateway runtime dependency.

The gateway loads the canonical catalogue request, result, problem, authority,
policy and evidence schemas from the repository-level `schemas/` directory when
its module is imported. The compiled `apps/mcp-gateway/dist/` output therefore runs
from a complete checkout or equivalent package layout that retains those canonical
schemas; it is not a standalone distribution. This prevents a second copied schema
set from drifting from the direct API and MCP advertisements.

The Explorer has no production runtime dependency. No provider SDK, geospatial
runtime, OPA binary, database driver or cloud dependency is present. The local
gateway transports read only the checksum-verified catalogue and make no provider
network call. Additions follow the live roadmap and dependency assurance rules.

GitHub Actions are pinned to immutable commits in `.github/workflows/ci.yml`; the
comments record the corresponding release tags checked on 19 August 2026.

Diagram rendering uses the same npm-locked WebAssembly package locally and in CI.
Each generated diagram manifest records the renderer version and output SHA-256.
