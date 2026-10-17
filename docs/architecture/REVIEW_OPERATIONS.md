# Operations review findings

Reviewed baseline: `97bc45635a91064cd78f06bf0848ad7636f05439`.
Owned document: `docs/architecture/BUILD_AND_OPERATIONS.md`.
All findings are maintenance/refactoring findings, not demonstrated vulnerabilities.
No implementation logic was changed or deleted.

## OP-01 — P3: remove four private helpers with no callers

**Confidence:** high for no callers within the tracked repository; external undocumented imports cannot be excluded by static analysis.

**Evidence:** Python AST name/attribute/import traversal over scripts and tests, then whole-repository exact-name searches. At the reviewed commit each helper occurs only at its definition:

- [`_mode`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/capture_delivery_evidence.py#L597-L598).
- [`_codex_text_contains_hidden_json_key`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/capture_delivery_evidence.py#L3737-L3739).
- [`_codex_text_contains_sensitive_key_fragment`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/capture_delivery_evidence.py#L3763-L3765).
- [`_strip_leading_jsonc_comments`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/gateway_image.py#L1847-L1850).

The two Codex wrappers project one half of the retained shared classifier result; current consumers use the shared classifier directly. [`_classify_codex_text_key_fragments`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/capture_delivery_evidence.py#L3705-L3734) and [`_leading_jsonc_comments`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/gateway_image.py#L1821-L1844) are live and must remain.

**Impact:** small but concrete dead surface inside already large, sensitive parsing modules; misleading entrypoints make later changes harder to assess.

**Proposed change:** remove exactly the four helpers in a dedicated cleanup; retain live classifiers and historical formats. Re-run the existing delivery-preservation/key-quarantine and gateway image contract/privacy mutation suites. No new tests are needed solely to prove deleted functions are absent.

**Reproduce:** `git grep -n -w -e _mode -e _codex_text_contains_hidden_json_key -e _codex_text_contains_sensitive_key_fragment -e _strip_leading_jsonc_comments 97bc45635a91064cd78f06bf0848ad7636f05439 -- scripts tests apps packages services`.

## OP-02 — P2: split the gateway-image helper module by responsibility

**Confidence:** high; direct structural and boundary inspection, not merely file size.

**Evidence:** `gateway_image.py` is 6,155 lines. Diagnostic privacy decoding/parsing occupies roughly [665–3031](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/gateway_image.py#L665-L3031), BuildKit process management [3175–3547](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/gateway_image.py#L3175-L3547), context/pin admission [3669–4323](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/gateway_image.py#L3669-L4323), and OCI/root-filesystem inspection begins at [4334](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/gateway_image.py#L4334-L4660). Consumers such as [`gateway_evidence.py`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/gateway_evidence.py#L10-L19) import both privacy and I/O helpers from the image constructor's module.

**Impact:** changing diagnostic syntax requires understanding a module that also constructs and verifies release images; test setup and imports inherit unrelated build concerns. The module's “shared deterministic construction and verification helpers” description understates the privacy parser subsystem.

**Proposed change:** extract cohesive internal modules for diagnostic privacy policy, bounded filesystem/JSON reads, build execution, build context/pins and OCI inspection; retain a compatibility facade during migration. Document dependency direction and keep the independent provenance verifier's byte comparison and freshness decisions independent. Do not deduplicate the producer and independent verifier into one derivation.

**Validation:** existing gateway-image contract, assurance, container diagnostics, OCI compatibility, node-advisory and provenance suites; compare canonical image/archive/evidence fixtures before and after; exact-image CI remains required before release.

## OP-03 — P2: give private capture/storage/projection code explicit internal boundaries

**Confidence:** high.

**Evidence:** `capture_delivery_evidence.py` is 7,873 lines combining filesystem ownership checks, secret scanning, journal transactions, Codex projection/thread closure, and GitHub acquisition. The writer alone spans [2159–3202](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/capture_delivery_evidence.py#L2159-L3202); Codex projection and closure span [3526–6516](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/capture_delivery_evidence.py#L3526-L6516); GitHub transport/acquisition spans [6519–7704](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/capture_delivery_evidence.py#L6519-L7704). The 4,376-line offline verifier imports numerous underscored helpers from capture [28–77](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_delivery_evidence.py#L28-L77); the recovery index likewise imports storage internals [30–45](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/index_recovered_delivery_evidence.py#L30-L45).

**Impact:** the producer, verifier and index rely on an implicit internal API. Private helper changes can affect multiple commands, and the one CLI module mixes network acquisition with offline semantics and crash recovery.

**Proposed change:** extract bounded store I/O/transaction primitives, public internal format constants, pure projection logic and source-specific acquisition modules. Keep the CLI thin. Explicitly distinguish shared low-level format primitives from independent semantic verification, preserving versioned legacy projections and fixed-point redaction checks.

**Validation:** existing preservation tests for transaction crashes [547–642](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_delivery_evidence_preservation.py#L547-L642), current/historical projection compatibility, serial/parallel verification equivalence, key quarantine and recovered-index tests. Use synthetic private stores, never production captures, for refactoring regression fixtures.

## OP-04 — P2: break contract validation into named contract-family checks

**Confidence:** high.

**Evidence:** [`validate_contracts.main`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/validate_contracts.py#L207-L1163) is 957 lines mixing fixture construction, schema registration, historical qualification manifests and negative selection mutations. Schema catalogue validation is separate [182–194](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/validate_contracts.py#L182-L194), but every family's execution remains interleaved in a single entrypoint.

**Impact:** adding a contract requires tracing mutable local fixture variables and global count accumulation through one large function; ownership and which examples cover which contracts are difficult to see.

**Proposed change:** split the existing checks into pure, named family functions returning labelled counts; retain central closed schema-catalogue validation and aggregate output. Keep deep-copied negative mutations and distinguish shape-only example validation from semantic cryptographic verification. Do not introduce reflection-based auto-discovery that silently misses a family.

**Validation:** `validate:contracts` must validate the same schemas/records and reject the same ten forbidden selection mutations; retain dedicated contract tests. A schema-valid synthetic digest must still not be treated as a verified receipt.

## OP-05 — P3: remove five AST-unused imports after export review

**Confidence:** high for unused within their modules; removal should confirm no intentional module re-export.

**Evidence:** top-level Python import aliases absent from every `ast.Name` use in the same module:

- `Iterable`, [`capture_delivery_evidence.py:38`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/capture_delivery_evidence.py#L38-L38).
- `BOUNDARIES`, [`index_recovered_delivery_evidence.py:30–45`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/index_recovered_delivery_evidence.py#L30-L45).
- `tempfile`, [`package_gateway_oci.py:9`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/package_gateway_oci.py#L9-L9).
- `LEDGER_SCHEMA`, [`verify_delivery_evidence.py:38`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_delivery_evidence.py#L38-L38).
- `json`, [`verify_qual_206_claude_exact_five_capability.py:10`](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/verify_qual_206_claude_exact_five_capability.py#L10-L10).

**Impact:** minor dependency noise; no demonstrated behavioural failure.

**Proposed change / validation:** remove in a low-risk import cleanup after whole-repository consumer checks; use existing affected tests and static import-use checks. Do not add tests that merely mirror imports.

## Intentional structures retained

- Producer/independent image derivation and offline provenance comparison are deliberate assurance boundaries.
- Legacy and versioned QUAL scripts are referenced by historical evidence, compiler inputs and tests; age or a newer lane does not establish dead code.
- `infra/` holds explicit placeholders, not abandoned executable provisioning code.
- Operational assertion flags record an operator's assertion, not a process observation. Documentation/comments now make this explicit.
- Local/public/hosted editions and product/private evidence have distinct acceptance gates; no such gate was relaxed in this review.
