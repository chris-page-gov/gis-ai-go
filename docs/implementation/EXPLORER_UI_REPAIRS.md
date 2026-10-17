# Explorer focus and Unicode repairs

This increment follows review findings [UI-01 and UI-02](../architecture/REVIEW_UI.md)
and documentation commit `24106afe`. The owner authorised both behavioural fixes.
Implementation links below follow this document's Git revision; the original
review retains its immutable baseline references.

## Behaviour

Navigation now focuses the rendered view, record, About or not-found heading.
The heading's `tabindex="-1"` permits programmatic focus without adding it to the
normal Tab sequence. [Destination selection](../../apps/public-explorer/src/main.ts#L120)
accounts for non-card views that retain a selected-record identifier, native
About links and malformed/unknown records. Existing search, facet and clear
controls retain focus after rendering. The skip link still focuses the static
main content; history focus uses the saved scroll position without scrolling to
the heading instead.

[Query normalisation](../../apps/public-explorer/src/state.ts#L24), input
`maxlength` and raw URL admission now use the same **200 UTF-16-unit budget**.
Normalisation happens before truncation, and truncation iterates complete code
points so it cannot split a supplementary character's surrogate pair. Oversized
incoming URL queries continue to be rejected; programmatically supplied state is
bounded before it becomes a shareable URL.

The input limit is deliberately unchanged. For example, 101 Deseret letters in
caller-created state become 100 complete letters and survive serialisation and
parsing. A short input whose compatibility characters expand during NFKC
normalisation is also bounded before it is saved. Ten-term and unsafe-control
rules remain in place.

## Verification

- Regression first: the expanded state suite failed four cases on the previous
  normaliser; the Graph navigation focus assertion failed in real Chromium before
  the focus change. These were failures of expected behaviour, not test setup.
- All **51 Vitest tests** and both build-policy Node test files passed.
- The Explorer TypeScript check passed, including the browser tests.
- A fresh OKF build produced 36 records; preparation verified 46 catalogue files,
  the build boundary checked 48 allowed inputs, and distribution checks passed
  for 51 files, CSP, relative asset paths and byte-identical catalogue output.
- Browser verification covers the complete local suite, including accessibility,
  keyboard/record/history/error navigation, control focus, Unicode URL reloads,
  hostile state, downloads and reviewed examples. Final outcome is recorded below.

The regression sources are [state tests](../../apps/public-explorer/test/unit/state.test.ts#L112),
[navigation focus tests](../../apps/public-explorer/test/browser/navigation-focus.spec.ts#L1)
and [browser journeys](../../apps/public-explorer/test/browser/journeys.spec.ts#L295).
The first complete browser run exposed a skip-link regression from newly effective
heading focus. Capturing its native main-content target before URL
canonicalisation corrected it; the existing skip assertion was retained and
extended to navigation after a view change.

Checks used the installed pinned TypeScript, Vitest, Vite and Playwright packages.
Local browser acceptance used system Chromium **151.0.7922.173**, with a temporary
configuration importing the repository's Playwright configuration and changing
only the executable, preview-command path, test-directory path and output path.
The maintained Chrome configuration was unchanged. Additional sandbox network
permission enabled the browser's local sockets and loopback preview; page
assurance continued to reject external requests. No provider calls were made.

GitHub access remains unavailable in this environment, so no remote pull request,
canonical CI result, release or deployment is claimed. Other maintenance findings
remain separate work.

## Final browser outcome

All **45 local browser tests passed** in Chromium (37 seconds), including all
four automated accessibility scans and the navigation, Unicode and stored-scroll
regressions. Repository-local link/research-integrity, changelog and whitespace
checks also passed.
