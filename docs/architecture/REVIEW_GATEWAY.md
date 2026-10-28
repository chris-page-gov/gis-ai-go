# Core gateway review

Baseline: `97bc45635a91064cd78f06bf0848ad7636f05439`. Reviewed all 34 core source files (12,324 baseline lines), excluding `sites-pilot*` and `web216*`. A repository-wide scan covered 294 exported names; unmatched exports were not classified as dead code merely for lacking external callers. Consumer searches covered exported declarations, entrypoints, tests and scripts.

## Review findings and refactor boundaries

The review found small confirmed dead fragments, not a removable core subsystem.
The five-tool path, blocked generic launchers, explicit legacy conformance path,
fixture geometry contracts and historical schema exports have different purposes.
Do not infer inactivity from a symbol search alone.

| ID | Finding and confidence | Impact and proposed change | Verification needed |
| --- | --- | --- | --- |
| GW-01 | **Confirmed unused declarations.** `ONS_ADAPTER_VERSION` import, private `publicPolicyOperations(ledger)` parameter, and unused `TestContext`, `DataQueryProblemCode`, `directTrace` test declarations. `Inventory.totalBytes` is returned but never consumed; the local accumulator still enforces the byte cap. | Remove only the unused binding/parameter/returned field. Keep the inventory byte-limit calculation. Reduces misleading dependencies and makes unused-symbol checks usable. Evidence: [import](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/data-query-application.ts#L26-L32), [unused parameter](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/governed-assembly.ts#L315-L321), [inventory type](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/catalogue-snapshot.ts#L46-L50), [accumulator and return](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/catalogue-snapshot.ts#L329-L341), [test imports](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/public-read-transport.test.ts#L1-L40), [unused local](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/public-read-transport.test.ts#L623-L633). | Typecheck with unused diagnostics; preserve inventory oversize test and policy/discovery suites. |
| GW-02 | **Confirmed unreachable conditional arm.** The resource-size check chooses between JSON and SSE by comparing their byte lengths, but SSE is exactly the same JSON plus a fixed ASCII prefix/suffix. | Assert the SSE bound directly and explain why it also bounds JSON; remove two redundant UTF-8 encodings. Evidence: [resource envelope](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-server.ts#L577-L599). | Preserve Unicode/escaped content, long request-ID and resource-size boundary cases in transport suites. |
| GW-03 | **High-confidence duplication/refactor candidate.** Exact-five candidate predicates repeat in activation and container authority; linked query/inspector mount checks repeat in direct and MCP constructors. | Extract pure predicates or a closed typed descriptor, preserving caller-specific authority checks, diagnostic messages, operation order and object-identity checks. Avoid a configurable registry that could expand activation. Evidence: [activation check](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/candidate-activation.ts#L64-L89), [container check](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/container-main.ts#L81-L126), [direct linkage](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/http-app.ts#L335-L400), [MCP linkage](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-server.ts#L816-L887). | Run forged-brand/proxy/accessor, suspension, exact-five discovery and direct/MCP parity tests. |
| GW-04 | **Confirmed repeated work.** Manifest/input path order checks call `toSorted()` inside `some()`, repeatedly sorting the same bounded array. | Sort once or compare adjacent entries while retaining the uniqueness check. This improves worst-case validation cost without widening the inventory. No runtime bottleneck is claimed without measurement. Evidence: [manifest paths](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/catalogue-snapshot.ts#L524-L532), [input paths](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/catalogue-snapshot.ts#L601-L609). | Preserve sorted/unsorted/duplicate and maximum-inventory cases; check identical rejection behaviour. |
| GW-05 | **High-confidence clarity/refactor candidate.** A Node body-read error fabricates a zero-length or oversized body and sometimes changes the method, then re-enters the direct Fetch handler to obtain a problem. | Extract an explicit shared body-failure-to-problem function. The current redispatch obscures precedence among route, media, identity and parsing errors and repeats body work. Evidence: [failure redispatch](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/http-server.ts#L820-L856), [problem mapping](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/http-app.ts#L311-L318). | First characterise current malformed length, oversized body, invalid route/media and GET/HEAD combinations; preserve status, problem body and disconnect semantics. |
| GW-06 | **High-confidence maintainability candidate.** `data-query-application.ts` combines parsing, control validation, provider evidence, cache adaptation, reconciliation and receipt publication; `openapi.ts` combines schema loading/embedding and route/health projection. | Extract bounded internal modules along these responsibilities. Keep the query state transition order visible in one orchestration function, and keep schema `$id`/`$ref` and byte output stable. Evidence: [query orchestration](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/data-query-application.ts#L985-L1275), [schema embedding](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/openapi.ts#L182-L426), [route projection](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/openapi.ts#L689-L850). | Use existing schema equality, receipt fixtures, cancellation, cache-classification and same-key concurrency suites as acceptance gates; do not replace independent verification with shared builders. |

No refactor or deletion is implemented by this documentation change. Inline comments
explain the query recovery/publication ordering, separation of question text from
selection parameters, and the unmounted synthetic execution boundary.

## Reviewed inventory and validation scope

Every core source module below was read. Repository-wide symbol/consumer searches
were used for dead-code candidates; exported versioned schemas and test seams were
retained as such. Tests were indexed across the full core suite, with implementation
and assertions inspected for the cited invariants and findings. This is not a claim
that every test branch was manually proved.

| Source module | Responsibility |
| --- | --- |
| [activation.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/activation.ts#L1-L25) | Frozen empty production activation |
| [bounded-json.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/bounded-json.ts#L1-L223) | Strict bounded UTF-8 JSON parser |
| [candidate-activation.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/candidate-activation.ts#L1-L94) | Fixed exact-five container activation builder |
| [catalogue-application.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/catalogue-application.ts#L1-L1224) | Search, describe, bounds, policy and inline/persisted receipts |
| [catalogue-snapshot.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/catalogue-snapshot.ts#L1-L838) | Filesystem/checksum validation and immutable snapshot brand |
| [container-healthcheck.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/container-healthcheck.ts#L1-L165) | Bounded local container health/readiness probe |
| [container-ingress.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/container-ingress.ts#L1-L73) | One public-origin or loopback authority projection |
| [container-main.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/container-main.ts#L1-L223) | Fixed container paths, stores, startup and shutdown |
| [cursor.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/cursor.ts#L1-L212) | Canonical criteria hashing and cursor codec |
| [data-query-application.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/data-query-application.ts#L1-L1307) | Fixed ONS query, cache admission, controls and reconciliation |
| [evidence-application.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/evidence-application.ts#L1-L426) | Receipt/key lookup, policy and current-call inspection receipt |
| [execution-envelope.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/execution-envelope.ts#L1-L407) | Synthetic gateway/Python request and result contract |
| [governed-assembly.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/governed-assembly.ts#L1-L603) | Composition, brand, capabilities, suspension and readiness |
| [http-app.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/http-app.ts#L1-L808) | Transport-neutral direct HTTP request/response handling |
| [http-main.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/http-main.ts#L1-L31) | Blocked generic loopback launcher |
| [http-server.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/http-server.ts#L1-L957) | Node HTTP ingress, admission, framing, disconnects and transport adaptation |
| [index.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/index.ts#L1-L18) | Public package exports |
| [local-candidate-capability.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/local-candidate-capability.ts#L1-L88) | Private local cache/vintage health registration |
| [local-candidate-main.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/local-candidate-main.ts#L1-L432) | Provider-free local launcher and cleanup |
| [mcp-constants.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-constants.ts#L1-L4) | Side-effect-free protocol and result limits |
| [mcp-http-core.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-http-core.ts#L1-L389) | Shared modern HTTP wire parsing, privacy guards and SDK adaptation |
| [mcp-http.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-http.ts#L1-L67) | Catalogue/governed/CPIH HTTP wrappers |
| [mcp-request-signal.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-request-signal.ts#L1-L53) | Per-request HTTP/SDK abort-signal composition |
| [mcp-server.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-server.ts#L1-L1005) | MCP operation/resource registration and complete result mapping |
| [mcp-stdio-main.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-stdio-main.ts#L1-L42) | Blocked generic STDIO launcher |
| [mcp-stdio.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-stdio.ts#L1-L377) | Bounded modern/explicit legacy STDIO transport |
| [mcp-wire-guards.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/mcp-wire-guards.ts#L1-L65) | Identity and caller-key reflection guards |
| [metadata.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/metadata.ts#L1-L13) | Inactive gateway product metadata |
| [openapi.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/openapi.ts#L1-L850) | Schema embedding, operation projection and readiness contract |
| [problem.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/problem.ts#L1-L309) | Shared catalogue problem/context construction |
| [public-origin.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/public-origin.ts#L1-L52) | Canonical public HTTPS-origin grammar |
| [readiness-integrity.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/readiness-integrity.ts#L1-L225) | Exact evidence-store dispatch verification and branding |
| [reconciliation-applications.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/reconciliation-applications.ts#L1-L37) | Private exact query/inspector-to-index bindings |
| [selection-application.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/src/selection-application.ts#L1-L682) | Closed deterministic selection and evidence |

Core test inventory (including the launcher acceptance and HTTP fixture):

- [candidate-activation.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/candidate-activation.test.ts#L1-L196)
- [catalogue-application.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/catalogue-application.test.ts#L1-L814)
- [catalogue-snapshot.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/catalogue-snapshot.test.ts#L1-L215)
- [container-main.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/container-main.test.ts#L1-L248)
- [cursor.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/cursor.test.ts#L1-L119)
- [data-query-application.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/data-query-application.test.ts#L1-L1821)
- [evidence-application.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/evidence-application.test.ts#L1-L431)
- [evidence-transport.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/evidence-transport.test.ts#L1-L873)
- [execution-envelope.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/execution-envelope.test.ts#L1-L259)
- [fixtures/qual-206-exact-five-http-server.mjs](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/fixtures/qual-206-exact-five-http-server.mjs#L1-L472)
- [governed-assembly.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/governed-assembly.test.ts#L1-L1815)
- [http-app.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/http-app.test.ts#L1-L691)
- [http-server-transport.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/http-server-transport.test.ts#L1-L739)
- [http-server.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/http-server.test.ts#L1-L96)
- [index.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/index.test.ts#L1-L27)
- [local-candidate-acceptance.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/local-candidate-acceptance.test.ts#L1-L733)
- [local-candidate-launcher.acceptance.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/local-candidate-launcher.acceptance.ts#L1-L267)
- [local-candidate-main.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/local-candidate-main.test.ts#L1-L522)
- [mcp-http-core.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/mcp-http-core.test.ts#L1-L196)
- [mcp-stdio.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/mcp-stdio.test.ts#L1-L1321)
- [mcp-transport.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/mcp-transport.test.ts#L1-L1206)
- [public-read-transport.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/public-read-transport.test.ts#L1-L2027)
- [qual-206-exact-five-http.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/qual-206-exact-five-http.test.ts#L1-L1104)
- [qual-206-host-015.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/qual-206-host-015.test.ts#L1-L267)
- [qual-206-local-protocol-matrix.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/qual-206-local-protocol-matrix.test.ts#L1-L355)
- [readiness-integrity.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/readiness-integrity.test.ts#L1-L155)
- [selection-application.test.ts](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/apps/mcp-gateway/test/selection-application.test.ts#L1-L344)

Files named `sites-pilot*` and `web216*` are reviewed in the separate workbench/pilot
chapter. Shared `mcp-http.ts`, `mcp-http-core.ts` and `readiness-integrity.ts` contain
small CPIH integration points; this chapter covers their shared transport/brand
behaviour and defers the CPIH application semantics to that chapter. Other packages,
scripts, schemas and service files are cross-referenced dependencies rather than
files owned by this gateway review.

Validation performed for this chapter:

- Read baseline source/test lines through `git show` and verified every generated
  immutable Git line link against that baseline.
- Ran the compiler with `--noEmit --noUnusedLocals --noUnusedParameters` as a diagnostic.
  It reported GW-01 and unused declarations in other component scopes; those are
  findings rather than failures introduced by comments.
- Standard gateway `tsc --project apps/mcp-gateway/tsconfig.json --noEmit` and
  `git diff --check` passed. Three pre-existing compiled test-file suites (cursor,
  execution envelope and selection application) also passed as supplementary checks;
  they do not replace a source rebuild and the coordinating test run.
- Confirmed the edited TypeScript files differ only by comments. The coordinating
  repository review records standard typecheck, tests and documentation checks.
