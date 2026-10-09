# Identity and permission matrix

Terraform uses additive IAM member resources. It does not replace a project's
whole policy, grant basic Owner/Editor to the runtime or create service-account
keys. Exact member names, project IDs and observed permissions belong in private
plan/results, not this public document.

## Google permissions

| Principal | Role or permissions | Scope | Purpose and remaining verification |
| --- | --- | --- | --- |
| Approved deployer | Approved resource administration and service-account act-as permissions | Selected pilot resources/project only | Terraform provisioning; preflight must inspect actual permission availability. No automatic broad role grant. |
| Approved image publisher | `roles/artifactregistry.writer` | Pilot image repository | Publish only the reviewed locally built OCI image; no repository-wide source upload. |
| Runtime service account | `roles/datastore.user`, conditional on pilot database resource | Named evidence database and descendants | Transactional evidence. The effective database condition must be tested against real Firestore; the application also enforces principal ownership. |
| Runtime service account | Platform-supported Cloud Run service-agent image/VPC access | Selected registry/subnet | Pull image and use direct VPC egress; service-agent/network requirements must be observed, especially in Shared VPC. No publisher permission needed at runtime. |
| Dedicated access/invoker service account | `roles/run.invoker` | One private Cloud Run service | Fixed-target transport only; not human identity or application entitlement. |
| Approved personal operator | `roles/iap.tunnelResourceAccessor`, destination port 22 condition | Dedicated access VM | Enter IAP SSH tunnel, never arbitrary target/port access. |
| Approved personal operator | `roles/compute.osAdminLogin` | Dedicated access VM | Reviewed proxy installation/operation. The current implementation needs admin login; do not describe it as ordinary unprivileged OS Login. |
| Approved personal operator | `roles/iam.serviceAccountUser` | Dedicated access/invoker service account | Attach/use the VM identity through OS Login; not a downloaded key. |
| Approved personal operator | Existing authorised `compute.instances.start` and `compute.instances.stop` permissions | Exact owned access VM | `connect-start-stop-owned-vm` must be in the recorded plan approval. The CLI does not grant these permissions or start another VM. |
| Compute Engine service agent | Custom role containing `compute.instances.start` and `compute.instances.stop` | Instance IAM binding on the exact owned access VM | Compute instance scheduling requires both permissions. The attached hourly UTC schedule contains only stops, with no automatic starts; hosted effectiveness remains untested. |
| Runtime service account, browser mode only | `roles/secretmanager.secretAccessor` | Each explicitly approved session-key/client-secret resource; configured immutable version | Cloud Run secret injection; preflight reads version metadata only and does not fetch secret values. |
| Backup custodian | Separately approved storage/backup permissions | Private backup bucket/database | No runtime blanket bucket writer or backup-restorer grant is implied. |
| Auditor/reviewer | Separately approved read-only operational permissions | Pilot resources | Inspect IAM, logs, revisions, costs and retention without a deployment grant. |

The foundation may enable the explicitly planned Run, Artifact Registry, Compute,
IAP, Firestore, Storage, IAM and DNS APIs. Preflight never enables them; API
activation is a cloud mutation covered by the first approval. APIs remain enabled
on destroy to avoid disrupting unrelated uses.

The personal VM's `cloud-platform` OAuth scope does not itself grant API access:
IAM still restricts the attached invoker account. Hosted tests must confirm that
it cannot access unrelated services, mutate evidence, mint arbitrary principals
or expose tokens. Cloud Run service-agent grants and subnet access are platform
prerequisites; they must not be guessed from a successful local Terraform check.

## Application roles and attributes

The reviewable source-bound policy is
[`infra/gcp/policy/gcp-public-metadata.v1.json`](../../../infra/gcp/policy/gcp-public-metadata.v1.json),
ID `gis-ai-go.gcp-public-metadata.v1`. Its role grants and tool map derive from the
actual implementation and bind exact source hashes. Lifecycle approval binds
this manifest; it is not a dynamically interpreted external policy service.

Role names are application/test roles, not claimed BDUK groups. The platform maps
approved exact OIDC subjects/groups to these roles through private configuration.
Unknown/missing claims deny; an email domain, claimed purpose or role header does
not grant access. Current roles/capabilities come from
`apps/mcp-gateway/src/gcp-identity.ts`.

| Role | Capabilities | Evidence boundary |
| --- | --- | --- |
| `viewer` | Website, knowledge read/search, captured CPIH selection | Selection is non-authorising; no query/export/inspection grant. |
| `analyst` | Viewer capabilities plus bounded captured CPIH query and evidence inspection | Own principal-scoped evidence only. |
| `evidence-auditor` | Website, knowledge read/search and evidence inspection | Same ownership scope; no automatic other-user evidence or provider execution. |
| `platform-operator` | Operational status capability | Does not inherit knowledge/query access. |
| `owner` | All admitted pilot capabilities, including admitted export | Only declared public metadata and the correct environment/ownership scope. |

The admitted MCP tool map is explicit: `okf_search` and `okf_describe` serve both
bundles; `okf_export` returns the authorised release inventory (owner only);
`web216_cpih_select`, `web216_cpih_query` and `web216_cpih_inspect` preserve the
maintained captured-data contract. Search is bounded to one to ten ASCII English
keywords and one to twenty records. No live-provider tool is added.

Every decision also checks verified-principal branding, token expiry, environment,
classification and resource ownership. `public-metadata` is the only admitted
classification. Even an owner role does not admit protected BDUK/licensed/private
archive data. Discovery, named invocation, APIs/resources/exports and evidence
lookup must use the same decision. Caches/cursors must carry or bind that scope.

The `single-owner-transport-pilot` principal is explicitly a transport milestone.
Its owner role is a configuration of that intermediate pilot; it is not a
cryptographically established human role and cannot pass real-user/Okta gates.
Deployed OIDC mode must validate independent issuer, audience, signature, expiry
and the configured claim mapping. No deployed role-switch endpoint is permitted.

## Revocation and credential handling

Google IAM/tunnel access and application OIDC access are revoked separately. Stop
the tunnel to end the local route; `connect` then attempts to stop its VM. Check
the result and `status` if cleanup fails. Remove the scoped invoker/IAP binding to
revoke transport access through a reviewed change. An already issued token and
in-flight operation may have a bounded remaining lifetime. Do not claim immediate
revocation without its actual observation.

The JWT verifier caches configured JWKS for at most five minutes and rejects
expired tokens on each decision. Group/subject roles are derived from configured
mappings and token claims; a group change can remain effective until token expiry
or a reviewed configuration change. Bearer JWTs have a one-hour maximum issued lifetime; the browser flow requires
access tokens and sessions of at most five minutes and checks stored session
status on use. The five-minute JWKS cache is not a five-minute group-revocation
guarantee. The approved policy update mechanism and observed maximum revocation
delay must be tested in hosted mode. Local clocks/fixture claims do not establish
real identity-provider or Google IAM propagation.

Secret references identify platform-managed material. Never put token values,
client secrets, credentials or key files in Terraform variables/state, config
examples, images, logs or the platform ZIP. The maintained browser adapter implements state, nonce, PKCE, secure cookies,
server-side session checks, Origin CSRF validation and logout revocation. Its
configured registration and secret references, actual hosted sign-in and independent
MCP OAuth interoperability remain identity integration gates. No Okta tenant,
workforce federation or human group is invented by these application roles.
