# Publish the full GIS Explorer

This runbook covers the static publication in
[ADR-0019](../decisions/ADR-0019-full-explorer-pages-publication.md).
The public default, complete HTTPS/browser checks and legacy rollback/restore
passed on 27 October 2026. The
[completed discovery evidence](#discovery-publication-evidence) below records exact sources,
workflow identities and outcomes. This work adds no gateway, provider service,
protected-data entitlement or hosted Ask OKF admission.

The subsequent [discovery repair](../implementation/OKF_EXPLORER_DISCOVERY.md)
adds facets, retained-record relationships and bounded source references. Its
producer and canonical consumer have merged after required PR assurance, with
the immutable consumer pin verified against the identical merged Git tree.
Complete GIS main CI and CodeQL passed all 13 checks with none skipped, and the
exact main archive and attestation are verified. Initial deploy `40506483121`
passed all three jobs, complete actual public HTTPS verification and all eight
browser cases first attempt. Historical rollback `40509547583` and restore
`40512243266` of the identical new archive also passed their actual public checks.
The previously accepted
`8e67ae88…` archive below retains its two-facet, zero-relationship projection;
its successful publication checks do not establish the richer discovery increment. The
[merged implementation evidence](../implementation/OKF_EXPLORER_DISCOVERY.md#merged-implementation-and-review-evidence)
records the main archive and all three accepted public phases separately from
the review-only candidate and earlier publication.

The public dependency closure retains the complete public metadata and
native-field/atomic source records. The separate new private capture feature is
preserved unchanged at
[35318abc](https://github.com/chris-page-gov/gis-ai-go/tree/35318abcce5e23c1509ed6ce131d81f5dfd0d38c)
with [unresolved review findings](EXPLORER_PAGES_CODEQL_REVIEW.md). It is not used
by this publisher. Existing main OS recovery remains in place. Public success
does not resolve that deferred feature's review or wider acquisition work.

## Discovery publication evidence

The discovery increment completed on 27 October 2026. The current bare
[GIS public URL](https://chris-page-gov.github.io/gis-ai-go/) serves exact source
`93fe753460a2a3c907d9b8257060e89c758e3c4e`, selected from successful complete
main CI `40500356691`, with tar SHA-256
`742eb25f698355fe021780d321e025a4b542a6ee32b8da60921c4a0d2e3b39b4`.
All 13 main checks passed without skips. The canonical consumer is pinned to
reviewed `75753709…`, whose Git tree equals merged upstream `46928e2a…`.
The [complete identity and assurance record](../implementation/OKF_EXPLORER_DISCOVERY.md#merged-implementation-and-review-evidence)
binds the source artefact, attestation, app tree/manifest, roots and scoped results.

| Actual public phase / attempt | Selected source / tar | Complete verified files / bytes | First-attempt browser passes | Automatic HTTP 503 retries / replay bytes |
| --- | --- | --- | --- | --- |
| [Deploy 40506483121](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40506483121) / 1 | `93fe7534…` / `742eb25f…` | 38,604 / 899,129,361 | 8 | 18 / 142,197 |
| [Rollback 40509547583](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40509547583) / 1 | `8e67ae88…` / `3fe87087…` | 37,279 / 714,610,618 | 8 | 5 / 25,008 |
| [Restore 40512243266](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40512243266) / 1 | The identical `93fe7534…` / `742eb25f…` archive | 38,604 / 899,129,361 | 8 | 10 / 280,000 |

All three phases passed source/archive/attestation validation, deployment and
actual canonical HTTPS verification. Each public walk checked all selected
logical bytes; every browser case passed first attempt with zero flaky, skipped
or unexpected results, mirrors or reported transport errors. Each phase used one
readiness probe / 1,398 bytes. Transient HTTP 503 responses recovered within the
unchanged bounded automatic retry policy, with no manual rerun and zero
application-consumed error-body bytes. Their phase-specific totals above are
separate from the earlier publication's retries below.

Rollback verified the original `8e67ae88…` app, roots and two-facet/zero-graph
profile. Restore verified the identical new archive, not a rebuilt candidate,
and the full discovery contract: 18 facets, 137 explicit relationships, 61,309
source-reference associations and two publishers. Four suggested facets remain
folded, with 12-pixel bars and compact controls; **All** exposes every dimension.
This completes static discovery publication and recovery acceptance. Later
documentation commits do not replace the selected source; the supported release,
human learning assessment, private findings and acquisition work remain separate.

## Build and check a local candidate

Use a clean GIS checkout and a separate canonical Explorer checkout at
`757537090af94eb6dda51de16938aa221fcda48d`. The checked
[publication configuration](../../config/explorer-publication.json) pins that
source, app tree, build manifest, public context prefix and capture timestamp.
The complete app remains unchanged; generated guides have separate
`explorer/GUIDE-PROVENANCE.json` source/output hashes and reference mappings.
An immutable reviewed head may remain the pin after upstream merge only when
its Git tree equals accepted main. Require full upstream PR assurance, merge,
that exact tree comparison and successful normal main workflow selection before
GIS merge or publication. Record declared conditional skips separately from the
full behavioural evidence; do not force selectors or claim a full main rerun.

Use the candidate CI toolchains: Node.js 24.22.1, GIS pnpm 10.33.2, Explorer
pnpm 10.34.7, uv 0.12.2 and Explorer CPython 3.12.11. Corepack selects each
repository's locked pnpm. Install GIS dependencies with the locked commands in
the [README](../../README.md#local-verification), then run from the GIS root:

```sh
bash scripts/build_explorer_pages_candidate.sh ../okf-explorer
```

The script builds the pinned app and guides, regenerates the complete public
projections, assembles legacy routes, packages, verifies and stages the archive,
then runs complete-byte verification and eight browser journeys. It requires new
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
and all eight browser journeys. Record the exact served-file count and bytes.
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

The accepted source's complete HTTPS inventory is recorded below. A later
publication must establish its own exact-source and complete-file evidence;
earlier loopback or public results cannot be relabelled for changed bytes.

## Retained legacy rollback

The following v1 selection was rechecked in GitHub metadata on
27 October 2026, 02:17:11 UTC before the recorded rehearsal:

| Identity | Value |
| --- | --- |
| Source commit | `f1bda209e6309bf4f14f7ab7f524c442e59917b8` |
| Source CI run | `32330917042` |
| Actions artefact ID | `9392991975` |
| Source tar SHA-256 | `acf072986dafc34795039e363d0d5d09af44432fa392ff3aee5525887e1081a4` |
| Actions ZIP SHA-256 | `b727ee694306c574dbdfb959000983c2212198984d578aa1803b32d0d23f0314` |
| Actions retention expiry | 18 November 2026, 04:10:51 UTC |
| Rehearsed v1 payload root SHA-256 | `80a649a5e4bebc36fb38c7b6d51d84056d1b2ff4c8b5f6b96c75bb6d03c6d245` |
| Rehearsed v1 OKF root SHA-256 | `f6da572916ea850f6825e276867504a835bc783d76cea8038f72c8d1d42c2750` |
| Rehearsed v1 checksum-ledger SHA-256 | `75d3a3c9ad8fad2cd7d5a8ee67851fd7655457aae9473ae717f0f4dbc67da815` |

Recheck the current API before use: the source run must still match, and the
exact-name artefact must be unique, unexpired and have its recorded transport
digest. The Actions ZIP digest is separate from the source tar digest above.
The recorded rollback below subsequently passed the workflow's source, archive,
attestation and public verification checks. Retention must still be rechecked
before any future use. Immutable release assets remain historical evidence;
they are not an alternative ingestion path for this workflow.

Rehearse `rollback` with the retained v1 run, source and tar digest. Let the
unchanged legacy verifier and public suite validate it. Then select the accepted
v2 main-run archive with `mode=restore` and verify the full public bytes and
journeys again. Record deployment run IDs, source/archive identities, roots and
results in [PROGRESS](../../PROGRESS.md) and the retained workflow evidence before
recording cutover and rollback/restore as complete. A deployment failure does not
authorise rebuilding an accepted archive or weakening its checks.


## Completed publication evidence

This section records the accepted `8e67ae88…` publication and its original seven
browser journeys. The later [discovery publication](#discovery-publication-evidence)
has separate acceptance with the eight-journey suite; it does not change the
source, inventory or outcomes recorded here.

Observed on 27 October 2026 for the archive recorded below. At that acceptance,
the bare [GIS root](https://chris-page-gov.github.io/gis-ai-go/) opened the full compact
Explorer. Recognised earlier catalogue query/record links intentionally open
`/legacy/` with their state. The static publication keeps product version `0.1.0`;
it does not replace the immutable supported release or admit a gateway service.

### Accepted publication bytes

GIS source [8e67ae88](https://github.com/chris-page-gov/gis-ai-go/commit/8e67ae88e68341120a712d102f692894fbd89659)
passed complete protected-main source CI
[40412716168](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40412716168)
and full CodeQL
[40412716256](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40412716256).
All ten main CI jobs, including independent verification and provenance, passed.
Its candidate walk and seven browser cases passed in loopback mode without retry;
actual public HTTPS results are identified separately below.

| Identity | Accepted value |
| --- | --- |
| GIS source | `8e67ae88e68341120a712d102f692894fbd89659` |
| Retained source artefact | `pages-source-8e67ae88e68341120a712d102f692894fbd89659`, ID `12695267839` |
| Actions ZIP SHA-256 / bytes | `47a1f3bbdb81116fbe58960fd03cdea9e1820b23fb62a38d782fe26d0e2e2b35` / 134,423,399 |
| Source artefact retention expiry | 24 January 2027, 22:28:36 UTC; recheck before future use |
| Source tar SHA-256 / bytes | `3fe870878a997965fce3d4aec4e407218479ac23e1653cca10ac910d5febfc0c` / 744,069,120 |
| Logical payload root SHA-256 | `fd08e1e07911956fe18b0af3d3e099bb26c864bf302f5ba99f6d0de1fd58f0e1` |
| OKF input root SHA-256 | `4baa97670ab0ebfcb17f3f0d67cabebb00a47dbe686fe33972b9ce9d4ea6e395` |
| Public checksum ledger SHA-256 | `7b4291bbd3f3fc28f91c2a88ef4e01e2cc17b7a969f32b810e73bfcc8ce5177a` |
| Snapshot | `okf-plus-1045d0770cc377a06f9eeb5a` |
| Complete served inventory | 37,279 files / 714,610,618 bytes |
| Metadata closure | 30,876 records, 2,915 native field nodes, three small linked practice paths / 11 steps |
| Explorer source | `7ffa3297ec85bf28c27963724f221d80579bed1b` |
| Explorer app tree SHA-256 | `d127aadb96a77711d5f7cc7aec8cf731cbf5ec1e3d49304d8132189ea4991f93` |
| Explorer app-manifest SHA-256 | `ab227164e2e114148425a453a0e04b6bb21230f79be1e059a3ff6936d57f45f2` |

### Verification repairs and retained failures

Initial [Pages run 40417221604](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40417221604)
used workflow/source `8e67ae88…` and the accepted archive above. Source validation
and deployment passed. Two public complete-file walks failed on different HTTP
503 responses before any browser journey ran. No byte-integrity failure was
reported, and these attempts remain failed despite the later successful deploy.

| Attempt | Verification job | Failed context passage | Diagnostic artefact ID / ZIP SHA-256 |
| --- | --- | --- | --- |
| 1 | `121902971948` | `2173111324335ce9db81a6c4b9f09976f983a8f981d05f2e9404c21a80194075.txt` | `12695184510` / `d940d9e22528988c46dee6e21431a977b8ef53bb7eb4444ba5760c4371583351` |
| 2 | `121904456364` | `213446f784129a2076e1996295663084f82212fb78b53ab0aff4fcfddf421c6e.txt` | `12695924459` / `6336a9494d7ae9506b9cc82bfe0f770f3fa4d8f9ea17bf8772429cdcbd270614` |

Transport repair [#184](https://github.com/chris-page-gov/gis-ai-go/pull/184)
added the bounded pacing/retry policy above. Accepted verifier commit
`0bc58f6dae852175d4acd67cf323243277a60c3a` passed complete main CI
[40423718672](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40423718672)
and CodeQL
[40423718582](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40423718582).
The byte-verifier SHA-256 is
`12466f389ed10d65c679719e24e7ab6ff49879f1cca831ef33ff650f5acabb01`.
Its 23 focused tests and injected local HTTP 503 complete-walk regression were
development evidence; they do not substitute for public acceptance.

The successful deploy below retained one native-field browser failure before its
configured retry passed. Trace inspection found a synchronous option lookup about
18 ms after switching to Building while its record shard was loading. Readiness
repair [#185](https://github.com/chris-page-gov/gis-ai-go/pull/185) waits for the
exact option within the existing bounded assertion. It preserves all field,
source, gap and discovery assertions, timeouts and retry limits. An actual two-second
Building-shard delay passed locally without retry. Accepted repair main
`3fbc813cabdcef259649a7cf51da39e69342e340` passed complete main CI
[40434327233](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40434327233) and full CodeQL
[40434327053](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40434327053).
Its test SHA-256 is `2e3d31faa1bbfc4f32daad1110a897f00df019b9f2e5dccd601081ad3e992d0e`.
All 13 protected-main checks passed. Its seven loopback browser cases passed first
attempt with zero flaky cases; that newly generated archive was not selected
for publication.
Neither repair changes the selected app, source archive or generated payload.

### Actual public phases

The workflow commit identifies the verifier and deployment procedure. The selected
source identifies the immutable served archive; these are deliberately separate.
The initial deploy and rollback passed normal source/archive/attestation
validation, deployment and actual public verification. Restore verification
passed all three jobs and the complete HTTPS/browser checks. No phase rebuilt
its selected archive.

| Phase / run / attempt | Workflow commit | Selected source / source CI / tar SHA-256 | Result |
| --- | --- | --- | --- |
| [Deploy 40427376279](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40427376279), attempt 1 | `0bc58f6dae852175d4acd67cf323243277a60c3a` | `8e67ae88…` / `40412716168` / `3fe87087…` as above | Success; complete HTTPS and seven eventual UI passes |
| [Rollback 40438001316](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40438001316), attempt 1 | `3fbc813cabdcef259649a7cf51da39e69342e340` | `f1bda209e6309bf4f14f7ab7f524c442e59917b8` / `32330917042` / `acf072986dafc34795039e363d0d5d09af44432fa392ff3aee5525887e1081a4` | Success; four actual HTTPS legacy cases passed |
| [Restore 40438260796](https://github.com/chris-page-gov/gis-ai-go/actions/runs/40438260796), attempt 1 | `3fbc813cabdcef259649a7cf51da39e69342e340` | The identical `8e67ae88…` / `40412716168` / `3fe87087…` archive above | Success; complete HTTPS and seven first-attempt UI passes |

| Phase | Validation job | Deployment job | Public-verification job |
| --- | --- | --- | --- |
| Deploy | `121936401354` | `121936837531` | `121936991820` |
| Rollback | `121971269032` | `121971405295` | `121971511026` |
| Restore | `121972118769` | `121972365161` | `121972442433` |

Rollback matched the retained v1 roots above. Its four actual HTTPS cases passed
in 9.7 seconds, with zero reported failures or flaky cases. The v1 suite checked
its payload manifest and public ledger entries; its reporter did not retain a
separate numeric full-byte-walk report or individual result JSON. Final restore
matched every accepted v2 source, payload, OKF, ledger and app identity above.

| Public evidence | Artefact ID | Actions ZIP SHA-256 |
| --- | --- | --- |
| Initial deploy validation | `12700836018` | `687887df3568528738ea12b22777118509dbceaeb99213f3d63cdc831e40beea` |
| Initial successful deploy | `12701470786` | `14a1d5f5828d4e8c3fd06de9d80bb29bcd62486d779479d8c20142e3fb8f90cb` |
| Rollback validation | `12705565081` | `82aaa496807594147d4d45ec9f0564b91c2ec81f459daca8e0ab9bc9082d20a2` |
| Rollback public verification | `12704559326` | `4557bda01fb441f97659e26cb20b3b9fa8a56eeae006b75bb7589426b415fc69` |
| Restore validation | `12705190713` | `d5247a8e4ef39231c61933e2783c5dc8ab0a634d1e93561ea2264ad3be314c2f` |
| Restore public verification | `12704929390` | `ec5b9e23c45f4d3ee0589e6850819476016499c354086bd9843f29dd899deb5b` |

The initial v2 public walk used `mode=deployed-publication` at the canonical HTTPS
URL, with no loopback mirror. Restore used the same mode and canonical URL.
Initial deploy checked all 37,279 files / 714,610,618 bytes in 771,521 ms. Its one
receipt probe consumed 1,398 bytes. Browser results
were six first-attempt passes, one recovered flaky case, zero skipped and zero
unexpected; all seven ultimately passed. That run is not a clean first-attempt
browser result. The retained artefact includes its failure trace and reports.
The suite exercises all three learning paths / 11 steps and checks 12-pixel colour
bars with folded facet cards at most 64 pixels high at 1,440, 390 and 320 pixels,
as well as keyboard, palette and accessibility assertions.

| Actual complete-walk transport | Deploy 40427376279 | Restore 40438260796 |
| --- | --- | --- |
| Verified files / bytes | 37,279 / 714,610,618 | 37,279 / 714,610,618 |
| Elapsed milliseconds | 771,521 | 772,660 |
| Pacing / configured spacing | Enabled / 20 ms, at most 50 starts/s | Enabled / 20 ms, at most 50 starts/s |
| Started requests | 37,280 | 37,280 |
| Minimum observed start gap | 20.000559 ms | 20.000614 ms |
| Peak queued / active requests | 12 / 12 | 12 / 12 |
| Retry reservations / extra requests / retried files | 1 / 1 / 1 | 1 / 1 / 1 |
| Reserved replay / received extra-response bytes | 4,346 / 4,346 | 6,371 / 6,371 |
| Transient status counts (429 / 502 / 503 / 504) | 0 / 0 / 1 / 0 | 0 / 0 / 1 / 0 |
| Cancelled error bodies / application-consumed error bytes | 1 / 0 | 1 / 0 |
| Browser expected / flaky / skipped / unexpected | 6 / 1 / 0 / 0 | 7 / 0 / 0 / 0 |

Each walk recovered one HTTP 503 at attempt 2 after 1,000 ms:

| Walk | Context passage under `gis/explorer/context/passages/` | Reserved replay bytes |
| --- | --- | --- |
| Deploy | `408242327c0ceb2882a5701f3b9e1e73cf8675ea86da60c5baa838c1339ee667.txt` | 4,346 |
| Restore | `e0a28308184f23fd661d363163626f7a957fd241d21c15f6a0d6a870809b4714.txt` | 6,371 |

Cancellation and consumed-body counts describe application behaviour, not
unmeasured network prefetch. Restore readiness used two receipt probes / 2,139
bytes within the existing 110,000 ms deadline. All seven restore browser cases
passed first attempt, with zero flaky, skipped or unexpected results and no
mirrored requests or transport failures.

The same selected 8e67 archive was restored; later verifier and documentation
commits do not become the deployed source. This accepts the static public default
and its technical checks. Human learning assessment, wider private acquisition,
the deferred feature's findings, protected-data rights and supported gateway or
hosted-service admission remain separate.
