# QUAL-206 Claude HOST-002 capability observation

## Purpose

This procedure observes one narrow model-mediated capability after the harness has
merged to protected `main`: Claude Code `2.1.245` uses local MCP `2026-07-28` STDIO
to complete frozen case `QUAL-206-HOST-002` with `catalogue.search`.

It does not activate the candidate or prove the exact-five journey, remote HTTP
interoperability, a live geospatial provider, registry publication, deployment or
release. The external SSD and the separately relocated `mcp-geo` ONS cache are not
used.

## Closed observation boundary

The launcher and observer enforce all of these conditions:

- a clean detached checkout whose `HEAD` is the exact local `origin/main` commit;
- the accepted Claude Code `2.1.245` executable identity;
- the pinned current model identifier `claude-sonnet-5`;
- one MCP server advertising only `catalogue.search` and no resources;
- no Claude built-in tools, `dontAsk` permission mode, one tool-use turn and the
  required final text-only turn;
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

For first-party login authentication, unset recognised credential variables before
the run. Do not use `--bare`: the exact 2.1.245 client reports that bare mode does
not read first-party login or keychain authentication. The harness therefore uses
the normal login profile while excluding user and project settings, disabling
built-in tools and failing unmatched permission requests closed. The private
preflight checks the authentication method, but no subscription value is published
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
the same independently verified receipt in exactly two reported model turns: one
tool-use turn and one final text-only turn. Continue to describe the five-operation
journey as repository-local until a separately governed model-host observation
exists. Remote HTTP, live provider, deployment, activation, registry and `v0.2.0`
release gates remain separate.
