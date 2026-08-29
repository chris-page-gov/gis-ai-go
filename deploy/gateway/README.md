# Local unregistered gateway Compose candidate

This local Compose file exercises the repository-only DEPLOY-207 container. It is
not a deployment definition. It mounts only the fixed exact-five candidate and its
three resources, with production registration false, on a loopback-only declaration
over an internal bridge that cannot reach the provider.

The current local image source uses the one reviewed `linux/amd64` composition:
UBI 10 micro as the runtime root, the official Node image as builder and checked
Node.js 24.19.0 donor, and UBI 10 Node.js 24 minimal as donor for the exact versioned
`libstdc++` object and GCC notices. The UBI micro root supplies exact `libgcc_s`.
The image includes the unmodified UBI EULA and all required licence
and source-provenance notices. It is not supported or endorsed by Red Hat. This
replacement is not accepted merely because it is constructed: run the complete
image gate and retain the new receipt, SBOM, scan and Compose evidence before using
it as a release candidate.

The checker supplies `GIS_AI_GO_GATEWAY_IMAGE` as the exact locally loaded image
identity and uses `pull_policy: never`. Do not replace it with a floating tag. The
only declared host socket is `127.0.0.1:8787`; the isolated bridge is internal and
the Compose definition passes no operator-supplied environment, secret or credential
to the container. The image interpolation value is not a container environment
variable. Two named volumes preserve the separately verified ledger and
reconciliation-index descriptors across restart.

Docker engines do not all realise a published port on an internal bridge. Acceptance
therefore records the declared and realised mappings separately. It permits only the
exact loopback mapping or no realised mapping on the verified internal bridge.
Classic Docker can serialise that second state as a `null` port value, Docker 28
can omit the unrealised entry from an empty port inventory, and containerd-backed
Docker Desktop can use an empty list. The checker first verifies the exact exposed
port and loopback host binding, then normalises only those three reviewed engine
forms to zero realised bindings. For that fallback, the host port must remain closed
before and after the full route matrix, which runs over container-local loopback. A
receipt with that fallback is not evidence of a usable host socket.

Run the complete image gate from the repository root:

```bash
docker buildx create \
  --name gis-ai-go-gateway \
  --driver docker-container \
  --driver-opt image=moby/buildkit:buildx-stable-1@sha256:28a898719c18a33f4e8000685287fa36fd0dd9560c6440227d3a732d79bb41d8 \
  --bootstrap
pnpm run check:gateway-image
```

If the fixed builder name already exists, verify it instead of replacing it. The
packager rejects a builder whose driver, version, configured image or realised image
digest differs.

The stable `check:gateway-image` aggregator materialises the checksum-bound source
context, builds and canonically verifies a deterministic OCI archive, creates the
full Syft SBOM and retains the inventory-bearing Trivy scans and database for offline
replay. A supplemental, digest-pinned Grype 0.117.0 lane separately checks the exact
standalone Node.js 24.19.0 component against the retained NVD CPE provider. The same
database and configuration must report the three reviewed High advisories for the
affected 24.18.0 control and no longer report them for the fixed 24.18.1 control.
The lane records only that the retained database has no High or Critical NVD CPE
match for the actual component; it does not claim that Node.js has no
vulnerabilities. The change does not alter the Node executable or gateway TypeScript
sources, but the revised schemas are copied into the image: exact OCI/rootfs bytes
therefore change and require a fresh build. The gate then loads those exact new image
bytes, exercises this Compose file, stops the service, restores the saved image and
confirms that the same volume identities remain readable. It removes its uniquely
named containers, network and volumes afterwards.

Success requires the exact closed 25-file `artifacts/gateway` directory: 24 subjects
plus `gateway-image-evidence-manifest.json`. This includes the actual and calibration
Node inputs and paired Grype JSON and CycloneDX reports, together with the retained
database and checksum. Dynamic engine, tool and database identities and phase
timings remain in that acceptance evidence, outside the reproducible OCI archive.
See the [complete runbook](../../docs/operations/DEPLOY-207_GATEWAY_CONTAINER.md)
for the inventory, offline replay, storage cost and protected-main attestation
boundary.

A local operator can privately retain that complete set. GitHub-hosted producing and
provenance runners form it only transiently: the Actions transport deliberately omits
the compiled Grype database because its provider data has no assumed blanket
redistribution grant. It retains the checksum and all other subjects. Protected
verification must rehydrate the exact checksum-bound archive from Anchore before the
directory is complete and any network-disabled replay starts. No durable private
archive is configured in GitHub Actions, so the transported bundle is not
independently replayable if Anchore later removes the exact URL. The release operator
must therefore download it promptly into an owner-supplied mode-0700 local directory,
run the checksum-bound restore and verify the completed private set. External
long-term replication remains an operational follow-up.

This is a local rollback-mechanism rehearsal only. A production rollback requires a
previous accepted image digest and an authorised runtime. The static Explorer is not
part of this Compose project and remains independent of gateway suspension.
