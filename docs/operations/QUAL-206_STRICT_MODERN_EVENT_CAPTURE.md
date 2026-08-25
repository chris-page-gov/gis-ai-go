# QUAL-206 strict-modern private event capture

This runbook covers the closed, private event collector for one MCP `2026-07-28`
exact-five STDIO session. The collector is an assurance component, not a host and
not public evidence. Its repository test uses a synthetic raw Node.js client so it
cannot establish independent desktop-host capability.

## Current claim boundary

The collector can record and the separate verifier can replay this exact journey:

| Stage | Required observation |
| --- | --- |
| Opening | `server/discover` advertises only MCP `2026-07-28` |
| Discovery | complete, unpaginated `tools/list` returns the unique five-operation set with the exact canonical input and output schemas; complete resource discovery returns one concrete catalogue and two templates |
| Resources | one full checksum-bound public catalogue, its exact catalogue record and one complete dependent evidence receipt are read successfully |
| Operations | `catalogue.search`, `catalogue.describe`, `selection.resolve`, one successful `data.query` and `evidence.inspect` all pass their canonical output schemas, deterministic checks and structured/plain-text parity |
| Cancellation | a second `data.query` starts its provider transport, is cancelled and produces no response |
| Unsupported surface | `prompts/list` returns exact JSON-RPC error `-32601` |
| Close | all four captured streams close, the child exits successfully, stderr is empty and temporary evidence state is removed |

That is 14 unique requests, 13 responses and one cancellation notification in one
session. The fixed fixture must also report two provider-transport starts, one
abort, four ledger events, no reported errors and no calls to the guarded network
APIs.

A passing capture still records:

- `capability_scored: false`;
- `exact_five_host_capability: false`; and
- `source_binding_ready: false`.

Those values are constants, not operator choices. `local_checkout_candidate_ready`
can be true only when the checkout is clean and detached, its `HEAD`, supplied
commit and local `refs/remotes/origin/main` agree, and the selected first-party
runtime files remain stable. This is a local remote-tracking-ref candidate, not
proof of the protected remote branch. It does not close source binding: installed
third-party runtime bytes are not yet in the closed material set.

## Trust and privacy boundaries

The collector binds the immediate parent executable, hashes the Node.js executable
it intends to spawn, and binds its own source, the exact-five fixture, the egress
guard and the selected first-party runtime material before and after the session.
It records that the fixed spawn arguments were used, but records
`spawned_process_identity_verified: false`: it does not independently inspect the
spawned process identity or loaded third-party runtime. It launches the fixture
directly, with a closed environment and no forwarded credentials, over
operating-system STDIO pipes. Limits cover frame size, event count, log bytes,
stderr, idle time and whole-session time.

Each canonical event binds the preceding event. The final owner-only manifest binds
the whole log, final event, byte count and event count. The independent verifier
reopens both files without following links, validates their closed schemas,
recomputes the chain and manifest, and replays the journey projections and outcome.
Neither file is public evidence.

Request identifiers, parameters and frames are hashed rather than written in raw
form. This is pseudonymisation, not anonymisation: known or low-entropy traffic may
still be linkable. Keep the event log and manifest together in a private directory
outside the repository, do not commit them and do not paste them into issues or CI
logs. The directory must be owned by the current user with mode `0700`; both new
files must have mode `0600` and one hard link.

## Run the repository assurance

Build the gateway first, then run the synthetic raw-client journey and the separate
verifier tests:

```bash
pnpm --filter @gis-ai-go/mcp-gateway run prepare:test
pnpm --filter @gis-ai-go/mcp-gateway run build
pnpm --filter @gis-ai-go/tool-registry run build
node --test tests/interoperability/test_qual_206_exact_five_stdio.mjs \
  tests/interoperability/test_qual_206_event_collector.mjs
uv run --locked --cache-dir .uv-cache python -m unittest \
  tests.contract.test_qual_206_strict_modern_host_events
```

The interoperability test creates and removes its own private capture. It proves the
collector and deterministic fixture work together; the client label in that test is
explicitly synthetic.

## Verify a retained private capture

Verification is read-only and produces no evidence artefact:

```bash
uv run --locked --cache-dir .uv-cache python \
  scripts/verify_qual_206_strict_modern_host_events.py \
  --event-log /absolute/private/path/events.jsonl \
  --manifest /absolute/private/path/manifest.json
```

The two paths must be distinct siblings under the same canonical private directory.
The verifier fails closed on malformed or non-canonical JSON, schema drift, a broken
event chain, mixed sessions, incomplete streams, journey or audit drift, a changed
file, unsafe permissions, a forged pass summary or a manifest mismatch.

## Independent-host use

For an actual desktop host, configure the collector directly as the MCP server
process. Do not insert a shell between the host and collector. Supply the expected
digest and byte length of the immediate host executable, a full source commit whose
protected-main status has been established separately, new absolute private output
paths and a fixed allowlisted client label. The collector's local
`origin/main` comparison is not that remote proof. Set
`GIS_AI_GO_QUAL_206_EVENT_CAPTURE=1` only for that bounded run.

Before treating any run as acceptance evidence, review the process tree to confirm
that the measured immediate parent is the intended host executable. A launcher,
helper, extension host or shell is a different attribution and must be described as
such. Retain the raw capture privately and publish only a separately compiled,
allowlisted projection.

This single-session route is not suitable for Claude Code `2.1.241`. Its automatic
modern STDIO negotiation launches a disposable `server/discover` process before
the operational process, and normal host orchestration cannot reproduce the fixed
14-request synthetic journey. Use the separate
[Claude composite observation](QUAL-206_CLAUDE_COMPOSITE_OBSERVATION.md) without
changing this exact conformance contract.

## Remaining acceptance work

The next use of this collector is an isolated desktop host that can run one process
and deliberately drive the complete exact-five journey. Claude uses the additive
two-process observation lane instead. Either result remains unscored until the host
process and complete runtime closure are source-bound and a separate public
projection contract accepts the stronger evidence.

Remote HTTP, a live provider, public runtime identity and TLS, governed storage and
recovery, operations, deployment, registry publication, activation and release all
remain separate gates.
