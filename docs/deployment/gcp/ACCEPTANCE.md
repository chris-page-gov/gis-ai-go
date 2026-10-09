# Acceptance evidence

The executable requirements catalogue is
[`evaluation/gcp-private-acceptance.v1.json`](../../../evaluation/gcp-private-acceptance.v1.json).
It preserves all **41** supplied handover requirements, their IDs, required levels
and statuses without weakening them. The catalogue starts `NOT_RUN`; it is not a
claim that tests have executed. `verify` emits a separate machine-readable result
and evidence inventory under private `artifacts/gcp/`.

Run the lifecycle verifier against the exact prepared/deployed release:

```sh
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.json verify
```

Only an observed test with retained evidence can be `PASS`. A required `FAIL` or
`BLOCKED` prevents its acceptance level and a non-zero verifier outcome.
`NOT_APPLICABLE` requires architecture-specific recorded justification and cannot
waive network privacy, separate identity, scoped policy, evidence durability or
another fixed requirement. `NOT_RUN` is not a pass. An old observation does not
establish readiness for changed source, policy, configuration or resources.

## Levels

| Level | Evidence required |
| --- | --- |
| `prepared-only` | Local source/build/admission/identity bindings and actual sanitised executable review package; no hosted claim. Required local/canonical checks must be recorded accurately. |
| `private-transport-smoke-tested` | Actual permitted private access and forbidden outside route observations, real invocation authentication and MCP wire smoke test; labelled ephemeral/single-owner limits if applicable. |
| `personal-reference-accepted` | Selected current UI/OKF+/MCP functionality, declared real personal identity/policy gates, persisted evidence after replacement, operations/cost/rollback/teardown gates. |
| `bduk-ready-for-review` | Portable sanitised implementation/plan/test package and exact platform input request; no BDUK approval or SSO claim. |
| `bduk-sandpit-accepted` | Actual platform approval and in-sandpit private network, Okta, real multi-role policy, runtime/storage/operations observations. |

`single-owner-transport-pilot` identifies a limited authentication milestone. It
cannot satisfy real human identity, completed browser SSO, independently
OAuth-authenticated MCP or BDUK Okta tests. An application JWT unit test is a local
identity-logic test, not hosted sign-in. A persisted local/emulated receipt is not
Cloud Run/Firestore replacement proof.

## Check mapping

`scripts/gcp/test_prepare.mjs`, lifecycle/proxy tests under
`tests/deployment/` and focused gateway GCP tests cover the new build,
connection, identity/policy, HTTP/MCP and storage seams. Existing OKF+, workbench and
canonical repository tests remain relevant. The run manifest records the exact
commands and outcomes; the table below maps requirements to evidence, not to an
unobserved pass.

| IDs | Local implementation checks | Hosted/platform evidence still required |
| --- | --- | --- |
| SRC01–SRC03 | Current authority/branch/dirty inventory; repository discovery; additive assembly and preserved entrypoints | Approved exact source/working-tree identity and unchanged existing release/deployments. |
| BUILD01–BUILD03 | Pinned dependencies, actual OKF/OKF+ verification, allowlisted context, source/config/bundle/policy hashes, local OCI when available, relevant canonical assurance | Observed published image digest/provenance and saved plan binding; no guessed tag. |
| NET01–NET03 | IaC rules, proxy fixed upstream, Host/Origin checks and schema validation | Inside UI/MCP success; public valid-token no content; unauthorised project/source denial; real routes/DNS/Shared VPC recognition. |
| NET04–NET05 | Loopback/IAP target rejection; recorded owned-VM start/stop authority; one-hour tunnel/finally-stop; cooperative reservation ledger and hourly stop-only IaC | Effective no-external-IP/SSH/firewall/listener readback; observed bootstrap and normal/error-exit VM stops; tunnel-close/access-ceases; stop-only UTC schedule readback/execution, allowing its declared delay. |
| AUTH01–AUTH03 | Distinct signed transport/human proofs; invalid signature/issuer/audience/expiry; spoofed headers | Allowed and forbidden real hosted identities; recorded actual Google principals and human subject. |
| AUTH04–AUTH05 | Bearer checks plus maintained OIDC discovery/code flow, state/nonce/S256 PKCE, encrypted cookies, session/flow CAS, CSRF and logout against signed local issuer fixtures | Actual registered browser/Okta sign-in and revocation; separate MCP OAuth client test. Local issuer fixtures are not Okta/platform evidence. |
| POL01–POL05 | Role-dependent discovery; named-call denial; equivalent resources/API/export/evidence; missing attributes and principal scope | Actual hosted roles, group changes, policy/token lifetime and measured maximum revocation delay. |
| MCP01–MCP04 | Real local initialise/discovery/tool/receipt wire checks; closed input/protocol/Origin handling, cancellation/refusals | Independent client through private route, exact negotiated versions, real evidence inspection and streaming/cancellation transcript. |
| KNOW01–KNOW04 | Known original OKF and expanded OKF+ records; release/content roots, provenance/rights/dates/gaps; corrupt/traversal rejection | Same admitted release through actual UI/MCP, unavailable private originals and accurate cached/live/count labels. |
| STATE01–STATE04 | Scoped claims/receipt/head verification; same/conflicting-key concurrency; CAS conflict/uncertain-write reconciliation | Real Firestore cross-instance/revision inspection, process loss, ownership, retention and rollback evidence. |
| OPS01–OPS03 | No provider/model path; bounded fixed destinations; log/error redaction tests and IAM resources | Runtime/page-network egress; effective least privilege; real logs/sensitive-header exclusion. |
| OPS04–OPS06 | Bound compatible-release rollback/destroy approval, deployment validity through explicit pilot end, fresh cleanup approval after expiry, and cost/retention model | Approved hosted rollback/deletion and access-hours scope; retained stopped-disk/DNS/evidence inventory; billing-currency prices, full-duration/retained costs, approved total spend and incurred costs. |
| PACK01–PACK02 | Actual generated ZIP/checksum, allowlisted/scrubbed inventory and truthful result statuses | Platform decision and immutable approval package identity; local results do not become hosted results. |

## Evidence content

Each result records requirement ID/status, observed time, source/release/config
identity, evidence paths and a reason for blocked/not-run/not-applicable results.
Retain bounded request/response protocol material only after redaction. Tokens,
cookies, private identities/project names, raw protected payloads and credentials
must not enter public evidence or the sanitised ZIP.

Hosted proof must include separate valid and invalid network/authentication cases.
An HTTP 200 homepage, `healthz`, HTML login redirect or accepted Terraform syntax
is not MCP, human SSO, private network or durability acceptance. Distinguish
network denial from IAM denial. Record negotiated protocol and independent client
version from the observed transcript rather than inferring them from a package.

For each bundle test, retain a known record ID, selected release/content root,
consumer route, source/citation fields, rights and explicit count/freshness gaps.
The original OKF's 36 records and expanded OKF+'s 30,833 metadata representations
remain separate grains; neither number establishes unique datasets or global
source coverage. Captured CPIH is historical cached evidence, not a new live
provider observation.

Persistence evidence must show the same owned receipt after actual instance or
revision replacement; concurrent duplicate keys must return the same valid
result, conflicting fingerprints must refuse, and lost-response reconciliation
must inspect the original committed result without executing it again. Code
rollback must preserve readable compatible evidence. Backups/PITR configuration
is not an executed backup/restore test or an independent rollback anchor.

## Current unexecuted gates

Cloud authentication, verified project billing/prices and first-mutation approval
are not present in this environment. Selected project and owner spending
authority are recorded privately and do not imply verified cloud access. No access
VM has been created. The 80-hour draft operating ceiling and illustrative USD
prices do not authorise deployment or establish fit within the total envelope.
Hosted VM cleanup/scheduling, private routing, real Google human SSO,
remote MCP OAuth interoperability, actual Firestore replacement/recovery,
rollback/destruction and BDUK platform/Okta tests therefore remain blocked or not
run as reported by the generated evidence. The BDUK profile additionally requires the approved browser client/callback,
identity HTTPS destinations and existing Secret Manager version references. The
absence of those prerequisites must not stop preparing/testing the implementation or producing the actual
sanitised review package.
