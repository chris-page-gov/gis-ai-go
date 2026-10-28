> Repository note: searchable text extracted from [peer-review.public.docx](peer-review.public.docx). Source wording is preserved as dated evidence; it is not repository instructions. See [the intake record](README.md) for scope, provenance and handling.

> This review concerns the earlier 11-page case-study paper. It is not a review of the revised briefing or PR #147.

# Peer review: Governance as Code — GIS AI-GO case study

Oct 13, 2026 · @Chris Page

## Summary verdict

**Recommendation: major revision before it goes to the meeting.** The core idea is strong, the case study is real, and every one of the six permalinks resolves to the code it describes. But the draft repeatedly presents a *designed, not yet built* control (the trusted-base agreement stage) as a property the system already has. The repository's own design document says plainly that "v2 does not claim that boundary is present". A reader who clicks through will find that gap, and it undermines the paper's central claim.

What works well:

- The thesis is precise and modest: governance as code makes the precise parts of governance run at software speed, without replacing human judgement.

- The policy / policy-as-code / governance-as-code distinction (section 2) is useful and clearly tabled.

- The case study is concrete, pinned to an exact commit, and the commit is the current head of main. The 35 contract tests in tests/contract/test_ci_impact_plan.py pass at that commit.

- Picking *meta-governance* (who may change the controls) as the distinctive feature is the right insight, and it is genuinely under-discussed.

The five changes that matter most:

1.  Separate what is implemented (shadow planner, fail-safe defaults, contract tests) from what is designed (trusted-base agreement, CODEOWNERS-protected workflow ownership). Fix the present-tense claims in section 2, section 3.5, Figure 4 and the meeting script.

2.  Restore the words "Before enforcement" that the ellipsis in the section 3.5 quotation removes.

3.  Correct the workflow excerpt line numbers (off by two) and Figure 4's logic.

4.  Say what the routing is *for* (cutting roughly 4–5 minutes off the pull-request critical path) and what evidence will decide promotion.

5.  Restructure for the meeting. Open with a cover box giving the purpose, the ask and a three-sentence summary. Keep the body to 4–5 pages built around the case. Move the history, business case, Mermaid sources and permalinks to appendices.

## Major issues

Seven issues would mislead a careful reader or fail a technical check. Each one below includes a suggested fix.

### M1. Designed controls are presented as working ones

The draft says, in the present tense, that "a policy change cannot reduce scrutiny of its own pull request" and that "disagreeing policy decisions fail closed" (section 2 table). The meeting script says "a changed policy is not allowed to govern the pull request that changes it" (section 9).

At commit 97bc456, the reverse is true. The workflow runs scripts/plan_ci_impact.py and the map from the **candidate head** (ci.yml lines 49–55). The step summary even labels the result "candidate-head shadow" (line 76). CI_IMPACT_ROUTING.md line 52 says "The current workflow still runs the planner and map from the candidate head". Line 125 says "v2 does not claim that boundary is present". No disagreement check exists yet, so nothing can "fail closed" on disagreement.

The system is safe today because **shadow mode skips nothing**, not because of the trust boundary. That is still a good governance story: the automation is not allowed to act until it has earned it. But it is a different story from the one the draft tells.

**Fix:** add an "Implemented vs designed" table and use it consistently in sections 1, 2, 3.5, 3.6, Figure 4 and 9. Rewrite the meeting script along these lines: "…and the design forbids a changed policy from governing its own pull request; until that check is built, the planner is not allowed to skip anything."

### M2. The section 3.5 quotation drops its own conditional

The excerpt jumps from line 99 to line 102 with "…". The elided words, lines 99–102, are: "Shadow reporting may execute that candidate safely because it cannot skip verification. **Before enforcement**, the workflow must instead execute the planner and map from the trusted pull-request base…". Removing "Before enforcement" turns a future requirement into an apparent current fact. Quoted evidence must not change meaning through ellipsis.

**Fix:** quote lines 98–107 in full. They are short, and line 107 (CODEOWNERS) is relevant to the separation-of-duties argument anyway.

### M3. The planner does not stop a map from re-routing its own control files

Section 3.2 says the planner "refuses to accept a map that weakens the safety defaults". That holds only for the three top-level fields (mode, unknown_path_policy, push_main_policy) and for the rule that every force_full rule must select all lanes (lines 309–310).

I tested this at the pinned commit. I moved .github/\*\* and scripts/plan_ci_impact.py out of global-assurance-control and into documentation-and-governance, keeping the patterns sorted. The planner **accepted the map**. For .github/workflows/ci.yml, the map itself and the planner, it then returned reason: matched-rules, force_full: false, selected_lanes: \[repository_assurance\] and gateway_image_required: false. The contract test test_global_workflow_change_selects_every_lane would catch this, but that test sits in the same tree a pull request can edit.

This is a very good finding *for* the paper, not against it. It is exactly why the trusted-base stage exists, and it shows concretely why meta-governance is needed.

**Fix:** qualify the sentence in 3.2, and use this scenario as the worked example in 3.5. Optionally, recommend a hard-coded invariant in the planner: the map, planner, workflow and routing tests must resolve to a force_full rule.

### M4. Figure 4 merges two separate decisions

In Figure 4, "both closed outputs exactly agree" leads, on "yes", to "May become eligible after full checks + merge". In the design, though, agreement decides **this pull request's** routing (gateway_image_required = false only when both are exactly false). A candidate policy becoming eligible is a separate, later event after merge and exact-main verification. Also, for a pull request that changes the policy, step 5 forces full assurance under the base policy, so the "yes" branch cannot apply to policy changes at all.

**Fix:** use two lanes. Lane (a): per-pull-request routing (base and candidate agree on false leads to reduced; anything else leads to full). Lane (b): policy lifecycle (a policy-changing pull request gets full checks, then merge, then exact-main verification, and only then becomes the trusted base).

### M5. The workflow excerpt has wrong line numbers

In section 3.4 the jq block is numbered 56–63. In ci.yml at the pinned commit it is lines **58–65**. Line 56 is the plan_sha256 calculation and line 57 is force_full. For a paper whose subtitle promises "immutable GitHub references", a line-number error is the first thing a technical reviewer will notice.

### M6. The paper never says what the routing is for, or how it will be judged

The reader is never told that the impact router is a **test-selection optimisation**. The design document estimates it saves about 4–5 minutes on the pull-request critical path, and it saves no runner minutes yet. Without that context, "governance" seems to be guarding nothing in particular.

The design document's **promotion gate** (lines 81–96) is the strongest governance-as-code material in the repository, and the draft leaves it out. It lists six evidence criteria, including "recommended lanes have no false negative against the complete checks". The "832 tracked paths all routed" baseline test (lines 116–120) is also missing.

**Fix:** add a short "What is being traded" paragraph at the start of section 3, and a subsection on evidence-based promotion. If shadow data exists, report it (number of plans, false negatives found). If it does not, say so.

### M7. "Evidence is retained" overstates a 30-day diagnostic artefact

The plan is uploaded with retention-days: 30 (ci.yml line 90), and the design document calls it "a 30-day diagnostic artefact". Sections 2 and 5 present retained evidence as an audit trail ("a reconstructable record of which policy was in force"). The plan does record both commits and the map SHA-256, which is good, but it is deleted after 30 days.

**Fix:** say "retained for 30 days as diagnostic evidence", and name what an audit-grade version would need: longer retention, signed attestation, or storage outside CI.

## Accuracy check against commit 97bc456

All six permalinks resolve, and the pinned commit is the current head of main. Four of the six excerpts are faithful. The workflow excerpt is misnumbered and the design-document excerpt changes the meaning. In every case the linked range differs from the lines actually shown.

| Draft section | Linked range | Lines shown | Verdict | Note |
| ------------------------------ | -------------- | ------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 3.1 map defaults | 1–12 | 1–9 | Accurate | Line 9 is \], in the source but \] in the draft. Lines 10–12 start lanes and add nothing. Link 1–9. |
| 3.1 global-assurance-control | 81–100 | 83–95 | Accurate | Mention that .github/\*\* also covers the map itself (it lives in .github/ci/), so the map protects its own file. Also say "every lane *applicable to the event*": for a pull request that is 2 lanes, gateway_image and repository_assurance, as the test at lines 241–243 asserts. |
| 3.2 planner invariants | 224–231 | 224–230 | Accurate but cut short | It starts at a bare raise. The if that guards it is line 223, so start at 223. The stronger fail-closed evidence is just above: \_closed_object rejects unknown keys, \_unique_json_object rejects duplicate keys, and \_reject_json_constant rejects NaN and Infinity (lines 199–222). The claim needs qualifying (M3). |
| 3.3 contract tests | 221–255 | 221–248 | Accurate | Explain what the mutation test proves: it checks that **the coverage assertion itself can fail** (a test of the test). Better examples exist for "refuses a weakened policy": test_map_rejects_a_non_full_unknown_path_policy (line 437) and test_empty_change_set_fails_closed_to_every_lane (line 348). No test covers mode != shadow or a weakened push_main_policy. |
| 3.4 workflow | 28–79 | 28–63 as labelled | **Wrong line numbers** | The jq block is lines 58–65, not 56–63 (M5). The actual fail-full fallback is the job output expression on **line 22** (steps.plan.outputs… \|\| steps.fail_full.outputs…), which the draft never shows. |
| 3.5 design document | 95–136 | 98–106 | **Meaning changed** | The ellipsis removes "Before enforcement" (M2). It also leaves out "passed exact-main verification" from the paraphrase above the excerpt. |

Three further points of technical precision:

- **"Fail closed" means two different things here.** A planner *decision* under uncertainty becomes full assurance (unmatched-path, empty-change-set, no-applicable-lane). A planner *failure*, such as an invalid map or bad path, makes the job fail, and the required assurance aggregator then **blocks the merge**. Section 3.4's "missing or malformed output does not silently turn into permission" is true, but the stronger and more accurate statement is that it stops the gate. Say so.

- **Rules combine by union.** Every matching rule adds lanes and any force_full match wins (lines 376–398). This is a monotonic, "more specific cannot weaken" design, and it is worth one sentence. A most-specific-match design would let a narrow rule reduce scrutiny.

- **Unused supporting evidence.** The workflow sets permissions: {} at the top level and grants contents: read per job (lines 13, 25–26). It pins third-party actions to full commit SHAs (lines 33, 85). It sets persist-credentials: false. These are textbook least-privilege and supply-chain controls written as code, and they would strengthen section 3 and the "Authority" and "Execution" layers of section 7.

One small inconsistency in the repository, which the paper does not need to mention: line 57 reads force_full with jq -r and no type check, whereas gateway_image_required is strictly checked as a Boolean. It is harmless while nothing consumes force_full, but it is worth tightening before enforcement.

## Citations and lineage

The references that could be checked are broadly accurate. The weaknesses are mismatched in-text links, two uncited references, a publication index used where the primary source belongs, and a lineage that leaves out the traditions this case descends from most directly.

### Reference-by-reference

| \# | Reference | Status | Action |
| ----- | ------------------------------------------------------------------------ | ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | Hoare 1969, CACM 12(10) 576–580 | Correct | Mention Floyd (1967), "Assigning Meanings to Programs", on which Hoare built. |
| 2 | Meyer, publication index | Weak source | The cited page is an index, and I could not find the "written in 1986" note on it. Cite the primary source: Meyer, "Applying 'Design by Contract'", *IEEE Computer* 25(10), 1992, 40–51, plus *Object-Oriented Software Construction* (Prentice Hall, 1988). |
| 3 | Fowler & Foemmel 2000 | Correct | Add Booch (1991), who coined "continuous integration", and Beck's Extreme Programming (1999), to support the "1990s" in the heading. |
| 4 | Git short history | Correct | None. |
| 5 | GitHub protected branches | Correct | Cited inline in section 5, but only as a bare hyperlink; give it a number. |
| 6 | CNCF / OPA (Ahmed, 13 Aug 2020) | Correct; confirms "started in 2016" | Name the author. It is a guest post republished from the Magalix blog. Prefer OPA's own documentation or CNCF project page as the primary source. |
| 7 | NIST SP 800-204C (Chandramouli, March 2022) | Correct | The abstract does name policy as code and infrastructure as code, high security assurance and continuous authority to operate (C-ATO). But section 4's sentence "NIST later treated policy as code…" links to the CNCF post, not to NIST. Point it at reference 7. |
| 8 | NIST OSCAL | Correct | Add the version and date (OSCAL 1.0.0, 2021) so the "2020s" heading has an anchor. |
| 9 | OpenAI, "Using Goals in Codex" (Pathak & Fabbri, 9 May 2026) | Correct | The "compact contract" and six-element description are accurately paraphrased. Add the authors and date. |
| 10 | OpenAI, "Build iterative repair loops with Codex" (11 May 2026) | Correct | The page says "produce an output, validate it, and use the feedback to improve the next pass". The draft's "produce → validate → feedback → repair" is a fair paraphrase, but don't present the arrows as a quotation. |
| 11 | OpenAI, "Running Codex safely at OpenAI" (8 May 2026) | **Never cited in the text** | Either use it (sandboxing, approval policy, network allow-lists and audit logs map directly onto section 7's Authority, Execution and Evidence layers) or remove it. |
| 12 | OpenAI, "A Practical Approach to Verifying Code at Scale" (1 Dec 2025) | **Never cited in the text** | Use it in section 6. Its finding that an AI reviewer is a support for human judgement, not a replacement, fits the thesis. Or remove it. |

### In-text link problems

- **Section 4, "2010s – infrastructure as code"** cites Fowler's *Continuous Integration* article (current version revised January 2024). That article covers infrastructure as code only in a sidebar, so it is the wrong source for this milestone. Infrastructure as code also predates the 2010s: CFEngine (Burgess, 1993) and Puppet (2005). Cite Humble & Farley, *Continuous Delivery* (2010), and Morris, *Infrastructure as Code* (O'Reilly, 2016).

- **Section 4, "2025–2026 – agentic software engineering"** links only to the Goals cookbook, but describes both the Goals and repair-loop pages.

- **Sections 4 and 6** both state the Goals "contract" claim. Say it once (section 6 is the better place) and cross-refer.

### Single-vendor sourcing

Every source for the agentic part of the argument is an OpenAI cookbook or blog post. For a public-sector paper this reads as vendor-led and dates quickly. Add at least one independent or standards source. Candidates are the UK government *AI Playbook* (2025), NCSC secure AI development guidance, academic work on agent benchmarks or specification gaming, or a second vendor's agent-governance documentation. This will balance the argument.

### Gaps in the lineage that a reviewer will expect

For a meeting paper, add only items 1, 2 and 5, one line each in the appendix lineage table. Keep the rest for a later, longer version.

1.  **Safe regression test selection.** The GIS AI-GO router *is* regression test selection: choose which checks to run from the changed files. The promotion criterion "no false negative against the complete checks" is the textbook definition of a *safe* selection technique (Rothermel & Harrold, 1997). Industrial examples include Google's TAP and Meta's predictive test selection (Machalica et al., 2019). This is the most important missing citation, because it shows the safety argument has a known theory.

2.  **Fail-safe defaults.** "Unknown paths fail closed" is Saltzer & Schroeder's principle of fail-safe defaults (1975). Their "complete mediation" and "separation of privilege" principles also support section 5.

3.  **Trusting the governor.** The rule that a policy must not govern its own introduction echoes Thompson's "Reflections on Trusting Trust" (1984), and the general bootstrapping problem of trusted bases.

4.  **Supply-chain provenance.** The repository already has provenance and attestation lanes. SLSA, in-toto and Sigstore are the "evidence as code" lineage for the "Evidence and lifecycle" layer.

5.  **Rules as Code.** For a UK public-sector author and audience, the closest relative of governance as code is Rules as Code: OECD OPSI, *Cracking the Code* (2020), New Zealand's Better Rules, and the Catala language. Leaving it out will stand out to DSIT and GDS readers. It also links naturally to your OKF legislation work.

6.  **"Code is law".** Lessig (1999) is the standard reference for the idea that software architecture regulates behaviour. One sentence would place the paper in the governance literature, not only the engineering one.

7.  **Prior uses of the phrase.** "Governance as code" and "compliance as code" are already used in cloud governance (for example Chef InSpec, HashiCorp Sentinel, Azure Policy). A sentence acknowledging prior usage, and saying how your definition differs, guards against a charge of coining an existing term.

## Argument, structure and audience

The argument is sound, but it is weaker than it could be in three places. The definition of governance as code shifts. The case study never shows an agent. And the document has not decided whether it is a paper or a briefing.

### A1. Pin down one definition and one test

Governance as code is defined three times, with three different boundaries:

- The working thesis: rules, authorities, gates and evidence turned into mechanisms.

- Section 2: the system governing the policy itself.

- Section 5: "the point at which policy-as-code starts to become governance-as-code" is when governance logic is version-controlled.

The section 5 version is too weak. Most OPA deployments already keep policy in Git behind CI, so by that test all policy as code is governance as code. Choose one boundary. I suggest: *policy as code becomes governance as code when the mechanism also encodes who may change the policy, under which policy that change is judged, what happens under uncertainty, and what evidence survives*. Then apply it as a checklist in section 3.6.

### A2. Connect the case study to agents

Sections 6–8 are about coding agents, but section 3 never mentions one. Two easy fixes:

- **Provenance.** The repository has an AGENTS.md. If the routing code, map or tests were written or changed by a coding agent, say so and describe the human role. That turns the case from illustrative into evidential.

- **The agent-specific risk.** The strongest reason agents make meta-governance urgent is *specification gaming*: an agent under pressure to turn CI green may weaken a test, relax a rule or edit the workflow. The global-assurance-control rule and the trusted-base design are a direct defence against that. The M3 experiment shows the attack path concretely. Section 8 currently explains novelty through "the producer is now a probabilistic system", which is weak: human authors are not deterministic either. The new elements are generation rate, correlated failures across many changes, and an author that can reach its own checks.

### A3. Be honest about separation of duties

Section 5 says repository rules can encode that "the producer of a change is not the sole authority". In GIS AI-GO, .github/CODEOWNERS is \* @chris-page-gov: one owner for every path. Branch-protection and ruleset settings live in GitHub settings, not in version control, so the paper cannot show them. The design document itself lists CODEOWNERS protection of workflow ownership as a pre-enforcement requirement (line 107).

This is a real **limitation of the case**, and it also illustrates a general point. The outermost enforcement point, the required assurance status check, is configured *outside* the code. That is a gap in governance as code which most real deployments share. It deserves a paragraph, and it is a good reason to recommend exporting rulesets as code.

### A4. Add the missing sections

- **Purpose and ask.** The draft never says what it wants from the meeting: to note, to discuss, or to agree something. Put this at the top. If there is a decision to take, state it as a recommendation. Examples would be adopting the six-layer model, or applying the pattern to other repositories.

- **Limitations, as a short box.** This is one single-maintainer repository, in shadow mode only, with no shadow results yet, and branch protection sits outside the code. Saying this first protects the paper from the obvious challenge in the room.

- **Implemented vs designed table** (see M1). This table is what the meeting will most need to see.

### A5. Shape it for the meeting

As a meeting submission, the draft is about twice the length it needs to be, and its main point does not appear until page 5. Members usually read submissions quickly, often on screen just before the meeting. It also mixes three registers: an academic lineage (section 4), a business case (section 5) and a speaking script (section 9). A suggested shape, at 4–5 pages plus appendices:

1.  **Cover box.** Give the purpose (for information, discussion or decision), what you are asking the meeting to do, and a three-sentence summary. The section 9 script is close to that summary: move it to the front and correct it as described in M1.

2.  **The idea and the case (about 2 pages).** Cover the thesis, the section 2 table, the implemented-vs-designed table and the case study, with one short excerpt per point. Show the M3 re-routing scenario as the worked example of meta-governance.

3.  **Why agents change things (1 page).** Condense sections 6–8, keeping the contract table and the "new vs not new" table.

4.  **Limitations and the ask (half a page).**

5.  **Appendices.** Put the lineage (section 4) as an 8-row table, the business case (section 5), the full code excerpts, the Mermaid sources and the permalinks here.

Cut Figure 2, which repeats the table above it. Remove the Mermaid source blocks from the body entirely.

### A6. Smaller argument points

- **Figure 1 against section 4.** Section 4 says governance as code "is not one invention with a single origin", but Figure 1 draws a single linear chain ending at agentic engineering. That implies both a causal sequence and that governance as code came before agents. Redraw it as converging strands, or caption it "simplified; not causal".

- **Section 6, "read every line carefully".** The point is correct but slightly overstated. Mature teams already did not read every line; they relied on tests and review sampling. The shift is in degree, which the section 8 table says better.

- **Section 7, the six layers.** Good, but abstract. Map each layer to GIS AI-GO and mark what exists and what is missing. For example: Intent, the pull-request description and promotion gate; Authority, CODEOWNERS (one owner); Policy, the map; Execution, least-privilege Actions with SHA pins; Verification, 35 contract tests; Evidence, a 30-day artefact. The gaps then become the paper's recommendations.

- **Goodhart risk.** Once tests become the verification surface, they become the target. One sentence on this, and on the need for checks the producer cannot see or edit, would complete section 6.

## Figures, layout and document hygiene

The figures need resizing and one needs its logic fixed. The file metadata also needs cleaning before anyone outside receives it. The page references below are from an 11-page A4 render of the .docx.

### Figures

| Figure | Problem | Fix |
| --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 (p.1) | Scaled to a 0.4-inch-high strip, so the node text is unreadable in print. It also implies a linear causal chain (A6). | Use a top-to-bottom or two-row layout at full width, or a timeline. |
| 2 (p.2) | The opposite problem: three boxes take more than 6 inches, most of a page, and the bitmap looks soft. It also repeats the table directly above it. | Cut it, or shrink it to about 2 inches. The table already makes the point. |
| 3 (p.4) | The rendered image says "plan_ci_impact.py closed validation + classification", but the Mermaid source printed under it says only plan_ci_impact.py, so they disagree. The text is tiny. The figure is split from its caption across pages 4–5. | Regenerate it from the source shown. Keep it with its caption. Add the failure branch: planner error leads to a failed job, which blocks merge. |
| 4 (p.5) | Wrong logic (M4). | Redraw as two lanes. |
| 5 (p.8) | Readable, but its Mermaid source splits across pages 8–9. | Move the sources to an appendix. |

Also export all figures as SVG or high-resolution PNG at a consistent text size, around 9 pt when printed.

### Layout

- **Mermaid source blocks** after every figure add about two pages and break the reading flow. Put them in an appendix, or link to .mmd files in the repository.

- **Code excerpts** carry line numbers as text inside the code. That's fine, but it makes the off-by-two in M5 easy to introduce. Generate the excerpts from the pinned commit with a script, which would itself be a nice piece of evidence-as-code.

- **Headings.** Section 5's subheadings are Heading 3 directly under Heading 1, skipping level 2. This breaks the navigation pane and any generated table of contents. Section 4's milestones are bold paragraphs, not headings, so they don't appear in navigation either.

- **Empty horizontal-rule tables.** Several one-cell empty tables are used as separators after figures and code. Screen readers announce them as tables. Use a paragraph border instead.

- **Raw URLs.** Repeated 120-character permalinks in the body and in Appendix A take up a lot of space. In the body, use short link text, for example "ci.yml L58–65 @ 97bc456", and keep full URLs only in Appendix A.

- **Section 6.** The two OpenAI links sit as orphan lines after the paragraph. Fold them into numbered citations.

### Accessibility (public-sector requirement)

- None of the five images has alt text. That fails WCAG 2.2 success criterion 1.1.1, which UK public-sector bodies must meet under the 2018 accessibility regulations if the document is published.

- The colour-coded callouts (blue thesis box, cream meeting box) need contrast checking.

- Tables need header rows marked as headers so they repeat across pages and are announced correctly.

### File metadata: fix before sharing

- docProps/core.xml gives the author as **"python-docx"**, the description as "generated by python-docx", an **empty title**, and created and modified dates of **23 December 2013**. Set the title, author, organisation and real dates.

- There is no version or status marker such as "Draft v0.x – not for circulation", and no author name or affiliation on the title page. Both are expected for a case study that cites a named public repository.

- The footer is fine. If it will be printed, consider adding page numbers.

## Minor and line-level edits

These are small fixes, in document order.

| Where | Current text | Suggested change |
| ------------------------------ | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Subtitle | "with immutable GitHub references" | Commit permalinks last only as long as the repository and commit stay reachable; a rename, deletion or history rewrite breaks them. Say "commit-pinned", or archive the commit with Software Heritage (SWHID) or a Zenodo DOI and cite that. |
| Sec. 1, para 1 | "protected branches encode approval conditions" | Fine. But this lineage list leaves out formal contracts, which then lead Figure 1. Keep the two consistent. |
| Sec. 1, para 3 | "tests hostile and unknown cases" | "Hostile" overstates one mutation test and some path-safety tests. Use "tests mutated, malformed and unknown cases". |
| Sec. 1, para 3 | "explicitly designs against a proposed policy governing its own change" | Accurate. Keep this wording and copy it into section 2 and section 9 (M1). |
| Sec. 2 table | "evidence is retained" | "evidence is recorded (30-day retention)" (M7). |
| Sec. 3 intro | "line references remain stable even when the default branch moves on" | Add: "The pinned commit (2 October 2026) was the head of main when checked on 13 October 2026." |
| Sec. 3.1 | "protected-main pushes require exact-commit full assurance" | Clarify that this is a planner rule, not GitHub branch protection: "pushes to main". Branch protection is not evidenced in the repository. |
| Sec. 3.1 | "covers the workflow, planner, its contract tests and core toolchain files" | Add "…and, through .github/\*\*, the impact map itself". |
| Sec. 3.2 | "refuses to accept a map that weakens the safety defaults" | "refuses a map that changes the three top-level safety defaults or lets a force-full rule select fewer than every lane" (M3). |
| Sec. 3.3 heading | "tested adversarially" | "tested against mutation and unknown inputs". "Adversarially" suggests red-teaming. |
| Sec. 3.4 | "Only a successfully produced, type-checked Boolean plan can change the recommendation" | Add: "…and the recommendation is not yet consumed by any job" (design doc lines 52–53, 135–137). |
| Sec. 3.5 heading | "the policy must not govern its own introduction" | Good. Add "(designed; not yet implemented)". |
| Sec. 3.5 | "becomes authoritative only after passing the existing policy's full checks and merging" | "…merging and passing exact-main verification". |
| Sec. 3.6 table | "Policy as code: the system evaluates which controls apply" | Add "(here: recommended, not yet applied)". |
| Sec. 4, 2010s | "DevOps and continuous-delivery practice generalised…" | Re-source (see Citations). |
| Sec. 4, 2016 | "popularised a general-purpose model" | Fine. Optionally add XACML (OASIS, 2003) as an earlier declarative policy standard. |
| Sec. 5 | "### Consistency" and the other subheads | Promote to Heading 2 (5.1–5.6) for consistent numbering. |
| Sec. 5, continuous assurance | "NIST SP 800-204C explicitly links…" | Add the reference number \[7\]. |
| Sec. 5, last para | "deployments and restrictions on who may push" | GitHub's wording is "require deployments to succeed before merging". Also add "rulesets", which have largely superseded classic branch protection. |
| Sec. 6 | "OpenAI's 2026 Codex guidance makes the connection explicit" | "…describes a Goal as a compact contract". The connection to Design by Contract is the author's, not OpenAI's. |
| Sec. 7 | "six coupled governance layers" | Say whether this model is original to the paper or adapted from elsewhere, and cite it if adapted. |
| Sec. 8 | "The producer is now a probabilistic system" | See A2: lead with rate, correlated failure and the author's ability to reach its own checks. |
| Sec. 9 | Whole script | Rewrite per M1. Keep it under 90 words for speaking. |
| Sec. 10 | Mixed citation style | Use one style throughout, author–date or numbered. Add accessed dates for web sources, and DOIs where they exist. |
| Throughout | Spelling | British spelling is consistent (artefact, organisation, judgement). "Fail-full" and "fail closed" are both used; define "fail-full" once. |

## Revision plan

This plan is ordered for a meeting submission. The first group fixes accuracy. The second makes the paper shorter and sharper. The third can wait if time is short.

**Before submission (accuracy)**

- [ ] Add an "Implemented vs designed" table and correct the present-tense claims in sections 1, 2, 3.5, 3.6 and 9 (M1)

- [ ] Quote design-document lines 98–107 in full, including "Before enforcement" (M2)

- [ ] Qualify the section 3.2 claim and add the re-routing scenario as the worked example (M3)

- [ ] Redraw Figure 4 as two lanes: per-pull-request routing and policy lifecycle (M4)

- [ ] Fix workflow excerpt line numbers to 58–65, show line 22, and make every link range match the lines shown (M5, accuracy table)

- [ ] Fix file metadata (author, title, dates) and add author, version and status to the title page

**Before submission (shape it for the meeting)**

- [ ] Add a cover box with the purpose, the ask and a three-sentence summary, and move the corrected meeting script there (A4, A5)

- [ ] Cut the body to 4–5 pages: condense sections 1–3, compress 6–8 to one page, and move sections 4 and 5, the Mermaid sources and the full permalinks to appendices (A5)

- [ ] Drop Figure 2, resize Figures 1 and 3, and regenerate Figure 3 from its source

- [ ] Add a short limitations box (A3, A4)

- [ ] Add one paragraph on what is being traded, plus the promotion gate as a short list (M6)

- [ ] Correct the retention claim (M7)

- [ ] Use one definition of governance as code throughout (A1)

- [ ] Add one paragraph linking the case to agents: who wrote the code, and specification gaming (A2)

**If time allows**

- [ ] Map the six layers onto GIS AI-GO as a table that also lists the gaps, which can double as the recommendations (A6)

- [ ] Add safe regression test selection, fail-safe defaults and Rules as Code to the appendix lineage table; re-source the infrastructure-as-code milestone; cite or drop references 11–12; add one non-vendor source

- [ ] Fix heading levels and separator tables, and add alt text and table header rows (required if meeting papers are published)

## Sources checked

The repository was fetched at commit 97bc45635a91064cd78f06bf0848ad7636f05439, and its 35 routing contract tests were run (all pass). The draft was rendered to 11 A4 pages for the layout review.

Repository files, all at that commit:

- [.github/ci/verification-impact-map.v2.json](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/.github/ci/verification-impact-map.v2.json)

- [scripts/plan_ci_impact.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/scripts/plan_ci_impact.py)

- [tests/contract/test_ci_impact_plan.py](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/tests/contract/test_ci_impact_plan.py)

- [.github/workflows/ci.yml](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/.github/workflows/ci.yml)

- [docs/implementation/CI_IMPACT_ROUTING.md](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/docs/implementation/CI_IMPACT_ROUTING.md)

- [.github/CODEOWNERS](https://github.com/chris-page-gov/gis-ai-go/blob/97bc45635a91064cd78f06bf0848ad7636f05439/.github/CODEOWNERS)

Web sources opened:

- [Using Goals in Codex](https://developers.openai.com/cookbook/examples/codex/using_goals_in_codex) (OpenAI, 9 May 2026)

- [Build iterative repair loops with Codex](https://developers.openai.com/cookbook/examples/codex/build_iterative_repair_loops_with_codex) (OpenAI, 11 May 2026)

- [Running Codex safely at OpenAI](https://openai.com/index/running-codex-safely/) (OpenAI, 8 May 2026)

- [A Practical Approach to Verifying Code at Scale](https://alignment.openai.com/scaling-code-verification/) (OpenAI, 1 Dec 2025)

- [NIST SP 800-204C](https://csrc.nist.gov/pubs/sp/800/204/c/final) (NIST, March 2022)

- [Introducing Policy As Code: The Open Policy Agent](https://www.cncf.io/blog/2020/08/13/introducing-policy-as-code-the-open-policy-agent-opa/) (CNCF, 13 Aug 2020)

- [NIST OSCAL](https://pages.nist.gov/OSCAL/)

- [Continuous Integration](https://martinfowler.com/articles/continuousIntegration.html) (Fowler, revised Jan 2024)

- [Meyer publications by date](https://se.inf.ethz.ch/~meyer/publications/index_date.html) (the 1986 note could not be found)

The suggested additional references (Floyd, Booch, Rothermel & Harrold, Saltzer & Schroeder, Thompson, Lessig, Humble & Farley, Morris, OECD OPSI, SLSA, Machalica et al.) are standard works cited from general knowledge. Check their exact bibliographic details before adding them.
