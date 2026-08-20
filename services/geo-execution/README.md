# Private geospatial execution service

This workspace implements the EXEC-202 deterministic execution boundary. It accepts
one versioned, gateway-constructed request envelope and dispatches only
`fixture.features.query` over five fictional point records. It does not authenticate
an end user, decide policy, fetch a provider, accept a URL or path, execute SQL or
code, or expose a public listener.

The process entry point binds to `127.0.0.1` only and exposes:

- `GET /internal/health`;
- `GET /internal/readiness`;
- `GET /internal/openapi.json`;
- `POST /internal/v1/execute`; and
- `DELETE /internal/v1/executions/{request_id}` for cooperative cancellation.

The checked-in JSON Schemas under `../../schemas/` are shared with the TypeScript
gateway. Python validates the closed contract independently so a missing runtime
schema library cannot weaken the boundary. Provider-native source, version, rights,
trace, CRS, axis-order, transformation and software evidence are preserved in every
success. Controlled problem envelopes contain no raw exception, stack, path or
provider message.

Run the unit and real-loopback tests with:

```bash
uv run --locked --cache-dir .uv-cache \
  python -m unittest discover -s services/geo-execution/tests -p 'test_*.py'
```

Run the hardened container acceptance with:

```bash
pnpm run test:execution-container
```

The image uses a digest-pinned official Python base, runs as UID/GID `65532`, has no
exposed port and passes with a read-only root filesystem, no network, no Linux
capabilities and `no-new-privileges`. A future internal deployment still needs an
orchestrator network policy and service-to-service trust decision; this candidate is
not deployed or registered.
