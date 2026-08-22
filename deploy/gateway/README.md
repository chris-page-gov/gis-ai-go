# Blocked gateway Compose candidate

This local Compose file exercises the repository-only DEPLOY-207 container. It is
not a deployment definition and it cannot activate a tool, direct operation,
resource, application or provider.

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
full Syft SBOM, retains every High and Critical Trivy finding and a reproducible
database bundle for offline replay, then loads those exact image bytes. It exercises
this Compose file, stops the service, restores the saved image and confirms that the
same volume identities remain readable. It removes its uniquely named containers,
network and volumes afterwards.

Success requires the exact closed 12-file `artifacts/gateway` directory: 11 subjects
plus `gateway-image-evidence-manifest.json`. Dynamic engine and tool versions and
phase timings remain in that acceptance evidence, outside the reproducible OCI
archive. See the [complete runbook](../../docs/operations/DEPLOY-207_GATEWAY_CONTAINER.md)
for the inventory and protected-main attestation boundary.

This is a local rollback-mechanism rehearsal only. A production rollback requires a
previous accepted image digest and an authorised runtime. The static Explorer is not
part of this Compose project and remains independent of gateway suspension.
