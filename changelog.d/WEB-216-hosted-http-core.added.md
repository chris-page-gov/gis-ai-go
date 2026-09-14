- Extract the existing MCP wire/privacy and bounded JSON safeguards into shared
  modules with unchanged legacy exports. Add an inactive JSON-mode hosted handler,
  an explicit filesystem-free evidence import subpath and an offline runtime
  packager. Actual local Workers tests cover invalid wire traffic, exact snapshot
  preservation and zero provider egress; Site ingress, identity and deployment
  acceptance remain separate.
