# ADR-0004: Public autonomous delivery

- status: accepted
- decided on: 19 August 2026
- decision maker: Chris Page
- supersedes: the Stage 0 pause and remote-publication restrictions in ADR-0001
  and ADR-0003

## Context

Stage 0 passed at `983b1a102aa8038c9f50ae1b1894315c3ae0b89f`. It deliberately
stopped at a local evidence foundation, but that pause left no live plan, progress,
changelog or implementation workflow and did not deliver a functional product. The
owner has confirmed the GIS AI GO identity, MIT licence and authority to build the
successor product without repeating the completed research.

## Decision

Publish `chris-page-gov/gis-ai-go` as a public MIT repository and build in the open.
GIS AI GO is the current identity; “Locus Accord” remains only in immutable historical
evidence.

Codex may autonomously:

- maintain the live roadmap, progress, backlog and architectural decisions;
- create and manage GitHub issues and milestones;
- branch, commit, open pull requests and squash-merge when mandatory checks pass;
- version, tag, create GitHub releases and deploy approved public/open surfaces;
- progress through evidence gates without requesting repeated stage-entry approval;
- refresh implementation facts that have materially changed, while using rather
  than repeating the completed research.

Every release still requires tests, provenance, accurate claims, a recorded
deployment boundary and rollback. `chris-page-gov/mcp-geo` remains read-only at
`56683b33c0cd02842b7f3ee465414c68a1f3f2a6`.

## Boundaries

Public code and artefacts may contain only public, publishable or clearly synthetic
data. Never commit secrets, provider credentials, protected/licensed feature
payloads, personal data or machine-specific paths.

A specific owner decision is still required for paid services, protected-data
rights, enterprise credentials, legal or trade mark commitments, accepting new
provider terms, material external spend, or destructive changes outside this
repository. Protected deployments require their own rights, security and isolated
infrastructure evidence.

## Consequences

- Evidence gates replace repeated permission gates for the open roadmap.
- GitHub issues and milestones carry work-item status; repository files retain the
  durable release scope and context.
- `main` is protected by pull requests and stable automated assurance.
- The research pack and Stage 0 verification remain historical evidence; they are
  not edited to simulate current authority.
- GitHub Pages remains off until the purpose-built Explorer passes publication,
  security and accessibility gates.
