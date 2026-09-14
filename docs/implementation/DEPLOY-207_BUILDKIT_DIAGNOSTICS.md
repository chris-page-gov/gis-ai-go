# Bounded BuildKit failure diagnostics

## Incident and evidence

On 14 September 2026, the two image builds in
[protected-main run 34881074877](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34881074877)
failed during packaging at source commit
`fd8106691bb5c3d63e5f11c21b16f1e7c26f4321`. Both failed again in the one
unchanged-source retry. Source assurance and CodeQL passed. The same Git tree had
passed PR assurance, but the source revision and revision-bound build materials
differed; this was not evidence of identical build contexts.

The helper sent both BuildKit streams to the null device. Its remaining Python
traceback contained a private temporary path and was withheld by the assurance
privacy guard. No retained diagnostic establishes the inner failure cause. Later
public endpoint availability cannot recover that historical fact. There was no
further identical retry.

The following storage increment at
`b9729b5cacc77e9f2b12790c40ad6349fae7b370` passed complete
[protected-main assurance](https://github.com/chris-page-gov/gis-ai-go/actions/runs/34884325687),
including both image derivations, attestation verification and provenance. That
new pass does not retrospectively identify or certify the earlier failure.

## Repair

Only the BuildKit invocation gains a non-blocking, bounded diagnostic collector.
It retains at most 64 KiB per stream while counting all bytes. A failed command
always reports fixed process, stage and error-class fields. Stage and error class
are pattern-based diagnostic hints, not an independently established cause.

An optional excerpt is limited to the final four lines and at most 4 KiB of
escaped published text **per stream**, plus bounded metadata. Exact known build
paths are replaced with labels; existing secret and private-path checks still
apply. Excessive output, invalid encoding, unsafe controls, unexpected private
paths or detected secrets withhold the excerpt. No arbitrary raw log is uploaded.

The existing 30-minute build deadline remains. Process-group termination and
non-blocking drain limits prevent inherited pipes from causing an indefinite
wait. A zero exit with a failed or incomplete stream is not accepted as success.
Successful runs stay silent. Both packaging entrypoints catch the controlled
error without reintroducing a path-bearing traceback.

Build inputs, image composition, pinned versions, integrity checks, independent
derivation and release gates are unchanged. This collector is for the existing
macOS/Linux build environment; it is not a general Windows subprocess adapter.

## Review and verification

A reused agent implemented the isolated patch. Root review found and required
regressions for a zero-exit/read-failure case, a potentially blocking threaded
pipe close and Unicode expansion beyond the rendered-text bound. The final
implementation uses selectors instead of reader threads.

The affected gateway contract and assurance suites passed 115 tests. Eight
focused checks passed after the final output-bound correction. These use local
synthetic subprocesses and mocked packaging, not Docker builds or provider calls.
Canonical PR and protected-main checks remain required before acceptance.
