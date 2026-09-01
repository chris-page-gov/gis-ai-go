# Run the `v0.2.0` local candidate

This guide is for someone who wants to clone GIS AI GO and connect a local MCP
client to the complete read-only candidate. It does not need Azure, a hostname, an
ONS account or an API key.

The important boundary is in the name: this is the **unreleased `v0.2.0` local
candidate**. The latest supported public release remains `v0.1.0`.

## What you will run

The command starts one HTTP server on your own computer:

```text
MCP client on this computer
        |
        | MCP Streamable HTTP
        v
http://127.0.0.1:8787/mcp
        |
        +-- five read-only tools
        +-- three read-only resources
        +-- private evidence state for this session
        +-- deterministic outage plus approved cache
```

`127.0.0.1` is the loopback address. It means the server is reachable from the
same computer only. It is not a public website and is not available to a cloud
client unless a separately governed tunnel or deployment is used.

## Before you start

You need:

- Git;
- Node.js `24.19.0`;
- pnpm `10.33.2`;
- Python 3.12 or later;
- uv `0.12.2`; and
- enough free space for the locked JavaScript dependencies and generated local
  build output.

You do not need Docker, a provider credential or an Azure account for this path.

Check the installed versions:

```bash
git --version
node --version
pnpm --version
python3 --version
uv --version
```

Use the repository baseline versions if Node.js, pnpm or uv differs. Python must
satisfy the version declared in `pyproject.toml`.

## 1. Clone and install

```bash
git clone https://github.com/chris-page-gov/gis-ai-go.git
cd gis-ai-go
pnpm install --frozen-lockfile
uv sync --locked --group dev --cache-dir .uv-cache
```

The install may contact the JavaScript and Python package registries. The running
local candidate does not need Internet access and must not call the live ONS
provider.

You can first run the repository's independent exact-five acceptance:

```bash
pnpm run test:local-candidate
```

It starts the maintained loopback entrypoint in a credential-free child, discovers
the five tools and three resource classes, calls all five tools, inspects linked
evidence, requires zero guarded provider egress and checks orderly teardown.

## 2. Start the local candidate

From the repository root on macOS or Linux, run:

```bash
./scripts/start-local-candidate
```

Keep that terminal open. The launcher builds the required checked source, creates
owner-only temporary evidence state and starts the server at
`http://127.0.0.1:8787`.

The launcher should report the local URL and the `candidate-unregistered` boundary.
Do not continue if it reports another address, a live provider or production
registration.

The direct wrapper replaces itself with the maintained Node.js runtime after the
build. That lets the runtime receive `Control-C` itself, remove the temporary state
and return a successful exit. `pnpm run start:local-candidate` is retained as a
convenience alias, but pnpm may print an `ELIFECYCLE` message when a terminal sends
`Control-C`; use the direct wrapper for the clean documented shutdown journey.

The startup event deliberately reports `software_version` as `0.1.0` and
`target_release` as `0.2.0`. The first value remains aligned with the unreleased
repository manifests; the second identifies the candidate being evaluated. The
manifests change only in the later release pull request after every `v0.2.0` gate
passes.

It also reports these fixed provenance fields:

```json
{
  "provider_egress": false,
  "provider_observation": "deterministic-in-memory-http-503",
  "data_query_source": "byte-verified-approved-cache"
}
```

## 3. Check health and readiness

Open a second terminal in the same checkout.

Check that the process is alive:

```bash
curl --fail --silent --show-error http://127.0.0.1:8787/healthz | python3 -m json.tool
```

The JSON response includes these fields, plus the verified catalogue identity:

```json
{
  "status": "ok",
  "lifecycle": "candidate-unregistered",
  "production_registration": false
}
```

Then check that the exact-five assembly and its evidence dependencies are ready:

```bash
curl --fail --silent --show-error http://127.0.0.1:8787/readyz | python3 -m json.tool
```

The JSON response is ready only when it reports:

```json
{
  "status": "ready",
  "reason": "candidate-assembly-verified",
  "production_registration": false
}
```

The complete response also lists the same exact five active tools and direct API
operations.

Health alone is not enough. Connect a client only when both checks return HTTP
`200`. The generated direct API contract is available for inspection at
`http://127.0.0.1:8787/openapi.json`.

## 4. Connect an MCP client

In a client that supports local MCP Streamable HTTP, create a server connection
with these values:

| Setting | Value |
| --- | --- |
| Name | `gis-ai-go-local-candidate` |
| Transport | Streamable HTTP |
| URL | `http://127.0.0.1:8787/mcp` |
| Authentication | none |

Client configuration file names and field names differ. A common configuration
shape looks like this, but use the documented configuration surface for your
client:

```json
{
  "mcpServers": {
    "gis-ai-go-local-candidate": {
      "type": "http",
      "url": "http://127.0.0.1:8787/mcp"
    }
  }
}
```

The client must run on the same computer. A website, hosted model session or remote
client cannot normally reach your computer's `127.0.0.1`. This quick start does not
configure a tunnel.

After saving the connection, refresh MCP discovery or restart the client if its
instructions require that. The client must discover exactly these five tools:

1. `catalogue.search`
2. `catalogue.describe`
3. `selection.resolve`
4. `data.query`
5. `evidence.inspect`

It must also discover exactly `catalogue.public`, `catalogue.record` and
`evidence.receipt`. Some clients display tool names with underscores, for example
`catalogue_search`, because they sanitise names for their own function interface.
That presentation does not add or rename a GIS AI GO capability.

Stop if the client shows fewer or more than five tools, requests a provider key, or
reports a production service. Capture the server output before troubleshooting.

## 5. Follow the governed journey

Use the client to follow this coherent ONS weekly-deaths journey and inspect its
tool-call trace after each step:

1. call `catalogue.search` with query `ONS Data API`, type facet `provider` and
   limit `1`, then confirm it returns `PV-ONS-DATA`;
2. call `catalogue.describe` for `PV-ONS-DATA`;
3. call `selection.resolve` for `PV-ONS-DATA`, dataset
   `weekly-deaths-region`, edition `time-series`, version `121`, England
   (`E92000001`), 2026, week 24 and all causes;
4. pass the returned fixed `data_query` parameters to `data.query`, with a new
   idempotency key; and
5. pass the `data.query` evidence receipt identifier to `evidence.inspect`.

The final value comes from the exact byte-verified approved T04 cache after a
deterministic in-memory HTTP `503`. The result, warning and receipt identify that
fallback explicitly; the receipt records `read-approved-provider-cache`. It is
suitable for learning and contract evaluation, not for quoting as a current ONS
statistic. The journey shows that catalogue discovery, deterministic selection,
cache-labelled execution and evidence inspection share one governed contract
without asking a language model to calculate geography.

The governed warning retains the phrase “The ONS request failed” because the shared
schema and historical QUAL-206 receipts are hash-bound. In this local profile it
means the deterministic in-memory `503`, not an attempted network request. The
startup provenance fields above make that boundary explicit.

## Safety guarantees

The dedicated launcher is deliberately narrower than a deployable service:

- it binds only to `127.0.0.1:8787`;
- it exposes exactly five read-only tools and three read-only resources;
- it uses checksum-bound repository catalogue material, a fixed deterministic
  in-memory HTTP `503` and the exact byte-verified approved T04 cache;
- it does not require, read or use a provider credential;
- its provider execution receives only the deterministic outage through an in-memory
  transport with no DNS, socket, HTTPS or fetch seam;
- it marks production registration as false; and
- it keeps the ledger and reconciliation index in an owner-only temporary directory
  for the running session.

The fixed outage transport is not a complete operating-system network sandbox.
It proves that this provider execution had no egress-capable transport; it does not
claim that the Node.js process is technically incapable of every possible network
operation.

The included approved cache has a recorded `stale_after` boundary of
`2027-02-20T20:21:08.947Z`. After that time, `data.query` must fail closed until a
new cache is reviewed, content-addressed and accepted through repository assurance.
Do not change the clock or weaken cache validation to keep the demonstration passing.

## Stop and clean up

Return to the terminal running the server and press `Control-C`. Wait for the
launcher to report that the server has stopped before closing the terminal.

An orderly `Control-C` (`SIGINT`) or `SIGTERM` removes the session's temporary
ledger and reconciliation state. Receipts created during the session therefore do
not survive a normal restart. Do not use this path to test backup, recovery or
durable evidence retention. An abrupt `SIGKILL`, power loss or process crash is
outside that cleanup guarantee.

If cleanup fails, the launcher reports `local_candidate_cleanup_failed`, returns a
failure status and retries deletion from its process exit hook. Do not treat that
session as a clean demonstration.

The launcher must not change tracked repository files. You can check afterwards:

```bash
git status --short
```

No output means the checkout remains clean.

## Common problems

### The port is already in use

Stop the other process using port `8787`, then run the same command again. Do not
change the launcher to a public address or an arbitrary port: its fixed loopback
authority is part of the reviewed boundary.

### Health works but readiness does not

Do not connect a client. Keep the complete launcher output and rerun from a clean
checkout with locked dependencies. Readiness protects the exact tool set and linked
session evidence state; bypassing it would make the result misleading.

### The client cannot connect

Confirm that the client is running on the same computer and supports MCP Streamable
HTTP. Recheck both URLs with `curl`. A client that supports STDIO only cannot attach
to this HTTP quick-start. `pnpm run demo:local` remains the separate one-shot STDIO
demonstration, but it starts its own child, completes the fixed journey and exits.

### The client shows underscored tool names

This is expected in clients that cannot expose a dot in a function name. Confirm
that there are still exactly five names and that each maps to the corresponding
dotted GIS AI GO tool.

## What Azure later unlocks

This local path proves that people can clone and exercise the provider-independent
candidate. An authorised Azure deployment, real hostname and budget are still
needed to collect the different evidence required for a supported public release:

- trusted public HTTPS, DNS and ingress behaviour;
- workload identity and governed provider egress;
- shared durable storage, backup and restore;
- operational limits, monitoring and incident handling;
- independent remote-host interoperability;
- exact deployed-image rollback; and
- MCP Registry publication after all release gates pass.

Those external steps may reuse the exact-five assembly, but they must not turn this
local approved-cache run into a claim about live provider data, production
activation or a released `v0.2.0` service.

For the shorter one-shot demonstration, see
[`QUAL-206 local demonstration`](QUAL-206_LOCAL_DEMONSTRATION.md). For the accepted
architecture boundary, see
[`ADR-0015`](../decisions/ADR-0015-provider-free-loopback-local-candidate.md).
