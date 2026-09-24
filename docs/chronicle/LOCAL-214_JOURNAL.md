# LOCAL-214: turning the local candidate into a colleague-facing edition

Work began on 24 September 2026 and continued on 25 September. This is a public
implementation journal, not a private transcript export. Scheduled preservation
remains paused. The exact acceptance commit and later CI observations belong in
the pull request and #118 record; this file must not hash itself.

## Starting point and decision

The implementation branch began at protected main
`1a824d9af62332529bf57ed4758ecf51be9c7af0` (#136). The owner selected #118 while
the wider hosted MCP question remained unresolved. The original checkout and
source repositories were left untouched; work used a separate worktree.

The substantive distinction was not “local means released”. LOCAL-212 already
supplied a loopback-only exact-five server. LOCAL-214 needed a reproducible
first-run artefact, clear lifetime information, an independent demonstration and
instructions that do not depend on this conversation. ADR-0017 keeps that edition
separate from the supported public service and keeps the actual unaided colleague
test as an explicit remaining gate if no colleague is available.

## Parallel work with bounded ownership

The lead model delegated three independent roles: local runtime/lifetime tests,
source packaging and the demonstration client, and the illustrated guide. The
lead owned the release profile, tracking corrections, dependency patch and
integration. A completed runtime worker was reused to review the separately
authored package/client/profile. Three delegated workers is not a claim about
the historical agent total or concurrent activity in earlier development.

This division kept file ownership explicit. Builds were coordinated because the
real launcher acceptance checks that tracked source does not change while the
server runs. The guide used vector illustrations rather than invented client
screenshots; its PDF has an accessible Markdown alternative.

## Changes and observations

- The existing approved-cache rejection was already correct at the expiry
  instant. The missing feature was visible capability status. A separate local
  field now exposes immutable source vintage, approval and expiry. Assembly
  readiness is not redefined as a claim that statistics are current.
- An internal constructor clock allows direct/MCP before/at/after tests without
  changing the system clock, exposing an override or extending the approval.
  Session receipt inspection remains available after expiry.
- The three open Hono dependency alerts shared one patched version. The update
  pins `4.13.5`; a production dependency audit reported no known vulnerabilities
  for that locked tree. This does not replace canonical image/SBOM checks or prove
  the absence of unknown vulnerabilities.
- The source packager rejects dirty source, links, unexpected source, mode changes
  and tampered blobs. Its archive includes a reconstructable Git identity, not
  trusted prebuilt JavaScript. Installed/generated directories are explicitly
  outside source-only verification.
- The first development client observation completed the five-tool path and
  three refusal cases in 15 wire requests. Initial assertions had incorrectly
  expected an operation field in two closed error families; those assertions were
  corrected against the actual schemas. That development run was not promoted
  into exact-source release acceptance.

## What independent review caught

The review found four concrete acceptance defects before integration:

1. A receipt's own valid digest did not establish its relationship to the current
   request, trace and result. The client now checks those links and recomputes the
   result-core digest; mutation tests substitute otherwise-valid receipts.
2. A compatible older server could pass without proving it served this source.
   The client now verifies local source identity, checks receipt software revision
   and retains the checked public results/receipts for inspection after shutdown.
3. The local profile checker omitted the `latest_supported_release` field.
   Validation now preserves the stable `0.1.0` boundary explicitly.
4. A structurally passing acceptance record could contain only an unrelated
   artefact hash. The schema now requires the actual source package, checksum
   ledger, package manifest, PDF and guide manifest.

These findings illustrate why tests of a verifier matter as much as a verifier's
happy-path output. The acceptance checker still cannot authenticate a human
attestation or prove that an external CI URL contains the claimed result. Those
remain explicit release-review responsibilities rather than hidden automation
claims.

The first PR CodeQL gate additionally flagged a test that wrote a deliberately
fabricated token-shaped string into a temporary repository. No real credential
was involved. The regression was changed to exercise the same scanner directly
in memory, avoiding clear-text persistence without dismissing the alert or
weakening production scanning. The changed commit requires fresh canonical checks.

An independent instruction-only reviewer completed the documented journey from a
fresh extraction of `9c1a1dfb1aa8ac350fc999490e935b16227bde10`, retaining the
checked result and observing orderly stop. That is an agent engineering review,
not the unaided colleague gate. It identified conflicting prerequisite wording
between the new guide and the older runbook. Both now distinguish Node's minimum,
the reproducible CI baseline and the actually observed newer macOS version.

Canonical repository assurance then rejected stale deterministic QUAL-206
material hashes after the package scripts, lockfile and HTTP health source changed.
The maintained generator reran its selected suites and refreshed the seven
non-live, unscored receipts. The diff changes only source hashes and derived
identities; it does not change assertions, outcomes, approval dates or authority.
This integration omission was caught by the required check, not a live client
failure. Historical commits retain the preceding receipt bytes.

## Tracking and remaining work

#125 was reopened because its aggregate OS/ONS/workbench milestones were not all
complete. Its bounded local CPIH slice is distinguished from the unfinished
geospatial join, wider stories and hosted acceptance. Documentation now records
that Sites browser authentication succeeded on 19 September; supported direct
MCP declaration/authentication remains the different unresolved dependency.

Follow the [acceptance policy](../operations/LOCAL-214_ACCEPTANCE.md) for current
gates, and the [walkthrough](../demonstrations/LOCAL-214_LOCAL_EDITION_WALKTHROUGH.md)
for a repeatable demonstration. Exact source, observed tool/OS versions, timing,
check results and any remaining operator action must accompany acceptance.
An automated clean-room check is not human research. Unavailable cost or timing
is not zero, and no token-cost estimate is inferred from the number of agents.
