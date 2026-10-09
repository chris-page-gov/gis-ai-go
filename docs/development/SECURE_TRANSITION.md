# Transfer reviewed source to the secure machine

The secure machine already has an older VS Code clone, and GitHub is its only
approved source-transfer route. Use that clone. A chat ZIP, a copied installer or
a prebuilt local image does not replace the reviewed repository source.

Fetching source is not permission to run it. Before executing any repository
script, installing dependencies, building or opening a development container, or
trusting the updated workspace on the secure machine, the platform must approve
the full source/security review and the exact development/build image's scan,
SBOM and provenance. Deployment, network, identity, data and spending approval
are later separate decisions. See [SECURITY.md](../../SECURITY.md).

Keep the existing VS Code workspace restricted/untrusted while reviewing. Do not
enable repository tasks, recommended extensions or a Dev Containers rebuild.
Use the platform's already approved Git client and review facilities.

## Fetch into the existing clone without executing source

In a terminal at the existing repository root, record its state and confirm the
remote is the intended repository:

```sh
git status --short --untracked-files=all
git branch --show-current
git rev-parse HEAD
git remote get-url origin
git fetch --no-tags origin codex/gcp-private-pilot
git rev-parse FETCH_HEAD
git show --stat --oneline FETCH_HEAD
git diff --stat HEAD FETCH_HEAD
git show FETCH_HEAD:SECURITY.md
git show FETCH_HEAD:docs/deployment/gcp/INSTALL_PLATFORM.md
```

The expected repository is `https://github.com/chris-page-gov/gis-ai-go.git` or
its platform-approved SSH equivalent. `chris-page-gov` is the GitHub organisation
identity; it is not a required workstation login or directory name. Do not
change another repository's remote to make these commands work.

The published installer baseline is full commit
`78ab9b2828b4c713ca467d38a77ffa3db2f03ab9`. This portability/security and
remediation increment uses the same publication branch; record the latest full
commit and its own reviewed evidence. A branch name is mutable: compare the
full fetched commit with the actual approval, not just that historical baseline.
These Git commands read/fetch source; they do not run its installer, tests or
container configuration.

Review the complete change, dependencies, scripts, container configuration,
runtime/data flows and known findings against the exact fetched commit. Include
the maintained dependency locks, source-rights inventory, required canonical CI,
image scan/SBOM/provenance, approved build route and remaining acceptance gates.
Existing local/mock evidence is useful input; it is not secure-platform approval.
The [sanitised security report](../security/GCP-223-SECURITY-REVIEW.md) retains the
original three MEDIUM findings and partial coverage. The updated maintained-lock
scan reports zero advisory entries; both original images remain blocked by
HIGH/CRITICAL package entries and incomplete inventory/binary coverage. Review
the actual remediation observations and exact final source before approval;
the archive correction passed its final focused checks and parent's recheck. Neither
the historical clone nor that dependency result grants execution.

## Preserve edits and switch only after source/image approval

If `git status` reports changes, stop before switching. Preserve and review that
work using the platform's normal process. Do not automatically stash it, reset
the branch, run `git clean` or overwrite local configuration. If platform policy
permits a separate clean clone to preserve independent work, that is a separately
chosen source location; it is not required by this runbook.

After the recorded source/image decision, and only with a clean checkout, select
the implementation branch. Check whether it already exists locally:

```sh
git branch --list codex/gcp-private-pilot
```

If it does not exist, create a tracking branch from the fetched remote branch:

```sh
git switch --create codex/gcp-private-pilot --track origin/codex/gcp-private-pilot
```

If it already exists, use it and accept only a fast-forward update:

```sh
git switch codex/gcp-private-pilot
git pull --ff-only origin codex/gcp-private-pilot
```

If the remote-tracking ref is absent because the older clone tracks only `main`,
fetch that exact ref explicitly with the approved Git client, then retry the
switch:

```sh
git fetch --no-tags origin \
  refs/heads/codex/gcp-private-pilot:refs/remotes/origin/codex/gcp-private-pilot
```

A dirty checkout, divergence or failed fast-forward is a stop condition, not a
reason to force an update. Once switched, record and compare again:

```sh
git status --short --untracked-files=all
git rev-parse HEAD
```

`HEAD` must equal the full approved source commit. If a later pull brought a
new commit, review that commit before any repository execution or container
opening. Retain the previously recorded branch/commit for recovery; do not use a
reset to undo preserved work.

## Admit the execution environment separately

Use the [development profile guide](README.md) to select the approved environment.
The secure profile requires the platform's immutable internal image digest and
actual recorded admission. An illustrative placeholder, an approved image family
or a successful local build is insufficient. The platform decides exact image
source, vulnerability disposition, provenance, registry, mirrors and certificate
trust. Do not substitute a mutable external image tag to get past a blocked gate.

After the independent review/platform decision, the explicit local admission
helper checks the exact source/image/profile bindings and cached image. It does
not authenticate an approver or turn a fabricated `PASS` record into authority.
Keep these real private records and the new admission output outside the source
checkout.

The source record uses `gis-ai-go.full-source-review.v1`, scope `full-source`, the
exact `source_sha256`, canonical report digest, checked coverage and an empty
unresolved-findings list before `PASS`. The image record uses
`gis-ai-go.devcontainer-image-review.v1`, the real internal `image_reference`,
the OCI archive/manifest digests, offline assurance receipt digest and explicit
observed signature/provenance/platform-policy results. Its manifest must match
the approved registry digest and assurance receipt. An offline OCI scan receipt alone does not bind a
registry image or prove its signature. The platform approval binds both record
hashes, source/image, offline BDUK profile, approver/change reference and expiry.
These operator records must describe actual review decisions, not generated
approvals. With those inputs, run:

```sh
./scripts/environment/environment.sh admit --profile bduk \
  --image "$GIS_AI_GO_SECURE_DEV_IMAGE" \
  --source-review ../gis-ai-go-private-review/source-review.json \
  --image-review ../gis-ai-go-private-review/image-review.json \
  --assurance-receipt ../gis-ai-go-private-review/image-assurance.json \
  --approval ../gis-ai-go-private-review/platform-approval.json \
  --output ../gis-ai-go-private-review/admission.json
```

The shown private directory is a portable example; use the platform's actual
approved custody location and immutable internal image reference. Missing or
mismatched records/image return `BLOCKED`; nothing is pulled or opened. An
existing checkout containing ignored material needs an exact permitted workspace
review or a separately approved source-only location before mounting. Preserve
the original work. `.gitignore` does not remove physical files from a bind mount.

An approved builder is a separate boundary from an editor container. It receives
only reviewed public/synthetic source and admitted metadata, with approved
registry/mirror/proxy/CA access. It does not receive the host Docker socket, host
home, cloud credentials or protected workbench folders. Do not disable TLS or
download tools through an unreviewed installer. Keep `gcloud` and deployment
credentials on the approved operator host; a development container does not need
them for offline source checks.

After these gates, use [the platform installer](../deployment/gcp/INSTALL_PLATFORM.md)
to create private configuration, inspect prerequisites and prepare a costed exact
deployment plan. The first cloud mutation still requires the platform's resource,
IAM, upload, identity, total-cost and retention decision. Source/image admission
does not grant that authority. Do not mount or upload protected BDUK data,
licensed feature payloads or private original-document archives.

## Acceptance and evidence

Retain full source/image/config/plan identities and actual command outcomes in
the approved private evidence location. The public repository holds sanitised
templates and admitted fixtures. Canonical CI, local/container tests, secure
workspace admission, real hosted authentication, persistent evidence and BDUK
acceptance are separate results. A checked-out branch, runnable container or
completed review ZIP does not pass the 41 hosted requirements.
