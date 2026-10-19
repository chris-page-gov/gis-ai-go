# Reporting OS data availability

The offline Python API in `scripts/okf_plus/availability.py` produces a small,
private report for one source, selector and native field. It keeps an access
claim separate from what should exist, what was observed and whether retrieval
finished. Reports carry source and version identifiers, spatial and temporal
scope, the exact field path, evidence references and receipt SHA256 values.

The repository owner owns this internal operation. Source metadata, supplied
observations and receipt contents remain evidence claims. The assessor does not
independently prove an entitlement, expectation, semantic mapping or observation.
Its output grants no runtime admission, retrieval, publication or execution
permission. Existing runtime admission checks apply separately.

## Separate questions

| Axis | Values | Meaning |
| --- | --- | --- |
| `access` | `allowed`, `denied`, `unknown` | The supplied access decision for this request. An allowed request does not establish that data exists. |
| `expected_presence` | `expected`, `not_expected`, `unknown` | A supplied expectation supported by source definitions, coverage or collection evidence. Neither expectation is inferred from an empty response. |
| `observed_presence` | `present`, `absent`, `unknown` | What the supplied observation and retrieval evidence establish for this scope. A present null or zero remains present. |
| `retrieval` | `complete`, `incomplete`, `not_attempted`, `failed` | Retrieval progress for the exact selector. Incomplete or failed retrieval does not establish absence. |

Use `unknown` when the relevant evidence is unavailable. Keep unknown version,
spatial or temporal context explicit instead of silently substituting the current
version or a broader area. A reported result applies to the supplied selector and
field; it does not extend to another selection or source version.

## Status and wording

| Status | Report wording and interpretation |
| --- | --- |
| `present_value` | “The property has a value.” Interpret it using the retained source definition. |
| `present_null` | “The property is present with a null value.” Its reason remains unknown unless the source defines it. |
| `present_zero` | “The property is present with a zero value.” Do not turn zero into missing data. |
| `property_missing` | “The requested property is absent from the inspected complete record.” Check the exact native field path and version. |
| `filtered_empty` | “The complete filtered selection returned no matching records.” This needs a known denominator and an explicit evidenced empty-result reason. |
| `outside_coverage` | “The selector is outside the evidenced coverage.” Preserve the coverage reference. |
| `not_collected` | “The source states this data is not collected for the selector.” Preserve the source statement. |
| `unavailable_product` | “The requested product is unavailable for the selector.” This is distinct from permission denial. |
| `retrieval_incomplete` | “Retrieval is incomplete; absence is not established.” Resume the same selector or explain the stopping limit. |
| `permission_denied` | “Access is denied for this request.” Do not report the data as absent. |
| `transient_failure` | “Retrieval failed; availability is unresolved.” Report the evidenced transient failure and a bounded next step. |
| `retrieval_failed` | “Retrieval failed; availability is unresolved.” The failure does not itself establish an access decision or absence. |
| `unknown` | “Availability is not established by the supplied evidence.” State which evidence is needed next. |

A supplied `property_missing` observation establishes absence only when retrieval
is complete. A supplied empty observation additionally needs
`denominator_known: true` and an explicit reason. The current API requires those
complete-empty conditions for `outside_coverage`, `not_collected` and
`unavailable_product` too; it does not derive those states from a catalogue or
coverage document automatically.

`expectation_gap` is true only when the supplied expectation is `expected` and
absence is established. A `not_expected` claim still needs evidence; it is not a
reason to suppress a contradictory positive observation. Access and retrieval
problems can take priority in the summary status while a retained positive
observation remains visible on the observation axis.

## Small report templates

Prefer one short per-field report, with evidence links available for inspection:

> **Pavement width — present, null.** The requested property exists with a null
> value in source version `{version}`, selection `{selector}`. The null's meaning
> is `{source-defined meaning or unknown}`. Evidence: `{reference}`.

> **Pavement width — property absent.** The native path `{path}` is missing from
> the inspected complete record for `{selector}` in `{version}`. Expected
> presence is `{expected/not_expected/unknown}`, based on `{reference or missing
> evidence}`. Next: check the source definition and native field mapping.

> **Road height — no matching records.** Retrieval completed for `{selector}`;
> the evidenced filtered selection is empty. This result does not say that the
> property is missing from an existing record. Evidence: `{receipt reference}`.

> **Building height — unresolved.** Retrieval stopped after `{reason}` for
> `{selector}`. Remaining pages have not been inspected. Next: resume within the
> documented limits.

> **Building height — access denied.** The request was denied under `{access
> decision reference}`. Data presence remains `{observed state or unknown}`.
> Next: review the entitlement or access decision.

Avoid adding a general coverage warning to every answer. State the requested
scope once and report a limitation when it changes the answer or next action.

## Integration

`assess_availability(spec)` consumes explicit evidence claims. It does not fetch
or inspect feature payloads. A caller must establish the native field mapping,
inspect the record and supply the relevant observation without treating a missing
alias as a missing source property. Observed values are not included in the
availability report.

`from_query_plan(...)` always reports `not_attempted` and unknown data presence.
A planner's `missing_fields` means no admitted candidate route covers the request;
it does not mean the requested data is absent. A selected candidate likewise does
not establish a successful retrieval. Access and expected-presence claims can be
supplied explicitly to this adapter.

`from_ngd_receipt(...)` reads receipt metadata without reading feature payloads.
A complete receipt is accepted as complete only when its selection collection
matches `source.id` and `selector.id` equals the SHA256 of the canonical native
selection, either as the digest or `urn:sha256:{digest}`. Canonical selection JSON
uses sorted keys and compact comma/colon separators. Discarded payloads,
reacquisition state or an unmatched selector result in incomplete retrieval for
this adapter. Transport failures and rate limiting are recorded as failed
retrieval with a transient failure reason; they do not imply denied access.

The current interface is an offline Python API; there is no CLI. Inputs are
bounded to 65,536 serialised bytes, 64 evidence references and a native path of at
most 16 parts. The receipt-path adapter also limits bytes read. These are metadata
budgets, not provider retrieval limits. Credential fields and credential-bearing
URLs are refused.

The optional output contract is
`okf-plus/schemas/data-availability.schema.json`. It checks structure, private
execution flags and several completeness invariants. Hash syntax validation is
separate from verifying receipt bytes and source claims. Synthetic regression
coverage is in `tests/contract/test_okf_plus_availability.py`.
