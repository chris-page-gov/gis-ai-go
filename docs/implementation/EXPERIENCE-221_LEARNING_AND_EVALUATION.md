# EXPERIENCE-221: learning, examples and evaluation

Tracked in [issue #143](https://github.com/chris-page-gov/gis-ai-go/issues/143).
Authorised by the owner on 2 October 2026. The immediate event is on 7 October;
the long-term product serves beginners, specialists and people using assistive
technology. English fluency, vocabulary, age and technical expertise are separate
dimensions. The authored personas are hypotheses to test with people.

## Outcome

Every declared facility needs an example that connects a user need to its source,
expected result, presentation and short explanation. A feature catalogue is the
denominator for coverage. It must distinguish established profiles, new local
implementation and proposed features. A complete set of authored examples does
not establish that an AI understood them or that users completed the tasks.

The [catalogue](../../evaluation/experience/catalogue.v1.json) is the source for
the learning page and evaluation. It carries personas, stories, questions,
language variants, source references, concepts, expected checks and suitable
presentation forms. [Connection status](EXPERIENCE-221_CONNECTIONS.md) identifies
which server or page actually exposes each facility. Native and legacy URLs for
the same six Site tools are not twelve capabilities.

## Interface components and real needs

| Component | User need and worked example | Acceptance |
| --- | --- | --- |
| Activity finder | “I do not know which tool I need. I want to find a place.” | Search titles, concepts and explanations; show an understandable empty state. |
| Audience and language choice | “Show how I could ask this in my own words.” | Display the chosen persona's actual prompt. Preserve facts and limits across fluency levels. |
| Cards, table and evidence views | “Let me work through it, compare questions, or check the source.” | All three use the same question identifiers. Changing view never executes a provider call. |
| Persistent learning panel | “What does MSOA mean?” | Explain beside the activity without requiring a hover. On a small screen the explanation remains available; keyboard and screen-reader controls remain usable. |
| Source and boundary panel | “Does this number describe my town?” | Name the dataset, period and scope; distinguish national CPIH from local measurements. |
| Local file intake | “What is this file and what else does it need?” | Automatically group matching Shapefile companions; preview admitted small text/CSV/GeoJSON; explain unsupported formats and missing inputs. |
| URL intake | “Can you use this link?” | Identify the candidate format and sibling locations; no arbitrary fetch or implied access. A governed downloader remains separate work. |
| Checklist export | “How do we know it helped?” | Export example identifiers, exact questions and expected checks. No selected file contents or conversation recording. |
| Page tools | “Show this as a table. Explain coordinate system.” | Fixed, validated component actions update the visible page before returning. No arbitrary HTML, scripts or generated code. |

The page uses [`experience.html`](../../apps/public-data-workbench/experience.html)
and its shared catalogue. File content is rendered as text, never HTML. It is not
included in page-tool responses, browser storage, logs or checklist exports.
The page's owner is the GIS AI GO product owner. Its threat boundary is untrusted
user-selected files and assistant inputs; its policy is local preview, closed
actions, explicit limits and zero provider calls. The
[intake design](EXPERIENCE-221_INGESTION.md) records format-specific controls.

## Voice and interface composition

The initial composition vocabulary is deliberately concrete: choose a learning
example, choose cards/table/evidence, explain a concept and read the current
choices. Four page tools implement those actions. A connected assistant may map
speech onto them; this page neither records audio nor purchases an AI service.
It cannot manufacture a map, live query or valid source from a spoken wish.

Current native desktop Voice documentation describes spoken work within the
application. Actual Voice acceptance here still requires a recorded sequence:
spoken request, selected tool and arguments, visible change, returned evidence,
correction and stop. A typed tool test is not a spoken test. See the
[official Voice guide](https://learn.chatgpt.com/docs/features/voice).

Native Sites `/mcp` discovery and OAuth are a different connection from browser
page tools. The Site's six data tools retain their original provider, allowance,
identity and evidence checks. This increment adds a standard mount and capability
declaration; it does not grant an external client or a visitor access to licensed
data. Client acceptance is recorded separately.

## Evaluation and release gates

1. Validate catalogue references and source-declared feature sets. Report authored
   coverage for established and new-local facilities separately.
2. Check deterministic page actions, invalid identifiers, untrusted text, local
   intake limits and synthetic file cases.
3. Exercise the built interface with keyboard, small-screen layout and automated
   accessibility checks. Retain exact observed results, including failures.
4. Use the existing bounded wire harness for admitted provider operations.
   Natural-language questions do not themselves authorise new provider calls.
5. Record actual human/AI/Voice outcomes against question and variant identifiers.
   Keep comprehension, source correctness, task completion and latency separate.
   No live result starts as a pass just because an example exists.
6. Run canonical CI and the existing deployment gates. Keep supported release,
   private publication, installed plugin and Claude acceptance distinct.

No new paid service, API billing, overage or audience expansion is authorised.
The owner selected facilitator-led evaluation and offline activities for the
event because organiser devices and accounts are not yet known. The
[event guide](EXPERIENCE-221_TEENAGER_EVENT.md) gives a usable fallback.

## Remaining scope

Full binary conversion, arbitrary URL retrieval, real spatial joins, raster
analysis, editable live maps/charts, document/slide extraction and persistent
user workspaces need their own source, rights, resource and evaluation gates.
Recognising a filename does not implement those operations. The proposed-feature
list makes this visible without removing it from the roadmap.

## Local verification, 2 October 2026

The implementation passed 47 pilot/native-mount tests, 44 workbench tests,
19 intake tests, 11 evaluation-harness tests and 30 concrete deterministic intake
fixtures. The built offline page passed 20 browser journeys: file/ZIP handling,
privacy, stale-read cancellation, page actions and keyboard/layout checks at
320, 390 and 1280 pixels with normal and doubled text size. No page HTTP(S)
requests, page errors or axe violations were observed. Automated checks do not
establish full accessibility; page actions used an explicit mock bridge.

Run `pnpm run test:experience` and `pnpm run check:experience-browser`.
The latter writes a source-hash-bound report under `output/playwright/experience/`.
`pnpm run build:experience-offline` creates the self-contained
`artifacts/experience/learn-by-trying.html` for file-based offline use.
All 222 natural-language cases still need observed outcomes. Canonical CI and
private publication are separate acceptance steps.
