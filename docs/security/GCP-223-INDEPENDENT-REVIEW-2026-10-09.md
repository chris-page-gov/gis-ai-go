# GCP-223 independent source review and follow-up

This is a sanitised derivative of the completed source review and subsequent
local remediation. It preserves the original findings and separates source
checks from image admission, hosted authentication and BDUK acceptance.

## Reviewed source and measured time

- Immutable scan input: `f3dd856fbb584705156f6cf7d6c344935e2e0a55`.
- Standard repository scan: `32c82a8a-dfad-463b-a267-478744b3df57`.
- Generated report SHA-256:
  `a901ef2c623f4c1a5c74be2a50723209c60c1bc50024a2f9e2c086d3d51c916b`.
- Review began at 19:50:48 UTC; completion was confirmed at 20:41:18 UTC on
  9 October 2026: **50 minutes 30 seconds**. This measures this review,
  including its setup and checkpointing, rather than the entire earlier task.
- **752 distinct tracked files** received whole-body source review. Overlapping
  reviews count once. The tracked inventory contains **32,234 files**.
- The owner reported switching to Daybreak. Backend model identifiers and token
  usage were unavailable. There was no controlled Fast-mode comparison, so no
  speedup, token charge or counterfactual cost is claimed.

The review covered maintained runtime code, operator scripts, schemas, tests,
selected current guides and imported context parsers. Approximately 30,000
OKF+ corpus records, most historical documents, retained fixture/evidence
semantics and installed or external dependency bytes were not exhaustively
audited. A file inventory, content hash, test assertion or architecture diagram
is not full semantic review of its contents. **Coverage remains partial.**

The scan used static source analysis. No application, tests, exploit payload,
cloud operation, provider request or external model call was executed during
that scan. The local checks below ran afterwards, against the patch.

## Findings and implemented corrections

| Original finding | Severity | Correction |
| --- | --- | --- |
| OCI and received scanner-database hidden tar metadata can exhaust host memory before ordinary member checks | MEDIUM | Shared resource guard at all ten read-mode tar entry points; bounded metadata processing and sequential member-cache retention |
| A workload-authenticated caller can exhaust the shared pre-human browser login pool | LOW | Stateless encrypted login start; bounded atomic replay ledger written only after human OIDC verification |

The original archive finding concerns host resource consumption. Neither code
execution, path traversal nor credential disclosure was established. Modern
compressed layer parsing permitted large accumulated hidden extension bodies
within its 32 GiB expanded-byte ceiling. Legacy layers already had a 512 MiB
spool limit; that material mitigation is preserved.

The shared stdlib-only guard limits each hidden extension to 64 KiB, aggregate
extension storage to 64 MiB, extension headers to 100,000, nesting to 16, and
retained PAX state to 128 attributes / 64 KiB. It rejects sparse metadata before
map processing and uses errors that cannot be silently treated as an archive
terminator. Ordinary bounded GNU/PAX metadata and opaque modern layer xattrs
remain accepted; legacy metadata policy remains stricter. Raw expanded bytes
still determine DiffID. Sequential layer readers discard cached TarInfo objects;
outer readers needing name lookup retain their bounded inventories.

Browser login no longer creates pending authentication documents. The existing
AES-GCM key protects version 2 flow cookies, including state, nonce, PKCE verifier,
original SID and five-minute expiry. After maintained-library ID-token and
resource access-token verification, a strong read/CAS ledger records the original
flow hash. A single document holds at most 256 live accepted flows, each retained
through its original expiry. A successful claim precedes session issuance;
session-allocation failure and logout do not erase that replay marker. Replay is
refused before another exchange. Expiry is rechecked after awaited operations.

Consumption now means **one accepted flow**, rather than one attempted exchange.
Failed verification stores no marker; concurrent valid attempts may both reach
the approved identity provider but can issue only one session for the same flow.
Token endpoint code-use rules, nonce, state, PKCE, private transport, durable
session revocation and application policy remain independent controls. Version 1
pending login cookies fail closed after upgrade; existing version 1 session
cookies keep their existing validation. Hosted rollout and issuer acceptance
remain untested. Verified humans can still reach bounded session/ledger capacity;
this change closes reservation by callers without a verified human identity.

One fresh read-only investigator and one fresh read-only candidate reviewer
were assigned per finding. Both pre-patch investigations completed. Parent
review separately traced each boundary.
The login reviewer identified four-round shared-ledger contention. A synchronised
local fixture reproduced four successes and one rejected fifth login despite
free capacity. The correction permits eight bounded rounds, matching the
server's eight admitted active requests. The final fixture admits all eight
distinct verified flows. The host subsequently reported both candidate-review
threads as `pending_init`; a bounded wait returned no final review. Those threads
were interrupted, and the parent performed the skill's separate bypass and
regression review fallback, including every changed direct caller and the
Firestore read/CAS contract. No further concrete bypass was established.
**Independent final candidate-review results are unavailable**, rather than
passed. The earlier contention observation is retained. No second fresh review
cycle is claimed.

Two current demo/probe client/server identity checks now match maintained SDK
2.2.0. Node integration 2.0.0 and historical accepted observations are preserved.
Active dependency-install instructions use frozen locks, disabled install hooks
and copy-only imports. Historical research and security observations remain
unchanged.

## Observed local checks

| Check | Observed result |
| --- | --- |
| Archive/image and GCP lifecycle/environment/proxy/installer Python checks | 308 pass |
| Compiled GCP runtime checks, including login flood, replay, expiry, failed session storage and concurrent callbacks | 30 pass |
| Demo receipt/result checks | 5 pass |
| Gateway TypeScript compilation | Pass |
| Syntax checks for the two corrected current demo/probe scripts | Pass |
| Conservative repository secret and machine-path scan | 32,361 text files scanned; no baseline match |

Tiny declared oversized headers were rejected before any extension-body read;
all hidden extension forms, nesting, cumulative global PAX and sparse variants
were exercised. Valid GNU/PAX/xattr layers preserved raw-byte DiffID. Four
hundred unauthenticated login starts produced zero authentication writes; a
victim flow still completed. Signed issuer and backend fixtures are local mocks,
not Google/Okta authentication or Firestore persistence evidence.

The first check attempts encountered read-only default cache locations and an
unpinned host pnpm fallback. Verification used the writable repository uv cache,
existing locked dependencies, Node 24.19.0 and Python 3.12.14; no package-manager
upgrade or new dependency was introduced. Two test expectations were corrected
for the established Blocked error and stateless login behaviour. The independently
reproduced contention failure remains a separate before/after observation.

Portable commands from the repository root, **only after that machine's source,
tooling and image admission**, include:

```sh
UV_CACHE_DIR="$PWD/.uv-cache" uv run --offline --locked python -m unittest tests.deployment.test_bounded_tar
node node_modules/typescript/bin/tsc --project apps/mcp-gateway/tsconfig.json
node --test apps/mcp-gateway/dist/test/gcp-*.test.js
node --test tests/test_local214_demo.mjs
UV_CACHE_DIR="$PWD/.uv-cache" uv run --offline --locked python scripts/scan_secrets.py
```

## Precise remaining gates and handover

1. Approve the final source commit/digest with the retained partial coverage,
   missing independent final candidate-review results and unresolved questions.
   This review's immutable input precedes the fixes; the parent fallback and
   local regression results are separately recorded. Source changes are locally
   corrected; complete remediation admission remains blocked by these gates.
2. Complete canonical repository assurance. Earlier full local assurance had
   native observer/collector fixture failures and no canonical Chrome. Previous
   CodeQL success is evidence for its own commit, not this follow-up.
3. Replace or remediate the blocked images, obtain fresh offline scans with
   complete coverage, and approve each image digest, SBOM, provenance/signature,
   licences, registry and builder. Earlier observed toolchain image counts were
   36 CRITICAL / 714 HIGH; GCP image counts were 5 CRITICAL / 69 HIGH. These are
   separate, dated images. This patch changes no image or image admission result.
4. Supply BDUK-approved project/billing, private networking, Okta registration,
   human-role mappings and platform approval. The personal £20 preference is
   not BDUK spending authority. Show exact account/project, resources, admitted
   upload inventory and a costed plan before the first cloud mutation.
5. Establish real private transport, Google workload identity, Okta human
   identity, server ABAC/RBAC, authentication failures, persistence, expiry,
   rollback and BDUK acceptance through approved hosted checks.

The public metadata cleaner has source-confirmed superlinear regex behaviour,
but an adversary controlling selected fixed-provider metadata and a victim
resource boundary were not established. Its original candidate remains
deferred. A browser's public-access result filter is not a storage/network ACL
for restricted records in a fetched shard. Initial inputs must remain admitted
public metadata and synthetic fixtures; no protected shard has been admitted.

Source is transferred through draft [PR #146](https://github.com/chris-page-gov/gis-ai-go/pull/146)
on `codex/gcp-private-pilot`. From the existing secure clone, approved Git can
fetch and display this report without executing repository scripts:

```sh
git status --short
git fetch origin
git show origin/codex/gcp-private-pilot:docs/security/GCP-223-INDEPENDENT-REVIEW-2026-10-09.md
```

Follow the [existing-clone transition](../development/SECURE_TRANSITION.md) and
[installer guide](../deployment/gcp/INSTALL_PLATFORM.md). Preserve dirty work;
do not reset, clean, automatically install dependencies or open a container.

On an admitted operator machine, the executable non-mutating package workflow is:

```sh
bash scripts/gcp/install-platform.sh init --config artifacts/gcp/bduk-review.json
bash scripts/gcp/install-platform.sh review --skip-prepare --config artifacts/gcp/bduk-review.json
```

The exclusive `init` refuses to overwrite an existing private config. Without
approved platform inputs, `review` returns blocked while retaining the actual
sanitised `platform-review.zip` and installer summary. `--skip-prepare` avoids an
image build; the package does not grant execution or deployment approval.

No cloud mutation, data upload, model/provider call, image publication, merge or
hosted deployment occurred during this increment. **Cloud cost incurred by this
increment: £0; hosted deployment URL: none.** This does not measure Codex billing
or the cost of any pre-existing resources. No cloud cleanup is needed for this
increment. For a later approved deployment, lifecycle `plan --destroy`, `destroy`
and rollback require the matching recorded approval; do not delete unrelated
platform resources.
