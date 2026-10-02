# OKF-220: retained ONS specification coverage

Reviewed: 2 October 2026. The initial check used retained local evidence only.
The existing export authority covered one bounded request to recover the exact
pinned dataset specification. That request succeeded and matched the recorded digest.
Original files remain in the ignored private specification hand-off; this
document records their structural coverage and the unresolved gaps.

| API family | Exact existing evidence | Export status |
| --- | --- | --- |
| Search and releases | Official `ONSdigital/dp-search-api`, commit `f634c78cc362654ddb464c4559d37202ba0034a9`, `swagger.yaml`. | Exact 19,054-byte file recovered and hash-verified against its successful capture receipt. |
| Dataset API | Official `ONSdigital/dp-dataset-api`, commit `ffe4c71027d7dd88484a408f0b19a823f312dfe6`, `swagger.yaml`. | Exact 109,486-byte file recovered by one authorised request and verified against the previously recorded digest. |
| Code-list API | [Official API documentation](https://developer.ons.gov.uk/code-list/) and a retained documentation response establish listing and child-route documentation. | No exact repository/path/commit for a machine specification is established in the retained evidence. No guessed specification is included. |
| Census population API | [Official API documentation](https://developer.ons.gov.uk/population-types/) and the retained population-list probe. | No pinned machine specification is retained. The population response is catalogue metadata, not an OpenAPI specification. |

The [search specification](https://github.com/ONSdigital/dp-search-api/blob/f634c78cc362654ddb464c4559d37202ba0034a9/swagger.yaml)
has SHA-256
`8b897c35a7c7d98cfef5faa158c8a12d04acebabf69b6eee849f1aaf70b95029`.
Its retained receipt records a successful fetch on 2 October 2026 at
07:31:15 UTC. The file declares Swagger 2.0, service version `1.0.0` and base
path `/v1`. Lexical inspection finds four paths, five operations and eleven
named definitions:

| Path | Declared operations |
| --- | --- |
| `/health` | GET |
| `/search` | GET, POST |
| `/search/releases` | GET |
| `/search/uris` | POST |

These are declared contract operations, not an allowlist for invocation. The
source declares an HTTP scheme; the metadata capturer continues to require
HTTPS. The file's own licence metadata names the Open Government Licence v3.0;
that declaration is retained with the original rather than replaced with a
blanket GIS licence assertion. No full YAML/OpenAPI validator was run in this
bounded preservation step, and the pin does not prove the deployed API runs
the same revision.

The recovered [dataset specification](https://github.com/ONSdigital/dp-dataset-api/blob/ffe4c71027d7dd88484a408f0b19a823f312dfe6/swagger.yaml)
has verified SHA-256
`269ed359fb2713734f450585027cae102585a6995559686cfe7404829a7d1f5a`.
The separate successful receipt records 2 October 2026 at 08:28:53 UTC, one
request, a 30-second wall deadline, a 16 MiB response ceiling, no redirects and
no retries. Its recorded elapsed time was 0.281349 seconds. This recovery did
not change the shared provider capture ledger.

The dataset file declares Swagger 2.0, service version `1.0.0`, base path
`/v1` and HTTPS. Lexical inspection finds 22 paths, 35 operations and 54 named
definitions: 15 GET, seven POST, nine PUT, two DELETE and two PATCH operations.
Private publication/ingestion and observation routes remain documentation
only; their presence does not authorise calls. Its declared licence is the
Open Government Licence v3.0. As for the search file, full OpenAPI conformance
and equality with the deployed service have not been established here.

The original missing-byte gap for this exact dataset specification is now
closed. The remaining machine-specification gaps are the code-list and Census
population APIs: official documentation and catalogue responses are available,
but no exact pinned specification file is retained for either. Those facts
must not be described as complete ONS Swagger coverage.

The private retained-originals manifest preserves the successful source URL,
receipt time, source commit, path, exact bytes/hash and upstream licence
declaration. The ordinary public metadata archive excludes these original
responses. A separate private archive can contain only admitted, hash-verified
documentation and specification originals; catalogue, observation and feature
responses remain outside that archive.

After the completed OS documentation capture and dataset-specification recovery,
the read-only private-export preflight passed for **637 distinct original
source URLs and 7,431,357 bytes**: 152 OS API Markdown pages, 478 NGD Markdown
pages, two selected download guides, three navigation indexes and the two ONS
Swagger files. These are verified inputs to the private export, not an already
created archive. They do not include all 1,673 pages referenced by the OS
Downloads navigation index. The final public metadata export and private
original archive must still be generated and independently checksum-checked
after the final build/verification sequence.
