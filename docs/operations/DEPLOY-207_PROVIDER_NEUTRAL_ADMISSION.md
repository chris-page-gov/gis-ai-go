# DEPLOY-207 provider-neutral admission and public HTTPS acceptance

Status: implemented repository contract and synthetic assurance fixture; no public
deployment, Azure resource, spend, live provider call, registration or release is
claimed.

Reviewed: 30 August 2026.

## Purpose

This pack turns the remaining deployment boundary into three closed document
contracts plus two filesystem-capability receipts. It prevents a configured
hostname, a successful local container or a transport-only document from being
promoted into live-provider or release evidence.

| Phase | Closed contract | What the contract covers |
| --- | --- | --- |
| Plan | [`deployment-admission-plan.schema.json`](../../schemas/deployment-admission-plan.schema.json) | Exact source, tree and OCI identities plus the controls and authority that must exist before provisioning. It always keeps deployment and release claims false. |
| Direct public transport | [`remote-https-acceptance.schema.json`](../../schemas/remote-https-acceptance.schema.json) | DNS, SNI, certificate, TLS, plaintext, application authority, exact-five capability and deployed operational-control evidence. It requires `live_provider_exercised: false`. |
| Live provider | [`deployed-live-provider-evidence.schema.json`](../../schemas/deployed-live-provider-evidence.schema.json) | One separately authorised and bounded ONS `data.query` through the already accepted public transport. It binds the exact transport document bytes and still keeps release readiness false. |

The deterministic verifier is
[`verify_deployment_admission.py`](../../scripts/verify_deployment_admission.py).
It is offline: it validates document shape and exact cross-document identities but
does not itself contact DNS, a TLS endpoint, a provider or a deployment API. It
therefore reports contract validity only. It does not attest that a stated
observation occurred, and it never reports a public deployment or live provider as
verified. A later reviewed capture and independent-attestation layer must establish
those claims from retained raw observations.

## Current non-deployment fixture

The five files under `tests/contract/fixtures/` are explicitly synthetic:

- `deployment-admission-plan.synthetic.v1.json`;
- `remote-https-acceptance.synthetic.v1.json`; and
- `deployed-live-provider-evidence.synthetic.v1.json`;
- `evidence-filesystem-capability-check-ledger.synthetic.v1.json`; and
- `evidence-filesystem-capability-check-reconciliation.synthetic.v1.json`.

They use the reserved `example.com` domain and fixed fake digests. They test the
contract and verifier only. The verifier reports contract-valid fields,
`observation_provenance_attested: false` and `release_ready: false`. It rejects
them when `--require-non-synthetic-contracts` is supplied. Changing classification
labels cannot turn any document into verified deployment evidence.

Run the complete synthetic contract chain with:

```bash
uv run --locked --cache-dir .uv-cache python \
  scripts/verify_deployment_admission.py \
  --plan tests/contract/fixtures/deployment-admission-plan.synthetic.v1.json \
  --transport tests/contract/fixtures/remote-https-acceptance.synthetic.v1.json \
  --ledger-filesystem-check \
    tests/contract/fixtures/evidence-filesystem-capability-check-ledger.synthetic.v1.json \
  --reconciliation-filesystem-check \
    tests/contract/fixtures/evidence-filesystem-capability-check-reconciliation.synthetic.v1.json \
  --live-provider \
    tests/contract/fixtures/deployed-live-provider-evidence.synthetic.v1.json
```

Run the hostile mutation suite with:

```bash
uv run --locked --cache-dir .uv-cache python -m unittest \
  tests.contract.test_deployment_admission
```

## Phase 1: complete the admission plan

Generate the plan from an exact clean protected-main checkout and the retained
gateway image evidence. Bind:

- the 40-character source commit and tree;
- the OCI archive SHA-256, manifest digest, configuration digest and closed
  evidence-manifest SHA-256; and
- `linux/amd64`, the MCP `2026-07-28` Streamable HTTP transport, the exact five
  tools and the exact three resources.

The one public origin must be a canonical lower-case DNS HTTPS origin without a
port or path. It must derive the exact Host list, Origin list and internal health
probe Host. Forwarded headers are never application authority, and loopback cannot
remain an alternative public authority.

Before the plan can change from `blocked-pending-authority` to
`authorised-pending-deployment-evidence`, it must record:

- a numeric monthly ceiling, currency, cost owner and enforceable hard-stop
  procedure; a budget alert is explicitly not a hard stop;
- named suspension, checkpoint, restore, rollback and incident routes;
- completed RPO, RTO, disposal and log-retention decisions;
- a non-static workload identity; and
- fencing for both rollout and provider-maintenance overlap.

The plan deliberately contains no credential, tenant secret, provider payload or
machine path.

## Phase 2: observe direct public HTTPS transport

Collect the transport document from an independent external client over the direct
public endpoint. A tunnel is forbidden for this phase. The retained evidence must
show all of the following.

### Network and application authority

- DNS answers for the exact hostname;
- the same hostname as SNI and the verified certificate name;
- a valid certificate chain and validity window;
- TLS 1.2 or 1.3 negotiated, with TLS 1.0 and 1.1 rejected;
- plaintext HTTP redirected to the canonical HTTPS origin or rejected before the
  gateway body is reached;
- the exact Host and Origin accepted;
- wrong Host, wrong Origin and loopback Host rejected; and
- `Forwarded`, `X-Forwarded-Host`, `X-Forwarded-Origin` and
  `X-Forwarded-Proto` unable to substitute for rejected application authority.

### Callable surface

- `/healthz`, `/readyz`, `/openapi.json` and `/mcp` pass their exact contracts;
- OpenAPI reports the same canonical origin and retains
  `candidate-unregistered`;
- MCP advertises exactly `catalogue.search`, `catalogue.describe`,
  `selection.resolve`, `data.query` and `evidence.inspect`;
- MCP exposes exactly `catalogue.public`, `catalogue.record` and
  `evidence.receipt`;
- every tool result is contract-valid, contains a valid receipt and has complete
  structured and plain-text forms with semantic parity; and
- the direct API and readiness operation sets match MCP discovery.

The `data.query` transport call in this phase must use the deterministic accepted
fixture path. It is not the later live ONS observation.

### Deployed operational controls

The transport phase is also the operational deployment acceptance. It must retain
evidence that:

- a unique admission lease is acquired before readiness;
- provider rollout and maintenance overlap tests admit at most one writer;
- loss of the lease removes readiness and stops serving before ownership is
  released;
- a least-privilege workload identity is in effect with no static credential;
- egress defaults to deny, admits only the exact accepted ONS origin and paths,
  blocks an unexpected domain and direct-IP route, and forwards no credential;
- the distinct ledger and reconciliation volumes each have an exact, digest-bound
  filesystem-capability receipt whose caller-supplied mount identity matches that
  volume, and pass mode-bit, hard-link,
  symbolic-link rejection, exclusive-create, file and directory `fsync`, restart
  persistence and no-overwrite restore tests;
- backup, RPO, RTO and disposal arrangements are tested rather than inferred from
  provider documentation;
- bounded logs contain correlation identifiers but no secret, raw idempotency key
  or machine path;
- suspension makes the public endpoint unavailable, a checkpoint restores into
  empty private roots and both stores re-verify; and
- a distinct previous accepted image is selected without rebuilding, then the
  candidate is restored without rebuilding, with both identities and health states
  retained.

Replica limits alone do not satisfy the writer-fence fields. A platform may overlap
revisions or maintenance replicas even when its ordinary steady-state count is one.

Verify the real plan and transport evidence with exact expected identities:

```bash
uv run --locked --cache-dir .uv-cache python \
  scripts/verify_deployment_admission.py \
  --plan PRIVATE_PLAN.json \
  --transport PRIVATE_TRANSPORT.json \
  --ledger-filesystem-check PRIVATE_LEDGER_FILESYSTEM_CHECK.json \
  --reconciliation-filesystem-check PRIVATE_RECONCILIATION_FILESYSTEM_CHECK.json \
  --expected-source-commit PROTECTED_MAIN_COMMIT \
  --expected-source-tree PROTECTED_MAIN_TREE \
  --expected-image-manifest sha256:EXACT_OCI_MANIFEST \
  --require-non-synthetic-contracts
```

This command proves that the non-synthetic documents satisfy the closed contracts
and the independently supplied source, tree and image expectations. It does not
authenticate their producer or prove the truth of their observation fields.

Keep private paths outside any committed evidence. A public projection must contain
only path-free identifiers and digests.

## Phase 3: make one bounded live-provider observation

Do not start this phase until the direct transport document passes and separate
provider-call authority is current. The live document must:

- bind the exact SHA-256 of the retained transport JSON;
- repeat the same source, tree, image, provider deployment and public authority;
- run after the accepted transport observation;
- make exactly one bounded `data.query` provider execution through public MCP
  Streamable HTTP;
- retain the fixed ONS dataset, edition, version, source date, rights and licence;
- verify the durable receipt and a subsequent `evidence.inspect` relation;
- verify structured and plain-text parity; and
- retain no provider payload, raw query, credential material, personal data or
  machine path.

Supplying a live document without its transport document fails closed. Mixing a
synthetic document into a real evidence chain also fails.

## What this pack does not authorise

Passing these repository contracts does not authorise or perform resource creation,
provider terms acceptance, spend, registry publication, production registration,
tagging or release. It does not turn the current synthetic fixtures into evidence.
Final `v0.2.0` admission must still reconcile QUAL-206 and DEPLOY-207 against the
exact protected-main and deployed artefacts.
