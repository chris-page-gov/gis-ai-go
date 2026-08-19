# Security policy

## Current status

GIS AI GO is a public open-source project with no supported production release yet.
The current gateway and execution service remain fail-closed scaffolds. Do not
connect unreviewed code to provider credentials, protected data or public listeners.

## Reporting

Use GitHub's private vulnerability reporting for this repository. Do not include
tokens, credentials, personal data, licensed feature payloads or exploit data in a
public issue. Ordinary non-sensitive defects may use the public bug template.

## Current controls

- live provider execution is denied by code and tests;
- `.env` files and generated artefacts are ignored;
- synthetic fixtures are the only permitted fixture class;
- application dependencies and GitHub Actions are pinned; the system Graphviz
  renderer is version-recorded but not yet reproducibly installed by CI;
- schema, link, secret and boundary checks run in the assurance command;
- no security claim is made for later identity, policy or hosting designs.

The custom secret scan is a repository baseline, not a substitute for platform secret
scanning, dependency review or a dedicated security assessment before publication.
