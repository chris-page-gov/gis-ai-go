# Public data workbench

Experimental WEB-216 local journey. This is separate from the two-tool WebMCP
Explorer, LOCAL-212 on port 8787, the supported Pages product and a `v0.2.0` release.

## Run from a clone

Use the repository's pinned Node, pnpm and Python/uv environment. Install once:

```sh
pnpm install --frozen-lockfile
uv sync --locked --group dev --cache-dir .uv-cache
pnpm start:public-data-workbench
```

Open **http://127.0.0.1:8788/**. The corresponding MCP endpoint is
**http://127.0.0.1:8788/mcp**. The no-argument launcher does not accept another
host, port, provider or static directory. Stop with Ctrl+C. Unlike LOCAL-212,
this experiment retains its owner-only evidence under the `.gis-ai-go` directory
in your home directory across orderly shutdowns. Do not delete it if you need to
inspect previous receipts. Missing, substituted or corrupt state fails closed;
there is no automatic destructive repair.

The [illustrated walkthrough and observed browser matrix](../../docs/implementation/WEB-216_LOCAL_WORKBENCH_WALKTHROUGH.md)
explain the controls, page tools, expected values and tested limits.

`pnpm --filter @gis-ai-go/public-data-workbench run preview` is a **discovery-only
visual preview** on port 4176. It cannot retrieve data, proxy to a laptop from a
hosted Site or bypass the exact-origin boundary. A deployed Site is not created
by running these commands.

## Try the manual journey

1. Search for `consumer prices`, or choose **Budget context**.
2. Read the retired `cpih01` warning. Its frozen catalogue record is not rewritten
   as current. Select the explicitly separate maintained `L522 / MM23` capture.
3. Choose July or January 2026, then **Review selection**. This makes a real MCP
   selection call; a plan does not grant permission or retrieve an observation.
4. Choose **Retrieve captured observation**. The fixed server independently
   verifies the selection, no-egress policy, capture and evidence capacity. A
   successful result includes a durable receipt and shows the returned index level.
5. Choose **Inspect stored receipt**, expand the machine-readable evidence or
   download the returned result. Inspection returns existing evidence, not a new
   inspection receipt or attestation.

The values are **index levels, base year 2015 = 100**, not inflation percentages.
They came from a bounded ONS API capture on 14 September 2026; a local retrieval
does not refresh them. No live source, general query or arbitrary geography is
enabled. A changed month requires review again. During the same page session,
retrying a plan reuses its opaque request key; closing the page loses that
ephemeral key, not the server's durable evidence. Save the returned receipt ID to
inspect an earlier result through MCP or the page tool after restart.

## Use your own AI

No model is embedded. A compatible host can expose four page-scoped tools:

| Page tool | Actual effect |
| --- | --- |
| `workbench_find_data` | Search seven contact-free frozen metadata projections and update visible matches. |
| `workbench_review_cpih_selection` | Call MCP selection and stage the non-authorising plan visibly. |
| `workbench_retrieve_cpih_and_store_receipt` | Read one admitted capture observation through MCP and persist its claim/receipt. |
| `workbench_inspect_receipt` | Read and display the existing result and stored receipt. |

All four change visible page state and conservatively declare `readOnlyHint:
false`; only retrieval changes durable server state. External metadata remains
untrusted. Tool names, schemas and hints are not security permissions. Cancellation
is bounded and a lost response is not proof that no receipt was persisted.

“Site tools” means the functions the **host browser exposes to its AI**, not a
button in the website. Registration and browser version alone do not prove that
Gemini, Copilot or another AI has received callable definitions. Feature detection
and actual host calls must be reported separately; unsupported browsers retain
the manual path. The MCP server advertises three separate experimental tools,
not the supported candidate's five-tool contract.

## Data, assurance and limits

The build reuses the Python experiment's deterministic projection and postings.
The browser accepts bounded ASCII English keywords; it does not claim general
Unicode case-fold equivalence or AI intent understanding. Curated concept edges
are displayed with their authored status. Seven development records are not a
full ONS catalogue or validated user-research sample. The public build excludes
contacts and observation payloads; values reach the page only through retrieval.

The official MCP client is pinned to 2.0.0 and protocol 2026-07-28. It can call
only this page's exact loopback endpoint, with no cookies or redirects. The Node
listener bounds input, concurrency and assets, refuses cross-origin requests and
uses an owner-only identity-bound durable store. The server verifies full admitted
capture material and stored records; the page's display checks are not an
independent cryptographic attestation. Lifecycle output states that checkout HEAD
and admitted static-byte hashes are not clean-build attestations.

Unit tests use mocks only for controller behaviour. Real MCP wire tests live in
the gateway. Actual browser/WebMCP acceptance is recorded separately in the
[WEB-216 journal](../../docs/chronicle/WEB-216_JOURNAL.md). Passing a build or mocked
registration test must not be described as successful hosted or AI-client use.

No OS/ONS geography join, enterprise identity, paid provider, public deployment
or supported release is implied. Sites persistence and provider controls require
separate implementation and acceptance.
