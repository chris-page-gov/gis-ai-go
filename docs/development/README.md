# Portable development environments

Use repository-relative paths and the host's own `$HOME` only when a personal
location is needed. The GitHub organisation name does not prescribe a local
profile. Keep private configuration, state, approvals and generated evidence in
the approved host's private custody. Operator/build outputs may use its ignored
`artifacts/`; review/admission records stay outside a source checkout that will
be bound into a secure editor container.

On the secure BDUK machine, start with
[the source transition and admission workflow](SECURE_TRANSITION.md). It preserves
the existing clone and dirty work, and requires full source/security and exact
image/platform approval before repository execution or container opening.

## Choose a profile

| Environment | Source and execution boundary | Credentials and acceptance |
| --- | --- | --- |
| Personal local development | Reviewed checkout with public/synthetic fixtures; approved local tools or `.devcontainer/local/devcontainer.json` | No provider/cloud credentials needed for offline checks. Local results do not establish hosted acceptance. |
| Managed cloud development | Authoritative checkout and observed session policy; optional `.devcontainer/cloud/devcontainer.json` | The optional container is offline by default; the approved host owns session proxy/CA/identity. A connected session does not prove cloud access or private routing. |
| Secure BDUK development | Exact GitHub source commit, approved internal image digest and `.devcontainer/bduk/devcontainer.json` with real admission | No automatic host home/socket/credential/protected-data mounts. Real platform identity/network/deployment approval remains separate. |
| Platform builder/operator | Separately reviewed build facilities, registry, tool versions and operator host | `gcloud` and authorised credentials remain on the approved host; exact resource/cost/upload approval precedes cloud mutation. |

The repository's source/lockfiles define Node 24.19.0, pnpm 10.33.2, Python 3.12+
and uv 0.12.2. GCP Terraform uses 1.13.4 and Google provider 6.49.0. A Git clone
supplies source and locks, not package caches, browser binaries, provider binaries
or container layers. Restricted networks need platform-approved mirrors and
installed tools; do not open new egress or replace locks to make a build pass.
The optional development image fixes Python to 3.12.14 and targets Linux amd64;
its toolchain lock is `.devcontainer/image/toolchain.lock.json`.

The optional profiles must not silently install tools, add Dev Container features,
run privileged, request sudo, mount a host Docker socket/home or inherit cloud
credential folders. Development and application runtime images serve different
purposes. A small runtime image does not provide all editor/build tools; a rich
development image is not automatically appropriate for Cloud Run.
See [image options and admission](CONTAINER_IMAGES.md) for the observed official
vendor sources and the exact-image gates.
See [build assurance](BUILD_ASSURANCE.md) for executable build/scan commands,
actual tool/image results and outstanding execution gates.
The [sanitised security record](../security/GCP-223-SECURITY-REVIEW.md) distinguishes
the sealed source findings and blocked original images from subsequent fixes
and the zero-advisory maintained-lock recheck. It does not admit an execution
environment or replace the platform's review of the exact published commit.

## Explicit helper commands

`scripts/environment/environment.sh` never runs as a container-open hook. Invoke
it only after the applicable source/build approval. It performs local checks;
it does not sign platform decisions, pull/open containers or start cloud login.

| Command | Purpose and limits |
| --- | --- |
| `source-manifest --output EXTERNAL_NEW_JSON` | Hash the actual admitted source tree, including relevant untracked work. It is an integrity inventory, not a security scan. |
| `workspace-manifest --output EXTERNAL_NEW_JSON` | Retain the exact ignored-file inventory privately for a separately reviewed reopening; it does not admit that material. |
| `prepare-image --output NEW_DIR` | Stage the locked image context from previously verified cache bytes. Optional `--download` is explicit acquisition; approved `--mirror`/`--ca-file` preserve HTTPS verification. |
| `build-image --context DIR --output NEW_OCI --builder EXISTING_BUILDER` | Build through an already approved OCI-capable builder with offline build steps and provenance. `BUILT_NOT_APPROVED` requires image review and platform admission. |
| `preflight` / `admit --profile local\|cloud\|bduk --image EXACT_REFERENCE` | Inspect the locally cached digest/profile without pulling or opening. BDUK requires exact source/image reviews, offline `--assurance-receipt` and platform approval; missing inputs return `BLOCKED`. |
| `check --container` | Check exact tools, non-root/capability controls and credential/socket exclusions inside an explicitly admitted container. |
| `install --container` | Explicit frozen, offline dependency installation with dependency scripts disabled; absent caches block it. |

Local/cloud use `GIS_AI_GO_DEV_IMAGE`; BDUK uses
`GIS_AI_GO_SECURE_DEV_IMAGE`. Supply the actual approved immutable
`registry/repository@sha256:64_HEX_DIGEST` reference; no default image is chosen.
Profiles use `--pull=never`, `--network=none`, no capabilities, no new privileges,
no automatic ports and explicit UID/GID `1000:1000` (the supplied image's `node` user). The editor also uses UID `1000`; it cannot select a different
UID through a named-user override. Open the selected profile manually
only after admission; the helper does not perform that action.

Keep source/image/platform review records and admission outputs in the approved
private location **outside the checkout**. A workspace bind includes ignored
files too: `.gitignore` does not exclude them from the container. Initial secure
admission requires a source-only workspace; protected data, credentials and
private original archives cannot become an implicit workspace mount. Preserve
existing material if this blocks opening; use the already approved host route
or a separately approved clean source clone rather than deleting/resetting work.
For a later reopening with generated dependencies/build outputs, the optional
`--workspace-review` must bind the exact ignored-file inventory and the platform
approval must bind that review and workspace digest. It is not a blanket folder
exception: changed bytes require a new review, and credentials/state/private
original archives remain excluded. No helper deletes existing material or
generates an approving decision.
Inspect effective container mounts/credential forwarding as well as the declared
configuration; editor integration must not add an SSH agent or credentials.

## Build and verify

On an approved host/builder with the approved package route, follow the ordinary
frozen lockfile workflow from the repository root:

```sh
pnpm install --frozen-lockfile --ignore-scripts --package-import-method=copy
uv sync --locked --group dev --cache-dir .uv-cache
pnpm run check
pnpm run test:gcp
```

The optional containers are offline. Stage exact admitted dependency/browser/
provider caches through the reviewed build route before use; ordinary online
installation commands cannot make their network available. Once manually opened,
the explicit `environment.sh check --container` and `install --container`
commands validate the pinned tools and use frozen offline dependencies. Missing
cache bytes remain blocked; they do not trigger a download or lifecycle hook.
Package imports use copies so cache hardlinks do not violate the runtime
verifier's independent unique-file requirement.

Keep full canonical assurance intact. Browser checks require the exact expected
browser binary and approved installation route; a different local browser smoke
test does not replace them. Any host-specific refused executable, unavailable
mirror, image or runtime prerequisite is a precise blocked gate. Preserve the
failure evidence and continue independent checks.

An approved platform builder may produce the GCP application image and its scan,
SBOM/provenance. The developer container need not gain a Docker socket for this.
Use the [GCP build/install runbook](../deployment/gcp/INSTALL_PLATFORM.md), its
allowlisted upload inventory and exact release bindings. Public metadata and
synthetic fixtures remain the initial data scope; no provider/model or protected
data call is enabled by choosing a profile.

## Operational boundaries

Keep transport authentication, human OIDC identity and server-side authorisation
distinct. Local signed issuer fixtures and emulated state test implementation,
not real Google/Okta identity or Firestore recovery. See
[GCP acceptance](../deployment/gcp/ACCEPTANCE.md) for the hosted gates.

Stop a local candidate with Ctrl-C. Development-container removal, application
rollback and cloud teardown have different effects. Keep owner-private evidence
and state according to their approved retention rather than removing them to
force a new build. Cloud removal uses the explicit approved destructive plan in
[cost and teardown](../deployment/gcp/COST_AND_TEARDOWN.md).
