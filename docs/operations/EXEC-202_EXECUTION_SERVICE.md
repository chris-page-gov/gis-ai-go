# EXEC-202 private execution service

Status: accepted private implementation on protected `main` through
[pull request 34](https://github.com/chris-page-gov/gis-ai-go/pull/34) as
`6837af6eaa01ffb45e7da08d6a9131cedd1b1a0b`; not deployed, activated or
registered.

## Delivered boundary

The candidate replaces the Stage 0 rejection stub with one typed deterministic
Python service. The TypeScript gateway can construct the exact
`gis-ai-go.execution-request.v1` envelope and validates the corresponding result
before use. Python independently rejects unknown operations, parameters and fields.

Only `fixture.features.query` is implemented. It selects from five fictional point
features using a bounded simple Polygon in `EPSG:4326` with explicit
`longitude-latitude` axis order. It performs no geometry repair, simplification or
CRS transformation. It has no provider adapter, credential, end-user identity,
policy engine, arbitrary fetch, file selection, SQL or dynamic-code surface.

The gateway assertion contains a decision identifier, digest and permitted
operation. It is a typed private hand-off, not a signature, bearer credential or
Python policy decision. A deployment must keep the execution process unreachable
from public or end-user networks and add reviewed service-to-service trust before
any non-loopback binding.

## Interfaces

| Method and path | Purpose | Boundary |
| --- | --- | --- |
| `GET /internal/health` | process health | private JSON only |
| `GET /internal/readiness` | synthetic fixture passed startup checks | no provider claim |
| `GET /internal/openapi.json` | self-contained OpenAPI 3.1 | private contract |
| `POST /internal/v1/execute` | one allowlisted synthetic execution | closed request/result schemas |
| `DELETE /internal/v1/executions/{request_id}` | cooperative cancellation | active identifiers only |

The shipped process binds only to `127.0.0.1`. The container declares no exposed
port. Every response is JSON with `no-store` and `nosniff`; unsupported hosts,
methods, routes, encodings, transfer encodings and media types fail closed.

Canonical schemas are:

- `schemas/execution-request.schema.json`;
- `schemas/execution-result.schema.json`; and
- `schemas/execution-problem.schema.json`.

The request, result and controlled problem examples under `providers/fixtures/`
form the cross-language acceptance case. Identical fixture envelopes under the same
valid deadline produce byte-identical canonical result and evidence bytes.

## Absolute limits

| Limit | Service maximum |
| --- | ---: |
| raw request | 65,536 bytes |
| canonical output | 262,144 bytes |
| returned features | 100 |
| Polygon coordinates | 128 |
| complexity units | 20,000 |
| deadline window | 30 seconds |
| concurrent requests | 8 |
| transport read timeout | 5 seconds |

The gateway may supply lower limits. Python enforces both the gateway values and
its own ceiling. Complexity for this operation is the squared outer-ring segment
count plus the fixed fixture feature count. Gzip and every other content encoding
are rejected rather than decompressed. Work checks cancellation and deadline at
each feature boundary.
The server rejects a ninth concurrent request with a controlled `429` and closes
slow or abandoned reads after five seconds.

## Evidence and errors

Success preserves the W3C trace context and exact synthetic provider, dataset,
version, rights and source URI chosen by the gateway. Evidence additionally records
the input and output SHA-256 identities, feature count, source/output CRS and axis
order, explicit `none` repair/simplification decisions, algorithm and service
version.

Failures use `gis-ai-go.execution-problem.v1`. Codes are controlled literals and
details never contain request values, provider errors, paths, SQL, URLs, stack
traces or exception text. Unexpected failures become `INTERNAL_ERROR`.

## Container acceptance and rollback

`pnpm run test:execution-container` builds the digest-pinned official Python
3.12.14 slim image and verifies:

- UID/GID `65532`;
- read-only application and root filesystems;
- `--network none`, no exposed port and a loopback listener;
- all capabilities dropped and `no-new-privileges`;
- bounded CPU, memory, process and temporary-storage settings; and
- internal health, readiness and OpenAPI from inside the container.

Rollback removes or reverts the private execution image and its gateway envelope
builder. The existing static Explorer and inactive catalogue transports do not call
this service and continue independently.

## Explicitly deferred

- ADAPT-203 live or cached open-data adapters;
- durable execution events, attestation and `evidence.inspect`;
- tool activation, public ingress, registry publication or production deployment;
- service identity, network policy and workload authentication; and
- a complete release-image operating-system SBOM and vulnerability assessment.
