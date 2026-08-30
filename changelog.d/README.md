# Changelog fragments

Add one concise Markdown bullet for every material pull request. Keep it to one
paragraph of no more than 1,024 UTF-8 bytes, end it with exactly one LF and indent
continuation lines by two spaces. Use:

```text
{issue-or-adr}.{added|changed|deprecated|removed|fixed|security}.md
```

For example, `DISC-102.added.md`. Use the change category that will appear under
`CHANGELOG.md`; do not add headings inside a fragment. Documentation-only typo fixes
need no fragment when they do not change behaviour or an asserted fact.

Validate the complete pending set with `pnpm run validate:changelog-fragments`.
`pnpm run preview:v0.2.0` writes a deterministic, ignored preparation artefact to
`artifacts/release/v0.2.0-preview.md`; it does not consume fragments or make a
release claim.

The release pull request moves fragments into `CHANGELOG.md`, deletes the consumed
files, synchronises every package version and verifies the release artefacts before
tagging.

`VERSION` uses stable `X.Y.Z` Semantic Versioning so the same value remains valid in
both npm and Python project metadata. Use branches and commit identifiers for preview
builds rather than placing prerelease syntax in the product version.
