Fix the bounded Claude Code capability launcher to allow the exact sanitised
permission alias for canonical `catalogue.search`, and regression-check the CLI
and settings allowlists while retaining the one-tool-use-round-trip boundary.
Keep the dotted MCP `2026-07-28` wire name distinct from Claude's underscored
permission alias, reject alias collisions and accept additional standards-compliant
request metadata without weakening the exact capability evidence predicate.
