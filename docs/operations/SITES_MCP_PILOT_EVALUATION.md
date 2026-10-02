# Private Sites MCP pilot evaluation

This is an exploratory development harness for the separate private Sites pilot.
It does not complete the public `v0.2.0` release, prove PSGA entitlement or replace
independent client and deployment acceptance. The
[case corpus](../../evaluation/sites-mcp-pilot-cases.v1.json) is developer-authored
and visible during implementation; it is not a blinded or independently validated
benchmark. Historical QUAL-206 corpora and observations remain unchanged.

## Questions and admission

| Cases | What they assess | Admission |
| --- | --- | --- |
| Q01–Q02 | OS named-place candidates and representative coordinates, preserving ambiguity | Initial, requires an appropriately configured OS Names API key |
| Q03 | OS Open Names product/release metadata | Initial, metadata only; no archive download |
| Q04–Q05 | Specified-month UK CPIH index levels, unit and native series | Initial, maintained L522/MM23; not a local inflation estimate |
| Q06–Q08 | Population, comparison and Census overcrowding | Conditional; no matching executable profile yet |
| Q09 | Point-to-MSOA containment | Conditional; a name match does not establish containment |
| Q10 | Inspect the preceding successful provider result's receipt | Initial; requires a successful earlier result in that repetition |
| Q11 | Explicitly disabled protected/PSGA capability | Negative capability check; private access is not entitlement |
| Q12 | Caller-supplied protected-data/entitlement fields | Negative closed-input check; no unadvertised tool is invoked |
| Q13 | ONS MSOA 2021 names/codes matching a name prefix | Initial; bounded England-and-Wales lookup with explicit truncation |

Q02 does not assert that the first text-search match represents the whole town.
The candidate type and interpretation remain part of the returned data. Q13
does not close Q09. Conditional cases are recorded as `not-admitted`, never
passed or silently replaced with different questions. Natural-language questions
document user intent; this harness sends fixed typed inputs, not model prompts.

Use the six advertised tools only: `sites_capabilities`, `sites_os_names`,
`sites_os_open_product`, `sites_ons_cpih`, `sites_ons_areas` and
`sites_evidence_inspect`. Unexpected or missing tools fail preflight before any
evaluation calls. Existing captured-CPIH tools are a separate historical profile.

## Reproducible local checks

Install the repository's locked Node and Python dependencies using its normal
instructions, then run:

```bash
node --test tests/interoperability/test_sites_mcp_evaluate.mjs
```

The tests inject Fetch and use the actual pinned MCP client `2.0.0`. They make no
network calls. They cover legacy initialisation for `2025-06-18` and `2025-11-25`,
modern `2026-07-28` discovery, semantic assertions, closed authority inputs,
secret/payload-free reports, report-schema validation, bounded requests under
concurrency, redirects, streaming, excessive responses and timeouts. The Python
schema check uses the repository's `.venv` and locked `jsonschema` dependency.

Local transport success does not establish hosted identity, provider availability
or a successful OAuth flow. Keep the provider, evidence-store and assembled
Workers tests as separate checks. Mandatory canonical CI remains unchanged.

## Authorise one live run

Use a private manifest with exact deployment identity and source revision. These
fields are operator declarations; compare them with the live Sites control plane
and deployed artefact independently. Successful provider responses must carry the
declared software revision. A self-reported revision is not build attestation.

The example below is a template: replace the deployment/source values and exact
Site origin after checking the actual deployment. Its small case set deliberately
does not require OS Names credentials. The hostname is illustrative.

```json
{
  "schema": "gis-ai-go.sites-mcp-evaluation-manifest.v1",
  "origin": "https://gis-pilot.example.chatgpt.site",
  "path": "/pilot/mcp",
  "deployment_id": "replace-with-confirmed-deployment-id",
  "source_revision": "0000000000000000000000000000000000000000",
  "protocol": "2025-06-18",
  "credential_kind": "sites-api-bypass-token",
  "enabled_case_ids": ["Q03", "Q04", "Q10", "Q11", "Q12", "Q13"],
  "maximum_requests": 20,
  "repeats": 1,
  "concurrency": 1,
  "deadline_ms": 30000,
  "allow_live": true
}
```

Run only after the approved credential is present in the named environment
variable. Do not put its value in a command, manifest, committed file or chat.
The output directory must be new and should be outside the repository:

```bash
node scripts/sites_mcp_evaluate.mjs \
  --live \
  --manifest /private/path/to/approved-manifest.json \
  --token-env GIS_AI_GO_SITES_TEST_TOKEN \
  --output /private/path/to/new-observation-directory
```

The command needs both `--live` and `allow_live: true`. It creates an owner-only
directory and `run.json` with exclusive creation. An earlier result is never
overwritten. An unsuccessful or incomplete run exits non-zero. Any missing
prerequisite for Q10 is visible as `missing-prerequisite`.

For `sites-api-bypass-token`, the same approved token is sent as
`OAI-Sites-Authorization: Bearer …` to the private platform ingress and as
`x-sites-pilot-test-token` to the explicitly enabled application test gate. The
application must have the corresponding digest configured. This is a test
credential, not a signed-in visitor or a completed OAuth exchange.

For a separately obtained `oauth-access-token`, only the standard `Authorization`
header is sent. The harness does not discover OAuth endpoints, register a client,
perform consent, generate or rotate a credential. Its `oauth_flow_verified` claim
remains false in either mode. Native Sites declaration, discovery and independent
client OAuth acceptance require their own observations.

No cookies or caller-provided authentication headers are forwarded. The harness
accepts only an exact HTTPS `*.chatgpt.site` origin and `/pilot/mcp`; it refuses
credentials/ports/query parameters in the target, substitutions and redirects.
Custom domains need a reviewed explicit extension. Streaming is deliberately
unadmitted for this finite-JSON pilot.

## Bounds, measurements and interpretation

Hard harness bounds are 100 wire requests, 20 repetitions, concurrency one or two,
30 seconds per wire request, 64 KiB request bytes and 1 MiB response bytes. The
manifest must choose equal or smaller limits. Initialisation, discovery, optional
SDK traffic and failed requests consume the same global wire budget. The harness
does not reset the application allowance or retry failed cases automatically.
Choose a manifest that leaves room for the handshake and discovery on every
repetition. Exhaustion is a partial result, never success.

Provider calls have separate centrally enforced application allowances. A CPIH
tool call can make two upstream requests. A failed operation may already have
consumed provider allowance or written a receipt; absence of success does not
mean zero consumption or definite absence. Inspect the independent allowance and
receipt checkpoint before another run. Codex usage resets do not reset provider
or Sites limits, and request caps are not financial billing stops.

Reports retain only:

- manifest, corpus and harness digests; declared deployment/source identity;
- case, stage, pass/fail assertions, receipt references and safe error codes;
- HTTP status, complete-response byte counts/digests and client elapsed time;
- the bounded numeric `mcp` duration from `Server-Timing`, when supplied;
- provider-reported upstream request counts, elapsed times and byte counts from
  successful new provider calls, without retaining their payloads;
- per-case and mixed-workload successful-call latency summaries, with sample size.

Null measurements mean unavailable. Zero must not be substituted. Inspection
returns old provider evidence but is not counted as a new provider call. Server
timing includes application dispatch, provider work and evidence persistence; it
does not separately measure D1 write time. Client time includes network and
protocol overhead. There are no model calls in this harness.

Start with a sequential smoke run. For exploratory performance, hold source,
deployment, question set and profile constant, then compare repetitions and
concurrency one/two within the remaining allowance. Use per-case median and range.
The mixed-workload summary is descriptive, not a comparable service objective.
The p95 is withheld below 20 successful samples in its group; even 20 samples is
exploratory and does not justify a service-level claim. Failed-call durations
remain in individual rows and must not disappear from reliability reporting.

Record first-after-deployment separately from subsequent requests. Do not label
either a guaranteed cold or warm Worker without platform evidence. The current
live profile declares no cache; a stored receipt inspection is not a live refresh
or approved outage fallback. Test any later cache policy as a separately identified
mode. Do not manufacture provider failures against live public endpoints merely
to test fallback or throttling; inject them in local tests.

`evaluateResult(caseDefinition, response, context)` is exported for independent
tests and future envelope evolution. It checks native identities/periods/units,
rights and source mode, the parameter/data/receipt content bindings, and relevant
denial semantics. It does not prove that the original provider response was
authentic, that the database committed durably or that an old valid snapshot has
not replaced a newer one. Source semantics, denied-path zero-egress, lost-response
recovery and quota atomicity also need provider/store/assembly tests.

Validate retained output against
[`sites-mcp-evaluation-run.schema.json`](../../schemas/sites-mcp-evaluation-run.schema.json).
Keep unsuccessful runs and their classifications. Publish only a reviewed
summary; no tokens, raw provider responses, personal data, licensed data or local
machine paths belong in the public repository.

## Separate acceptance observations

Before claiming broader deployment acceptance, retain evidence for actual native
MCP declaration/OAuth, owner-only access and unauthorised rejection, independent
client calls, manual/WebMCP parity, cancellation and uncertain writes, provider
suspension, receipt retention across deployment, independently retained
checkpoints and an explicit application-plus-data restore. Test the emergency
stop and reinstate disabled operator access after the bounded checks.

Natural-language host trials can then use the same questions while recording
client/model version, tool selection, clarification, citations and unsupported
answers. Keep that assessment separate from deterministic typed-tool correctness,
network performance and provider licensing. A new model does not turn this
developer-authored corpus into independent user-research evidence.
