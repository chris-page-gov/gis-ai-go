# QUAL-206 local HTTP transport preflight

This runbook covers the additive real-socket HTTP preflight for the
candidate-unregistered exact-five assembly. It does not replace the historical
STDIO lanes or the independent-host capability pack.

The preflight starts one direct child process, binds an operating-system listener
to an ephemeral port on `127.0.0.1`, and drives the MCP `2026-07-28` journey with
a deterministic synthetic client. The port and raw protocol material are retained
only in an owner-only private capture. The public projection is path-free.

## Claim boundary

A passing public projection is classified exactly as
`local-http-transport-preflight`. It proves that the local candidate assembly:

- exposed the exact five operations and three resource classes over a real HTTP
  socket;
- completed discovery, listing, three resource reads and all five tool calls;
- preserved structured-content and plain-text parity for every tool result;
- advertised only the five direct API operations plus the three fixed operational
  routes through OpenAPI, with exact methods, operation identities and canonical
  MCP request and success-schema bindings, and reported the same active set through
  readiness;
- aborted a second, distinctly keyed `data.query` after its deterministic fixture
  transport started, with private digest-only audit attribution proving that the
  successful key has its completed ledger event while the aborted key remains
  pending without a resolution, receipt, record or ledger event;
- returned exact JSON-RPC `-32601` for `prompts/list`;
- produced two fixture-provider starts, one abort, four ledger events, no guarded
  external-network attempt and no reported fixture error; and
- closed its listener and removed its temporary state before the capture was
  finalised.

It does **not** prove TLS, a secure tunnel, a public hostname, an independent
remote host, a live provider, Claude Code or model capability, registration,
activation, deployment or release. `remote_host_acceptance` remains `false` and
Claude Code and model capability remain `unscored`.

The public contract also records `complete_runtime_source_binding: false`. The
repository commit, tree and named runtime materials are bound, but the complete
loaded runtime closure is not yet captured. In particular, the named material
list omits some executed, ignored first-party gateway build outputs as well as the
loaded third-party runtime closure. Do not widen this claim. The collector hashes
the exact named material list immediately before child execution and again after
the child has closed, including the two declared ignored built HTTP runtime files
and governed OKF manifest and bundle. The private capture retains both hashes.
Replay requires the two observed hashes and the current pre/post replay hashes to
remain equal; that check covers only the named list and is not a complete runtime
source binding.

For a clean durable run, both collector and verifier use the fixed system Git
executable with replacement objects, filesystem-monitor shortcuts and the
untracked cache disabled. They reject assume-unchanged, skip-worktree and
filesystem-monitor index flags, and require every tracked named material to equal
its blob in the recorded tree. The four declared derived OKF and built gateway
files remain outside that tree comparison; they stay covered by the pre/post hash
checks. Other executed first-party build outputs and third-party runtime bytes are
outside the named set, which is why `complete_runtime_source_binding` remains
`false`.

## Contracts and programmes

- Private capture contract:
  `schemas/qual-206-local-http-private-capture-v1.schema.json`
- Path-free public contract:
  `schemas/qual-206-local-http-transport-preflight.schema.json`
- Real-socket collector: `scripts/qual_206_local_http_preflight.mjs`
- Offline replay verifier:
  `scripts/qual_206_verify_local_http_preflight.py`
- Immutable canonical schema-digest manifest:
  `schemas/qual-206-exact-five-tool-schema-digests.v1.json`
- Test-only child launcher:
  `apps/mcp-gateway/test/fixtures/qual-206-exact-five-http-server.mjs`

The collector reuses the same output contracts and deterministic fixture facts as
the canonical exact-five STDIO lane. The verifier independently parses the raw
JSON-RPC and audit bytes. Python independently checks all ten domain-separated
canonical schema identities against the immutable committed manifest before any
result is accepted. Node tests bind that manifest to `EXPECTED_TOOL_SCHEMAS`.
Replay launches no external Node process and does not weaken executable trust. It
then validates tool outputs, compares resource content with the governed OKF
artefact, checks evidence references, recomputes both captured idempotency-key
digests independently and recomputes all published facts. The public projection
retains only the successful/aborted booleans; neither raw keys nor their digests
are published.

## Focused development gate

Build the governed gateway and its workspace dependencies, then run the focused
tests:

```bash
pnpm --filter @gis-ai-go/mcp-gateway run prepare:test
pnpm --filter @gis-ai-go/mcp-gateway run build
node --test tests/interoperability/test_qual_206_local_http_preflight.mjs
uv run --locked --cache-dir .uv-cache python -m unittest \
  tests.interoperability.test_qual_206_local_http_preflight
```

The Node test uses one genuine loopback socket. A sandbox that prohibits local
listeners will fail with `listen EPERM`; run that focused test in the normal local
development environment rather than relabelling an in-process handler as socket
evidence.

On a dirty development branch, capture and private-contract checks can pass, but
the offline verifier must refuse a durable public projection. This is expected.

## Durable capture from exact protected main

Only perform this step from the exact accepted protected-main commit after its
normal repository and security checks have passed.

1. Confirm `git status --short` is empty and record the full commit and tree.
2. Build the gateway using the focused development-gate commands above.
3. Create a new owner-owned directory with mode `0700` outside the repository.
4. Set `GIS_AI_GO_QUAL_206_LOCAL_HTTP_CAPTURE=1` for the collector invocation and
   provide a canonical absolute path for a **new** capture file in that directory.
5. Run the offline verifier against the resulting `0600` capture and provide a
   canonical absolute path for a **new** public projection file.

Example, with placeholders replaced by freshly created absolute paths:

```bash
GIS_AI_GO_QUAL_206_LOCAL_HTTP_CAPTURE=1 \
  node scripts/qual_206_local_http_preflight.mjs \
  --capture /ABSOLUTE/OWNER-ONLY-DIRECTORY/private-capture.json

uv run --locked --cache-dir .uv-cache python \
  scripts/qual_206_verify_local_http_preflight.py \
  --capture /ABSOLUTE/OWNER-ONLY-DIRECTORY/private-capture.json \
  --public-output /ABSOLUTE/NEW-PUBLIC-PROJECTION.json
```

The collector itself supplies the child-only fixture authority, source commit,
private audit descriptor and provider-egress guard. Do not invoke the fixture as a
service or expose its ephemeral port.

The verifier requires all of the following before it writes anything public:

- a canonical capture path outside the repository, in a non-symbolic,
  owner-owned directory with exact mode `0700`;
- an owner-owned, singly linked regular capture file with exact mode `0600`;
- a capture that passes the private schema and contains exactly 14 raw requests;
- exact request/response correlation and modern-protocol metadata;
- an ordered nine-event audit with exact final counters and two key-attributed
  private evidence states;
- deterministic tool, resource, key-attributed cancellation, exact closed OpenAPI
  callable-contract and readiness replay;
- exact pre/post execution hashes for every named source material, equality with
  the current replay bytes and no material drift during replay;
- current commit and tree equality; and
- a clean current worktree and a capture that records that clean state.

The output is staged in an exclusive temporary file in the pinned destination
directory, completely written, synchronised and read back before an atomic
no-overwrite hard link creates the final name. The directory and absolute path are
then rechecked and synchronised. An existing path is never overwritten, and a
caught finalisation failure removes both the temporary entry and any final entry
that still identifies the staged inode.

### Accepted protected-main evidence

The durable
[`25 August 2026 public projection`](../../tests/interoperability/evidence/local-http-transport-preflight-2026-08-25.json)
was captured and independently replayed from exact protected-main commit
`066a9cb22f719d22e29c95cd99857ddf694c878e`, tree
`43116491557d53c4c0ad2d3a6768761ccf873df4`. Its file SHA-256 is
`c227791068c662c64e14fa9ec354d8d8030e5cc2e3d64b0d8ff93101e1b67274`.
Every protected-main CI job passed in
[run 32851616717](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32851616717),
including repository, image, independent-derivation, attestation and provenance
assurance. Every analysis in
[CodeQL run 32851615811](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32851615811)
also passed for Actions, JavaScript/TypeScript and Python.

The accepted projection records exactly 14 requests and 13 responses over one
ephemeral IPv4 loopback listener. It covers the exact five operations and three
resource classes; the response-free request is the deliberately aborted second
`data.query`. The owner-only private capture remains local and unpublished. This
acceptance does not widen the claim: it is local HTTP transport preflight only,
with remote-host acceptance false, Claude Code and model capability unscored, and
no live provider, registration, activation, deployment or release exercised.

## Evidence handling

Keep the private capture outside the repository at an owner-controlled private
destination. It contains the ephemeral listener location, raw request arguments,
raw results and complete audit lines. Do not publish or commit it.

The public projection contains only hashes, bounded semantic facts, relative
repository material paths and explicit negative claims. Before proposing it for
review, confirm that it contains no absolute path, hostname, port, endpoint or raw
idempotency key. The verifier performs these checks, but review the projection as
well.

The accepted public projection is the path-free instance linked above. Do not
commit the private capture or treat its local retention as deployment evidence.
Repeat the complete protected-main capture and replay procedure after any harness
or runtime-material change rather than relabelling the accepted bytes.

## Stop conditions

Stop without producing a public projection if any of these occur:

- the listener binds anywhere other than IPv4 loopback or does not use an
  ephemeral port;
- stdout or stderr is non-empty, an audit line is malformed, or the child does
  not exit cleanly;
- the operation, resource, exact OpenAPI path/method/identity/schema binding or
  readiness sets differ;
- any advertised tool input or output schema differs from the canonical exact-five
  schema material;
- a result violates its schema or structured/plain-text parity;
- the second provider dispatch does not abort, produces a response, resolves its
  idempotency claim or acquires any receipt, record or ledger event;
- provider counts differ from two starts and one abort, ledger events differ
  from four, or any guarded external-network attempt or reported error occurs;
- temporary fixture state is not removed;
- the private capture is inside the repository or its parent is not canonical,
  owner-owned and mode `0700`;
- source material hashes drift during replay; or
- Git index concealment or replacement-object state is present, or a tracked
  named material differs from its recorded tree blob;
- public-output write, readback, directory synchronisation or final path identity
  cannot be established; or
- the current worktree is not clean.

Do not weaken this lane or edit historical evidence to make a failed capture pass.
