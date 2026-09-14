# WEB-216: captured CPIH contracts

This increment implements an **inactive experimental application**, not an
activated MCP server, a WebMCP host observation, a Site deployment or supported
`v0.2.0`. [ADR-0016](../decisions/ADR-0016-webmcp-public-data-workbench.md) keeps it
separate from the existing five-tool weekly-deaths candidate and two-tool WebMCP
demonstrator. The [maintained-source experiment](WEB-216_ONS_RETRIEVAL_EXPERIMENT.md)
establishes the admitted public capture; this component performs no provider call.

## What the contracts mean

| Contract | What it establishes | What it cannot establish |
| --- | --- | --- |
| Selection plan | An exact proposed L522/MM23 month, capture and index measure | Execution permission, live data or a provider grant |
| Compile-time query scope | Only January or July 2026 from the pinned public capture, one observation, no egress | General CPIH, Census, Nomis, OS or arbitrary-URL access |
| CPIH receipt v1 | Exact parameters, result, source declarations, software and operation time | Durable storage or independent attestation by itself |
| Public evidence record v3 | Verified ingest, immutable record/event linkage and retention | A different meaning for the unchanged inline receipt |
| CPIH reconciliation index | One key bound to one capture/month and its durable outcome | Permission to reclaim an incomplete operation automatically |

The result preserves the native `L522`, `MM23`, URI, decimal observation string,
dates and unit. January is `139.4` and July is `142.7`: **index values with 2015 =
100, not percentage inflation rates**. The complete two-month projection is
verified against its independently pinned canonical hash. Original response-body
hashes remain source declarations: this application does not re-verify bodies
that are absent from its input. The provider's next-release text is explicitly
unvalidated. A later query time does not make the historical capture current.

## Execution and retry order

1. Validate the closed proposal and recheck the genuine linked stores.
2. Validate the pinned material, software, time and bounded correlation inputs.
3. For a new key, require available ledger capacity before acquiring the claim.
4. Acquire the immutable claim and independently verify the exact receipt material.
5. Publish the resolution, persist the receipt's record/event, then re-read the
   completed linkage before returning success.

A repeat completed key returns its original receipt and result, including its
original software identity. A changed month conflicts. A resolution whose record
was never committed remains pending, including after restart; it is not reported
as success or silently executed again. Corruption blocks execution and inspection.
A full store blocks new claims but allows existing completed results to be read.
The new inspector reads the original stored operation; it does **not** manufacture
a receipt for the inspection itself or claim the legacy inspection contract.

The schema constants are public and inspectable in source. Reading a constant or
constructing a receipt is not evidence that the application was executed. The
transport must accept only the branded application; options, plans, metadata and
caller-written policy cannot substitute another implementation.

## Separation and tests

The new index is a frozen, separately branded capability, not an instance accepted
by the legacy query/inspection application. Existing receipt families and their
content identities remain unchanged. Both the legacy inspection application and
its policy explicitly reject a genuinely persisted CPIH-family record.

The focused tests cover both months, source substitution and rehashing, unknown
fields, unit/period errors, immutable storage, restart, replay/conflict, incomplete
publication, corrupt files, private permissions, capacity and lost-write failure.
Application tests cover closed options, copied/foreign stores, cancelled admission,
non-authorising selection and capacity-aware retry. Existing evidence golden
identities, legacy inspection and readiness tests remain independent regressions.

No launcher, route, provider, model, browser host, supported operation list or
release gate is activated by these component exports. The next acceptance step is
an actual MCP wire journey followed by the shared manual/WebMCP page, not another
claim based solely on direct function tests.
