# Threat model and assurance: enforce at every route to data

> **Evidence notation.** Bracketed identifiers such as `[S-MCP-SPEC]` resolve through [`data/sources.json`](../data/sources.json). **Verified fact**, **assumption**, **recommendation** and **unresolved question** are deliberately separated. Retrieval date: **19 August 2026**.


## Method

This is a design-stage data-flow threat model. Likelihood and impact are ordinal working judgements, not measured probabilities. Every threat has preventive, detective, response, residual-risk and test fields in [`data/risks.json`](../data/risks.json).

## Highest-priority paths

1. **Confused deputy:** an agent uses an organisation-owned provider credential beyond the human’s authority.
2. **Policy bypass:** a raw endpoint, widget, map/tile route or cache avoids the PEP.
3. **Cross-tier leakage:** protected data enters an open cache, result or artefact.
4. **Credential misuse/replay:** provider or delegated tokens are stolen or reused.
5. **Prompt/tool poisoning:** provider metadata attempts to redirect agent behaviour.
6. **Provenance/audit spoofing:** results cannot be reconstructed or evidence is altered.
7. **Expensive/malicious spatial input:** geometry, archive or query complexity creates denial of service.
8. **Licence change:** cached or derived data remains available after rights change.

## Threat register

| ID | Threat | Path | Likelihood | Impact | Residual |
| --- | --- | --- | --- | --- | --- |
| RK01 | Prompt injection through metadata | malicious provider record or dataset description | high | high | medium |
| RK02 | Tool poisoning | misleading capability metadata or schema drift | medium | high | low-medium |
| RK03 | Confused deputy | agent uses organisation credential beyond user authority | high | critical | medium |
| RK04 | Agent identity substitution | client claims another agent or host | medium | high | low-medium |
| RK05 | Token theft or replay | bearer token leakage | medium | critical | medium |
| RK06 | Overbroad scopes | one token can call unrelated protected operations | medium | high | medium |
| RK07 | False device posture | client asserts managed/compliant status | high | high | low |
| RK08 | Policy bypass | alternate endpoint/cache/widget skips PEP | medium | critical | medium |
| RK09 | Provider credential misuse | service credential used outside authorised context | medium | critical | medium |
| RK10 | SSRF/arbitrary URL fetch | tool accepts attacker-controlled URL | high | high | low-medium |
| RK11 | Licence/data exfiltration | protected data exported to public destination | medium | critical | medium |
| RK12 | Cross-tenant/tier leakage | cache or query result reused across entitlement contexts | medium | critical | low-medium |
| RK13 | Cache poisoning | malicious or corrupt provider/cache content promoted | medium | high | low |
| RK14 | Stale or revoked entitlement | long job continues after access changes | medium | high | medium |
| RK15 | Malicious geometry | pathological coordinate/geometry causes crash or excessive compute | high | high | low-medium |
| RK16 | Archive/decompression bomb | provider download exhausts storage or memory | medium | high | low |
| RK17 | Expensive-query denial of service | spatial join/export consumes shared resources | high | high | medium |
| RK18 | Map/tile abuse | high-volume requests create cost or expose coverage | medium | medium | low-medium |
| RK19 | Widget/WebMCP origin attack | embedded/origin-confused UI invokes tools | medium | high | medium |
| RK20 | Provenance spoofing | result claims false source/version or receipt | medium | critical | low-medium |
| RK21 | Audit tampering | operator alters or deletes evidence | low-medium | critical | low |
| RK22 | Derived-data inference | open aggregate reveals sensitive protected detail | medium | high | medium |
| RK23 | Supply-chain compromise | dependency/container is malicious | medium | critical | medium |
| RK24 | Model/tool hallucination | agent invents provider result or geometry | high | high | low-medium |
| RK25 | Sensitive query-history exposure | logs reveal locations or investigations | medium | high | medium |
| RK26 | CRS/axis-order error | valid-looking but wrong location/area result | medium | high | low-medium |
| RK27 | Temporal geography mismatch | statistics joined to wrong boundary vintage | high | high | low |
| RK28 | Provider outage | authoritative source unavailable | high | medium | low-medium |
| RK29 | Licence withdrawal/change | previously allowed cache/export becomes invalid | medium | critical | medium |
| RK30 | Operational drift across tiers | open/PSGA/commercial deployments diverge | medium | high | medium |

## Assurance gates

- threat model reviewed before Stage 2 and whenever a provider/tier/action is added;
- automated schema, protocol, policy, licence-obligation and cache-isolation tests;
- malicious metadata/geometry/archive/query fixtures;
- dependency locks, SBOM, SCA, signed images and minimal runtime identities;
- DPIA and data-minimisation review for protected query history;
- accessibility and equality-impact review for map/non-visual journeys;
- ATRS assessment before deployment where the service meets the applicable criteria;
- security architecture review and penetration/red-team tests before PSGA/commercial pilot;
- incident runbooks for emergency deny, registry suspension, credential revocation, Task cancellation, cache quarantine, agent quarantine and evidence freeze. [S-NCSC-CAF] [S-ICO-DPIA] [S-ATRS] [S-WCAG]

## Audit privacy

Audit must be useful without becoming a sensitive shadow dataset. Log stable/pseudonymous actor and resource identifiers, purpose and policy references, source/version, operation parameters or their digest, transformations, outcome and artefact references. Do not log tokens, secrets, provider credentials, unnecessary full geometries, free-text prompt contents or sensitive query payloads when a bounded digest/reference is sufficient. Restrict audit search and apply retention by risk/legal need.

## Verification and challenge

The result receipt schema is [`schemas/evidence-receipt.schema.json`](../schemas/evidence-receipt.schema.json). A challenge workflow reloads the immutable policy version and PIP evidence snapshots, replays the deterministic decision, verifies source/output hashes and records any correction as an append-only event.
