# Platform review request: private OKF/MCP pilot

Date: 5 October 2026. Status: implementation review request; **not deployment or
BDUK approval**. This document is sanitised. Full account/project/billing,
configuration, plan and result evidence remain in owner/platform-private custody.

Please review deployment of GIS AI GO's current website, original OKF and expanded
OKF+ evidence surfaces, captured-data workbench and custom Streamable HTTP MCP
server in an approved BDUK sandpit. The boundary must be network-private. Browser
and machine clients use the approved Okta integration and server-enforced
attribute/role policy; tool discovery cannot grant a forbidden named invocation.

The initial scope contains admitted public metadata and synthetic fixtures. It
excludes protected BDUK data, licensed feature payloads, private original-document
archives, credentials, BigQuery, external models and live-provider calls. New
content, provider or client access needs a separately scoped data/identity and
cost decision. Passing personal local/transport tests cannot grant those rights.

## Actual package identity

`package-approval` generates the transferable ZIP, checksum manifest and redacted
summary from the implementation. Review the generated package's actual identities,
not values invented in this template:

| Identity | Authoritative generated evidence |
| --- | --- |
| Source revision and admitted working tree | Source/build manifest and per-file digests |
| IaC/provider/tool/lock identities | Submitted infrastructure and checksum manifest |
| Application image and provenance | Local OCI/build evidence; real published digest when publication is approved |
| OKF/OKF+ profiles, content roots, rights/counts | Prepared bundle/release and upload manifests |
| UI/API/MCP/policy scope | Runtime capability and policy manifests; repository discovery |
| Resource/change/cost plan | Sanitised submitted plan with unresolved cloud inputs explicit; the documented London illustration retains unverified billing/FX/tax gates. Local ignored cost evidence is excluded from the source ZIP and requires separate sanitisation and approval binding. |
| Test results and gaps | Machine-readable acceptance report and retained local logs |
| Review ZIP identity | Generated SHA-256 checksum; compare before execution |

The ZIP is an actual implementation package with executable scripts and tests;
unavailable credentials do not prevent producing it. Its sanitised configuration
examples deliberately have unresolved account/project/billing/spend fields. The
reviewer must restore private approved inputs rather than execute examples as
accepted deployment configuration.

## Required platform inputs

| Area | Supply or approve | Until supplied |
| --- | --- | --- |
| Project/billing/region | Exact project ID/number, organisation/service-project relationship, approved location, cost centre/currency, spend envelope and pilot duration | No cloud mutation. |
| Source/workspace admission | Full security/source review for the exact fetched GitHub commit, dependency locks and remaining canonical gates | No repository script, dependency install, container build/opening or workspace trust on the secure machine before the recorded decision. |
| Development/build image admission | Exact internal image digest, vulnerability disposition, SBOM/provenance/signature policy, permitted toolchain and custodian | Secure profile fails closed; image family or mutable tag approval is insufficient. |
| Build/runtime identities | Approved deployer, publisher, service agents, runtime/invoker identities and resource-scoped permissions | No broad Owner/Editor or downloadable keys. |
| Build facilities | Approved local/platform build route, base image/digests, dependency mirrors, registry and scan/provenance gates | No source checkout upload or internet installer. |
| Network | Shared VPC host/service project, subnet, DNS/routes/private API path, user/developer connection, firewall/network ownership | Internal ingress; consume existing platform infrastructure. |
| Network proof | Permitted inside test source and valid-token outside/unauthorised-source tests, bypass controls | Ingress configuration alone cannot pass privacy. |
| Okta application identity | Exact issuer/tenant, audience/client/resource IDs, JWKS route, redirects, scopes, groups/subject mapping, token/session lifetime and revocation | Human SSO and multi-role acceptance remain blocked. |
| Federation | Existing workforce OIDC/SAML/IAP route and owners, or separately selected application-level OIDC architecture | No new organisation/federation modification. |
| MCP OAuth | Approved resource/server discovery, PKCE and client registration/interoperability route | A browser cookie/HTML login is not an authenticated MCP pass. |
| Policy/data ownership | Real group-to-role mapping, admitted release/classification, evidence ownership, permitted operations and client recipients | Default deny; email suffix/purpose does not grant authority. |
| Egress | Google API/private VIP rules; explicitly approved Okta/JWKS or identity gateway destinations | No arbitrary internet, model or live-provider egress. |
| State/retention | Firestore database/location/IAM conditions, capacity, PITR/backup/restore, independent checkpoint, retention/disposal owners | No filesystem durability, executed backup or recovery-objective claim. |
| Secrets | Approved secret-store references, secret owners/rotation and injection route | No embedded secrets in config, Terraform state, image or ZIP. |
| Assurance | Canonical CI, IaC validation, scan/provenance, policy/security and independent hosted tests | Existing release gates remain intact. |
| Operations/cost | Logging/redaction/sinks, audit/support owner, stop/revoke, budgets/alerts, retention and deletion authority | Pilot only; alerts do not stop spend; no production SLA claim. |

## Identity decision to record

Workforce Identity Federation with Okta OIDC/SAML needs a Google Cloud
organisation and concerns Google access. Application OIDC concerns the actual
human/client subject and claims used by policy. A personal Google project cannot
prove the workforce path. SAML may be upstream federation; it is not `/mcp`'s
bearer-token protocol. Select and approve the exact supported architecture,
issuer/audiences and ownership rather than treating these as interchangeable.

The personal VM/tunnel is an on-demand operator access bridge into Cloud Run;
the application does not need that VM running between connections. Its draft
80-hour reserved-usage ceiling, one-hour tunnels, finally-stop and hourly UTC
stop-only schedule require exact scoped approval and real operating evidence.
Compute scheduling can lag 15 minutes; local ledger enforcement and budget alerts
are not a financial hard stop. No personal VM has been created here. BDUK uses
the approved network connection. Its private gateway must convey separately validated
transport and application tokens; it must not replace human identity with the
Cloud Run invoker service account or trust caller-written email/role headers.
The implementation includes strict bearer verification and a maintained
`openid-client` 6.8.8 browser code flow with state/nonce/S256 PKCE, five-minute
secure sessions, stored flow/session CAS, Origin CSRF validation and POST logout.
BDUK deployment requires its exact approved browser registration, endpoint
allowlist and pinned session-key/client-secret references. Actual provider sign-in,
revocation and direct MCP OAuth remain separate hosted acceptance gates. The
platform must allow the declared Okta discovery/token/JWKS HTTPS route independently
of Google private API access; no provider/model egress is implied.

## Package review and execution

Review the ZIP checksum, per-file inventory, locks, actual source/build identities,
capability/rights matrix, IaC and IAM changes, allowed destinations, tests,
redacted results, cost worksheet and runbook. The package excludes private
configuration/state, personal identities/projects, credentials, research archives
and private originals. Verify the sanitisation scan and archive inventory before
sharing it.

The secure machine's source route is GitHub. Follow
[the existing-clone transition](../../development/SECURE_TRANSITION.md), retaining
dirty work and the exact reviewed full commit. A source review package can inform
the decision without authorising its execution. The editor container, approved
builder and operator host have separate permissions; no default socket/home,
credential or protected-data mount connects them. A mirror or CA change is an
explicit platform input, never permission to disable TLS.

Keep infrastructure approval and application release approval separate where
platform policy requires. The recorded approval must bind the exact immutable
plan/source/image/bundle/policy identities, allowed actions, cost envelope,
retention, expiry and exceptions. Revalidate prerequisite readback immediately
before applying; unchanged prior approval is reusable only inside that scope.
Deployment approval cannot outlive the explicit pilot end or 90 days from its
decision. Personal VM starts/stops require the recorded
`connect-start-stop-owned-vm` action and exact owned resource. A fresh destructive
plan has a seven-day approval review window and can cover cleanup after pilot
expiry. Stopped disks, DNS and retained evidence/images/logs remain in the cost
inventory until their approved removal or disposal.

Report `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN` or justified `NOT_APPLICABLE` for each
of the 41 retained acceptance requirements. Local fixtures/emulation, hosted
network/identity/storage and BDUK acceptance are different evidence lanes. A
homepage/health result is not MCP proof, a Google invoker token is not Okta proof,
and the review ZIP is not enterprise approval.

## Platform decision record

Decision, approvers, approved environment/project, immutable plan/package IDs,
actions, cost envelope, data/client scope, conditions/exclusions, expiry and
retention/deletion authority must be recorded in the private approval evidence.
Until that evidence exists the requested BDUK deployment remains blocked; local
implementation, package preparation and deterministic validation can continue.
