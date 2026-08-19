# Security policy

## Current status

GIS AI GO is a local Stage 0 foundation, not a deployed service. It has no supported
production release and must not be connected to provider credentials, protected data
or public network listeners.

## Reporting

Report a suspected vulnerability privately to the repository owner. Do not include
tokens, credentials, personal data, licensed feature payloads or exploit data in a
public issue. A private reporting channel must be configured before any remote
repository is published.

## Stage 0 controls

- live provider execution is denied by code and tests;
- `.env` files and generated artefacts are ignored;
- synthetic fixtures are the only permitted fixture class;
- application dependencies and GitHub Actions are pinned; the system Graphviz
  renderer is version-recorded but not yet reproducibly installed by CI;
- schema, link, secret and boundary checks run in the assurance command;
- no security claim is made for later identity, policy or hosting designs.

The custom secret scan is a Stage 0 baseline, not a substitute for platform secret
scanning, dependency review or a dedicated security assessment before publication.
