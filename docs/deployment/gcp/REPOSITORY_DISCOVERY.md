# Repository discovery for the GCP adaptation

Observed on 5 October 2026. The authoritative local source revision is
`97bc45635a91064cd78f06bf0848ad7636f05439`. The release preparer additionally binds
the actual working tree, including relevant uncommitted implementation files;
this revision alone is not a clean-build or hosted acceptance claim.

## Two distinct knowledge pipelines

| Pipeline | Actual local producer and validator | Record grain and retained limitation | Hosted consumer |
| --- | --- | --- | --- |
| `okf/` | `scripts/build_okf.py`, its locked HMLR inputs, JSON Schema checks and checksum receipt | 36 curated public discovery records. This is the supported Explorer catalogue, not the expanded OS/ONS inventory. | Existing Explorer and WebMCP Explorer, preserved under separate private routes. |
| `okf-plus/` | `scripts/okf_plus/verify.py`: source-to-Markdown consistency, `build.py`, pinned schemas, complete context projection, retrieval suite and independently pinned Explorer context engine | 30,833 source-native catalogue representations, retained separately across OS/ONS metadata lanes. Counts are not unique products; global completeness and semantic certification remain unestablished. | GCP knowledge API, browser knowledge surface and custom MCP metadata operations use the same release. |

The expanded build consumes the checked-in `okf-plus/source/*.json`, the
reviewable Markdown/YAML-LD records, profile, schemas, pinned vendor contracts and
the exact source lock. The normal verifier works from those admitted local
inputs. It does not need to harvest replacements, inspect a private original
archive or call a provider. The initial full run verified the importer before
building the entire retained corpus.

`scripts/okf_plus/export.py` is the reviewed public metadata hand-off. It checks
the final verification, source digest chain, bundle checksums and context output
inventory. `export_documents.py` is a separate owner-private archive mechanism:
its original OS documentation and retained specifications are explicitly
excluded from the GCP build context. Public documentation projections retain
structure and provenance; they do not republish original prose or examples.

The actual expanded descriptor remains `okf.json`, with its own entrypoint and
profile status. Its context projection has separately pinned descriptors and
contracts. No universal `/.well-known` OKF discovery convention is invented.
Installed Ask OKF admission and the four interpretation questions needing
context remain separate gates.

## Website, workbench and transport seams

The existing `apps/public-explorer` and `apps/webmcp-explorer` are locally built
static catalogue interfaces with explicit distribution inventories and
checksum-bound public catalogue assets. Both remain available in the private
deployment. They honestly retain the 36-record source they were designed for.
The additional GCP knowledge surface uses the full OKF+ release; an independently
working MCP connection is not used as proof that either legacy catalogue changed
its data source.

The private root portal links these separate existing interfaces with their true
corpus counts. `/knowledge` is an ordinary manual browser interface over the same
authenticated `/api/knowledge/search`, `/api/knowledge/describe` and `/api/release`
implementations used by MCP. It displays the admitted content identity, bounded
results, exact source records, rights, dates and evidence limits. All assets are
local; the interface needs neither an AI host nor an external model request.

`apps/public-data-workbench` implements seven contact-free frozen metadata
stories and the bounded maintained `L522 / MM23` CPIH capture for January and
July 2026. Its ordinary browser controls and page tools share one controller.
The local edition pins `http://127.0.0.1:8788/mcp`; the existing Sites edition pins
its private Sites origin and `/workbench/mcp`. Neither transport is a suitable
unchanged GCP browser client. The additive `gcp` build mode uses this page's exact
origin at `/mcp`, HTTPS or the fixed `http://127.0.0.1:8789` personal tunnel.
The runtime independently enforces its deployment allowlist. The browser refuses
destination substitution and preserves redirect, cache, cancellation and
credential boundaries. Its display checks use the existing hosted transaction
evidence contract.

The CPIH projection is the admitted cached fixture
`tests/fixtures/web216/current-cpih-projection.json`; its original capture date
and source vintage remain visible. Retrieval does not refresh it or activate
live execution. Workbench discovery remains a seven-record sample, with a
separate link to expanded knowledge discovery.

The custom Streamable HTTP adaptation uses the repository's pinned MCP SDK and
shared transport-neutral selection, hosted capture and evidence implementations.
It is a new GCP entrypoint, not exposure of the local-only candidate's listener.
The Sites/Workers native page mount, login environment and Voice facilities are
host capabilities. Ordinary Cloud Run HTTP and optional browser WebMCP feature
detection do not establish those integrations or external AI-client acceptance.

## State contracts that must survive the port

`web216-hosted-cpih-application.ts` validates the admitted capture, resolves
non-authorising selections, writes a scoped claim/receipt and re-reads evidence
for inspection. The maintained `web216-transactional-contract` defines canonical
store identity, records, events, bounded capacity, sequence/hash chains and
conflict behaviour. The D1 adapter supplies snapshot and conditional batch
semantics; an unchanged Worker or a renamed local file backend cannot supply
that behaviour on Cloud Run.

The GCP adapter preserves the hosted application behind a Firestore transaction
boundary. Instance-local files and Cloud Storage FUSE are not evidence stores.
Local fixture and emulator/mock tests do not prove hosted transactions,
cross-revision persistence, authentication or BDUK acceptance. Those observations
must be produced after an approved deployment.

## Deliberate release and upload inventory

`node scripts/gcp/prepare.mjs --output artifacts/gcp/<run>/prepared` runs offline
knowledge verification, TypeScript builds, current UI builds and workbench tests.
It creates a new `context/` containing only these categories:

- `Containerfile` with the existing digest-pinned Node 24.19.0 base;
- `/app/gateway`, `/app/node_modules` and the launcher: built application code
  and the exact installed production dependency closure, with licence notices;
- `/app/schemas`: exactly the canonical JSON contracts declared by the maintained
  HTTP assembly. The preparer imports the actual staged runtime and OIDC package
  to detect missing runtime dependencies before accepting an image;
- `/app/static/{explorer,webmcp,workbench}`: checked local assets;
- `/app/bundles/okf`, `/app/bundles/okf-plus` and
  `/app/bundles/okf-plus-context`: complete admitted generated metadata outputs;
- `/app/bundles/cpih-projection.json`: the bounded redistributable cached fixture;
- the release manifest, deny-by-default runtime template and project notices.

The preparer refuses symlinks, state, environment files, credentials, archives,
private/capture/research paths, tests, source maps and arbitrary added build
inputs. It scans the actual outgoing metadata and browser assets using the
reviewed public-export patterns. Production packages are materialised from
installed pinned dependencies; the container has no dependency installation
step. `verifyPrepared()` rechecks the complete exact inventory and hashes before
publication. The source manifest includes build inputs and relevant uncommitted
file hashes. It contains identities, not private source archive contents.

The final expanded generated bundle measures **596,817,491 bytes** (about
569 MiB), with another **255,612,053 bytes** (about 244 MiB) of complete context
outputs. The prepared allowlist totals **33,389 files / 869,112,769 bytes**;
the OCI archive totals **311,709,696 bytes**. It must not be described as a tiny catalogue. `manifest.json` records
the actual complete file and byte totals. The initial profile bakes the measured
release into the image. Memory, startup, image storage and redeployment cost
remain explicit sizing checks; changing to a bucket requires the separate
immutable release and authenticated delivery contract.

The additive private pilot container uses the Node digest already recorded in
the existing gateway build. A local registry pull verified that exact digest.
It preserves non-root execution, read-only application files, pinned dependencies
and a network-disabled build step. It is a separate Debian-based pilot image;
the hardened UBI local candidate's assurance is not inherited. Its own container
and release checks and the platform's image acceptance remain required.
The production dependency manifest records observed installed file bytes and the
lockfile digest; this observation is explicitly not a package-byte attestation.

The preparer makes no GCP resource changes and does not publish anything. Its
runtime configuration template deliberately lacks usable project/transport/URL
bindings when those prerequisites are unresolved. A complete approved operator
binding is required for hosted readiness.

## Final local integration observations

The accepted local release is
`e1223d0f47deb2f73d554404d02a42ebf0cd9bad68be86efd15a4b50688c289b`,
with OCI manifest
`sha256:3ef00620adfc26290444eec5fd7d7c60abbf1274c79c28b4e90615a99a188a4f`.
Evidence is under `artifacts/gcp/1784b702d63d0ba7/`.

`full-release-http-mcp-local.json` records actual admitted payloads through the
actual Node HTTP assembly, private proxy and pinned MCP SDK: both corpus counts,
identical web/MCP record hashes, resolved legacy source references, all six
owner tools, release resource and the complete 189,929,585-byte OKF+ JSON export.
The export was streamed and its complete hash matched the admitted file.
Identity was RSA-signed synthetic transport verified with an offline JWKS
constructor seam; storage was an atomic memory mock with no writes. This proves
local integration, without establishing hosted IAM, human SSO, BDUK policy
acceptance or Firestore persistence.

`local-image-identity.json` verifies the loaded Docker image's config digest and
root filesystem against the same OCI archive. `local-image-boot.json` records
the actual full-corpus image under a 2 GiB memory limit, a read-only root and no
network: startup in 8.45 seconds, process RSS 788,836 KiB, observed cgroup peak
793,579,520 bytes, no OOM kill and clean SIGTERM exit. Its deliberately neutral
binding serves liveness and returns 503 for readiness, application content and
MCP. Resource observations are local, with no hosted scaling or cost claim.
