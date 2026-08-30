# DEPLOY-207 Azure admission decision pack

Status: provider-specific decision preparation; no Azure authority, resource,
deployment or spend is claimed.

Reviewed: 30 August 2026.

## Purpose

This pack turns the remaining Azure questions into explicit Tuesday decisions. It
does not contain deployable infrastructure or invented tenant, subscription, region,
hostname, owner or cost values. The provider-neutral contracts remain authoritative:

- [`deployment-admission-plan.schema.json`](../../schemas/deployment-admission-plan.schema.json)
  describes the plan that must be complete before provisioning;
- [`remote-https-acceptance.schema.json`](../../schemas/remote-https-acceptance.schema.json)
  separates public transport evidence from provider execution; and
- [`deployed-live-provider-evidence.schema.json`](../../schemas/deployed-live-provider-evidence.schema.json)
  admits the later, separately authorised live-provider observation.

Azure Container Apps is a plausible candidate, not an accepted runtime. The exact
provider-neutral image and application contracts must remain unchanged if another
provider is selected.

## Facts established from current Microsoft documentation

| Topic | Current source-backed fact | GIS AI GO consequence |
| --- | --- | --- |
| Public ingress | Container Apps HTTP ingress provides a generated FQDN, TLS termination and HTTPS using TLS 1.2 or 1.3. Port 80 redirects to HTTPS by default. | The first candidate can use the generated FQDN as the one exact `GIS_AI_GO_PUBLIC_HTTPS_ORIGIN`; a custom domain is not required initially. The live acceptance run must still prove the realised endpoint. |
| Request authority | Container Apps adds forwarded headers. The application already treats them as untrusted authority. | The immediate ingress must preserve the real public `Host`; a forwarded header cannot repair a wrong `Host` or `Origin`. |
| Probes | Container Apps supports HTTP(S) and TCP probes, not `exec` probes. Its resource schema documents custom HTTP headers and specifically recommends setting `Host` through `httpHeaders`. | Define explicit HTTP startup, liveness and readiness probes and supply the exact generated FQDN in the `Host` header for `/healthz` and `/readyz`. Do not rely on the portal's default TCP probes. |
| Replicas and revisions | Replica limits are per revision, but platform maintenance can temporarily create extra replicas. Revision changes can overlap old and new runtime state. | `minReplicas: 1` and `maxReplicas: 1` do not prove single-writer operation. A separate lease or fence must prevent two replicas or revisions from writing the linked ledger and reconciliation index. |
| Persistent files | Azure Files NFS supports POSIX permissions, hard links and symbolic links. It uses network controls rather than user identity. | Two independently identified NFS shares are candidates for the distinct ledger and reconciliation volumes, subject to the repository filesystem probe on each actual mount and a private network boundary. The checkpoint destination remains separately governed. Documentation alone is not acceptance. |
| Recovery | Azure Files NFS supports snapshots, but the documented Azure file-share backup feature is not supported for NFS shares. | Tuesday's decision must name the snapshot/export mechanism, independent checkpoint destination, schedule, retention, RPO, RTO, restore test and disposal owner. |
| Cost control | Azure budgets generate alerts; they do not stop running resources or consumption, and cost data is delayed. | A numeric monthly ceiling needs a separately owned hard-stop procedure or enforceable service limits. A budget alert alone is not authority to continue spending. |

Primary sources:

- [Container Apps ingress](https://learn.microsoft.com/en-us/Azure/container-apps/ingress-overview)
- [Container Apps health probes](https://learn.microsoft.com/en-us/azure/container-apps/health-probes)
- [Container Apps ARM and Bicep template reference](https://learn.microsoft.com/en-us/azure/templates/microsoft.app/containerapps)
- [Container Apps scaling](https://learn.microsoft.com/en-us/azure/container-apps/scale-app)
- [Container Apps revisions](https://learn.microsoft.com/en-us/azure/container-apps/revisions)
- [Azure Files mounts in Container Apps](https://learn.microsoft.com/en-us/azure/container-apps/storage-mounts-azure-files)
- [Azure Files NFS](https://learn.microsoft.com/en-us/azure/storage/files/files-nfs-protocol)
- [Azure Files deployment planning](https://learn.microsoft.com/en-us/azure/storage/files/storage-files-planning)
- [Azure budget behaviour](https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets)

Recheck these mutable sources when the deployment plan is completed.

## Decisions required before provisioning

Record each value in the closed deployment-admission plan. `TBC`, a blank value or
an undocumented default fails admission.

| Decision | Required record |
| --- | --- |
| Authority | Named decision owner, approval time, authorised activity and expiry or review point. |
| Azure boundary | Tenant, subscription, resource group, resource owner and least-privilege deployment identity. |
| Location | Selected region and the evidence that the required Container Apps, networking, registry, logging and NFS services are available there. |
| Spend | Currency, numeric monthly ceiling, alert thresholds, responsible recipient and a hard-stop action that is not merely an Azure budget alert. |
| Image | Registry, immutable OCI digest and proof that the bytes equal the protected-main accepted image. Mutable tags are diagnostic labels only. |
| Public authority | Generated FQDN for the first candidate, exact HTTPS origin and whether a later custom domain is separately authorised. |
| Ingress | External HTTPS only, private target port `8787`, exact `Host` probes, plaintext behaviour and log-safe rejection of authority substitution. |
| Writer fence | Lease store, holder identity, acquisition/renewal/expiry rules, old-revision exclusion, readiness behaviour and recovery operator. |
| Storage | Two independently identified NFS shares, their private endpoints or service endpoints, UID/GID and mode expectations, volume capacities, encryption and a passed filesystem-capability receipt for each mount. |
| Recovery | Separately governed checkpoint destination, snapshot/export schedule, RPO, RTO, retention, restore rehearsal and disposal procedure. |
| Egress | Exact ONS destination policy, DNS behaviour, proxy boundary and denial of other outbound traffic. |
| Identity and secrets | Workload identity, registry pull authority and the handling boundary for any storage credential. No secret belongs in source, plans or evidence. |
| Operations | Named deploy, suspend, checkpoint, restore, rollback, cost and incident operators, with bounded logs and retention. |
| Previous image | Exact accepted rollback digest and evidence that it remains retrievable without rebuilding. |

## Recommended first-candidate shape

This is a recommendation to test, not deployable configuration:

1. use one Container Apps environment with external HTTP ingress and its generated
   FQDN;
2. send traffic only to the exact protected-main image digest;
3. keep the application target on private port `8787` and configure explicit HTTP
   probes carrying the public `Host`;
4. request one normal replica but require the external writer fence before readiness,
   because the platform can create temporary overlapping replicas;
5. mount two independently identified private-network Azure Files NFS shares, one
   for the ledger and one for the reconciliation index, only after the filesystem
   probe proves the required POSIX and hard-link behaviour on each actual mount;
   keep the checkpoint destination separately governed; and
6. keep the MCP Registry entry absent until deployment, remote HTTPS, provider,
   recovery, suspension and rollback evidence all pass.

## Authorised execution sequence after Tuesday's decisions

Each step stops on an unfilled field, failed checker or identity mismatch.

1. Complete and validate the deployment-admission plan without credentials.
2. Re-verify the exact source, OCI digest, SBOM, vulnerability evidence and retained
   scanner databases.
3. Provision the bounded resource group, environment, registry access, private
   network, two NFS shares, separately governed checkpoint destination, logs,
   alerts and hard-stop controls.
4. Run and retain a separately bound filesystem-capability check on each mounted
   ledger and reconciliation share before starting the gateway writer.
5. Deploy the unregistered image digest with the writer fence closed, then verify
   health and deliberately blocked readiness.
6. Acquire the sole-writer lease, verify capacity-aware readiness and run the
   transport-only remote HTTPS acceptance pack. Keep live-provider claims false.
7. Make one separately recorded bounded live `data.query` observation and verify
   its trace, policy, result, receipt and plain-text parity.
8. Stop the writer, checkpoint, restore into empty roots, resume, suspend the
   service, roll back to the previous exact image and restore the candidate without
   rebuilding.
9. Complete QUAL-206 and DEPLOY-207 evidence. Only then prepare the sole version
   change, tag, GitHub Release, deployed release rerun and MCP Registry publication.

## Reject or stop if

- the budget is treated as a hard spending cap;
- replica limits are treated as a single-writer fence;
- the generated FQDN, TLS certificate or NFS documentation is treated as runtime
  evidence without a real observation;
- a storage mount lacks the exact filesystem-capability receipt;
- the ingress rewrites a rejected `Host` to loopback or trusts caller-controlled
  forwarded headers;
- the provider requires broad credentials, public storage, general egress or an
  unbounded log stream;
- any requested change weakens the five-tool, three-resource, durable-evidence or
  non-registration boundary; or
- deployment proceeds without a named suspension, rollback and cost operator.
