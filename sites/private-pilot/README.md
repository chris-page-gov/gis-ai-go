# Private Sites live-data pilot assembly

This directory is an additive assembly overlay for the existing private Site. It
contains the manual `/pilot` page, `/pilot/mcp` route, native `/mcp` route, trusted runtime wrapper and
one schema migration. It does not alter the old `/demo`, `/workbench`, captured
CPIH store or supported GIS AI GO release.

## Build and source binding

1. Use an exact clean, committed GIS AI GO checkout whose required assurance has
   passed. Run `scripts/package_sites_pilot_runtime.mjs` with the admitted pinned
   Site tooling and a new output directory, as documented by that script.
2. Copy this overlay's `app/pilot/`, `app/mcp/` and `server/sites-pilot-runtime.mjs` into the
   recovered Site source. Install the generated runtime, `bundle-manifest.json`
   licence and third-party notices under `server/vendor/sites-pilot/`. Preserve the Site's existing
   routes, dependency lock, audience and configuration.
   Add `"mcp"` to the existing `.openai/hosting.json` `capabilities` array,
   preserving every existing capability and the exact `project_id`. If the
   capability array is absent, the additional field is
   `"capabilities": ["mcp"]`; otherwise append `"mcp"` once to that array.
   This is a merge instruction, not a replacement hosting manifest.
   This declaration is specified by the installed Sites MCP skill, version
   `0.1.75`, reviewed on 2 October 2026. Confirm the built hosting manifest retains it.
3. Register and apply `drizzle/0001_sites_pilot.sql` through the existing Site's
   reviewed migration mechanism. The SQL adds only the two pilot tables. It seeds
   four enabled provider rows at 120 attempts each and never refills or re-enables
   an existing row. Do not run schema or allowance SQL from a request handler.
   Copy `db/sites-pilot-schema.ts`, export its two tables from the existing
   `db/schema.ts`, and install the generated `drizzle/meta/0001_snapshot.json`.
   Preserve the legacy schema and journal entry; add the matching pilot entry.
   The snapshot is generated using the pinned Drizzle tooling and is checked
   against the published DDL, including SQLite primary-key nullability.
4. Set the trusted bindings below. The wrapper requires the configured source
   revision to equal the packaged manifest's `source_revision`. The declaration
   is a source binding, not independent build attestation.
5. In the assembled Site, run its pinned TypeScript check, lint and production
   build. Run the genuine local Workers/D1 MCP sequence and manual-page browser
   checks before deployment. Validate live identity, persistence, quota exhaustion
   and rollback separately on the deployed private endpoint.

Run the built artefact probe from the GIS AI GO checkout:

```sh
node scripts/test_sites_pilot_built_worker.mjs \
  --tooling-root /path/to/pinned/site \
  --site-root /path/to/built/site \
  --bundle-manifest /path/to/package/bundle-manifest.json
```

It uses the actual built Worker and local D1 with synthetic identity and intercepted
provider fixtures. It checks all six tools, denial paths, source binding, migration
replay, receipt persistence across restart and the existing workbench/static routes.
Its output explicitly excludes hosted authentication and database-recovery claims.

After starting the built Site preview at `http://localhost:4177`, run
`node scripts/test_sites_pilot_page.mjs` from the GIS AI GO checkout. The check
uses installed Chrome, intercepts the three MCP messages with a synthetic
capability response, verifies all six explanation links and checks keyboard
focus, layout and automated accessibility. It refuses external requests and
records HTTP/page errors. Restart the preview after rebuilding so its asset
manifest matches the new output. This is local UI evidence, not hosted identity
or provider acceptance.

The overlay alone cannot typecheck or build as a standalone application: it uses
the host Site's pinned React, Vinext and Workers types and the generated vendor
runtime. Do not replace that runtime with test fixtures to make a build pass.

## Deployment archive layout

Preserve the build plugin's `dist/.openai/drizzle/**` tree alongside
`dist/server/**` and `dist/client/**`. Include the source `.openai/hosting.json`
at the archive root as required by Sites. Do not flatten `dist/server` to `server`
or relocate the generated migration tree. From the clean, committed Site source:

```sh
COPYFILE_DISABLE=1 tar -cf /private/path/pilot-build.tar .openai/hosting.json dist
```

Inspect the archive before publication: it must contain the supported
`dist/server/index.js` entrypoint, both matching hosting manifests and the exact
generated migration tree, without source maps, secrets or macOS `._` metadata.
The public runtime package and private Site source have separate revisions.
Record both, plus local archive and returned platform archive digests; the
platform may normalise the archive, so its digest is a separate observation.

Preserve published migration SQL and journal entries byte-for-byte. The pilot's
four initial allowance rows are fixed operational configuration, with no provider
payload; replay cannot refill or re-enable them. This is a deliberate reviewed
initial-provisioning choice, distinct from general data seeding or backfill.
Keep typed schema and generated snapshot metadata consistent with the published
DDL. Never repair a missing migration by allowing ordinary requests to create
tables or reset allowances. Verify the actual tables after publication before
any live-provider evaluation; a successful deployment status is insufficient.

A repeated save for the same source revision may return the previous saved
version. Check its returned archive metadata before assuming a corrected archive
was accepted. Use an actual corrected source revision for a new candidate; do
not mutate or overwrite historical deployment evidence.

## Trusted worker bindings

| Binding | Meaning |
| --- | --- |
| `DB` | Existing Site D1 binding, containing the additive pilot migration. |
| `SITES_PILOT_ORIGIN` | Exact canonical HTTPS Site origin, with no path, explicit port or trailing slash. |
| `SITES_PILOT_SOURCE_REVISION` | Exact 40-character source revision from the packaged manifest. |
| `OS_NAMES_API_KEY` | Optional server-side secret for the OS Names API. Missing credentials disable that query without a provider call. |
| `SITES_PILOT_TEST_TOKEN_SHA256` | Optional SHA-256 of a private application test token. The token itself is never embedded in the page or wrapper. |

Use the platform's trusted environment/secret mechanism. Do not substitute
request headers, query parameters, browser storage, source files or public logs.
Configuration changes require a fresh deployment/isolate; conflicting cached
configuration fails closed. The wrapper never prints binding values or provider
errors.

Authentication and authorisation remain in the reviewed MCP handler. The wrapper
does not invent another identity-header rule. The owner-private Sites dispatcher
must enforce its existing audience and protect the platform identity headers.
An explicitly configured application test token is a separate test route; passing
that route does not prove native Sites MCP OAuth or independent-client acceptance.

The native `/mcp` route uses the same six-tool application with its exact path and
the same D1 store, persistent provider allowances and receipts. It never accepts
the application test token as user identity. Both routes retain exact-origin,
method, body, time and input checks; an incoming URL is never rewritten to another
route to pass those checks. Both mounts share one two-request isolate capacity. Cancelled requests retain
capacity until their underlying work settles. Provider allowances and receipt
limits remain shared durable controls.
Removing the admitted origin stops both routes after redeployment.

Publishing this overlay is a separate acceptance step. After a successful private
publication, call `get_site` with `include_mcp_connection: true`; preserve the
returned endpoint, OAuth resource and plugin ID. Reuse the Sites-provisioned App
and plugin, then offer that plugin through `plugin_management.suggest_plugins`.
Do not create a second App, run `codex mcp add`/`login`, invent an OAuth flow or
distribute the private test token as a connector credential. A successful native
read-only `sites_capabilities` call must precede any native live-provider test.
The assembled Worker probe uses synthetic identity and cannot establish hosted
OAuth, user consent, plugin installation or Claude acceptance.

## Manual and MCP behaviour

The page uses same-origin, credentialled MCP JSON requests with protocol
`2025-11-25`: initialise, initialised notification and one tool call. Its six tools
are capabilities, OS Names, OS OpenData product metadata, ONS MSOA names/codes,
ONS CPIH and receipt inspection. The browser never receives a provider credential
or calls an upstream provider directly. This page adds no WebMCP registration.

Manual questions and AI calls therefore reach the same provider validation,
durable allowance and receipt code. The page provides labels, keyboard focus,
busy/status/error announcements, cancellation and reflow. These implementation
features still require real-browser accessibility and journey verification.

The initial allowance is 120 attempted upstream calls per provider and at most
20 per minute per provider. Failed calls count; CPIH normally needs two attempts.
There are no automatic retries and no allowance refill on migration replay. The
receipt cap is 128. These are application controls, not proof of a platform
billing stop or permission to buy services.

OS named points are not detailed addresses or boundaries. MSOA name matches are
not point containment; `complete: false` explicitly identifies a partial result.
CPIH values are index levels, and calculated changes are labelled separately from
published inflation rates. Live results retain source attribution and dates.
Receipt inspection is historical evidence, not a fresh provider query, independent
attestation or verified disaster recovery. PSGA data remains disabled.

## Stop, rotate and recover

To stop the whole pilot, remove `SITES_PILOT_ORIGIN` through the Sites environment
tool and redeploy the exact currently saved version. Confirm its terminal status
and a `503` pilot response with no new provider attempts. This does not cancel an
already issued upstream request. Preserve the previous environment revision in the
private operating record. Reinstating the exact admitted origin and redeploying
re-enables the pilot without resetting allowance or receipts.

To revoke application test access, remove `SITES_PILOT_TEST_TOKEN_SHA256` and
redeploy. Confirm that the former token fails and ordinary owner access still
works. Platform bypass-token replacement and application token revocation are
separate operations. To rotate an OS key, replace its secret and redeploy; never
return the key to a browser or put it in a command-line argument.

For code rollback, use the exact baseline version identifier already returned by
Sites, then verify the legacy pages and unchanged owner-only audience. Retain the
pilot version identifier for restoration without rebuilding. Additive SQL means
rolling code back does not remove pilot tables or refill provider allowances.

An owner-only export of every pilot receipt and allowance row, with an independently
retained digest and capture time, supplies a comparison checkpoint. A paginated or
truncated read is incomplete until every returned continuation is exhausted and
the row counts agree. A checkpoint export is not an exercised database backup or
restore. The currently exposed connector provides read access but no database
restore or row-deletion operation; record recovery and deletion as unavailable
until the platform supplies a supported operation. Do not add an unreviewed
administrative HTTP route to bypass that gap or overwrite legacy data.

The application retains at most 128 permitted open-data receipts and four allowance
rows; it has no automatic expiry or deletion. Chris Page owns stop, revocation,
checkpoint custody and eventual pilot removal. These are experimental operating
arrangements, with no accepted recovery objective or service-level commitment.
