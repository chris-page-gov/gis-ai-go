Fixed protected-main gateway provenance so the OIDC job attests the immutable original
producer artefact only after a separate clean OCI derivation is byte-identical, the full
evidence replay succeeds, and a dependency-free verifier independently enforces source,
subject and vulnerability-freshness bindings using the privileged runner clock. Both
evidence-verification layers now reject malformed, unexpected or duplicate
security-critical CycloneDX properties before the SBOM can be attested. The privileged
verifier also uses the producer's byte-identical escaped-Unicode JSON encoding so a
valid realised SBOM reaches that check instead of failing closed on serialisation drift.
The offline Grype verifier now recognises that separate imports of one checksum-bound
archive can have different physical SQLite layouts: it compares their closed path and
size shape while preserving exact archive, status, result and within-assessment hash
mutation checks.
