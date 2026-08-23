# External incident evidence and negative-assurance crosswalk

Reviewed on 23 August 2026.

This is the supported assurance change arising from source S1. It maps the incident
categories reported on page 30 of the AvePoint/Osterman report to the existing GIS
AI GO threat register and implementation evidence. It neither changes risk ratings
nor treats respondent reports as measured incident prevalence.

## Evidence qualification

Page 30 presents these as percentages of respondents for each breach type and labels
the chart as covering respondents who experienced one or more breaches, but it does
not state a separate category denominator. This crosswalk reproduces the reported
values without recalculating or inferring that denominator. The survey is vendor
sponsored, global and not specific to UK Government. The categories are therefore
an external challenge set for coverage analysis, not acceptance evidence that a GIS
AI GO control works.

| Respondent-reported category | Reported proportion | Existing risks | Current evidence and boundary |
| --- | ---: | --- | --- |
| Sensitive or confidential data exposed or retained | 50.1% | RK11 licence/data exfiltration; RK12 cross-tier leakage; RK25 sensitive query-history exposure | Public v0.2 contracts are open, read-only and fixed-schema; receipts retain commitments rather than query/result material; container assurance scans logs and artefacts for sensitive sentinels. Protected-tier isolation, production logging and backup evidence remain absent. |
| Malicious or untrusted input manipulation | 49.6% | RK01 prompt injection; RK10 arbitrary fetch; RK15 malicious geometry; RK16 decompression bomb | Provider content is treated as data, inputs are schema and byte bounded, the ONS adapter has fixed egress, and adversarial local tests cover hostile metadata, URLs, payloads and compression. No claim is made for an unrestricted model/tool environment. |
| Autonomous unauthorised action | 34.1% | RK03 confused deputy; RK08 policy bypass; RK14 stale authority | The v0.2 target is read-only and its authority and policy are server owned. Shipped production capability arrays remain empty and default readiness remains blocked. The compile-time exact-five assembly is unregistered, always reports production registration false and becomes candidate-ready only while all five operations and their dependencies remain intact. This proves a bounded negative property only; consequential action, permits and cancellation remain deferred. |
| Unauthorised or shadow identity | 30.1% | RK04 agent identity substitution; RK05 token replay; RK06 overbroad scopes; RK09 provider credential misuse | The repository has a closed capability registry and no production credential or protected identity path. It does not yet demonstrate deny-unknown workload identity. That belongs to the protected authority work planned for v0.3.0. |
| Upstream supply-chain compromise | 21.9% | RK02 tool poisoning; RK23 supply-chain compromise; RK30 operational drift | Exact source/build identities, lock files, two byte-identical builds, complete SBOM, CodeQL and image evidence are present. These controls reduce and expose risk; they do not prove the supply chain safe or accept retained vulnerabilities. |
| Agent exceeds intended scope or causes systemic failure | 20.1% | RK06 overbroad scopes; RK08 policy bypass; RK17 exhaustion; RK24 model/tool hallucination | Closed schemas, fixed providers, deterministic execution, request/resource ceilings and a compile-time exact-five assembly bound the unregistered candidate. Public policy, provider state and explicit suspension can only remove operations, while shipped production activation arrays remain empty. Multi-agent, mutating and protected-scope behaviour is not implemented. |
| Insufficient logging or auditability hindered investigation | 7.1% | RK20 provenance spoofing; RK21 audit tampering; RK25 telemetry leakage | Canonical receipts, a durable content-addressed ledger, receipt inspection and source/build provenance are implemented behind inactive boundaries. The ledger is not signed, WORM, externally checkpointed, backed up or deployed. |

## Negative assurance already demonstrated

Negative assurance means evidence that specified attempts to reach a prohibited
state or action were rejected under defined test conditions. It is narrower than a
general claim of unreachability or safety.

The existing repository demonstrates, through executable tests and generated
assurance, that under its stated local candidate conditions:

- planned or suspended tools do not enter the callable set, and registry metadata
  cannot activate runtime capability;
- a caller cannot introduce an arbitrary provider URL, redirect, credential or
  proxy into the fixed ONS adapter;
- denied, cancelled, malformed or evidence-failed operations do not return a
  successful result with a valid receipt;
- exact-key retry cannot repeat provider execution after an accepted or uncertain
  operation state;
- the blocked container does not advertise tools, provider capability or readiness;
  and
- protected or personal payloads are outside the public contracts and retained
  evidence boundary.

These properties are exercised across the gateway, provider-adapter, execution,
contract, interoperability and container suites. The integrated Stage 2 mapping in
[`docs/threat-model/QUAL-206_STAGE_2_RELEASE.md`](../../../threat-model/QUAL-206_STAGE_2_RELEASE.md)
retains the exact residual gates.

## Supported conclusion

The survey adds external coverage context for the existing threat families, but does
not establish their risk priority or justify new v0.2 runtime behaviour. The next
gaps are specifically
protected identity, protected-tier policy-filtered discovery, delegated authority,
consequential action recovery and production evidence operations. They should be
designed and tested in later work rather than implied by the anonymous open tier.
