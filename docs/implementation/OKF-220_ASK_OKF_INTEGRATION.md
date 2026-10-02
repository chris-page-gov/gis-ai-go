# OKF-220: Explorer and Ask OKF context integration

Reviewed on 2 October 2026. Status: additive local producer and pinned-engine
contract tests implemented; hosted publication and installed Ask OKF admission
remain separate.

## Intended result and supported contracts

[`context_projection.py`](../../scripts/okf_plus/context_projection.py) converts
the matching generated `search-index.json` and `okf-bundle.json` into a complete
Explorer `okf-context-corpus.v3`. Every input record has a discovery card, indexed
source text, a complete evidence record and a hash-bound passage. Temporal extent,
update cadence, release catalogues/feeds, rights, provenance and explicit unknowns
remain available from the entire corpus, including records outside the smaller
representative index.

A single `okf-context-index.v1` cannot hold the initial 11,097-record inventory:
the pinned runtime allows at most 10,000 records and 8 MiB. The producer therefore
emits a full corpus v3 plus a representative v1 index. It never labels that
representative index as the full catalogue. `--all-records` explicitly records
the invocation's intent; all input records are always retained in corpus v3.

The schema and runtime baseline is
[`okf-explorer` at `84fb37f11411c04db8c58046827061f741249002`](https://github.com/chris-page-gov/okf-explorer/tree/84fb37f11411c04db8c58046827061f741249002).
The exact required files are retained under
[`okf-plus/vendor/explorer-context`](../../okf-plus/vendor/explorer-context/manifest.json):
five TypeScript engine files, eight JSON Schema files and both upstream licence
notices, totalling 176,059 source bytes. Every file has an upstream path, immutable
source URL, byte length and SHA-256 in the vendor manifest. The producer verifies
the manifest's pinned digest and every file before use. It resolves JSON Schema
references only through an in-memory local registry. Compatibility checks execute
copies of the verified engine files in a temporary directory. A sibling Explorer
checkout, Git access and network access are unnecessary.

The source and hash manifest SHA-256 is
`5f43735afcc49fad7dd20e7f893a9c9011d5a441d131dc77d80e94eaf37a8ea9`.
The upstream code licence is MIT. Both the complete MIT notice and the upstream
code/content licence split are retained unchanged; no upstream corpus, source
index, application or service registry is copied. The projection and validation
reports retain this vendor-manifest digest as well as the upstream revision.

Relevant upstream contracts are the
[producer index](https://github.com/chris-page-gov/okf-explorer/blob/84fb37f11411c04db8c58046827061f741249002/profiles/context-assembly/v1/index.schema.json),
[corpus v3](https://github.com/chris-page-gov/okf-explorer/blob/84fb37f11411c04db8c58046827061f741249002/profiles/context-assembly/v1/corpus-v3.schema.json),
[evidence unit](https://github.com/chris-page-gov/okf-explorer/blob/84fb37f11411c04db8c58046827061f741249002/profiles/context-assembly/v1/evidence-unit.schema.json)
and [corpus assembler](https://github.com/chris-page-gov/okf-explorer/blob/84fb37f11411c04db8c58046827061f741249002/apps/okf-explorer/src/lib/context/corpusV3.ts).

## Artefact contents and exact boundaries

| Artefact | Purpose and verification |
| --- | --- |
| `manifest.json` | Schema-valid full corpus v3 inventory with byte/hash bindings for the base, record/card, search and relationship files. Native input revision/digest are retained in producer extensions. |
| `base-index.json` | Authored `Concept` and `SourceFamily` navigation nodes, when supplied by the input. Each points to its complete metadata record; the producer invents no domain applicability rule. |
| `records/*.json.gz` | Canonically ordered complete evidence records in bounded shards. No evidence text, temporal fact, source object or rights field is truncated. |
| `passages/*.txt` | Complete original Markdown body followed by every semantic front-matter field as canonical JSON. A single UTF-8 span binds the whole normalised metadata passage. |
| `discovery/*.json.gz` | Separate navigation cards, each bound to the complete evidence record digest. Bounded aliases are discovery aids; every original field remains in evidence and source postings. |
| `search/*.json.gz` | All-record source/discovery postings in the upstream 256-bucket format, using unchanged BM25 v1 parameters. This is a compatible context corpus, not a renamed OKF+ search index. |
| `relationships/*.json.gz` | Complete incident entries, counts and ID digests. Only derived navigation from an authored concept/source-family node to its own metadata is asserted. Source-authored assertions remain in complete metadata; they are not silently promoted to evidence requirements. |
| `index.json` | Bounded v1 evaluation index: all authored concepts/source families and the first two canonical IDs per family by default. Every excluded input ID is listed in the projection manifest. |
| `projection-manifest.json` | Input snapshot bindings, exact whole-corpus counts, representative selection/omissions, explicit provenance mapping gaps and output hashes. No evidence record or metadata field is omitted from the full corpus. |
| `descriptor-entrypoints.json` | Concrete candidate `context_assembly` and `context_corpus` references, with bytes/digests and the projection-manifest hash. This is an integration fragment, not a claim that an Explorer descriptor or remote service was changed. |
| `schema-validation.json` | All-record/card/posting/adjacency schema validation, exact upstream schema hashes and transferred input-file hashes. |
| `engine-validation.json` | Optional actual pinned-engine observations for specified questions: context identity, selected IDs, corpus/candidate counts, omissions, evidence status and bounded file use. |

Semantic hashes use UTF-8 canonical JSON with sorted keys and no final newline,
matching the Explorer engine. Transferred files and decoded compressed files have
separate hashes. The projection manifest itself is hash-bound by the entrypoint
fragment, avoiding a self-referential digest.

The record is labelled `normalized` under the upstream contract's exact spelling;
its authority is `derived`. These identifiers are deliberate exceptions to the
repository's British English prose convention. Source-native status and review
metadata remain unchanged inside the complete record. A whole normalised
metadata passage is not a verbatim official publication or a complete statistical
answer.

Original response URLs, digests, locators and capture timestamps are mapped when
present. A source reference without a complete HTTP capture binding remains whole
in the evidence text and is listed as a mapping gap. The producer never invents
an upstream response digest or capture date. The generated passage has its own
explicit capture timestamp and proposed publication URL; this proves local
projection identity, not remote availability. Candidate URLs must be replaced or
accepted through the eventual publication process and then verified live.

## Reproducible local verification

The complete automated sequence is:

```sh
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/verify.py
```

It first checks that current snapshots reproduce the authored Markdown, builds
the current source, evaluates the 40-question corpus, projects every record,
validates every schema record and independently audits the complete passages and
discovery bindings. Finally it runs four real-record checks with the pinned
engine: a tail identifier outside the representative index; cadence, feed and
rights facts; an unsupported observation request; and an unknown question.
The 36 retrieval checks are scored separately from the four context-required
questions, which remain explicitly unassessed. A failed check returns a non-zero
exit status. Python network operations and the engine's fetch path are denied
during this offline sequence.

Outputs remain under `artifacts/okf-plus`: `bundle/`, `context/`,
`retrieval-evaluation.json`, `context-cases.json` and the bounded machine report
`verification.json`. The report binds source revision, input digest, transferred
input bytes, question corpus, vendor manifest and generated artefact digests. A
successful status is `passed-automated-checks`; it does not pass the separate
semantic-review or hosted-admission gates. `--revision` and `--captured-at` can
make the candidate revision and capture timestamp explicit.

Use the repository's locked Python environment (`uv run --locked` or its existing
`.venv`) and the repository's supported Node runtime for the engine checks. A fixed UTC
capture timestamp is an explicit input, so repeated builds from the same inputs
produce identical bytes. Supply the actual timestamp of the projection capture,
not an inferred provider publication date.

```sh
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/context_projection.py \
  --search-index artifacts/okf-plus/bundle/search-index.json \
  --bundle artifacts/okf-plus/bundle/okf-bundle.json \
  --output artifacts/okf-plus/context \
  --publication-base https://chris-page-gov.github.io/gis-ai-go/okf-plus/context/ \
  --captured-at "$OKF_CONTEXT_CAPTURED_AT" \
  --all-records

uv run --locked --cache-dir .uv-cache python -m unittest \
  tests.contract.test_okf_plus_context
```

The producer refuses mismatched record sets, changed snapshot identities,
search/bundle metadata disagreement, oversized whole records and unmarked output
directories. It performs no provider calls. The test suite includes nine checks:
complete metadata/passage identity; input mismatch; oversize rejection;
explicit missing upstream bindings; deterministic output and entrypoint hashes;
safe installation; actual pinned-engine retrieval/refusal; changed vendor-file
rejection; and changed vendor-manifest rejection.

The pinned-engine test uses a 41-record synthetic corpus and retrieves `TAIL999`,
which is outside the representative shortlist. It requires the complete temporal
range, monthly cadence, release feed, unknown next-release label and rights
limitation. It also checks authored navigation, unknown-question insufficiency
and explicit budget omission. Its fetch substitute reads only hash-bound local
files; a real network call throws. The integration test always runs and needs no
environment variable or external checkout. The nine checks passed locally with
Node `26.7.0`; this is local compatibility evidence, not a substitute for the
repository's canonical CI runtime and required assurance.

To verify additional actual-corpus questions, pass `--engine-cases` with a local
JSON array. Each item has `question`, optional `expectedId`, `requiredText`,
`budget`, `expectOmission` and `expectInsufficient`. Expected IDs and required
facts must come from the bound input records. A passing retrieval check does not
upgrade an `insufficient` evidence package to a sufficient answer.

## Hosted Ask OKF dependency

The inspected Ask OKF service admits only its approved DWP bundle and exact
source/engine pairs. See the [reuse review](OKF-220_REUSE_REVIEW.md#explorer-and-ask-okf-integration)
for the pinned service evidence. This producer neither changes that registry nor
adds an executable provider tool.

The next admission work is concrete: publish these hash-bound files, incorporate
the reviewed entrypoint fragment into an accepted Explorer descriptor, register
the new logical bundle and immutable source/engine pair in the separately owned
service, preserve DWP replay behaviour, and verify full structured/text MCP
packages plus the actual installed client. Until then, whole-corpus local engine
compatibility and remote Ask OKF availability remain separate claims.
