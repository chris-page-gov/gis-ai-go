# Completing the local candidate while hosting is unavailable

Work item: [LOCAL-214 #118](https://github.com/chris-page-gov/gis-ai-go/issues/118).

Plan date: 14 September 2026. Baseline:
`6c76c92a18da779766f8d49acbbd7dbbd31abb97`, containing the accepted LOCAL-212
runtime from `57e49322e305b499fccfbb6c46bc15e2a0ff38f9`.
Status: investigated and proposed for staged implementation; no release boundary
is changed by this document.

## What can be completed now

The repository already has a cloneable, client-connectable, provider-free exact-five
candidate. [LOCAL-212](../operations/LOCAL-212_CLEAN_CLONE_LOCAL_CANDIDATE.md)
documents the supported setup and the accepted test. One launcher starts the five
read-only tools and three resources on IPv4 loopback; it uses the checked catalogue,
an in-memory provider outage, an approved cache and private session evidence.

The next achievable outcome is an independently usable local evaluation edition:
a colleague can obtain an identified artefact, install its pinned prerequisites,
start it, complete a clear demonstration, inspect the evidence and stop it using
only the published instructions. Its results and limits must remain understandable
without this development conversation or the owner's external SSD.

That can be finished without Azure. The existing public `v0.2.0` definition also
requires deployment and rollback evidence, so local completion needs an explicit
additional release profile. Rewording a local result as a public deployment would
not satisfy those existing gates.

## Separate completion tracks

| Track | Completion claim | Needs paid hosting? |
| --- | --- | --- |
| Local evaluation edition | Exact-five provider-free journey, reproducible setup, client guide, evidence and teardown, clearly labelled data vintage | No |
| Local durable-service rehearsal | Single writer, persistent local stores, checkpoint/restore and restart evidence under a new explicit local profile | No; separate from the current disposable launcher |
| Supported public `v0.2.0` service | Public HTTPS, admitted live-provider path, operational ownership, deployment and rollback, Registry publication | Hosting authority and an operational envelope are still required |

The first track should finish before optional durable-service expansion. This
keeps the immediately useful colleague demonstration small and measurable.

## Stage L1: accept the local edition contract

Create an additive decision and work item defining a local evaluation release.
Preserve ADR-0015's existing provider-free launcher and the public release gate.
Recommended packaging is a GitHub prerelease such as `v0.2.0-local.1`, explicitly
excluded from the latest supported public release. The final tag spelling and
version policy must agree with repository version checks before publication;
this example is a proposal, not an existing tag.

Acceptance:

- the first page identifies the exact source commit, software version, target
  edition and supported operating systems;
- it states that data is a reviewed fixed observation, not a current statistical
  service, and that evidence survives only the current process session;
- local, public-service and future-platform claims each have a source and a status;
- the release contains no provider credentials, user-specific paths or dependence
  on an owner's preserved evidence store;
- a versioned local acceptance manifest records each required check and its
  evidence pointer; and
- no existing public-service issue is closed solely because local acceptance passes.

The current guide is for macOS or Linux. Windows is not a demonstrated support
claim. A Windows/WSL path can be added only with a corresponding real-machine test.

## Stage L2: close reliability and longevity gaps

The [runtime review](reviews/RUNTIME_REVIEW.md) identified local cache freshness
and duplicated readiness work as concrete follow-up areas. It also identified
a shorter provider deadline expiring while an admission lease is held; that needs
a focused regression and fix before an expanded live-provider profile. The approved cache
expires at `2027-02-20T20:21:08.947Z`. A useful local edition needs a visible expiry
and an owned renewal or synthetic-profile plan.

Acceptance:

- startup explains missing/wrong prerequisites and port conflicts in plain English;
- the three dependency alerts recorded in AUI-12 have an evidence-backed
  disposition, with a compatible tested update where required;
- readiness or a clearly separate local capability-health field explains cache
  expiry and preserves access to evidence recovery;
- tests cover before, at and after the expiry instant without changing the system
  clock or weakening historical approval;
- the first edition publishes its data validity window and renewal owner;
- a new synthetic learning profile, if chosen, has separate identifiers, fixtures,
  receipts and an accepted decision; it never silently substitutes for T04;
- failed startup, normal SIGINT/SIGTERM and repeated stop have predictable results;
- the guide explains abrupt-exit limits and does not promise crash cleanup or
  restart recovery for the disposable launcher; and
- the same five calls remain available through direct API and supported local MCP
  HTTP, with identical governed meaning and explicit cache provenance.

A live-provider profile on the user's own machine could be considered later under
existing provider-call authority. It still needs a separate reviewed entrypoint,
egress bounds, rights checks and observations. It is not required for the first
local edition and is not obtained by weakening the provider-free launcher.

## Stage L3: package and prove the first-run journey

Use the maintained `./scripts/start-local-candidate` command. Reduce repeated
build work only after measuring it; an unchecked stale `dist` directory must not
become the way to make startup faster. A prebuilt local artefact is useful only
when its complete source/build dependency closure is verifiable.

Acceptance:

1. Start with a clean checkout or downloaded source artefact at the release commit.
2. Install from lockfiles using documented Node.js, pnpm, Python and uv versions.
3. Build and start using the one published command, without development-agent files,
   provider credentials, a private cache or the external SSD.
4. Verify health and readiness, exactly five tools and three resource classes.
5. Complete search, describe, selection, query and receipt inspection from a
   separate local MCP client, retaining the client and protocol versions.
6. Independently verify result contracts, distinct receipts, query-to-inspection
   linkage and complete plain-text results.
7. Show missing constraints, refused arbitrary input, repeated idempotency key and
   a source/vintage warning so the demonstration explains failure behaviour too.
8. Confirm no provider transport egress in the documented evaluation path, stop
   cleanly, verify temporary-state removal and confirm tracked files are unchanged.

Record cold install, cold start, warm start and five-call latency separately, with
hardware/runtime information and unavailable values marked. Test on current macOS
arm64 and one Linux environment before claiming both; reuse current CI evidence
where it proves the exact release artefact. Do not rerun live AI observations for
unchanged documentation. Repeat only where a changed client, protocol, schema or
entrypoint invalidates the existing evidence.

## Stage L4: make the demonstration teachable

Build a learning path that begins with a successful five-call journey, then explains
the machinery used to make it trustworthy:

| Learner question | Demonstration or explanation |
| --- | --- |
| What does my AI do? | It translates the question into tool arguments; deterministic code selects and processes approved data |
| What is a contract? | A versioned agreement about permitted input, result and error shapes, illustrated by one accepted and one rejected call |
| What does governance as code mean? | Show the server-owned authority context, the rule that allows the operation and the obligations carried into its receipt |
| Why does the tool refuse a request? | Show missing constraints, denied operation, provider suspension and evidence failure as distinct causes |
| What does a receipt prove? | Recompute its content identity and explain that a digest is neither a digital signature nor a claim that the data is current |
| How did agents write the code? | Link the chronicle's parent/child task records, bounded delegated work, review and integration evidence |
| Why are there many tests and scans? | Connect unit, contract, integration, adversarial, security, dependency and browser checks to different failure modes |
| What remains before public service? | Follow the separate public deployment track and show the difference between local evidence and public operational evidence |

The figures should use one question or boundary per diagram, a portrait-A4 text
area of approximately 170 by 247 mm, vector artwork, readable text at final print
size and captions that state the evidence boundary. Split wide flows into stacked
figures. Include a print review at 100% scale; a large on-screen SVG alone is not
proof that the printed diagram is legible. Screenshots must identify client
version and step, omit private information and have explanatory alternatives.

## Stage L5: complete review and publish the local edition

The full code review requires every maintained runtime, front-end, schema,
assurance and operational-script file to have a completed review disposition.
The runtime report covers all 80 maintained source files and explicitly
distinguishes complete-file reading from critical-path inspection. Use that
coverage register with the companion reviews; do not convert it into a claim
that every line of the whole repository was audited or all defects eliminated.
Confirmed blockers need fixes or an explicit bounded support limitation with
tests before the edition is described as ready.

Acceptance:

- the documentation and local acceptance manifest refer to the same immutable
  source/build artefact;
- all required changed-path and release-profile checks pass on protected main;
- a clean-clone reviewer can finish the walkthrough without author assistance;
- the public chronicle includes both successful controls and the measured cost of
  failures, retries, CI waiting and model changes where records permit;
- publish the local prerelease, checksum ledger, beginner walkthrough, A4 PDF and
  source/evidence index together; and
- record the local completion decision while leaving public deployment gates open.

## Later optimisation stage

Modularisation and optimisation are a separate stage after the first usable
edition, apart from defects that prevent its promised journey. Implement the
ordered plan in the runtime review and the other component reviews. Establish
measured baselines before changing caching or validation, preserve byte-identical
contracts and receipts where required, and record the original/resulting code and
costs in the chronicle. This is how the narrative can show learning from the
development process rather than simply celebrating the amount of work.

## Public hosting work that remains external

Public DNS/TLS, a provider/hostname, a numeric budget where applicable, operational
ownership, live-provider deployment evidence, remote direct-HTTP interoperability,
workload trust, governed storage, monitoring and real deployed rollback remain
separate. Local simulations and current tunnel evidence can prepare those tasks;
they cannot manufacture the missing public-service observations. The exact
five-tool assembly and retained contracts are reusable when that environment is
available.
