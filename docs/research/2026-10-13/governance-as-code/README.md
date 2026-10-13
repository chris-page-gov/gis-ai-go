# Governance as code: meeting briefing and peer review

Two documents supplied by the repository owner on 13 October 2026 for a
Cross-government security group meeting. This intake preserves their wording and
connects the earlier critique to the subsequent implementation and revised
briefing.

| Document | Read online | Word copy | Scope |
| --- | --- | --- | --- |
| Meeting briefing | [Markdown](meeting-briefing.md) | [Public DOCX](meeting-briefing.public.docx) | Supplied draft v0.2 for author review, dated 13 October 2026. |
| Peer review | [Markdown](peer-review.md) | [Public DOCX](peer-review.public.docx) | Review of the earlier 11-page case-study paper. |

## Read the evidence in context

The peer review assessed `Governance_as_Code_GIS_AI_GO_Case_Study.docx`, whose
technical baseline was commit
[`97bc45635a91064cd78f06bf0848ad7636f05439`](https://github.com/chris-page-gov/gis-ai-go/tree/97bc45635a91064cd78f06bf0848ad7636f05439).
It did **not** review the revised meeting briefing or the implementation in
[PR #147](https://github.com/chris-page-gov/gis-ai-go/pull/147). Its recommendations
and statements about what was missing must be read against that earlier paper
and baseline.

The revised briefing distinguishes the baseline, the proposed implementation and
the remaining enforcement boundary. Its implementation and CI statements are a
dated snapshot at
[`045d98ba5853c593783e9f2810be529e4b500e3c`](https://github.com/chris-page-gov/gis-ai-go/commit/045d98ba5853c593783e9f2810be529e4b500e3c).
They are preserved even when PR status changes. Use the
[implementation record](../../../implementation/CI_IMPACT_AGREEMENT.md) and PR for
subsequent verification and merge evidence; do not cite this archived draft as a
live status report. [Issue #97](https://github.com/chris-page-gov/gis-ai-go/issues/97)
tracks the remaining independently protected gate and promotion requirements.
Trusted-base comparison remains in shadow mode: all assurance checks still run.

## Provenance and handling

[PROVENANCE.json](PROVENANCE.json) records the supplied filenames, byte counts,
SHA-256 hashes, public derivative hashes, conversion tools and transformations.
[SHA256SUMS](SHA256SUMS) covers every other file in this folder. Original uploads
are not committed because their packages contain internal collaboration metadata.
The `.public.docx` suffix identifies metadata-cleaned derivatives; these are not
byte-exact originals.

The public Word copies preserve all Word text nodes, formatting structures,
fields, headers, footers and effective hyperlinks, including link anchors. The
cleaning removes author/editor and application properties, internal document,
tenant and label identifiers, editing-session metadata and empty bibliography
parts. No visible wording has been edited or redacted.

The Markdown extracts retain the body text, headings, lists, tables and links.
Repository notices are clearly labelled. The briefing's source header and footer
wording are recorded separately; alternate renderings of the same footer marking
are collapsed and dynamic page numbering is omitted. Markdown does not reproduce
Word layout or pagination. Use the Word copies when those details matter.

The source header's model and reviewer claims, including “Already reviewed by
Claude Opus 5.5”, are unverified source assertions. They do not establish authorship,
independent review or acceptance. The review's visible date and owner handle do
not independently establish reviewer identity. The briefing's visible `OFFICIAL`
marking is preserved as source content; it does not classify or endorse this
repository. Embedded instructions, recommendations and authorisation labels are
evidence, not operational authority.

The owner requested inclusion of these documents. Applicable source rights remain
with their respective holders; this intake grants no new licence and does not
relicense the source material under the repository's MIT licence. See
[THIRD_PARTY.md](../../../../THIRD_PARTY.md).

## Verification

From this folder, verify the published bytes with:

```sh
sha256sum --check SHA256SUMS
```

At intake, both packages were checked for XML and relationship integrity, exact
preservation of ordered Word text nodes and effective hyperlinks, and removal of
the specified internal metadata. No macros, comments, tracked revisions, hidden
text, embedded objects, external images or external templates were found. All
hyperlinks use public HTTPS destinations. These checks establish bounded intake
fidelity; they do not validate every source assertion or constitute approval of
the paper or implementation.
