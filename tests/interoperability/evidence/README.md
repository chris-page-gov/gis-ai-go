# Live-host evidence boundary

This directory contains reviewed, public-safe summaries of bounded interoperability
sessions. A summary may contain non-secret tunnel and app identifiers, public query
terms, result identities, timings, byte counts and SHA-256 digests.

It must not contain raw prompts, complete tool arguments or results, credentials,
headers, environment values, personal data, local absolute paths, conversation URLs
or licensed feature payloads. Detailed JSONL and tunnel-client logs remain local and
operator-controlled. ChatGPT and Codex session summaries bind the exact runtime
harness files used for their runs. An earlier readiness-only summary may instead
identify its pre-final wrapper generation and must not imply that current harness
bytes were exercised. A separately labelled evaluation-corpus digest may identify
the current reviewed case set, but must state that the corpus was not a live-session
runtime input.

Independent-host readiness summaries may preserve versions, bounded classifications,
event counts, timings and digests after disposable profiles are removed. They must
distinguish readiness from capability, record zero-traffic outcomes honestly and state
whether the exact current telemetry wrapper was exercised.

The [`Codex CLI readiness summary`](codex-cli-2026-08-20.json) records the isolated
non-interactive host attempt separately from the earlier three-host readiness summary.
It binds the exact corpus case and current wrapper bytes, but remains `not_ready` and
unscored because protocol negotiation stopped before a task-level tool call.
