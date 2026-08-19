# MCP gateway boundary

This package pins the official TypeScript server SDK line and exposes Stage 0 metadata
only. It starts no listener, registers no tools and makes no provider or policy calls.
Live execution is rejected by `assertStageZeroRequest` and covered by unit tests.
