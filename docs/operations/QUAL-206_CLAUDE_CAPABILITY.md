# QUAL-206 Claude HOST-002 capability observation

## Purpose

This procedure observes one narrow model-mediated capability after the harness has
merged to protected `main`: Claude Code `2.1.245` uses local MCP `2026-07-28` STDIO
to complete frozen case `QUAL-206-HOST-002` with `catalogue.search`.

It does not activate the candidate or prove the exact-five journey, remote HTTP
interoperability, a live geospatial provider, registry publication, deployment or
release. The external SSD and the separately relocated `mcp-geo` ONS cache are not
used.

## Accepted evidence

The verifier-produced
[`Claude Code 2.1.245 HOST-002 capability projection`](../../tests/interoperability/evidence/claude-code-2.1.245-host-002-capability-2026-08-26.json)
records a pass from exact protected-main commit
`5837bd65a482e90238c466673318f007e305c744`, tree
`d68d0cdb12fd555fbb41da0d6d4aba23a69ef44f`. Its SHA-256 is
`558a2a5a337dc2c601b982c11e644390e68c858342b0fe28f9b40bf68d740ebb`.
Every exact-main CI job passed in
[run 32941380816](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32941380816),
and every analysis passed in
[CodeQL run 32941380576](https://github.com/chris-page-gov/gis-ai-go/actions/runs/32941380576).

Claude Code `2.1.245`, reporting model `claude-sonnet-5`, completed MCP
`2026-07-28` case `QUAL-206-HOST-002` with exactly one canonical
`catalogue.search` call and a valid independently checked receipt. The accepted
projection records a two-agentic-turn CLI ceiling and exact final host
`num_turns: 3`; the counters are not interchangeable. This is one bounded
capability pass only. Exact-five model capability, remote HTTP interoperability,
live geospatial-provider use, registry publication, activation, deployment and
release remain explicitly false and open. The raw observation remains local and
owner-only.

## Closed observation boundary

The launcher and observer enforce all of these conditions:

- a clean detached checkout whose `HEAD` is the exact local `origin/main` commit;
- the accepted Claude Code `2.1.245` executable identity;
- the pinned current model identifier `claude-sonnet-5`;
- the documented Claude v2 MCP runtime with automatic modern/legacy-era probing;
- one MCP server advertising only canonical operation `catalogue.search` and no
  resources, with the exact Claude permission alias
  `mcp__gis-ai-go-qual-206-host-002__catalogue_search`;
- no Claude built-in tools, `dontAsk` permission mode, a two-agentic-turn CLI
  ceiling and an exact three-turn final host report;
- exactly one call with `{"query":"INSPIRE","limit":1}` across all MCP child
  sessions;
- no recognised credential environment variable forwarded to the MCP child and
  zero geospatial-provider calls;
- an exact, identity-bound macOS Seatbelt profile that denies all MCP-subtree
  network access, plus a pre-run probe proving durable `fsync` writes still work
  and a loopback connection is denied;
- deterministic record and title checks plus independent inline-receipt
  verification; and
- exact agreement between the observed MCP result and Claude's closed structured
  output.

The server uses the repository's deterministic public fixture. Only model-provider
traffic is expected outside the local machine; one tool-use lifecycle can involve
more than one provider API request. The model can reach the provider, but the MCP
observer and fixture subtree cannot reach any network, including loopback.

Claude Code [documents `--max-turns`](https://code.claude.com/docs/en/cli-usage)
as an error-producing ceiling on agentic turns.
An exact `2.1.245` observation showed that a ceiling of one ended with
`error_max_turns` after the valid MCP result, before Claude could emit the required
structured final response. A second exact observation completed with a CLI ceiling
of two and reported `num_turns: 3`. These are distinct Claude counters: the
launcher records the two-agentic-turn limit, while the verifier requires the exact
three-turn final report. The independent global claim still permits exactly one
MCP tool call, and no public evidence is written until every field passes offline
verification.

The harness rebuilds the enumerated generated first-party runtime closure from an
isolated archive of the accepted source and requires an exact closure match. It
also binds the installed dependency closure, lockfile, Node runtime and narrowly
allowlisted pnpm workspace links. It deliberately claims neither complete
first-party generated-closure binding nor complete runtime source binding:
installed dependency bytes are measured, but are not independently reconstructed
from authenticated upstream source, and local build-tool identity and source remain
unbound in this step.

## Assurance before any model call

Do not run a live observation from an implementation branch. First run:

```bash
pnpm run test:interoperability
uv run --locked --cache-dir .uv-cache \
  python -m unittest tests.contract.test_qual_206_claude_capability
pnpm run validate:contracts
pnpm run validate:links
pnpm run validate:secrets
```

The capability contract module invokes the complete Node harness regression file.
This keeps the new suite in the repository gate while preserving the byte-exact,
package-bound historical v1 evaluation receipts.

Merge the harness only after the complete repository gate, pull-request checks and
protected-main checks pass. The implementation pull request must contain no live
capability evidence.

## Authentication choice

The preferred route uses the repository owner's normal Claude first-party login.
Run `claude auth login` interactively if `claude auth status --json` says that the
client is logged out. This user action is required because the harness neither
handles nor stores login credentials.

Claude Code has separate MCP runtime generations and negotiation modes. The
capability launcher pins `MCP_SDK_GENERATION=v2` and
`MCP_PROTOCOL_NEGOTIATION=auto`, matching the accepted strict-modern transport
observation. This keeps `server/discover` and the final MCP `2026-07-28` session
available on the model-task path; it is invocation-local configuration, not a
gateway activation switch and is not forwarded into the fixture's closed child
environment.

Claude Code `2.1.245` normalises the dot in the advertised `catalogue.search`
operation to an underscore on its permission surface. The launcher therefore
allowlists the exact host-facing alias
`mcp__gis-ai-go-qual-206-host-002__catalogue_search`, while the MCP wire request,
observer contract and evidence continue to use the canonical `catalogue.search`
name. The regression fixture checks both the command-line and settings allowlists
so these two namespaces cannot silently diverge again. The alias builder applies
the current MCP tool-name guidance—1 to 128 ASCII letters, digits, underscores,
hyphens and dots—and rejects any canonical-name collision after Claude's observed
dot-to-underscore transformation. `catalogue.search` therefore remains the public
protocol name; `catalogue_search` is not a replacement API.

MCP request `_meta` is an open extension object. The observer requires the core
`io.modelcontextprotocol/protocolVersion` and
`io.modelcontextprotocol/clientCapabilities` fields and permits additional client
metadata whose keys follow the standard prefix-and-name grammar, instead of
treating the object as a closed record. The optional
`io.modelcontextprotocol/clientInfo` is checked separately as an observation
attribution predicate; it is not trusted as a security identity, which remains
bound to the independently measured Claude executable. This first-and-only call
still requires exact top-level parameters and rejects `requestState` or
`inputResponses`, because the observer never issues an `input_required` result.
See the official
[tool-name guidance](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
and [`_meta` rules](https://modelcontextprotocol.io/specification/2026-07-28/basic#_meta).

For first-party login authentication, unset recognised credential variables before
the run. Do not use `--bare`: the exact 2.1.245 client reports that bare mode does
not read first-party login or keychain authentication. The harness therefore uses
the normal login profile while excluding user and project settings, disabling
built-in tools and failing unmatched permission requests closed. The private
preflight checks the authentication method. It also deliberately omits
`CLAUDE_CODE_SIMPLE=1`: the exact 2.1.245 client treats that mode as logged out even
when its normal macOS Keychain login is valid. No subscription value is published
and this observation makes no billing or remaining-allocation claim.

The alternative API-key route requires `ANTHROPIC_API_KEY` and an owner-supplied
numeric `--max-budget-usd` value. The harness does not invent a spending limit.

## One protected-main run

From the clean detached protected-main checkout, build the generated test runtime:

```bash
pnpm --filter @gis-ai-go/mcp-gateway run prepare:test
pnpm --filter @gis-ai-go/mcp-gateway run build
```

Resolve the Claude executable and create one new private directory:

```bash
QUAL206_COMMIT="$(git rev-parse HEAD)"
QUAL206_CLAUDE_BIN="$(python3 -c \
  'import os, shutil; print(os.path.realpath(shutil.which("claude")))')"
QUAL206_PRIVATE_ROOT="$(mktemp -d -t gis-ai-go-qual206-claude)"
QUAL206_PRIVATE_ROOT="$(cd "$QUAL206_PRIVATE_ROOT" && pwd -P)"
chmod 700 "$QUAL206_PRIVATE_ROOT"
QUAL206_MODEL_ID="claude-sonnet-5"
```

Unset provider credentials and run the first-party-login lane:

```bash
unset OPENAI_API_KEY CODEX_API_KEY ANTHROPIC_API_KEY ANTHROPIC_AUTH_TOKEN
unset CLAUDE_CODE_OAUTH_TOKEN ANTHROPIC_BASE_URL CLAUDE_CODE_USE_BEDROCK
unset CLAUDE_CODE_USE_VERTEX CLAUDE_CODE_USE_FOUNDRY AWS_ACCESS_KEY_ID
unset AWS_SECRET_ACCESS_KEY AWS_SESSION_TOKEN GOOGLE_APPLICATION_CREDENTIALS
unset AZURE_CLIENT_SECRET

GIS_AI_GO_QUAL_206_CLAUDE_CAPABILITY=1 \
node scripts/qual_206_claude_capability_harness.mjs \
  --private-root "$QUAL206_PRIVATE_ROOT" \
  --claude-bin "$QUAL206_CLAUDE_BIN" \
  --source-commit "$QUAL206_COMMIT" \
  --model "$QUAL206_MODEL_ID" \
  --auth-kind first-party-login
```

The launcher writes only a small non-sensitive status to standard output. Raw
Claude output, MCP configuration and hash-chained observations remain in the
owner-only private directory. Keep that directory local unless the owner names a
private destination.

For the API-key lane, use `--auth-kind api-key` and add the explicitly authorised
`--max-budget-usd` value. The launcher applies `--bare` automatically and removes
the key before starting the MCP child.

## Verify and project

Verification is deliberately offline. It requires the same unchanged clean,
detached protected-main checkout. Choose a new output filename and run:

```bash
QUAL206_PUBLIC_DIRECTORY="$(pwd -P)/tests/interoperability/evidence"
QUAL206_PUBLIC_NAME="claude-code-2.1.245-host-002-capability-YYYY-MM-DD.json"
QUAL206_PUBLIC_OUTPUT="$QUAL206_PUBLIC_DIRECTORY/$QUAL206_PUBLIC_NAME"

uv run --locked --cache-dir .uv-cache \
  python scripts/verify_qual_206_claude_capability.py \
  --private-root "$QUAL206_PRIVATE_ROOT" \
  --output "$QUAL206_PUBLIC_OUTPUT"
```

The verifier rejects incomplete, failed, widened, tampered or unbound runs before
creating output. A successful projection contains no prompt text, response body,
local path, process identifier, user identity or credential. Review the new JSON,
register that exact evidence instance in contract validation, and submit it in a
separate evidence pull request.

## Interpretation

A verified pass means only that the exact Claude client and model completed one
bounded `catalogue.search` case through the strict-modern STDIO surface and returned
the same independently verified receipt under a two-agentic-turn CLI ceiling, with
an exact final host report of `num_turns: 3`. Continue to describe the five-operation
journey as repository-local until a separately governed model-host observation
exists. Remote HTTP, live provider, deployment, activation, registry and `v0.2.0`
release gates remain separate.
