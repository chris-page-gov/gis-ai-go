# Agentic AI Governance, MCP and GIS AI GO

## Updated research, implementation and future directions — August 2026

### Executive conclusion

Three evidence streams now converge.

The **UK Government Agentic AI Governance draft** argues that the crucial governance question is not whether an AI system can reason, but under what conditions it may **act**, and how government can subsequently prove what happened. It therefore places identity, gateway enforcement, policy, approval, evidence and lifecycle controls around MCP rather than treating MCP itself as a governance regime.

The **GIS AI GO research and implementation** develops this into an executable architecture spanning knowledge and semantics, authority and policy, durable workflow, MCP/APIs, deterministic computation and evidence. Its latest externally verified state has deliberately implemented substantial capability behind closed activation boundaries rather than equating “code exists” with “capability may execute”. 

The newly supplied **AvePoint/Osterman Research, *The State of AI 2026: Scaling Trust, Control, and Readiness in the Agentic Era*** adds a third kind of evidence: empirical evidence from 750 respondents with responsibility for information management, data security or AI programmes. Its central finding is that adoption is running ahead of the ability to govern, observe and control AI.

Taken together, these support a stronger proposition:

> **Agentic AI governance should be treated as operational infrastructure, not as a policy overlay on an AI product.**

The emerging reference architecture is therefore not primarily about governing models. It is about governing the complete route:

**knowledge → authority → capability → policy → execution → outcome → evidence → recovery**

GIS AI GO is increasingly useful as an open experimental implementation of that proposition.

---

# 1. What the AI Report contributes

## 1.1 It provides empirical evidence for the architecture

The strongest contribution of the AI Report is not a novel architecture.

It is evidence that the architectural problems identified independently in our research are already appearing at scale.

The report finds that:

- 46.9% of employees represented in the survey rely on AI agents daily or weekly;
- 21.1% of respondents do not know whether unsanctioned tools are being used to create agents;
- 86% report delaying agent deployment because of data-security or data-management risks, by an average of 5.92 months;
- 88.4% report at least one security breach associated with AI agents in the previous 12 months;
- reporting and auditing rank amongst the most difficult internal readiness problems;
- the most common planned investment is in governance tooling that monitors agent actions for alignment with data-governance policy.

Those findings give external support to the proposition that **registry, policy enforcement, observability and evidence are not secondary assurance functions**.

They are becoming prerequisites for deployment.

---

# 2. The “confidence–incident paradox” is especially important

One of the report's strongest findings is what it calls the **Confidence-Incident Paradox**.

More than four in five respondents say they are confident about preventing unauthorised data access, yet high rates of AI-related unauthorised-access incidents occur amongst those same organisations.

The report expands this point later: organisations can possess policies, sanctioned tools and pilots while operational controls still fail. It argues that incidents depend upon whether access is actually governed, usage is visible and guardrails are actually enforced.

This is highly relevant to our work.

It creates a useful distinction between:

**declared governance**

and

**demonstrated governance**.

That distinction should become explicit in the UK Government research.

For example:

| Declared governance | Demonstrated governance |
|---|---|
| “Agents must not access unauthorised data.” | A test demonstrates that unauthorised authority cannot discover or invoke the capability. |
| “High-risk actions require approval.” | Execution cannot proceed without cryptographically or structurally bound approval evidence. |
| “All actions are audited.” | A tool invocation cannot complete successfully without producing the required evidence object. |
| “Only approved agents may operate.” | An unknown agent identity fails admission and cannot acquire capability. |
| “Production is controlled.” | The executable remains unreachable until the independently defined activation conditions are satisfied. |

This is precisely where GIS AI GO's approach is unusually valuable.

---

# 3. The AI Report strongly reinforces the shift from output risk to action risk

The *Unofficial Draft* identifies the transition from reasoning to tool invocation as the decisive governance boundary.

The AI Report independently reaches essentially the same conclusion from operational evidence.

Its AI-agent section states that the risk changes when systems move from outputs to autonomous actions: controls designed around human decision-making may break down when agents operate continuously across systems.

Its expert perspective puts the distinction particularly clearly: agent autonomy changes the risk from flawed outputs to flawed actions, requiring visibility, enforceable guardrails, auditable records and recovery.

This substantially strengthens one of our foundational claims:

> **The principal unit of governance should be the attempted action, not simply the generated answer.**

That should now be elevated from architectural recommendation to one of the central research propositions.

---

# 4. A further contribution: data governance belongs upstream of agent governance

The AI Report also adds emphasis that our MCP-focused work could otherwise underweight.

It argues that **data readiness is AI readiness**.

AI-generated information introduces lineage, quality, lifecycle and reuse problems, while existing enterprise data may already contain substantial volumes of old, poorly classified or poorly governed information.

Its expert commentary argues that classification, retention, lifecycle management and access control become AI safeguards rather than merely information-management housekeeping.

This gives additional importance to GIS AI GO's **C1 — Domain knowledge and semantics**.

The six-control GIS AI GO architecture currently starts with:

1. domain knowledge and semantics;
2. authority, identity and policy;
3. durable workflow and human control;
4. MCP, APIs and events;
5. authoritative data and deterministic computation;
6. evidence, audit and assurance. 

That first control is not decorative metadata.

It is part of governance.

An agent cannot make a properly governed decision about information it cannot correctly characterise.

That strengthens the case for OKF as a **knowledge-governance substrate**.

---

# 5. OKF should therefore capture more than discovery metadata

The earlier GIS AI GO research already correctly limits OKF's role: it describes knowledge, provenance and governance properties without pretending to replace runtime policy.

The AI Report suggests extending the **descriptive governance vocabulary**, for example to include:

- provenance;
- authority/source;
- lifecycle state;
- freshness;
- quality assessment;
- classification;
- sensitivity;
- retention;
- machine-generated status;
- fitness for purpose;
- known uncertainty;
- rights/licence;
- permitted or expected uses.

Runtime policy still determines whether something may actually be used.

But this richer knowledge description provides better material upon which policy can operate.

The conceptual division becomes:

> **OKF describes what we know about the resource.  
> Policy decides whether it may be used here.  
> Deterministic systems perform the authorised operation.  
> Evidence records what happened.**

---

# 6. The “shadow agent” problem validates the registry model

The AI Report reports a material visibility problem around unsanctioned agent-building tools, including respondents who simply do not know whether such tools are being used.

This directly reinforces the *Unofficial Draft's* recommendation for curated registries and its warning against arbitrary public MCP servers. The earlier report recommends a private or curated production registry and blocking direct arbitrary public-server access unless reviewed, mirrored or proxied.

The research should now broaden this from a **server registry** into a **capability inventory**.

Government needs to know about at least:

- deployed agents;
- agent/workload identities;
- MCP servers;
- tools;
- provider adapters;
- data resources;
- policies;
- workflows;
- deployments;
- current capability state.

An unregistered agent should not simply be labelled “shadow AI”.

It should lack the technical authority required to cross governed infrastructure boundaries.

---

# 7. GIS AI GO can exemplify a stronger answer to shadow agents

A mature reference implementation should show that being able to run code is not the same as having organisational authority.

An unknown agent should be able to propose an action but fail to acquire:

- trusted authority context;
- protected discovery;
- transaction permits;
- provider credentials;
- protected data;
- consequential tool invocation.

This turns agent inventory from passive CMDB-style knowledge into an actual security primitive.

A future GIS AI GO protected experiment should therefore test:

> **Can an otherwise valid MCP client with an unrecognised agent/workload identity obtain any privileged capability?**

The required result should be demonstrably **no**.

---

# 8. Human-in-the-loop needs to be treated carefully

The AI Report finds significant concern about agents bypassing human-in-the-loop controls. Among the “extremely concerned” cohort this is its leading agent concern.

It also reports that adding HITL controls is the most common mitigation respondents have used.

This validates the importance of the problem, but it should **not cause us simply to maximise human approval**.

The *Unofficial Draft* is stronger here because it explicitly proposes **risk-tiered** approval.

Our research should go further still.

The proper design question is:

> **What authority must be present before this particular action may execute?**

The answer may be:

- autonomous permission;
- standing delegation;
- policy-based step-up;
- explicit approval;
- two-person control;
- professional/legal authority;
- prohibition.

Human intervention is therefore one possible mechanism for satisfying an authority requirement.

It is not itself the governance architecture.

---

# 9. The incident breakdown gives GIS AI GO a concrete adversarial test catalogue

Page 30 of the AI Report is especially valuable.

It reports the following types of agent-related incident:

- sensitive/confidential data exposed or retained;
- unauthorised or shadow identities created or misused;
- autonomous unauthorised actions;
- malicious or untrusted input manipulation;
- upstream supply-chain compromise;
- agents operating beyond intended scope;
- insufficient logging preventing investigation.

This maps remarkably well onto the existing GIS AI GO threat work.

It should now become an explicit **industry-evidence-derived threat family** in the reference implementation.

For example:

| Reported failure | GIS AI GO control/test |
|---|---|
| Data exposure | rights/classification controls, fixed result schemas, privacy-bound evidence |
| Shadow identity | registered workload/agent identity and deny-unknown admission |
| Unauthorised action | policy enforcement and transaction permit |
| Malicious input | prompt/data isolation, schema-bound tools, no arbitrary fetch |
| Supply-chain compromise | pinned dependencies, SBOM, attestations, source/build identity |
| Agent exceeds scope | bounded capabilities and purpose/resource restrictions |
| Missing investigation evidence | action receipt, trace and durable evidence |

That gives the reference implementation external empirical justification for its test programme.

---

# 10. The AI Report gives stronger support to recovery as a governance primitive

The report repeatedly pairs prevention with the ability to **detect, correct and recover**.

Its expert section describes recovery capabilities as necessary to limit the blast radius of mistakes.

The conclusion similarly says trust depends upon the ability to control access, govern operation, audit activity **and recover when something goes wrong**.

This supports something the *Unofficial Draft* already contains but which deserves greater prominence:

- gateway kill switch;
- credential revocation;
- agent quarantine;
- registry suspension;
- evidence freeze.

The governance reference model should explicitly add:

### Reversibility and recovery

A consequential capability should state:

- whether it is reversible;
- how reversal works;
- who may order reversal;
- whether retries are safe;
- what happens after an uncertain outcome;
- how capability is suspended;
- how evidence is preserved.

This is particularly important for future mutating GIS AI GO experiments.

---

# 11. The report's Agent Management Platform idea is useful — but should not become our architecture

The report repeatedly introduces an **Agent Management Platform (AMP)** as a unified layer for visibility, lifecycle control, policy enforcement and auditability.

It also interprets planned enterprise spending on agent monitoring, security, analytics and cost controls as early evidence of an AMP market.

This is useful market evidence.

But I would **not rename our architecture “AMP” or make GIS AI GO an AMP implementation**.

AMP is presently best treated as a developing market/category abstraction.

Our architecture is more fundamental and portable:

- knowledge;
- identity/authority;
- policy;
- lifecycle;
- discovery;
- execution;
- evidence;
- recovery.

An AMP might implement some or all of those functions.

The UK Government reference model should specify **the required properties**, not procure a product-category label.

---

# 12. The AI Report also reinforces the economic argument for governance

An interesting section of the report discusses AI FinOps and the need to attribute variable agent costs to actual outcomes. Agent systems may generate variable expenditure through model calls, retries, reasoning traces and multi-agent loops.

This is not central to the earlier governance paper, but it should be added.

A governed action should potentially carry:

- cost ceiling;
- resource budget;
- provider quota;
- execution count;
- retry budget;
- accumulated cost;
- expected value/outcome category.

This is another reason to mediate actions through a controlled gateway rather than allowing agents unrestricted downstream access.

**Cost is a policy dimension.**

---

# 13. One important caution: the AI Report is evidence, not specification

The AvePoint/Osterman work should be treated carefully.

It is a vendor-sponsored global survey, although it states that the research was conducted by Osterman Research and was intended to produce findings independent of a particular platform.

The sample contains financial services/insurance, healthcare and government/public-sector respondents and spans EMEA, the Americas and APAC, including the UK.

That makes it highly relevant.

But it is **not**:

- UK Government-specific;
- a security incident dataset independently verified by investigators;
- a technical standard;
- a legal analysis;
- a specification of agent behaviour.

Particularly striking survey figures such as the reported **88.4% agent-related security breach rate** should therefore be described precisely as **respondent-reported survey findings**, not as a measured global breach prevalence.

That distinction matters.

---

# 14. The report also contains terminology that should not silently enter the reference architecture

For example, it sometimes describes agents as autonomously “learning” or making probabilistic decisions.

That is a reasonable high-level enterprise description, but it does not accurately describe every agent architecture.

A deterministic orchestration using an LLM for selected planning decisions is different from an online-learning autonomous system.

Our technical work should therefore preserve the more precise definition:

> An agent is a system that can select or sequence actions towards a goal and invoke capabilities, with the relevant governance risk arising from what authority and capability the surrounding system permits it to exercise.

We should use the survey to demonstrate the **operational phenomenon**, not inherit all its technical terminology.

---

# 15. The report validates the six-control GIS AI GO architecture

The mapping is unusually strong.

| AI Report evidence | GIS AI GO architecture |
|---|---|
| Data readiness | **C1 Domain knowledge & semantics**, C5 authoritative data |
| Identity/shadow agents | **C2 Authority, identity & policy** |
| HITL and action oversight | **C3 Durable workflow & human control** |
| Agent/tool governance | **C4 MCP, APIs & events** |
| Data quality/security | **C5 authoritative systems & computation** |
| Monitoring/audit/recovery | **C6 Evidence, audit & assurance** |

This means the AI Report should **not create a seventh architectural layer**.

Instead it supplies empirical validation for the six-control model.

---

# 16. Where GIS AI GO currently sits

The latest externally verified repository checkpoint is now substantially beyond the original August research design.

The supported public product remains `v0.1.0`, a static governed metadata/discovery Explorer rather than a public MCP service. 

Behind that public-release boundary, protected-main development has implemented or demonstrated:

- bounded catalogue discovery;
- direct API and MCP transports;
- deterministic execution;
- evidence receipts;
- durable evidence ledger structures;
- evidence inspection;
- provider selection;
- a bounded ONS adapter;
- data query;
- idempotency and lost-response reconciliation;
- capability/profile registry;
- host interoperability testing;
- reproducible builds;
- SBOM and security analysis;
- provenance attestations;
- container and deployment assurance.

The latest externally visible commit adds the blocked gateway container assurance work and deliberately preserves `503` readiness and the no-deployment/no-provider/no-release boundary. 

Because GIS AI GO remains under **active Codex development**, that is the latest externally verifiable checkpoint rather than necessarily the current working-tree state.

This distinction should be retained explicitly in future reporting.

---

# 17. GIS AI GO's strongest governance innovation may be “capability state”

Most systems discuss whether a tool exists.

GIS AI GO is increasingly distinguishing:

- specified;
- implemented;
- tested;
- reviewed;
- merged;
- released;
- deployed;
- discoverable;
- callable.

Those states should become formal.

A capability can be completely implemented while remaining deliberately non-callable.

That is an important governance property.

I recommend formalising something resembling:

**CapabilityState**

```text
defined
implemented
verified
approved
released
deployed
discoverable
callable
suspended
retired
```

Each transition should have an authority and evidence requirement.

That would be useful far beyond GIS AI GO.

---

# 18. The AI Report particularly strengthens the case for proving negative properties

The Confidence-Incident Paradox shows why an organisation's confidence that a control exists is weak evidence.

Therefore governance tests should establish not merely:

> authorised operation succeeds

but also:

> prohibited operation cannot succeed.

Examples:

- anonymous caller cannot reach protected data;
- unregistered agent cannot acquire privileged capability;
- deprecated tool is not discoverable;
- policy-denied call does not reach provider execution;
- failed approval cannot be replayed;
- cancelled transaction cannot continue unnoticed;
- arbitrary network destination cannot be introduced;
- protected data cannot enter public logs;
- service cannot become ready before activation gates pass.

That is a significant theme I would now explicitly call:

## Negative assurance

**Evidence that prohibited system states and prohibited actions are unreachable under defined conditions.**

This deserves to become a first-class property in the reference model.

---

# 19. Evidence receipts should become more ambitious

The *Unofficial Draft* proposed a common evidence record containing identity, tool invocation, policy, approval, result and outcome.

GIS AI GO has already begun strengthening this through canonical, content-addressed evidence.

The AI Report makes the purpose clearer.

If visibility and investigation are major operational weaknesses, the receipt should answer:

### Who?

- human actor;
- agent/workload;
- delegation chain;
- organisation/service.

### Why?

- purpose;
- legal/organisational authority;
- requested task.

### What capability?

- server;
- tool;
- tool version;
- schema;
- capability state.

### What resource?

- provider;
- dataset;
- version;
- licence;
- classification.

### What decision?

- policy;
- policy version;
- verdict;
- obligations;
- approval;
- permit.

### What execution?

- parameters or commitment;
- software/build;
- provider request;
- deterministic transformation.

### What happened?

- result;
- downstream effect;
- error;
- retry/idempotency state.

### What proves it?

- trace;
- receipt;
- ledger reference;
- artefact identity;
- attestation.

This is approaching something general enough to call a:

## Government Agent Action Receipt

GIS AI GO could be the first experimental implementation.

---

# 20. The next major research experiment should be authority, not more tools

The present open/read-only work is already proving a great deal.

I would resist expanding the number of provider tools rapidly.

The highest-value next experiments are increasingly governance experiments.

### Experiment A — recognised versus unrecognised agent

Two otherwise identical clients.

One possesses a registered workload identity; the other does not.

Prove that their capability sets differ correctly.

### Experiment B — policy-filtered discovery

The same query under:

- anonymous authority;
- ordinary authenticated authority;
- protected-data entitlement.

Prove that discovery itself is governed.

### Experiment C — bounded delegation

A user delegates one action to one agent for one purpose.

Prove that the authority cannot be repurposed.

### Experiment D — transaction permit

Policy converts an approved proposed action into a single-purpose, expiring execution permit.

Execution independently verifies it.

### Experiment E — synthetic consequential action

Introduce an entirely synthetic but state-changing operation.

Test:

- approval;
- idempotency;
- cancellation;
- unknown outcome;
- recovery;
- rollback;
- suspension.

Only after those properties are demonstrated should the same architecture be considered for real consequential action.

---

# 21. A further future direction: authority graphs

The *Unofficial Draft* correctly proposed a distinct agent identity.

The developing research suggests that a single `agent_id` will eventually be insufficient.

A transaction may involve:

**citizen / subject**
↓  
**human user**
↓  
**agent**
↓  
**government workload**
↓  
**MCP server**
↓  
**provider service**

There may also be:

- a delegating agent;
- department;
- device;
- approving officer;
- external organisation.

The relevant governance object is therefore an **authority graph**.

The action receipt should eventually capture enough of that graph to answer:

> On whose authority did this system act?

---

# 22. A further future direction: assurance graph

The same principle extends from runtime evidence to system assurance.

The research should aim eventually to link:

**requirement**
→ **control**
→ **policy**
→ **test**
→ **commit**
→ **build**
→ **SBOM**
→ **attestation**
→ **release**
→ **deployment**
→ **runtime action**
→ **receipt**
→ **incident / appeal**

That would create an **assurance graph** rather than a folder full of compliance documents.

It could answer:

> Is the system operating today actually the system whose controls were reviewed?

and:

> Which deployed action proves compliance with which requirement, under which policy version?

This could become one of the most useful generalisable outputs of GIS AI GO.

---

# 23. Revised UK Government research structure

I would now split the work into four related outputs.

## 1. Agentic Action Governance Reference Model

Protocol-independent.

Defines:

- authority;
- capability;
- consequence;
- policy;
- human control;
- execution;
- evidence;
- lifecycle;
- recovery.

## 2. UK Government MCP Profile

Defines how the reference model applies specifically to MCP:

- version;
- identity;
- authorisation;
- discovery;
- metadata;
- extensions;
- gateway;
- conformance;
- registry;
- trace/evidence.

## 3. Agent Governance Evidence and Assurance Specification

Defines:

- authority context;
- action receipt;
- capability-state evidence;
- assurance graph;
- incident evidence;
- retention;
- inspection.

## 4. GIS AI GO Reference Implementation

Provides the experimental proof:

- OKF;
- MCP;
- deterministic computation;
- policy;
- evidence;
- deployment;
- adversarial tests;
- known failures;
- interoperability evidence.

The AvePoint/Osterman report belongs primarily in the **evidence base for 1 and 3**, rather than becoming part of the normative specification.

---

# 24. Updated assessment of the AI Report

The AI Report contributes in five distinct ways.

### 1. Strong validation

It independently reinforces our principal thesis that **agentic AI is an action-control problem more than a model-control problem**. Its own expert section uses almost exactly that framing.

### 2. Empirical urgency

It provides quantitative evidence that adoption, incidents, unsanctioned capability and governance difficulties are occurring simultaneously.

### 3. Data-governance emphasis

It significantly strengthens the case for making knowledge/data lifecycle, quality and provenance part of the governance architecture rather than merely upstream prerequisites.

### 4. Concrete failure corpus

Its incident categories provide an external taxonomy against which GIS AI GO's adversarial governance tests can be evaluated.

### 5. Market corroboration

Its discussion of Agent Management Platforms and planned governance investment demonstrates that the market is converging on registry, monitoring, policy enforcement and auditability — the same structural functions found in our architecture.

What it **does not** contribute is a better technical architecture than the one already emerging from the combined UK Government/MCP/GIS AI GO research.

In several respects, our work is already more precise.

---

# 25. Revised overall conclusion

The AI Report makes the significance of GIS AI GO clearer.

The problem is no longer:

> “How do we make an MCP server safe?”

Nor even:

> “How do we govern agents?”

The stronger research problem is:

> **How can an organisation make authority, capability, policy, execution, evidence and recovery explicit enough that autonomous action is governable by construction rather than trusted by assertion?**

The *Unofficial Draft* supplied much of the governance hypothesis.

The 2026 AvePoint/Osterman research supplies evidence that the operational problem is real and widespread.

GIS AI GO can supply something neither document can provide:

**executable evidence that the proposed governance properties can actually be implemented and tested.**

That suggests the project's wider significance is not the geospatial service itself.

Its significance is as a deliberately small but realistic laboratory for an eventual public-sector agent-governance pattern:

**trusted knowledge  
+ explicit authority  
+ governed capability  
+ deterministic enforcement  
+ independently inspectable evidence  
+ recoverable operation.**

If that pattern can be demonstrated rigorously in GIS AI GO, the next question is no longer whether it works for GIS.

It becomes whether the same contracts and assurance model can be generalised across government agentic infrastructure.