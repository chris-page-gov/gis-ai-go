# Evaluation: prove the boundary, not only the happy path

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## Evaluation contract

Each release must test factual correctness, tool selection, policy compliance, licence compliance, provenance completeness, reproducibility, latency, cache behaviour, cost, accessibility, client interoperability and graceful degradation. A model answer without a tool/source receipt is not a pass for a data-backed scenario.

## Scenario suite

| ID | Scenario | Expected evidence |
| --- | --- | --- |
| E01 | Anonymous discovery of open boundaries and statistics | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E02 | Anonymous AI uses the public site without scraping | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E03 | Current and historic geographies containing a coordinate | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E04 | PSGA user on compliant managed device requests protected OS detail | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E05 | Same user on unmanaged device is denied or downgraded | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E06 | Named-user delegated agent uses a short-lived transaction permit | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E07 | Approved service workload refreshes a cache | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E08 | Commercial user receives only contract entitlement | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E09 | HMLR, ONS and LandIS open query with full provenance | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E10 | Protected OS enrichment does not leak to public cache | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E11 | Provider outage uses approved cache with freshness warning | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E12 | Licence/policy change invalidates cache and capability | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E13 | Host without Apps receives complete non-visual result | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E14 | WebMCP-capable browser agent uses safe page tools | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E15 | WebMCP-incapable agent follows linked OKF/API | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E16 | High-volume export triggers approval or denial | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E17 | Malicious record attempts prompt injection | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E18 | Client claims false role or posture | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E19 | Policy decision is challenged and reconstructed | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E20 | Emergency tool/provider suspension | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E21 | Malformed geometry and decompression bomb are rejected | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E22 | CRS and axis-order round-trip | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E23 | Temporal geography mismatch is detected | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E24 | Cross-tier cache key contamination test | Policy/licence outcome, deterministic result or safe denial, and complete receipt |
| E25 | Accessibility and keyboard-only public journey | Policy/licence outcome, deterministic result or safe denial, and complete receipt |

## Test layers

1. **Schema and property tests:** authority context, policy decisions, receipts, provider/tool/workflow profiles, geometry limits and cursor determinism.
2. **Provider adapter contract tests:** frozen public fixtures, source-native errors, retries, rate limits and licence metadata.
3. **Policy tests:** open/PSGA/commercial personas, device posture, purpose, fields, resolution, exports, cache and emergency deny.
4. **Protocol tests:** MCP 2026-07-28 conformance, stateless requests, discover/list ordering, cache hints, Tasks/MRTR and host interoperability.
5. **Browser/accessibility tests:** ordinary browser, screen reader/keyboard, responsive layout, WebMCP supported/unsupported and no-JavaScript fallback.
6. **Security tests:** prompt injection, false claims, SSRF, malicious geometry/archive, cross-tier cache, replay and provenance tampering.
7. **Operational tests:** provider outage, stale cache, licence withdrawal, cancellation, rollback, evidence freeze and disaster recovery.

## Gold evidence

Fixtures must record provider/source version, retrieval date, checksum, licence and expected transformation. Protected scenarios use synthetic data and test identities unless the organisation explicitly authorises a controlled test environment. No licensed dataset contents belong in this public suite.

## Release thresholds

- 100% pass for policy deny/obligation, cross-tier isolation, receipt integrity and secret scanning;
- 100% pass for required accessible keyboard journeys;
- 100% deterministic repeatability for frozen fixtures;
- explicit measured thresholds for latency, cost and provider quota before pilot;
- no unexplained host/client variance;
- all failed or waived cases linked to an owner, risk and expiry.

The detailed machine-readable suite is [`data/evaluation-cases.json`](../data/evaluation-cases.json).
