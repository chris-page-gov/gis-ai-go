# Hosting: static public pack, Azure protected path, portable exit

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## Recommendation

1. Publish the research and Stage 1 open discovery pack as a relative-link static site on ordinary static hosting.
2. Use Azure UK for the first protected pilot because Entra Conditional Access, managed identities and managed PostgreSQL/PostGIS align with the recommended identity and device posture model. [S-AZURE-REGIONS] [S-AZURE-POSTGIS] [S-ENTRA-CA]
3. Preserve portability through containers, OpenAPI/OGC contracts, PostgreSQL, open geospatial formats, OPA policy tests and infrastructure as code. GCP and AWS are credible alternatives where the organisational landing zone dictates. [S-GCP-REGIONS] [S-AWS-REGIONS]
4. Use Cloudflare or equivalent CDN/static hosting for the public edge only; do not place protected geospatial authority there without a separately evidenced backend/control model.

## Options

| Option | Open | PSGA/commercial | Identity/data strengths | Decision |
| --- | --- | --- | --- | --- |
| Portable static hosting (GitHub Pages/Cloudflare Pages) | strong | not suitable / not suitable | Optional public sign-in only; no protected backend; none; static/object host | Initial public research pack and Stage 1 demonstrator |
| ChatGPT Sites | conditional experiment | not suitable on current evidence / not suitable on current evidence | Sign in with ChatGPT where available; not established for this design; platform features subject to current beta | Optional open mirror only after account-specific verification |
| Microsoft Azure managed platform | strong | strong with landing-zone controls / strong with isolation | Entra ID, Conditional Access, managed identities; managed PostgreSQL extensions; Blob Storage | Preferred protected pilot and credible production path |
| Google Cloud managed platform | strong | strong with approved landing zone / strong | Cloud IAM, workforce/workload identity, external OIDC; Cloud SQL PostgreSQL; Cloud Storage | Strong alternative where DSIT/GCP landing zones dominate |
| AWS managed platform | strong | strong with approved landing zone / strong | IAM, workforce federation, external OIDC; RDS/Aurora PostgreSQL; S3 | Strong alternative for AWS-established organisations |
| Cloudflare edge platform | excellent | limited for core geospatial authority / limited without separate backend | Access/Zero Trust or external OIDC; external; R2 | Public edge/static delivery, not protected geospatial authority |
| Shared multi-tier deployment | possible | high-risk / high-risk | shared; shared namespaces; shared buckets/prefixes | Reject as the default |
| Federated organisational deployments | strong federation | strong long-term / contract-specific | local enterprise identity plus federation; per operator; per operator | Credible long-term route after central reference implementation |

## ChatGPT Sites

**Verified fact at retrieval.** Sites is a beta product and the official material requires account/region and data-residency checks. It is not evidence for a protected PSGA/commercial deployment. [S-OPENAI-SITES] [S-OPENAI-SITES-RESIDENCY]

**Recommendation.** Conduct only an optional open or synthetic experiment after confirming actual UK Pro availability. Keep the canonical pack portable and independently hostable so Sites can be added or removed without changing the evidence/data model.

## Azure protected pilot topology

- public/static front end and public OKF artefacts;
- separate authenticated MCP gateway on Container Apps or App Service;
- private Python geospatial execution service;
- Azure Database for PostgreSQL with PostGIS;
- separate Blob containers/accounts or subscriptions per tier where risk requires;
- Entra ID, Conditional Access and managed identities;
- OPA sidecar/service with versioned policy bundle;
- Key Vault and server-side provider credential broker;
- API Management/Front Door where gateway/rate/WAF controls are justified;
- OpenTelemetry/Azure Monitor plus an evidence store with restricted identities;
- private endpoints/VNet and egress allow-listing for protected provider access.

## Cost caveat

The ranges in [`data/hosting-options.json`](../data/hosting-options.json) are deliberately broad architecture-order assumptions. They exclude people, support, procurement, provider-data charges, security tooling, discounts, VAT and incident/DR requirements. A measured workload and the actual departmental landing zone are required before a business case.

## Exit strategy

- keep OKF/JSON/Markdown and public assets relative and host-neutral;
- store vector/raster artefacts in open formats;
- use PostgreSQL/PostGIS rather than cloud-only query semantics;
- keep policy input/decision schemas engine-neutral and test OPA separately;
- use OpenTelemetry and W3C Trace Context;
- use Terraform/Bicep-equivalent modular IaC with documented provider substitutions;
- avoid Kubernetes until workload or organisational requirements justify it.
