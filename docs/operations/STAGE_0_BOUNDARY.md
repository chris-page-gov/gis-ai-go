# Stage 0 boundary

## Permitted

- governance and architecture records;
- candidate schemas and synthetic fixtures;
- non-networked TypeScript and Python service boundaries;
- source, link, schema, secret, unit and diagram checks;
- dependency locks and a generated manifest SBOM;
- local Git history and local verification.

## Not permitted

- live provider calls or arbitrary URL fetching;
- access tokens, API keys, licensed feature data or personal data;
- public network listeners or server registration;
- OIDC, enterprise device posture or protected policy integration;
- cloud resources, containers, infrastructure deployment or a public site;
- copying MCP-Geo wholesale;
- proceeding to Stage 1 without explicit human approval.

## Verification gate

Report the exact commit, repository and generated boundaries, locked dependency and
SDK versions, schema and source integrity, secret and SBOM results, unit tests,
deviations and rollback. A clean report pauses the work; it does not authorise Stage 1.
