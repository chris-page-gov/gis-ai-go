# Dependency security maintenance — 2 November 2026

The candidate updates the split MCP Node adapter to 2.1.0 and client to 2.3.0,
Hono to 4.13.11, its Node server to 2.1.3, the jsdom Undici dependency to
8.12.2, Vite to 8.2.4, matching Vitest packages to 4.1.12 and the optional
chronicle Pillow renderer to 13.0.0. The server remains 2.3.0. Current client
admission and report schemas name 2.3.0; historical observations keep their
original versions.

The full resolved lock and print requirement exclude all 82 affected ranges
in the reviewed alert snapshot. This is dependency presence and version
reconciliation, not evidence of exploitation or a repository-wide security scan.
The existing application request bounds, Host/Origin policy, provider admission
and deployment gates remain required.

Local type checking, gateway TypeScript tests, Explorer unit and browser tests,
synthetic sites and local-client interoperability, public-read policy, contract,
link, secret, SBOM and complete OKF+ verification pass. The optional chronicle
build also produces its review PDF with Pillow 13.0.0. Several complete local
tests require Linux filesystem primitives or the reviewed executable identity;
their macOS failures do not establish a passing canonical run.

The first canonical repository run failed on the changed lock binding in the
mutable, non-live QUAL-206 receipt set. Its existing deterministic generator
regenerates that binding; it does not rewrite historical live observations.
The strict evidence test's expected hash is updated to those reviewed generated
bytes; its classification and all-false live/release claims remain asserted.
The separate gateway image job built and reproduced the OCI image and generated
its SBOM, then failed closed at `node-report-validation`. Its raw scanner output
was withheld by the existing evidence policy. The cause remains unproven;
there is no waiver, passing vulnerability-scan claim or deployment authority.
Full canonical CI, including that image gate, must pass before verification is
complete. No publication, protected-provider request or alert dismissal follows
from this candidate.

The follow-up processing pass corrected the fragment's two top-level bullets;
the checked release format requires one. It also corrected the current workbench
client version in its README. Pinned Linux workspace type checks, dependency
unit suites, the real documented launcher with pnpm 10.33.2 and uv 0.12.2, and
39 receipt/boundary tests passed. The initial launcher attempt used the host's
unmatched tool versions and failed before health; the pinned rerun passed.

Closed static diagnostics preserve the existing privacy checks and failure
stages. In canonical run `41483536290`, image job `125408100424` identified
`privacy-json`: structural report normalisation and cross-format identities
passed before the raw report's privacy check refused it. This does not establish
that the rejected content is benign. Raw scanner output remains withheld and
the image gate remains required. CodeQL passed at `0e7c97cc`.

The subsequent field diagnostic in run `41485303993`, image job `125414919124`,
identified the actual Node report's description for CVE-2026-105482. The
[official October security release](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases)
identifies patched Node.js 24.22.1. The public advisory is HIGH; updating only
description handling would leave the old 24.19.0 runtime vulnerable.

The candidate's exact runtime and receipt schemas now select 24.22.1. Its
upstream archive checksum, extracted binary and licence hashes agree with the
independently pulled official amd64 Docker image. The build/test baseline remains
separate. The actual component uses October's advisory; the historical
24.18.0/24.18.1 calibration still uses July's advisory and its existing HIGH
controls. No finding, severity or calibration rule is suppressed.

The public description contains a literal backslash-zero DNS example. Privacy
decoding interprets that example as a control character. Older calibration
reports can retain the same public prose after the actual runtime is patched.
The compatibility check recognises only its exact 670 UTF-8 bytes and SHA-256,
under the literal `description` key beside the exact CVE identifier. The
[retained public source](../../tests/fixtures/node-runtime-advisory/README.md)
pins the immutable CVEProject commit and complete record checksum; independent
review fetched that commit and reproduced the retained checksum. This establishes
membership of reviewed public bytes, not arbitrary report provenance.

The privacy walker still counts the original bytes, nodes and depth and inspects
all keys, enclosing credential contexts and siblings. Original report bytes,
digests and replay remain unchanged. Standalone prose, changed or appended text,
wrong keys or identifiers, actual NUL and private siblings remain rejected.
The same walker handles parsed and canonical textual evidence, so offline replay
does not require a filename-based exemption. Focused adversarial checks and
independent review passed. Fresh exact-image build, scan, replay and complete
canonical CI remain merge prerequisites.

The first patched-runtime run, `41488623262`, stopped before building the image:
the current third-party notice had changed, while its live entry in
`okf/source-lock.json` retained the older checksum. Refreshing that one binding
restored the deterministic OKF build. The supported local receipt generator
then passed its selected suites and refreshed the two affected material bindings
and their derived suite, receipt and set identifiers. Outcomes, assertions,
classification and historical observation pins remain unchanged.

The next package attempt in `41489523050` exposed a separate exact-size binding:
the root-filesystem verifier still named the old Node binary and licence sizes.
Independent inspection of the checksum-verified 24.22.1 archive measured
126,879,696 bytes for `bin/node` and 157,609 bytes for `LICENSE`, matching their
newly pinned hashes. The candidate now pins those measured sizes explicitly and
rejects the old sizes. No comparison or image-composition requirement is relaxed.

## Accepted PR increment

Exact head `7c36d9711312986efe0999f973c90cfabc87776d` passed complete
[PR CI](https://github.com/chris-page-gov/gis-ai-go/actions/runs/41491411239)
and [CodeQL](https://github.com/chris-page-gov/gis-ai-go/actions/runs/41491400740).
Repository assurance, actual gateway packaging/reproducibility, the 488-component
SBOM, vulnerability scan, container acceptance, offline replay, full Explorer
candidate and aggregate assurance passed. Independent derivation and provenance
are main-event checks and were correctly skipped on the PR event.

[PR #192](https://github.com/chris-page-gov/gis-ai-go/pull/192) merged by squash as
`4573634b822f4d964c91f66380dc702d0ce7e82c`. Dependabot PRs #191, #170, #169,
#166 and #158 were closed with individual comments explaining their replacement.
The requested direct versions are included. PR #170's incidental transitive
refresh was deliberately excluded; the retained pins satisfy Vite 8.2.4's
published ranges. No deployment or alert dismissal is claimed. PR #146 was
left untouched.
