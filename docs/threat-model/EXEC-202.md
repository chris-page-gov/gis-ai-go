# EXEC-202 threat notes

Scope: the private synthetic-only execution candidate. This is a focused design and
regression record, not a production penetration test or deployment approval.

## Trust boundary

The TypeScript gateway constructs a closed envelope after its own policy path. The
Python process accepts only that shape over loopback and does not authenticate an
end user or decide whether an operation is permitted. The gateway assertion is not
cryptographically authenticated. Its safety therefore depends on the current
loopback/private-process boundary; any container-network deployment needs an
explicit workload identity and network-policy design before activation.

Repository schemas and request data are untrusted inputs. The implementation uses
independent runtime validation and controlled literals. Only checked-in fictional
features are executable data.

## Controls and residual risk

| Research risk | Candidate control | Residual boundary |
| --- | --- | --- |
| RK03 confused deputy and RK08 policy bypass | Exact operation plus matching gateway assertion are required; Python has no identity or policy API. | The assertion is not a signature. Non-loopback deployment needs workload trust and replay analysis. |
| RK10 SSRF and arbitrary URL fetch | The request schema contains no URL/path and dispatch has no network, file, SQL, shell, eval or dynamic import route. | ADAPT-203 must add a separate fixed-endpoint adapter allowlist. |
| RK15 malicious geometry and RK26 axis error | One simple closed Polygon, explicit EPSG:4326/longitude-latitude, finite range checks, no holes, self-intersection, silent repair, simplification or transform. | Later geometry types and transformations need library-specific correctness evidence. |
| RK16 decompression bomb | Every content encoding and transfer encoding is rejected; raw bodies are capped before JSON parsing. | Future archive or provider compression needs streamed compressed and expanded-size controls. |
| RK17 expensive-query denial of service | Absolute and gateway-lower byte, coordinate, feature, complexity, output and 30-second limits; eight-request admission, five-second read timeout and cooperative deadline/cancellation checkpoints. | The in-memory cancellation registry is process-local and not durable across restart. |
| RK20 provenance spoofing | Exact selected source/version/rights survive the round trip; deterministic input/output digests and transformation/software evidence accompany each result. | Evidence is not signed, persisted or attested; EVID-204 owns that later boundary. |
| RK23 supply-chain compromise | Official Python image is multi-architecture digest pinned; no Python runtime dependency is added; repository SBOM binds the base digest. | Full image package SBOM, vulnerability scan and image attestation remain release gates. |
| RK30 operational drift | OpenAPI, JSON Schemas, gateway types, Python validation and shared fixtures are tested together. | A deployed orchestrator and gateway-to-service compatibility matrix do not yet exist. |

## Negative assurance

Automated regressions cover unknown fields and operations, bad source selections,
malformed and self-intersecting geometry, invalid CRS and axis order, excessive
coordinates/features/bytes/complexity/output, duplicate keys, non-finite values,
invalid UTF-8, compression, timeout, live cancellation, hostile Host and media-type
headers, unexpected runtime errors and forbidden URL/path/SQL/shell/code call
surfaces. Controlled problems are checked for absence of reflected hostile content,
stack traces and machine paths.
