# Security policy

## Current status

GIS AI GO is intended for public open-source development and has no supported
production release yet. During bootstrap it may be private while publication
controls are verified.
The current gateway and execution service remain fail-closed scaffolds. Do not
connect unreviewed code to provider credentials, protected data or public listeners.

## Reporting

Use GitHub's private vulnerability reporting once the verified public repository
has that feature enabled. Until then, report privately to the repository owner. Do
not include
tokens, credentials, personal data, licensed feature payloads or exploit data in a
public issue. Ordinary non-sensitive defects may use the public bug template.

## Current controls

- live provider execution is denied by code and tests;
- `.env` files and generated artefacts are ignored;
- synthetic fixtures are the only permitted fixture class;
- application dependencies, the WebAssembly diagram renderer and GitHub Actions are
  lockfile or commit pinned;
- schema, link, secret and boundary checks run in the assurance command;
- no security claim is made for later identity, policy or hosting designs.

The custom secret scan is a repository baseline, not a substitute for platform secret
scanning, dependency review or a dedicated security assessment before publication.
