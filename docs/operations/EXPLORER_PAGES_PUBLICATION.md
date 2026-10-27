# Publish the full GIS Explorer

This runbook covers the static publication in
[ADR-0019](../decisions/ADR-0019-full-explorer-pages-publication.md).
Live cutover, public verification and rollback/restore remain pending until their
exact workflow results are recorded. This work adds no gateway, provider service,
protected-data entitlement or hosted Ask OKF admission.

The public dependency closure retains the complete public metadata and
native-field/atomic source records. The separate new private capture feature is
preserved unchanged at
[35318abc](https://github.com/chris-page-gov/gis-ai-go/tree/35318abcce5e23c1509ed6ce131d81f5dfd0d38c)
with [unresolved review findings](EXPLORER_PAGES_CODEQL_REVIEW.md). It is not used
by this publisher. Existing main OS recovery remains in place. Public success
does not resolve that deferred feature's review or wider acquisition work.

## Build and check a local candidate

Use a clean GIS checkout and a separate canonical Explorer checkout at
`7ffa3297ec85bf28c27963724f221d80579bed1b`. The checked
[publication configuration](../../config/explorer-publication.json) pins that
source, app tree, build manifest, public context prefix and capture timestamp.
The complete app remains unchanged; generated guides have separate
`explorer/GUIDE-PROVENANCE.json` source/output hashes and reference mappings.

Use the candidate CI toolchains: Node.js 24.22.1, GIS pnpm 10.33.2, Explorer
pnpm 10.34.7, uv 0.12.2 and Explorer CPython 3.12.11. Corepack selects each
repository's locked pnpm. Install GIS dependencies with the locked commands in
the [README](../../README.md#local-verification), then run from the GIS root:

```sh
bash scripts/build_explorer_pages_candidate.sh ../okf-explorer
```

The script builds the pinned app and guides, regenerates the complete public
projections, assembles legacy routes, packages, verifies and stages the archive,
then runs complete-byte verification and seven browser journeys. It requires new
output directories; preserve earlier candidates and use a fresh checkout to rerun.

The three files in `artifacts/pages/` are the immutable source archive:
`artifact.tar`, `artifact.tar.sha256` and `archive-receipt.json`.
`artifacts/explorer-pages-candidate/` holds the local staged payload and server
log; `apps/public-explorer/test-results/explorer-public/` holds byte and browser
results. Local mode explicitly mirrors the canonical URL prefix into the exact
loopback-served stage. Its receipts say `loopback-candidate`; they do not establish
that the public HTTPS site serves those bytes.

## Select and deploy the accepted source

Merge only after mandatory PR assurance. The complete successful protected-main
push CI must include the Explorer candidate and provenance attestation. Its
`pages-source-FULL_COMMIT` artefact contains the archive built and checked in
that run. PR `pages-review-*` artefacts are review evidence, not deployment input.

Dispatch `.github/workflows/pages.yml` on `main` with these inputs:

| Input | Required value |
| --- | --- |
| `source_run_id` | Successful complete main-push CI run ID |
| `source_commit` | That run's full 40-character GIS commit |
| `archive_sha256` | SHA-256 of its accepted `artifact.tar` |
| `mode` | `deploy`, `rollback` or `restore` |
| `reason` | Concise public audit reason without private details |

The workflow checks the source run, unique retained artefact, archive digest,
attestation and complete logical payload. It stages those verified bytes and uses
GitHub's pinned official Pages transport through the existing branch-restricted
environment. It does not rebuild the site during deployment.

Public mode uses the actual canonical HTTPS site and forbids local interception.
A bounded receipt wait allows CDN propagation: at most 110 seconds and 55 probes,
each capped at 64 KiB with a five-second request deadline. A matching receipt is
followed by strict complete-file streaming verification with bounded concurrency
and all seven browser journeys. Record the exact served-file count and bytes.
The full public walk keeps at most 12 workers and spaces actual request starts
by at least 20 milliseconds (at most 50 per second); loopback checks are unpaced.
Only HTTP 429, 502, 503 and 504 permit up to two extra attempts per file, with
shared ceilings of 64 extra requests and 64 MiB of reserved replay bytes.
Backoff is one then two seconds, respecting a valid Retry-After up to ten
seconds; a longer or malformed value fails closed. Error bodies are cancelled
without being read. Queueing, backoff and retries remain inside the 20-minute
walk deadline, and each actual request retains its 30-second deadline.
Pass and failure reports record reservations, actual extra starts, statuses and
received retry-body bytes; verified file and byte totals still count the complete
successful inventory once. A hash, length, identity or redirect failure is never
retried or skipped.

The pre-split local candidate checked all 37,279 public files; the narrowed
source requires fresh complete verification with its new input digest and snapshot.

## Retained legacy rollback

The following v1 selection was present in GitHub metadata on 26 October 2026:

| Identity | Value |
| --- | --- |
| Source commit | `f1bda209e6309bf4f14f7ab7f524c442e59917b8` |
| Source CI run | `32330917042` |
| Actions artefact ID | `9392991975` |
| Source tar SHA-256 | `acf072986dafc34795039e363d0d5d09af44432fa392ff3aee5525887e1081a4` |
| Actions ZIP SHA-256 | `b727ee694306c574dbdfb959000983c2212198984d578aa1803b32d0d23f0314` |
| Actions retention expiry | 18 November 2026, 04:10:51 UTC |

Recheck the current API before use: the source run must still match, and the
exact-name artefact must be unique, unexpired and have its recorded transport
digest. The Actions ZIP digest is separate from the source tar digest above.
This readiness observation did not download the archive or perform fresh
cryptographic or public-byte verification. Immutable release assets remain
historical evidence; they are not an alternative ingestion path for this workflow.

Rehearse `rollback` with the retained v1 run, source and tar digest. Let the
unchanged legacy verifier and public suite validate it. Then select the accepted
v2 main-run archive with `mode=restore` and verify the full public bytes and
journeys again. Record deployment run IDs, source/archive identities, roots and
results in [PROGRESS](../../PROGRESS.md) and the retained workflow evidence before
recording cutover and rollback/restore as complete. A deployment failure does not
authorise rebuilding an accepted archive or weakening its checks.
