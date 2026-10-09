# Operate the private GCP pilot

This additive pilot hosts GIS AI GO's current website, admitted OKF and OKF+
evidence surfaces, captured-data workbench and custom Streamable HTTP MCP server
on ordinary Cloud Run. It is separate from the supported `v0.1.0` public Explorer,
existing Sites deployments and the provider-free loopback local edition. It does
not activate the deliberately blocked generic gateway entrypoints.

The initial release admits public metadata and synthetic fixtures. It has no live
provider, external model, BigQuery, licensed feature or private-original-document
path. Joining the private network and passing Cloud Run invocation authentication
are separate from establishing a human identity and passing application policy.

## Current acceptance boundary

The implementation and review package can be exercised locally. The selected project and owner spending envelope are recorded privately.
Billing/pricing verification, an approved resource plan, deployed revision and
private hosted URL remain unresolved. The initial environment preflight had no
authenticated `gcloud` session. Hosted network, real human identity, Firestore replacement,
rollback and teardown checks remain separate gates. Local identity fixtures and
storage simulations cannot pass those gates.

Read [repository discovery](REPOSITORY_DISCOVERY.md),
[architecture](ARCHITECTURE.md), [acceptance](ACCEPTANCE.md) and
[cost and teardown](COST_AND_TEARDOWN.md) before operating the pilot.
The [dated local observations](LOCAL_OBSERVATION.md) record actual checks, material
identities, remaining canonical failures and cloud prerequisites.
For the BDUK operator entry script and complete command sequence, use
[install on the secure platform](INSTALL_PLATFORM.md).

## Local preparation

Use the existing isolated checkout; preserve unrelated changes. Never reset it to
a public checkpoint to run these scripts. Keep real configuration, plan,
approval, Terraform state and result files in ignored `artifacts/gcp/`, with owner
access only. Sanitised examples are `infra/gcp/environments/personal/config.example.json`
and `infra/gcp/environments/bduk-sandpit/config.example.json`.

The repository pins Node, pnpm and uv through its existing manifests. Terraform
is pinned to `1.13.4`; the Google provider is pinned to `6.49.0`. Docker must have a
working daemon for the application image. Install dependencies through the
repository's normal frozen-lockfile workflow before preparation:

```sh
pnpm install --frozen-lockfile
uv sync --locked --group dev --cache-dir .uv-cache
```

Choose the appropriate sanitised example, copy it into the ignored private
artefact directory and fill the exact project/account, region, approved network,
identity and cost inputs. Example nulls are unresolved prerequisites and never
permission to create resources. Do not put secret values into the JSON; use
approved secret references. The schema rejects unknown properties. For the personal profile, create a new
owner-private configuration without replacing an existing file:

```sh
umask 077
mkdir -p artifacts/gcp
cp -n infra/gcp/environments/personal/config.example.json artifacts/gcp/personal.json
```

Set `policy.policy_release` to `gis-ai-go.gcp-public-metadata.v1` and
`policy.role_toolsets_manifest` to
`infra/gcp/policy/gcp-public-metadata.v1.json`. These names identify the implemented
source-bound policy; real platform group/subject mappings remain private inputs.
Fill the remaining file through your editor, then run:

```sh
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.json preflight
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.json prepare
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.json plan
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.json package-approval
```

`preflight` is read only. It distinguishes missing, denied and unknown cloud
prerequisites. `prepare` builds locally from admitted inputs, creates an explicit
build/upload inventory and records hashes. It never uploads the checkout.
`plan` describes resources, API/IAM changes, uploaded material, cost assumptions,
retention and unresolved gates; it must not enable APIs or bootstrap state.
The approval package can be produced without cloud access.

## Account and first cloud change

The owner performs any Google sign-in directly using the official `gcloud auth
login` flow and selects the exact intended personal account and project. Never
send a password, passkey, MFA code, access token or account key through chat. The
operator must re-run preflight after signing in; a remote Codex environment does
not inherit a laptop session or private route.

Before the first cloud mutation, review one private approval record containing
the observed account, project ID and number, selected billing account/currency,
exact resource and IAM plan, upload inventory, image/bundle/policy identities,
cost estimate, spend envelope, pilot end, access route and recovery action.
An unresolved billing account or budget blocks mutation. Approval binds the
reviewed inputs and expiry; changes outside that scope require a new plan.

```sh
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.json apply \
  --approved-plan APPROVED_PLAN_ID
```

The plan writes `artifacts/gcp/<config-digest16>/approvals/<plan-id>.template.json`.
After the owner approves the concrete plan, record that decision in the matching
`<plan-id>.approval.json`: `status: APPROVED`, the observed configured account as
`approved_by`, approval/expiry timestamps, and the exact plan binding and spend
scope. Deployment authority expires no later than the explicit pilot end and
90 days after the decision. An unchanged recorded scope can authorise subsequent
connections within that period. A fresh destructive approval has a seven-day
review window and can authorise cleanup after the pilot ends. Do not fabricate this record or treat template
creation as approval. An identifier alone does not grant authority. The command
checks the recorded approval and bound inputs. Application publication is part of the reviewed plan;
never manually substitute an image tag for its verified digest or upload the
whole repository using `gcloud run deploy --source .`.

## Connect and inspect

The personal VM is an on-demand private access bridge: the website, MCP and
evidence store run on Cloud Run/Firestore. No VM has been created by this local
implementation. Once deployment is approved, `apply` stops the owned VM after
proxy bootstrap, including its error cleanup. The VM has no external IP. Its
fixed-target proxy listens only on `127.0.0.1:8081`; the local tunnel listens only
on `127.0.0.1:8789`.

`connect` reuses the deployed plan's recorded approval, or the explicitly selected
`--approved-plan`, and requires its `connect-start-stop-owned-vm` action. It starts
only that owned VM, keeps the IAP SSH tunnel in the foreground for at most one
hour, then attempts to stop the VM on normal exit, Ctrl-C, timeout or error. Keep
it running while using the printed browser and MCP URLs:

```sh
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.json connect
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.json status
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.json verify
```

The URLs printed by a successful connection are local transport addresses. The
canonical Cloud Run URL remains the invocation/resource audience where specified.
The printed route is an observed connection only after the tunnel succeeds; this
document contains no invented deployed address. Closing the tunnel ends that
local access route and invokes VM stop cleanup. A stop failure is a blocked
result: inspect `status` immediately rather than assuming cleanup succeeded.
A laptop `gcloud run services proxy` command alone does not put the laptop on the
private VPC.

The personal IaC adds an hourly UTC stop schedule with no automatic start.
Compute scheduling can be delayed by 15 minutes; effective execution still needs
hosted evidence. The local CLI reserves 1.25 hours per connection in a private
ledger and refuses another connection above the configured ceiling. The example
80-hour ceiling is a proposed costing assumption, not owner-approved usage.
This cooperative ledger and stop schedule are not a hard billing cap. The stopped
VM's 10 GiB boot disk, two private DNS zones, images, evidence, backups and logs
remain chargeable. Verify billing-currency prices and the owner's total envelope
before approving the plan.

The connection supplies Cloud Run transport authentication. Personal configuration
keeps the explicit owner transport milestone. The BDUK OIDC mode validates an
independent bearer identity; its optional `identity.browser` implementation uses
pinned `openid-client` 6.8.8 through `/auth/login`, `/auth/callback` and POST
`/auth/logout`. It requires the approved client/callback/endpoint registration,
five-minute secure sessions and Secret Manager version references. The BDUK
profile blocks deployment when this registration/configuration is missing.

Actual browser Google/Okta sign-in and direct MCP OAuth client discovery/registration
require their own hosted observations. A Cloud Run invoker credential must never
be presented as the user's role or entitlement. Browser cookies are not credentials
for an independent MCP client. See the architecture for the distinct network
permissions required for approved identity endpoints.

`verify` writes machine-readable statuses and evidence. A failed or blocked
required gate yields a non-zero exit. `status` queries current resources and
revision identity rather than treating an old successful log as current health.
Keep full results owner-private; share only the scrubbed review package.

## Roll back or remove

Retain the previous compatible image, bundle and policy release and the evidence
retention decision. Rollback is an application change, not an evidence reset:

```sh
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.json rollback \
  --release APPROVED_RELEASE_ID
```

Prepare and review the explicit destructive plan before removal, then execute
only its recorded scope. An expired pilot does not prevent a fresh approved
cleanup plan:

```sh
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.json plan --destroy
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.json destroy \
  --approved-plan APPROVED_DESTROY_PLAN_ID
```

Inspect the output and `status` for retained evidence, images, disk, logs and
other chargeable resources. Do not delete an existing project as a shortcut.
Stopping Cloud Run requests or closing a tunnel does not remove VM/storage
charges. See [cost and teardown](COST_AND_TEARDOWN.md) for the retained-resource
checklist and unresolved deletion decisions.

## BDUK hand-off

Use the separate BDUK profile and state with the platform's approved network,
project, build facilities and identities. BDUK users join that network; a personal
bastion is not their access requirement. Submit the actual sanitised package and
[platform request](PLATFORM_APPROVAL.md). Personal hosting, local role fixtures
and a complete package do not constitute BDUK approval or actual Okta acceptance.
