# Source labels and display fallbacks

A source can supply a category code without supplying its label. The interface
may need readable display text, such as `Label not supplied · X1`, but that text
must not become a supplier label in an export. The optional `entry.labelOrigin`
metadata keeps these roles separate. It does not change the code, category
identity, native row, source snapshot or definition.

## Contract and ownership

The source-projection owner chooses and verifies the native label field against
the original source. The host admits the complete reviewed payload using the
[classification schema](../../okf-plus/schemas/classification-browser.schema.json)
and [offline validator](../../scripts/okf_plus/label_origin.py). The browser repeats
bounded checks before displaying it. The knowledge-framework maintainer owns the
export and discovery interpretation. These components provide no source retrieval,
provider execution, publication permission or hosted service.

For a fictional row whose native `description` object has no `value` property:

```json
{
  "kind": "project-display-fallback",
  "sourceId": "fictional-source",
  "sourceLocator": "/rows/0",
  "nativePointer": "/native/description/value",
  "nativeState": "absent",
  "languagePointer": "/native/description/lang",
  "displayLanguage": "en-GB"
}
```

These are all required fields of the optional, closed object. `sourceId` and
`sourceLocator` must match the entry and resolve to a declared source with a
SHA-256 binding. A JSON Pointer starts at `/native/`; escaped slashes, tildes and
an explicitly empty property name remain valid. Every parent must exist. Only a
terminal object property may be absent; an absent array index is refused.

- `source-native` requires the exact native string, including an empty or
  whitespace-only string. It cannot silently replace, trim or translate it.
- `project-display-fallback` requires an absent or null native value. It cannot
  be used to overwrite an existing source string. Its display text remains a
  human-facing label and record title, with its origin stated visibly.
- `nativeState` distinguishes `absent`, `null`, `empty-string` and `string`.
  If `description` itself is missing or null, point to that field, not to an
  imagined child. Missing description and missing value are different evidence.
- `languagePointer` is either an exact native pointer or null for no assertion.
  Native language evidence is kept separate from `displayLanguage`. A fallback
  has null or absent `labelLanguage`, even if a neighbouring native language
  field exists. Empty, null, absent and unasserted native language remain distinct.

Metadata is optional for compatibility. Without it, existing display and export
behaviour remains unchanged; omission is not retrospective proof that a label
came from a supplier. Existing payload files need not be rewritten. New exports separately require an
explicit reviewed producer revision and complete discovery-index schema validation;
see the [export guide](../../docs/implementation/CLASSIFICATION_RELEASE_DISCOVERY.md).

## Export and search

An explicit fallback remains the record's readable `title`. It does not create
`skos:prefLabel`, `rdfs:label`, an alias or a source-native lexical form. The code
and any existing notation, native row, source pointer and source hash remain.
Other independently qualified aliases remain unchanged, but the exact fallback
text cannot be declared as an alias or source-native search form.

The discovery index marks only the `/title` occurrence with `labelOrigin`.
This optional marker states display origin; it supplies no source-stated
lexical authority. The record remains Concept or Documentation according to the
existing code-role rules. It does not become a concept merely because it has
readable display text. Export receipts count source-native, fallback and
legacy-unqualified entries only when explicit origin metadata is present.

Search still finds the displayed fallback. Choosing it reveals its origin,
native state and pointer, and the separately labelled language evidence.
No synonym, equivalence, language, hierarchy or definition is inferred.

## Bounds, threats and evidence

Explicit-origin entries are admitted as inert JSON snapshots: accessors,
custom serialisation hooks, cycles, non-finite numbers and unpaired surrogates
are refused. The complete entry is limited to 128 KiB of compact UTF-8 JSON,
4,096 nodes and depth 16; origin metadata is limited to 8 KiB. JSON punctuation,
escaped strings and numeric tokens count towards the byte limit. Existing
native-display and whole-payload limits also apply. A failed check refuses the
payload visibly or refuses export before creating an output directory. Every
generated knowledge card also passes the canonical record schema. An empty source label is valid source/UI evidence,
but cannot supply that schema’s non-empty human title: export is refused without
replacing the source label or creating output. An authored title policy for such
rows remains a separate future contract.

The main risks are fabricated provenance, promoting authored text to a native
label, and a value changing after validation. Closed metadata, exact pointers,
source bindings and inert snapshots address those structural risks. They cannot
prove that a source is authentic, that the selected native field means “label”,
or that use and publication rights are sufficient. Complete source-specific
reconstruction and independent acceptance remain separate requirements.

## Checks and remaining acceptance

```sh
python -m unittest tests.test_okf_plus_label_origin
node examples/geography-task-experience/test_classification_browser.cjs
```

Run the commands from the repository root. The existing `test:python` discovery
and `test:experience` entry points include these suites. Fictional cases cover
missing and null containers and values, empty and ordinary labels, separate
language roles, pointer escaping, source mismatch, false alias promotion,
byte bounds, hostile callbacks and complete small exports with hash readback.
They do not contain supplier rows. Canonical repository assurance, rendered-host
checks, source-specific rights and publication remain separate gates.
