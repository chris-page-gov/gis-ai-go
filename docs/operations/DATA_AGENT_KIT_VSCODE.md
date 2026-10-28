# Google Cloud Data Agent Kit in VS Code

Work item: [issue 188](https://github.com/chris-page-gov/gis-ai-go/issues/188).
Owner: repository owner; protected-machine installation and Google access remain
with that environment's administrator. Sources reviewed: 27 October 2026.

## Scope and observed status

This prepares the **client environment** for exploring a public OKF projection in
Google Knowledge Catalog. It does not import OKF, create an MCP server, deploy the
unmerged GCP pilot, enable services or establish protected-data rights.

| Item | Recorded state |
| --- | --- |
| Repository | `chris-page-gov/gis-ai-go`; confirmed by owner |
| Workspace recommendation | `GoogleCloudTools.datacloud` |
| Workspace notebook execution setting | Explicitly disabled |
| Existing personal GCP project | Reuse the owner's existing local configuration; exact ID is not present here |
| Current executor | Cloud checkout; no desktop terminal, `code`, `gcloud` or configured GCP identity |
| Desktop extension/version/sign-in | Not observed |
| Knowledge Catalog service selection and permissions | Not observed |
| OKF projection and authenticated retrieval | Not performed |

The older branch's [personal example](https://github.com/chris-page-gov/gis-ai-go/blob/75ddaebd9c92c810579619ad949415ad44aee710/infra/gcp/environments/personal/config.example.json)
leaves account/project values empty. Its private configuration is not available in
this checkout. Do not infer a project ID from a repository or display name, create
a replacement project, or copy personal sign-in state to a protected machine.

## Portable workspace configuration

- [Extension recommendation](../../.vscode/extensions.json): suggests the official
  Google extension; it neither installs nor pins a version.
- [Workspace settings](../../.vscode/settings.json): sets the documented
  `google.datacloud.executeCellToolForNotebookMCP` to `false`. This disables that
  notebook execution capability, not every possible mutating tool or terminal action.
- [Offline preflight](../../scripts/data_agent_kit_preflight.mjs): checks these files
  and, optionally, local prerequisite/version evidence. It makes zero cloud calls,
  writes no configuration and never starts a login, installer or subprocess.

Google documents project/region and service selection through its settings UI.
No undocumented JSON keys for those controls are supplied. Account, project,
region, proxy and credential settings remain local to each approved environment.

From the repository root, check the portable files with the repository's pinned
Node.js baseline (`24.19.0`):

```sh
node scripts/data_agent_kit_preflight.mjs --workspace-only
```

A pass proves only the checked workspace files. Standard output explicitly leaves
desktop sign-in, project/permissions and catalogue retrieval `not-evaluated`.
Exit codes are `0` for the selected scope passing, `1` for invalid arguments and
`2` for missing or mismatched prerequisites. The local preflight checks whether
CLIs are present on PATH; it does not prove that they run or that the extension's
UI or MCP tools are functioning. Exercise those steps below.

## Command-line-first personal setup

Run these from the terminal in the intended VS Code clone. Retain the existing
coding assistant; Data Agent Kit supplies data integrations. Use a separate VS
Code profile if preferred. Replace the uppercase placeholders with verified local
values. The commands are single-line so they work in PowerShell and POSIX shells.
The commands below have been checked against the official references; they have
**not** run against the owner's desktop or Google project in this cloud executor.

### Inspect the existing configuration

```sh
git remote -v
code --version
gcloud version
node --version
gcloud config configurations list
gcloud config get-value account
gcloud config get-value project
gcloud config get-value compute/region
gcloud config get-value dataplex/location
gcloud config get-value billing/quota_project
gcloud config get-value auth/impersonate_service_account
```

Keep the output private and record the active configuration name before changing
anything. Install missing tools through the approved software route. For macOS,
VS Code's command palette can install the `code` shell command. A missing CLI does
not prove the desktop application is absent.

If necessary, select the configuration already used for the earlier personal GCP
work, then recheck its account and project:

```sh
gcloud config configurations activate EXISTING_CONFIGURATION
gcloud config get-value account
gcloud config get-value project
```

If no verified existing project is found, stop project-specific commands and
recover the old private `artifacts/gcp/personal-config.json` or the actual project
ID. Do not create a new project to make setup pass. An unset region is not evidence
of a catalogue location.

### Check access without changing cloud resources

These are read-only cloud requests. Keep them bounded, use the exact project and
do not enable HTTP body logging:

```sh
gcloud projects describe EXISTING_PROJECT_ID --format="value(projectId,lifecycleState)" --quiet
gcloud billing projects describe EXISTING_PROJECT_ID --format="value(billingEnabled)" --quiet
gcloud services list --enabled --project=EXISTING_PROJECT_ID --filter="config.name=dataplex.googleapis.com" --format="value(config.name)" --limit=1 --quiet
```

An empty service result means the enabled API was not observed. An access-denied
error means that this identity could not inspect the state; neither result grants
permission to enable billing or a service. Billing inspection may need an
administrator even when catalogue reads are allowed.

If local CLI properties are missing or incorrect, set only verified values:

```sh
gcloud config set project EXISTING_PROJECT_ID
gcloud config set compute/region APPROVED_REGION
gcloud config set dataplex/location CATALOGUE_LOCATION
```

These commands change local defaults, not the underlying project or catalogue.
`CATALOGUE_LOCATION` must match the entry group; it may differ from the compute
region. Preserve the previously approved quota/billing context. A
`billing/quota_project` property identifies quota attribution, not a billing-account
attachment or spending ceiling.

Only if the existing credential is missing or the account is incorrect, run:

```sh
gcloud auth login EXISTING_PERSONAL_ACCOUNT
gcloud auth application-default login
```

Choose that same approved account in the ADC browser flow. These commands open
local authorisation prompts and write credentials to Google's local facilities.
ADC is separate from the active gcloud configuration; ADC login replaces any
existing local ADC. Preserve an approved impersonation setup rather than replacing
it with personal credentials. If the agreed existing project needs quota
attribution for ADC, use `gcloud auth application-default set-quota-project
EXISTING_PROJECT_ID`; that changes local ADC and requires the relevant service
usage permission. These are not unattended steps. Do not print access tokens, export credentials or
copy login state into the repository. Reuse working credentials rather than
repeating sign-in.

### Install the approved extension from the CLI

Use the exact version approved for this environment:

```sh
code --install-extension GoogleCloudTools.datacloud@APPROVED_VERSION
code --list-extensions --show-versions
```

The official extension is published by Google in the
[Marketplace](https://marketplace.visualstudio.com/items?itemName=GoogleCloudTools.datacloud).
There is no tested desktop extension version in this executor. Select a reviewed
exact release through the organisation's software process; do not install a
changing `latest` or substitute the separate CLI plugin's version. The version
capture section below records the installed baseline for the protected machine.

### Finish the extension-specific controls

Three controls remain in Google's documented extension UI:

1. Run **Google Cloud Data Agent Kit: Sign in** and complete its local browser
   flow if not already signed in. A successful gcloud login alone does not prove
   extension sign-in. Browser, trust and operating-system prompts need the operator.
2. Under **Settings → Settings → Common**, synchronise the verified existing
   account, project, region and billing context with the CLI. If a mismatch warning
   is shown, Google documents using its sync control. Check the direction of sync
   so stale extension settings do not overwrite the intended CLI configuration.
3. Under **Settings → Settings → Service Integrations**, select **Knowledge
   Catalog** only. Review and copy any **Missing permissions** list for the
   administrator; this procedure sends no email and does not automatically enable
   additional services.

No supported `gcloud data-agent-kit` command or equivalent VS Code settings keys
for these controls were established by the reviewed documentation. The separate
CLI plugin's setup script configures that plugin, not the IDE extension; it is
not used as an undocumented workaround.

Review the coding assistant's configured MCP servers and confirmation controls.
Enable only the required discovery tools. Data Agent Kit supports the managed
`https://dataplex.googleapis.com/mcp` endpoint; no custom Cloud Run deployment is
needed for discovery.

### Administrator commands if prerequisites are missing

The minimum client permissions are appropriately scoped
`roles/dataplex.catalogViewer` and project-level `roles/mcp.toolUser`. The
following are **cloud changes**, not part of the offline preflight. Run only the
missing, authorised operation using the actual target and principal; do not paste
this block as a blanket setup script:

```sh
gcloud services enable dataplex.googleapis.com --project=EXISTING_PROJECT_ID --quiet
gcloud projects add-iam-policy-binding EXISTING_PROJECT_ID --member=APPROVED_PRINCIPAL --role=roles/mcp.toolUser --condition=None --quiet
gcloud dataplex entry-groups add-iam-policy-binding OKF_ENTRY_GROUP --project=EXISTING_PROJECT_ID --location=CATALOGUE_LOCATION --member=APPROVED_PRINCIPAL --role=roles/dataplex.catalogViewer --quiet
```

Use a member such as the actual `user:` or approved `serviceAccount:` principal.
The entry group must already exist; creating/importing it is a separate task.
This viewer binding grants catalogue visibility for that entry group; it does not
remove broader access granted elsewhere. Verify existing grants before claiming
group-only visibility. Exact-group requests limit retrieval scope, not IAM rights.
If a wider search cannot operate under that scope, retain the scoped grant and
test exact-group listing rather than broadening access automatically. Do not grant
catalogue administration or data-product mutation merely to inspect metadata.

Data Agent Kit documents signed-in user credentials and service-account
impersonation. If using an existing approved impersonated account, ensure both the
extension's actual MCP path and gcloud/ADC use the intended identity; setting a
gcloud property alone is not evidence that the extension follows it. This setup
does not provision a distinct Google Agent Identity. Do not create service-account
keys or copy ADC files into the repository.

## Capture and reproduce exact software versions

Keep the version evidence local. `artifacts/` is ignored and excluded from the
repository's baseline scanner; it is not a secret store. Store actual credentials
in the platform's credential facilities outside the checkout.

In PowerShell:

```powershell
New-Item -ItemType Directory -Force artifacts/data-agent-kit | Out-Null
code --version > artifacts/data-agent-kit/vscode-version.txt
code --list-extensions --show-versions > artifacts/data-agent-kit/extensions.txt
gcloud version > artifacts/data-agent-kit/gcloud-version.txt
node --version > artifacts/data-agent-kit/node-version.txt
```

In a POSIX shell:

```sh
mkdir -p artifacts/data-agent-kit
code --version > artifacts/data-agent-kit/vscode-version.txt
code --list-extensions --show-versions > artifacts/data-agent-kit/extensions.txt
gcloud version > artifacts/data-agent-kit/gcloud-version.txt
node --version > artifacts/data-agent-kit/node-version.txt
```

Record the exact `GoogleCloudTools.datacloud@X.Y.Z` version from that inventory.
Replace `APPROVED_VERSION` below with the recorded, approved numeric version:

```sh
code --install-extension GoogleCloudTools.datacloud@APPROVED_VERSION
node scripts/data_agent_kit_preflight.mjs --extension-list artifacts/data-agent-kit/extensions.txt --extension-version APPROVED_VERSION
```

The first command installs software and can open local trust/network prompts.
The second is offline and can be repeated. Keep extension auto-updates under the
protected machine's software policy; a later version needs a new recorded check.
Match the active VS Code profile when capturing/installing (use the supported
`--profile` option if necessary). In a remote workspace, verify **Developer:
Show Running Extensions** and the Extensions view's local/remote grouping. Install
and authenticate on the host where the extension actually runs; do not force
`remote.extensionKind` to work around placement problems.

## Protected-machine reproduction

1. Transfer only the reviewed Git revision and approved software packages. Install
   the recorded VS Code, extension and SDK versions through the organisation's
   approved route. If Marketplace access is unavailable, obtain the approved VSIX,
   record its SHA-256 and verify the transferred file before installation. Use
   `Get-FileHash -Algorithm SHA256 APPROVED.vsix` on Windows or the approved
   platform checksum tool. `code --install-extension APPROVED.vsix` installs the
   local package. No VSIX or downloaded SDK belongs in this repository.
2. Use the protected machine's own approved identity, project, region and network
   configuration. Do not reproduce the personal account login there. Follow the
   command-line sequence and only the three remaining extension-specific UI
   controls, limiting service selection to Knowledge Catalog.
3. Have the administrator verify access to the extension distribution/sign-in
   services and the selected Google APIs, including `dataplex.googleapis.com`.
   Obtain the exact required hosts from the approved package and authentication
   path. Do not disable TLS verification, bypass a proxy or assume a generic
   wildcard is a sufficient enterprise network configuration.
4. Repeat version capture and offline preflight. Keep account/project/IAM output,
   network diagnostics and screenshots in approved private storage.
5. Before an AI-assisted test, confirm the intended assistant and recipient are
   approved for the selected material. Use public or synthetic OKF records for the
   initial check. Installing an extension does not authorise licensed feature
   payloads or protected documents to be transferred to an AI service.

## Actual acceptance and rollback

After the OKF projection exists, the Google API can first be checked from the CLI
with one exact-group list and one known entry lookup:

```sh
gcloud dataplex entries list --entry-group=OKF_ENTRY_GROUP --location=CATALOGUE_LOCATION --project=EXISTING_PROJECT_ID --limit=5 --page-size=5 --format=json --quiet
gcloud dataplex entries lookup EXACT_ENTRY_ID --entry-group=OKF_ENTRY_GROUP --location=CATALOGUE_LOCATION --project=EXISTING_PROJECT_ID --view=all --format=json --quiet
```

For a search test with an approved keyword and project-wide search permission:

```sh
gcloud dataplex entries search OKF_KEYWORD --project=EXISTING_PROJECT_ID --scope=projects/EXISTING_PROJECT_ID --limit=5 --page-size=5 --format=json --quiet
```

Always set `--scope`; otherwise Google documents an organisation-wide default.
Five results bound output, not a guaranteed number of HTTP requests or a cost
ceiling. `lookup --view=all` returns at most 100 aspects; verify the intended
record's aspect count before treating it as complete. CLI API success is separate
from MCP acceptance. Do not fabricate a `gcloud` command for MCP tool discovery.

The subsequent MCP check is bounded: one tool discovery, one search limited to
five results and one exact entry lookup within the agreed OKF entry group. Confirm
IDs, source references, rights, dates and explicit limitations survive retrieval.
Only run it after an OKF projection exists. An empty catalogue is not an import
failure if this task has not imported anything. Catalogue import remains separate
work; do not load the 30,876-record corpus as an installation test.

Record privately: Git commit; operating system; extension host; VS Code, Node,
extension and gcloud versions; actual project/region/effective identity; allowed
tools; observed discovery/search/lookup; denied-access result using an existing
unprivileged test identity if available; and any exact blocker. Do not create a
new identity or change access to fabricate a negative test. Logs containing an
agent name are not proof of a separately authenticated Agent Identity.

To roll back the client setup, deselect Knowledge Catalog, disable the extension
for the workspace/profile, or remove the two introduced workspace files when
reverting this change. Restore any locally changed gcloud configuration from the
private pre-change record. A client rollback neither revokes OAuth authorisation
nor removes cloud IAM grants or API enablement; handle any such changes through
their separately recorded administrator procedure.

## Source verification on 27 October 2026

On the cloud executor, Node.js `24.19.0` passed both JavaScript syntax checks,
seven offline preflight tests and the workspace-only CLI check. The first test
run used `--test-isolation=none` because the sandbox rejected Node subprocesses
with `EPERM`. Subsequent approved execution passed the canonical
`pnpm run test:data-agent-kit-setup` command with normal test isolation.
Local link/research-integrity, changelog, secret/machine-path, manifest-version and
whitespace checks passed. Independent review corrected an additive-IAM explanation.

Initial CI at `4397d6aa` found the deterministic QUAL-206 receipt set's package
manifest binding stale after the test command was added. The existing
`pnpm run generate:qual-206-local-evaluations` rebuilt and ran its fixture suites,
regenerated the set and passed seven receipt-contract tests. Only the package
hash and derived set identity changed; all receipt contents and non-live/unscored
claims remain unchanged. The dependency lock files were not changed. The host
launcher reported pnpm `11.19.0`; the repository's declared `10.33.2` baseline
remains unchanged, and full canonical CI on the repaired source is still required.

The local-prerequisites CLI returned exit `2`, correctly recording missing `code`,
`gcloud` and exact extension-version evidence. No desktop or live Google acceptance
is inferred from the passing source checks. The Google commands in this guide are
documented instructions, not a record of execution.

## Source register

- [Google installation and sign-in](https://docs.cloud.google.com/data-agent-kit/install)
- [Google project/region configuration and notebook setting](https://docs.cloud.google.com/data-agent-kit/configure)
- [Google CLI/extension settings synchronisation](https://docs.cloud.google.com/data-agent-kit/troubleshooting)
- [Google required roles and APIs](https://docs.cloud.google.com/data-agent-kit/permissions)
- [Google MCP integrations and impersonation](https://docs.cloud.google.com/data-agent-kit/use-mcp-servers)
- [Knowledge Catalog managed MCP](https://docs.cloud.google.com/knowledge-catalog/docs/use-remote-mcp)
- [VS Code CLI version selection and inventories](https://code.visualstudio.com/docs/configure/command-line)
- [VS Code remote extension placement](https://code.visualstudio.com/docs/remote/ssh#_managing-extensions)
- [gcloud local configuration](https://docs.cloud.google.com/sdk/gcloud/reference/config/set)
- [gcloud ADC login](https://docs.cloud.google.com/sdk/gcloud/reference/auth/application-default/login)
- [gcloud ADC quota project](https://docs.cloud.google.com/sdk/gcloud/reference/auth/application-default/set-quota-project)
- [gcloud API inspection](https://docs.cloud.google.com/sdk/gcloud/reference/services/list)
- [gcloud project billing inspection](https://docs.cloud.google.com/sdk/gcloud/reference/billing/projects/describe)
- [gcloud scoped entry-group IAM](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/entry-groups/add-iam-policy-binding)
- [gcloud exact-group listing](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/entries/list)
- [gcloud project-scoped search](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/entries/search)
- [gcloud entry lookup and aspect limits](https://docs.cloud.google.com/sdk/gcloud/reference/dataplex/entries/lookup)

These are dated product references, not a claim that the desktop or cloud setup
has passed. Do not use a changing `latest` package as a reproducibility baseline.
