# Policy-test boundary

The accepted local implementation has compiled, default-deny public policies in
[`packages/policy-client`](../../packages/policy-client/). Its tests cover the
catalogue policy, public-read v2 operations and evidence-inspection v3:

```bash
pnpm --filter @gis-ai-go/policy-client run test
```

These tests also run through the complete repository check. Related gateway and
execution-service tests exercise enforcement at the operation boundaries.

An external OPA/Rego policy decision point, enterprise identity and protected-tier
policy integration remain future work under the
[roadmap](../../docs/implementation/ROADMAP.md). Passing the local policy suite
does not establish any of those integrations. Current acceptance and release
boundaries are recorded in [`PROGRESS.md`](../../PROGRESS.md).
