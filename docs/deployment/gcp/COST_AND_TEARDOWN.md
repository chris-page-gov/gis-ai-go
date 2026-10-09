# Cost approval and teardown

This public worksheet is parameterised; actual account/project and the owner's
recorded operating envelope belong in private configuration and approval.
Estimated and actual cloud cost remain unresolved until the operator verifies the
exact project/billing attachment,
regional SKUs, expected usage and pilot duration. The code does not assume GBP,
convert USD prices without a verified basis or promise that a private pilot is
free.

## Parameterised costed plan

The closed configuration contains `authority.spend_envelope`. For a mutation it
must specify `currency`, `maximum_initial`, `maximum_monthly`, `pilot_days` (1 to
90), `pricing_as_of`, `pricing_source`, `assumptions`, `estimated_initial`,
`estimated_monthly`, `maximum_total`, `estimated_total`, `estimated_retained` and
`budget_is_alert_only: true`. The selected initial/monthly estimates and the
full-duration total including retained charges must fit the approved maxima. Null/unpriced inputs block approval/apply. The private
approval additionally records the exact billing account/currency and pilot end.

Use regional prices and workload assumptions in the billing currency. Do not
assume free-tier eligibility or deduct credits as a reason to enlarge authority.
Where the owner grants a total envelope, the initial, full-duration and retained
resource costs together must fit that total; a monthly maximum alone is not
sufficient. The personal draft now uses an on-demand access VM requiring approved
start/stop scope, a one-hour foreground tunnel and stop cleanup, plus an hourly
UTC stop-only schedule. There is no automatic start. Compute scheduling can lag
15 minutes and neither its actual execution nor cloud billing has been observed.
The CLI conservatively reserves 1.25 hours per session in its private ledger; the
example 80-hour ceiling is a proposed costed usage assumption, not owner-approved
hours or a hard financial cap. The same worksheet supports either a newly approved personal foundation or the
incremental BDUK cost on platform-provided resources.

| Line item | Price/usage inputs | Estimate |
| --- | --- | --- |
| Access VM | Approved machine/zone, hourly rate `p_vm`, running hours `h_vm` | `p_vm × h_vm`; stopping saves compute but retains its boot disk. |
| VM boot disk | 10 GiB `pd-balanced`, regional GiB-month price `p_disk`, retained month fraction `f` | `10 × p_disk × f` plus separately selected snapshots. |
| Cloud Run requests | Active vCPU-seconds `s_cpu`, GiB-seconds `s_mem`, request count `n`, corresponding rates | `s_cpu × p_cpu + s_mem × p_mem + n × p_request`; any free allowances are a separately verified adjustment. |
| Firestore | Reads `r`, writes `w`, deletes `d`, billed index reads, storage GiB-month `g_db` and regional rates | `r × p_read + w × p_write + d × p_delete + g_db × p_db`; transaction retries and read-back verification add operations. |
| Firestore recovery | PITR GiB-month/backup or restore operations and approved retention | Add the enabled PITR and separately configured backup/export/restore SKU charges. |
| Private backup bucket | Retained/versioned GiB-month, storage class/region, operations and transfer | `g_backup × p_backup + operation + transfer charges`; the Terraform bucket is not proof of an executed backup job. |
| Artifact Registry | Current and rollback image GiB-month, transfer and any enabled scanning | `g_images × p_registry + transfer/scan charges`; include retained earlier digests. |
| Cloud DNS | Two private zones when personal network is created, query volume | `zones × p_zone + queries × p_query`. |
| Cloud Logging | Ingest GiB, retention beyond included period and selected logs bucket policy | `g_logs × p_ingest + retention charges`; exclude secrets/payloads before ingestion. |
| Network | Region/source/destination, internet or inter-region transfer where selected | Actual transfer SKU × measured/estimated GiB; no NAT/LB fee assumed because neither is in the baseline. |
| Initial build/publication | Local Docker work; approved registry upload and first data/state provisioning | Local compute is outside GCP billing; price cloud uploads/operations and bootstrap explicitly. |

The example runtime has zero minimum instances, at most two instances, one vCPU,
2 GiB and bounded requests. These are sizing inputs, not a total spend cap. The
access VM, disks, image store, Firestore/PITR, private bucket, DNS and logs retain
cost independently of request traffic. The pilot duration is a recorded operating
deadline; no scheduled teardown is claimed unless actually configured and tested.

Before approval, replace each variable with an observed SKU/rate and a numerical
usage assumption. Include initial and monthly totals, a maximum usage scenario,
retained-resource total after stopping, currency, source date and any unresolved
line item. A null line item cannot be silently treated as zero. The approval card
must show the dated resulting totals and operating envelope.

## Illustrative London baseline, priced on 5 October 2026

These are observed official **Default USD** prices for `europe-west2`, followed by
explicit workload assumptions. They are a costed illustration, not the selected
account's billing-currency quote or permission to deploy. Gross prices exclude
unverified credits/free allowances. The sanitised source extracts, response hashes,
exact arithmetic and scenarios are retained in
`artifacts/gcp/costs-illustrative-london-2026-10-05.json`.
The source review ZIP excludes ignored artifact files, including that local
worksheet evidence. Review and bind a separately sanitised cost worksheet before
any deployment approval; do not assume its presence in the source package.
The documented illustration does not establish the selected billing currency.

The illustration spans 88 days (2,112 hours), using 730 hours for pro-rated monthly
storage. Recalculate from the actual approved start/end timestamps. It assumes one
`e2-micro`, its 10 GiB balanced boot disk, two private DNS zones, 1 GiB of registry
layers, 1 GiB of private backup objects, 0.01 GiB average evidence/index/PITR
storage, 10,000 Firestore reads, 1,000 writes, 10,000 DNS queries and 1 GiB of logs.
Cloud Run has one vCPU, 2 GiB and zero minimum instances; the example includes
1,000 requests and 3,000 billable active seconds in total, including an illustrative
startup allowance. Actual cold starts and billed image bytes must be measured.

| Item | Observed USD rate | 88-day illustrative cost, USD |
| --- | --- | ---: |
| Always-on London `e2-micro` | 0.010791945/hour | 22.7926 |
| 10 GiB `pd-balanced` disk | 0.12/GiB-month | 3.4718 |
| Two private DNS zones | 0.20/zone-month, first 25 zones | 1.1573 |
| Registry layers, 1 GiB | 0.10/GiB-month, without deducting the account-wide free allowance | 0.2893 |
| Private Standard backup objects, 1 GiB | 0.023/GiB-month | 0.0665 |
| Firestore storage plus PITR, 0.01 GiB | 0.117 + 0.18/GiB-month | 0.0086 |
| Firestore 10,000 reads and 1,000 writes | 0.039 and 0.117 per 100,000 documents | 0.0051 |
| Cloud Run example | 0.0000336/vCPU-second + 0.0000035/GiB-second + 0.40/million requests | 0.1222 |
| DNS 10,000 regular queries | 0.40/million | 0.0040 |
| Logs, 1 GiB ingestion, gross | 0.50/GiB; first 30 days included | 0.5000 |
| **Priced subtotal** | **Excludes the unresolved items below** | **28.4173** |

The subtotal excludes unverified transfer/network telemetry, vulnerability
scanning, tax, billing conversion and any later identity/secret-store charges.
It also excludes continuing retained charges after the period. Those are unresolved
line items, not assumed zero. A completed approval plan must price or justify each
of them and include retained charges within the total envelope.

For a £20 **total** envelope, this subtotal alone requires a billing conversion of
at most **£0.7038 per USD** before all unresolved costs. The following conversion
values are sensitivity assumptions, not exchange-rate observations:

| Illustrative GBP per USD | Always-on priced subtotal in GBP, before tax and unresolved costs |
| ---: | ---: |
| 0.70 | 19.89 |
| 0.75 | 21.31 |
| 0.80 | 22.73 |

Always-on operation is a comparison scenario; the current personal draft is
on demand. The always-on scenario is not established to fit £20. Do not approve it
using a convenient assumed exchange rate, promotional balance or alerts-only
budget. London is not an eligible US `e2-micro` free-tier region.

A **scenario** with 176 VM running hours (two hours on each of 88 days) has a priced
subtotal of **USD 7.5241**; 80 running hours has **USD 6.4881**. The disk/DNS/storage
remain present throughout. The 80-hour case is the proposed draft usage ceiling;
it is not an additional budget granted by the owner. The cost evidence predates
the executable on-demand controls and records scenarios rather than deployed
scheduling. `connect` now requires the recorded `connect-start-stop-owned-vm`
action, starts only the owned bridge, and attempts its stop after normal exit,
Ctrl-C, timeout or error. `apply` also stops it after bootstrap/error cleanup.
Its one-hour session ceiling plus possible 15-minute scheduling delay explains
the cooperative 1.25-hour ledger reservation; the hourly stop may shorten a
session. Any failed stop or schedule invalidates an assumption of bounded running
hours until corrected and observed. The local ledger is not an authoritative
cloud quota and can be bypassed outside this CLI.

The **USD 6.4881** priced subtotal remains before unresolved FX/tax/transfer,
identity/secret costs and later retention. Verify the selected billing-currency
quote and these extras, then present the exact resource/hours/total-cost plan for
approval. Do not infer that it fits the £20 total envelope. No VM exists here and
no running hours or incurred charge has been observed.

After operational removal, retaining 1 GiB of registry images, 1 GiB of backup
objects, 0.01 GiB of evidence/PITR and 1 GiB of logs beyond 30 days costs an
illustrative **USD 0.1360/month**, excluding operations/transfer. If the VM is merely
stopped while its 10 GiB disk and two DNS zones remain, that retained illustration
rises to **USD 1.7360/month**. Actual `destroy` may remove images/DNS/disks; inspect
its retained inventory instead of assuming either scenario. Protected evidence and
backup storage continue until the separately approved disposal decision.

## Official pricing references

The following official pages returned HTTP 200 on **5 October 2026**. That is a
read-only source observation, not validation of a selected project's billing
currency, discounts or regional SKU quote. Dynamic pricing tables include multiple
regions/consumption models; copy the selected rows and basis into the private plan.

- [Cloud Run](https://cloud.google.com/run/pricing)
- [Compute Engine, including London E2 shared-core tables](https://cloud.google.com/products/compute/pricing/general-purpose)
- [Persistent Disk pricing](https://cloud.google.com/compute/disks-image-pricing)
- [Firestore](https://cloud.google.com/firestore/pricing)
- [Artifact Registry](https://cloud.google.com/artifact-registry/pricing)
- [Cloud Storage](https://cloud.google.com/storage/pricing)
- [Cloud DNS](https://cloud.google.com/dns/pricing)
- [Logging and observability](https://cloud.google.com/products/observability/pricing)
- [Google Cloud pricing calculator](https://cloud.google.com/products/calculator)
- [Budgets and alerts](https://docs.cloud.google.com/billing/docs/how-to/budgets)

A standard Google budget alerts; it does not impose a hard spending cap. The
schema's `budget_is_alert_only` records that limitation. Any financial stop,
resource schedule or quota must be explicitly implemented, approved and observed
before it is described as protection.

## Stop, roll back and destroy

Closing the managed tunnel stops that laptop route and invokes owned-VM stop
cleanup. If `connect` reports `STOP_BLOCKED`, inspect `status` immediately; do not
rely on an unobserved scheduled fallback. Stopping/removing the VM or reducing
request traffic has a different resource and billing effect. Revoking a transport
binding and changing application identity/policy are separate operations.

Rollback selects the recorded compatible image/bundle/policy release and
re-verifies evidence. It must not reinitialise/delete Firestore, refill quotas,
adopt corrupt state or pretend an old cached result was freshly retrieved. Keep
the prior approved image and manifest long enough to execute the rollback; that
retention is a costed choice.

`destroy` produces/requires an explicit destructive plan targeting owned pilot
resources. A fresh destructive approval has a seven-day review window and is
allowed after the operating pilot expires. Deployment/access approval expires by
the explicit pilot end and at most 90 days after its decision; it is not deletion
authority. The baseline protects the named evidence database and backup bucket
from destruction, keeps versioned backup objects and leaves APIs enabled. Cloud
Run deletion protection must be deliberately handled within the reviewed plan.
State removal is not resource deletion. A separately approved retention decision
is required before deleting retained evidence/backups or changing those
protections; never remove a lifecycle guard just to make a command succeed.

| Resource | After default operational removal | Required follow-up |
| --- | --- | --- |
| Cloud Run service/revisions | Planned removal of owned service | Verify service/revision state and invocation binding removal. |
| Personal VM and boot disk | Planned owned VM removal; confirm disk deletion flag | Read actual disk inventory; retained disks/snapshots still bill. |
| Personal firewall/DNS/network | Only owned infrastructure eligible | Confirm no unrelated dependants; inspect retained DNS zones/routes. |
| Firestore database/evidence/PITR | Retained and protected | Report size/cost/retention owner; approved separate deletion/disposal decision. |
| Private backup bucket/versions | Retained and protected; no force destroy | Report object/version counts, retention and charges; separate reviewed disposal. |
| Artifact Registry images | As recorded in the destroy plan | Confirm whether repository/images remain; do not assume tagged-image removal deletes untagged layers. |
| Logs/audit/backups | Retention may outlive runtime | List log buckets/sinks/snapshots/PITR and their retention/cost. |
| APIs, project and billing attachment | Kept | Do not disable shared APIs, detach billing or delete a project as a shortcut. |
| Local config/state/plans | Owner-private artefacts | Retain the needed audit/approval evidence securely; dispose of local credential-bearing material through the owner's normal process. |

Run `status` after the approved change and retain the observed resource inventory.
Hosted rollback and deletion have not been exercised by local/mock tests. No
actual incurred GCP charge is asserted until billing/resource readback establishes
it; inspect Billing reports/export where the authorised account permits access.
