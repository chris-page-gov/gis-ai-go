# Reusable OKF+ learning paths

The authored [learning-path records](../../okf-plus/records/learning-path/)
describe three independent practice routes: pavement width, building heights
and road elevation. Each remains below 16 KiB. Definitions and source-native
field descriptions stay in their existing concept, collection and documentation
records. The learning sequence links those identities without creating semantic
relationships between OS features.

## Source contract and ownership

`details.learningPath` uses the optional project
[`gis-ai-go.okf-plus-learning-path.v1` schema](../../okf-plus/schemas/learning-path.schema.json).
It records a stable path ID, title, objectives, path prerequisites, prerequisite
concepts and ordered practice steps. Every step identifies one retained record,
an observable outcome, a practice prompt, estimated minutes, concept references
and source references. Array order is the authored sequence. Source references
retain the target record's exact URL; they are not a new capture or a claim that
the current live source was checked.

The repository owner owns this authored contract. Its threats include unsafe
source links, unresolved identities, oversized navigation, accidental assessment
claims and promoting a learning link into a data relationship. The schema bounds
the shape and text. Focused checks resolve all record and concept links, bind
sources to their target records, check local Markdown links and reject malformed
navigation. Metadata grants no data-execution authority.

These paths have no path-level prerequisite: learners can start with any of the
three questions. `prerequisiteConcepts` explains the knowledge useful before a
path. It neither locks browsing nor records competence. All records remain
project-authored and have no human learning-outcome acceptance.

## Existing Explorer presentation

The existing Explorer already provides a large-bundle learning Reader with
`okf-large-learning-presentation.v1`. The producer maps each stable `recordId` to
its actual local Reader route and projects title, outcome, practice and minutes
into that presentation. It must verify every route against the generated corpus
and preserve the small source records as the authority. It must not generate a
curriculum from search ranking or encode source definitions in UI code.

The source contract carries unassessed path prerequisites and concept/source
references independently of any application. Explorer's assessed v2 programmes
remain a separate facility; these records declare no programme, assessor or
competency award. Practice ticks are neither assessment nor certification.

## Evidence boundaries

Pavement practice distinguishes Road Link v5 attribution from Pavement Link v1
and preserves their geometry limits. Building practice checks absolute and
relative height meanings, datum, quality and product-specific chimney rules.
Road practice distinguishes gain from absolute elevation, and checks 3D
geometry, response CRS, ODN height, heighting methods and inferred terrain.
Retained metadata, current technical availability, complete selected retrieval
and whole-area coverage remain different evidence claims.

Run the focused source checks with:

```sh
uv run --locked --cache-dir .uv-cache python -m unittest tests.contract.test_okf_plus_learning_paths
```

The normal OKF+ builder includes these Markdown records in the full bundle.
Browser loading, source navigation, keyboard behaviour and learning
comprehension remain separate checks in the consuming application.
