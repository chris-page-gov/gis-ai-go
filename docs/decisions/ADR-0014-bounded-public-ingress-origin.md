# ADR-0014: Bounded public ingress origin

- status: accepted; provider-neutral preparation
- date: 29 August 2026
- decision owner: Chris Page
- work items: [QUAL-206](https://github.com/chris-page-gov/gis-ai-go/issues/24) and
  [DEPLOY-207](https://github.com/chris-page-gov/gis-ai-go/issues/25)
- release target: `v0.2.0`, subject to the remaining activation gates

## Context

The accepted exact-five container listens on `0.0.0.0:8787` so the fixed local
Compose bridge can reach it, but its application Host and Origin allowlists were
loopback-only. A future TLS ingress preserving an honest public `Host` would
therefore be rejected. Rewriting that authority to loopback would make the request
work while removing the application-level public-authority check that QUAL-206
requires.

The public provider, hostname and TLS certificate are not selected. Repository
preparation must therefore admit no invented deployment details and must not turn a
configuration value into evidence that DNS, TLS, a public endpoint or registration
exists.

## Decision

The fixed container may read one non-secret authority setting:
`GIS_AI_GO_PUBLIC_HTTPS_ORIGIN`. This is an ingress allowlist input only. It is not
an activation, provider, tool, storage, credential, registration or deployment
setting.

The setting has two fail-closed modes:

- when absent, the existing fixed loopback Host and Origin boundary remains;
- when present, it must be one exact canonical `https://` origin containing a
  lowercase dotted DNS-shaped hostname and no port, path, query, fragment,
  credentials, wildcard, IP literal or admitted special-use suffix. This syntactic
  check does not prove DNS delegation or public reachability.

Public mode replaces, rather than extends, the loopback authority. One parsed value
derives the exact direct Host and Origin lists, the MCP Host, hostname and Origin
lists, the Host used by the internal health checker, and the OpenAPI server origin.
The health checker still connects privately to `127.0.0.1:8787`, but supplies the
same public Host as admitted traffic. This prevents a second loopback application
authority from remaining open in public mode.

`Forwarded` and `X-Forwarded-*` headers have no authority. They cannot substitute
for a rejected Host or Origin. The gateway accepts only the actual `Host` and
`Origin` presented by the immediate ingress. The configured OpenAPI document marks
`x-gis-ai-go-public-ingress-configured` as true but keeps
`x-gis-ai-go-public-deployment` false.

The original closed-builder decision is narrowed only by this one authority input.
There remains no environment seam for changing activation, operations, resources,
provider policy, cache material, paths, commands, production registration or
evidence storage.

## Evidence boundary

Repository tests must prove both modes, hostile and non-canonical values, exact
public Host and Origin admission over a real local socket, rejection of loopback,
wrong-port and forwarded-header substitution, exact-five discovery, and honest
OpenAPI projection. These tests use the IANA-reserved fixture
`https://gateway.example.com`; it is not a proposed service hostname.

The setting and tests do not prove:

- public DNS, certificate ownership, SNI or a trusted TLS chain;
- TLS version, cipher, plaintext rejection or proxy header handling;
- an independently reachable endpoint or remote-host interoperability;
- workload identity, provider egress, persistent storage or operational controls;
- deployment, registration, activation, rollback or release readiness.

Those claims require an authorised runtime, real hostname and certificate, exact
image binding, independent observation and the remaining DEPLOY-207 evidence.

## Consequences

- The exact image can later sit behind a TLS ingress without rewriting the public
  authority to loopback.
- Local Compose remains unchanged and supplies no environment setting.
- A public deployment definition may eventually supply this one exact non-secret
  value, but must independently restrict the private listener and prove TLS and
  proxy behaviour.
- Any different authority, multiple hostnames, non-default public port or wider
  ingress model requires a new decision and tests.
- The production registration flag remains false, and no provider call or public
  endpoint is created by this decision.
