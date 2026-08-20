# EVID-204 canonical public inline evidence

- status: accepted on protected `main`; operations remain inactive
- work item: [EVID-204](https://github.com/chris-page-gov/gis-ai-go/issues/22)
- decision: [ADR-0010](../decisions/ADR-0010-canonical-public-inline-evidence.md)
- supported public release: [`v0.1.0`][release]

## Outcome boundary

This slice adds canonical, verifiable evidence to the two inactive in-process
catalogue operations. It does not activate a route or MCP tool and it does not
publish a service.

The server constructs one anonymous-open authority context. A checked-in compiled
JSON policy denies by default and allows only `catalogue.search` and
`catalogue.describe` over the bounded public metadata catalogue. The policy is not
OPA and the authority context is not a user, organisation, credential or workload
identity.

Each successful application result carries an inline evidence receipt that binds
the normalised parameters, exact catalogue publication, result core, gateway
software, trace identifiers, public policy decision and record-specific licence
evidence. The receipt says `inline-only`, `not-persisted` and `not-attested`.

## Deliberate exclusions

This slice provides no:

- event stream, append-only ledger, persistence or evidence lookup;
- signature, attester, identity provider, OPA service or protected entitlement;
- provider or execution receipt, provider call or geometry processing;
- MCP listener, catalogue HTTP route, advertised tool or active API operation;
- receipt freshness or expiry validation, a nonce or one-time replay prevention;
  an otherwise valid receipt remains valid when presented again with the exact
  independently supplied material; or
- public deployment beyond the unchanged static `v0.1.0` Explorer.

Readiness remains blocked until transport conformance and interoperability are
implemented and reviewed. Persistence, corruption recovery and `evidence.inspect`
remain open acceptance work under EVID-204.

The later inactive durable-ledger candidate is documented separately in
[`EVID-204_DURABLE_LEDGER.md`](EVID-204_DURABLE_LEDGER.md). It preserves this
accepted inline receipt as the issue-time record and adds a separate storage event
and reference only after persistence succeeds.

## Verification contract

The candidate must pass all of the following before a pull request is opened:

1. schema fixtures validate against the closed authority, policy, decision,
   receipt and catalogue-result contracts;
2. RFC 8785 canonicalisation tests cover ordering, number and Unicode controls,
   unsupported values and adversarial structures;
3. domain-separated content identities are deterministic and reject mutation,
   truncation, replay across domains and wrong independently supplied material;
4. the compiled policy proves default deny, exact operation allow-listing and the
   public/open/non-personal/non-protected boundary;
5. catalogue application tests prove every success has a valid receipt and no
   receiptless exported result path remains;
6. receipts omit raw queries, cursors, caller identity, credentials, prompts,
   machine paths and evidence URIs; and
7. the complete locked repository assurance gate and independent security review
   pass with the immutable research tree unchanged.

## Evidence state

| Evidence | State |
| --- | --- |
| Local implementation commit | `9d4b3148a23925a91e5e44c3fba7b966bae958c5` |
| Focused package tests | passing: 19/20/2/6/41 |
| Complete locked local gate | passing on the exact candidate bytes before commit |
| Independent evidence-core review | `SHIP`; no P0, P1 or P2 finding |
| Whole-diff reviews | `SHIP`; 60/60 files; no P0–P2 finding |
| Pull-request assurance and CodeQL | passing on [pull request 29][pr29] |
| Main assurance, provenance and attestation | passing: `af9043955470568c146397d1a25dd8813eb7aa55` |

These passing rows accept only this bounded inactive slice. They do not claim a
listener, route, advertised tool, public service or durable evidence store.

The complete gate also passed 94 repository Python tests, 2 execution-boundary
tests, 16 Explorer build-policy tests, 42 Explorer unit and component tests and 27
real-browser tests. It validated 11 manifests and locks, 15 schemas and 55 records,
308 local links, 183 immutable research hashes, 2 ledgers and 71 source identifiers,
scanned 508 text files, rendered 9 diagrams and generated a 149-component SBOM. Two
clean locked builds produced byte-identical Pages archive SHA-256
`f6adb7998c26bef62a651ec825e3a4426d955af4a09167b264dfa221d0ef28b0`; this
slice does not change or deploy that static product.

The final independent integration review found no material evidence error. The
final security diff review sealed exact snapshot
`codex-security-snapshot/v1:sha256:f0233f6a5d8a4d5b3d31f17ea9b9f65effdf3998f3d5acc833d87da147525f90`
after reviewing all 31 modified and 29 added files. The protected pull-request and
main evidence is recorded below.

The candidate commit passed assurance in
[run 32357195428](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32357195428)
and CodeQL in
[run 32357192770](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32357192770).
It then squash-merged through
[pull request 29](https://github.com/chris-page-gov/gis-ai-go/pull/29) as protected-main
commit `af9043955470568c146397d1a25dd8813eb7aa55`.

Protected-main assurance and provenance passed in
[run 32357424957](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32357424957),
and all three CodeQL analyses passed in
[run 32357427549](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32357427549)
with no open code-scanning alert. The retained Pages-source artefact
`9402226353` has GitHub transport digest
`sha256:bb5b30081d43ed30afb271aaa860a89e8dd1c91d67afe5e713a66904b33cbebd`.
Independent archive verification passed for SHA-256
`5253b24944e2579791bcb22f42fa6792fa5a27e34e6b36f29ffde0162b509362`,
payload root `8d15da326f7a0fb4abfadbc3629166bb741050e24ae17044243673b599b3d7a8`
and OKF content root
`99f3d0419aba2a1a6f18fd05f0c3f87123d6d8f2db4520ca3d0f9d6df45f5bd7`.
Strict `gh attestation verify` passed with the exact repository, signer workflow,
source ref, source commit and GitHub-hosted-runner requirement;
[attestation 41836254](https://github.com/chris-page-gov/gis-ai-go/attestations/41836254)
contains SLSA provenance for run 32357424957 attempt 1 and that archive digest.

[pr29]: https://github.com/chris-page-gov/gis-ai-go/pull/29
[release]: https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0
