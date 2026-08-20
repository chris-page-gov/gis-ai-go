# ADR-0010: Canonical public inline evidence

- status: accepted
- date: 20 August 2026
- decision owner: Chris Page
- work item: [EVID-204](https://github.com/chris-page-gov/gis-ai-go/issues/22)

## Context

The inactive gateway can verify the public catalogue and execute deterministic
search and description in process, but it cannot yet return an honest policy
decision or evidence receipt. The preserved research contracts are permissive
candidates designed for protected identity, provider execution and a future
evidence store. Reusing them for anonymous public catalogue access would imply
identity, persistence and attestation that do not exist.

The first evidence slice must close the catalogue application path without
activating a route or tool and without creating a temporary in-memory map that is
described as an append-only ledger.

## Decision

GIS AI GO will use RFC 8785 JSON Canonicalisation Scheme (JCS) for the bounded JSON
values covered by public evidence. The implementation will reject values outside
the interoperable JSON model, including non-finite numbers, sparse arrays, cycles,
non-plain objects, accessors and unpaired Unicode surrogates. Content identities use
SHA-256 with a product, contract-version and purpose domain separator.

The catalogue application will construct one anonymous-open authority context on
the server. It carries no person, organisation, credential, device, client role or
caller-supplied authority. A checked-in compiled JSON policy will:

- deny by default;
- allow only `catalogue.search` and `catalogue.describe`;
- require public, open, read-only, non-personal and non-protected inputs; and
- return controlled obligations for inline evidence, record licences, described
  resource licences, attribution, non-persistence and non-attestation.

This is a compiled public document evaluated in process. It is not OPA, Rego,
authentication, entitlement or an enterprise policy decision point.

Every successful in-process catalogue result must take one path: validate and
normalise the request, select bounded public records, construct authority, evaluate
policy, construct the receipt-free result core, build and verify its inline receipt,
validate the complete result and then return it. Receiptless result builders must
not remain public bypasses.

The receipt will bind:

- request, trace and governed operation identifiers;
- a digest of normalised semantic parameters, never raw query or cursor text;
- the exact catalogue identity, revision and content root;
- deterministic transformation and gateway software identity;
- the receipt-free result digest, media type and returned-record count;
- sorted record-specific record licence, described-resource licence and attribution
  evidence; and
- the embedded authority context and policy decision.

It will state `inline-only`, `not-persisted` and `not-attested`. It will contain no
receipt URI, attester, signature, caller identity, prompt, geometry, machine path or
unnecessary raw request value.

After this slice, readiness remains blocked and the active tool and API-operation
arrays remain empty. The block reason moves from missing policy/evidence to missing
transport and interoperability verification.

## Consequences

- Equivalent bounded inputs and result cores have stable, testable content
  identities.
- Policy, authority, catalogue, result and licence mutations fail receipt
  verification rather than producing a weaker claim.
- The application cannot return a success result without inline public evidence.
- Timestamps remain injectable so tests are deterministic and one server time can
  be used for each receipt.
- The verifier checks that `created_at` is a timestamp but does not compare it with
  a clock. Receipts have no expiry, nonce or one-time replay prevention, so an
  otherwise valid receipt remains valid when presented again with the same
  independently supplied material.
- The receipt proves structural and content binding only; it is not a signature,
  computation attestation or durable audit record.

## Deferred work

This decision does not implement canonical events, event sequencing, append-only
storage, hash chains, restart verification, corruption recovery, `evidence.inspect`,
receipt freshness or expiry checks, nonce or replay state, provider or execution
receipts, full cross-service trace propagation, MCP/API routes, service publication
or registry entry. Those need their own reviewed contracts and operational evidence.

## Threat boundary

This slice directly reduces the policy-bypass, provenance-spoofing and receipt-
tampering paths represented by research risks RK08, RK20 and RK21. It reduces RK25
query-history exposure by retaining only a digest of normalised parameters. RK21
deletion and mutable-overwrite risks remain open until a real append-only store is
implemented and verified.
