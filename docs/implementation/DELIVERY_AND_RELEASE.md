# Delivery and release model

## Branch and pull request flow

- `main` is always releasable and accepts changes through pull requests.
- Use short-lived `codex/{work-item}-{description}` branches.
- Use Conventional Commits, for example
  `feat(explorer): add catalogue facets` or `fix(policy): deny unknown licences`.
- Open a draft pull request while work or evidence is incomplete.
- Every material pull request links a backlog item, carries a changelog fragment,
  states its deployment boundary and records rollback.
- Merge by squash after required checks pass and conversations are resolved. Delete
  the branch after merge; do not force-push or delete `main`.
- A lone developer is not required to approve their own pull request. The mandatory
  independent controls are automated assurance and explicit evidence.

## Required assurance

The stable required check is `assurance`. It must run type checks, unit and contract
tests, source/link/research integrity, secret scanning, diagrams and SBOM generation.
Feature work adds affected browser, accessibility, protocol, policy, provider and
deployment tests to the same required gate or a separately required stable check.

Pinned dependencies and GitHub Actions remain mandatory. A dependency change must
update lock files, regenerate the SBOM, record the reason and pass the relevant
same-pattern tests.

## Change and version management

- Use Semantic Versioning. Until `v1.0.0`, minor releases may introduce new public
  capabilities and patch releases remain backwards compatible.
- Keep `VERSION`, root/component npm and Python manifests and workspace-lock versions
  synchronised. `pnpm run validate:versions` enforces this invariant.
- Feature branches add `changelog.d` fragments; the release pull request folds them
  into `CHANGELOG.md` and deletes them.
- The release commit is the only commit that changes versions, finalises the dated
  changelog section and prepares release notes.
- Tag the exact verified release commit as `vX.Y.Z`; never move a published tag.

## Release evidence

Before tagging, record:

- exact commit, clean working tree and required remote checks;
- dependency locks, generated SBOM and source/provenance integrity;
- unit, contract, security, accessibility, browser and interoperability results
  affected by the release;
- built artefact checksums and deployment target;
- known deviations, support boundary and rollback command or procedure.

Create the GitHub release from the immutable tag. Attach or link the checksummed
artefacts and evidence record. Do not describe a local scaffold, draft or synthetic
test as a deployed capability.

## Deployment and rollback

Before the first tag, a public acceptance candidate may deploy only from an attested
successful protected-`main` artefact under the DISC-104 workflow. A supported
release deploys only the artefact built and attested from the exact verified release
commit, after that commit carries its immutable tag. Verify the exact deployed
commit in a real browser/client, including identity, primary
journeys, accessibility, console, security controls and rollback. The live Pages
Explorer remains a release candidate until the `v0.1.0` gate passes; the historical
research viewer is never the product deployment.

Prefer an ordinary revert or previous immutable artefact over history rewriting.
Suspend a provider, tool, registry entry or protected tier independently when its
evidence boundary fails.
