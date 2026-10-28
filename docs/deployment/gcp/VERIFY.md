# Observe the private deployment

`deploy.sh verify` runs bounded HTTP observations and the independent pinned MCP
SDK. Keep `deploy.sh connect` running in a separate terminal for the personal
profile. Verification does not open a tunnel, replace a revision, update IAM or
terminate resources. All 41 required acceptance gates are reported, including
precise blocked gates; a partial probe does not pass a wider requirement.

```bash
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.private.json connect
# Separate terminal, while the reviewed private connection is active:
./scripts/gcp/deploy.sh --config artifacts/gcp/personal.private.json verify
```

The helper interface is executable independently for a recorded deployment:

```bash
python3 scripts/gcp/verify_hosted.py \
  --config artifacts/gcp/personal.private.json \
  --deployment artifacts/gcp/CONFIG_DIGEST/deployed.json \
  --output artifacts/gcp/CONFIG_DIGEST/hosted-results.json
```

The personal single-owner transport milestone uses the VM's signed service-account
invocation credential; it does not establish a separate signed-in human identity,
browser session or standards-compatible OAuth. The BDUK profile needs approved
private network access and real signed identity. Existing secure process bindings
may supply `GIS_GCP_ALLOWED_IDENTITY_TOKEN`, `GIS_GCP_FORBIDDEN_IDENTITY_TOKEN` and
`GIS_GCP_READER_IDENTITY_TOKEN`. Supply them through the approved credential route,
never a shell argument, checked-in file or chat. Their values are never printed.
The reader fixture must be a real provisioned viewer identity in the reviewed
role mapping. Merely supplying a token does not imply valid identity or role.

BDUK may provide `GIS_GCP_PRIVATE_BASE_URL` as one exact approved HTTPS origin;
the personal profile accepts only `http://127.0.0.1:8789`. The helper does not follow
redirects or send tokens to another target. Optional `GIS_GCP_TRANSPORT_TOKEN` is
independently verified against the canonical Cloud Run audience, issuer, exact
workload subject, signature and expiry before any outside-path request. A generic
403 is never marked a network privacy pass. Independent outside-source topology,
ingress-versus-IAM denial and unauthorised other-project observations remain
required platform evidence; this script records them as blocked until observed.

Only an apply approval that explicitly includes `verify-bounded-evidence` enables
query tests. The deployment record must carry
`verification_evidence_writes_authorised: true`. The probe otherwise runs metadata
and selection reads and records evidence writes as blocked. An authorised probe
uses one semantic key for two concurrent requests, replay and conflict refusal;
it reuses that key on subsequent runs. It performs no live provider or model call.

The first successful query writes `mcp-persistence-anchor.json` beside the private
results. After a separately approved replacement, rerun verification. `STATE01`
passes only when read-only GCP observation shows a different sole-serving ready
revision with 100% traffic and receipt inspection returns the identical verified
record digest. A receipt read during the original revision proves inspection, not
restart durability. Separate crash/lost-response, authorised principal ownership,
expiry and cross-instance tests remain required; they are not fabricated from a
successful replay. Rollback and teardown checks also require their approved
operations and observed evidence.

Run the verifier's local control tests without cloud access:

```bash
uv run --locked python -m unittest discover -s tests/deployment -p test_gcp_verify.py -v
node --check scripts/gcp/verify_mcp.mjs
```

These local HTTP fixtures and mocked cloud reads validate bounds and evidence
classification. They do not establish hosted authentication, GCP persistence or
BDUK acceptance. The evidence reports `PASS`, `FAIL`, `BLOCKED`, `NOT_RUN` and
justified `NOT_APPLICABLE`; required unresolved gates make verification exit 2.
