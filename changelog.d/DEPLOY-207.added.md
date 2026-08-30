- Add a digest-pinned, non-root blocked gateway OCI image and offline Compose harness
  with checksum-bound source, network-isolated materialisation, repeat-build identity,
  a complete SBOM, replayable vulnerability evidence, private volumes, suspension,
  exact-image restoration and a closed attestation manifest. One canonical archive
  supports Docker and containerd without changing image identity; bounded diagnostics,
  private evidence quarantine and host-closed probes prevent partial or sensitive
  output from being promoted. Use a fixed `linux/amd64` UBI 10 composition with the
  checked Node.js 24.19.0 executable, exact runtime libraries, complete licence notices
  and explicit Red Hat no-support boundary. No service, provider or production
  rollback is activated or deployed.
