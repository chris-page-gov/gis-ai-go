# WEB-216: public-data workbench

Status: authorised discovery and implementation work package; inception record.
Date: 14 September 2026.
Implementation baseline: `872d075c4ac0518c89ad3c2300e8da085fa242af`.

This document records the owner's requested direction, initial source findings,
experiments and acceptance sequence. It is not evidence of a new running service,
completed benchmark, provider call or deployment.

## Outcome and protected boundaries

Evolve the GIS AI GO WebMCP explorer into a working surface where a person and
their own compatible AI can identify appropriate ONS statistics through OKF,
resolve the geography and dataset selection, retrieve bounded data through the
governed MCP service, and inspect the returned data and provenance together.
Ordnance Survey and ONS geography are part of the data design, not decorative
map layers added afterwards.

- Implement in GIS AI GO on an isolated branch. Keep the existing local candidate,
  supported Pages artefact and release evidence unchanged until an affected,
  reviewed implementation is accepted.
- Treat `mcp-geo`, `okf-ons` and `govuk-webmcp` as read-only sources. In particular,
  do not modify, rebuild, redeploy or change competition-submission state in
  `govuk-webmcp`.
- Reuse concepts and explicitly attributed contracts, not entire repositories or
  their private material. Pin committed source revisions. Treat uncommitted
  source changes as drafts, not accepted upstream functionality.
- Start with public, redistributable data and bounded public read operations.
  Product-specific OS rights, attribution and credentials still apply. Government
  staff personas do not imply authority to use staff identity or protected data.
- Preserve the person's own AI as the interpretation layer. No embedded model is
  required. Statistical and geospatial calculations remain deterministic.
- Current [ADR-0013](../decisions/ADR-0013-webmcp-page-tools-boundary.md) describes
  the existing two-tool metadata-only experiment. A new architecture decision,
  threat review and result contracts must precede provider-backed page tools;
  do not silently rewrite historical evidence or widen those two tools.

## First source findings

The [source and story crosswalk](WEB-216_SOURCE_AND_STORY_CROSSWALK.md) records
three pinned repository baselines, reusable contracts and proposed reconciled
personas/stories. It separates historical authored scenarios from observed
capabilities and new user-research hypotheses.

The current WebMCP app searches and describes public catalogue records; it does
not retrieve observations. The gateway's existing ONS adapter is deliberately
bound to one dataset/version/observation request, not a general dataset browser.
See [the app guide](../../apps/webmcp-explorer/README.md) and
[the ONS adapter](../../packages/provider-adapter-sdk/src/ons-data-api.ts).
General discovery must therefore not be presented as general execution support.

The existing gateway provides a web Request/Response transport seam, but ingress,
durable evidence and provider-network controls have platform-specific dependencies.
See [the MCP handler](../../apps/mcp-gateway/src/mcp-http.ts),
[reconciliation storage](../../packages/evidence/src/reconciliation-index.ts) and
[provider transport](../../packages/provider-adapter-sdk/src/fixed-https.ts).
Sites deployment feasibility is an experiment, not permission to remove them.

## Shared journey and proposed website

The proposed first screen is a data workbench, not a marketing landing page:

1. **Choose a task and place.** Short story examples, a manual route and explicit
   guidance for using the visitor's AI. Disambiguate place, nation, geography
   level and period before requesting data.
2. **Find suitable evidence.** Show relevant datasets, why each matches, alternatives,
   coverage, source, units, limitations and what cannot be answered.
3. **Review the selection.** Show dataset, edition/version, dimensions, geography
   codes/vintage, intended joins, estimated result size and execution availability.
   Metadata suitability is not authorisation or evidence that values exist.
4. **Retrieve the data.** The MCP service revalidates the selection, applies policy,
   performs bounded retrieval and returns data and verifiable evidence.
5. **Inspect and use the result.** A table, appropriate map or chart, provenance and
   a compact machine-readable result support the person's AI analysis. Clearly
   separate provider observations, derived values and AI-written interpretation.

Keep beginner explanations beside unfamiliar concepts, with technical detail on
demand. Preserve the complete keyboard-accessible manual journey when page tools
are unavailable. Unsupported, ambiguous, denied, stale, offline and partial-result
states are first-class results, not empty success messages.

### Integration variants to test

- **Dual connection:** the visitor's AI uses page tools for discovery and its
  separately connected MCP client for retrieval. Test the actual host's ability to
  use both and return the selected result to the page; do not assume this bridge.
- **Page-mediated MCP:** a narrow page tool calls a same-origin backend which acts
  as an MCP client to a fixed, approved service. The backend retains credentials,
  admission and evidence controls; the browser cannot submit an arbitrary target.
- **Sites-hosted MCP:** a compatible server-side deployment offers a real MCP HTTP
  endpoint and the same page interface. This requires proven replacement storage,
  concurrency, ingress and provider controls, and independent MCP-client tests.

WebMCP itself does not establish a remote MCP connection. A hosted Site cannot
reach a laptop's loopback address as though it were its own server. Begin the
end-to-end experiment locally; record hosted connectivity as a separate gate.

## Dataset and selection contracts

Keep three separately versioned layers:

1. **Discovery metadata:** source-native identity, concepts, distributions,
   licences, coverage, dimensions, refresh information and execution support.
2. **Selection proposal:** pinned dataset/edition/version, explicit dimension
   values, geography identities, intended derivations and bounded result limits.
   A proposal or its hash cannot grant execution authority.
3. **Retrieved evidence:** actual source/version, retrieval time, values, units,
   missing/suppressed-value handling, transformations, limits and receipt linkage.

For geography, retain GSS code family, nation, geography level, boundary vintage,
coordinate reference system and any exact/best-fit derivation. Preserve source
UPRN/USRN/TOID identifiers where applicable. Do not join using names alone, treat
postcodes as stable polygons, assume GB coverage means UK, or infer property-level
facts from area statistics. OS Open UPRN supplies identifiers and locations, not
an open address-text service. A boundary overlay is not a legal parcel boundary.

ONS statistical API, Census and Nomis families require separate capability
descriptions; Open Geography supplies a different discovery and geography lane.
Resolve actual dimensions/options before execution. Refuse an incompatible
geography or vintage; do not fabricate a lookup or silently interpolate.

## Experiment programme

Use the same pinned, rights-reviewed corpus and held-out story questions across
variants. All experiments below are planned, not completed. Record unsuccessful
and unavailable cases. Prefer the simplest variant that meets correctness,
governance and usability requirements; no design is labelled optimal in advance.
The eight OKF-ONS smoke tasks and twelve gold questions are useful development
material, not an unseen evaluation set. Its confirmatory protocol calls for at
least 50 subject-reviewed unseen questions, preregistration, repetitions and
blinded adjudication. Without that independent work, report exploratory results
and a provisional engineering choice, not validated user needs or optimality.

| ID | Question and variants | Evidence and decision rule |
| --- | --- | --- |
| X01 | Which metadata should be built? Compare story-led subsets, full dataset-level catalogue indexing and hybrid incremental enrichment with lazy dimension options. | Coverage of answerable stories, build time, bytes, peak memory, freshness lag and upstream requests. No bulk observation mirror by default. |
| X02 | Which discovery method helps choose the right data? Compare current bounded keyword/facet search with explicit OKF concept/geography relationships; consider semantic ranking only if a measured gap remains. | Held-out relevance judgements, top-k recall/precision, ambiguous-query clarification, out-of-scope abstention, latency and result size. Review labels before tuning. |
| X03 | Can a selection become a valid query across ONS API families? | Exact metadata-to-query round trips; wrong/missing dimensions, unsupported geography, retired endpoint, changed version, suppression and time semantics must be represented correctly. |
| X04 | Which OS/ONS integration is defensible? Compare authoritative code lookups with purpose-appropriate spatial joins and documented crosswalks. | Known expected joins, cardinality, unmatched/duplicate counts, boundary-edge cases, nation coverage, vintage conflicts and lineage. No silent best-fit substitution. |
| X05 | Which storage/serving layout is proportionate? Compare compact static metadata, indexed relational metadata and columnar/object-store partitions for larger data. | Same logical results; cold/warm latency, transfer bytes, memory, hosting compatibility and cost. Test D1/R2 limits rather than assuming desktop SQL/GIS extensions exist there. |
| X06 | Can refresh be incremental without missing changes? Compare full reference rebuild with checksum/version-aware incremental builds. | Equal logical output, explicit additions/changes/deletions, atomic publication, stale-source handling and measured avoided work. |
| X07 | Which WebMCP-to-MCP path actually works? Compare the three integration variants above. | Exact-version tool discovery, real MCP calls, same visible/tool result, evidence inspection, cancellation, timeout, restart, duplicate request and lost-response behaviour. Mocks do not prove host support. |
| X08 | Does the workbench help the reconciled personas? | Story completion, correct dataset/geography selection, explanation comprehension, keyboard/reflow/accessibility checks and safe failure. Automated tests are not user-research evidence. |
| X09 | Are consumption and operating limits acceptable? | Bounded upstream calls, retries, result sizes and client context use; separate build, hosting, provider and model costs. Unavailable cost remains unknown, not zero. No paid scale test without a specific budget. |

Before each live probe, read the current official endpoint/client contract and
run the relevant offline validation. Set explicit call, time, byte and retry caps;
start serially and increase only when evidence justifies it. Use the existing
source-time journal pattern to record experiment ID, start/end, exact source and
code revisions, configuration, commands, outcome and attributable usage. Do not
retain unnecessary personal prompts or publish private client transcripts.

## Delivery sequence and completion evidence

- **M1 — inception:** source-by-source persona/story crosswalk, existing-versus-new
  distinction, protected-repository record, this experiment plan and acceptance
  criteria. Initial inspection is not empirical validation.
- **M2 — dataset foundation:** run X01–X06 on a bounded corpus, publish reproducible
  results and an architecture decision. Preserve rejected alternatives and costs.
- **M3 — local vertical slice:** implement one government-staff story from OKF
  discovery through actual MCP retrieval to a shared visible result, with a manual
  alternative and a provider-free reproducible test. Mark cached and live results
  accurately. Never use the old fixed observation as if it answered a new story.
- **M4 — geospatial and user-story coverage:** implement the selected OS/ONS joins,
  views, controls and negative cases; run X07–X09 and the reconciled acceptance set.
- **M5 — hosted demonstrator:** prove the selected Sites integration, deployed
  access, persistence where required, exact host interoperability and rollback.
  Preserve the current Site audience. A changed public audience, protected source,
  new paid commitment or unavailable credential remains a separate decision.

Use affected local checks during development and the existing mandatory canonical
assurance before acceptance. Do not repeatedly rebuild unchanged inputs. This work
does not close the full hosted MCP or public `v0.2.0` release gates by implication.

## Current primary references

Reviewed on 14 September 2026; documentation describes contracts, not a successful
live provider observation:

- [ONS dataset structure](https://developer.ons.gov.uk/dataset/).
- [ONS observations: Census and CMD differences](https://developer.ons.gov.uk/observations/).
- [OS Open UPRN specification](https://docs.os.uk/os-downloads/products/addresses-and-names-portfolio/os-open-uprn/os-open-uprn-technical-specification).
- [OS Boundary-Line information](https://docs.os.uk/os-downloads/products/areas-and-zones-portfolio/boundary-line/boundary-line-product-information).
- [Sites hosting](https://learn.chatgpt.com/docs/sites) and
  [Site tools](https://learn.chatgpt.com/docs/webmcp), checked in the preceding
  hosting assessment. Availability, platform limits and host compatibility need
  fresh verification for the implementation. Public data does not remove all
  privacy risks from queries or logs; Sites documents no residency guarantee.
