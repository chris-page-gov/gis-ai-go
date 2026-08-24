Strengthen the blocked UBI gateway release gate with measured merged-rootfs
verification, exact critical runtime and licence bindings, closed final-stage
instructions, direct inventory-bearing Trivy scans of the exact gateway and donor
OCI archives, and deterministic network-disabled retained-database replay. Add a
supplemental digest-pinned Grype 0.117.0/NVD CPE lane for the standalone Node.js
24.19.0 runtime, calibrated against affected 24.18.0 and fixed 24.18.1 controls,
without changing the Node executable or gateway TypeScript sources. The revised
schemas are copied into the image, so this change requires fresh OCI/rootfs bytes and
a fresh assurance run. Hold the exact Grype database through each producing run;
transport only its checksum and rehydrate the database from Anchore for immediate
protected offline replay. Require the protected artefact to be downloaded promptly
to an owner-supplied mode-0700 local directory, rehydrated and verified there; an
external long-term replica remains an operational follow-up.

Make Trivy database acquisition resilient on shared CI runners without weakening
the vulnerability gate: try the three official database locations in a fixed order
with a fresh cache per attempt, retain only a closed successful cache, and map total
registry exhaustion to fixed privacy-safe phase metadata. Scanning and replay remain
digest-pinned, network-disabled and unable to update the retained database.

Make donor-image evidence independent of the Docker daemon's image-store backend.
Export the digest-pinned UBI library donor through the already pinned BuildKit
builder, require its layers and derived configuration to match the exact upstream
manifest and configuration apart from BuildKit's sole deterministic top-level
`created` normalisation, and reconstruct one deterministic closed OCI archive with
the exact source configuration.
Map external acquisition/export failures and donor-integrity validation failures to
distinct fixed privacy-safe phases without replaying registry, temporary-path or
runner details.
