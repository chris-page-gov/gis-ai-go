# Gateway validator dependency repair

Review date: 24 October 2026. Related work:
[issue #153](https://github.com/chris-page-gov/gis-ai-go/issues/153) and
[PR #182](https://github.com/chris-page-gov/gis-ai-go/pull/182).

The mandatory gateway image job reached `vulnerability-policy` and failed closed
at the previous candidate. That stage runs after scanner, database, report,
coverage and Node advisory validation; it rejects any retained High or Critical
finding with an available fix. The failed job did not publish its gateway scan
artefacts, so its exact Trivy finding list is unavailable. No stale report is
promoted to acceptance of the changed lockfile.

An independent official production registry audit identified Zod `4.4.3` on the
gateway's `@modelcontextprotocol/server` dependency path as High under
[GHSA-mrhx-c7xc-m3w5](https://github.com/advisories/GHSA-mrhx-c7xc-m3w5)
and `CVE-2023-54404`. The advisory, updated on 23 October, marks versions below
`4.6.6` affected and `4.6.6` fixed. Oversized constrained collections can reach
element validation before their size admission, accumulating unnecessary work.
The server's declared `zod: ^4.2.0` range admits the patch.

The workspace now pins Zod `4.6.6` through its existing reviewed override method.
The regenerated lock retains exact package integrity and changes no server,
adapter, client or image base pin. All resolved Zod copies follow the same fixed
version. The regression loads the validator through the server's own dependency
resolution and requires a constrained oversized array to be refused before its
element transform runs, while a valid array still runs that transform normally.
Existing body and SDK argument-element limits remain required and unchanged.

The post-update official production audit reports zero High or Critical findings.
It still reports two Moderate findings: Hono `4.13.7` in the gateway adapter and
MCP client `2.2.0` in the separate public-data workbench. They remain explicitly
outside this High-finding repair; this audit is neither a claim of complete
vulnerability absence nor a substitute for the image's current Trivy/Node scans.

The managed environment's Red Hat registry request is denied by its HTTP policy,
so a fresh exact image build cannot be claimed from this environment. Canonical
GitHub Actions must rebuild, scan and verify the final image before merge under
the existing gates. No vulnerability threshold, retained finding, scanner,
publication rule or evidence-privacy control is weakened.

Local verification passed the new effective-validator regression, all 360 existing
gateway unit cases and the separate launcher lifecycle acceptance. The first unit
run exposed the checkout's restrictive launcher mode; restoring Git's declared
`0755` mode fixed that case without changing source. The lifecycle check also
required the existing pinned pnpm `10.33.2` and uv `0.12.2` executables on its
isolated path. No tool version guard was relaxed.

The canonical local receipt generator re-executed its seven deterministic cases;
its lockfile binding and derived set identity were refreshed. The 98 repository
boundary, gateway-image contract and local-receipt checks passed. Changelog
validation accepted all 143 fragments, and the diff passed whitespace checks.
The initial registry audit identified one High finding; the new audit records
zero High/Critical findings and the two separate Moderate findings described above.

The next canonical repository run exercised 1,673 Python tests and identified one
missed review binding: the strict-modern test still pinned the prior regenerable
local receipt. Independent comparison confirmed that only the lockfile hash and
derived set ID changed. The regenerable receipt pin was refreshed to its actual
SHA-256, `c47248aa090d61877aa83740772c1690fe7a6b120641ca40a549a534de897ea4`.
Historical evidence maps, classifications, claims and recorded outcomes remain
unchanged; no receipt was edited to satisfy this guard.
