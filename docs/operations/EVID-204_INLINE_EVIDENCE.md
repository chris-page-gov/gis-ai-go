# EVID-204 canonical public inline evidence

- status: local candidate; complete locked local gate passing
- work item: [EVID-204](https://github.com/chris-page-gov/gis-ai-go/issues/22)
- decision: [ADR-0010](../decisions/ADR-0010-canonical-public-inline-evidence.md)
- supported public release: [`v0.1.0`](https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0)

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
| Local implementation commit | pending |
| Focused schema and package tests | passing: 19 contracts, 20 evidence, 2 authority, 6 policy and 41 gateway tests |
| Complete locked local gate | passing on the uncommitted candidate working tree |
| Independent evidence-core review | `SHIP`; no P0, P1 or P2 finding |
| Independent whole-diff security and contract review | `SHIP`; no P0, P1 or P2 finding across all 60 candidate files |
| Pull request assurance and CodeQL | pending |
| Protected-main assurance, provenance and attestation | pending |

Pending rows are not capability claims. Update them only from exact retained
evidence after the corresponding gate succeeds.

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
after reviewing all 31 modified and 29 added files. The remaining pending rows are
remote publication evidence, not local implementation gaps.
