# Build and image assurance

Observed on 9 October 2026. This is implementation status and a reproducible
build workflow, not a source review, image approval or BDUK acceptance record.
Complete [secure source and image admission](SECURE_TRANSITION.md) before running
any repository command on the secure machine. Perform prerequisite acquisition
and image construction through the separately approved builder.

## Observed results

The development toolchain image built from its seven-file allowlisted context
with offline build steps and maximum BuildKit provenance. An actual offline,
read-only container check passed at UID/GID 1000:1000, with capabilities dropped
and no new privileges. Node 24.19.0, pnpm 10.33.2, Python 3.12.14, uv 0.12.2,
Terraform 1.13.4, Git and Bash were observed. The editor profiles fix both the
container and editor UID; they do not infer it from a host profile name.

These checks establish tool compatibility and the tested container controls.
They do not admit the image. The actual offline Syft/Trivy scans returned:

| Material | SBOM packages | CRITICAL | HIGH | Result |
| --- | ---: | ---: | ---: | --- |
| Development toolchain image | 1,932 Syft / 1,933 SPDX | 36 | 714 | BLOCKED; 11 Trivy Go package entries lack versions, and binary/package coverage is incomplete |
| Earlier GCP application image | 252 Syft / 253 SPDX | 5 | 69 | BLOCKED; binary package coverage is incomplete |
| Original pnpm and uv locks, including development dependencies | 156 npm / 8 Python | 0 | 5 | Original observation also contained six MEDIUM and three LOW advisories |
| Updated pnpm and uv locks, including development dependencies | 155 npm / 8 Python | 0 | 0 | Actual offline recheck returned zero advisory entries at every severity; exact input/database scope only |

Counts are package vulnerability entries, not unique CVEs. No unfixed findings
were ignored. The database was updated at `2026-10-09T13:10:00Z`; its retained
bytes and freshness were checked. Publisher provenance and independent platform
trust remain separate requirements. Original receipts, full SBOMs, raw reports,
private diagnostics and SHA-bound report reassessments remain in private evidence
custody. Missing versions and unassessed package types still block a passing
receipt. Reassessment did not change the original reports or receipts.

The sealed repository source scan identified three MEDIUM approval-integrity,
package-membership and received-archive resource-budget findings, with partial
semantic coverage. Its full-repository scope does not mean every document, test
or dependency implementation received complete semantic review. The
[sanitised review and supplemental remediation record](../security/GCP-223-SECURITY-REVIEW.md)
retains the original evidence hashes and separate fix observations. The fixed
lifecycle's focused regression suite passed 70 checks and the archive suite
passed 39. Supplemental static review found no additional concrete bypass in the
lifecycle, packaging or dependency changes. Its archive metadata-retention
finding was corrected with bounded PAX state and removal of processed parser
cache entries; the parent rechecked the reproduced trigger and valid controls.
These are focused local remediation results; the sealed audit remains unchanged.
The aggregate local GCP checks passed as described below. The final published
commit requires its own exact source review; the initial scan registration was
the earlier installer commit. Execution, packaging
and deployment on the secure machine remain blocked until the findings, coverage
and exact-image/platform gates are resolved.

The updated lock scan used the retained schema-2 database and includes development
dependencies. Its actual Trivy JSON has SHA-256
`43ad316ca4896a799b5270698ca252989b94fcd89de08f22db4889d113c1c711`;
the 16-input manifest has SHA-256
`098841b7b1407e093ddf2b7578443dfaf098ffda05f36f74c7e710349bb836bd`.
This result supersedes the lock observation for those inputs, not the original
image assessments. Fresh child images, complete package/binary coverage and
trusted signature/provenance/database checks are still required.

The original development OCI identities are:

```text
archive SHA-256: e5279c15e5ea6ffecb9e191ac481a7347fb425c4af2feae9641210f07a23bf1a
root index: sha256:6f4eb1e6a0ccd7df460c8d6bdf00dd4a2bcb19fbd0a1418e4a0a80e8c772b836
runtime manifest: sha256:7c81bac8215b7d0d02d4c391fccdb821b13ef695d44df230586123adadb09f55
config: sha256:07ca462d9c2de2552ac7f24fca824429b3b0aa565a66765240d5039d9d93f7f5
```

The earlier GCP image root manifest is
`sha256:3ef00620adfc26290444eec5fd7d7c60abbf1274c79c28b4e90615a99a188a4f`.
It is historical image evidence; later lifecycle/source changes require fresh
preparation and approval. Neither image was published to a registry or deployed.

## Explicit build commands

On the approved builder, use already admitted tooling bytes and a fresh output
directory. Acquisition requires the explicit `--download` option, approved
network/mirror and CA route; the default stages from the existing cache only.

```sh
./scripts/environment/environment.sh prepare-image \
  --cache "$GIS_AI_GO_TOOL_CACHE" --output "$GIS_AI_GO_BUILD_DIR/context"
./scripts/environment/environment.sh build-image \
  --context "$GIS_AI_GO_BUILD_DIR/context" \
  --output "$GIS_AI_GO_BUILD_DIR/toolchain.oci.tar" \
  --builder "$GIS_AI_GO_BUILDX_BUILDER"
```

The named variables are task-specific paths/identities supplied by the approved
host. Do not replace `$HOME` or inject a developer's personal profile path.
The image context includes no repository application, credentials, proxy CA,
private configuration, original archives or protected data. The supplied bases
are digest-pinned official Node/Python images; this image is not a Docker
Hardened Image. See [vendor options](CONTAINER_IMAGES.md) before selecting an
approved replacement. Changing a base or adding tooling requires child-image
assurance and compatibility checks.

BuildKit provenance is retained, but its presence does not verify a trusted
builder or signature. The classic Docker image store cannot directly load the
tested maximum-provenance OCI index. A separately exported Docker archive was
used for the local tool check and matched the same runtime config digest; it
does not replace the original OCI/provenance evidence or bind a registry image.

## Offline image scan

Use the installed, digest-pinned Syft 1.42.2 and Trivy 0.74.0 images recorded in
`scripts/security/image_assurance.py`, a closed fresh Trivy schema-2 database
cache, and a fresh private output directory outside the mounted checkout.
The command acquires nothing, opens no external network and grants no approval.

```sh
python3 scripts/security/image_assurance.py \
  --archive "$GIS_AI_GO_BUILD_DIR/toolchain.oci.tar" \
  --manifest-digest "$GIS_AI_GO_OCI_ROOT_DIGEST" \
  --db-cache "$GIS_AI_GO_TRIVY_CACHE" \
  --output-dir "$GIS_AI_GO_REVIEW_DIR/image-assurance"
```

The helper validates the complete original OCI closure and layer diff IDs. It
builds a private OCI directory containing only the already validated runtime
manifest/config/layers so both tools can read it. The original archive/root,
selected child and derived file inventory remain bound in the evidence. Inline
descriptor bytes must match their declared size/hash and archived blob; external
descriptor URLs are refused. Attestations are retained as unverified evidence.

Each scanner uses a preloaded exact digest with `--pull=never`, no network,
read-only root, non-root UID, no capabilities or new privileges, two CPUs,
6 GiB memory with no swap, 256 processes and a 4 GiB temporary filesystem.
Run scans sequentially and provide space for retained private image/database
snapshots and reports. Sanitised stderr is retained privately with a 1 MiB cap.
The helper returns exit 2 and `BLOCKED` for missing/stale tools or database,
invalid or incomplete inventory, identity mismatches, or HIGH/CRITICAL findings.
It never treats an empty, failed or incomplete report as a clean scan.

Retain exact source/image inventories, complete dependency and licence closure,
fresh scan results, trusted signatures/provenance and actual platform decisions.
Approved mirrors must preserve the exact image and its verification evidence.
Do not disable TLS, add a Docker socket to the editor, allow automatic installs,
or substitute a mutable tag to make a blocked build or admission pass.

## Checks and cleanup

Local affected checks passed: 23 environment tests, 44 image-assurance tests,
all workspace TypeScript checks, shell/Python syntax,
source privacy, documentation links, preserved research hashes and changelog
validation. Mock scanner tests are separate from the actual image scans above.
The fixed lifecycle passed 70 focused checks. The subsequent `pnpm run test:gcp`
suite passed 26 runtime, 111 Python deployment and seven packaging/UI checks;
the 70 lifecycle checks are included in that deployment total. The aggregate
private log has SHA-256
`6c28508660926565c4f002c0ee0f793bc5d2556ac2ff23f063d860a9f390b9ef`.
After the dependency update, workspace type checks, 18 dependency-pin/historical
matrix checks, `pnpm run test:public-data-workbench` (52 passes) and
`pnpm run test:typescript` (639 passes) passed; one provider check was skipped
because its credential prerequisite was absent. The ordinary launcher lifecycle
passed. Its dirty-source LOCAL-214 exact-source demo/archive acceptance reported
`NOT_RUN` and remains outstanding.
`pnpm run test:interoperability` then passed 76 checks with 14 skips, followed by
seven non-live, unscored receipt checks. They establish local protocol/evidence
behaviour, not hosted-client or live-provider acceptance.
The full local `pnpm run check` reached 1,249 Python checks and failed three
gates with seven skips: native observer fixtures, a stale deterministic receipt
binding and strict collector runtime-identity uniqueness. The binding is now
corrected and its 33 owning checks pass. Copy-only offline dependency imports
and all 23 environment checks pass, but collector uniqueness still refuses;
native assertions remain intact. The canonical Chrome binary is absent.
Canonical CI is still required; hosted authentication, persistence and all
41 GCP acceptance requirements remain unproved. No secure-machine execution,
cloud mutation, protected-data upload, model call or live-provider call occurred.

The actual container checks used `--rm`, leaving no running development container.
Stop/remove only the named development container when finished. Keep private
evidence under approved retention; remove only explicitly owned disposable
contexts, caches or image IDs. Do not use global Docker pruning, Git resets or
checkout cleaning. Cloud rollback/destroy still require the separately approved
destructive plan in the GCP runbook; this increment created no cloud resources.
