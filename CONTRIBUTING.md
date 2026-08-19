# Contributing

GIS AI GO accepts work scoped by the live roadmap and issue backlog.

Before proposing a change:

1. read [AGENTS.md](AGENTS.md) and the current ADRs;
2. link the pull request to a stable work item or explain the maintenance need;
3. keep fixtures public or unambiguously synthetic;
4. never commit credentials, protected/licensed payloads or personal data;
5. preserve the immutable research pack unchanged;
6. add tests and provenance for every promoted contract or decision;
7. add a changelog fragment for a material change;
8. run `pnpm run check` from the repository root.

Use British English and plain language. Keep facts, assumptions, recommendations and
unresolved questions distinct. Do not add a dependency without pinning it, updating
both lock files where relevant, regenerating the SBOM and recording why it is needed.

Use a short-lived `codex/{work-item}-{description}` branch and Conventional Commits.
Open a draft pull request while evidence is incomplete. Changes are squash-merged
after mandatory assurance passes.

By submitting a contribution, you confirm that you have the right to provide it and
agree that it is licensed under the repository's MIT licence.
