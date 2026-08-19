# Governance

## Decision authority

The repository owner and copyright holder, Chris Page, retains final authority for
licensing changes, protected or commercially licensed data, paid services,
enterprise credentials and legal commitments. ADR-0004 authorises Codex to deliver,
release and deploy the open roadmap without repeated stage-entry approval.

## Evidence gates

1. Stage 0 established the repository, evidence, contracts and assurance harness.
2. Open discovery, MCP and governed-platform releases advance when their documented
   tests, provenance, security, accessibility and rollback evidence pass.
3. Protected-data pilots and material paid infrastructure require separate rights,
   security and owner decisions.

A release decision must state scope, evidence, known deviations and rollback.
Material architectural changes require an ADR under `docs/decisions/`.

## Stewardship

Every future tool, provider, dataset and workflow must identify an owner, steward,
status, policy boundary, evidence route and decommissioning route. Source systems
remain authoritative; GIS AI GO does not invent licence or legal authority.

## Publication boundary

The public GitHub repository, open-source releases, hardened GitHub Pages Explorer
and tested open service are authorised by ADR-0004. A source push is not proof that a
site or service is deployed: every published surface needs exact-commit verification
and an evidence-backed rollback. Protected integrations, paid hosting, provider
terms and formal registry/package publication remain subject to their recorded
release and rights gates.
