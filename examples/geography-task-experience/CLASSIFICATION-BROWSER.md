# Source code-list browser

These are source assets for an offline host, with fictional test data. They are
not a standalone deployed application and contain no supplier classification
list. The host supplies a separately reviewed projection conforming to
`gis-ai-go.classification-browser.v1` and the repository's classification-browser
JSON schema. Rights to a list and rights to publish it must be assessed separately.

The browser keeps selected source lists separate from the learning glossary. It
shows 20 results per page, with scheme and entry identity preserved. A matching
code in another scheme is an exact text comparison, not an equivalence assertion.
Source dates, list coverage and definition coverage remain separate.

## Host integration

1. Keep the existing model and all task workspaces unchanged. Add a fourth
   Reference tab labelled **Code lists**, with ID `ref-tab-codelists`,
   `data-reference="codelists"`, `role="tab"`, `aria-selected="false"`,
   `tabindex="-1"` and `aria-controls="ref-panel-codelists"`. Add the corresponding
   initially hidden panel with `role="tabpanel"` and
   `aria-labelledby="ref-tab-codelists"`. It contains an empty element with
   ID `classification-browser`.
2. Use the successor `experience.js` and `OVERLAY-CONTRACT.v1.json` here. They
   extend the previous overlay's reference tab list, keyboard wrap and optional
   contextual action hook. They do not replace the host map or native-data
   renderer. All other host and glossary integration requirements still apply.
3. Load `classification-browser.js` and `classification-browser.css`. Once the
   host is ready, call:

   ```js
   const codeLists = ClassificationBrowser.create(
     document.getElementById('classification-browser'), reviewedPayload
   );
   ```

4. Supply reviewed JSON as data, never executable provider text. A separate
   same-origin JSON asset is preferable. If embedding JSON in a script, escape
   `<`, U+2028 and U+2029 so provider text cannot terminate the script element.
   The widget never fetches anything. It only provides HTTPS source anchors for
   deliberate user selection; unsupported or credential-bearing links are
   visibly withheld.
5. Optional contextual glossary links use
   `window.classificationTermAction(term, card)`. Configure exact glossary term
   IDs and reviewed scheme IDs or literal search text in the host. Append a
   text-only button which opens the reference pane, selects `codelists`, calls
   `codeLists.setFilter(query, optionalSchemeId)` and focuses its search input.
   This is a navigation aid, not a semantic relationship. An unknown scheme ID
   is refused. Do not add hundreds of native codes to the learning glossary.

Pinning and folding remain owned by the overlay. They do not rebuild the widget,
so its scheme, query, page and selected entry survive. Only a deliberate filter
change resets the selected entry. Native buttons, select, input and details
provide keyboard interaction; the matched count is a polite live status. Picking
an entry or a supplied parent moves focus to the detail heading.

## What the display means

- `null`, an empty string and an absent optional field remain different. A
  missing required field is a contract error. A label does not become a definition.
- Optional `labelLanguage` is shown only when supplied. It accepts explicit null
  or a string of 1–80 characters; an empty language string is a contract error.
  Language is never guessed from the text. A whitespace-only source definition
  remains visible as a quoted string, but does not count as a supplied definition.
- Parent and level fields are used only as supplied. Missing, empty, ambiguous
  or self-referencing parent codes remain unresolved. Prefixes and label matches
  do not create a hierarchy. A direct parent is not an inferred ancestry tree.
- The selected source-list denominator is shown alongside retained counts.
  Unknown denominators do not produce percentages. Even a complete selected
  list does not establish complete coverage of a product, jurisdiction or all
  vocabularies. Definition completeness is checked independently.
- Edition, reference date, publication date, retrieval time and projection review
  date are labelled separately. Source strings are not coerced into guessed dates.
- The native-field expander shows all supplied JSON fields for that entry. It
  preserves JSON value types, but does not claim original file byte identity,
  numeric lexical spelling or fully interpreted field semantics. Source hashes
  and locators point to the separate provenance.
- The selected entry can show up to 20 other exact-code occurrences, with their
  total count and an explicit limit if more exist. No supplier crosswalk is inferred.

## Admission and bounds

The host must run the repository schema and source-projection validator first.
The UI performs closed-shape, identity, source-reference, count and scoped
definition checks as defence in depth. It is not a general JSON Schema engine.
Additional display limits are 128 KiB of formatted UTF-8 JSON, depth 16 and 4,096
nodes per native object, and 16 MiB of formatted native text across the payload.
An unsupported object refuses the payload visibly;
native fields are not silently truncated. Search input is limited to 500
characters. The UI does not modify the supplied projection.

Run the source-only checks without installing dependencies:

```sh
node test_classification_browser.cjs
node test_overlay_contract.cjs
```

The first suite uses fictional lists, including malicious text and repeated codes.
The second tests the existing overlay's task, pin, fold, skip-link and learning
behaviour with the fourth tab. Rendered browser checks and actual source-data
integration are separate acceptance steps; human comprehension and assistive
technology evaluation are not implied by these tests.
