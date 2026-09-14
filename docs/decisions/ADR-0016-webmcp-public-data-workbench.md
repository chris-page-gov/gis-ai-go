# ADR-0016: experimental public-data workbench

- status: accepted experimental boundary; local activation implementation under assurance
- date: 14 September 2026
- decision owner: Chris Page
- work item: [WEB-216 #125](https://github.com/chris-page-gov/gis-ai-go/issues/125)
- release target: experimental local workbench, not supported `v0.2.0`

## Context

The owner authorised OKF-led ONS discovery, bounded MCP retrieval, OS/ONS geography
and a shared person/AI workbench. The [inception](../implementation/WEB-216_PUBLIC_DATA_WORKBENCH.md)
and [source crosswalk](../implementation/WEB-216_SOURCE_AND_STORY_CROSSWALK.md)
define the scope. The metadata foundation is accepted through PR #127; its corpus
does not grant execution authority. The maintained CPIH experiment identifies
L522/MM23 independently of the retired `cpih01` record.

The existing exact-five assembly is intentionally fixed to one weekly-deaths
observation. Its policy, selection, adapter and receipt verification independently
enforce that identity. Replacing a value, changing an integer to a decimal or
labelling the old cache as CPIH would defeat those controls. The existing
[ADR-0013](ADR-0013-webmcp-page-tools-boundary.md) two-tool `/demo` also promises no
MCP retrieval or durable evidence; its names and historical evidence stay intact.

## Local implementation decision

Add a separately named experimental workbench entrypoint and CPIH assembly. Reuse
the reviewed transport and content-addressed evidence mechanisms through narrow
additions, not a caller-configurable plugin registry or a duplicated gateway.
Do not modify the old constructors, local-candidate port, approved outage/cache
behaviour, generic inactive defaults, Pages build or release identities.

The first CPIH execution source is the explicitly admitted, validated public
capture from 14 September 2026. It contains a small, source-hash-bound projection
for January and July 2026. This is **captured data**, not live retrieval; the local
adapter must have no provider egress. No artificial provider outage is introduced
to make it look eligible for the old cache path. The new transformation is
`read-validated-cpih-capture`.

The browser's manual controls and WebMCP callbacks use the same MCP client path:

```text
Find evidence → review exact selection → call MCP → inspect receipt
                                       ↓
                          same visible table and provenance
```

Discovery may present the broader metadata corpus, but executable support is a
separate server-authored allowlist. Only the admitted L522/MM23 capture and its
exact supported periods may execute. A discovery result, supplied URL, concept
edge, client plan hash or caller-written policy cannot add authority. Unsupported
records remain useful discovery results with explicit execution-unavailable text.

Selection returns a non-executable proposal. Query independently checks the closed
resource/profile, selected period, capture identity and public/no-egress policy.
The result retains native `cdid`, `datasetId`, URI, observation string, index unit,
base year, release, observation update, capture time, source-body hashes and
transformation lineage. Do not invent an edition/version to fit another API family.
Source `nextRelease` text is not a validated promise. Local data cannot silently
become “current” as time passes.

## Evidence and authority

Add one separately identified CPIH receipt family with strict structure and
full-material verification. Its mere construction is not proof of persistence.
Integrate it additively with the existing ledger and inspection machinery; old
receipt families must retain byte-for-byte verification semantics. Query success
requires durable persistence and a linked inspectable record. Use an owner-only
local ledger separate from LOCAL-212's deliberately transient session store.
Record retention and filesystem prerequisites before starting the new launcher.

Preserve the existing claim/idempotency and lost-response distinctions. An invalid,
missing or corrupt store prevents data success. Restart must verify the retained
record chain. No private prompts, credentials, arbitrary paths or AI-written
interpretation belong in public receipts. Hashes prove checked content bindings,
not independent source authenticity or attestation.

## Threat and host boundaries

- Use statically authored tool names, descriptions and closed input schemas.
  Source metadata is untrusted evidence, never executable instructions.
- Keep exact Host/Origin, protocol, request size, timeout and cancellation checks.
  Do not use a proxy to disguise an otherwise forbidden browser origin.
- Accept no arbitrary provider URL, credential, file path, tool name or callback.
- Validate schema bounds in executable code as well as advertising them to clients.
- Update the visible page before returning a page-tool result. Preserve a complete
  accessible manual journey and honest unsupported-host state.
- A page action that records or stages state must not claim to be read-only merely
  because the underlying dataset is public. Choose annotations from actual effects.
- Capture-backed execution has no external provider or model request. The user's
  own AI remains the interpretation layer; a model is not embedded in the page.

The local slice does not prove that the published Site can reach a laptop, host
the existing filesystem-backed gateway or reproduce pinned-address transport.
The existing Site and owner-private audience are retained. Hosted MCP requires
separately tested equivalents for persistence, concurrency, ingress and provider
controls. Platform storage or a successful deployment is not itself proof of those
equivalents. No paid commitment or protected-data access is authorised by this ADR.

## Acceptance before activation

1. Closed profile, selection, policy, receipt and result contracts with adversarial
   identity/unit/period/hash/unknown-field tests.
2. Additive ledger/reconciliation integration; corruption, persistence failure,
   restart, duplicate and conflicting-request tests; unchanged old-family results.
3. Real loopback MCP initialise/list/call sequence ending in persisted receipt
   inspection, with zero provider egress. Python parsing or a direct callback is
   not an MCP observation.
4. Manual/WebMCP parity, visible dated provenance, index-not-percentage guidance,
   keyboard/reflow/accessibility, cancellation and unsupported-host checks.
5. Exact-version AI-host observation before claiming that host interoperates.
6. Independent review and canonical PR/protected-main assurance before acceptance;
   later hosting, deployment and rollback evidence before a hosted capability claim.

The separately named local launcher binds exactly `127.0.0.1:8788`, serves its
admitted static assets and three experimental MCP tools, and retains a separate
owner-only evidence store. It has no arguments or provider configuration. The
browser registers four page tools, including local discovery; the supported
five-tool candidate on port 8787 and the old two-tool Site remain unchanged.

The [local walkthrough](../implementation/WEB-216_LOCAL_WORKBENCH_WALKTHROUGH.md)
records real wire and browser observations against the implementation working
tree. These observations do not replace exact-head canonical acceptance, prove
hosted execution or close M4/M5. A successful local activation must not be
described as the supported `v0.2.0` release.

## Hosted-storage experiment

The next inactive foundation uses a separate, bounded transactional snapshot and
D1-compatible compare-and-swap adapter. It does not substitute a database row for
the old filesystem evidence or silently claim equivalent operational guarantees.
The asynchronous application returns a distinct result family and verifies full
source material and chain internally before projecting a selected record.

The [hosted-storage experiment](../implementation/WEB-216_HOSTED_STORAGE_EXPERIMENT.md)
records atomicity, uncertainty, capacity, software-generation and retention limits.
There is no HTTP mount or automatic migration/initialisation in this increment.
Primary binding, freshness, deployment, retention operations and independent
rollback evidence remain assembly/host obligations; local tests do not grant them.
