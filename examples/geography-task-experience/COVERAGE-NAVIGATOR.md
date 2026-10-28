# Dated coverage navigator

This optional component presents a host-reviewed statement of coverage. It does
not calculate coverage from supplier data. The host supplies an explicitly dated
basis, row counts, separate evidence gates and directed relationships. Native
row labels, gate statuses and limitations remain exact display text.

Folded help explains four terms when needed:

- **Documentary denominator:** entries in the selected catalogue or scope statement;
  these are not counts of passing tests or processed payloads.
- **Tested evidence:** a check supports its recorded input, method and result.
- **Scoped status:** a gate status is read with its stated limit, not as a verdict
  about a whole product, current edition or every jurisdiction.
- **Directed relationship:** an evidenced arrow does not establish transitive
  identity, containment, a common snapshot or an unperformed spatial test.

No completion percentage or full-coverage claim is admitted. Inclusion, exclusion
and unclassified scope are separate. Review hashes are displayed references,
not independently verified acceptance.

## Contract and host ownership

The closed [JSON Schema](../../okf-plus/schemas/coverage-navigator.schema.json)
defines the structural contract. `CoverageNavigator.parse()` additionally checks
actual counts, unique identities, exact gate membership, resolvable relationship
endpoints, valid calendar dates and bounded canonical source URLs. It accepts a
JSON string only and returns a deeply frozen independent value. Input is limited
to 1 MiB UTF-8, 256 rows, 16 gates, 64 nodes and 128 relationships. Each evidence
association and text field is bounded. Duplicate JSON member spellings follow
standard `JSON.parse` last-member behaviour; hosts needing exact lexical provenance
must reject duplicates and verify source bytes before supplying this display view.

The host owns source admission, rights, exact-source preservation, date roles and
receipt verification. Schema validity does not establish the truth or freshness
of a supplied status. The widget's `asOf` is the statement date; it is not silently
applied as every source's publication or effective date. Supply the original date
roles and limits in the basis, gate and evidence text. Missing knowledge must be
stated explicitly, not replaced with a positive claim.

Load `coverage-navigator.js` as a classic browser script and its stylesheet after
the host styles. Provide separate native disclosure and content elements:

```html
<details class="coverage-disclosure">
  <summary>Coverage and remaining work</summary>
  <section class="coverage-navigator"></section>
</details>
```

Then call `CoverageNavigator.mount(disclosure, content, reviewedJsonText,
'unique-host-prefix')`. Use a unique lower-case prefix for multiple instances.
The component builds only when first opened. Closing and reopening preserves its
controls; `dispose()` makes its handlers inert. `create()` supports immediate
rendering and provides `setFilter(query, scope)`, `snapshot()` and `dispose()`.
Invalid filter values refuse before changing state. Public API error text is finite.

Rows page in groups of five. A selected row uses a native button and moves focus
to its detail heading. Filtering clears stale detail; paging and changing the view
retain it. Gates, review references and learning help use native `details` and
`summary`. The host retains task, pin, reference, collection and browser-history
ownership. This component performs no DOM click simulation, storage, fetching,
model invocation, feature processing or provider operation.

Permitted links are canonical, query-free HTTPS documentation addresses on the
explicit OS, ONS and Nomis host list in the source, plus `example.org` for fictional
fixtures. No dynamic route is a loader. Links open only following a user action
and use `noopener noreferrer`. All other source text uses `textContent`.

## Validation and release gates

Run the fictional JavaScript checks with:

```sh
node examples/geography-task-experience/test_coverage_navigator.cjs
python -m unittest discover -s tests/contract -p test_coverage_navigator.py
```

The normal `test:experience` script includes the JavaScript suite. The schema test
also checks malformed shapes; runtime tests cover relational constraints, finite
failures, supplementary Unicode, bounds, independent instances and host isolation.

The companion `.reference-inspector select` rule bounds an outer collection
selector that sits outside the inner code-list widget. It changes sizing only;
no collection-selection state or code-list caps change. Static CSS assertions do
not replace actual narrow-pane browser, keyboard, zoom or assistive-technology
checks. A public-source candidate is not a deployment or accepted supplier view.

Owner: the geography task experience host. Threats include false or stale coverage
claims, input amplification, unsafe links and cross-panel state changes. Policy:
closed bounded display data, explicit date and limits, inert source text, no
provider transport and no implication of authorisation. Evidence: fictional
contract and state tests; rendered-host and source-admission evidence remain
separate. See the [component guide](README.md),
[task composition guidance](../../docs/implementation/GEOGRAPHY_TASK_COMPOSITION.md)
and [shared action boundaries](SHARED-ACTIONS.md).

## Local browser smoke path

`coverage-smoke.html` is a fictional three-pane host with the exact synthetic
fixture, an outer collection selector and a lazy coverage panel. Serve this
directory on loopback using an existing approved local static server, for example
`python3 -m http.server 8000 --bind 127.0.0.1`, then inspect
`http://127.0.0.1:8000/coverage-smoke.html`. It does not change another running host.
Check native keyboard opening, search, paging, selected-heading focus, view
switching, fold/reopen state and narrow reference-pane width. Record browser
results separately; the synthetic tests are not a browser acceptance receipt.
