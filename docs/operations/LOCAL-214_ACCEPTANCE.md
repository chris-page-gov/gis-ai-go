# Local evaluation edition: acceptance and hand-off

Edition proposal: `v0.2.0-local.1`. Software: `0.1.0`. Target: `0.2.0`.
The supported public release remains `v0.1.0`.

[ADR-0017](../decisions/ADR-0017-local-evaluation-edition.md) accepts a separate
local profile, not a waiver of the existing public-service gates. The
[beginner walkthrough](../demonstrations/LOCAL-214_LOCAL_EDITION_WALKTHROUGH.md)
is the first-run route. The machine-readable
[profile](../../evaluation/local-edition-profile.v1.json) names the required gates.

## Exact-artefact record

Create the final acceptance record only for a clean immutable source commit.
Record its full commit and tree, SHA-256 of every distributed artefact and one
entry for each gate. Use the
[acceptance schema](../../schemas/local-edition-acceptance.v1.schema.json), then:

```bash
uv run --locked --cache-dir .uv-cache python scripts/check_local214_profile.py
uv run --locked --cache-dir .uv-cache python scripts/check_local214_profile.py \
  --record artifacts/local214-acceptance.json
```

The second command checks structure, not success. Add `--require-pass` only when
asking whether all recorded gates pass. Neither command authenticates a publisher
or verifies the truth of human/CI attestations: the release reviewer must inspect
each evidence pointer and compare the exact artefact bytes and source identity.
Do not add a self-referential source hash to a tracked acceptance document.

| Gate | Required observation |
| --- | --- |
| Local process | Maintained launcher, exact five tools/three resources, zero guarded provider egress, failed startup, normal stop and temporary-state removal |
| Independent client | Included pinned SDK client completes five calls, three resource classes, distinct recomputable receipts, plain-text parity and three negative cases |
| Expiry | Direct API and MCP tests before, at and after the unchanged cutoff; evidence inspection remains available |
| Source archive | Two identical packages from the same clean commit; extracted source verifies; tamper/extra source/symlink/mode failures are tested |
| macOS and Linux | Separate fresh-source locked install/start/demo/stop observations, with actual OS/architecture/tool versions |
| Dependencies | Advisory-specific disposition, compatible patch, fresh SDK/HTTP, lockfile, SBOM and image assurance |
| A4 print | All pages rendered and inspected at print size; Markdown remains the accessible alternative to the untagged PDF |
| Independent instructions | Clean-room reviewer follows only the published guide; defects and assistance are recorded |
| Unaided colleague | An actual colleague completes the guide without author assistance; an agent review is not substituted |
| Protected main | Required canonical repository/image/provenance and CodeQL checks on the exact accepted source |

Keep missing, failed and unavailable gates explicit. In particular, an unavailable
colleague is not a failed implementation but still prevents full #118 closure and
local prerelease acceptance under the agreed plan. Completed implementation may
be reviewed and merged while that gate remains open.

## Dependency disposition, 24 September 2026

The three medium-severity Hono alerts recorded in AUI-12 were still open when
implementation began. All identified versions below `4.13.5` as affected. The
workspace override and lockfile now pin the compatible `4.13.5` patch, rather than
requesting a risk waiver or dismissing the alerts as unreachable.

| Advisory | Disposition |
| --- | --- |
| [GHSA-gqvv-2mrq-wpjv](https://github.com/honojs/hono/security/advisories/GHSA-gqvv-2mrq-wpjv) | Replace affected dependency; no application `toSSG()` use found in the maintained gateway source |
| [GHSA-crvj-82cr-hjcx](https://github.com/honojs/hono/security/advisories/GHSA-crvj-82cr-hjcx) | Replace affected dependency; the SDK HTTP boundary is relevant, so do not assume local loopback removes parser risk |
| [GHSA-g6gw-c38x-mqfc](https://github.com/honojs/hono/security/advisories/GHSA-g6gw-c38x-mqfc) | Replace affected dependency; no direct application `parseBody()` call found, but no exhaustive transitive reachability exemption is claimed |

These are dependency-remediation decisions, not claims that each published exploit
was reproduced. Close the compatibility gate only with the new SDK/HTTP and
canonical image/SBOM observations. Leave the historical review and old artefact
digests intact. GitHub alert closure is a separate observed scanner state.

## Packaging and publication

The packager accepts only clean committed regular tracked source, checks the
baseline disclosure rules and emits a deterministic source archive, external
manifest and checksum ledger. It excludes installed/generated output and needs
no private evidence store. The archive verifier reconstructs source Git blob,
tree and commit identities; a hash match is not a signature. Compare the named
commit and checksum with the trusted repository/release record before execution.

From a clean source checkout, choose a new output directory outside it:

```bash
python3 -m scripts.local214_package package --output-dir ../local214-package
```

The directory must not already exist. The package includes its verified source
identity, lockfiles, guide sources and illustration sources. Generate the PDF from
that same immutable source, record its input/output hashes and distribute it with
the source package and acceptance record after all gates pass. Do not package
private transcripts, screenshots, host paths or preserved research exclusions.

If and only if acceptance passes, use tag `v0.2.0-local.1`, GitHub prerelease true
and latest false. Check the uploaded asset hashes and release flags. Record the
decision in #118, leaving #23–#25 and the wider #125 programme open.

## Measurement and remaining boundaries

Separate dependency-install, first build/start, subsequent build/start and
five-call latency. A clean checkout with a warm package cache is not a network-cold
install. Report hardware and runtime versions; unknown time or model cost is not
zero. The deterministic demonstration makes no model call and does not validate
any particular AI product's current UI or authentication.

The approved observation expires at `2027-02-20T20:21:08.947Z`; Chris Page owns
reviewed renewal. Receipts are session-only. Browser sign-in to Sites is complete,
but supported direct-client MCP declaration/authentication and wider hosted
acceptance remain separate. Scheduled preservation remains paused.
