### Added

- A digest-pinned, non-root blocked gateway OCI image and offline Compose harness,
  with materialised checksum-bound source, script-disabled dependency
  materialisation before the closed source-copy boundary, post-source network
  isolation, canonical OCI/source/runtime verification, repeat-build identity, a
  full image SBOM, retained replayable vulnerability evidence, private durable
  volumes, suspension, exact-image restore and one closed evidence manifest for
  protected-main attestation. Its one canonical OCI archive includes a strictly
  derived Docker-save `manifest.json` compatibility envelope that references the
  existing configuration, layers and fixed tag without changing OCI blob or image
  identity, so classic Docker and containerd-backed engines consume the same image
  rather than separate archives. Failed `docker load` operations stream binary
  output through bounded fixed-status diagnostics that disclose neither an exact
  length nor a content-derived hash. Generated textual evidence uses
  one bounded private-path and credential-material gate, and the final bundle is
  built in an owner-private quarantine that is atomically promoted only after
  complete verification; the repository artefact parent must be a stable real
  owner-controlled, non-writable directory with identity and permissions rechecked
  around each trusted phase, each textual subject has an 8 MiB fail-closed privacy
  bound, parsed JSON shares that bound cumulatively, and reserved
  boundary-terminated phase frames prevent separately safe child streams from
  composing in logs. Uncaptured Compose actions and exact-image save or removal
  discard unused process output without buffering. Failed runs upload no partial
  candidate bytes. Compose acceptance also validates the exact exposed port and
  loopback binding and treats only Docker's reviewed omitted, `null` or empty-list
  internal-network states as zero realised host bindings, with bounded host-closed
  probes around the container-local route matrix. No service, provider or production
  rollback is activated or deployed.
