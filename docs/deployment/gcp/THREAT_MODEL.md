# Private GCP pilot threat model

Scope: current website, original OKF and expanded OKF+ surfaces, captured-data
workbench, custom HTTP MCP, fixed-target access proxy, lifecycle scripts, build
context and Firestore evidence. Initial data is admitted public metadata and
synthetic fixtures. No secure BDUK, licensed features, private original archives,
external model or live provider is admitted.

Protected assets are release integrity, private network reachability, transport
credentials, verified human claims, principal-scoped evidence/idempotency,
spending authority and unrelated repository/cloud state. Provider prose, source
records, returned URLs, uploaded handover material and client arguments remain
untrusted data. They cannot change destinations, permissions or task authority.

## Trust boundaries and abuse paths

| Abuse path | Control | Required evidence or residual limit |
| --- | --- | --- |
| Reach app through public `run.app` route using a valid invoker credential | Internal ingress, approved VPC route and invocation IAM | Test valid-token public origin, unauthorised source/project and permitted inside route; a generic 403 is insufficient. |
| Expose VM/proxy to internet or LAN | No external VM IP; IAP-only TCP 22; loopback proxy and local forwarding | Read effective VM/firewall/listener state, test tunnel closure. |
| Convert proxy into SSRF/token vending | Fixed canonical Run upstream, TLS verification, bounded requests, injected invocation headers | Host/path/header/destination negative tests; no arbitrary URL or token-return endpoint. |
| Spoof human email/group/role using headers | Independent signed token verification and rejection of forged identity headers | Invalid issuer/audience/signature/expiry and forged-header tests. Transport SA is not human SSO. |
| Invoke hidden tool directly or use alternate API/export | One deny-by-default policy across discovery/invocation/resources/exports | Role matrix, direct hidden-call denial, cursor/cache/ownership checks. |
| Escalate through missing attributes or user purpose | Fixed environment/classification, exact issuer/subject/group mapping | Missing/unknown attributes deny. BDUK domain suffix is not entitlement. |
| Read another principal's evidence or replay their key | Principal/operation-scoped keys, receipt ownership and policy | Two-principal tests, same/conflicting-key concurrency and direct lookup denial. |
| Duplicate/corrupt evidence after retries, crash or lost response | Transactional state transitions, canonical content verification and reconciliation | Actual Firestore cross-instance/revision replacement and crash tests; local mocks prove only local behaviour. |
| Restore an older internally valid store unnoticed | Independently retained checkpoint required for rollback detection | Hashes alone are not attestation or an independent rollback anchor. Backup/restore remains unproved until exercised. |
| Upload private checkout material or credentials | Generated allowlisted build context and per-file inventory | Inspect upload inventory; no `.git`, env, state, research/private archives or arbitrary untracked material. |
| Substitute an image/bundle/config after approval | Plan binds source/config/image/bundle/policy identities and expiry | Reject changed inputs, wrong account/project and guessed mutable tags. |
| Exfiltrate through assets, provider URLs or model APIs | Same-origin assets; provider/model paths disabled; private API egress | Actual browser/network egress observation and DNS/firewall review. Application allowlist is not global egress proof. |
| Leak tokens, raw private requests or identity via logs/errors | Metadata-only redacted logs; generic identity errors | Inspect real logs; no shell tracing/config dumps. |
| Overspend or delete unrelated resources | Explicit total-cost/pilot authority; approved owned-VM start/stop; one-hour tunnel, finally-stop, hourly stop schedule and cooperative 1.25-hour reservation ledger; owned-resource destructive plan | Scheduling can lag 15 minutes or fail; the proposed 80-hour ceiling is not approved usage. CLI controls and alerts are not a hard billing cap. Stopped disk/DNS/images/evidence/logs remain chargeable. |
| Compromise software bootstrap/supply chain | Pinned runtime/dependencies/provider/tool versions and TLS/checksum/signature checks | Image/provenance/scan and independent derivation gates remain mandatory where applicable. Never disable verification. |

## Network and egress

The personal VPC rules allow tagged runtime/access HTTPS to private Google API VIP
`199.36.153.8/30` and deny other IPv4 egress. Private DNS maps approved Google API
and `run.app` lookups to that route. Metadata/OS DNS behaviour, direct VPC Cloud Run
source handling, service-agent access and the effective firewall policy require
hosted inspection. Configuration does not prove the whole boundary.

No unrestricted NAT is added for bootstrap. Stage reviewed proxy code via the
IAP/SSH connection and use the selected maintained/pinned VM image. The operator
must verify its installed Python/TLS trust prerequisites before starting the
proxy; a missing prerequisite blocks that path rather than opening internet
package installation by default.

No cloud VM or stop schedule has been created by the local implementation.
Hosted acceptance must observe bootstrap cleanup, normal/error tunnel cleanup,
off-period VM state and the effective hourly UTC stop policy with no start
schedule. Its Compute service agent has start/stop permissions bound to the owned
instance because the scheduler requires both. Local ledger locking avoids two
connections from one ledger; deleting/copying the ledger or using another machine
can bypass the cooperative hours ceiling. It is not a server-enforced quota.
If cleanup is blocked, a fresh explicit destructive approval can remove owned
resources after the pilot end; expiry must not prevent safe reviewed teardown.

OIDC JWKS fetches use fixed operator-authored HTTPS URLs, bounded size/deadline,
redirect rejection and short cache lifetime. Personal Google certificate routes
fit the declared Google API path. BDUK additionally requires a platform-approved HTTPS path to the exact Okta
discovery, authorisation, token and JWKS endpoints. Runtime token/JWKS traffic and
the browser's declared authentication redirect are identity flows, distinct from
provider/model traffic. The restrictive personal baseline cannot silently allow
arbitrary internet access to make Okta work.

The optional maintained `openid-client` browser adapter validates discovery,
state/nonce, S256 PKCE, code grant and exact issuer/subject binding. Flow state is
consumed once using Firestore CAS. Encrypted Secure/HttpOnly `__Host-` cookies,
five-minute sessions, stored-session checks, Origin checks for mutations and
revocation on POST logout constrain replay/CSRF. Cookie identity never substitutes
for the signed Google transport proof. Exact registration/endpoints and pinned
Secret Manager versions are platform inputs. Flow/session metadata uses 256 fixed slots per family, 512 documents in total,
with bounded compare-and-swap reuse after expiry. Tokens, state, nonce and PKCE
verifier remain in encrypted cookies rather than database metadata. Slot reuse
does not prove backup/restore or disposal; its cost/retention decision remains
explicit.

## Data and external clients

Public metadata is not licence-free data, complete coverage, a live-provider
result or authority for the associated features. Preserve rights, gaps, source
versions and count grains. Generated evidence cannot manufacture missing input
facts. Reject corrupt/unexpected bundle bytes and traversal/symlink paths; there
is no private-original download route.

An external MCP client receives the evidence it reads. A GCP-only backend does
not contain that onward transfer. Personal tests use public/synthetic material;
secure BDUK external-client use requires separately recorded data/identity/client
approval. No arbitrary upload, remote URL fetch or unbounded query is admitted.

## Residual acceptance gates

Local negative tests and protocol traces are useful implementation evidence.
They cannot establish real Google/Okta identity, private ingress from actual
outside sources, hosted Firestore durability, audit log redaction, actual pricing,
rollback/teardown or BDUK acceptance. The implemented browser state/nonce/PKCE/session/CSRF path must be observed with
the approved real identity provider. Standards-compatible authenticated remote
MCP client integration has a separate registration/interoperability gate. Neither
is completed by signed local identity-provider fixtures. See [acceptance](ACCEPTANCE.md).
