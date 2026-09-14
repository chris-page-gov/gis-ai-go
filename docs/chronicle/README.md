# How we built GIS AI GO

**Volume 1: from research to a local MCP candidate, under human governance.**

Editorial date: 14 September 2026. Product history is frozen at
`6c76c92a18da779766f8d49acbbd7dbbd31abb97` (PR #115). Later guidance changes and
review findings are dated additions, not claims about what was known earlier.
Work is tracked in [CHRON-213 #117](https://github.com/chris-page-gov/gis-ai-go/issues/117)
and the [Claude retrospective #86](https://github.com/chris-page-gov/gis-ai-go/issues/86).

Subsequent work is recorded in the [WEB-216 source-time journal](WEB-216_JOURNAL.md).
It does not move this volume's product cut-off or claim that ongoing experiments
have completed.

The dated Claude recovery edition replaces the initial twelve-row minimum with
a reviewed 31-outcome chronology, corrects timestamp semantics and separates
recoverable evidence from the still-unprovable exhaustive-history claim. It does
not move the product baseline or disclose private transcripts or granular costs.

GIS AI GO is a case study of model-led software implementation within authority
set by a person. The owner chose the purpose, rights, priorities and acceptable
external commitments. Codex decomposed work, created delegated assignments,
wrote code and tests, investigated failures and prepared changes for protected
integration. Automated controls supplied repeatable checks on those changes.

The record includes delays, corrections and unfinished work. It does not establish
that this is the first autonomous coding project, that every decision was good,
or that a model upgrade caused a measured improvement. Those would require
additional comparative evidence.

## Choose your route

1. Read [the story](NARRATIVE.md) for the chronological account and its limits.
2. Follow [the learning path](LEARNING_PATH.md) to understand the concepts, inspect
   the code and try the local demonstration.
3. Read [agent history](AGENT_HISTORY.md) and [the Claude investigation](CLAUDE_RETROSPECTIVE.md)
   for the evidence behind delegation and repeated attempts.
4. Read [the code-review synthesis](CODE_REVIEW.md), detailed
   [runtime review](reviews/RUNTIME_REVIEW.md) and
   [assurance/UI review](reviews/ASSURANCE_AND_UI_REVIEW.md).
5. Examine [guidance and model transitions](GUIDANCE_REVIEW.md),
   [local completion](LOCAL_COMPLETION_PLAN.md) and the
   [separate improvement stage](IMPROVEMENT_PLAN.md).
6. Use [the evidence method](EVIDENCE_METHOD.md), [public commit ledger](data/commits.csv)
   and [claim index](data/claims.json) to check the account.

## Print and share

The canonical source is this Markdown collection. The build script produces a
self-contained HTML reader, an A4 PDF, source ledger and SHA-256 manifest. Each
diagram uses a short vertical flow or small comparison, at readable print size;
the long agent inventory belongs in a searchable table rather than a 600-node
diagram. Captions and text describe the relationships for readers who cannot see
the figures.

```bash
python scripts/build_chronicle.py --output artifacts/chronicle-html
```

HTML and SVG generation use the Python standard library. PDF generation requires
the separately pinned documentation dependency in `docs/chronicle/requirements-print.txt`:

```bash
uv run --with-requirements docs/chronicle/requirements-print.txt \
  python scripts/build_chronicle.py --output artifacts/chronicle --pdf
```

Use separate output directories for HTML-only and PDF builds. A repeat build
checks its previous manifest and refuses unexpected or changed files; choose a
new empty directory if the output inventory changes. The builder never cleans an
unrelated directory automatically. It needs repository history through the named
baseline; use a full clone rather than a shallow checkout.

Generated artefacts are kept out of product builds. A later public Pages route can
package the reviewed chronicle through the existing publication process. The
reader and PDF are review editions until the source/disclosure check is complete;
private evidence and granular cost data stay local. They contain no private-store
paths or raw conversation export.

The product remains an unreleased local `v0.2.0` candidate. The supported public
release is still `v0.1.0`. This volume closes an account of the local milestone;
public deployment and operational experience belong in a subsequent volume.
