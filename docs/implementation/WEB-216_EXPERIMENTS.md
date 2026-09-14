# WEB-216: dataset foundation experiments

Protocol recorded on 14 September 2026, before running the new benchmark.
This is a development experiment, not a confirmatory evaluation or an optimality
claim. The [work package](WEB-216_PUBLIC_DATA_WORKBENCH.md) remains authoritative
for the later provider, geography, host and user-research gates.

## Question and source boundary

Can a small, pinned metadata view support useful discovery without transferring
all rich records into every browser or AI context? Can unchanged projections be
reused without leaving stale entries after additions, changes or deletions?

Use committed `okf-ons` revision
`4aa41c71dd570ceccb661768af95c4d69f49162b`, snapshot
`metadata-enrichment-2026-07-21-r6`. Import exact source records, not a build of
the currently modified upstream checkout. The competition repository is not used
as an execution environment or changed.

The starter has five ONS Data API records and two Nomis definitions. The comparison
has all 337 ONS Data API records in that snapshot and those same two Nomis records:
339 metadata records, **not all ONS datasets**, all Nomis data or current live data.
There are no observations, geometries, ELS records or OS payloads in this corpus.
The [source manifest](../../tests/fixtures/web216/source-manifest.json) pins
the source objects and the derivative scope separately. Source-wide acquisition
receipts do not prove an individual record's retrieval time.

Source: Office for National Statistics. The metadata is reused on the basis of
the published [ONS terms](https://www.ons.gov.uk/help/terms-conditions) and
[Nomis copyright conditions](https://www.nomisweb.co.uk/home/copyright.asp), checked
on 14 September 2026. These permit Crown material reuse under the Open Government
Licence subject to exceptions; they do not grant blanket rights over third-party,
restricted, postcode or map material. Metadata discovery never grants access to
observations. The repository's MIT code licence does not replace source terms.

## Predeclared comparison

| Experiment | Arms and measurements | Limit |
| --- | --- | --- |
| X01, layout | Seven-record rich subset; 339-record rich catalogue; the same 339 summaries with lazy exact-record details. Count canonical UTF-8 JSON bytes, logical hashes, build timings and first-result detail bytes. | Byte arithmetic is not browser, compression or network measurement. The subset has less coverage. |
| X02, retrieval | Keyword plus source facet; the same baseline with author-supplied concept hints and explicit, versioned native-dimension edges. Record top five, first relevant rank, recall at five, one out-of-subset coverage case and a no-match control. | Five public development cases, four with relevance labels; not automatic intent understanding, held out, subject-expert validated, or a semantic abstention or clarification test. |
| X06, refresh | No-op and synthetic add/change/delete schedules; compare complete logical output with a fresh full build, including search postings and concepts. | Process-local projection reuse only; no durable cache, atomic production publication, parallel build or provider refresh claim. |

The curated vocabulary maps native `C_AGE`, `GENDER`, `GEOGRAPHY`, `ltla` and
`occupancy_rating_rooms_6a` to explicit concepts. Each edge records its native
dimension and engineering-mapping status. It is not an equivalence assertion or
a learned semantic model. In particular, a `ltla` dimension is not evidence that
two releases share a boundary vintage or that a dataset covers the whole UK.

The search input is restricted to title, description and keywords. Concept edges
come from the explicit dimension vocabulary. Evaluation aliases, gold answers,
arbitrary annotations and standalone instruction fields are excluded from indexing.
Instruction-like text inside permitted metadata fields remains searchable data,
never executable instructions. Source metadata remains untrusted even when its
bytes are hash-verified. This lexical harness does not test a model's susceptibility
to prompt injection.

The upstream ONS-Q001, ONS-Q003 and ONS-Q012 questions informed the development
cases. Expected identities are passed only to scoring, after ranking. Both the
questions and concept vocabulary are visible to the developer; no result can be
called independent or blinded. A later confirmatory evaluation requires the
separate preregistered, subject-reviewed corpus in the work package.
The additional weekly-deaths case is derived from a known source title and is
deliberately absent from the seven-record subset. It checks that a coverage
difference is observable, not how often real users need the larger catalogue.

## Reproduce

The seven-record test fixture is versioned, so a clone does not need another
repository or any API key for the tests:

```bash
python3 -m unittest tests.test_web216_corpus tests.test_web216_experiments
python3 scripts/web216_experiments.py \
  --output artifacts/web216/story-experiment.json
```

For the comparison, provide a read-only local clone containing the exact upstream
commit. No upstream code is run and no network requests are made by these commands:

```bash
python3 scripts/web216_corpus.py --source-repo ../okf-ons \
  --scope comparison --output artifacts/web216/comparison-corpus.json
python3 scripts/web216_experiments.py \
  --corpus artifacts/web216/comparison-corpus.json \
  --output artifacts/web216/comparison-experiment.json --repeats 5
```

Output paths must be new; an earlier result is never silently overwritten.
Keep the command, exact code commit, source and configuration hashes, start time,
duration, environment, output and outcome together. Repeat measurements vary;
logical hashes and byte counts must not. A provider charge of zero describes this
offline command only. Agent token cost is unknown unless separately measured.

## What this increment cannot establish

This does not implement general ONS/Census/Nomis retrieval, a production OKF
index, a geography join, browser WebMCP registration, AI-client interoperability
or a Sites deployment. X03, X04 and X05 need separate source and execution
experiments. Existing two-tool WebMCP and fixed provider operation contracts
remain unchanged. A metadata match must never be displayed as a retrieved value.

Recorded outcomes and engineering decisions follow in the
[WEB-216 development journal](../chronicle/WEB-216_JOURNAL.md).
