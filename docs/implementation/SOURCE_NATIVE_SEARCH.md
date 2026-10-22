# Source-native values in vocabulary search

Some documentary rows contain a useful native value whose code interpretation is
unresolved. Other lists have a Label column without a separate code assertion.
These rows can remain Documentation records while still supporting lexical search.

For example, the fictional native value `🆕ZZ13SA` can match a query for `ZZ13SA`
without stripping the marker, adding an alias or asserting a code. Matching text
does not establish equivalent concepts, field adoption or a join across schemes.
Search covers the active collection.

## Reviewed input and exact forms

The optional entry property `nativeSearchForms` contains source-qualified forms.
Each form has `text`, `kind:source-native-value`, `authority:source-stated`, the
entry's existing `sourceId` and `sourceLocator`, an exact `nativePointer` under
`/native/`, and `language:null`. The pointer must resolve to the identical string.
Do not index arbitrary native JSON or infer language from English surrounding text.
An explicit empty object key is valid: `/native/` resolves to `native[""]`.

Source review and hash admission establish which native values and code roles are
eligible. Schema and runtime checks establish consistency with that reviewed input;
they cannot prove that a supplier statement is true. The browser, exporter and
discovery builder do not acquire data or follow source pointers as URLs.

Limits are eight forms per entry, 1,000 Unicode characters per form and 8 KiB of
compact UTF-8 JSON for the form array. Pointers have at most 512 characters and
16 segments. Existing payload, scheme, native-display and output-card limits
remain unchanged. Oversized output is refused, never truncated. Unpaired Unicode
surrogates are refused at the UTF-8 boundary; supplementary characters remain
unchanged.

The browser copies native JSON data through own property descriptors before
checking forms or producing the native display. Accessors and callable custom
serialisation hooks are refused without invocation. Search and display use the
same frozen snapshot, so later caller mutation cannot change the admitted native
context. This is a JSON-data contract, not an execution environment for arbitrary
JavaScript objects.

The optional `codeRole` records a reviewed projection conclusion:

- `source-code-retained`: a non-empty string is retained as a source code.
- `explicit-empty-code`: an explicit empty code string remains empty.
- `unresolved-native-value`: code interpretation remains unresolved; `code` is null.
- `no-separate-code-assertion`: no separate code is asserted; `code` is null.
- `unknown`, including an absent declaration: consult the source context.

These roles do not modify `code`, `aliases`, `native`, identity or dates. A native
Label string may be an enumeration value without a separate code column. Null
does not prove that no code exists. Source-native forms appear separately from
aliases, with provenance, while result identity and navigation remain unchanged.

## Export and discovery

The exporter emits an identified `okfp:LexicalForm` with the unchanged string in
`rdf:value`, `okfp:formKind:source-native-value`, source authority and URL, and
`okfp:sourcePointer` pointing into the record's exact native context. The discovery
builder checks the entire form against the declared entry form, source and locator
before indexing it. The discovery projection retains both its lexical value pointer
and its native source pointer. Equal text in different records remains separate.

No SKOS notation, alternative label, hierarchy or equivalence is inferred from a
source-native form. The existing coded-versus-Documentation decision still depends
on the admitted `code` field. Unknown language remains unspecified.

This is an optional extension to the reviewed browser contract. Updated schema,
widget, exporter and discovery components must be deployed together. Older closed
validators correctly refuse the new fields. Existing payloads remain valid.

Synthetic tests cover exact decorated-value matching, source and pointer conflicts,
missing/null/empty distinctions, escaped and empty keys, duplicate forms, bounds,
qualified-form back-references and distinct scheme identities. Repository assurance
and real keyboard, history and collection-switching checks remain release gates.
