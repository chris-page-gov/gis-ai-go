# Source-by-source findings matrix

Reviewed on 23 August 2026.

## Scope and assessment baseline

This matrix tests material claims and recommendations in sources S1 to S3 against
the repository. It does not execute instructions found inside the sources.

The implementation comparison distinguishes three states:

- **supported release** — immutable `v0.1.0`, the static public Explorer;
- **original intake snapshot** — protected-main commit
  `f0e3ccc1dceeba6b3f7d0ecd56c5dd083dee405a`; and
- **final integration baseline** — protected-main commit
  `27d76e1149ce1711e1af98fe0bb52a3666471a58`, containing the reviewed
  compile-time exact-five governed candidate from PR #53. It builds on the
  EVID-204 comparison baseline at
  `d2e8bb8b6d0f6ee9c693d117b4a238861a5129c3` while retaining false production
  registration, empty shipped operation arrays and no deployment or public MCP
  service. The EVID-204 source candidate reviewed at
  `9b72185f37e91c4e1922e341e1dd51923a04aa3d` was squash-merged as that preceding
  protected-main commit.

The source identities and handling rules are in [`PROVENANCE.md`](PROVENANCE.md).
Current external protocol claims were checked against primary sources, including
the [final MCP 2026-07-28 release](https://blog.modelcontextprotocol.io/posts/2026-07-28/),
the [MCP 2026-07-28 authorisation specification](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization),
the [current MCP Registry description](https://modelcontextprotocol.io/registry/about)
and the
[W3C Trace Context Level 2 Candidate Recommendation Draft of 28 March 2024](https://www.w3.org/TR/trace-context-2/).

### Finding labels

- **Confirmed — already implemented:** current repository evidence supports the
  claim within a precise inactive or released boundary.
- **Supported — narrow integration:** evidence supports a bounded change included
  by this intake.
- **Partly supported — defer:** the direction is plausible, but the current tier or
  evidence does not support implementation now.
- **Context only:** useful research context, not a product requirement or proof.
- **Rejected:** inaccurate, unverified, unsafe or outside the authorised boundary.

## S1 — AvePoint/Osterman Research, *The State of AI 2026*

All percentages below are respondent-reported survey findings. They must not be
described as independently measured global or UK Government prevalence.

| ID and source locator | Claim or observation | Test against GIS AI GO | Finding and action |
| --- | --- | --- | --- |
| S1-01, pp. 4 and 6 | The report is based on a global survey of 750 people responsible for information management, data security or AI programmes. | The report's demographic design provides relevant operational context, but no sample in the repository can independently reproduce or validate it. It is not UK Government-specific. | **Context only.** Retain the sample, sponsorship and generalisability limits beside every quantitative use. |
| S1-02, pp. 18–19 | 46.9% of represented employees use agents daily or weekly; 21.1% of respondents do not know whether unsanctioned tools are used to create agents. | `profiles/tool-registry.v1.json` provides a closed 12-capability inventory and `apps/mcp-gateway/src/governed-assembly.ts` derives one exact-five, compile-time candidate from that registry, public policy, provider lifecycle and evidence state. `apps/mcp-gateway/src/activation.ts` and every shipped entrypoint still keep production operation arrays empty. The repository does not inventory or authenticate deployed agents. | **Partly supported — defer.** The capability inventory and candidate projection are evidence-backed; workload/agent inventory and deny-unknown identity belong to the later protected-authority experiment, not anonymous v0.2. |
| S1-03, p. 27 | 86% report an agent deployment delay averaging 5.92 months because of data-security or data-management risk. | GIS AI GO uses explicit evidence and activation gates, but one survey statistic cannot set its schedule, thresholds or release decision. | **Context only.** Do not weaken or accelerate gates because of the reported delay. |
| S1-04, pp. 16 and 30 | 88.4% report at least one AI-agent security breach in the previous 12 months. | The repository cannot validate respondent incident histories. Its acceptance evidence concerns only its own fixed candidate. | **Context only.** Use the figure only with the respondent-reported and vendor-sponsored qualifiers. It is not evidence that GIS AI GO is safe or unsafe. |
| S1-05, pp. 5 and 12 | High confidence coexists with reported unauthorised-access incidents: 62% among the highest-confidence group and 72% among respondents reporting “very confident”. | `evaluation/qual-206-local-evaluation-receipts.v1.json`, `docs/threat-model/QUAL-206_STAGE_2_RELEASE.md` and the repository/image gates test behaviours and retain failed or blocked states rather than relying on assurance statements. | **Supported — narrow integration.** Name the existing pattern **negative assurance** and continue to bind claims to executable evidence. Do not infer causation from the survey association. |
| S1-06, p. 30 | Seven reported incident categories cover exposure, malicious input, unauthorised action, shadow identity, supply chain, exceeded scope and missing auditability. | Every category maps to one or more of RK01–RK30 in `evaluation/threat-risks.json`; coverage and residual gaps differ materially. | **Supported — narrow integration.** The qualified mapping is integrated in [`THREAT_EVIDENCE_CROSSWALK.md`](THREAT_EVIDENCE_CROSSWALK.md). No risk is re-rated and no test pass is inferred from the survey. |
| S1-07, p. 29 | Planned investment is led by governance monitoring (62.4%), followed by agent-security, cost, analytics and erroneous-action controls. | GIS AI GO already separates registry, policy, execution, evidence and assurance. Spending intentions do not prove an Agent Management Platform category, product architecture or control effectiveness. | **Context only.** Preserve as market evidence; do not rename GIS AI GO or introduce a platform dependency. |
| S1-08, pp. 12 and 21 | AI FinOps should connect variable agent spend, retries and loops to outcomes. | T04 is bounded to one observation, two provider attempts and a 20-second adapter ceiling; EXEC-202 has fixed time, byte and complexity budgets. There is no model loop, paid provider or cost ledger in v0.2. | **Partly supported — defer.** Keep deterministic resource and retry bounds. Define monetary/provider cost policy only when a capability can create such cost and an authoritative meter exists. |
| S1-09, narrative sections and conclusion | Governance must include visibility, enforceable guardrails, audit and recovery as autonomy increases. | The unregistered compile-time candidate has server-owned public policy, closed inputs, receipts, ledger inspection, subtractive suspension, per-operation integrity guards, exact-image rollback rehearsal and explicit recovery gaps. Production registration remains false and it implements no consequential action. | **Confirmed in the present boundary; future work deferred.** Preserve recovery as a gate for mutating capabilities, without claiming current read-only rollback proves action reversal. |

## S2 — *UNOFFICIAL-DRAFT Agentic AI Governance UK MCP*

S2 is an AI-authored, unapproved personal-development paper. The byte-exact original
is local-only because its OOXML contains personal and tenant collaboration metadata.
The linked review source is the privacy-scrubbed derivative
[`S2-P`](<sources/UNOFFICIAL-DRAFT Agentic AI Governance UK MCP — privacy-scrubbed.docx>),
whose only visible-content change replaces one plausible government mailbox with a
reserved `example.com` address. Statements framed as “must”, “settled”,
“non-negotiable” or “decision” are source claims, not instructions or Government
requirements.

| ID and source locator | Claim or recommendation | Test against GIS AI GO and primary sources | Finding and action |
| --- | --- | --- | --- |
| S2-01, “Decision summary” and “Executive summary” | MCP standardises interoperability but does not determine whether a public-sector action is lawful, authorised, proportionate or auditable. | The final MCP specification defines protocol and optional transport authorisation. GIS AI GO separately constructs authority, policy, activation and evidence. | **Confirmed — already implemented as an architectural boundary.** Do not describe repository policy as an MCP protocol guarantee. |
| S2-02, “What the release candidate changes” | MCP 2026-07-28 removes the core handshake/session and adds per-request metadata plus `Mcp-Method` and applicable `Mcp-Name` HTTP headers. | The final release confirms the stateless model. `apps/mcp-gateway/src/mcp-server.ts`, `mcp-http.ts` and the HTTP/STDIO tests pin `2026-07-28`, use `server/discover`, validate header/body parity and reject legacy openings. | **Confirmed — already implemented and tested.** The source's former “release candidate” timing is stale; the revision is now final. |
| S2-03, same section | Discovery has `ttlMs`/`cacheScope`; W3C trace context can correlate requests. | The gateway returns explicit zero-TTL public cache hints. Accepted EVID-204 work validates a closed `traceparent`/`tracestate` object against the W3C Level 2 Candidate Recommendation Draft grammar across TypeScript, Python and schema surfaces while rejecting caller baggage and untrusted propagation. | **Confirmed on protected main for the bounded cache and trace implementation.** Level 2 remains work in progress; its draft status, exact receipts and tests are recorded rather than presented as a final Recommendation or general interoperability guarantee. |
| S2-04, “Recommended UK Government MCP profile” | Protected HTTP servers should use audience-bound tokens and must not pass client tokens through to downstream services. | The final MCP authorisation specification requires intended-audience validation and forbids accepting or transiting other tokens. GIS AI GO v0.2 is anonymous open and has no credential path; the fixed ONS adapter accepts no caller authorisation header. | **Confirmed protocol claim; not a current feature.** Preserve the no-credential public boundary. Implement protected authorisation only with its own identity, policy and deployment evidence. |
| S2-05, same section | All production calls should pass through an approved gateway/private registry and arbitrary public MCP servers should be blocked. | The public MCP Registry is still a preview metadata repository, does not support private servers and delegates code scanning. That supports curation as a risk control, but does not make the draft's blanket blocking stance a protocol requirement. GIS AI GO's registry is a closed local profile, not an enterprise registry. | **Partly supported — defer policy choice.** Keep the GIS AI GO runtime allowlist and no arbitrary server/fetch paths. Do not claim a Government-wide policy or build a private registry in v0.2. |
| S2-06, “Minimum controls” and recommendations | Consequential actions need risk-tiered authority and, where justified, human approval. | `workflow.execute` is explicitly mutating, unimplemented and deferred to v0.3. The current five-tool target is read-only. No approval or permit service exists. | **Partly supported — defer.** Treat approval as one mechanism for satisfying authority, not as a blanket control. Do not add a cosmetic HITL field to the anonymous tier. |
| S2-07, Appendix A | Tool metadata should include ownership, classification, risk, action type, approval, retention, schemas and versions. | The current profile records IDs, lifecycle, read/mutate status, access tiers, policy attributes, schemas, versions, provenance, fallback, threats and source binding. It does not assert a Government owner, legal basis, ATRS record or protected classification. | **Partly confirmed.** Current metadata is appropriate to an open personal-repository candidate. Organisation-specific fields require real ownership and authority; invented values are rejected. |
| S2-08, Appendix B | A common evidence record should include actor/delegation, call, parameters or digest, policy, approval, result/outcome, trace and store reference. | `schemas/evidence-receipt-v2.schema.json` binds server-owned anonymous authority, operation, normalised-parameter digest, policy, resource/rights, transformation, software, result digest and verification. Durable storage is a separate post-write reference. It intentionally stores no human identity, prompt, raw query or full result. | **Confirmed as a useful superset, partly implemented.** Preserve data minimisation and issue-time truth. A protected/mutating receipt should be a separately reviewed version, not an expansion that weakens the public receipt. |
| S2-09, Appendices A and B worked refund example | Illustrative HMRC identities, accounts, legal bases, classifications, retention and transaction values demonstrate the proposed schemas. | The values are unverified, resemble real government/person data and concern consequential financial action outside GIS AI GO. | **Rejected.** Do not import, test, publish as fact, or treat as a safe fixture. Any future mutating example must be clearly fictional, non-governmental and independently reviewed. |
| S2-10, “Legal, accountability and redress” and worked examples | Specific legal duties and publication/retention conclusions apply to the hypothetical services. | No legal review or departmental approval accompanies the source, and the repository is not authorised to make those determinations. | **Rejected as implementation authority.** Retain as a research question only; obtain qualified legal/records/privacy decisions before a real protected or consequential pilot. |
| S2-11, document presentation and provenance statements | The draft carries an `OFFICIAL` footer while also declaring itself unofficial, AI-authored and unapproved. | The statements conflict; no originating Government organisation, information owner or classification authority is established. The tracked privacy-scrubbed derivative retains the visible footer as source evidence while removing its non-visible Purview identifiers. | **Rejected classification claim.** Preserve the byte-exact original locally and the visible marking in the derivative, record the conflict and never inherit the footer as repository classification or endorsement. |

## S3 — updated advisory review

S3 is a thoughtful synthesis, but it remains an advisory secondary source. Its
implementation statements were checked against the repository rather than accepted
at face value.

| ID and source locator | Claim or recommendation | Test against GIS AI GO | Finding and action |
| --- | --- | --- | --- |
| S3-01, executive conclusion and sections 3/15 | Agent governance is operational infrastructure around the route from knowledge and authority to execution, evidence and recovery; action is the principal governance unit. | The repository separates OKF, authority, policy, activation, deterministic execution, results, receipts, ledger and rollback. Current operational action is deliberately read-only. | **Confirmed as the current design direction.** No new architectural layer or runtime dependency is needed. |
| S3-02, sections 2 and 18 | Distinguish declared from demonstrated governance and formalise negative assurance. | Protected-main and release claims are bound to exact commits, builds, tests and explicit blocked states. Zero-default activation, no arbitrary egress, evidence-failure and readiness tests demonstrate several defined negative properties. | **Supported — narrow integration.** The crosswalk defines the term and its bounded present evidence. Avoid absolute claims such as “cannot ever”. |
| S3-03, sections 4 and 5 | Expand OKF descriptive governance vocabulary across provenance, authority, lifecycle, freshness, quality, classification, sensitivity, retention, machine generation, fitness, uncertainty, rights and uses. | `okf/profile/public-discovery-v1.json` already requires authority, publication, access, rights, freshness, status, sources and limitations. Quality assessment, retention, machine-generation status, fitness and uncertainty are not a coherent mandatory vocabulary across all records. | **Partly supported — defer schema change.** Record a later OKF profile design task. Do not change a 36-record supported publication without field semantics, source evidence, migration, generated-output and consumer tests. |
| S3-04, sections 6, 7 and 17 | Expand registry thinking to a capability inventory and formal lifecycle or `CapabilityState`. | The tool profile already separates `implementationState`, `lifecycleState`, discovery eligibility, seven activation gates, target state and runtime authority. Its `candidate-unregistered` projection can contain only the exact five supported operations, while public policy, provider state and explicit suspension can only subtract from discovery. Production callability remains separately empty. It does not model every proposed state or actor-authorised transition. | **Confirmed concept; formalisation deferred.** The present multidimensional state is stronger than a single linear enum. Any new contract should preserve separate implementation, assurance, release, deployment, discovery and callability facts. |
| S3-05, section 9 | Treat survey incident categories as an industry-derived adversarial test family. | All seven categories map to existing RK01–RK30, but protected identity and consequential-action coverage remains design-stage. | **Supported — narrow integration.** Added the qualified crosswalk; no synthetic test is marked passed merely because a category maps to a risk. |
| S3-06, section 10 | Make reversibility and recovery explicit: reversal authority, safe retry, uncertain outcome, suspension and evidence preservation. | Receipt-only reconciliation blocks duplicate execution after lost response; deployment evidence rehearses suspension and exact-image restoration. There is no mutating user action to reverse and no production disaster recovery. | **Partly supported — defer.** Reuse these properties as gates for the future synthetic consequential-action experiment. Do not relabel service rollback as business-action reversal. |
| S3-07, section 12 | Make cost ceiling, resource budget, quota, execution count, retries and accumulated cost policy dimensions. | Runtime ceilings, attempts and timing are already deterministic; monetary cost and value are not observable in the current no-model, no-paid-provider path. | **Partly supported — defer.** Keep resource limits now. Add monetary fields only with authoritative metering and a capability that incurs variable external cost. |
| S3-08, section 19 | Enrich receipts to answer who, why, capability, resource, decision, execution, outcome and proof. | The anonymous public receipt already answers most capability/resource/decision/execution/proof questions through content identities and digests. Human, agent, organisation, delegation, approval and downstream-effect fields would be false or privacy-expanding in the present tier. | **Partly supported — defer protected version.** Do not add null, invented or personal fields to v2. Design a distinct protected/mutating receipt with retention and access policy. |
| S3-09, section 20 | Prioritise recognised identity, policy-filtered discovery, bounded delegation, transaction permits and a synthetic consequential action over rapidly adding providers. | The unregistered v0.2 candidate now applies its fixed anonymous-open policy, provider lifecycle and explicit suspensions identically to direct and MCP discovery. `docs/implementation/ROADMAP.md` still places recognised authority, protected policy, delegation and permits in v0.3; `workflow.execute` is deferred. Independent-host, deployment and release assurance remain open for v0.2. | **Supported future direction, no current scope change.** Finish v0.2 first; then run the protected-authority and consequential-action experiments with synthetic data and no real protected integration. |
| S3-10, sections 21 and 22 | Model authority and assurance as graphs linking actors, controls, tests, commits, builds, releases, deployments and receipts. | Repository provenance, SLSA attestations, SBOM, release evidence and content-addressed receipts create many graph edges, but no single queryable graph or protected authority chain exists. | **Partly supported — research design.** Preserve exact identifiers now; define a use case and minimal interoperable model before adding a graph store or schema. |
| S3-11, section 23 | Separate a protocol-independent action-governance model, an MCP profile, an evidence specification and the GIS AI GO implementation. | The repository already distinguishes historical research, ADRs/contracts, operations evidence and implementation, but it is not an official UK Government profile or standard. | **Supported editorial boundary.** Keep normative claims separate from experimental evidence; no repository rename or product claim follows. |
| S3-12, sections 11 and 14 | Do not adopt vendor category terms such as Agent Management Platform or imprecise claims about agents “learning” as architecture. | GIS AI GO is protocol/provider-neutral and defines bounded deterministic components. | **Confirmed — no change.** Use precise capability and authority language; market terminology remains contextual. |
| S3-13, section 16 | The supported product is v0.1.0 while protected-main development has substantial inactive v0.2 capability and no public MCP service. | `README.md`, `CONTEXT.md`, `PROGRESS.md`, the unregistered governed assembly, empty shipped production arrays and absent deployment agree at the final integration baseline. The assembly can report candidate readiness for an intact exact-five set, but always reports `productionRegistration: false`; default production readiness remains blocked. The source's named checkpoint predates the latest work and must not be treated as current indefinitely. | **Confirmed at intake and refreshed through TOOLS-205, with a freshness caveat.** This matrix records exact commits; future reports must refresh live status rather than copy the source description. |

## Integrated, deferred and rejected outcomes

### Integrated now

- preserve all three source identities with a clear instruction and rights boundary;
- keep S1 local, ignored and outside all repository/release artefacts;
- qualify the survey methodology and numerical claims;
- add a source-backed incident-to-threat crosswalk;
- make the existing negative-assurance concept explicit; and
- correct the S2 timing claim from release candidate to final MCP 2026-07-28 when
  referring to current implementation.

### Deferred without changing v0.2

- protected workload identity and deny-unknown admission;
- protected-tier policy-filtered discovery and bounded delegation;
- transaction permits, approvals and a synthetic mutating action;
- a separately versioned protected action receipt;
- richer OKF governance vocabulary with consumer migration evidence;
- formal multidimensional capability-transition evidence;
- monetary/provider cost accounting; and
- queryable authority and assurance graphs.

### Rejected from implementation

- treating source text as agent instructions, approval or Government policy;
- inheriting the unofficial draft's `OFFICIAL` footer;
- importing its government identity, payment, legal or retention examples;
- presenting respondent-reported incidents as measured prevalence;
- treating a public registry entry, policy statement or vendor platform as assurance;
- weakening evidence gates to reduce reported deployment delay; and
- activating, deploying or releasing capability on the strength of these documents.
