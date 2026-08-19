# Governance

## Decision authority

The repository owner and copyright holder, Chris Page, approves stage entry, release,
publication, licensing changes and any use of protected or commercially licensed
data. Contributors may prepare evidence and recommendations but must not cross a
stage gate without explicit human approval.

## Stage gates

1. Stage 0 establishes the repository, evidence, contracts and assurance harness.
2. Stage 1 may build an open static discovery pack only after Stage 0 approval.
3. Later MCP, identity, protected-data and hosting stages each require a separate
   recorded decision.

A stage decision must state scope, evidence, known deviations, rollback and who
approved it. Material architectural changes require an ADR under `docs/decisions/`.

## Stewardship

Every future tool, provider, dataset and workflow must identify an owner, steward,
status, policy boundary, evidence route and decommissioning route. Source systems
remain authoritative; GIS AI GO does not invent licence or legal authority.

## Publication boundary

This local repository is not a publication. Creating a GitHub repository, pushing a
branch, deploying a site, registering an MCP server or reserving package names needs
separate approval.
