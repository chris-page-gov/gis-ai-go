# ADR-0019: Network-private GCP pilot with transactional evidence

- status: proposed implementation decision; local implementation authorised,
  cloud mutation and hosted acceptance require the recorded deployment gates
- date: 5 October 2026
- decision owner: Chris Page
- release target: additive private personal pilot and transferable BDUK review
  package; not supported `v0.2.0`

## Context

The owner commissioned a private GCP deployment of the current website, both OKF
pipelines, evidence surfaces and custom Streamable HTTP MCP implementation. The
local working tree is authoritative and existing Sites/public/local releases must
be preserved. The older candidate is deliberately loopback-only and cannot be
made a cloud product by changing its bind address.

The hosted evidence work already separates transport, application semantics and
transactional persistence. Cloud Run instance-local files are ephemeral; neither
single-instance settings nor a bucket-mounted filesystem supplies the required
multi-writer claim, evidence and reconciliation semantics. The initial content is
admitted public metadata and synthetic fixtures, with no external model, live
provider, credential transfer, licensed feature, protected BDUK extract or private
original archive.

## Decision

Build a separately named GCP runtime assembly and a reusable lifecycle entrypoint.
Use ordinary Cloud Run, internal ingress and scoped invocation IAM. Personal
operator access uses an authenticated IAP SSH tunnel to a dedicated VM without an
external IP, then a loopback fixed-target TLS authentication proxy and Private
Google Access. The BDUK profile consumes the platform's approved private network
rather than mandating that personal tunnel.

Keep network reachability, Google transport principal, independently verified
human/client identity and application policy as separate interfaces. Test
role-dependent discovery, direct invocation and equivalent evidence/API/resource
paths. Unknown/missing attributes deny; a claimed role, email suffix or user
purpose does not grant access. An owner transport smoke test is not real Google
human SSO, MCP OAuth interoperability or BDUK Okta acceptance.

Pin admitted OKF/OKF+ releases and serve the actual expanded corpus through current
consumer contracts. Generate an allowlisted build context and immutable image
identity. The separately named pinned Debian-based pilot image does not inherit
the existing UBI candidate image assurance; its build/provenance/scan gates and
actual size/startup/memory evidence remain explicit. Preserve metadata rights, source-native IDs, separate count grains,
source dates, provenance and explicit gaps. Local build preparation performs no
cloud upload and never includes the whole checkout.

Use one GCP-native transactional evidence product: Firestore. Preserve canonical
receipt verification and scoped idempotency/ownership, compare-and-swap writes,
conflicting-fingerprint rejection and loss-of-response reconciliation. Keep
provisioning outside request handlers; do not initialise missing history
implicitly. Transactions/retries cannot repeat provider effects. Existing
filesystem/D1 adapters and evidence families keep their original contracts.
Firestore persistence remains a hosted gate until replacement/concurrency tests
run against the selected deployed instance.

Use explicit private configuration and isolated state for personal and BDUK
profiles. The first cloud mutation requires a costed saved plan binding the exact
account/project/billing, resources, IAM, upload inventory, source/configuration,
image/bundle/policy digests, spend envelope and expiry. Reuse that approval within
scope. Never attach an arbitrary billing account, create enterprise federation,
change organisation policy or adopt paid services to satisfy a local test.

## Alternatives considered

A public IAP-only website does not meet the network-private requirement. Google's
managed BigQuery MCP service does not host this application or its evidence
contracts. Exposing the local candidate changes its accepted threat/identity
boundary. Cloud Storage FUSE does not provide the evidence transaction semantics.
Cloud SQL would add fixed operational/cost overhead for a bounded claim/receipt
model; it remains a separately justified alternative if a future accepted contract
requires relational transactions. Multiple database products are unnecessary.

## Consequences and gates

The pilot gains infrastructure, private connection, OIDC/policy and durable-store
assurance obligations. Runtime/VM bootstrap egress must remain declared and
bounded; no unrestricted NAT is silently added. Firestore transaction/contention,
quota, document size, per-operation charges and retained storage must be measured.
There is no claimed automatic deletion, disaster recovery, independent rollback
anchor or hard spending cap. Budgets normally alert and do not stop expenditure.

The review package can be completed without cloud credentials, and local tests
can establish implementation properties. Actual private network authentication,
human/MCP sign-in, cross-revision persistence, rollback, teardown, costs and BDUK
platform/Okta acceptance remain observed gates. A failed essential gate blocks its
acceptance level while independent authorised work continues.

The supported product stays `v0.1.0`. Existing generic-entrypoint, public hosting,
image assurance, provider, identity, release and Sites acceptance gates remain in
force. This decision does not authorise a public release, enterprise changes or
protected-data hosting.

See [architecture](../deployment/gcp/ARCHITECTURE.md),
[acceptance](../deployment/gcp/ACCEPTANCE.md) and
[cost/teardown](../deployment/gcp/COST_AND_TEARDOWN.md) for implementation mappings
and remaining operational decisions.
