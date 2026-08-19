# Security policy

## Current status

GIS AI GO is a public open-source project and has no supported production release
yet.
The current gateway and execution service remain fail-closed scaffolds. Do not
connect unreviewed code to provider credentials, protected data or public listeners.

## Reporting

Use [GitHub private vulnerability reporting](https://github.com/chris-page-gov/gis-ai-go/security/advisories/new)
for suspected vulnerabilities. Do not include tokens, credentials, personal data,
licensed feature payloads or exploit data in a public issue. Ordinary non-sensitive
defects may use the public bug template.

## Current controls

- live provider execution is denied by code and tests;
- `.env` files and generated artefacts are ignored;
- synthetic fixtures are the only permitted fixture class;
- application dependencies, the WebAssembly diagram renderer and GitHub Actions are
  lockfile or commit pinned;
- schema, link, secret and boundary checks run in the assurance command;
- GitHub secret scanning, push protection, Dependabot security updates and CodeQL
  default setup are enabled for the public repository;
- no security claim is made for later identity, policy or hosting designs.

The custom and platform scans are baselines, not substitutes for dependency review
or a dedicated security assessment before a supported release.
