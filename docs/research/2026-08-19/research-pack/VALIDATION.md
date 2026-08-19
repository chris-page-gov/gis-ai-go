# Validation report

**Status: PASSED**  
Generated: 2026-08-19T13:30:00+01:00

| Check | Status | Detail |
| --- | --- | --- |
| JSON parse | passed | 26 JSON files parsed |
| JSON Schema and examples | passed | 6 schemas checked; 52 instances validated |
| Source-reference integrity | passed | 186 references resolved to 71 source records |
| OKF 0.2 frontmatter | passed | 95 OKF concepts/indexes parsed with type |
| Required pack structure | passed | 11 required roots and 13 reports present |
| Relative Markdown links | passed | 235 relative Markdown links resolved |
| JavaScript syntax | passed | app.js and data.js pass node --check |
| Static HTML contract | passed | Static HTML contract and no remote assets confirmed |
| Diagram render | passed | 9 Mermaid sources and 9 portable SVGs present |
| Secret-pattern scan | passed | No high-confidence credential/private-key patterns found |
| Commissioned record counts | passed | {'decisions': 20, 'requirements': 50, 'tools': 12, 'workflows': 10, 'risks': 30, 'evaluations': 25, 'names': 20} |
| Headless browser interaction | passed | Initialisation, 20 decisions, inspect/data card, 9 diagrams, WebMCP search and zero browser errors passed; static HTTP endpoints returned 200. |

## Scope limitations

- No live provider, protected identity, licensed cache or cloud deployment was exercised.
- Browser interaction was smoke-tested in Chromium; cross-browser and assistive-technology certification belongs to implementation.
- Provider licences, product availability and pricing require revalidation at implementation gates.
