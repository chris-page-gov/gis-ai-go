# QUAL-206 Claude composite STDIO observation

This runbook covers a private, credential-free transport observation of Claude
Code against the inactive strict-modern GIS AI GO fixture. It does not replace the
exact 14-request conformance journey and does not score host capability.

Claude Code `2.1.241` supports MCP `2026-07-28`, but its modern STDIO negotiation
uses two direct child processes. The first is a disposable `server/discover` probe;
the second is the modern session. A single-process collector with fixed output
paths cannot represent that behaviour safely.

## Source-by-source decision matrix

| Source | Supported finding | Implementation consequence | Disposition |
| --- | --- | --- | --- |
| Local Claude Code `2.1.241` binary | The binary contains the final `2026-07-28` protocol, `server/discover` handling and automatic negotiation. In automatic mode it launches a disposable discovery process before the modern session. | Capture two direct Claude children under one run identity; do not reuse fixed output paths. | Supported and implemented additively. |
| [Official Claude MCP runtime documentation](https://code.claude.com/docs/en/mcp#MCP-client-runtimes) | The v2 runtime is available from Claude Code `2.1.232`; modern STDIO negotiation is selected with `MCP_PROTOCOL_NEGOTIATION=auto`. | Pin `MCP_SDK_GENERATION=v2` and `MCP_PROTOCOL_NEGOTIATION=auto` in the isolated observation environment. | Supported and required for this observation. |
| [Official Claude environment-variable reference](https://code.claude.com/docs/en/env-vars) | Claude runtime and non-essential traffic controls can be set per invocation. | Use a disposable profile and an allowlisted invocation environment; do not change normal Claude settings. | Supported and required for isolation. |
| [MCP `2026-07-28` release](https://blog.modelcontextprotocol.io/posts/2026-07-28/) | `server/discover` is the optional stateless opening for the final protocol. | Require one successful negotiation probe and a second session with no legacy `initialize`. | Supported protocol target. |
| Existing exact-five collector and replay verifier | The deterministic synthetic contract requires one ordered 14-request session, including cancellation and unsupported `prompts/list`. | Preserve that harness unchanged. Claude transport readiness is a separate composite observation, not an exact-five pass. | Preserved as the stronger model-independent conformance lane. |

The local binary observed during preflight was:

- executable: the locally installed versioned Claude Code `2.1.241` binary (the
  machine-specific absolute path remains private);
- version: `2.1.241 (Claude Code)`;
- byte length: `325055632`; and
- SHA-256: `1495eb7c42d3b4451f5f1cd38b6d498d22a4a38c802bc2be5c1cf1795e64820d`.

Recompute those values immediately before every observation. A changed binary is a
new host candidate and must not be accepted under these values.

## Composite observation contract

The observer is configured directly as the MCP STDIO command, so both observer
processes remain direct children of Claude. Each process:

- verifies the same run ID, exact source commit and immediate Claude parent PID,
  executable digest and byte length;
- allocates a distinct owner-only session directory beneath one private capture
  root;
- launches the inactive strict-modern fixture with a closed, credential-free child
  environment and guarded provider egress;
- closes that child idempotently, escalating from EOF to `SIGTERM` and `SIGKILL`
  within Claude's one-second disposal boundary so a failed fixture cannot remain
  orphaned;
- forwards operating-system STDIO without a shell or coordinator;
- records only bounded, allowlisted projections and cryptographic digests; and
- writes a hash-chained event log plus a closed manifest using exclusive,
  no-follow files.

The offline verifier requires exactly two completed sessions:

1. one negotiation probe containing only a successful `server/discover`; and
2. one modern session containing no `initialize`, an exact successful `tools/list`
   and only requests that claim MCP `2026-07-28`.

Both sessions must close cleanly with no anomaly, stderr, pending request, provider
call or third process. `capability_scored`, `host_capability` and
`source_binding_ready` remain false constants. This proves bounded transport
readiness only.

Claude may dispose of a completed observer with `SIGTERM` or `SIGINT`. The
observer accepts either signal only after every observed request has one matched,
contract-valid response claiming MCP `2026-07-28`; it then applies the same
sub-second child shutdown boundary. A signal before that point remains an anomaly
and fails closed. The first failed-closed exact-main attempt established this
distinction: the discovery child used `SIGTERM`, while the completed modern
`tools/list` child used `SIGINT`.

## Repository assurance

Build the gateway contracts, then run the observer and independent verifier tests:

```bash
pnpm --filter @gis-ai-go/mcp-gateway run prepare:test
pnpm --filter @gis-ai-go/mcp-gateway run build
pnpm --filter @gis-ai-go/tool-registry run build
node --test tests/interoperability/test_qual_206_claude_stdio_observer.mjs
uv run --locked --cache-dir .uv-cache python -m unittest \
  tests.contract.test_qual_206_claude_composite_observation
```

## Prepare an isolated observation

Use a new private root outside the repository. Its profile, capture, temporary and
client-output directories must be owned by the current user with mode `0700`. The
checkout must be clean and detached, and its `HEAD`, supplied source commit and
fresh local `origin/main` must all identify the same protected-main commit.

Generate one UUID run ID. Write only the explicit MCP server object to the
disposable Claude configuration. Substitute freshly verified absolute paths and
identity values:

```json
{
  "mcpServers": {
    "gis-ai-go-qual-206": {
      "type": "stdio",
      "command": "<BOUND_NODE_EXECUTABLE>",
      "args": [
        "<DETACHED_REPOSITORY>/scripts/qual_206_claude_stdio_observer.mjs",
        "--claude-composite-observation-only",
        "--capture-root", "<PRIVATE_CAPTURE_ROOT>",
        "--run-id", "<RUN_UUID>",
        "--client", "claude-code-2.1.241",
        "--source-commit", "<PROTECTED_MAIN_COMMIT>",
        "--expected-parent-sha256", "<CLAUDE_EXECUTABLE_SHA256>",
        "--expected-parent-bytes", "<CLAUDE_EXECUTABLE_BYTES>"
      ],
      "env": {
        "GIS_AI_GO_QUAL_206_EVENT_CAPTURE": "1"
      },
      "alwaysLoad": true,
      "timeout": 120000
    }
  }
}
```

For the credential-free health observation, use only the disposable
`CLAUDE_CONFIG_DIR` and run `claude mcp list`. Set the v2 runtime and automatic
protocol negotiation for this process. Remove all recognised provider credentials
from both the parent and MCP child environments. Do not log in, copy a token, use a
model prompt or change the normal Claude profile as part of this step.

## Verify the retained private capture

Verification is read-only and writes no evidence artefact:

```bash
uv run --locked --cache-dir .uv-cache python \
  scripts/verify_qual_206_claude_composite_observation.py \
  --capture-root <PRIVATE_CAPTURE_ROOT> \
  --run-id <RUN_UUID> \
  --source-commit <PROTECTED_MAIN_COMMIT> \
  --expected-parent-sha256 <CLAUDE_EXECUTABLE_SHA256> \
  --expected-parent-bytes <CLAUDE_EXECUTABLE_BYTES>
```

Keep the raw logs, manifests and Claude client output private and outside the
repository. Publish only a separately compiled, allowlisted, path-free projection
after review.

## Stop conditions

Stop without making a claim if:

- the checkout is not clean, detached and equal to freshly fetched protected
  `origin/main`;
- the Claude executable digest or byte length differs from the supplied identity;
- a managed MCP configuration or managed settings file appears;
- the capture root is not a new canonical owner-only directory;
- Claude starts any unexpected third observer process;
- either session uses legacy `initialize`, omits the final protocol claim, reports
  an anomaly or fails closed verification;
- any credential reaches the MCP definition or observer child environment; or
- a model or provider call would be required for the transport-only observation.

Model-mediated operation and resource calls, remote HTTP, live provider access,
runtime source closure, activation, deployment, registry publication and release
remain separate gates.
