- Strengthen the blocked UBI gateway release gate with merged-rootfs verification,
  exact runtime and licence bindings, direct inventory-bearing Trivy scans and
  network-disabled database replay. Add a digest-pinned Grype 0.117.0 lane for Node.js
  24.19.0, calibrated against affected and fixed controls, and retain its exact
  database for checksum-bound offline replay. Acquire Trivy databases from three
  official locations in a fixed fail-closed order. Derive the UBI donor archive with
  the pinned BuildKit builder and verify it against the upstream manifest independently
  of the Docker image-store backend. Map acquisition and integrity failures to bounded
  privacy-safe phases, and require prompt owner-private preservation of each accepted
  protected-main evidence set.
