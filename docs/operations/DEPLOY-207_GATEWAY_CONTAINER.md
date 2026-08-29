# DEPLOY-207 local unregistered gateway container

Status: accepted exact-five repository-only candidate on protected `main`. The fixed
UBI 10 replacement passed complete clean-source repository and image assurance, and
the closed container activation merged through
[pull request 98](https://github.com/chris-page-gov/gis-ai-go/pull/98) as runtime
commit `f253605ab26628e821d4ebc3809cf13c883d57ed`. The QUAL-206 protected-main
ancestry repair merged through
[pull request 99](https://github.com/chris-page-gov/gis-ai-go/pull/99) at
`c7eca721b084356dace8f264d7531b2180093b2d`. The candidate is not published,
registered or deployed.

This runbook covers the image, local Compose and assurance slice that can proceed
without selecting a public runtime. It does not activate GIS AI GO for production, contact ONS,
publish an image, create an HTTPS endpoint, register an MCP service or change the
supported `v0.1.0` release.

## Protected-main acceptance

At exact protected-main commit `c7eca721b084356dace8f264d7531b2180093b2d`,
[CI run 33237523106](https://github.com/chris-page-gov/gis-ai-go/actions/runs/33237523106)
passed repository assurance, the producer image, independent clean OCI derivation,
exact byte comparison, aggregate assurance, provenance and attestation verification.
[CodeQL run 33237523042](https://github.com/chris-page-gov/gis-ai-go/actions/runs/33237523042)
passed Actions, JavaScript/TypeScript and Python. This completes the first
DEPLOY-207 candidate criterion only; it makes no public-host, live-provider,
deployment, rollback or release claim.

The repository-only container foundation merged through
[pull request 48](https://github.com/chris-page-gov/gis-ai-go/pull/48). The later
QUAL-206 preflight changed admitted provider and assurance source, then merged
through [pull request 49](https://github.com/chris-page-gov/gis-ai-go/pull/49) as
protected-main commit `f0e3ccc1dceeba6b3f7d0ecd56c5dd083dee405a`.
[Run 32567301935](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32567301935)
rebuilt and verified the exact image for that source, two-build identity, full SBOM,
retained vulnerability evidence, Compose boundary, storage restart, suspension and
exact-image restore. The canonical OCI archive has SHA-256
`1c6976c1242782d13b14fd826c64fec28b81513b1258f6359a6cce3f9dfb397a` and image
manifest digest
`sha256:c191f23ef6ceb16c324992075592a91a2171cc9b8b7f668fd153de5d0b549690`.
Strict attestations bind the
[OCI archive](https://github.com/chris-page-gov/gis-ai-go/attestations/42310989),
[full image SBOM](https://github.com/chris-page-gov/gis-ai-go/attestations/42310990)
and [closed evidence manifest](https://github.com/chris-page-gov/gis-ai-go/attestations/42310993)
to that exact source. This acceptance publishes no image or service and changes no
activation state.

The PR #48 and PR #49 identities immediately above describe the earlier Debian
Bookworm runtime and must not be reused for UBI. The later UBI identities recorded
at the start of this section are the accepted protected-main evidence. The historical
clean-source identities below remain separate; every later source-changing candidate
still requires fresh pull-request, protected-main and attestation evidence.

## Fixed UBI replacement candidate

The local replacement is deliberately one fixed `linux/amd64` composition, not a
general base-image profile. Its realised root is the exact UBI 10 micro image at
`registry.access.redhat.com/ubi10-micro@sha256:422bd02268e317995a8fbb9c81c0835aa99798a234b5619c52350843d5ed5c4d`.
The official Node image remains the build environment and supplies the checked
Node.js 24.19.0 executable and complete bundled Node licence. The exact UBI 10
Node.js 24 minimal image at
`registry.access.redhat.com/ubi10/nodejs-24-minimal@sha256:e0e44d118dfba1c90e8adbdc751d6db2a1c5f9b0856d31d577054f8ea5216e2d`
supplies only the checked versioned `libstdc++` object and GCC runtime licence
notices. UBI micro supplies the checked `libgcc_s` object and link; the final stage
creates the checked `libstdc++.so.6` link without network access. A scratch final
stage prevents donor product, vendor, maintainer and default-command metadata from
being inherited.

The verifier reconstructs the merged root filesystem in layer order before it
accepts a receipt or SBOM. It applies ordinary and opaque-directory whiteouts,
rejects duplicate paths and descendants below a file or link, and measures every
remaining entry's type, mode, owner, modification time, size, target and content
hash. It preserves hard-link inode semantics in header order, reanchors surviving
link groups deterministically and rejects impossible link metadata. Every parent
must be an explicit directory before its child is applied. Fixed path and component
bounds and one batched removal pass per layer bound verification work. Sparse files
and unmeasured PAX, ACL, extended-attribute or capability metadata are rejected;
only effective `path` and `linkpath` PAX fields are admitted. The receipt and SBOM
bind the complete measured inventory hash. They also bind and recheck the exact Node
executable, GCC runtime objects and links, repository and upstream licences,
notices, non-login home and persistent-storage directories. The three reviewed
licence directories are closed against extra files. The complete inventory hash,
together with byte-identical second-build comparison and the pinned hash of the
whole normalised final-stage Containerfile instruction sequence, is the control for
changed or additional non-critical files. A second `RUN`, `COPY` or `ADD`, or an
extra shell operation inside the reviewed `RUN`, therefore fails before packaging.

The repository owner accepted the applicable UBI terms for this fixed route on
24 August 2026. Every derived image includes the unmodified UBI EULA at
`/usr/share/licenses/gis-ai-go/RED_HAT_UBI_EULA.pdf`, the repository licence,
`THIRD_PARTY.md`, the complete Node notice and the GCC runtime notices. Its labels
state that Red Hat does not support or endorse the image. Exact corresponding Red
Hat source-container references, upstream Node source and archive identity, copied
file hashes and redistribution duties are recorded in
[`THIRD_PARTY.md`](../../THIRD_PARTY.md) and the closed image receipt. This records
the accepted boundary; it is not legal advice and does not accept changed inputs or
later terms.

### Clean-source local assurance identity

The complete repository and image gates passed from clean source commit
`f8d3210064a2fc88f85722d373f935b355c8d289` on 24 August 2026. Two isolated
no-cache builds produced byte-identical OCI archives. That local evidence records:

- image manifest
  `sha256:17b882a53f233d776985187c84d9b5724ad16d9c8c78e832c5cdeef81ecc4c88`;
- OCI archive SHA-256
  `4868d00038f7766cf41a5a71377156ee369c5e6cd6acea423a17546be7887c2d`;
- 488-component full image SBOM SHA-256
  `44d56247bfcc18a7966d3bff74fbde32cebcf3084d100c800943d34f1fb38b3e`;
- zero Trivy image findings and calibrated standalone Node results against retained
  Grype database SHA-256
  `20a7315860b2d07231103a73bedec01de31e7a7f3d590aedfc61709dc9e117f9`;
- successful network-disabled replay; and
- closed evidence-manifest SHA-256
  `10c8f3b1dbd05cf59b543cacb0fd31ca811507f25b20c0a4fb7b0148dac335b5`,
  after Compose runtime, persistence, suspension and exact-image restore passed.

The 488-component SBOM contains 23 installed Red Hat runtime RPMs, 3 signing-key
RPM metadata components and 13 Node package components discovered in the final
image. A separately bound RPM/library component identifies the copied
`libstdc++` as Red Hat version `14.3.1-4.4.el10` with its exact package URL,
donor image identity and final-file hash. The exact Node and `libgcc_s` file
components are part of the 446 measured file components; the remaining components
are the gateway application and operating system. The SBOM contains no `gzip`,
`util-linux`, `libblkid` or `libmount` RPM component. The full 25-file evidence set,
including the retained Grype database, remains owner-local with private permissions;
the 24-file CI transport subset excludes that database. These identities are not a
registry artefact, protected attestation or release candidate. Every later source
commit must create and verify its own exact OCI/rootfs bytes, including both scanner
lanes, before its identity can be recorded.

## Exact boundary

The image has one fixed entry point. It binds `0.0.0.0:8787` inside the container so
the local bridge can reach it. Compose declares only `127.0.0.1:8787` for host
publication. Startup:

1. rejects command-line arguments;
2. reasserts that generic production activation and metadata remain blocked;
3. verifies the fixed `/app/artifacts/okf` bundle;
4. opens and fully verifies the fixed, disjoint ledger and reconciliation roots;
5. byte- and semantic-verifies the sole fixed approved T04 cache record;
6. passes only those four already verified inputs to a closed builder, which creates
   the fixed active ONS adapter and mounts the exact ordered five operations plus
   their three MCP resources; and
7. emits only a bounded lifecycle event, the unregistered state and catalogue revision.

The exact assembly is local and unregistered. It has no path, environment,
command-line, serialised configuration or arbitrary loader seam, and its production
registration value is always false.

The container HTTP surface is deliberately:

| Route | Expected result |
| --- | --- |
| `GET /healthz` | `200`, unregistered lifecycle and exact catalogue identity |
| `GET /readyz` | `200`, exact ordered five and production registration false; `503 reconciliation-capacity-exhausted` only when no new immutable claim can be admitted |
| `GET /openapi.json` | `200`, the same exact five direct operation paths |
| `POST /mcp` discovery | exact five tools and three matching resources |
| `POST /catalogue/search` | local catalogue result and durable evidence |

No metrics, administration or activation endpoint is added. The Docker health
check verifies health plus either exact ready state or the capacity-exhausted state
that preserves recovery access. Acceptance
does not call `data.query` and therefore makes no provider request.

## Pinned construction

The builder uses the public multi-architecture Node `24.19.0-bookworm-slim` index
at `sha256:3638d9a6fe4030bd716be989438248074489337ba3275657f93595428be4fc03`,
but the only admitted target is `linux/amd64` and the receipt binds that platform.
The build downloads pnpm `10.33.2`, verifies its independently published SHA-512
before installation, fetches the frozen dependency graph and creates a
production-only `pnpm deploy` tree while dependency networking is still available.
Both package-manager installation commands and the deploy materialiser disable
scripts. A later frozen offline workspace install and compilation replace only the
reviewed workspace outputs in that tree. Before the broad source copy, the builder
also retrieves the exact official UBI EULA with redirects disabled and rejects a
changed status, size or SHA-256. The runtime installs no operating-system package
and runs as numeric `65532:65532`. Its scratch composition carries the UBI micro
root, only the checked Node and UBI-donor library objects, the production dependency
tree, application outputs and required notices. Build-only tests, declarations and
pnpm metadata, together with the unused npm and Corepack package-manager trees and
entry points, do not enter the final image.

Construction does not give BuildKit the repository checkout. The packager first
materialises a temporary context containing the exact Git-tracked allowlist, the one
approved ONS cache record and the generated OKF projection. The OKF directory must be a closed regular-file set that
matches `CHECKSUMS.sha256`; every materialised file is then checked against the
context inventory before the build starts. `build-context.sha256` binds the path and
bytes of every admitted file.

The dedicated `Containerfile.dockerignore` is a second boundary. It begins with a
deny-all rule, admits only the lock and workspace manifests, required gateway and
transitive packages, schemas, licence and verified OKF output, and ends with explicit
exclusions for `.env` and `.env.*` at every depth. The context inventory independently
rejects those environment-file names. Repository sources excluded by both controls
cannot enter the image accidentally.

The only four network-enabled `RUN` instructions complete before the exact broad
application, package, schema and OKF source-copy inventory: the build verifies and
installs the pinned pnpm tarball, runs the frozen package fetch, materialises the
production deploy tree with scripts disabled and retrieves the hash- and
size-checked UBI EULA. The structural verifier admits those four instructions only,
including the exact EULA URL and integrity values, derives the network-disabled
boundary from the first
non-manifest source copy and rejects every later network-enabled build instruction.
After source is copied, the frozen offline install, compilation, reviewed-output
replacement and runtime-stage mutation all execute with BuildKit networking disabled.
The verifier also rejects install, prepare, packing and publication lifecycle hooks
in every admitted root or workspace package manifest. This defence in depth does not
replace or alter pnpm dependency build-policy controls.

BuildKit is fixed to v0.32.2 at
`sha256:28a898719c18a33f4e8000685287fa36fd0dd9560c6440227d3a732d79bb41d8`.
The build receives the source commit time as `SOURCE_DATE_EPOCH`, disables inline
SBOM and provenance variance, and emits fixed `linux/amd64` OCI output. The packager
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
- fixed UBI micro runtime and source-container identities;
- fixed UBI Node.js donor and source-container identities;
- upstream and copied Node identities, realised library paths, link targets and
  hashes, exact base or donor providers, EULA and notice identities, and the explicit
  no-support boundary;
- target `linux/amd64` platform;
- archive, manifest, configuration and every layer digest; and
- the exact-five unregistered runtime claims and the sole approved cache bytes.

One canonical verifier recalculates the source and materialised-context identities,
parses the bounded OCI layout and expanded layers, rejects unreachable blobs, checks
every digest and requires the closed runtime configuration: numeric non-root user,
fixed entry point, one exposed port, fixed environment, health check, stop signal and
exact-five unregistered labels. Docker, Compose, Buildx and scanner versions and phase timings
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
supported. The local bridge can prove that the unregistered candidate has no egress; it
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
6. scan the exact gateway OCI archive directly for all High and Critical findings
   with pinned Trivy 0.74.0 and `--list-all-pkgs`; require the direct report to
   cover the exact 23 installed runtime RPMs, 3 signing-key RPM metadata records
   and 13 Node packages in the SBOM; independently export the exact pinned donor
   through the pinned BuildKit builder, reconstruct and retain its source OCI graph,
   and scan it so the copied `libstdc++` RPM is covered; then retain the checksummed
   database and both reports and replay both scans with no network;
   separately use digest-pinned Grype 0.117.0 and one retained NVD CPE database to
   scan the exact Node.js 24.19.0 component and the 24.18.0 affected and 24.18.1
   fixed controls, retaining each input and paired JSON and CycloneDX report before
   replaying the complete lane with no network;
7. load the exact OCI archive and start only the local Compose candidate;
8. record declared and realised ingress, then verify health, exact-five readiness,
   three resources, one successful `catalogue.search`, direct and MCP Host filtering,
   limits, non-root/read-only execution and internal-network egress denial over the
   accepted loopback path;
9. hash both mode-0600 storage descriptors, restart and confirm they are unchanged;
10. verify that a raw request key and machine paths do not enter the bounded logs;
11. stop the exact container, prove its state is exited and that it rejects an exec
    probe, and close a realised host-loopback port when present;
12. save, remove, reload and restart the exact image identity while retaining the
    same volume identities; and
13. require the exact closed evidence directory, validate all closed receipts and
    schemas, bind all 24 subjects in one final manifest and replay every retained
    Trivy and Grype scan.

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

The successful private producing directory contains exactly 25 regular,
non-symbolic-link files: 24 checksum-bound subjects plus their manifest.

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
gateway-node.grype-db.tar.zst
gateway-node.grype-db.tar.zst.sha256
gateway-node.actual.input.cdx.json
gateway-node.actual.grype.json
gateway-node.actual.grype.cdx.json
gateway-node.affected.input.cdx.json
gateway-node.affected.grype.json
gateway-node.affected.grype.cdx.json
gateway-node.fixed.input.cdx.json
gateway-node.fixed.grype.json
gateway-node.fixed.grype.cdx.json
gateway-image.vulnerability-scan.json
gateway-runtime-library-donor.oci.tar
gateway-runtime-library-donor.trivy-report.json
image-receipt.json
```

The image receipt, vulnerability scan, container acceptance and evidence manifest
use closed schemas; their canonical JSON and transitive source, image, SBOM, scan,
database, Compose and engine bindings are rechecked. An extra, missing, linked or
non-regular directory entry fails the gate.

CI runs primary image assurance after ordinary repository assurance. The stable final
`assurance` job succeeds only when those ordinary repository and primary gateway-image
producers succeed. Protected-main provenance additionally requires the independent
derivation and verification jobs described below. A successful primary image job
uploads `gateway-image-<commit>-without-grype-db`: the checksum-bound Grype database
archive is deliberately excluded, while its checksum and every other subject are
transported. Failed runs do not upload the candidate, a partial directory or its
quarantine, and cannot reach provenance. GitHub Actions retains
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
Protected-main runs add two unprivileged trust domains before provenance. An
independent image job checks out the exact clean commit, regenerates the OKF
projection and produces a separate canonical OCI derivation without receiving any
producer artefact. Its fresh, isolated runner uses the same contract-fixed BuildKit
builder name and pinned image as the producer runner; independence comes from the
runner, checkout and artefact boundary, not from an alternative unchecked builder
identity. A separate verification job downloads the producer and independent
artefacts by their immutable current-run artefact IDs, regenerates the OKF projection,
acquires and digest-checks the pinned scanners, and rehydrates the exact Grype database
archive from Anchore using its retained URL, length and SHA-256. It then re-verifies
the complete producer directory against the checked-out commit, requires a current
Node advisory, verifies the independent receipt and requires the two OCI archives and
their checksums to be byte-identical. Neither job has an OIDC token or attestation
permission.

The OIDC provenance job remains dependent on that full replay but does not accept a
re-upload from it. It downloads the exact original producer artefact and independent
derivation by their current-run artefact IDs. One standard-library-only verifier
requires the known closed producer transport inventory, rechecks the manifest-bound
OCI, SBOM and vulnerability receipt, compares the OCI bytes and checksums again, and
uses the privileged runner clock to enforce the assessment, database and NVD provider
freshness windows. It also requires the exact gateway SBOM property-name inventory,
rejects malformed or duplicate properties, uses the producer's exact canonical JSON
encoding and binds the source and image identities. Only then does the job separately
attest the original OCI archive, full image SBOM and evidence manifest. It installs no
project dependency and runs no Docker or scanner command.

All GitHub-hosted jobs are ephemeral. No authorised durable database destination is
configured in GitHub Actions, so the transported artefact is evidence of immediate
checksum-rehydrated verification, not a self-contained long-term offline replay
bundle. If Anchore stops serving the exact URL, later replay from the 90-day artefact
fails closed. The required handoff is therefore to download the protected artefact
promptly into an owner-supplied mode-0700 local directory, rehydrate the exact database
there and verify the completed private set. External long-term replication remains an
operational follow-up. Pull requests cannot deploy or publish an image.

Use an owner-chosen path outside the repository; do not put that private path in a
public receipt, log or document. After the protected workflow succeeds:

```bash
export GIS_AI_GO_PRIVATE_EVIDENCE_DIR=/owner/chosen/private/path
export GIS_AI_GO_RUN_ID="PROTECTED_WORKFLOW_RUN_ID"
export GIS_AI_GO_COMMIT="40_CHARACTER_PROTECTED_MAIN_COMMIT"
install -d -m 0700 "$GIS_AI_GO_PRIVATE_EVIDENCE_DIR"
gh run download "$GIS_AI_GO_RUN_ID" \
  --name "gateway-image-$GIS_AI_GO_COMMIT-without-grype-db" \
  --dir "$GIS_AI_GO_PRIVATE_EVIDENCE_DIR"
uv run --locked --cache-dir .uv-cache python scripts/node_runtime_advisory.py \
  restore-database \
  --scan "$GIS_AI_GO_PRIVATE_EVIDENCE_DIR/gateway-image.vulnerability-scan.json" \
  --output-dir "$GIS_AI_GO_PRIVATE_EVIDENCE_DIR"
uv run --locked --cache-dir .uv-cache python scripts/verify_gateway_image_evidence.py \
  --directory "$GIS_AI_GO_PRIVATE_EVIDENCE_DIR" \
  --expected-source-commit "$GIS_AI_GO_COMMIT" \
  --require-clean
```

The restore is networked and accepts only the exact Anchore origin, path, length and
SHA-256 retained in the receipt. The final verifier imports those local bytes and
replays the three Node roles with `--pull=never` and `--network=none`. Preserve the
completed directory locally until the owner names its private long-term destination.

## SBOM and vulnerability policy

The repository-wide deterministic SBOM records the exact Node builder, UBI micro
runtime and UBI Node.js library-donor identities. The separate image SBOM inventories
the full realised operating-system and Node production package set from the OCI
archive. Because Syft cannot infer a package relationship for individual objects
copied across stages, the generator adds receipt-derived file components for the
Node executable, base-provided `libgcc_s` and donor-provided `libstdc++`. Their
hashes, licences, providers and source references are closed values, and the verifier
reconstructs and compares those components exactly. The top-level image component
also binds the receipt hash, both UBI source-container identities, the EULA hash and
the no-support boundary. Existing
Syft components are not filtered or replaced. Source identity, timestamp, serial
number and list ordering are normalised against the image receipt.

The raw Trivy report and closed scan projection retain every reported High and
Critical finding. The policy fails only when any of those findings has a non-empty
fixed version; unfixed findings remain recorded rather than being hidden or
misrepresented as patched. The scanner image is immutable, while the public
vulnerability database is time-varying. Database acquisition uses the pinned
scanner in a capability-free, read-only container and tries three allowlisted
official locations in order: the Google pull-through mirror, GitHub Container
Registry and AWS Public ECR. Each attempt starts with a separate empty cache; only
a successful cache with the closed two-file inventory is retained. A 270-second
in-container timeout leaves a 30-second margin inside the host subprocess bound.
Exhausting all three locations fails the phase with fixed metadata and no registry
response, credential or runner path in the public log. The gate then packages exactly
`db/metadata.json` and `db/trivy.db` into a canonical gzip archive, records their
individual and archive hashes and sizes, and proves that a network-disabled,
`--skip-db-update --offline-scan` replay produces the same stable report projection
without changing the database.

The retained donor archive does not depend on whether the host Docker daemon uses
the classic or containerd image store. The gate uses the already verified, pinned
BuildKit builder to export a base-only `linux/amd64` OCI graph with provenance and
SBOM generation disabled. The Buildx client uses the pinned BuildKit builder to read
the immutable upstream manifest and configuration; their digests must match the
donor reference, and every exported layer plus the BuildKit-derived configuration
must match that source graph before a canonical archive is written. The sole
permitted intermediate configuration difference is BuildKit's deterministic
normalisation of top-level `created` to the final source history timestamp; the
canonical archive restores the exact source configuration. An external
metadata or export failure emits only
`failure_stage=runtime-library-donor-acquisition`; a digest, graph or canonical
archive failure emits only `failure_stage=runtime-library-donor-validation`.
Registry responses, commands, temporary paths and runner paths are not replayed.

Trivy's operating-system and language-package inventories do not provide advisory
coverage for the standalone Node executable recorded as `pkg:generic/node@24.19.0`.
The supplemental lane closes that specific gap without changing the Node executable
or gateway TypeScript sources. The assurance schemas are nevertheless copied into
the image, so the OCI/rootfs bytes change and need a fresh build. The lane uses the
exact `linux/amd64` image for
[Grype 0.117.0](https://github.com/anchore/grype/releases/tag/v0.117.0), pinned by
digest, and stock CPE matching against the NVD provider in one retained Grype
database. The actual single-component input is reconstructed from the image receipt,
full SBOM and measured root filesystem; its package URL, Node.js CPE, executable hash
and upstream archive identity must agree, and a second Node identity or executable
fails the gate.

The same scanner, configuration and database must produce the expected High matches
for Node.js 24.18.0 and must not produce them for 24.18.1. Those controls exercise
`CVE-2026-56846`, `CVE-2026-56848` and `CVE-2026-58043`, which the
[official Node.js July 2026 advisory](https://nodejs.org/en/blog/vulnerability/july-2026-security-releases)
identifies as High issues fixed by the 24.18.1 security release. The retained actual
JSON and CycloneDX reports must still contain the exact 24.19.0 component, have no
ignored match and have no High or Critical NVD CPE match. That is the complete claim:
it is not a claim that Node.js has no vulnerabilities, and it does not extend to a
provider, ecosystem or database that is absent from the retained evidence.

The closed configuration also forbids VEX documents, CPE synthesis, package/path
exclusions and Node-relevant ignore rules. Each role binds the SHA-256 of its full
normalised match semantics, including severity, fix state and versions, searched and
found CPEs, matcher and version constraint; offline replay must reproduce that hash.
The NVD provider capture time must be no later than the database build, the build no
later than assessment, and the provider capture no more than three days old at the
original assessment.

Grype downloads its public database once, validates the archive checksum and
provider inventory, and retains the database archive, checksum, three exact inputs
and six raw reports. Verification imports that same archive and replays all six
format scans with `--pull=never` and `--network=none`; changed, stale, non-NVD,
swapped or synthesised-CPE evidence fails. Anchore documents both the
[database lifecycle](https://oss.anchore.com/docs/guides/vulnerability/database/)
and [local database import](https://oss.anchore.com/docs/reference/grype/cli/).
The downloader uses only the fixed public request headers `Accept:
application/zstd` and `User-Agent: gis-ai-go/0.1 vulnerability-evidence`, disables
ambient proxies and rejects redirects before checking the exact origin, media type,
length and SHA-256. Grype reports `from: manual import` after a local import; the
normaliser accepts only that exact marker and binds it back to the separately
retained Anchore URL, checksum, schema and build time. It does not reinterpret the
marker as independent network provenance.

Grype can materialise two imports of the same checksum-bound archive as physically
different but logically equivalent SQLite files. Cross-import verification therefore
requires the exact closed file paths and byte sizes, the same validated archive and
database status, and byte-equivalent normalised scan results. It still compares the
full imported-file SHA-256 inventory immediately before and after each assessment,
so any mutation within a scan fails closed; physical hashes from separate imports
are retained as evidence but are not treated as a stable database identity.

The database acquired on 24 August 2026 is 146,543,041 bytes compressed and expands
to about 2.08 GB. A later evidence run may acquire different bytes and must record
its own size, hash, schema and build time. The archive is dynamic private assurance
evidence, not part of the OCI image, uploaded Actions artefact or a release asset.
The producing and protected-verification jobs each need temporary space for the
expanded database and reports, and protected verification downloads about 147 MB
again to rehydrate the checksum-bound archive. Anchore states that it publishes the
collated database at no cost, but runner, private storage and transfer costs still
apply. [Grype's Apache-2.0 software licence](https://github.com/anchore/grype/blob/v0.117.0/LICENSE)
is not treated as a licence for the compiled provider datasets. The NVD provider
remains subject to the
[NVD terms of use](https://nvd.nist.gov/developers/terms-of-use), including its
requested source and non-endorsement notice. This assurance-only material is not
added to the runtime's bundled third-party notice; keeping it in this runbook avoids
changing that separate runtime file merely to describe external scanner evidence.

Both Trivy passes run as the invoking host UID and GID so the capability-free
container can write the owner-private mode-0700 cache on native Linux as well as
Docker Desktop. Its private `/tmp` tmpfs has the same numeric owner. The scanner
still has a read-only root filesystem, all capabilities dropped and
`no-new-privileges`; the offline replay additionally retains `--pull=never` and
`--network=none`. The gate does not make either mount group- or world-writable and
does not restore `CAP_DAC_OVERRIDE`. The Grype scans use the same non-root,
read-only, capability-free container boundary; only initial database acquisition is
network-enabled.

The retained database, full report, scanner and engine versions, and phase times are
dynamic assurance evidence. A later scan may change without changing the image and
must be treated as newer evidence, not an OCI reproducibility failure.

The historical protected-main Debian candidate retains three unfixed High findings.
The fixed UBI composition removes those exact Debian package instances from the
candidate topology by replacement, not by suppressing evidence. The earlier local
Trivy gate establishes the 26-RPM realised topology and records zero High or Critical
Trivy findings for those local bytes. The current gate additionally requires the
narrow, calibrated Node NVD CPE result described above. Neither result supersedes
protected-main evidence or establishes release readiness until clean-source and
protected assurance reproduce it. The historical status and replacement exit
criteria are recorded in the
[QUAL-206 gateway image vulnerability disposition](QUAL-206_IMAGE_VULNERABILITY_DISPOSITION.md).
A passing fixable-only policy is not owner risk acceptance or release readiness.

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
