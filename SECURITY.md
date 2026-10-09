# Security policy

## Current status

GIS AI GO is a public open-source project. Its supported `v0.1.0` release is a
static, metadata-only discovery product hosted on GitHub Pages.
The generic gateway and execution entrypoints remain fail-closed. The accepted
local exact-five candidate and the additive private GCP deployment have distinct
entrypoints and acceptance requirements. The GCP website, OKF/OKF+ evidence
surfaces and custom Streamable HTTP MCP are implemented and locally tested;
hosted authentication, persistence and BDUK acceptance remain unverified. Do not
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
  production registration. The private GCP profile admits public metadata and
  synthetic fixtures only and makes no external model or live-provider calls;
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
- private Cloud Run requires approved private ingress and separate transport
  identity, human identity and server-enforced application authorisation. BDUK
  uses approved platform networking and Okta inputs; these contracts require
  real hosted evidence before acceptance;
- development profiles use explicit image digests, non-root execution, no
  privilege escalation, no default external network, and no automatic source
  scripts, dependency installation or deployment. Editor containers do not
  receive host Docker sockets, cloud credentials or protected data; and
- local tests and source/container scans establish only their recorded scope.
  They do not grant platform execution, deployment, spending or data authority.

## Secure-machine execution and container builds

Keep the existing workspace untrusted while fetching and reviewing source with
the platform's approved Git client. Before executing repository scripts,
installing dependencies, building, or opening a development container on the
secure machine, require an approved full-source review for the exact commit and
source digest. Retain the scan's findings, coverage and unresolved questions;
partial coverage or an unresolved finding is not a clean bill of health.

Separately approve the immutable image digest, its SBOM, a fresh offline
vulnerability scan, provenance/signature verification, licences, builder and
registry. HIGH/CRITICAL image findings block the supplied image-assurance helper.
A missing/stale database, unknown scanner version or malformed report blocks it
too. A scan result does not authenticate a platform approver or substitute for
the platform's vulnerability policy. Development and deployment images need
their own evidence.

Use a reviewed minimal build context, checksum-pinned tools and frozen dependency
locks. Acquire public dependencies through approved mirrors before offline build
steps; preserve certificate/signature/checksum checks. Do not mount host home,
SSH agents, cloud configuration, the Docker socket or protected workbench
folders. Gitignore does not remove physical files from a workspace bind mount.
Inspect actual engine mounts and Dev Containers credential integrations before
accepting an editor session. An authorised build service is a separate boundary.

Docker Hardened Images, Chainguard or distroless are possible platform choices;
an image-family name is not approval for a digest, a vulnerability result, or a
FIPS/STIG certification. The supplied toolchain uses pinned Docker Official
Images and does not claim to be a Docker Hardened Image. See the
[profile guide](docs/development/README.md),
[secure transition](docs/development/SECURE_TRANSITION.md) and
[GCP platform review](docs/deployment/gcp/PLATFORM_APPROVAL.md).

The custom and platform scans are baselines, not substitutes for dependency review
or a dedicated security assessment before a later networked service, identity,
policy or provider-integration release.
