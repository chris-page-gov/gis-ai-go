# QUAL-206 host interoperability and secure-tunnel runbook

- status: local conformance and four ChatGPT secure-tunnel probes passed, including
  the current final telemetry wrapper;
  four independent-host readiness attempts are documented but not ready;
  capability scoring and activation remain pending
- reviewed source base: `66507f9a6e6c0da23a8af4682268f9362d93bc06`
- supported public product: immutable
  [`v0.1.0`](https://github.com/chris-page-gov/gis-ai-go/releases/tag/v0.1.0)
- production MCP activation: empty
- production direct-API activation: empty
- default readiness: `503`

## Purpose and boundary

This runbook makes host and tunnel claims repeatable without turning the local
conformance seam into a supported service. The seam exposes exactly:

- `catalogue.search`;
- `catalogue.describe`;
- `gis-ai-go://catalogue/public`; and
- `gis-ai-go://catalogue/records/{record_id}`.

The conformance entry point refuses to start unless
`GIS_AI_GO_QUAL_206_CONFORMANCE=1` and a full lowercase source commit are supplied.
Neither production executable supplies those test-only options. No provider is
called, no provider credential is needed and no public endpoint is created.

## Build the exact local candidate

Use a complete checkout because the accepted gateway still loads canonical schemas
from the repository layout:

```bash
pnpm install --frozen-lockfile
uv sync --locked
pnpm run build:okf
pnpm --filter @gis-ai-go/contracts run build
pnpm --filter @gis-ai-go/evidence run build
pnpm --filter @gis-ai-go/authority-context run build
pnpm --filter @gis-ai-go/policy-client run build
pnpm --filter @gis-ai-go/mcp-gateway run build
pnpm run test:interoperability
```

For a manual STDIO run:

```bash
export GIS_AI_GO_QUAL_206_CONFORMANCE=1
export GIS_AI_GO_QUAL_206_SOURCE_COMMIT=<full-reviewed-commit>
node scripts/qual_206_conformance_server.mjs
```

Do not add either variable to a production service definition.

## Telemetry contract

Wrap any local host command with the repository proxy:

```bash
node scripts/qual_206_telemetry_proxy.mjs \
  --log /absolute/private/path/session.jsonl \
  --client <bounded-client-label> \
  -- node scripts/qual_206_conformance_server.mjs
```

The JSONL record captures:

- session, client, source-commit and Node identities;
- MCP method and bounded tool name;
- request and response byte counts and SHA-256 digests;
- hashed request identifiers, result status, bounded error code and duration;
- digest-only `truncated_frame` events for unterminated input or output at EOF; and
- process exit, signal and pending-request count.

It does not record raw prompts, arguments, responses, headers, tokens, environment
values or server stderr. Server stderr is represented by byte count and digest only.
The file is created with mode `0600`. Public evidence should publish only a reviewed,
path-free summary and checksums; retain the detailed JSONL locally.

## OpenAI secure tunnel and ChatGPT

### Verified client

The live probe used official `openai/tunnel-client` `v0.0.12`:

- release archive SHA-256:
  `42fb3138dc9c081d5777cb7e8bd1e041cc48b67c4978dbab3c5167ca1aabca02`;
- extracted Darwin arm64 binary SHA-256:
  `b1757220cf4722cec9085ee4a908cf0ee4c1a499a33bd99979b9a9c7669e29b1`;
- reported build:
  `0.0.12+881c9a8fed7cccbe6607cd419863bbca506b8215`.

Verify downloaded bytes against the release's `SHA256SUMS.txt` before use.

### Key handling

The existing project runtime key was reused only through the launch environment.
For the observed sessions, the private profile stored only `env:OPENAI_API_KEY`,
never the key value. A later operator may use a separately exported, scoped alias,
but must record the environment-variable name that the profile actually referenced.
Do not pass the key on a command line, paste it into ChatGPT, add its value to a host
configuration, enable raw HTTP logging or commit it. Creating or changing a tunnel
requires an authorised Platform session or organisation admin key; the runtime
project key alone cannot do administrative tunnel CRUD.

### Create and connect

1. In the OpenAI Platform, open **Settings → Organisation → Tunnels**.
2. Create a tunnel with a descriptive, non-secret name, select the intended
   organisation and ChatGPT workspace, and record its non-secret tunnel ID.
3. Create a temporary profile directory outside the repository.
4. Connect the reviewed STDIO command:

```bash
tunnel-client runtimes connect \
  --alias <local-alias> \
  --profile <profile-name> \
  --profile-dir <private-temporary-profile-directory> \
  --runtime-api-key env:OPENAI_API_KEY \
  --tunnel-id <tunnel-id> \
  --mcp-command '<absolute telemetry-proxy and conformance-server command>'
```

5. Require `runtimes status <alias> --json` to report process running, local
   `/healthz` and `/readyz` `200`, remote identity exact, and runtime state `ready`.
6. In ChatGPT, enable developer mode under **Settings → Security and login**.
7. Choose **Plugins → Create app → Tunnel**, select the exact tunnel, select
   **No Auth** for this anonymous-open local catalogue, acknowledge the unreviewed
   connector warning, create the app and connect it.
8. Inspect the app before use. It must advertise only the two expected read actions
   with the exact closed input schemas.

The current authorised proof used:

- tunnel name: `gis-ai-go-v0-2-interoperability`;
- tunnel ID: `tunnel_6a873e7214308191bfe27240c1c03f68`;
- ChatGPT app: `GIS AI GO v0.2 interoperability`;
- app ID: `asdk_app_6a873f853628819184bccb4a9b961576`;
- app version ID: `asdk_app_v_6a873f85363081918f25a5aeaee98159`.

These identifiers are evidence, not secrets or a promise of permanent uptime.
The tunnel metadata persists, but the app works only while the reviewed local
runtime is running.

### Live acceptance probe

The prompt was:

> Use only GIS AI GO v0.2 interoperability. Search the public catalogue for
> INSPIRE. Return the first record ID, title, and inline evidence receipt ID. Do
> not use web search or any other plugin.

The initial temporary-server probe completed in approximately 13 seconds. A second
probe exercised the first repository telemetry wrapper. After independent review,
the wrapper was hardened to isolate the child environment, digest rather than relay
stderr, and allowlist logged method and operation names. A third probe from those
exact bytes completed in approximately 13 seconds. EOF telemetry hardening then
changed the wrapper, so the historical run was retained without relabelling it. A
fourth authorised probe from the final wrapper completed in approximately 9 seconds
and returned:

- record ID `hmlr:dataset:inspire-index-polygons`;
- title `Index polygons spatial data (INSPIRE)`; and
- receipt ID
  `gis-ai-go:evidence-receipt:sha256:c911e6ee04607f0c109ce5ae3d30e98dc0e463ff8f74b2567b9c83efad7caf61`.

The fourth run's repository JSONL recorded one request, one successful response,
the exact source commit, byte counts, SHA-256 digests and 46.193125 ms server time.
The tunnel metrics recorded one successful control-plane command, 342 ms from
enqueue to response delivery and 276 ms from poll to response delivery. At capture,
the bounded queue and worker occupancy were both zero. No raw prompt, argument,
result, header or key was retained. The reviewed, path-free
[`live-host evidence`](../../tests/interoperability/evidence/chatgpt-tunnel-2026-08-20.json)
binds those values to the exact final-wrapper bytes used in this current session.
The detailed digest-only JSONL is retained locally with mode `0600`; its reviewed
public record contains the exact byte count, SHA-256 digest and event counts but no
machine path or conversation URL.

## Independent-host matrix

Use a temporary, isolated profile for every host. Never modify a normal user-wide
MCP registry for a conformance run.

| Host | Required test | Current evidence state |
| --- | --- | --- |
| ChatGPT | Secure tunnel, discovery, search, receipt and text fallback | Four probes passed; latest run binds the final wrapper and current receipt |
| Codex CLI 0.146.1 | Isolated non-interactive STDIO search and inline evidence | `not_ready`: legacy `2025-06-18` initialisation rejected `-32022`; capability unscored |
| Antigravity IDE 1.107.0 | Temporary profile, STDIO discovery, search, resource and fallback | `not_ready`: isolated profile signed out and server directory unavailable; zero MCP traffic |
| Claude Code 2.1.204 | Strict temporary MCP configuration and non-persistent session | `not_ready`: legacy `initialize` rejected `-32022`; capability unscored |
| VS Code 1.134.0 | Temporary workspace and MCP registry; prove correct window attachment | `not_ready`: no GitHub token and no proved chat attachment; zero MCP traffic |
| Official SDK client | HTTP and STDIO discovery, calls, resources and shutdown | Accepted on protected `main` |

For every host, distinguish readiness from capability. Authentication, workspace
attachment or client launch failures are `not_ready`; they do not become zero-score
server results. Run the capability pack only after discovery and listing succeed.

### Repeat the isolated STDIO host probes

Start from the reviewed checkout and create one disposable root. Do not reuse a
normal host profile or put an AI-provider credential in the MCP definition. Remove
both OpenAI key variable names from every non-OpenAI host parent and its MCP proxy
process:

```bash
export QUAL206_REPO="$(pwd -P)"
export QUAL206_SOURCE_COMMIT="$(git rev-parse HEAD)"
export QUAL206_NODE="$(command -v node)"
export QUAL206_HOST_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/gis-ai-go-qual206-hosts.XXXXXX")"
mkdir -p "$QUAL206_HOST_ROOT"/telemetry
mkdir -p "$QUAL206_HOST_ROOT"/claude
mkdir -p "$QUAL206_HOST_ROOT"/antigravity/{user-data,extensions,workspace}
mkdir -p "$QUAL206_HOST_ROOT"/vscode/{user-data,extensions,workspace}
mkdir -p "$QUAL206_HOST_ROOT"/{codex-home,codex-profile,codex-workspace,codex-raw}
chmod 0700 "$QUAL206_HOST_ROOT"/{codex-home,codex-profile,codex-workspace,codex-raw}
```

For each host, use a STDIO definition with command `/usr/bin/env` and this ordered
argument list, substituting the host name in the telemetry path and client label:

```text
-u
OPENAI_API_KEY
-u
CODEX_API_KEY
GIS_AI_GO_QUAL_206_CONFORMANCE=1
GIS_AI_GO_QUAL_206_SOURCE_COMMIT=<QUAL206_SOURCE_COMMIT>
<QUAL206_NODE>
<QUAL206_REPO>/scripts/qual_206_telemetry_proxy.mjs
--log
<QUAL206_HOST_ROOT>/telemetry/<host>.jsonl
--client
<bounded-host-version-label>
--
<QUAL206_NODE>
<QUAL206_REPO>/scripts/qual_206_conformance_server.mjs
```

Build that closed definition and select the exact readiness prompt from the corpus:

```bash
qual206_mcp_server() {
  jq -cn \
    --arg commit "$QUAL206_SOURCE_COMMIT" \
    --arg node "$QUAL206_NODE" \
    --arg proxy "$QUAL206_REPO/scripts/qual_206_telemetry_proxy.mjs" \
    --arg log "$QUAL206_HOST_ROOT/telemetry/$1.jsonl" \
    --arg client "$2" \
    --arg server "$QUAL206_REPO/scripts/qual_206_conformance_server.mjs" \
    '{type:"stdio",command:"/usr/bin/env",args:[
      "-u","OPENAI_API_KEY","-u","CODEX_API_KEY",
      "GIS_AI_GO_QUAL_206_CONFORMANCE=1",
      "GIS_AI_GO_QUAL_206_SOURCE_COMMIT="+$commit,
      $node,$proxy,"--log",$log,"--client",$client,"--",$node,$server
    ]}'
}
export QUAL206_PROMPT="$(jq -r \
  '.cases[] | select(.id == "QUAL-206-HOST-001") | .prompt' \
  tests/interoperability/qual_206_cases.json)"
```

### Repeat the isolated Codex CLI probe

The current official OpenAI documentation supports local STDIO MCP servers in
Codex configuration and recommends `codex exec --ephemeral` with JSONL output for
non-interactive runs. It also says to supply `CODEX_API_KEY` only to the individual
automation invocation. See [Model Context Protocol](https://developers.openai.com/codex/mcp/),
[non-interactive mode](https://developers.openai.com/codex/noninteractive/) and the
[configuration reference](https://developers.openai.com/codex/config-reference/).

Use an empty disposable Git workspace and the exact `QUAL-206-HOST-002` corpus
case. The MCP command strips both supported API-key variable names before starting
the telemetry proxy, so neither the proxy nor its server child receives the
credential. The execution command also enables Codex's default secret-name
exclusions, preventing a later model-spawned shell subprocess from inheriting the
single-invocation API key:

```bash
git -C "$QUAL206_HOST_ROOT/codex-workspace" init -q

/usr/bin/env \
  HOME="$QUAL206_HOST_ROOT/codex-profile" \
  CODEX_HOME="$QUAL206_HOST_ROOT/codex-home" \
  codex mcp add gis-ai-go-qual-206 -- \
  /usr/bin/env -u CODEX_API_KEY -u OPENAI_API_KEY \
  GIS_AI_GO_QUAL_206_CONFORMANCE=1 \
  "GIS_AI_GO_QUAL_206_SOURCE_COMMIT=$QUAL206_SOURCE_COMMIT" \
  "$QUAL206_NODE" "$QUAL206_REPO/scripts/qual_206_telemetry_proxy.mjs" \
  --log "$QUAL206_HOST_ROOT/telemetry/codex.jsonl" \
  --client codex-cli-0.146.1 -- \
  "$QUAL206_NODE" "$QUAL206_REPO/scripts/qual_206_conformance_server.mjs"

test -n "${OPENAI_API_KEY:-}" || exit 1
umask 077
jq -r '.cases[] | select(.id == "QUAL-206-HOST-002") | .prompt' \
  tests/interoperability/qual_206_cases.json | \
  CODEX_API_KEY=${OPENAI_API_KEY} /usr/bin/env -u OPENAI_API_KEY \
  HOME="$QUAL206_HOST_ROOT/codex-profile" \
  CODEX_HOME="$QUAL206_HOST_ROOT/codex-home" \
  codex -a never exec --strict-config --json --ephemeral --ignore-rules \
  --sandbox read-only --model gpt-5.6-luna \
  -c 'model_reasoning_effort="low"' \
  -c 'shell_environment_policy.ignore_default_excludes=false' \
  -c 'mcp_servers.gis-ai-go-qual-206.required=true' \
  -c 'mcp_servers.gis-ai-go-qual-206.enabled_tools=["catalogue.search"]' \
  -c 'mcp_servers.gis-ai-go-qual-206.default_tools_approval_mode="auto"' \
  -c 'mcp_servers.gis-ai-go-qual-206.startup_timeout_sec=10' \
  -c 'mcp_servers.gis-ai-go-qual-206.tool_timeout_sec=60' \
  --color never -C "$QUAL206_HOST_ROOT/codex-workspace" - \
  > "$QUAL206_HOST_ROOT/codex-raw/events.jsonl" \
  2> "$QUAL206_HOST_ROOT/codex-raw/stderr.log"
```

Do not put either key value in the MCP definition. Review and hash the three raw
files only inside the disposable `0700` root; they are created as `0600` by the
proxy or restrictive umask. Publish only the path-free summary.

The reviewed 0.146.1 attempt selected `gpt-5.6-luna`, but the model never ran.
Codex sent an `initialize` request for MCP `2025-06-18`; the modern-only seam
returned `-32022` with supported version `2026-07-28` in 151.129542 ms. The CLI
exited `1` after approximately 299 ms, emitted no stdout and made no task-level
tool call. The proxy recorded three current-wrapper events. This is protocol
negotiation `not_ready`, with capability unscored—not a zero capability score.
The CLI reported version 0.146.1 but no source commit. The path-free
[`Codex CLI evidence`](../../tests/interoperability/evidence/codex-cli-2026-08-20.json)
records the binary, harness, prompt, frame and private-output digests without
publishing raw diagnostics or temporary paths. The accepted evidence records that
historical negotiation attempt; the shell-environment hardening above is a safer
repeat procedure and is not relabelled as an observed step.

For Claude Code, write only the closed server wrapper to the isolated file, then
run the non-persistent client:

```bash
MCP_SERVER_JSON="$(qual206_mcp_server claude claude-code-2.1.204)"
jq -n --argjson server "$MCP_SERVER_JSON" \
  '{mcpServers:{"gis-ai-go-qual-206":$server}}' \
  > "$QUAL206_HOST_ROOT/claude/mcp.json"
/usr/bin/env -u OPENAI_API_KEY -u CODEX_API_KEY \
  CLAUDE_CONFIG_DIR="$QUAL206_HOST_ROOT/claude" claude \
  --bare --print --no-session-persistence --strict-mcp-config \
  --mcp-config "$QUAL206_HOST_ROOT/claude/mcp.json" \
  --output-format json "$QUAL206_PROMPT"
```

The 2.1.204 probe supplied no Anthropic credential. It returned `Not logged in`,
and its `initialize` exchange was rejected with the expected `-32022` because this
candidate deliberately sets `legacy: "reject"`. A separate isolated `claude mcp
list` check produced start, `initialize`, bounded error and clean-end telemetry.
Classify this as protocol-negotiation `not_ready`; do not score capabilities.

Repeat that health check by writing only this public-safe object to the isolated
`$CLAUDE_CONFIG_DIR/.claude.json`; substitute the variables from the common setup:

```json
{
  "mcpServers": {
    "gis-ai-go-qual-206": {
      "type": "stdio",
      "command": "/usr/bin/env",
      "args": [
        "-u",
        "OPENAI_API_KEY",
        "-u",
        "CODEX_API_KEY",
        "<QUAL206_NODE>",
        "<QUAL206_REPO>/scripts/qual_206_telemetry_proxy.mjs",
        "--log",
        "<QUAL206_HOST_ROOT>/telemetry/claude-health.jsonl",
        "--client",
        "claude-code-health-2.1.204",
        "--",
        "<QUAL206_NODE>",
        "<QUAL206_REPO>/scripts/qual_206_conformance_server.mjs"
      ],
      "env": {
        "GIS_AI_GO_QUAL_206_CONFORMANCE": "1",
        "GIS_AI_GO_QUAL_206_SOURCE_COMMIT": "<QUAL206_SOURCE_COMMIT>"
      }
    }
  }
}
```

Then run:

```bash
/usr/bin/env -u OPENAI_API_KEY -u CODEX_API_KEY \
  CLAUDE_CONFIG_DIR="$QUAL206_HOST_ROOT/claude" claude mcp list
```

The reviewed attempt returned `Failed to connect`; its bounded four-event telemetry
ended cleanly with error `-32022`, no pending request and no capability call.

For Antigravity IDE, use the application CLI and pass the JSON definition through
`--add-mcp`:

```bash
AG_BIN='/Applications/Antigravity IDE.app/Contents/Resources/app/bin/antigravity-ide'
MCP_SERVER_JSON="$(qual206_mcp_server antigravity antigravity-ide-1.107.0)"
MCP_DEFINITION_JSON="$(jq -cn --argjson server "$MCP_SERVER_JSON" \
  '$server | del(.type) + {name:"gis-ai-go-qual-206"}')"
/usr/bin/env -u OPENAI_API_KEY -u CODEX_API_KEY "$AG_BIN" \
  --user-data-dir "$QUAL206_HOST_ROOT/antigravity/user-data" \
  --extensions-dir "$QUAL206_HOST_ROOT/antigravity/extensions" \
  --sync off --new-window --add-mcp "$MCP_DEFINITION_JSON" \
  "$QUAL206_HOST_ROOT/antigravity/workspace"
```

Submit the prompt only after visibly confirming that this isolated window is
focused. The 1.107.0 probe (commit
`ecfbad74d93962fc8ca485d93ab9b4f3d4cb6cf8`) was signed out, could not load its
server directory and emitted no MCP/proxy traffic. Classify it `not_ready`; do not
infer a server capability failure.

For VS Code, use the same isolated launch pattern:

```bash
MCP_SERVER_JSON="$(qual206_mcp_server vscode vscode-1.134.0)"
MCP_DEFINITION_JSON="$(jq -cn --argjson server "$MCP_SERVER_JSON" \
  '$server | del(.type) + {name:"gis-ai-go-qual-206"}')"
/usr/bin/env -u OPENAI_API_KEY -u CODEX_API_KEY code \
  --user-data-dir "$QUAL206_HOST_ROOT/vscode/user-data" \
  --extensions-dir "$QUAL206_HOST_ROOT/vscode/extensions" \
  --sync off --new-window --add-mcp "$MCP_DEFINITION_JSON" \
  "$QUAL206_HOST_ROOT/vscode/workspace"
```

Again submit the prompt only after visibly confirming the isolated window. The
1.134.0 probe (commit `110a328ea54b42367b803ec53ee0bf52ef26b419`) had no
GitHub token and did not prove that chat attached to the intended host. It emitted
no MCP/proxy traffic, so classify it `not_ready` and leave capability unscored.

After each attempt, terminate only processes whose full command contains the
disposable root. Confirm none remain before deleting that root. Review the bounded
proxy JSONL and host logs for readiness evidence, but never publish raw host logs,
tokens, device identifiers, profile databases or absolute temporary paths.

The path-free
[`independent-host readiness summary`](../../tests/interoperability/evidence/independent-host-readiness-2026-08-20.json)
preserves the reviewed versions, classifications, zero-traffic outcomes and Claude
telemetry digests. These attempts used an earlier telemetry-wrapper generation; the
summary says so explicitly and makes no claim that they exercised the final wrapper
or proved capability. The separate Codex summary exercises the current wrapper and
does not rewrite or upgrade those earlier host claims. Retained-file scans found no
key, but the historical non-OpenAI probes did not capture their parent-process
environments; do not treat those scans as proof of process-level absence. The
hardened repeat procedure above closes that boundary for future probes.

## Historical failure-derived cases

[`qual_206_cases.json`](../../tests/interoperability/qual_206_cases.json) contains
seven public-safe cases derived from the `mcp-geo` multi-client evaluations and
curated postmortems at exact commit
`56683b33c0cd02842b7f3ee465414c68a1f3f2a6`, plus three current
candidate-assurance cases for catalogue search, untrusted metadata and the
activation boundary. Each historical case cites one or more entries in the
six-path SHA-256-bound source register. Candidate-assurance cases state their
current contract or threat-model basis without claiming historical provenance.
The historical cases preserve lessons about:

- readiness before capability scoring;
- workspace and authentication failures versus server failures;
- resource retrieval that must lead to a useful answer;
- structured-error recovery;
- complete non-App fallbacks;
- offline and live-credential tracks remaining separate; and
- transport telemetry minimisation.

The corpus does not copy raw conversations, local session paths, keys, personal
data or licensed feature payloads. Changes to a historical case require a fresh
review against its cited source-hashed material; changes to a candidate-assurance
case require review against the current named contract or threat boundary.

## Local assurance evidence

The complete locked `pnpm run check` gate passed on the final ChatGPT evidence
bytes on 20 August 2026 with loopback permission for the real HTTP tests:

- contracts `19`, evidence `25`, authority `2`, policy `6`, provider adapter `10`,
  tool registry `7`, gateway `99` and interoperability `10` tests;
- Explorer build-policy `16`, unit/component `42` and browser `27` tests;
- repository Python `105` and execution-service `20` tests;
- two byte-identical release builds; the exact candidate digest is recorded by the
  gate and pull-request evidence rather than self-referenced in this commit;
- `25` schemas and `65` records, `336` local links, `183` research hashes,
  `2` ledgers and `71` source identifiers;
- `594` scanned text files with no baseline secret or machine-path match;
- `9` rendered diagrams; and
- a CycloneDX SBOM with `165` components.

The first sandboxed attempt denied nine loopback binds with `EPERM`. The identical
gate passed when rerun with loopback permission; no test was skipped or weakened.
These are local candidate results. The candidate commit, protected pull-request
checks and protected-main provenance remain pending.

## Teardown and repeatability

After a bounded run:

1. export a redacted summary and checksum the local telemetry file;
2. disconnect or disable the ChatGPT development app when it is not being tested;
3. run `tunnel-client runtimes stop <alias>`;
4. confirm health and readiness are no longer reachable;
5. retain or delete remote tunnel metadata according to the next scheduled run;
6. remove the temporary host profiles and local detailed logs; and
7. rerun from an exact protected-main commit for any publication claim.

Do not claim production support, public service availability, independent-host
interoperability or activation from the ChatGPT-only proof.
