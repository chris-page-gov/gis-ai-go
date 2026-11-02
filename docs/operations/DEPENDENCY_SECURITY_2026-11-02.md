# Dependency security candidate — 2 November 2026

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
