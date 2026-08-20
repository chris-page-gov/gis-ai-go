# OKF publication

The live GIS AI GO publication is generated from reviewed inputs under `source/`, the
explicit profile under `profile/` and digest-locked third-party evidence under
`vendor/`. The immutable research OKF remains evidence under `docs/research/` and is
never rewritten as live product state.

Build the candidate into ignored `artifacts/okf/`:

```bash
pnpm run build:okf
```

The build verifies every locked input and the exact vendored-file inventory,
allowlists three reviewed HMLR metadata records, requires record-level authority,
public-data classification, access, separate record/resource rights, freshness and
source envelopes, and emits Markdown, JSON, JSON-LD, checksums and a deterministic
receipt. It contains no provider distributions, property rows, addresses,
transactions or geometry.

The source lock records why the unresolved abbreviated HMLR research reference is
superseded by the approved immutable `okf-LandRegistry` `v0.3.0` release. Imported
terms and attribution are documented in [`THIRD_PARTY.md`](../THIRD_PARTY.md).

The `v0.1.0` product supports this exact 36-record publication in the GIS AI GO
Explorer. The project-local publication and profile statuses remain candidates:
product support does not assert that the OKF profile is a final external standard or
that every described source is open or operationally supported.
