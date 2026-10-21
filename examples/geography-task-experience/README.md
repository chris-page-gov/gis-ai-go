# Geography task experience overlay

These are source assets for a host application, not a standalone or deployed app.
They organise an existing geography workspace into a task navigator, one active
workspace and a reference inspector. Pinning keeps the current reference when
the task changes. Folding hides a pane without discarding its query or state.

The [UX specification](UX-SPEC.md) and [persona/story matrix](STORY-MATRIX.md)
explain the authored learning and evaluation scope. The repository's
[task-composition guide](../../docs/implementation/GEOGRAPHY_TASK_COMPOSITION.md)
owns the conceptual evidence-group matrix. UI panes, evidence groups and
Docker/storage infrastructure are different things.

## Host integration

1. Provide the DOM and safe `$` and `el` functions specified by
   [the versioned contract](OVERLAY-CONTRACT.v1.json). Build each task section
   with its existing controls, captions, keyboard alternatives and provenance.
2. Inject the separately reviewed vocabulary JSON at
   `__VOCABULARY_REGISTRY__` in `experience.js`. It needs `terms` and `sources`
   arrays. Merge [the help supplement](HELP-SUPPLEMENT.v2.json) only after
   checking unique IDs and resolving every source reference against that base.
   The supplement is not independently complete. Keep source review status and
   search-variant authority; a retrieval alias is not an equivalence assertion.
3. Load the host's base stylesheet before `experience.css`. The overlay expects
   the documented class structure; review its interaction with the host CSS.
4. Once the host has loaded its model and built the DOM, call
   `initialiseExperience()` once. Existing cross-task selection handlers should
   call `experienceShow()` and, where relevant, `experienceFeatureView()`.
5. Keep all data operations in the host. This overlay performs no acquisition,
   conversion, spatial join or account action. It only opens an HTTPS source
   link after the user selects it. It reserves the `#task/` URL fragment and ignores unrelated anchors such as skip-link targets. A supplied reference skip link unfolds the inspector before native anchor navigation.

Run the source-only synthetic contract checks with:

```sh
node test_overlay_contract.cjs
```

These tests use synthetic terms and DOM objects. They test state transitions,
search, source-link safety and integration assumptions. They do not replace
rendered-browser, keyboard, screen-reader or human comprehension checks in the
actual host. No private model or selected feature is needed or included.

## Limits

The glossary is deliberately partial. The 13 named format, identifier and modelling gaps from the first audit now
have reviewed primary-source definitions. Future source-guidance entries must
say when a plain-English definition is not yet reviewed. Native attribute names remain
source-owned; their mere presence does not mean their complete semantics have
been explained. The task composition does not assert universal containment,
common source epochs or a navigable network. Practice ticks are in memory and
are not an assessment.

## Selected source code lists

The fourth Reference tab is **Code lists**. It preserves selected supplier lists
separately from the learning glossary. The [code-list integration guide](CLASSIFICATION-BROWSER.md)
defines its reviewed data contract, bounded rendering, safe source links, source
dates, explicit gaps and exact-code comparison limits. No supplier lists are
embedded in these public source assets. A complete selected list is not a
claim of complete product or vocabulary coverage.

The existing test entry point also runs the fictional code-list contract suite;
no additional package or network access is required.
