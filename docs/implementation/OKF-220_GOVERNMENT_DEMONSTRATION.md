# OKF-220: government demonstration rehearsal

Prepared on 2 October 2026. This is a rehearsal plan, not a record of completed
Voice integration, deployment acceptance or government service accreditation.

## Purpose and boundaries

Show colleagues how a geospatial question can lead to a bounded source search,
an explicit interpretation and an inspectable evidence receipt. Use native
desktop Voice for the conversation, the existing owner-private Sites pilot for
its admitted open-data functions, and local OKF+ retrieval for metadata and
source discovery. The presenter operates the desktop and shares only cleared
public-data results; colleagues do not need accounts or access to the private Site.

The native Voice-to-tool path and installed Ask OKF admission of this inventory
remain unverified. Until demonstrated, say when the presenter manually runs a
search or selects a Site control. Local context compatibility does not establish
installed connector access: see the [Ask OKF integration boundary](OKF-220_ASK_OKF_INTEGRATION.md).
Use the [private pilot checkpoint](SITES-218_PRIVATE_MCP_PILOT.md) and
[hosted observation](SITES-218_HOSTED_OBSERVATION.md) for existing evidence,
without presenting historical results as fresh calls.

## Preflight with the owner present

1. Test the microphone, speaker, mute and stop controls with a short,
   non-sensitive conversation. Resolve any operating-system or application
   permission prompt while the owner is present. Do not leave an unattended
   permission-dependent test running.
2. Open the existing private pilot through the owner's normal signed-in route.
   Check the admitted capabilities, current revision and remaining provider
   allowances against the private operating record. Do not widen its audience,
   reset allowances or put credentials into a browser prompt or presentation.
3. Prepare the current local search index and inspect its verification report.
   The [OKF+ instructions](../../okf-plus/README.md) describe the offline build
   and check. Keep a clearly dated, cleared retained-result example available if
   Voice, authentication or live access is unavailable.
4. Select the existing plan's Standard mode and a suitable economical model for
   routine retrieval where available. Do not buy credits, configure API billing
   or enable chargeable overage for this rehearsal.

## Three ten-minute rehearsals

Use two minutes to introduce the question, six minutes to demonstrate and two
minutes to record evidence and corrections. Run each rehearsal once before
deciding whether a repeat would answer a specific outstanding question.

| Rehearsal | Concrete questions and actions | Evidence and limit |
| --- | --- | --- |
| 1. Find the right source | “What does OS Open Names provide?” Then “Where is NGD address-classification label `ZW99TP` documented?” Ask which retrieved facts describe release cadence and which describe temporal coverage. Run local OKF+ search and inspect the linked native metadata. | Zero provider calls. Preserve native identifiers, source links, coverage gaps and the distinction between a documented label and an asserted API enumeration. A metadata answer does not provide a licensed feature. |
| 2. Explain a place match | “Which named places match Warwick?” Use OS Names with at most five candidates. Then “Which MSOA 2021 names start with Warwick?” Use ONS area-name lookup with at most five results. Inspect a result receipt. | At most two provider attempts if the existing live preflight admits them. Name matching is not point containment or an exhaustive list of areas covering the town. Show candidate type, native code, CRS where returned, and any incomplete-result flag. |
| 3. Compare a statistic and refuse an unsupported inference | “Compare the UK CPIH index in January and July 2026.” Inspect native series, months, units and receipt. Then ask “Does that measure inflation in Warwick?” and explain why the supplied evidence cannot answer that. Show the protected-capability boundary without requesting protected payloads. | One CPIH comparison may require two upstream attempts. National CPIH does not establish local inflation. A refusal must identify the missing evidence rather than invent a local estimate. |

This plan permits no new spending and proposes at most four upstream attempts
across the live portions, with no automatic retries. Follow the existing
[evaluation runbook](../operations/SITES_MCP_PILOT_EVALUATION.md) for admission
and a separate wire-request bound. Failed attempts can consume allowance. Use
clearly labelled historical evidence if the live preconditions are unmet.

An example local search, from the repository root:

```sh
uv run --locked --cache-dir .uv-cache python scripts/okf_plus/search.py \
  --index artifacts/okf-plus/bundle/search-index.json \
  --question "Where is the NGD address-classification label ZW99TP documented?" \
  --max-records 5 --max-bytes 65536
```

## Record useful measurements

For each question, record the source revision or index digest, input, selected
source, result or refusal, receipt reference, omissions and any presenter
correction. Time question end to visible result and question end to spoken
answer separately. Keep Voice time distinct from the typed-call measurements
produced by [`sites_mcp_evaluate.mjs`](../../scripts/sites_mcp_evaluate.mjs) and
its [question corpus](../../evaluation/sites-mcp-pilot-cases.v1.json).
That harness does not test natural-language understanding. Three rehearsals
cannot establish a latency service level or a meaningful tail percentile.

Keep private before/after usage readings, elapsed Voice minutes and concurrent
work notes; account-wide usage differences are not exact task costs. Publish
only cleared aggregate findings, without account details, tokens or private
payloads. Record whether each action was manual or actually invoked by Voice.
An eventual Voice acceptance test must demonstrate the invocation, input,
authenticated result and matching receipt, including an unsupported-question
refusal. Installed Ask OKF admission remains a separate test.

## Product and cost assumptions

Official guidance checked on 2 October 2026 prices native desktop Voice at
$0.05 per minute, or 1.25 credits per minute under the documented additional-credit
pricing. Thirty active minutes therefore represent 37.5 credits for Voice alone;
backend model work consumes additional usage. This is a planning calculation,
not a promise of an incremental bill. Sites is included for eligible plans during
the public beta, not a permanent production-hosting price commitment.
See [pricing](https://learn.chatgpt.com/docs/pricing) and
[native Voice guidance](https://learn.chatgpt.com/docs/features/voice).

Keep the first demonstration within the existing native application and bounded
retrieval. A custom [Live API application](https://developers.openai.com/api/docs/guides/live)
adds implementation work and separate [API billing](https://developers.openai.com/api/docs/pricing);
ChatGPT credits do not establish its funding. Dots is not a prerequisite:
the current [Dots access guidance](https://learn.chatgpt.com/docs/dots#access)
excludes the UK from personal Pro availability. Recheck product availability and
pricing before a later rehearsal rather than purchasing a different plan here.
