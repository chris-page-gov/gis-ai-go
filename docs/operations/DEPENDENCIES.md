# Dependency baseline

All installed dependencies are exact in `pnpm-lock.yaml` or `uv.lock`.

| Surface | Version or constraint | Purpose |
| --- | --- | --- |
| Node.js | `24.19.0` LTS baseline; engine `>=24.19.0` | TypeScript build and tests |
| pnpm | `10.33.2` | JavaScript workspace and lock |
| TypeScript | `7.0.2` | Strict type checking |
| `@types/node` | `24.13.3` | Node.js 24 types |
| `@modelcontextprotocol/server` | `2.0.0` | Pinned Stage 2 gateway SDK target; no server is started |
| Python | `>=3.12` | Portable deterministic service and assurance scripts |
| uv | `0.12.2` | Python workspace and lock |
| jsonschema | `4.26.0` | Draft 2020-12 schema and fixture validation |
| Graphviz | CI `2.42.2-9build1`; local verification records the detected version | Diagram rendering |

No provider SDK, web framework, geospatial runtime, OPA binary, database driver or
cloud dependency is present yet. Additions follow the live roadmap and dependency
assurance rules.

GitHub Actions are pinned to immutable commits in `.github/workflows/ci.yml`; the
comments record the corresponding release tags checked on 19 August 2026.

CI installs the exact Graphviz package supplied by Ubuntu 24.04 LTS. Local systems
may use a different version; every render records the detected version, and release
evidence is produced by the pinned CI environment.
