# Security policy

## Current status

GIS AI GO is a public open-source project. Its supported `v0.1.0` release is a
static, metadata-only discovery product hosted on GitHub Pages.
The generic gateway and execution entrypoints remain fail-closed. A fixed local,
unregistered exact-five container candidate exists for bounded demonstration. Do not
connect unreviewed code to provider credentials, protected data or public listeners.
The public Explorer is a static metadata-only build; it is not a provider client or
property-information service.

## Reporting

Use [GitHub private vulnerability reporting](https://github.com/chris-page-gov/gis-ai-go/security/advisories/new)
for suspected vulnerabilities. Do not include tokens, credentials, personal data,
licensed feature payloads or exploit data in a public issue. Ordinary non-sensitive
defects may use the public bug template.

## Current controls

- live provider execution is available only through the fixed local unregistered
  candidate; its reviewed Compose harness has no external egress, credentials or
  production registration;
- `.env` files and generated artefacts are ignored;
- synthetic fixtures are the only permitted fixture class;
- application dependencies, the WebAssembly diagram renderer and GitHub Actions are
  lockfile or commit pinned;
- schema, link, secret and boundary checks run in the assurance command;
- the Explorer verifies its source inventory and checksums before build, ships no
  production JavaScript dependency, renders catalogue values as text, allowlists
  navigation, rejects symlinked or unallowlisted build inputs and outputs, requires
  its exact restrictive Content Security Policy and makes no cross-origin runtime
  request;
- browser assurance covers hostile URL state, exact-origin requests, console errors,
  keyboard operation and machine-readable download integrity;
- GitHub secret scanning, push protection, Dependabot security updates and CodeQL
  default setup are enabled for the public repository;
- the supported tag is protected against update and deletion by a no-bypass
  ruleset; and
- the immutable GitHub Release retains the checksummed archive, receipts,
  attestation verification, release evidence and dependency SBOM;
- no security claim is made for later identity, policy, provider or service designs.

The custom and platform scans are baselines, not substitutes for dependency review
or a dedicated security assessment before a later networked service, identity,
policy or provider-integration release.
