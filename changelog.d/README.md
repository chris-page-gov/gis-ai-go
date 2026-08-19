# Changelog fragments

Add one concise Markdown bullet for every material pull request. Use:

```text
{issue-or-adr}.{added|changed|deprecated|removed|fixed|security}.md
```

For example, `DISC-102.added.md`. Use the change category that will appear under
`CHANGELOG.md`; do not add headings inside a fragment. Documentation-only typo fixes
need no fragment when they do not change behaviour or an asserted fact.

The release pull request moves fragments into `CHANGELOG.md`, deletes the consumed
files, synchronises every package version and verifies the release artefacts before
tagging.

`VERSION` uses stable `X.Y.Z` Semantic Versioning so the same value remains valid in
both npm and Python project metadata. Use branches and commit identifiers for preview
builds rather than placing prerelease syntax in the product version.
