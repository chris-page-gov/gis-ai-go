# Select a reviewed collection

The optional `collection-selector.js` wraps the existing code-list widget with
an explicit collection choice. It contains no supplier lists, network client,
provider credentials or URL resolver. The examples and tests use fictional
collections only. An offline host supplies each separately reviewed JSON text
by an exact ID.

The host owns source admission, rights, integrity and the ID-to-data binding.
The selector owns selection, bounded parsing, visible progress, cancellation and
replacement of the widget leaf. The existing overlay retains task navigation,
reference tabs, pinning, folding, keyboard controls and history. This component
does not register a remote tool or change the shared-action contract.

## Closed catalogue and payload contracts

`collection-catalogue.schema.json` defines 1–8 uniquely identified collections.
Each has a title, scope note, scheme count, entry-occurrence count and
`selected-sources-only` coverage. IDs are host navigation identifiers, not
supplier scheme names. Runtime checks supplement the schema with uniqueness,
non-blank text and a 32 KiB UTF-8 catalogue limit. No URL field is accepted.

Each payload remains a separate `gis-ai-go.classification-browser.v1` document.
Its raw JSON text is limited to 16 MiB and it must pass the existing widget's
closed validation and match the catalogue counts. The widget's 64-scheme and
20,000-entry-per-scheme limits are unchanged. The host must first validate the
canonical [payload schema](../../okf-plus/schemas/classification-browser.schema.json),
source evidence and exact data identity; matching counts alone is insufficient.

Collection switching does not concatenate, deduplicate or translate schemes.
The selection identity is `(collectionId, schemeId, entryId)`. Identical IDs,
labels or codes across collections do not establish equivalence. Native field
types, dates, version context, coverage and unresolved states stay with their
original schemes. **Search and exact-code comparison cover only the active
collection.** Global search remains an explicit gap.

## Minimal host integration

Load `classification-browser.js` and then `collection-selector.js` as classic
scripts. They expose browser globals; the repository's `type: module` package
setting does not require importing these assets as CommonJS. Supply text data
and a trusted host callback:

```js
const reviewedTexts = new Map(/* exact admitted ID-to-JSON-text pairs */);
const collections = ClassificationCollections.create(
  document.getElementById('classification-browser'),
  reviewedCatalogueText,
  initialCollectionId,
  reviewedTexts.get(initialCollectionId),
  {
    loadCollection: async (id, {signal}) => {
      if (signal.aborted || !reviewedTexts.has(id)) throw new Error();
      return reviewedTexts.get(id);
    }
  }
);
```

The callback receives an admitted ID and AbortSignal, never a supplied URL. It
returns a primitive JSON string. A host using local files must bind each ID to
an exact reviewed file and hash, refuse arbitrary routes and redirects, check
complete bounded bytes, and honour cancellation. This example supplies no such
transport and does not authorise remote loading. When embedding catalogue or
payload text in HTML, retain the escaping requirements in the
[code-list browser guide](CLASSIFICATION-BROWSER.md).

The existing glossary hook can deliberately select a known collection before
filtering it:

```js
const result = await collections.selectCollection(knownCollectionId);
if (result.ok && collections.snapshot().activeCollectionId === knownCollectionId) {
  collections.setFilter(knownCollectionId, query, knownSchemeId);
  collections.focusSearch(knownCollectionId);
}
```

Both query and scheme ID must be strings. An inactive collection cannot be
filtered by a contextual action. The host separately opens the reference tab;
the selector does not simulate clicks, change task/history or alter pinning.
Do not create an implicit global scheme resolver from a scheme ID alone.

## Failure, cancellation and accessibility

A labelled native select lists collections and their counts. A polite live
region reports loading, refusal and cancellation. The active collection title,
supplied scheme count, retained entry-occurrence count and active-search scope
remain visible. The complete collection scope and global-search/completeness
limits appear in a native, initially closed **Scope and search limits**
disclosure. Its summary uses the browser's normal keyboard behaviour. Selection
does not replace this disclosure node or reset its open state or focus; its
context changes only after a new collection is accepted. No scope text is
truncated. A cancelled or failed selection keeps the old widget, filter, page,
selected entry and disclosures intact. Successful switching starts the new
widget at its default filter. Returning to the already active collection does
not reload it. Asynchronous completion does not steal focus.

The selector checks a 30-second monotonic deadline before and after detached
rendering, as well as running a timer. At most two host promises may remain
unsettled. Cancellation requests abort; it does not falsely declare that an
uncooperative host has finished. Stale, late or cancelled responses cannot
replace the current display. Re-entrant callbacks and changing data descriptors
are handled through captured values and finite error projection. Host exception
text and accessors are not displayed. There is no automatic retry or payload
cache. JavaScript cannot pre-empt a synchronous host callback; the post-callback
check refuses its late result.

`dispose()` stops new work and invalidates pending results while leaving the
current widget readable. It does not claim to terminate work outside the host's
control. Native controls provide manual fallback; human comprehension and
assistive-technology acceptance remain host-specific.

## Evidence and tests

The focused threats are arbitrary-route input, stale asynchronous replacement,
changing host inputs, oversized or invalid payloads, exception disclosure and
unintended task/reference side effects. The closed schema, host ownership and
fictional tests address this bounded local component; they do not confer
provider authority or source correctness.

Run `node test_collection_selector.cjs` in this directory. The affected
`test:experience` command also includes this suite. The repository Python tests
validate the catalogue schema with fictional data. Existing widget and overlay
tests remain unchanged. Synthetic checks cover malformed data, false-like
filter values, stale/cancelled loads, re-entrancy, deadlines, capacity and
pin/fold/task/history compatibility. Disclosure checks preserve complete scope
text, native controls, focus and open state during success, failure and
cancellation. Real-browser, host-loader, source-data,
rights and publication checks remain separate.
