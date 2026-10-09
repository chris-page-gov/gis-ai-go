# GCP-222 observed local results

Observed on 5 October 2026 in the existing authoritative checkout, branch
`codex/gcp-private-pilot`, based on
`97bc45635a91064cd78f06bf0848ad7636f05439`. The implementation is an uncommitted
working-tree increment. No GCP cloud mutation, publication or owner approval of
the first mutation has occurred. There is no observed GCP website or MCP URL.

## Implemented and exercised

The additive entrypoint serves the current portal, Explorer, workbench, OKF/OKF+
knowledge surfaces and six custom Streamable HTTP MCP tools. The deployment
contract provides the ten requested lifecycle commands, private Cloud Run,
private API/DNS routing, an on-demand personal access VM, durable evidence
operations and a separate BDUK profile consuming approved platform resources.
Transport authentication, human OIDC identity and application policy are distinct.
The browser OIDC implementation uses pinned `openid-client` 6.8.8; actual Google
or Okta sign-in has not been observed.

| Check | Observed result | Evidence under `artifacts/gcp/` |
| --- | --- | --- |
| Final focused command `pnpm run test:gcp` | PASS: 26 runtime, 66 Python lifecycle/proxy/verifier and seven packaging/UI tests | `gcp-final-check-20261005.log` |
| Terraform formatting, init without backend and validation | PASS: four environment roots and two modules | `terraform-final-20261005/results.json` |
| Terraform mocked plans | PASS: two foundation and five service cases; no real cloud plan | `terraform-final-20261005/11.log`, `14.log` |
| Fresh full OKF+ build verification | PASS: 30,833 retained representations, zero omissions; four interpretation questions remain unassessed | `metadata-final-20261005/okf-plus/verification.json` |
| Actual full release HTTP, proxy and MCP | PASS: 36 OKF and 30,833 OKF+ representations, six SDK tools, release resource, matching web/MCP records and full export | `1784b702d63d0ba7/full-release-http-mcp-local.json` |
| Complete OKF+ JSON through actual Python proxy | PASS: 189,929,585 bytes, matching SHA-256; bounded streaming | Same full-release evidence |
| Local OCI identity | PASS: loaded image config/root filesystem matches the accepted OCI archive | `1784b702d63d0ba7/local-image-identity.json` |
| Final container boot | PASS: UID 65532, read-only, no network, enforced 2 GiB, 8.45 seconds startup, RSS 788,836 KiB, no OOM, clean SIGTERM exit | `1784b702d63d0ba7/local-image-boot.json` |
| Existing browser assertions using Chromium | PASS: 27 Explorer, 11 WebMCP and 20 offline experience journeys | `browser-supplement/`, `experience-browser-chromium/report.json` |
| New portal/knowledge browser journeys | PASS: nine journeys including refusal, keyboard, mobile/doubled text and automated accessibility checks | `browser-local-20261005-fixed/report.json` |
| Regenerable local receipt binding | PASS: 33 targeted tests after the authorised package/lock binding refresh; receipt bodies and claims unchanged | `qual-material-final-20261005.log` |

The full-release harness uses signed synthetic RSA/JWKS identities and mocked
atomic storage through isolated constructor seams. Its upstream TLS seam is
local. It made no external provider/model calls or evidence writes. The real
container's neutral configuration returns liveness 200 and readiness/content/MCP
503 until its real deployment identity and store bindings are established.
These observations prove local packaging and behaviour, not hosted privacy,
authentication, durable persistence or BDUK acceptance.

## Required assurance still open

The final canonical `pnpm run check` exited 1: Python ran 1,114 tests with eight
failures, one error and seven skips, after passing type checking, TypeScript and
interoperability stages. One stale regenerable receipt hash caused by the
authorised dependency change was then corrected and its 33 targeted tests passed.
The full canonical command was not repeated after that correction.

The other failures remain observed: recovery fixtures cannot create an output
outside any checkout because this sandbox exposes `.git` markers at both writable
roots; executable observer tests encounter Darwin inode mapping and process
termination differences; a strict collector rejects non-unique source hardlinks
in this checkout. The guards were preserved. The existing execution-container
check separately failed in this environment's Docker setup; it is not the new
Cloud Run image test. Canonical CI remains an outstanding release gate.

The canonical browser command requires `/opt/google/chrome/chrome`, which is
absent. Its 27 checks failed before assertions. Supplemental Chromium configuration
preserved and passed all 38 Explorer/WebMCP assertions; the 20 offline experience
journeys also passed using the existing supported Chromium option. This does not
claim that the canonical Chrome command passed.

Remaining canonical stages were exercised individually: Sites pilot (47), Explorer
unit tests (101), local client, experience/intake, geo execution (22), release
reproducibility, versions, public-read, contracts, links, diagrams and SBOM passed.
Changelog and secret scanning initially found new-change issues; both were fixed
and rerun successfully. Logs retain both initial and corrected outcomes.

## Immutable local material

The accepted output directory is `artifacts/gcp/1784b702d63d0ba7/`.

- Release ID: `e1223d0f47deb2f73d554404d02a42ebf0cd9bad68be86efd15a4b50688c289b`.
- OCI digest: `sha256:3ef00620adfc26290444eec5fd7d7c60abbf1274c79c28b4e90615a99a188a4f`.
- Manifest SHA-256: `c2f0abcf23829b5de92ff2fba2e9fae509c49542edae06d7a4f177d535e42079`.
- Allowlisted material: 33,389 files, 869,112,769 bytes; OCI archive: 311,709,696 bytes.
- Initial data: admitted public metadata and synthetic fixtures. Credentials,
  licensed feature payloads, private original-document archives and protected
  BDUK data are excluded. Nothing was uploaded to GCP.

`platform-review.zip` and its adjacent `.sha256` are generated by
`package-approval`. The ZIP contains sanitised implementation, executable scripts,
policy, pinned locks, acceptance requirements, inventory and local observations.
Follow its `SOURCE_REPLAY.md`: obtain the pinned public base and overlay the
reviewed GCP application/deployment material. It is a review overlay, not a full
checkout, OCI image or private archive. It does not reproduce every unrelated
canonical test fixture. Original working-source/build hashes and hashes of the
post-redaction ZIP files are distinct evidence.

## Read-only cloud inspection and exact gates

The exercised commands used the existing owner-private configuration:

```sh
./scripts/gcp/deploy.sh --config artifacts/gcp/personal-config.json preflight
./scripts/gcp/deploy.sh --config artifacts/gcp/personal-config.json plan
./scripts/gcp/deploy.sh --config artifacts/gcp/personal-config.json status
./scripts/gcp/deploy.sh --config artifacts/gcp/personal-config.json verify
./scripts/gcp/deploy.sh --config artifacts/gcp/personal-config.json package-approval
```

Preflight and plan are blocked (exit 2); status reports `BLOCKED` rather than a
deployed address. Verify establishes `prepared-only` and returns exit 2, with all
41 hosted requirements blocked. CLI logs and `verification.json` are retained in
the accepted output directory. No `apply`, cloud `connect`, `rollback` or `destroy`
was executed.

Unresolved personal inputs are: `gcloud` and digest-preserving publisher `skopeo`;
verified active account/project number/billing attachment and currency evidence;
dated complete spending envelope; retention policy and store nonce/date/software
revision; exact immutable VM image/zone and authorised access principals. The owner
supplied a £20 **total** ceiling and pilot end of 31 December 2026. No billing
account, price quote or cloud mutation approval was inferred.

The dated official London USD costing record gives an illustrative **USD 6.49**
subtotal for a proposed 80 total VM hours, versus **USD 28.42** if always running
for the illustrative 88-day period. FX, tax, transfer/scanning and post-pilot
retention are unresolved; this is not a complete quote or a claim to fit £20.
The observed costs are in
`artifacts/gcp/costs-illustrative-london-2026-10-05.json`, included in the ZIP.

The VM only bridges the private connection. `connect` starts it within recorded
approval, forwards loopback for at most one hour and attempts to stop it on exit;
an hourly UTC stop-only schedule provides a fallback that can be 15 minutes late.
No automatic start is configured. Mock plans and lifecycle tests cover these
controls; actual hosted shutdown remains a gate. The CLI reserves 1.25 hours per
session against the proposed ceiling. Neither that ledger nor scheduling is a
hard billing cap. Stopped disk/DNS and retained evidence/images/logs still cost.

BDUK additionally needs platform network/build/IAM/egress approval, actual Okta
registration and role mappings, real multi-role policy and OAuth-client evidence,
hosted persistence/restart/backup recovery, rollback and teardown observations.
The existing 41-gate matrix is preserved. See [platform review](PLATFORM_APPROVAL.md)
and [verification](VERIFY.md).

## Cleanup

No GCP resources were created here. When a deployment exists, closing a foreground
connection attempts to stop its owned VM; inspect `status` if stop fails. Removal
requires `plan --destroy` and a fresh exact `destroy --approved-plan` decision,
including after pilot expiry. Protected Firestore and backup storage are retained;
their disposal and remaining charges require the recorded retention decision.
Use the [runbook](README.md) and [cost/teardown checklist](COST_AND_TEARDOWN.md).
