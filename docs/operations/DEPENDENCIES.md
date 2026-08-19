# Dependency baseline

All installed dependencies are exact in `pnpm-lock.yaml` or `uv.lock`.

| Surface | Version or constraint | Purpose |
| --- | --- | --- |
| Node.js | `24.19.0` LTS baseline; engine `>=24.19.0` | TypeScript build and tests |
| pnpm | `10.33.2` | JavaScript workspace and lock |
| TypeScript | `7.0.2` | Strict type checking |
| `@types/node` | `24.13.3` | Node.js 24 types |
| `@modelcontextprotocol/server` | `2.0.0` | Pinned Stage 2 gateway SDK target; no server is started |
| `@viz-js/viz` | `3.29.0` | Lockfile-pinned WebAssembly Graphviz renderer |
| Python | `>=3.12` | Portable deterministic service and assurance scripts |
| uv | `0.12.2` | Python workspace and lock |
| jsonschema | `4.26.0` | Draft 2020-12 OKF, schema and fixture validation |

No provider SDK, web framework, geospatial runtime, OPA binary, database driver or
cloud dependency is present yet. Additions follow the live roadmap and dependency
assurance rules.

GitHub Actions are pinned to immutable commits in `.github/workflows/ci.yml`; the
comments record the corresponding release tags checked on 19 August 2026.

Diagram rendering uses the same npm-locked WebAssembly package locally and in CI.
Each generated diagram manifest records the renderer version and output SHA-256.
