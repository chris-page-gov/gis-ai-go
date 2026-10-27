# OKF Explorer cloud continuation

Owner agreement: 24 October 2026. Related work: [issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153).

> Current evidence — 27 October 2026: the compact canonical Explorer and complete
> public bundle are now the [verified GIS public default](../operations/EXPLORER_PAGES_PUBLICATION.md#discovery-publication-evidence).
> The dated handoff below remains historical evidence. The separate private
> capture review and human learning assessment remain outstanding.

The owner then requested the [discovery repair](OKF_EXPLORER_DISCOVERY.md) for
the public archive's two-facet, zero-relationship projection. Its additional
facets, governed links and bounded source references are a separate increment
whose producer and canonical consumer have merged after required PR assurance.
Complete GIS main CI, CodeQL and the attested main archive have passed. Initial
deployment passed the complete actual public HTTPS walk and all eight browser
cases first attempt. Historical rollback and restore of the identical new
archive also passed their actual public checks. The static discovery publication
and recovery rehearsal are complete. Earlier `8e67ae88…` acceptance remains
separate from the new discovery publication.

## Agreed outcome

Extend the existing [OKF Explorer](https://github.com/chris-page-gov/okf-explorer)
to consume the full GIS AI GO OKF+ metadata and present learning paths,
contextual explanations and source references. The owner agreed that this is
integration with the existing application. Add missing reusable learning-path
metadata to the bundle as small linked records, keeping definitions, provenance
and retrieval semantics application-independent. Inspect existing Explorer
learning support before adding another representation or interface.

The owner requested publication of the reconciled source and continuation in a
fresh cloud chat. Use `codex/okf-223-reconcile-main` in
`chris-page-gov/gis-ai-go`. Its handoff documentation builds on reconciled source
commit `c8a99446017ab9d35c59fc5999ab60e4b339c3dd`, including main at
`59ba0dd1f3d2d06e1188ce382211e82fb679b258` and the original local work. Verify the
remote branch's actual head when starting; publication is not a main merge or
release acceptance.

## Two repositories, separate responsibilities

* **GIS AI GO** owns this OS/ONS knowledge bundle, producers, source evidence,
  bounded semantic retrieval and acquisition planning.
* **OKF Explorer** is the existing application in the separate repository linked
  above. Obtain its current checkout and read its own agent instructions before
  implementation. `apps/public-explorer` in GIS AI GO is a smaller catalogue demo;
  it is not the canonical OKF Explorer application.

The [existing integration](OKF-220_ASK_OKF_INTEGRATION.md) already produces a full
Explorer context corpus v3 with bounded discovery, record, search and relationship
files. Its smaller v1 index is representative only. The descriptor entrypoints
are an integration fragment, not proof of hosted registration. Reuse this work
and check compatibility with the actual Explorer revision. The vendored engines
are pinned to upstream `84fb37f11411c04db8c58046827061f741249002`; that is a dated
compatibility baseline, not a current UI checkout.

The reconciled atomic view contains 32,596 small cards with bounded
search/read/explain. It is separate from the full metadata context projection.
Audit identity and version mappings before connecting them. Do not replace a
small demo's input with a large monolithic bundle or require the AI/browser to
read the entire corpus to explain one field.

## Starting evidence and reusable assets

Read [AGENTS.md](../../AGENTS.md), [PROGRESS.md](../../PROGRESS.md),
[CONTEXT.md](../../CONTEXT.md), the
[reconciliation record](OKF-223_RECONCILIATION.md), the integration guide above
and [OS recovery record](OKF_OS_RECOVERY.md).

* `examples/geography-task-experience/README.md` describes the five-stage
  geography learning overlay and its host contract. It is not standalone.
* `okf-plus/profile/learning-vocabulary.json` contains the reviewed vocabulary;
  `examples/geography-task-experience/HELP-SUPPLEMENT.v2.json` supplies additional
  help. Resolve IDs and source references before integrating them.
* `apps/public-data-workbench/experience.html` is an earlier learning preview
  with 82 authored activities, 222 questions, nine personas and 54 concepts. It
  does not establish full-corpus or live OS integration.
* `scripts/okf_plus/semantic_search.py` provides bounded atomic retrieval;
  `scripts/okf_plus/context_projection.py` supplies the existing Explorer
  projection. Preserve evidence scopes and explicit unknowns.

With the repository's pinned dependencies installed, the existing offline
commands are:

```sh
pnpm run build:okf-semantics
pnpm run build:experience-offline
pnpm run search:okf-semantics --max-records 5 --max-bytes 16384 search "pavement width"
```

The preview output is `artifacts/experience/learn-by-trying.html`. Build and dev
commands for the canonical Explorer must come from its actual checkout.

## Environment and private evidence

Start the fresh chat with the latest published `gis-ai-go` environment
configuration. Check observed credential and network readiness there; an older
running instance does not prove that published settings are missing or that the
key is invalid. The primary requested OS hosts are `api.os.uk`, `docs.os.uk`,
`osmetadata.astuntechnology.com` and `www.ordnancesurvey.co.uk`. Validate actual
bounded access before describing live retrieval as working. Never print the key.
Offline integration should proceed independently of live access.

Generated outputs, ignored handoff archives, account-specific captures and
private selected geography models do not travel with a Git branch. Rebuild
public metadata outputs; restore private evidence only from authorised private
storage when needed. The existing owner authority and limits in CONTEXT.md
apply: metadata now, geographic data on demand, rate limits observed, complete
selected processing followed by verified disposal of temporary payloads.
Do not build a permanent national replica. Dataset requests need a conditional
duration estimate and an API-versus-download comparison.

## Reviewable next increment

1. Verify the starting revisions, environment and both repositories. Identify
   existing Explorer bundle admission and learning facilities.
2. Reuse or add small linked learning-path records with stable IDs, objectives,
   prerequisites, sequence and concept/source references. Keep definitions in
   their authoritative records and distinguish learning links from assertions
   about OS data.
3. Connect the existing Explorer to the bounded metadata and explanation paths.
   Selecting a field should reveal source/version, definition, units, methods,
   qualifications, coverage and retrieval instructions where evidenced. Missing
   information must remain explicit.
4. Make the learning paths and JIT explanations usable in the running Explorer.
   Review pavement width, building heights and road elevation, preserving the
   distinction between relative height, vertical datum and inferred terrain.
5. Provide a runnable preview and targeted browser/accessibility evidence. Check
   links, bounded loading, provenance and representative questions. A schema or
   catalogue entry does not prove that every conceivable question is answerable.

The source reconciliation's focused checks and both OKF audits passed. Its wider
gate remains incomplete on unchanged process-observer tests and unavailable
Chrome. The offline preview built successfully; this instance's system Chromium
blocked local-file navigation. Those limits do not transfer as passing browser
acceptance. Run affected checks in the fresh environment and retain the existing
release gates.

## Start prompt

> Continue from `codex/okf-223-reconcile-main` in `chris-page-gov/gis-ai-go` using
> the latest published cloud environment. Read
> `docs/implementation/OKF_EXPLORER_CLOUD_HANDOFF.md` and follow its agreed scope.
> Make the separate `chris-page-gov/okf-explorer` checkout available and extend
> that existing application to consume the OKF+ bundle with learning paths,
> contextual explanations and source references. Reuse existing integration and
> learning support; keep reusable knowledge in small linked bundle records.
> Verify environment readiness without exposing secrets and continue offline
> integration where live OS access is unavailable. Deliver a runnable review
> preview, relevant verification and an accurate account of remaining gaps.
