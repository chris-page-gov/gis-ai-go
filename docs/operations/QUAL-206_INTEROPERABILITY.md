# QUAL-206 host interoperability and secure-tunnel runbook

- status: local conformance and four ChatGPT secure-tunnel probes passed, including
  the current final telemetry wrapper;
  a test-only real-process exact-five STDIO transcript, cancellation, unsupported
  traffic and all seven suspension scenarios pass locally with zero live-provider
  calls;
  four 20 August independent-host readiness attempts remain documented as not
  ready; a separate 23 August Claude Code legacy STDIO observation from exact
  protected-main bytes passed initialisation and tool listing, with capability
  unscored;
  deterministic `HOST-015` application recovery passes locally but remains non-live
  and unscored; capability scoring and activation remain pending
- reviewed source base: `66507f9a6e6c0da23a8af4682268f9362d93bc06`
- Claude transport-readiness source: protected `main` commit
  `30b575beb27ff805745a2864c1acf44392774046`
- legacy fallback integration base: protected `main` commit
  `5a7e441bfc754af2bf95ec49a5ec113951c7c0bf`
- legacy fallback status: accepted through
  [pull request 40](https://github.com/chris-page-gov/gis-ai-go/pull/40) at
  protected `main` commit `e1fc1cbe69ea72c9aa310607d80f392ef56b0d58`;
  it has not been deployed; its constructor-only launcher has since been exercised
  by isolated Claude Code transport from later protected-main bytes
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

The same interoperability command also runs a separate deterministic
`QUAL-206-HOST-015` gateway fixture. That fixture mounts the inactive data and
inspection applications only in process with a controlled provider transport and
temporary private stores. It is not exposed by the catalogue conformance server or
secure tunnel and is not live-host evidence.

The complete gateway test suite additionally runs a separately named exact-five
STDIO subprocess test.
It can start only with its exact test flag, authority argument, full source commit,
closed scenario and private audit pipe. It wraps the branded
`candidate-unregistered` assembly, fragments JSON-RPC frames across real stdin and
stdout pipes and injects one fixed ONS response into the exact adapter, so no
provider network request is made. The active journey discovers and safely calls all
five operations, reads the catalogue, record and evidence resources, and checks
structured/plain-text parity. Separate subprocesses prove cancellation, unsupported
traffic and all seven subtractive suspension scenarios. This fixture is not a
shipped entrypoint, manual host procedure, live-provider result or activation
mechanism.

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
pnpm run test:typescript
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
| Claude Code 2.1.204, modern-only seam, 20 August | Strict temporary MCP configuration and non-persistent session | `not_ready`: legacy `initialize` rejected `-32022`; capability unscored |
| Claude Code 2.1.204, protected-main legacy seam, 23 August | Isolated `mcp list` transport check against the protected-main source named below | `ready`: legacy initialisation and `tools/list` passed; capability unscored |
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

## Constructor-only legacy STDIO fallback

This separately reviewed and accepted fallback addresses only the protocol-opening failure
seen in current Codex CLI `0.146.1` and Claude Code `2.1.204`. The retained Codex
frame requested `2025-06-18`; the retained Claude frame used the same legacy
`initialize` method. Those observations remain bound to source commit `66507f9`
and the modern-only harness bytes recorded in their existing evidence files. Do
not relabel either result or replace its source commit after testing this fallback.

The implementation was reviewed after a conflict-free rebase onto protected `main`
commit `5a7e441bfc754af2bf95ec49a5ec113951c7c0bf`, which contained the accepted
ADAPT-203 provider slice and inactive public-read v2 prerequisite. The fallback
patch had no path overlap with the v2 change and remained byte-identical across its
runtime, tests, launcher and retained evidence; only its provenance and status prose
changed. It then merged through
[pull request 40](https://github.com/chris-page-gov/gis-ai-go/pull/40) as
`e1fc1cbe69ea72c9aa310607d80f392ef56b0d58`, preserving reviewed tree
`7887453327c8da2ed435d7637c3818afd3632fb4`. Protected-main
[CI](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32431175681) and
[CodeQL](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32431175548)
passed. No host was rerun and the retained observations remain unscored.

The repository pins the official Model Context Protocol SDK packages to `2.0.0`.
That SDK exposes `serveStdio(factory, { legacy: "serve" })`, which pins a
connection to the legacy era after its opening, and the official client exposes
`versionNegotiation: { mode: "legacy" }`. GIS AI GO uses those APIs only through:

- `startCatalogueLegacyConformanceStdio`;
- the exact, non-serialisable `MCP_LEGACY_CONFORMANCE_ONLY` constructor symbol;
- the singleton legacy protocol revision `2025-06-18`; and
- the same bounded framing, activated local-conformance operations, schemas,
  application functions, structured errors and resources as the modern path.

`startCatalogueStdio`, `runCatalogueStdioMain`, MCP HTTP and all package start
scripts remain strict `2026-07-28` paths. The production activation arrays remain
empty. Supplying conformance-looking environment variables to the shipped STDIO
executable does not enable the fallback. There is no production environment or
command-line escape, and no tunnel or public endpoint is created.

### Build and verify an exact fallback checkout

Do not use an uncommitted working tree for retained host evidence. After the
fallback has a reviewed commit, create a detached checkout of that exact source:

```bash
export QUAL206_FALLBACK_COMMIT=<full-reviewed-fallback-commit>
export QUAL206_FALLBACK_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/gis-ai-go-qual206-fallback.XXXXXX")"
git worktree add --detach "$QUAL206_FALLBACK_ROOT/repository" \
  "$QUAL206_FALLBACK_COMMIT"
cd "$QUAL206_FALLBACK_ROOT/repository"
test "$(git rev-parse HEAD)" = "$QUAL206_FALLBACK_COMMIT"
test -z "$(git status --porcelain)"
pnpm install --frozen-lockfile
uv sync --locked
pnpm run test:interoperability
pnpm --filter @gis-ai-go/mcp-gateway run test
```

The raw and official-client regressions cover `initialize`,
`notifications/initialized`, `tools/list`, `tools/call`, `resources/list`,
`resources/templates/list` and `resources/read`. Further tests prove semantic
schema, application-result and structured-error parity, exact constructor
authority and non-bypass of the shipped STDIO executable.

### Run the fallback through minimised telemetry

Use only the separately named test launcher. It fails unless both the existing
conformance environment gate and the exact test-only argument are present:

```bash
export GIS_AI_GO_QUAL_206_CONFORMANCE=1
export GIS_AI_GO_QUAL_206_SOURCE_COMMIT="$QUAL206_FALLBACK_COMMIT"
umask 077
node scripts/qual_206_telemetry_proxy.mjs \
  --log "$QUAL206_FALLBACK_ROOT/legacy-host.jsonl" \
  --client <bounded-host-version-label> -- \
  node scripts/qual_206_legacy_conformance_server.mjs \
  --legacy-stdio-conformance-only
```

For a host registry, retain the `/usr/bin/env -u OPENAI_API_KEY -u CODEX_API_KEY`
outer command from the independent-host procedure. Replace only the final server
command with this ordered pair:

```text
<QUAL206_NODE> <QUAL206_REPO>/scripts/qual_206_legacy_conformance_server.mjs
--legacy-stdio-conformance-only
```

The unchanged proxy records allowlisted method and operation labels, frame and
parameter sizes and SHA-256 digests, response outcome and timing, source commit
and process lifecycle. It never records raw parameters, results, credentials or
stderr. The two opening methods remain deliberately labelled `other`; their exact
frame and parameter hashes still document the negotiation without retaining the
client identity payload.

Use `claude mcp list` first because it checks connection health without asking a
model to perform a task. A Codex registry listing confirms configuration but does
not itself open the MCP server; do not invoke a model task merely to manufacture a
readiness result when model authentication is unavailable. Transport readiness may
be `ready` after initialisation and listing succeed; capability remains `unscored`
until a bounded call and result are observed. Remove the disposable profile,
telemetry and detached worktree after a
reviewed path-free summary is produced.

One credential-stripped exploratory Claude Code `2.1.204` health check against the
uncommitted candidate completed the `2025-06-18` initialise exchange and
`tools/list`, then exited cleanly with no pending request. It used no model
authentication and made no model task, tool call or resource read. Codex CLI
`0.146.1` accepted the same closed server definition through a configuration-only
check, but its registry command does not open the server; Codex connectivity
therefore remains untested and capability remains unscored. The new path-free
[`exploratory summary`](../../tests/interoperability/evidence/legacy-fallback-exploratory-2026-08-20.json)
binds the source and compiled runtime bytes, frame and parameter digests, timings
and isolation controls. It explicitly has no candidate commit and is not accepted
host evidence; repeat it from an exact reviewed commit before making a support
claim.

That exploratory summary deliberately retains base commit `b798a40`, a null
candidate commit and its original runtime hashes because those are the bytes that
were observed. The rebase did not rerun a host, use a credential, touch the
ChatGPT tunnel or upgrade that exploratory observation into accepted evidence.

### Protected-main Claude Code transport readiness

A later isolated `claude mcp list` observation repeated the transport check from a
clean, detached checkout of exact protected-main commit
`30b575beb27ff805745a2864c1acf44392774046`, tree
`bb84c13d618984304d5db300be775275b8037ea8`. The current telemetry wrapper and
the protected-main source blobs are bound in the separate
[`Claude Code legacy STDIO readiness summary`](../../tests/interoperability/evidence/claude-code-legacy-stdio-readiness-2026-08-23.json).
The temporary profile removed both supported OpenAI key variables from the parent
and MCP child environments, supplied no model authentication and left no scoped
process running after the check.

Claude Code `2.1.204` returned `Connected`. Its `2025-06-18` legacy STDIO session
completed initialisation, the initialised notification and `tools/list`, then exited
cleanly with no malformed, truncated or pending request. This makes the tested
transport `ready`; it does not score host capability. The launcher was the
constructor-only two-tool conformance seam, not the exact-five unregistered
production assembly. No model task, tool call, resource read, live provider,
remote HTTP host, registration, activation, deployment or release was exercised.

This new record does not change either historical result. The 20 August
modern-only attempt remains `not_ready` because it received `-32022`, and the
uncommitted fallback observation remains exploratory. Complete a separately
authorised, bounded model task before scoring Claude capability, and complete the
remaining independent desktop and remote HTTP evidence before claiming the full
independent-host gate.

This fallback is local-only. Do not attach it to the existing ChatGPT tunnel,
change that tunnel's profile, publish its address, activate a production tool or
infer general host compatibility from the official-client regression.

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

### Pending deterministic expansion

The ten-case [`qual_206_cases.json`](../../tests/interoperability/qual_206_cases.json)
remains byte-identical at SHA-256
`23ac9bc1a76d524bd0e250b11b9ba321b09e66bd5921f1463f50c150001cd389`
and Git blob `728c9902b98c45f0a123127cb0756e86ba7a1113`. This preserves the exact
corpus identity recorded by the earlier ChatGPT and Codex sessions.

The separate schema-validated
[`qual_206_cases_expansion.json`](../../tests/interoperability/qual_206_cases_expansion.json)
composes seven additional cases with that frozen base. Every new case is `non-live`
and `unscored`. Six remain pending behind the
`design-only-no-runtime-wiring` activation boundary. `HOST-015` alone is locally
passing at `local-runtime-wired-production-unactivated`; this does not make it an
observed host result or evidence of current public tool availability.

| Case | Boundary | Expected pre-activation assertion |
| --- | --- | --- |
| `HOST-011` | `selection.resolve` ambiguity | Ambiguous or incomplete selection fails before a provider call or evidence write; only the exact reviewed resource can resolve. |
| `HOST-012` | historical and near-match drift | Historical, workplace and unreviewed `latest` candidates do not replace fixed dataset version `121`; equal scores remain ambiguous. |
| `HOST-013` | `data.query` validation | Dataset, version, dimension, option, order, unknown-field and limit mutations fail before adapter egress with no receipt or ledger write. |
| `HOST-014` | partial and drifted output | Empty, duplicate, identity-drifted, count-mismatched or degraded output is never described as complete and cannot gain evidence. |
| `HOST-015` | response lost after persistence | **Locally passing, non-live and unscored:** one caller key prevents another execution after restart, and inspect v2 recovers the verified receipt without replaying the result. |
| `HOST-017` | tool metadata and repair-hint poisoning | Registry drift fails closed; instruction-like metadata remains quoted data and cannot select an unregistered tool or external destination. |
| `HOST-018` | host fallback provenance | Use a complete same-source structured or text result, or report unsupported; never substitute web search, another plugin, a custom artefact or an external service. |

The executable test title begins
`QUAL-206-HOST-015 drops a persisted response then reconciles after restart`. Its
first-call wrapper awaits the application success, verifies persistence and then
throws without exposing the result or receipt identity. Fresh ledger, index and
application instances reopen. A same-key retry returns receipt-free
`idempotency_completed` with status `409` before health, estimate, rights,
provenance or provider execution. A separate inspect v2 call recovers the original
receipt, record, event and storage identities. Assertions require exactly one
provider execution, record and event and scan index/problem/inspection material for
the raw key and observation.

The accepted inactive public-read transport and reconciliation slices also prove
direct, modern MCP HTTP and modern MCP STDIO parity for the wrapper, completed retry
and v2 inspection. They do not edit the source-hashed ten-case corpus, turn the local
fixture into host evidence or change any historic result. `data.query` advertises
`idempotentHint: true` because the mandatory key cannot repeat side effects; a repeat
returns `409`, not a replayed success. See the
[public-read transport boundary](TOOLS-205_PUBLIC_READ_TRANSPORT.md).

Reproduce the evidence with `pnpm run test:interoperability`. The script builds the
gateway, runs the historical minimised-telemetry harness and explicitly runs the
compiled `apps/mcp-gateway/dist/test/qual-206-host-015.test.js` fixture. The local
fixture records deterministic counters and content identities in assertions; it
does not publish a session log or raw request/result. Host sessions must continue to
use the digest-only proxy described above, with frame sizes, hashes, timings and
bounded outcomes rather than raw keys, arguments or responses.

`HOST-016` is deliberately not a runnable case. Its source-bound cache incident
shows why an ingested status cannot prove shard coverage. The implemented-inactive
T04 fallback is one exact content-addressed ONS observation cache; it does not prove
multi-shard coverage. Make `HOST-016` runnable only after a governed coverage cache
records source version, expected and ingested shard counts, checksums, retrieval
time, licence, expiry and rebuild identity. Until then, a runnable coverage claim
would misrepresent the product boundary.

The expansion extends the retained coverage without changing earlier case objects:
`HOST-015` adds the lost-response evidence boundary related to `HOST-002`,
`HOST-017` supplies a concrete registry and repair-hint matrix related to
`HOST-006`, and `HOST-018` adds the external-substitution prohibition related to
`HOST-005`. Existing live and readiness results retain their original labels.

## Earlier ChatGPT-candidate local assurance

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
These are the earlier local candidate results for the final ChatGPT evidence
wrapper. They predate the legacy fallback and remain historical. Their then-current
candidate commit, protected pull-request checks and protected-main provenance were
pending at that point.

## Rebased fallback-candidate local assurance

On 21 August 2026, the rebased local fallback candidate passed:

- interoperability `13/13` and gateway `105/105` tests, including raw and
  official SDK `2025-06-18` journeys, modern-only production entrypoints and
  constructor-authority non-bypass;
- the complete locked `pnpm run check` gate with contracts `19`, evidence `38`,
  authority `3`, policy `11`, provider adapter `32`, tool registry `7`, gateway
  `105` and interoperability `13` tests;
- Explorer build-policy `16`, unit/component `42` and browser `27` tests;
- repository Python `109` and execution-service `20` tests;
- two byte-identical release builds, `35` schemas and `76` records, `343` local
  links, `183` research hashes, `2` ledgers and `71` source identifiers;
- a `633`-file secret and machine-path scan, `9` rendered diagrams and a
  `165`-component CycloneDX SBOM.

The provider-adapter suite passed `31` deterministic tests and deliberately skipped
its single explicitly enabled live probe. No provider call, host probe, credential,
tunnel action, activation or deployment formed part of this rebase assurance. The
fallback subsequently passed exact pull-request review and protected-main assurance
through pull request 40. No host was rerun during that acceptance, so its exploratory
readiness and capability classifications remain unchanged.

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
