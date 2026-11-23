# Gateway image security maintenance — 23 November 2026

The standards-reference PR exposed a gateway image assurance failure at
`node-report-validation`. The bounded diagnostic identified the actual Node
report's description for CVE-2026-123864. The retained public CVE record
reproduces that privacy rejection. The [November Node.js security advisory](https://nodejs.org/en/blog/vulnerability/november-2026-security-releases)
also identifies 24.22.3 as the patched 24.x release, so the earlier 24.22.1
runtime needs updating independently of description handling.

The candidate updates the donor image, exact Node version, PURL, CPE, binary
hash and size, upstream archive checksum, receipt and scan schemas, and closed
runtime instruction identity together. The original runtime instruction
sequence was checked against its retained hash. Its new sequence differs only
in the Node version and binary checksum. Existing composition, filesystem,
network, licence, non-root execution and admission checks remain active.

The official Node release archive has SHA-256
`4f2b175a6d53a5c617a80dba2676238a0688cef28c6da4eba35c7d844e66fcfb`.
Its `bin/node` is 126,891,984 bytes with SHA-256
`a7ec1b37e6ff9d187e4198c5b6df9a4eb1c74dd31804fb3bac55cc4ceca1ac01`.
Both the binary and complete licence match the independently retrieved official
Docker image's amd64 layers. The licence bytes and existing GCC/UBI inputs are
unchanged. `THIRD_PARTY.md` and its live source-lock binding are updated together.

The [public advisory fixture](../../tests/fixtures/node-runtime-advisory/README.md)
pins the exact source record and description bytes. The privacy walker recognises
those bytes only under the literal `description` key beside that exact CVE ID.
It retains byte, node and depth limits, enclosing credential checks and sibling
inspection. Changed prose, standalone descriptions, other IDs and keys, actual
control bytes and private siblings remain rejected. The unchanged raw scanner
reports retain their original hashes for replay. No finding or severity is
suppressed; older calibration scans may still contain this advisory after the
actual runtime is patched.

Local regression checks cover both report formats and canonical text, malicious
mutations, ordinary report handling and the exact image contract. Passing those
checks does not establish Linux image acceptance. Exact-image construction,
reproducibility, SBOM, vulnerability scan, container acceptance, offline replay
and complete canonical CI must pass before merge. Independent main-event
derivation and provenance remain separate. No provider call, deployment,
registration, release or alert dismissal follows from this source repair.

The first candidate passed exact Linux image packaging, reproducibility, the
488-component SBOM, vulnerability scanning and retained offline replay in
[run 45181630703](https://github.com/chris-page-gov/gis-ai-go/actions/runs/45181630703).
Container acceptance then failed with its traceback withheld by the privacy
guard. The CLI now emits only closed stage and reason codes on failure, including
the two existing health-readiness deadlines. Unknown failures receive a fixed
unknown code; paths, exception text and environment values are never emitted.
The parent runner forwards only one valid closed code from bounded, privacy-safe
stderr in the failed acceptance phase. It rejects malformed or duplicate codes
and codes appearing in stdout, and still fails the phase.
Library exceptions and cleanup remain intact. The full acceptance gate remains
required and failed evidence cannot be promoted.

The next candidate completed the runtime phases but failed while finalising the
receipt. Schema failures now identify only the index of a matching node in the
reviewed public acceptance schema. The finite code list is shared with the
parent runner; receipt values, instance paths and validator messages remain
withheld. Unrecognised schemas receive a fixed unknown code. This diagnostic
preserves the original validation exception and does not permit an invalid
receipt to be written or promoted.
