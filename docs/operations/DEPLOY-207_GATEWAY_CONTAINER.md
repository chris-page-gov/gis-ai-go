# DEPLOY-207 blocked gateway container

Status: repository-only candidate; inactive and undeployed.

This runbook covers the image, local Compose and assurance slice that can proceed
without selecting a public runtime. It does not activate GIS AI GO, contact ONS,
publish an image, create an HTTPS endpoint, register an MCP service or change the
supported `v0.1.0` release.

## Exact boundary

The image has one fixed entry point. It binds `0.0.0.0:8787` inside the container so
the local bridge can reach it. Compose declares only `127.0.0.1:8787` for host
publication. Startup:

1. rejects command-line arguments;
2. asserts that production activation is blocked and every active list is empty;
3. verifies the fixed `/app/artifacts/okf` bundle;
4. opens and fully verifies the fixed, disjoint ledger and reconciliation roots;
5. constructs the gateway without an operation, resource, application or provider
   override; and
6. emits only a bounded lifecycle event and the catalogue revision.

The opened storage proves that the volume topology is admissible. It is not mounted
into an application while no operation is active.

The container HTTP surface is deliberately:

| Route | Expected result |
| --- | --- |
| `GET /healthz` | `200`, candidate lifecycle and exact catalogue identity |
| `GET /readyz` | `503`, the reviewed block reason and empty operation arrays |
| `GET /openapi.json` | `200`, with only health, readiness and OpenAPI paths |
| `POST /mcp` `server/discover` | `200`, with no capability |
| Any direct operation | fixed `400 invalid_request` |

No metrics, administration or activation endpoint is added. The Docker health
check uses health, not readiness, so an intact blocked candidate is healthy but
honestly not ready for service.

## Pinned construction

The Containerfile uses the public multi-architecture Node
`24.19.0-bookworm-slim` index at
`sha256:3638d9a6fe4030bd716be989438248074489337ba3275657f93595428be4fc03`.
The build downloads pnpm `10.33.2`, verifies its independently published SHA-512
before installation, fetches the frozen dependency graph and creates a
production-only `pnpm deploy` tree while dependency networking is still available.
Both package-manager installation commands and the deploy materialiser disable
scripts. A later frozen offline workspace install and compilation replace only the
reviewed workspace outputs in that tree. The runtime stage installs no
operating-system package and runs as numeric `65532:65532`. The runtime removes
build-only tests, declarations and pnpm metadata, together with the unused npm and
Corepack package-manager trees and entry points, after construction.

Construction does not give BuildKit the repository checkout. The packager first
materialises a temporary context containing the exact Git-tracked allowlist plus the
generated OKF projection. The OKF directory must be a closed regular-file set that
matches `CHECKSUMS.sha256`; every materialised file is then checked against the
context inventory before the build starts. `build-context.sha256` binds the path and
bytes of every admitted file.

The dedicated `Containerfile.dockerignore` is a second boundary. It begins with a
deny-all rule, admits only the lock and workspace manifests, required gateway and
transitive packages, schemas, licence and verified OKF output, and ends with explicit
exclusions for `.env` and `.env.*` at every depth. The context inventory independently
rejects those environment-file names. Repository sources excluded by both controls
cannot enter the image accidentally.

The only three network-enabled `RUN` instructions complete before the exact broad
application, package, schema and OKF source-copy inventory: the build verifies and
installs the pinned pnpm tarball, runs the frozen package fetch and materialises the
production deploy tree with scripts disabled. The structural verifier admits those
three instructions only, derives the network-disabled boundary from the first
non-manifest source copy and rejects every later network-enabled build instruction.
After source is copied, the frozen offline install, compilation, reviewed-output
replacement and runtime-stage mutation all execute with BuildKit networking disabled.
The verifier also rejects install, prepare, packing and publication lifecycle hooks
in every admitted root or workspace package manifest. This defence in depth does not
replace or alter pnpm dependency build-policy controls.

BuildKit is fixed to v0.32.2 at
`sha256:28a898719c18a33f4e8000685287fa36fd0dd9560c6440227d3a732d79bb41d8`.
The build receives the source commit time as `SOURCE_DATE_EPOCH`, disables inline
SBOM and provenance variance, and emits one-platform OCI output. The packager
normalises the outer OCI tar ownership, modes, order and timestamps. Two isolated,
no-cache builds must have the same archive bytes and index, manifest, configuration
and layer digests.

The one canonical archive is an OCI layout with a single, strictly derived
Docker-save `manifest.json` compatibility envelope. That envelope references only
the existing OCI configuration and ordered layer blobs plus the fixed local image
tag. It adds no second image, archive or image blob and does not change the OCI
index, manifest, configuration or layer identities. The same canonical archive can
therefore be loaded by classic Docker engines as well as consumed through the OCI
layout on containerd-backed engines; any divergence between the compatibility
envelope and the OCI graph fails verification.

The checked receipt binds:

- repository, source commit, version and source cleanliness;
- complete admitted build-context checksum manifest;
- Node, pnpm and BuildKit identities;
- target platform;
- archive, manifest, configuration and every layer digest; and
- the unchanged zero-capability runtime claims.

One canonical verifier recalculates the source and materialised-context identities,
parses the bounded OCI layout and expanded layers, rejects unreachable blobs, checks
every digest and requires the closed runtime configuration: numeric non-root user,
fixed entry point, one exposed port, fixed environment, health check, stop signal and
zero-capability labels. Docker, Compose, Buildx and scanner versions and phase timings
belong to acceptance evidence outside the reproducible OCI bytes.

A dirty development build can be created only with an explicit checker flag and is
labelled `non-publishable-development-build`. CI and provenance reject it.

## Local Compose controls

`deploy/gateway/compose.candidate.yaml` consumes only an exact image already loaded
locally. It has no build key, uses `pull_policy: never` and passes no operator-supplied
environment, secret or credential into the container. The checker supplies only the
exact image reference for Compose interpolation. The definition applies:

- a loopback-only host-publication declaration;
- a read-only root filesystem and fixed numeric user;
- all capabilities dropped and `no-new-privileges`;
- a small no-execute temporary filesystem;
- bounded CPU, memory, swap, processes and file descriptors;
- one replica and no restart loop;
- one internal bridge with no external egress;
- bounded local JSON logs; and
- two named volumes at `/var/lib/gis-ai-go/ledger` and
  `/var/lib/gis-ai-go/reconciliation`.

The evidence ledger remains a single-writer component. Scaling this service is not
supported. The local bridge can prove that the blocked candidate has no egress; it
cannot supply the domain-aware ONS network policy required by a later active
candidate.

Engine behaviour is recorded rather than inferred. The checker accepts exactly one
of two semantic ingress states: `127.0.0.1:8787`, or no realised host port while the
single inspected bridge remains internal. Classic Docker serialises a suppressed
internal-network binding as an exact `null` value; Docker 28 can omit the unrealised
entry from an empty `NetworkSettings.Ports` object; and containerd-backed Docker
Desktop can serialise it as an empty list. The checker first requires the exact
`Config.ExposedPorts` and loopback `HostConfig.PortBindings`, then normalises only
those three reviewed no-binding forms to an empty semantic `realised` list. Missing
declarations, extra ports, wildcard, IPv6 or otherwise different mappings fail. In
the no-binding state the host port must remain unreachable around
the complete HTTP, Host and MCP matrix on `127.0.0.1:8787` inside the container, and
the same transport is rechecked after restart and exact-image restore. The receipt
records declared and realised mappings separately; this Compose file must not be
described as host-usable unless its receipt records `host-loopback`.

## Assurance commands

The ordinary repository gate validates the source, schema, unit tests, documentation
and workflow contract. The separate image gate requires Docker and public package,
base-image, scanner-image and vulnerability-database downloads:

```bash
pnpm install --frozen-lockfile
uv sync --locked --group dev --cache-dir .uv-cache
pnpm run check
docker buildx create \
  --name gis-ai-go-gateway \
  --driver docker-container \
  --driver-opt image=moby/buildkit:buildx-stable-1@sha256:28a898719c18a33f4e8000685287fa36fd0dd9560c6440227d3a732d79bb41d8 \
  --bootstrap
pnpm run check:gateway-image
```

The builder name is fixed. If that name already exists, inspect it first rather than
replacing it implicitly. The packager fails unless its driver, version, configured
image reference, running container image digest and name all match the reviewed
BuildKit identity. The CI job creates and removes that isolated builder explicitly.

`check:gateway-image` is the single final image-assurance aggregator. It runs every
phase in a private mode-0700 sibling quarantine, writes the evidence manifest last
and invokes the complete verifier with offline vulnerability-scan replay. Only a
complete verified directory is atomically promoted to `artifacts/gateway`; a failed
run removes its owned quarantine and leaves no publishable gateway directory.
Calling selected component scripts is useful for diagnosis but is not the final gate.

Each phase sends binary standard output and standard error to separate concurrent
collectors. They count bytes only to enforce the bound while retaining at most 1 MiB
per stream.
Output is replayed only after the process exits successfully and both streams, plus
their combined projection, are bounded UTF-8 without unsafe controls, private paths
or credential material. Every non-empty replayed stream ends with a fixed punctuation
marker line. That line is reserved: child output containing it is withheld, and a
trusted transcript is classified as separate, boundary-terminated phase frames. Content
therefore cannot combine across streams or phases into a credential or GitHub Actions
command even after line folding.
Otherwise the raw output is withheld and the job emits only fixed phase and stream
status and reason metadata. Rejected output exposes no exact length or content-derived
hash. Non-zero exits, timeouts and start errors likewise expose neither child output
nor command arguments. Their raised errors are fixed and detached from the underlying
process exception. Each phase has an isolated process group;
timeout and completion terminate any surviving descendants before quarantine cleanup
or promotion.

Within container acceptance, uncaptured Compose actions and exact-image save or
removal redirect both output streams to the null device because their output is not
evidence. Structured Compose and Docker queries remain explicitly captured for
validation. This prevents incidental progress or compatibility warnings from
forwarding absolute runner paths into the parent phase transcript.

The image gate performs this fixed sequence:

1. rebuild and verify the OKF identity;
2. materialise and checksum the Git-tracked plus verified-OKF build context;
3. build, package and canonically verify the OCI archive, source receipt and closed
   runtime configuration;
4. perform a second no-cache build and compare exact bytes and content digests;
5. generate a full, unfiltered CycloneDX image SBOM with pinned Syft 1.42.2;
6. scan the SBOM for all High and Critical findings with pinned Trivy 0.74.0, retain
   the checksummed database and report, and prove an offline replay;
7. load the exact OCI archive and start only the local Compose candidate;
8. record declared and realised ingress, then verify health, blocked readiness,
   zero capability, direct and MCP Host filtering, limits, non-root/read-only
   execution and internal-network egress denial over the accepted loopback path;
9. hash both mode-0600 storage descriptors, restart and confirm they are unchanged;
10. verify that a raw request key and machine paths do not enter the bounded logs;
11. stop the exact container, prove its state is exited and that it rejects an exec
    probe, and close a realised host-loopback port when present;
12. save, remove, reload and restart the exact image identity while retaining the
    same volume identities; and
13. require the exact closed evidence directory, validate all closed receipts and
    schemas, bind all 11 subjects in one final manifest and replay the retained scan.

Step 12 is a local restore-mechanism rehearsal, not evidence of a production
rollback. A real rollback must select a previous accepted registry digest and an
authorised runtime without rebuilding either image.

The checker drains each `docker load` stream incrementally as binary data, retains
only a bounded prefix and counts bytes solely to enforce the limit. A failed,
timed-out or malformed load therefore emits only fixed stream status and reason
metadata, with no exact output length or content-derived hash. Secret-shaped values,
private machine paths, invalid UTF-8, unsafe control characters and over-limit output
remain withheld.
This diagnostic path cannot weaken the exact-image check or turn a load failure
into acceptance.

The successful evidence directory contains exactly 12 regular, non-symbolic-link
files: 11 checksum-bound subjects plus their manifest.

```text
build-context.sha256
container-acceptance.json
gateway-image-evidence-manifest.json
gateway-image.oci.tar
gateway-image.oci.tar.sha256
gateway-image.sbom.cdx.json
gateway-image.sbom.cdx.json.sha256
gateway-image.trivy-db.tar.gz
gateway-image.trivy-db.tar.gz.sha256
gateway-image.trivy-report.json
gateway-image.vulnerability-scan.json
image-receipt.json
```

The image receipt, vulnerability scan, container acceptance and evidence manifest
use closed schemas; their canonical JSON and transitive source, image, SBOM, scan,
database, Compose and engine bindings are rechecked. An extra, missing, linked or
non-regular directory entry fails the gate.

CI runs image assurance after ordinary repository assurance. The stable final
`assurance` job succeeds only when both producers succeed. A successful image job
uploads `gateway-image-<commit>`. Failed runs do not upload the candidate, a partial
directory or its quarantine, and cannot reach provenance. GitHub Actions retains
ordinary job logs under the workflow's normal retention policy; those logs are not
evidence artefacts and are not covered by the textual-evidence privacy gate. The
repository `artifacts` parent must be a real directory: a symbolic link or an
owner, permission or identity change is rejected before candidate cleanup,
quarantine creation or
promotion and is rechecked around every trusted producer and verifier. These checks
detect workspace drift; they are not a sandbox against another malicious process
running as the repository owner, which could also alter source and evidence. Each
textual subject is rejected before parsing when it exceeds the 8 MiB privacy bound.
Parsed JSON also has one cumulative 8 MiB UTF-8 budget across all key and string
occurrences, in addition to its depth and node bounds.
On protected-main runs, provenance downloads and re-verifies the complete
directory against the checked-out commit, regenerates the OKF projection, and separately
attests the OCI archive, full image SBOM and evidence
manifest. Pull requests cannot deploy or publish an image.

## SBOM and vulnerability policy

The repository-wide deterministic SBOM records the exact Node base identity. The
separate image SBOM inventories the full realised operating-system and Node
production package set from the OCI archive. Syft output is not component-filtered.
Its source identity, timestamp, serial number and list ordering are normalised against
the image receipt; no component is removed.

The raw Trivy report and closed scan projection retain every reported High and
Critical finding. The policy fails only when any of those findings has a non-empty
fixed version; unfixed findings remain recorded rather than being hidden or
misrepresented as patched. The scanner image is immutable, while the public
vulnerability database is time-varying. The gate therefore packages exactly
`db/metadata.json` and `db/trivy.db` into a canonical gzip archive, records their
individual and archive hashes and sizes, and proves that a network-disabled,
`--skip-db-update --offline-scan` replay produces the same stable report projection
without changing the database.

Both scanner passes run as the invoking host UID and GID so the capability-free
container can write the owner-private mode-0700 cache on native Linux as well as
Docker Desktop. Its private `/tmp` tmpfs has the same numeric owner. The scanner
still has a read-only root filesystem, all capabilities dropped and
`no-new-privileges`; the offline replay additionally retains `--pull=never` and
`--network=none`. The gate does not make either mount group- or world-writable and
does not restore `CAP_DAC_OVERRIDE`.

The retained database, full report, scanner and engine versions, and phase times are
dynamic assurance evidence. A later scan may change without changing the image and
must be treated as newer evidence, not an OCI reproducibility failure.

The protected-main candidate retains three unfixed High findings. Their exact
package status, constrained current exposure and non-accepting release decision are
recorded in the
[QUAL-206 gateway image vulnerability disposition](QUAL-206_IMAGE_VULNERABILITY_DISPOSITION.md).
A passing fixable-only policy is not owner risk acceptance or release readiness;
a patched base rebuilt into new candidate bytes or a separately recorded explicit
owner risk acceptance remains mandatory before release.

## Deployment and rollback blockers

Repository assurance does not resolve these external requirements:

- an authorised no-cost or otherwise approved Node runtime;
- public hostname, TLS ingress and exact Host/Origin allowlists;
- workload identity and non-loopback network policy;
- domain-aware egress limited to the accepted ONS origin and paths;
- persistent-volume backup, restore, disposal, capacity and operator processes;
- a previous accepted gateway image for real rollback;
- live QUAL-206 and all remaining activation gates; and
- any paid service, new provider terms, enterprise credential or registry terms.

If no authorised runtime is available, stop at the verified container artefact. Do
not describe it as deployed, supported, activated or registered. The static
Explorer is outside this Compose project and remains available when the gateway is
stopped or rolled back.
