# Codex hand-off: Locus Accord Stage 0 only

## Controlling instruction

This hand-off prepares a **new repository** for a governed geospatial knowledge and action platform. It does not authorise creation of that repository in the current research phase. When a human explicitly authorises implementation, Codex must start with **Stage 0 only**, pause at the verification gate and report evidence before proceeding.

Do **not** modify, rename, archive, transfer or create branches/PRs in `chris-page-gov/mcp-geo`. Treat it as read-only historical evidence at commit `56683b33c0cd02842b7f3ee465414c68a1f3f2a6`.

## Read first

1. [`../report/00-executive-decision.md`](../report/00-executive-decision.md)
2. [`ARCHITECTURE_DECISIONS.md`](ARCHITECTURE_DECISIONS.md)
3. [`TECHNICAL_SPEC.md`](TECHNICAL_SPEC.md)
4. [`AGENTS.md`](AGENTS.md)
5. [`../data/requirements.json`](../data/requirements.json)
6. all schemas in [`../schemas/`](../schemas/)
7. [`ACCEPTANCE_TESTS.md`](ACCEPTANCE_TESTS.md)
8. [`MIGRATION_HARVEST.md`](MIGRATION_HARVEST.md)

## Product objective

Create a governed geospatial knowledge and action platform with:

- OKF 0.2 discovery and evidence-linked public presentation;
- MCP 2026-07-28 policy-filtered tools/resources;
- TypeScript MCP/control gateway;
- Python deterministic geospatial execution service;
- PostGIS and object storage;
- OIDC/OAuth, OPA, transaction permits and trusted device posture;
- physically separated open, PSGA and commercial tiers;
- canonical audit events and result evidence receipts;
- complete non-UI results for every optional MCP App;
- an open read-only WebMCP experiment only.

## Stage 0 authorised deliverables after human approval

- new repository skeleton from [`REPOSITORY_TREE.txt`](REPOSITORY_TREE.txt);
- `README.md`, `LICENSE`, `SECURITY.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `GOVERNANCE.md`, `AGENTS.md`;
- copied/adapted decision records and schemas, retaining source links and dates;
- TypeScript and Python workspace scaffolds with no live provider calls;
- synthetic fixtures only;
- schema validation, source/link integrity, secret scan, dependency lock and unit-test CI;
- threat/acceptance test manifests;
- architecture diagrams rendered in CI;
- no cloud resources, provider credentials, licensed data, protected identity integration or deployment.

## Verification pause

Before Stage 1, Codex must report:

- exact commit SHA;
- tree and generated-file boundaries;
- dependency/SDK versions and locks;
- schema-validation results;
- source/link integrity results;
- secret/SBOM results;
- test results;
- unresolved deviations from decisions D01–D20;
- rollback method.

A human must explicitly approve the next stage.

## Non-goals

No production deployment, no PSGA/commercial data, no provider credential brokerage, no autonomous legal/planning decisions, no arbitrary URL fetching, no general code execution, no Kubernetes and no migration by copying MCP-Geo wholesale.
