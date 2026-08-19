# Stage 0 dependency baseline

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
| Graphviz | system tool | Diagram rendering; local verification used `15.1.1`, but CI installation is unresolved |

No provider SDK, web framework, geospatial runtime, OPA binary, database driver or
cloud dependency is present in Stage 0. Their selection remains gated.

GitHub Actions are pinned to immutable commits in `.github/workflows/ci.yml`; the
comments record the corresponding release tags checked on 19 August 2026.

Graphviz is the Stage 0 reproducibility exception. The hosted runner may provide a
different version or no `dot` executable. Pinning or installing a verified Graphviz
build is required before treating diagram output as reproducible release evidence.
