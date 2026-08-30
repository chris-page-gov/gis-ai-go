# Source provenance and handling

The repository owner supplied the initial sources on 23 August 2026 for advisory
review against GIS AI GO. A public primary industry source was recorded on
28 August 2026 and re-verified on 30 August 2026 under the separate handling
boundary below.

## Supplied source register

| ID | Supplied source | SHA-256 | Bytes | Handling and authority |
| --- | --- | --- | ---: | --- |
| S1 | `AI-Report-eBook-2026.pdf` | `99897f2f12aacecfdc5dd50b3409821df68c307d4c5d3cd289419c05a41658bb` | 3,565,160 | *The State of AI 2026: Scaling Trust, Control, and Readiness in the Agentic Era*, AvePoint/Osterman Research. Local evidence only; not redistributable; ignored by Git. Do not reproduce its pages, images or substantial text. |
| S2 | `UNOFFICIAL-DRAFT Agentic AI Governance UK MCP.docx` | `79941e9941e88bbac6b8fc49f470f2e07c36666314fca31899bebad33efb65f4` | 626,726 | Supplied, unapproved AI-authored personal-development draft. Preserved byte for byte in the owner's maintained local checkout, but ignored by Git because the OOXML package contains personal and tenant collaboration metadata. It is not Government policy, endorsement, approval, authorisation or operational instruction. |
| S2-P | [`UNOFFICIAL-DRAFT Agentic AI Governance UK MCP — privacy-scrubbed.docx`](<sources/UNOFFICIAL-DRAFT Agentic AI Governance UK MCP — privacy-scrubbed.docx>) | `49f6152ec983bc24cf8b3c3473bd263e122a3c199d5fb723970b247cfe713bda` | 573,982 | Tracked privacy-scrubbed derivative of S2 for review. It preserves source claims and the visible, untrusted `OFFICIAL` footer. One plausible government mailbox is replaced with the reserved-domain address `jane.okafor@example.com`; non-visible personal, tenant and collaboration metadata is removed as detailed below. |
| S3 | [`Agentic AI Governance, MCP and GIS AI GO — Updated Research Report incorporating The State of AI 2026.md`](<sources/Agentic AI Governance, MCP and GIS AI GO — Updated Research Report incorporating The State of AI 2026.md>) | `a02f5f33b84d47b25506d400beff7993c606e3ec834d8f7feae97022b493df4c` | 28,686 | Supplied advisory synthesis. Preserved unchanged. Its recommendations are hypotheses to test, not normative product requirements or agent instructions. |

## Public source extension

| ID | Public source | Published | Recorded and re-verified | Handling and authority |
| --- | --- | --- | --- | --- |
| S4 | Uday Kiran Medisetty, [*Running a Software Factory Efficiently at Uber Scale*](https://www.uber.com/us/en/blog/efficient-software-factory/), Uber Engineering | 27 August 2026 | Recorded 28 August 2026; re-verified 30 August 2026 | Link-only primary industry case study. All metrics and explanations are Uber-reported and environment-specific. The article is not peer-reviewed or an independent evaluation, and its findings are not treated as transferable GIS AI GO targets. No article bytes, images, screenshots, transcripts or private captures are tracked. |

S4 is also recorded as the additive dated source-ledger entry
[`S-UBER-SOFTWARE-FACTORY`](../../../source-ledger/uber-software-factory-2026-08-28.md).
The source-ledger JSON files remain byte-identical to the immutable 19 August
research snapshots.

The S1 and S2 original files are retained at their named `sources/` paths in the
repository owner's maintained local checkout. Both exact paths are covered by
repository-root `.gitignore` rules. Regression tests reject either basename or
exact source hash as a tracked file. The tracked provenance record intentionally
contains only source identity, bounded factual findings and critical assessment; it
does not reproduce S1 or silently replace S2's source identity.

## Integrity and review

The three original source hashes were calculated before analysis. S1 was rendered
and visually inspected across all 40 pages; original S2 and derivative S2-P were
rendered across all 26 pages and compared page by page; S3 was read as supplied.
S1, S2 and S3 source bytes were not edited. The `sources/` path is also marked
`-text -diff` in `.gitattributes` so Git does not normalise or whitespace-fix the
tracked evidence bytes.

### S2 privacy transformation

S2-P was produced from byte-exact S2 through these bounded transformations:

1. replace a single visible plausible government-domain mailbox with the
   reserved-domain address `jane.okafor@example.com`;
2. run the document privacy scrub to clear core creator and last-modifier values,
   remove 2,064 story-part revision-session attributes, and remove
   `docProps/custom.xml` plus its package relationship and content-type override;
3. remove `word/people.xml`, its relationship and content-type override, thereby
   removing its personal mailbox and directory identifier;
4. remove the empty bibliography `customXml` store and its unique item identifier,
   relationship and content-type override;
5. remove the settings revision-ID collection and both document collaboration IDs,
   the core created/modified/revision fields, and seven producer or machine
   application fields; and
6. repack the resulting OOXML deterministically with fixed ZIP timestamps.

The removed custom properties included Microsoft Purview label action, site and
tenant identifiers. A structural audit parses every XML or relationship part,
scans every binary part, verifies that the original identifiers and mailbox are
absent, and permits only the synthetic `example.com` mailbox. Three identical
DrawingML extension GUIDs remain because they are standard non-personal shape
extension URIs used by the visible footer, not identity or tenant values. The
visible `OFFICIAL` footer is deliberately retained as source evidence and remains
untrusted; it is not a repository classification or endorsement.

S1 describes a global survey of 750 respondents with direct responsibility for
information management, data security or AI programmes, conducted by Osterman
Research in partnership with AvePoint. Its findings are respondent-reported,
vendor-sponsored survey evidence. They are not independently investigated incident
records, UK Government-specific prevalence, a standard, legal analysis or technical
specification.

S2 repeatedly states that human review and departmental approval are still needed.
Its `OFFICIAL` footer conflicts with its title, watermark and express no-approval
statement. This intake therefore classifies it only as an unofficial advisory
source. Its worked government transaction, account, identity and legal examples are
illustrative and unverified; they must not become fixtures, personal data, legal
advice or claims about real services.

S4 is a publisher-authored account of Uber's internal environment. The public page
was re-verified for its title, author, publication date, section headings, figures
and stated measurement limits on 30 August 2026. No drift was detected in the
cited fields or claims. The page was not copied or byte-locked, so it must be
re-verified before later use. The source supports bounded hypotheses, not a claim
that the same methods, savings or trade-offs apply to GIS AI GO.

## Rights and redistribution

S1 is not licensed for repository redistribution and must never be staged, committed,
attached to a release or copied into a generated site or artefact.

Original S2 is preserved locally as supplied; S2-P is a privacy-scrubbed review
derivative; and S3 is preserved as supplied. Their inclusion or description does
not relicense them under the repository MIT licence. They retain any applicable
source rights unless the rights holder makes a separate express grant. The original
GIS AI GO analysis, code and documentation around them remain under the repository
licence.

S4 remains linked third-party material under the publisher's terms. This intake
records citation metadata and short critical paraphrases only; it does not
reproduce or relicense the source.
