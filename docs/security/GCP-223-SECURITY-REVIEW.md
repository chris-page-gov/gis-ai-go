# GCP-223 security review and remediation record

Observed on 9 October 2026. This is an owner-authorised, sanitised public
derivative of the sealed repository review and subsequent fix observations.
It is suitable for source transfer through GitHub. It excludes private host
identities, absolute host paths, credentials, raw scanner reports, dependency
databases, private configuration and protected data.

The original review reported **three MEDIUM source findings and partial semantic
coverage**. Both originally scanned images remain **BLOCKED**. The subsequent
maintained-lock recheck returned zero advisory entries. Focused lifecycle
regressions passed 71 checks and the final archive regressions passed 39.
Supplemental independent review found a further archive metadata-retention case;
the revised boundary passed the parent's direct recheck and regression controls.
All three source findings are remediated within this focused local verification
scope. Complete source/CI and image/platform admission remain separate gates.
No secure-machine execution, image
admission, cloud deployment or BDUK acceptance is granted by publication.

## Original review scope and custody

The Standard repository scan completed against a working-tree target registered
at commit `78ab9b2828b4c713ca467d38a77ffa3db2f03ab9`, with snapshot digest
`codex-security-snapshot/v1:sha256:f60826e2c8256ea5972f8d166efdf121f728f9f87d17897806648e5b640a3e8a`.
Its requested scope was the full repository, with no path exclusions. Source
changed concurrently during the task, so that registration is not approval of
the final source commit published after remediation. Scan token usage was
unavailable.

The review covered the maintained website, file intake, local and hosted MCP
assemblies, identity, policy, evidence, providers, execution service,
infrastructure, build and operator workflows. Additional source-only reviews
covered historical qualification observers/verifiers and documentation tools.
These reads found no additional source-supported issue. Structural inventories,
privacy searches, metadata and advisory scans are separate from full semantic
review of every test, document, corpus record or third-party dependency byte.
The canonical coverage outcome remains partial.

The original canonical report, findings, coverage and manifest remain immutable
in private evidence custody. The following hashes identify those original
bytes; the private originals are not copied into this repository.

| Original evidence | SHA-256 |
| --- | --- |
| Canonical report | `74d2d719e2fc7747dc501897847cb9227755cb83a86c88af48d6c1470f5b2d5e` |
| Findings | `0bdf713a739de5430125699fe032b5c97ca1c82abacd3654a4a240e247971b62` |
| Coverage | `37a7e70f820850f155f0af043a3f1c7dd2564677d8cd6ab1b31f02b04703d3c3` |
| Scan manifest | `b5d7019a4ba872b18248c2fd8808faea5bc4b012118d0c1b0c0b3edb5756b17b` |
| Original image and lock observations | `9c0ec1d8da0a928cb85e82ead4c6caaf18f11a76261216aa5480a33d0c0b37ae` |

## Source findings in the sealed review

All three were validated from source and explicit caller controls. No hostile
archive, malicious source link, credential read, exploit or cloud mutation was
executed during that validation. The model treats ordinary operators as trusted:
the attacker supplies lower-trust archive or contribution bytes across an
operator review boundary.

| Finding | Original severity and confidence | Source boundary | Supplemental fix verification |
| --- | --- | --- | --- |
| `csf_abb1ea931e2d97c98d0d70be`: OKF+ compressed tar extension headers can exhaust memory | MEDIUM; high confidence | Received archive to offline parser | Remediated; 39 checks pass, including the independently identified metadata-retention case |
| `csf_0c831d7b64d205d21dbf36aa`: cloud approval omits symlinked IaC bytes later consumed | MEDIUM; medium confidence | Contributed source to approved cloud execution | 71 focused lifecycle checks pass; supplemental review found no additional concrete bypass |
| `csf_3ec0a21650c5a95f5c2495d6`: review-package source symlinks can include host-file contents | MEDIUM; high confidence | Contributed source to transfer ZIP membership | 71 focused lifecycle checks pass; supplemental review found no additional concrete bypass |

### Received archive resource budget

The two OKF+ verification CLIs call the shared archive verifier in
[export.py](../../scripts/okf_plus/export.py). A supplied compressed archive
reaches Python tar parsing before yielded-member checks run. PAX and GNU
extension-header bodies can be decompressed and allocated internally before the
verifier sees a regular member. The existing compressed-size, regular-member,
aggregate payload, member-count, path, link, manifest and digest checks do not
bound that earlier work. No extraction or remote upload route is required;
the demonstrated source path is an operator-triggered local denial of service.

The required correction is a raw decompressed-tar budget and bounded extension
framing before the general parser, preserving member and manifest controls.
Verification must include oversized extension bodies and decompression limits.

### Cloud approval source binding

In the original [lifecycle.py](../../scripts/gcp/lifecycle.py), source inventory
omits symbolic links while IaC materialisation dereferences them. A contributor's
link can point to a mutable referent whose bytes are absent from the approved
source digest. Later service planning consumes those bytes under the legitimate
operator's cloud authority. Checks on permitted resource addresses/actions do
not compare every concrete attribute with the approved scope. Changing the
referent after review can therefore alter resource behaviour without forging
approval.

The required correction is a closed, non-link source inventory, with the IaC
and generated variables actually consumed by Terraform bound to approval.
Comparing every concrete resource attribute with the reviewed scope is further
architectural hardening recommended by the original scan; the source-binding
fix does not claim to implement that redesign.

### Transfer-package membership

The original lifecycle package branch enumerates physical application/package/
deployment-test files, accepts ordinary code/JSON suffixes, and follows a source
symlink when reading text. An admitted contribution can consequently copy an
operator-readable host file into the local review ZIP. Redacting known private
configuration values does not redact arbitrary host-file contents. The ZIP is
not uploaded automatically; later sharing is a separate exposure step.

The required correction is package membership derived from the approved public
source inventory, uniform rejection of links and special/private inputs before
reading, and a complete outgoing-artifact check before making privacy claims.

## Supplemental remediation observations

The owner authorised fixing all three findings and publishing this sanitised
record through GitHub. Fixes, focused negative checks, source bindings and
dependency reassessment are recorded here only after their actual results are
available. They supplement the sealed audit; they do not rewrite its findings,
severity, original image receipts or partial coverage outcome.

The following focused lifecycle command passed **71 checks** against the fixed
source:

```sh
python3 -m unittest discover -s tests/deployment -p test_gcp_lifecycle.py -v
```

The lifecycle source now uses one bounded descriptor-based reader for inventory,
policy, prepared-source checks, IaC and ZIP payloads. It refuses symbolic-link
leaves/ancestors, hardlinks, missing files and special files, and binds stable
bytes and modes. Terraform receives admitted Git-inventory bytes and bound
generated variables; ignored and stale executable inputs and target aliases are
refused. Valid saved-plan, state/provider-cache preservation and ordinary
non-ignored untracked source cases remain covered.

Review ZIP membership is derived from that inventory and its existing public
allowlist. Private environment/state/backup inputs and ignored cost artifacts are
excluded. Executable modes, configured-input redaction and outgoing checksums
remain covered. These controls close the reported source-alias and membership
paths; they do not redesign the service resource-attribute policy or certify
every source file's content as public. The aggregate `pnpm run test:gcp` local
suite also passed: 26 runtime, 115 Python deployment and seven packaging/UI
checks. The 71 focused lifecycle checks are included in the deployment total,
not an additional aggregate count. The supplemental static review found no
additional concrete bypass in the lifecycle, packaging or dependency changes.

| Supplemental fixed lifecycle source | SHA-256 |
| --- | --- |
| `scripts/gcp/lifecycle.py` | `fac5dc20a4e87d60ff1a32d40c8a3ebd2536a8de200c50bbc15bdb3b968bf221` |
| `tests/deployment/test_gcp_lifecycle.py` | `932845247978777928249d0896dafafb6c5aa53a75f600f0eaf77d7ee0cc2591` |
| Aggregate local GCP check log | `71ee55d7b6923c71aceaa4a77834fb843bee894de51227060f7dd4fd52a2d4c3` |

The final archive regression command passed **39 checks**: 17 existing checks and 22
new resource-budget checks.

```sh
python -m unittest tests.contract.test_okf_plus_export \
  tests.contract.test_okf_plus_export_documents \
  tests.contract.test_okf_plus_export_archive_limits -q
```

The shared verifier now limits raw decompressed bytes to 3 GiB, including
headers, padding, trailing bytes and concatenated gzip streams. Extension checks
run before PAX local/global/Solaris and GNU name/link body reads: a padded
extension body is limited to 64 KiB, aggregate extensions including headers to
64 MiB, extension count to 100,000 and consecutive extension depth to 16. Tests
assert that oversized extension forms stop after their 512-byte header. Sparse
variants are refused before hidden-map processing; nonzero trailing content and
truncation are rejected. Existing 256 MiB member, 2 GiB payload, 100,000-file,
path, manifest and digest controls remain. Normal public/private round trips
with bounded Unicode PAX, global/Solaris metadata and GNU long names passed.

| Supplemental fixed archive source | SHA-256 |
| --- | --- |
| `scripts/okf_plus/export.py` | `52d9c9b36d111a2f39144814624c39ac5a1ed1efc56a916a1311b2704724d255` |
| `tests/contract/test_okf_plus_export_archive_limits.py` | `cd7104b48f30631e056ed87e36813b79f67a2b9a7f8c1f9011e70acb20fd1142` |
| Final archive local-check receipt | `1d0babf846f60ccbe0af8bbe7455b7120ca94c5a05e2fe58d389283902f3687e` |

The supplemental independent static review identified global PAX dictionary
copies retained on every parsed member. A bounded synthetic reproduction used
a 1,967-byte archive with 500 attributes and 30 empty files: the initial candidate
retained 31 member objects and 15,500 attributes despite its input limits.
The revision bounds accumulated global and combined local/global state to 128
attributes and 64 KiB before parser copies, and clears fully hashed members from
the parser cache. The original trigger now refuses the attribute count. Valid
100-attribute, 31-member controls retain at most one cached member and none after
verification. Four ordered trigger/control checks and all 39 nearest contract
checks pass. The parent traced and checked this revision; no second independent
review cycle is claimed. These results establish the tested correction, not
complete source or image acceptance.

The review considered these immutable patch identities; it did not execute an
application, test, network call or credential inspection:

| Supplemental static-review input | SHA-256 |
| --- | --- |
| Original remediation patch | `8730f066a4482c8cf209291b3caefe83fe840f8badd4976756fb1966632fd1d2` |
| Sites dependency-version companion patch | `552b852c1bd11aa249505a3c01ee3f131faf89cf8de8173a69a65b5e11cf81a1` |

The subsequent actual offline Trivy lock scan included development dependencies
and listed all packages. It observed 155 npm and eight Python packages, with
**zero advisory entries at every severity**, using the retained schema-2 database
updated at `2026-10-09T13:10:00.476847953Z`. The database publisher-trust limitation
still applies. The updated closure pins MCP client/server `2.2.0`, MCP Node
`2.0.0` with its compatible `^2.0` peer, Hono `4.13.7`, source-map-js `1.2.2` and
Undici `8.10.2`. Workspace type checks and 18 pin/historical-matrix checks passed.
The bounded Sites evaluator now requires and reports the current `2.2.0` client;
its schema also accepts historical `2.0.0` observations. All 22 injected/offline
Sites evaluation tests passed, without live provider calls.
The deterministic local receipt set was regenerated for the updated lock hash;
only that binding and the derived set identity changed. Its bodies and claims
remain unchanged. All 33 strict-modern/local-receipt binding checks passed.
`pnpm run test:public-data-workbench` passed 52 checks across four Vitest files;
`pnpm run test:typescript` passed 639 source-unit/launcher checks, with one
provider check skipped because its credential prerequisite was absent. The
launcher lifecycle passed, but its dirty-source LOCAL-214 exact-source demo/
archive acceptance reported `NOT_RUN`; that acceptance remains outstanding.
The 67 environment/image-assurance unit checks also passed; their mock scanner
cases remain separate from the actual blocked image scans. The final
`pnpm run test:interoperability` rerun passed 76 checks with 14 skips, followed by
seven non-live, unscored receipt checks. These are local protocol/evidence
observations, not hosted-client, live-provider or BDUK acceptance.

| Supplemental dependency evidence | SHA-256 |
| --- | --- |
| Actual Trivy lock recheck JSON | `43ad316ca4896a799b5270698ca252989b94fcd89de08f22db4889d113c1c711` |
| Exact 16-input manifest for that recheck | `098841b7b1407e093ddf2b7578443dfaf098ffda05f36f74c7e710349bb836bd` |

## Published CodeQL follow-through

[Draft PR #146](https://github.com/chris-page-gov/gis-ai-go/pull/146) publishes
the implementation and this sanitised report. Its first published remediation
commit, `ffdfff4cec678b7e84583f42accfa9acfd31d664`, produced
[three CodeQL annotations](https://github.com/chris-page-gov/gis-ai-go/runs/113986521013).
Static triage preserves each annotation; it does not invent repository alert IDs
or treat repeated header annotations as independent demonstrated exploits.

The HIGH incomplete-URL-substring annotation is not actionable in the observed
path. `enabled_apis` is constructed as a list of full service names; Python list
membership already compares complete values. The condition now spells out
element equality. Seven service-list cases exercise the real preflight path:
empty, prefix/suffix/URL/case variants refuse, while the exact service and
duplicates pass. This is a clarity change, not correction of a demonstrated
substring vulnerability. No secret values are read or APIs enabled.

The two MEDIUM response-splitting annotations concern upstream response headers
passed to Python's HTTP server. Production uses one fixed authenticated HTTPS
Cloud Run origin and a loopback-only listener. Static inspection did not establish
a lower-trust caller-controlled value through the maintained application;
initial exploitability remains unproven. Nevertheless, the response boundary
previously forwarded parser-retained folded CRLF and control values. A bounded
synthetic upstream reproduced four invalid field variants while a legitimate
two-cookie response passed through the same path.

The shared response-header guard now materialises and validates every upstream
field before buffering any status or header, including fields later filtered.
It rejects CR/LF, invalid ASCII token names, illegal field controls and values
outside Latin-1; invalid material produces one empty `502` and closes the upstream
connection. It refuses invalid values rather than silently stripping them.
Repeated `Set-Cookie` fields retain their order and individual values. Body
streaming and existing response/export budgets remain intact.

Syntax/import checks passed before the negative cases. All 19 malformed field
variants now refuse before a success status, upstream marker or body; valid
cookies, HTAB/Latin-1 fields, streaming and the 17 MiB admitted public export
remain covered. All **11 proxy checks** and the aggregate GCP suite above pass:

```sh
python3 -m unittest tests.deployment.test_gcp_proxy -v
pnpm run test:gcp
```

One fresh read-only investigator and one fresh read-only candidate reviewer
independently traced this boundary. The candidate reviewer found no concrete
surviving bypass or introduced regression; it inspected source and tests without
executing them. The parent ran the ordered local checks above. A raw upstream
CRLF sequence parsed as separate valid fields cannot be distinguished from
ordinary upstream fields; no caller-controlled production route to such a
response was established. Do not treat boundary hardening as proof of original
lower-trust exploitability.

| Supplemental proxy evidence | SHA-256 |
| --- | --- |
| `scripts/gcp/access_proxy.py` | `ea0b7f90a4da1c14f24a2b6e2de5235ca39b3025fab0e61818adfaa19a93b47a` |
| `tests/deployment/test_gcp_proxy.py` | `567e0806a71ef292f31b591e0c6e64092267a8d15e5a3989bf88665c5c7a7a35` |
| Focused proxy check log | `8bf788f48502c1309566f80a6228ed4ae9fd2e5510c80d8dd83a1b389a8f6826` |
| Candidate supplied for independent static review | `71a73c0f9d86985672711f8a157891ca065e7b93ce851d17b4cfbfc17355420d` |

## Original image and dependency observations

Actual digest-pinned Syft 1.42.2 and Trivy 0.74.0 ran against frozen offline OCI
and database snapshots. The retained database was updated on 9 October 2026 at
13:10 UTC and its bytes/freshness were checked. Independent database publisher
trust, builder authority and image signatures remain unresolved.

| Original material | CRITICAL | HIGH | HIGH/CRITICAL entries | Additional blocker |
| --- | ---: | ---: | ---: | --- |
| Development toolchain image | 36 | 714 | 750 | Invalid/incomplete package inventory; 11 Go package entries lack versions; binary/package coverage incomplete |
| Earlier GCP application image | 5 | 69 | 74 | Unassessed binary package type and incomplete coverage |
| Original maintained pnpm and uv locks, including development dependencies | 0 | 5 | 5 | Also six MEDIUM and three LOW advisories; original result retained |

These counts are package vulnerability entries, not unique CVEs. They do not
establish application exploitability without reachability analysis. No findings
were ignored to produce a passing result. Fixing source or locks does not change
the bytes, counts or blocked status of an original image.

| Original material identity | SHA-256 |
| --- | --- |
| Development OCI archive | `e5279c15e5ea6ffecb9e191ac481a7347fb425c4af2feae9641210f07a23bf1a` |
| Development OCI root index | `6f4eb1e6a0ccd7df460c8d6bdf00dd4a2bcb19fbd0a1418e4a0a80e8c772b836` |
| Development runtime manifest | `7c81bac8215b7d0d02d4c391fccdb821b13ef695d44df230586123adadb09f55` |
| Development original blocked receipt | `5744f4d3e076e80b50dd22d884d8992104e95e443882d57ed9ed9e69160cd0c8` |
| Development original Trivy report | `7cbff855dca7ed6927479aea9a691b6d8fe2c92d1ad6883fad428519ffe1a2db` |
| Earlier GCP OCI archive | `51297ab392c499554866260fe2f25cc30d6b56b753a5ac368f8fee8fb164837e` |
| Earlier GCP runtime manifest | `3ef00620adfc26290444eec5fd7d7c60abbf1274c79c28b4e90615a99a188a4f` |
| Earlier GCP original blocked receipt | `931b534c1be40dc0dab3b877ece02b851c975591e2adce95515a3d7479dd9f69` |
| Earlier GCP original Trivy report | `9356cf159107c0392d4ae5d1fb5dd17c62530fe0395383aeae475895557fe59c` |
| Original maintained-lock advisory report | `4baf151778d0e7a6a80b97afc1b9a3304435767170caba803083c91503313516` |

See [build and image assurance](../development/BUILD_ASSURANCE.md) for commands,
observed tool compatibility, scanner isolation, evidence retention and cleanup.
Neither original image was published to a registry or deployed.

## Remaining acceptance gates

The complete local `pnpm run check` was attempted. Its Python stage ran 1,249
checks with three failures and seven skips: native Darwin/SIGKILL observer
fixtures, the subsequently corrected deterministic receipt binding, and a
runtime-identity uniqueness refusal in the strict collector journey. After the
binding correction, its 33 owning checks passed. An offline copy-only dependency
install produced 5,103 dependency files with one link each; the collector's
uniqueness refusal still reproduces, so no passing collector acceptance is
claimed. Source and CI install commands use copy imports and disable dependency
hooks. No process/identity assertion was relaxed to make these checks pass.
The canonical Chrome binary is absent, so canonical browser checks remain
unrun. At the first published remediation commit, GitHub's Repository assurance
job failed in its Run assurance step with exit code 1; Gateway image assurance
passed. Detailed action logs could not be retrieved because their download host
was denied by this environment's network policy. This does not establish the
remote failure's cause. Canonical CI against the final published commit and
fresh CodeQL analysis must resolve their gates; no alert dismissal or query
suppression is claimed.

1. Complete canonical CI against the final published source. Preserve the tested
   lifecycle, packaging and archive guarantees. Retain the zero-advisory
   recheck against its exact inputs and database; it is not a claim of complete
   third-party semantic review or database publisher trust.
2. Review and approve the exact final published source commit. Preserve the
   original partial semantic coverage and close or explicitly retain each
   unresolved test, support, document, corpus and third-party proof gap. A
   structural inventory or search is not an individually completed review.
3. Select the platform-approved base, registry, mirror, CA and builder. Produce
   fresh development and GCP child images, complete versioned SBOMs, dependency/
   licence closure and fresh vulnerability scans. Missing versions, unassessed
   binaries and HIGH/CRITICAL entries continue to block image acceptance.
4. Verify signatures/provenance against actual trusted builders and publishers,
   and establish database publisher trust. Retained attestations or an offline
   scanner result alone do not satisfy this requirement.
5. Complete [secure-machine source/image/workspace admission](../development/SECURE_TRANSITION.md)
   and the actual platform decision before running repository scripts,
   installing dependencies, building or opening containers there. Inspect the
   effective editor/engine controls; keep credentials and protected material
   outside the mounted workspace.
6. Retain the separate first-cloud-mutation approval: exact account/project,
   resources, upload inventory, billing/currency/prices, spending and duration.
   No source publication or security fix supplies that approval.
7. Observe hosted transport and human authentication, Okta registration and
   network rules, policy refusal, persistence, recovery and BDUK acceptance.
   All 41 [GCP acceptance requirements](../deployment/gcp/ACCEPTANCE.md) remain
   unproved by these local source/image checks.

The sealed scan remains an audit of its original snapshot. This public
derivative, a passing focused test, or a GitHub branch publication does not
authorise secure execution, image publication, cloud mutation or release.
