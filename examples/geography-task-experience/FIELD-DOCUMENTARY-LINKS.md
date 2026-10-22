# Documentary links for selected fields

This optional panel helps a reader follow a selected field from its native
schema or queryables description to a documented attribute and code-list link.
It is a source component with fictional tests. It includes no supplier payload,
provider transport, current-service check or deployed host.

## Read the evidence in context

A **schema** describes allowed data structures and values. A **queryable** is a
property advertised for supported filtering; returned properties are not
necessarily queryable. The folded help links the official
[JSON Schema Draft 7 validation specification](https://json-schema.org/draft-07/draft-handrews-json-schema-validation-01)
and [OS NGD queryables documentation](https://docs.os.uk/os-apis/accessing-os-apis/os-ngd-api-features/technical-specification/queryables).
These links explain the concepts; they do not validate a host's selected data.

**Documentary candidate** and **API adoption** are project evidence terms. A
documentary candidate connects a native field name and version to an explicit
attribute-level documentation link. API adoption needs evidence that the API
field uses that particular list and edition. A matching name, list of values or
page-level link alone does not establish adoption or semantic equivalence.

Keep each native property name, `originalName`, case, JSON pointer, value type
and version context. Former-name text is displayed as source text and is not
promoted to a search alias. Case-insensitive substring search is a display
convenience; it does not create a field binding. Schema and queryable occurrences
remain distinct. Queryables display the **version from the companion feature
schema**, rather than claiming their own declared version.

Recorded request start and end are retrieval evidence, not publication,
reference or effective dates. A documentation data-schema version does not
establish a code-list edition. The panel retains unknown dates and unresolved
versions. Its default candidate view sits alongside filters for no applicable
link, no exact field match, missing native version and multiple matches. A gap
does not establish missing supplier data or a supplier error.

Historical source wording about nullability is preserved with an adjacent
qualification. A nullable type combined with an `enum` that excludes null
legitimately rejects null; this is not inherently a contradiction. The
[schema interpretation guide](../../docs/implementation/NGD_SCHEMA_INTERPRETATION.md)
explains intersecting constraints, object-only conflicts and metaschema checks.

## Host contract and ownership

The geography experience maintainer owns this optional presentation component.
The host owns source selection, lawful storage, provenance review and its
publication decision. JSON shape checks and matching digests do not establish
source authority or permission to publish.

- Load `field-documentary-browser.js` as a classic script. It exposes
  `FieldDocumentaryBrowser`; the repository's module setting is exercised with
  VM-based tests, without changing the browser loader.
- Supply a UTF-8 JSON string conforming to
  [the field-documentary schema](field-documentary-browser.schema.json).
  `parse()` also checks cross-references, native pointers, source hashes,
  companion versions, constraints and counts. The schema covers wrapper shape;
  it does not replace these semantic checks or independent source review.
- The input is bounded to 4 MiB, 64 native resources, 16 documents, 1,024
  documentary sections and 2,048 field occurrences. Ten results appear per page.
  These limits do not enlarge the separate code-list widget or collection caps.
- Provide a native `details` element, initially closed, with a `summary` and
  child container. Call `mount(disclosure, container, reviewedJsonText)` once.
  The first opening validates and renders; closing preserves its filter and
  selected detail. Add `field-documentary-browser` to the child container and
  `field-documentary-disclosure` to the outer element, and load the scoped CSS.
- Place the panel within the existing Code lists reference pane. Keep task,
  reference, pin, fold and browser-history ownership with the host. The panel
  registers no tool or action and changes no URL or collection state.

The panel searches the selected field observations only. The active vocabulary
collection keeps its own search scope and selected scheme. Both remain visible
as distinct sources of evidence; equal identifiers are not merged.

## Threat, policy and failure boundaries

Source strings and markup are untrusted data. The panel uses `textContent`, not
HTML interpretation. It evaluates no source instructions, formulas or scripts.
Payload links allow only HTTPS OS documentation/API hosts without credentials,
queries, fragments or custom ports; code-list links have a further path limit.
The two official learning links are fixed authored literals, separate from the
payload-link policy. Links open only through the reader's own selection, with
`noopener noreferrer`. The component makes no request itself.

The input API accepts text, not caller-supplied objects with getters. Filter
values are validated and copied before use. Unsupported assertions of API
adoption or equivalence are refused. Invalid input produces a finite visible
message and leaves the existing code-list collection intact. The host should
retain its ordinary source-reading route if the optional panel cannot load.

Native buttons, selects, labels and disclosures provide the keyboard fallback.
Selecting a result focuses its detail heading. Paging preserves the selected
detail and open disclosures; changing filters clears stale detail. Real-browser,
assistive-technology and comprehension checks remain host acceptance gates.

## Evidence and tests

From the repository root, run:

```sh
node examples/geography-task-experience/test_field_documentary_browser.cjs
uv run --locked --cache-dir .uv-cache python -m unittest tests.test_field_documentary_browser
```

`test:experience` includes the synthetic widget suite. The Python suite validates
the same fictional fixture against the schema and probes shape/limit failures.
The widget tests cover provenance and pointer mutations, version uncertainty,
safe text and links, finite failures, filter snapshots, paging, focus and folded
help. The fixture's official hostnames exercise URL policy only; its routes,
identifiers, hashes and content are fictional and are never requested.

The public repository includes no actual field projection, private source
receipts or feature observations. Supplier-specific completeness, rights,
current service behaviour and actual browser acceptance require separate
evidence. No new acquisition or publication permission follows from this guide.
