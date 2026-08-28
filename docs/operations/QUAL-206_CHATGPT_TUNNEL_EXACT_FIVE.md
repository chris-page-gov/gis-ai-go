# QUAL-206 ChatGPT secure-tunnel exact-five observation

- status: evidence pack only; no exact-five ChatGPT observation or public pass
  is included in these bytes
- host lane: ChatGPT remote host through the OpenAI secure tunnel
- local child transport: operating-system STDIO pipes
- direct public Streamable HTTP over TLS: not exercised
- provider: one deterministic synthetic response; guarded live-provider calls must
  remain zero
- production registration, activation, deployment and release: not exercised

## Purpose

This runbook prepares one bounded ChatGPT observation of the unchanged
`exact-five-v1` capability profile. It is additive to the accepted Claude Code
local STDIO result. It does not change, repeat or relabel that result.

The observation can establish only this narrow claim:

> ChatGPT, acting as a remote host through the reviewed OpenAI secure tunnel,
> completed the five ordered MCP `2026-07-28` calls through one byte-bound local
> STDIO observer to a separate network-denied deterministic fixture/server.

It cannot establish a direct public MCP endpoint, public hostname, product TLS
ingress, live geospatial-provider operation, registry publication, activation,
deployment or release. The public projection keeps each of those claims false.

## Why the pack is merged before the observation

The observer, schemas, result checker, independent verifier and mutation tests must
first pass review on protected `main`. The live step must then use a new clean,
detached worktree at that exact protected-main commit. This avoids using unreviewed
capture code and prevents a later commit from being attributed to an earlier run.

Use two pull requests:

1. merge this evidence-preparation pack with no live result;
2. make one bounded observation from exact protected `main`, independently verify
   the private capture, then submit only the minimised public projection.

Do not make the live observation from the pack branch.

## Frozen profile

The host-facing profile is
[`qual_206_chatgpt_tunnel_exact_five_profile.v1.json`][profile].
It presents no built-in tools or resources and requires these calls in order:

1. `catalogue.search`;
2. `catalogue.describe`;
3. `selection.resolve`;
4. `data.query`;
5. `evidence.inspect`, using the receipt ID returned by `catalogue.search`.

All five calls must occur in one call-bearing MCP session. Up to eight contiguous
session slots are available because the host may open separate discovery-only
sessions. A second call-bearing session, wrong call order, duplicate call, sixth
call, changed schema or missing receipt relationship fails the global claim.

Tool names and schemas pass through unchanged. This lane does not apply the
Claude-specific tool-name projection and does not attach Claude terminal or model
response semantics to ChatGPT.

## Reviewed tunnel client

Use only official `openai/tunnel-client` `v0.0.13` for this observation:

- release:
  [`v0.0.13`](https://github.com/openai/tunnel-client/releases/tag/v0.0.13);
- source comparison:
  [`v0.0.12...v0.0.13`](https://github.com/openai/tunnel-client/compare/v0.0.12...v0.0.13);
- archive SHA-256:
  `15abf165f06050af642c948ba6bd6c905191dc5420a9422dadde2b49d892e2c6`;
- `SHA256SUMS.txt` SHA-256:
  `e6495395e8f5d952b0edc34a0b552426e38472973a7602f94b3868fbcd9aceb4`;
- extracted Darwin arm64 binary bytes: `20336818`;
- extracted binary SHA-256:
  `814b5e7ad378e6dfeb7eeebf12df37ff879cfe58fd504769cabfc3e3b4cf99f6`;
- exact reported version:
  `0.0.13+4b5267f823be0b046bb883aacb51603cfde3a0ea`
  `(git sha: 4b5267f823be0b046bb883aacb51603cfde3a0ea)`.

This update is material: it includes STDIO lifecycle and shared-connection changes.
The harness independently remeasures the executable and refuses any other bytes or
reported build. The earlier `v0.0.12` observations remain historical and are not
upgraded by this pack.

## Private and public material

Use two new, separate owner-only roots outside the repository:

- the **capture root** contains only the allowlisted event/session files, global
  claim, before/after/stopped status envelopes and final run manifest;
- the **operator root** contains the generated tunnel profile, state and raw local
  tunnel-client output.

The two roots must be new sibling directories under one pre-existing, owner-only
`0700` parent. Both roots are `0700`; retained files are `0600`. The operator root can contain
local paths, endpoints and process details and must never be committed. The capture
root also remains private. Only the independent verifier's path-free projection may
enter `tests/interoperability/evidence/`.

The projection excludes prompts, complete arguments and results, paths, endpoints,
ports, PIDs, request/session/run identifiers, conversation URLs and credentials.

## Preflight after the pack is merged

Fetch protected `main`, create a new detached worktree and confirm the commit is the
same as `origin/main`:

```bash
git fetch origin main
git worktree add --detach <new-worktree> origin/main
cd <new-worktree>
test "$(git rev-parse HEAD)" = "$(git rev-parse origin/main)"
test -z "$(git status --porcelain=v1 --untracked-files=all)"
```

This evidence lane is deliberately narrower than the repository's general Node
support. It requires the reviewed local macOS toolchain: Node `v26.7.0` (50,320
bytes, SHA-256
`1ef99ea25fe70c9b67e7efe768ef8ee22148d3cabc703db6131b57aeb617d040`), pnpm
`10.33.2`, and `/usr/bin/sandbox-exec` (102,560 bytes, SHA-256
`8290e4be7387a0df83cd1559e86afd880464f269450573d012795761fe298f16`).
The harness binds the pnpm wrapper, bundled distribution and complete 1,073-entry
package runtime rather than trusting `PATH`. Supply the reviewed Node and pnpm paths
explicitly; do not derive the pnpm path from `PATH` in this evidence lane. If a
macOS, Node or pnpm update changes these identities, stop and review the new
toolchain in a separate change; do not edit a pin during an observation.

Confirm the selected runtimes before building:

```bash
export QUAL206_NODE=<canonical-reviewed-node-v26.7.0-binary>
export QUAL206_PNPM=<canonical-reviewed-pnpm-10.33.2-wrapper>
export QUAL206_PNPM_ROOT="$(cd "$(dirname "$QUAL206_PNPM")/.." && pwd -P)"
export QUAL206_PNPM_DIST="$QUAL206_PNPM_ROOT/dist/pnpm.cjs"

test "$(stat -f %z "$QUAL206_NODE")" = "50320"
test "$(shasum -a 256 "$QUAL206_NODE" | cut -d ' ' -f 1)" = \
  "1ef99ea25fe70c9b67e7efe768ef8ee22148d3cabc703db6131b57aeb617d040"
test "$("$QUAL206_NODE" --version)" = "v26.7.0"
test "$(stat -f %z "$QUAL206_PNPM")" = "1102"
test "$(shasum -a 256 "$QUAL206_PNPM" | cut -d ' ' -f 1)" = \
  "b276da51dc8ca5b0d3ee3371695b50fc8b3244b281b091c63a3f082a88dadeb9"
test "$(stat -f %z "$QUAL206_PNPM_DIST")" = "7844838"
test "$(shasum -a 256 "$QUAL206_PNPM_DIST" | cut -d ' ' -f 1)" = \
  "a04379c877cf74b4cbc585ab3a14fd52eea2d52b5aa0fb854cbd4485cd73b347"
test "$(stat -f %z /usr/bin/sandbox-exec)" = "102560"
test "$(shasum -a 256 /usr/bin/sandbox-exec | cut -d ' ' -f 1)" = \
  "8290e4be7387a0df83cd1559e86afd880464f269450573d012795761fe298f16"

"$QUAL206_NODE" --input-type=module --eval '
  import { verifyPnpmRuntime } from
    "./scripts/qual_206_claude_capability_harness.mjs";
  verifyPnpmRuntime(process.argv[1], process.execPath);
' "$QUAL206_PNPM"
```

Build the runtime materials the observer imports:

```bash
"$QUAL206_NODE" "$QUAL206_PNPM_DIST" \
  install --offline --frozen-lockfile --ignore-scripts --ignore-pnpmfile \
  --package-import-method=copy --verify-store-integrity
uv sync --locked --offline
"$QUAL206_NODE" "$QUAL206_PNPM_DIST" run build:okf
"$QUAL206_NODE" "$QUAL206_PNPM_DIST" --filter @gis-ai-go/contracts run build
"$QUAL206_NODE" "$QUAL206_PNPM_DIST" --filter @gis-ai-go/evidence run build
"$QUAL206_NODE" "$QUAL206_PNPM_DIST" --filter @gis-ai-go/authority-context run build
"$QUAL206_NODE" "$QUAL206_PNPM_DIST" --filter @gis-ai-go/policy-client run build
"$QUAL206_NODE" "$QUAL206_PNPM_DIST" --filter @gis-ai-go/provider-adapter-sdk run build
"$QUAL206_NODE" "$QUAL206_PNPM_DIST" --filter @gis-ai-go/tool-registry run build
"$QUAL206_NODE" "$QUAL206_PNPM_DIST" --filter @gis-ai-go/mcp-gateway run prepare:test
"$QUAL206_NODE" "$QUAL206_PNPM_DIST" --filter @gis-ai-go/mcp-gateway run build
```

Run the focused offline pack checks before opening a tunnel:

```bash
"$QUAL206_NODE" --test \
  tests/interoperability/test_qual_206_chatgpt_tunnel_exact_five_harness.mjs \
  tests/interoperability/test_qual_206_chatgpt_tunnel_exact_five_observer.mjs
.venv/bin/python -m unittest \
  tests.contract.test_qual_206_chatgpt_tunnel_exact_five
```

The macOS observer test intentionally checks the real parent process and may need
local process-inspection permission. Do not remove that check to make a sandboxed
test pass. Linux CI does not exercise the macOS process-parent, network-sandbox or
finaliser runtime path, so retain the successful macOS output with the private
operator record before the observation.

## Prepare the bounded runtime

The existing authorised tunnel is:

- remote name: `gis-ai-go-v0-2-interoperability`;
- remote ID: `tunnel_6a873e7214308191bfe27240c1c03f68`.

The pack deliberately uses the fresh local alias and profile
`gis-ai-go-v0-2-exact-five-v1`. Supply the runtime key only by environment
reference. Prefer `CONTROL_PLANE_API_KEY`; do not pass its value on a command line,
write it to the repository or expose it to the observer/MCP child.

Create one new owner-only parent, reserve two not-yet-created sibling paths beneath
it, and create a lowercase UUID v4. Then run the non-networking prepare phase:

```bash
export QUAL206_PRIVATE_PARENT="$(mktemp -d /private/tmp/gis-ai-go-qual206.XXXXXX)"
chmod 700 "$QUAL206_PRIVATE_PARENT"
export QUAL206_CAPTURE_ROOT="$QUAL206_PRIVATE_PARENT/capture"
export QUAL206_OPERATOR_ROOT="$QUAL206_PRIVATE_PARENT/operator"
export QUAL206_RUN_ID=<lowercase-uuid-v4>
export QUAL206_SOURCE_COMMIT="$(git rev-parse HEAD)"
export QUAL206_TUNNEL_CLIENT=<absolute-reviewed-v0.0.13-binary>
export GIS_AI_GO_QUAL_206_CHATGPT_TUNNEL_EXACT_FIVE_HARNESS=1

"$QUAL206_NODE" scripts/qual_206_chatgpt_tunnel_exact_five_harness.mjs \
  --chatgpt-tunnel-exact-five-harness-only \
  --phase prepare \
  --capture-root "$QUAL206_CAPTURE_ROOT" \
  --operator-root "$QUAL206_OPERATOR_ROOT" \
  --run-id "$QUAL206_RUN_ID" \
  --source-commit "$QUAL206_SOURCE_COMMIT" \
  --client "$QUAL206_TUNNEL_CLIENT" \
  --pnpm "$QUAL206_PNPM" \
  --runtime-key-env CONTROL_PLANE_API_KEY
```

The prepare phase requires a clean detached checkout at exact `origin/main`, verifies
the repository origin and pins the executable. It also rebuilds the generated
first-party runtime under network denial, reconstructs a second dependency tree
from the tracked lockfile with scripts and pnpmfile hooks disabled, and compares its
package content with the installed runtime before executing that content. It invokes
the reviewed pnpm distribution through pinned Node only after its wrapper,
distribution and complete package closure match the reviewed identity, then
remeasures them after the version check. `--pnpm` must be the existing canonical
absolute path exported above; the prepare phase does not select a package manager
from ambient `PATH`. The build directly invokes the matched TypeScript compiler
rather than generated `.bin` shims. The exact generated and installed-dependency
closures are then bound into the observer command. It writes a private plan but does
not connect to OpenAI.

## Connect and attest readiness

With `CONTROL_PLANE_API_KEY` present only in the parent environment, connect:

```bash
"$QUAL206_NODE" scripts/qual_206_chatgpt_tunnel_exact_five_harness.mjs \
  --chatgpt-tunnel-exact-five-harness-only \
  --phase connect \
  --operator-root "$QUAL206_OPERATOR_ROOT"
```

The harness supplies exactly one `--mcp-command`; it never supplies
`--mcp-server-url`. The command starts with `/usr/bin/env -i`, so the local observer
and fixture receive no recognised provider credential. The tunnel client executes
that argv directly; the observer binds its immediate parent to the reviewed
`v0.0.13` bytes.

In this evidence contract, **MCP child** means the downstream deterministic GIS AI GO
fixture process that the credential-free observer starts. It does not mean the
observer that the tunnel client starts directly. The observer is byte-bound and
receives no recognised credential, but the network-sandbox claim applies only to
that downstream fixture: the observer starts it through the reviewed macOS
`sandbox-exec` deny-network profile. Accordingly, every `mcp_child_network_*` field
describes the fixture process and must not be read as a claim that the immediate
observer process is itself network-sandboxed.

Connect success is insufficient by itself. The harness obtains a fresh JSON status,
then invokes the reviewed client's credential-free
`health --url-file ... --pid ... --require-control-plane-poll --json` probe before
it emits an endpoint-free `tunnel-status-before.json`. It requires:

- exact local alias, remote tunnel ID and remote name;
- the fixed profile and SHA-256 digest of the exact reviewed MCP command;
- successful remote lookup with no local or remote error and no stale state;
- managed process running, runtime state `ready`, healthy and ready true;
- effective local `/healthz` and `/readyz` status `200`; and
- one recent successful control-plane poll, proved by a positive
  `commands_poll_last_successful_timestamp_seconds` metric from the exact bound
  loopback runtime. The timestamp must be an integer no more than 120 seconds old;
  only 5 seconds of future clock skew is tolerated.

In tunnel-client `v0.0.13`, `runtimes status` can legitimately report
`state: unknown` with `no live admin UI system snapshot` for the current managed
runtime even when its local endpoints are ready. The harness does not turn that
unknown state into a pass. It keeps the status identity checks and uses the
client's purpose-built poll probe as the independent readiness condition. The
probe receives no runtime credential, must resolve the exact owner-only health URL
file to `127.0.0.1`, must confirm that the exact managed process ID is still
running, and must return healthy `200` responses from both endpoints.

The poll probe allows up to eight attempts, separated by 5 seconds, so the bounded
window covers the reviewed client's 30-second long poll and 5-second deadline
guardrail. Each probe command also has a 5-second execution cap. It
retries only the exact first-party `no successful control-plane poll observed`
startup result. Missing metrics, locator drift, endpoint failure, malformed output,
stderr, a different error or any other exit fails closed and triggers the normal
automatic teardown. The isolated tunnel process receives no proxy environment and
the generated control-plane profile has no proxy configuration, so a successful
poll remains bound to the direct control-plane route.

Any mismatch fails closed.

## Refresh the ChatGPT app before use

In ChatGPT developer mode, refresh or recreate the version of app
`GIS AI GO v0.2 interoperability` for app ID
`asdk_app_6a873f853628819184bccb4a9b961576`, selecting the exact tunnel above.
Before prompting, inspect the refreshed app and confirm that it presents exactly the
five canonical operations with their closed schemas. Record the displayed non-secret
`asdk_app_v_...` identifier. ChatGPT refreshes the developer connection in place, so
that identifier is not an immutable tool-surface version and may remain unchanged.
The captured, exact `tools/list` result is the authoritative schema evidence.

## One bounded host observation

[The MCP 2026-07-28 request identifier rule][mcp-basic] applies to requests that
are still outstanding. The observer accepts an identifier reused only after the earlier
response has completed. Simultaneous reuse, an orphan response or a duplicate
response fails closed. `request_id_unique: true` records that no request with
the same identifier was awaiting a response when the request was issued.

Start a new ChatGPT conversation and select only the refreshed GIS AI GO app. Keep
the full prompt and conversation identifier private. In substance, instruct ChatGPT
to use only that app, make the five profile calls in their listed order, use the
search receipt for `evidence.inspect`, use no web search or other tool, and report
completion without inventing a value.

Observe the model label displayed by ChatGPT. Do not infer an internal model name
that the interface does not show.

The observer permits discovery-only connections but creates the global claim only
for one complete call-bearing session. A failed attempt does not produce a public
pass. Do not edit the capture to repair it; use a new run ID and new roots for any
authorised repeat.

Immediately after the host finishes, obtain the second attested status:

```bash
"$QUAL206_NODE" scripts/qual_206_chatgpt_tunnel_exact_five_harness.mjs \
  --chatgpt-tunnel-exact-five-harness-only \
  --phase status-after \
  --operator-root "$QUAL206_OPERATOR_ROOT"
```

## Stop and prove teardown

Stop the exact managed alias before finalisation:

```bash
"$QUAL206_NODE" scripts/qual_206_chatgpt_tunnel_exact_five_harness.mjs \
  --chatgpt-tunnel-exact-five-harness-only \
  --phase stop \
  --operator-root "$QUAL206_OPERATOR_ROOT"
```

Run this immediately after the second ready-status attestation. Do not wait for the
persistent ChatGPT transport to close itself: it remains open after the fifth
response and would reach the fail-closed inter-frame deadline.

During a managed stop, the pinned tunnel client `v0.0.13` can first forward a host
`SIGTERM`, then have its STDIO OnStop hook close observer stdin and send a second
`SIGTERM`. The observer treats the first signal as the causal teardown stimulus and
absorbs the duplicate idempotently; it does not emit a second lifecycle event. EOF
can also arrive before the first signal. The observer distinguishes and records both
valid causal orderings: `stdin-eof-and-sigterm` when EOF arrives first, and
`sigterm-then-stdin-eof` when EOF arrives within the bounded 250-millisecond grace
after the first signal. It still requires EOF before accepting teardown. A signal
without EOF before that grace expires, a partial frame, an incomplete call or any
request still in flight remains a fatal anomaly. This bounded delivery grace changes
no call, result, receipt or publication predicate.

The stop is local and credential-free. It re-verifies the pinned tunnel-client
bytes, requires the exact profile and command digest, and writes
`tunnel-status-stopped.json`. That envelope must show the process stopped, health
and readiness false, no remote lookup, and no claim that the remote tunnel was
removed. Do not finalise or publish evidence without it.

Do not install a pending operating-system or application update, restart the Mac or
otherwise change the reviewed toolchain while the live observation is running. An
update is safe only after the managed observation has stopped and its private
capture and operator records have been persisted.

## Finalise and independently verify

Hash the private conversation identifier locally; pass only the SHA-256 digest to
the finaliser. Use UTC timestamps from the private operator record for the bounded
host observation window. The ready `before` and `after` status observations must
bracket those timestamps and every host protocol request and response. Observer
startup and readiness audit events may precede the host window; managed teardown,
stream closure and summary events may follow it. Then create the immutable private
run manifest:

```bash
.venv/bin/python \
  scripts/finalise_qual_206_chatgpt_tunnel_exact_five.py \
  --private-root "$QUAL206_CAPTURE_ROOT" \
  --node "$QUAL206_NODE" \
  --pnpm "$QUAL206_PNPM" \
  --started-at <UTC-start> \
  --finished-at <UTC-finish> \
  --displayed-model <operator-observed-model-label> \
  --app-version-id <operator-observed-asdk-app-version-id> \
  --conversation-id-sha256 <sha256>
```

Run the independent verifier and publish to a new evidence filename only:

```bash
.venv/bin/python \
  scripts/verify_qual_206_chatgpt_tunnel_exact_five.py \
  --private-root "$QUAL206_CAPTURE_ROOT" \
  --node "$QUAL206_NODE" \
  --pnpm "$QUAL206_PNPM" \
  --output "$(pwd -P)/tests/interoperability/evidence/<new-public-filename>.json"
```

The verifier independently replays the event chain and every result contract,
checks the five distinct receipts and inspection relationship, remeasures all bound
source/runtime files, verifies all three tunnel statuses and scans the projection for
private fields. It publishes a pass only. A failure leaves no public output.

Review the new projection deliberately before committing it. The evidence-only pull
request must bind its parent protected-main commit and must not contain the capture
or operator roots.

Confirm the app no longer reaches the local runtime. Keep the complete private
capture and operator material local until the owner specifies a private destination.
Do not delete, publish or move it as part of the evidence pull request.

## Stop conditions

Do not publish a pass if any of these occurs:

- the checkout is not clean, detached and exact protected `main`;
- client bytes or reported build differ from the reviewed `v0.0.13` identity;
- the refreshed app or captured `tools/list` presents anything other than the exact
  five-tool surface;
- either ready-status attestation fails, remote identity drifts, or the stopped
  attestation does not prove local teardown;
- the host splits the five calls across sessions, changes order, duplicates or adds
  a call;
- any advertised schema differs from the canonical profile;
- the search receipt is not the receipt inspected;
- the fixture sees a credential, permits network access or records a guarded live
  provider call;
- raw material, a path, endpoint, port, process/request/session/run identifier or
  conversation identifier enters the public projection; or
- the independent verifier or protected-main checks fail.

None of these stop conditions is grounds to weaken a schema or verifier.

[profile]: ../../tests/interoperability/fixtures/qual_206_chatgpt_tunnel_exact_five_profile.v1.json
[mcp-basic]: https://modelcontextprotocol.io/specification/2026-07-28/basic
