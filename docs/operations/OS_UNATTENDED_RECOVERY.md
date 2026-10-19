# Bounded unattended OS metadata recovery

Run the supervisor in the managed workspace:

```sh
python -m scripts.okf_plus.recovery_run --max-wall-seconds 28800
```

It can continue without an open laptop while its workspace process remains alive.
Closing the laptop is not evidence that the process or workspace will survive.
The supervisor cannot prevent suspension, termination or expiry of the execution
environment. It makes no promise of completing overnight.

The default wall budget is eight hours; the maximum is 86,400 seconds. Writer
checks normally occur every 30 seconds, with waits capped at 60 seconds. Wall
budgets are checked between phases and before capture. Existing capture calls
have their own bounded request deadlines; a running local verification or export
phase finishes or fails before the next supervisor wall-budget check. These are
operational bounds, not an operating-system lifetime guarantee.

The supervisor takes its own single-writer lock and observes the documentation
writer's lock. It never deletes, overrides or takes over another writer's lock.
An existing writer can finish independently. Once that lock is free, the
supervisor reads the current checkpoint and recomputes requested, processed,
captured, failed and unresolved document counts from the frozen target list.

When unresolved targets remain, it invokes only the existing documentation sync
with a cumulative ceiling of 3,000 requests, at most 2,303 attempted documents per
batch and a deadline of at most one hour per call. It only resumes a checkpoint
whose stop reason is empty, a wall deadline or a document batch ceiling. A prior
429, another stop reason or a batch that makes no unresolved-target progress
blocks further capture. Known failed request receipts are reused without another
network attempt. It does not retrieve OS feature datasets or read credentials
itself; the existing documentation capture uses its established fixed routes.

Once unresolved targets reach zero, known failures remain failures. The
supervisor verifies every captured raw response's checksum and exact passage
reconstruction, then exports source field cards and all-collection candidate
passage links. Each invocation uses a new final output directory; existing final
exports are not overwritten. A run with captured documents and known HTTP 307 redirect failures
finishes as `finished_partial`, not as complete source coverage. The regression
suite also exercises a synthetic cohort of 307 failed documents; that count is a
test fixture, not a claim about the live capture.

Receipts and exports remain beneath the ignored private directory:

```text
artifacts/okf-plus/private-recovery-supervisor/
  checkpoint.json
  supervisor.lock
  run-<unique-id>/
    receipt.json
    field-cards/
    field-passages-final/
```

Before capture or auditing, the checkpoint scope must exactly match the current
frozen source indexes. A changed source scope fails without promoting a saved
completeness claim or modifying documentation evidence.

Each phase records source HEAD, counts or verification/export evidence and private
output locations. Supervisor receipts are written by atomic replacement with file and parent
directory synchronisation. An audit
or export failure leaves the documentation checkpoint and previous evidence
available; the private receipt records the exception type. No support message is
sent and no private output is published to GitHub.

To inspect progress, read `checkpoint.json` and the source documentation
checkpoint at `artifacts/okf-plus/private-os-documents/checkpoint.json`. A saved
status describes the last recorded state; it does not prove that a process is
still running. Check the process in the workspace separately.

After a process stops, use the same command to resume. A currently active
supervisor refuses a duplicate start. A new invocation rereads the source
checkpoint and uses a new immutable output directory; known non-resumable stops
still need review rather than blind retries. The optional output schema is
`okf-plus/schemas/recovery-supervisor.schema.json`; offline regression tests are in
`tests/contract/test_okf_plus_recovery_run.py`.
