Fixed protected-main gateway provenance so the OIDC job attests the immutable original
producer artefact only after a separate clean OCI derivation is byte-identical, the full
evidence replay succeeds, and a dependency-free verifier independently enforces source,
subject and vulnerability-freshness bindings using the privileged runner clock. Both
evidence-verification layers now reject malformed, unexpected or duplicate
security-critical CycloneDX properties before the SBOM can be attested.
