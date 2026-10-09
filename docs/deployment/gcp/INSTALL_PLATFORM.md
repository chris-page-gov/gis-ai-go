# Install on the BDUK GCP sandpit

Use `scripts/gcp/install-platform.sh` on an approved Linux/WSL build or operator
machine containing this reviewed repository increment. It is one entry script
over the existing approval-bound deployment lifecycle. Copying only the script
is insufficient: it needs the runtime, infrastructure, locks and admitted public
metadata from the repository or reviewed source-replay package.

On the secure machine, full source/security review and the exact development/build
image's scan, SBOM, provenance and platform admission must pass **before** running
any repository script (including `--help`), installing dependencies, building or
opening a container, or trusting the updated workspace. Read
[the secure transition workflow](../../development/SECURE_TRANSITION.md) first.
The published branch and earlier local tests do not establish this approval.
The [current source/image assurance status](../../development/BUILD_ASSURANCE.md)
blocks secure-machine execution, packaging and deployment until its findings
and exact admission gates are resolved.

The target is ordinary Cloud Run with internal ingress on the approved BDUK GCP
network, the current website/workbench, both OKF evidence surfaces and the custom
Streamable HTTP MCP server. This profile consumes existing platform network,
registry, runtime/invoker identities, Firestore and backup storage. It creates no
personal tunnel VM. Joining the private network, authenticating Cloud Run transport,
authenticating the human through Okta and authorising a tool are distinct checks.

## Clone through GitHub

The secure machine already has an older clone in VS Code. Use GitHub to fetch
the implementation into that clone for review, with the workspace kept restricted:

```sh
git status --short --untracked-files=all
git remote get-url origin
git fetch --no-tags origin codex/gcp-private-pilot
git rev-parse FETCH_HEAD
git show --stat --oneline FETCH_HEAD
git diff --stat HEAD FETCH_HEAD
```

Confirm the remote is `chris-page-gov/gis-ai-go`, record the full fetched commit
and compare it with the actual source review/approval. The published installer
baseline is `78ab9b2828b4c713ca467d38a77ffa3db2f03ab9`; later changes need their
own reviewed published commit. Before switching, stop for dirty work or divergence;
do not automatically stash/reset/clean. The
[transition guide](../../development/SECURE_TRANSITION.md#preserve-edits-and-switch-only-after-sourceimage-approval)
gives the existing/new local branch and fast-forward commands after approval.
`main` keeps its existing release. The implementation branch carries local test
evidence and outstanding canonical/hosted gates; cloning it does not approve
deployment. No chat ZIP overlay is needed for this route. Private configuration,
credentials, state, approved plans and built images remain outside Git.

If external package registries cannot be reached from the secure machine, provide
the pinned tools/dependencies through the platform's approved internal mirrors
or existing build environment before review. A Git clone supplies source and
locks; it does not supply Docker images, npm/uv caches or Terraform provider
binaries. The script never opens additional internet access automatically.

## 1. Prepare the approved operator machine

Complete the source/image admission above before these execution steps. A secure
development container and a platform builder are separate reviewed boundaries:
the former does not gain a host Docker socket to satisfy a builder prerequisite.
Use the approved builder with an immutable internal image, registry/mirrors,
proxy and CA trust, and keep `gcloud`/credentials on the approved operator host.
Do not mount a host home, credential directory or protected BDUK workbench.

Provide Bash, Python 3.12+, Node 24.19.0+ and pnpm 10.33.2; the repository's uv
lock workflow; Terraform 1.13.4 and its locked Google 6.49.0 provider; a Docker
Buildx builder capable of OCI export; `skopeo` and the platform-supported Google
Cloud CLI. Use platform-approved package mirrors, proxy and certificate trust.
The script does not install system tools, weaken TLS, start a login or upload source.

From the reviewed repository root, install the frozen dependencies through that
approved route:

```sh
pnpm install --frozen-lockfile --ignore-scripts --package-import-method=copy
uv sync --locked --group dev --cache-dir .uv-cache
```

Retain the actual working tree. Do not reset it to the public GitHub checkpoint.
The secure machine uses the complete reviewed GitHub source; a chat ZIP is not
its transfer route. On another explicitly approved source-replay route, follow
`SOURCE_REPLAY.md` before applying the reviewed overlay. Local tests are available through
`pnpm run test:gcp`; they cannot establish hosted BDUK acceptance.

## 2. Create and complete a private configuration

```sh
./scripts/gcp/install-platform.sh init
./scripts/gcp/install-platform.sh inputs
```

`init` exclusively creates `artifacts/gcp/bduk-sandpit.json` with mode 600 and
refuses to overwrite any existing file. It generates only a draft store nonce,
creation time and available local Git revision. It grants no authority and leaves
platform/account/billing/identity/spend inputs unresolved. This draft is for a new
store scope; reuse the actual recorded identity when configuring an existing
evidence store. The default configuration uses no personal project, account,
budget, pilot duration or VM authority from the earlier personal plan.

Edit the JSON using your platform-approved editor and custody rules. Put approved
resource names and secret **references** in the file, never passwords, tokens,
client-secret values or downloaded keys. `inputs` lists unresolved field names
without cloud requests; a schema error or null prerequisite blocks installation.

| Area | Exact fields requiring platform inputs |
| --- | --- |
| Project/billing | `project.id`, `number`, `expected_account`, `billing_account`, `region`, `billing_currency`, `billing_currency_evidence` |
| Authority/cost | `authority.platform_approval_reference`, `spend_envelope`, `pilot_end`; dated initial/monthly/total/retained costs and ceilings in the billing currency |
| Private network | `network.vpc_id`, `subnet_id`, `shared_vpc_host_project`, `transport_principals`; keep `access_mode: platform-approved-private-network` and both VM flags false |
| Transport/runtime | `identity.runtime_service_account`, `transport_service_account`, `transport_subject` (actual unique subject), approved publisher/invoker permissions |
| Human/API identity | `identity.oidc_issuer`, `resource_audience`, `jwks_uri`, `client_id`, `claims_mapping.subject_roles`, `group_attribute_mapping.claim` and `.roles` |
| Browser SSO | `identity.browser` with the exact approved registration, redirects, endpoints, scopes and numbered secret references described below |
| Stored evidence | Existing `state.evidence_store.database_id`/`collection`, `bundle_store.backup_bucket_name`, `retention_policy`, and the actual store nonce/date/software revision |
| Build/release | `operations.image_repository`, approved build/registry route and the immutable locally prepared source/image/bundle/policy identities |

`project.billing_currency_evidence` points to a private JSON observation containing
`billing_account`, `currency`, `observed_at` and `source`. It is metadata, not a
credential. See [costs](COST_AND_TEARDOWN.md) and the schema for the complete cost
envelope; do not substitute illustrative USD figures for the platform's quote.

The approved browser object contains these keys:

```text
client_id
client_auth_method             none or client_secret_basic, as registered
callback_url                   exact approved HTTPS origin + /auth/callback
allowed_redirect_uris          approved exact callback URLs
allowed_endpoints              exact approved discovery/authorisation/token/JWKS URLs
scopes                         approved subset including openid
session_seconds                300
session_key_secret             {resource: projects/.../secrets/..., version: numbered version}
client_secret                  matching numbered secret reference, or null for registered public client
```

The platform provides the actual application-level Okta registration and approved
identity HTTPS egress independently of the Google private API path. No workforce
federation, organisation policy or Okta application is created automatically.
Role mappings must match the source-bound manifest
`infra/gcp/policy/gcp-public-metadata.v1.json`; unknown subjects/attributes deny.
An invoker service account cannot replace the real human subject.

## 3. Build and obtain the review package

```sh
./scripts/gcp/install-platform.sh review
```

This performs read-only preflight, local preparation, read-only planning and
`package-approval`. A missing cloud prerequisite or local build failure does not
prevent the independent package stage. Current, fully verified preparation is
reused. Existing unverified/partial material is preserved and blocks preparation;
use a new reviewed draft configuration/release scope rather than deleting it to
force a pass or damaging historical recovery evidence.

If the approved build route is unavailable, create the actual implementation
package and record the missing image gate with:

```sh
./scripts/gcp/install-platform.sh review --skip-prepare
```

The package, plan and private run logs are under
`artifacts/gcp/<config-digest16>/`. The terminal prints stage outcomes and evidence
paths, not raw account/token responses. `installer-runs/<run-id>/summary.json`
preserves every stage; exit 2 means a gate remains blocked even if the ZIP was
created. A successful review means prepared review material, not hosted acceptance.

Review the ZIP checksum and sanitisation before transferring it. It includes the
installer, executable lifecycle, infrastructure, runtime sources, tests, policy,
locks and admitted inventory. Configuration, state, original archives and protected
data are excluded. Initial data remains public metadata and synthetic fixtures;
no live provider, model call or licensed feature path is introduced.

## 4. Record the exact platform decision, then install

Use the exact saved plan and approval template generated in the previous step.
Before the first cloud mutation, the approver reviews observed account/project
and billing, the resource/IAM diff, immutable source/config/image/policy identities,
upload inventory, complete costs, allowed actions, expiry and retention decision.
Record the approved template as its corresponding `.approval.json` according to
the [lifecycle runbook](README.md#account-and-first-cloud-change). This script never
creates, signs or infers that decision. Setting a JSON boolean is insufficient.

```sh
./scripts/gcp/install-platform.sh install --approved-plan APPROVED_PLAN_ID
```

Replace `APPROVED_PLAN_ID` with the actual 24-hex ID. Installation delegates to
the existing saved-plan verifier and checks real cloud identity. It does not
rebuild, replan or alter configuration before using the approval. Changed source,
config, content, costs, actions or expiry invalidate the scope. A valid recorded
decision is reused within that scope, including compatible recovery; the installer
does not introduce another approval prompt.

After successful apply it runs `verify` and `status`. Blocked hosted checks keep
the result blocked even when resources were created. Actual service/revision
observations and URLs are in the private `status.json`/`deployed.json`; use them
through the platform-approved private connection. `connect` intentionally refuses
to substitute a personal bastion for that connection.

## 5. Observe, recover or remove

```sh
./scripts/gcp/install-platform.sh status
./scripts/gcp/install-platform.sh verify
./scripts/gcp/install-platform.sh rollback --release APPROVED_RELEASE_ID
./scripts/gcp/install-platform.sh plan --destroy
./scripts/gcp/install-platform.sh destroy --approved-plan APPROVED_DESTROY_PLAN_ID
```

Rollback uses an existing compatible approved release and retains evidence.
Destroy needs its own exact destructive decision; it can run after pilot expiry.
It preserves protected evidence/backups, enabled APIs and platform-retained logs.
Inspect the actual retained resources and charges; do not delete the platform
project as a shortcut. Use `--config artifacts/gcp/ANOTHER_PRIVATE_CONFIG.json`
for every step when selecting a separately reviewed configuration.

All 41 [hosted acceptance requirements](ACCEPTANCE.md) remain separate from local
tests, mock plans or successful script execution. Actual Okta/role refusals,
inside/outside network proof, durable cross-revision evidence, recovery, rollback
and teardown must be observed on the approved platform.

## Observed local installer checks

The earlier 9 October 2026 installer observation passed all 20 installer tests
and the then-current 119-test focused GCP command. Shell syntax, links, secret
scanning and changelog validation also passed.
Actual CLI `init` created a mode-600 draft, `inputs` returned exit 2 for unresolved
platform fields, and `review --skip-prepare` returned exit 2 while successfully
creating the sanitised ZIP. Existing deployment/build material was retained.
These are local orchestration tests with no inherited platform credentials; no
BDUK cloud mutation or hosted acceptance occurred. Logs are under
`artifacts/gcp/platform-installer-20261009/`.

After the security remediation on the same date, `pnpm run test:gcp` passed 144
local checks: 26 runtime, 111 Python deployment and seven packaging/UI checks.
The 70 focused lifecycle checks are included in the deployment total. The
aggregate log is `artifacts/environment/gcp-223-remediation-gcp.log`, SHA-256
`6c28508660926565c4f002c0ee0f793bc5d2556ac2ff23f063d860a9f390b9ef`.
See the [sanitised security record](../../security/GCP-223-SECURITY-REVIEW.md) for
the distinct sealed audit, source-fix observations and remaining image/platform
gates. These checks do not establish hosted authentication, persistence or BDUK
acceptance.
