# Contributing

GIS AI GO currently accepts Stage 0 foundation work only.

Before proposing a change:

1. read [AGENTS.md](AGENTS.md) and the current ADRs;
2. keep fixtures public or unambiguously synthetic;
3. do not add live provider calls, credentials, infrastructure or deployment;
4. preserve the immutable research pack unchanged;
5. add tests and provenance for every promoted contract or decision;
6. run `pnpm run check` from the repository root.

Use British English and plain language. Keep facts, assumptions, recommendations and
unresolved questions distinct. Do not add a dependency without pinning it, updating
both lock files where relevant, regenerating the SBOM and recording why it is needed.
