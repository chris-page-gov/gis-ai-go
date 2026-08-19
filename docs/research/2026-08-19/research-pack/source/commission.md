# Deep Research Prompt: Designing a Governed Geospatial Knowledge and Action Platform

## Commission

Conduct a source-backed, implementation-oriented research and architecture exercise to determine how to replace — rather than incrementally patch — the existing `chris-page-gov/mcp-geo` prototype with a new, production-minded geospatial knowledge and action platform.

The successor must combine:

- authoritative UK geospatial and statistical information;
- human and machine-readable discovery through Open Knowledge Format (OKF);
- current Model Context Protocol capabilities;
- browser-native structured interaction where WebMCP is appropriate;
- modern mapping and cloud-native geospatial techniques;
- proper identity, OAuth-based authorisation and attribute-based access control;
- enforceable data-licensing and policy constraints;
- complete provenance, evidence and audit;
- interactive human presentation;
- portability between AI hosts and cloud environments; and
- a sufficiently precise implementation pack for Codex to create the new repository.

Do not merely recommend a newer version of the current server. Establish what the product ought to be, which responsibilities belong in it, and which should remain in upstream data services, gateways, identity providers, workflow systems, policy engines or client applications.

Use British English throughout.

Do not stop to request clarification. Record material assumptions, distinguish them from verified facts and continue.

---

## 1. Intended outcome

The principal outcome is not just a narrative report. Produce a **linked, explorable research and decision pack** backed by machine-readable data, preferably an OKF bundle that can power:

- a self-contained static website;
- OKF Explorer or a clearly specified evolution of it;
- search and faceted navigation;
- graph, timeline and map views;
- evidence-linked data cards;
- architecture and decision exploration;
- source and provenance inspection;
- export to Markdown and JSON; and
- direct implementation handoff to Codex.

Treat “SeeLinks-style” as a functional description of a linked, explorable evidence pack unless a specific authoritative product with that name is positively identified. Do not make the research dependent upon an unidentified proprietary service.

The pack must be easy to share and must work from ordinary static hosting wherever possible. Its public form must contain only open, publishable or synthetic information.

---

## 2. Starting repositories and evidence

Inspect the following repositories in depth:

- `https://github.com/chris-page-gov/mcp-geo.git`
- `https://github.com/chris-page-gov/okf-explorer.git`
- `https://github.com/chris-page-gov/okf-ons.git`
- `https://github.com/chris-page-gov/okf-LandRegistry.git`
- the OKF material under the Google Cloud Platform Knowledge Catalog repository;
- any repository, site or bundle linked from those sources that is necessary to understand the current HMLR example or the normative and experimental forms of OKF.

For each repository:

1. Record the repository, branch, commit SHA, retrieval date and apparent version.
2. Inspect architecture, schemas, tools, resources, prompts, UI, tests, deployment files, security controls, policy artefacts, evaluation material, changelog and unresolved plans.
3. Distinguish:
   - normative specifications;
   - experimental specifications;
   - provider-specific profiles;
   - application conventions;
   - generated artefacts;
   - historical evidence;
   - abandoned experiments; and
   - reusable implementation assets.
4. Do not treat vendored or locally copied specifications as current authority when live official specifications are available.
5. Produce a **forensic harvest matrix** for the current MCP-Geo repository:
   - retain unchanged;
   - retain concept but redesign;
   - migrate after testing;
   - preserve only as historical evidence;
   - discard;
   - unresolved pending investigation.

Pay particular attention to lessons embodied in:

- the existing geography-level model;
- OS, ONS, NOMIS and LandIS adapters;
- boundary and statistics caches;
- routing and mapping work;
- MCP Apps experiments;
- map fallbacks;
- protocol-version work;
- existing tool and resource schemas;
- evaluation questions;
- correlation and provenance fields;
- OWASP or tool-risk inventories;
- test fixtures and failure cases;
- client interoperability work; and
- evidence of excessive coupling or tool proliferation.

Do not rewrite the existing repository in place. Assess whether it should remain an archived learning journal while the successor begins in a new repository.

---

## 3. Source and research discipline

Use primary sources wherever they exist.

Prioritise:

- official MCP specifications, extension specifications, SDK documentation and working-group material;
- official OpenAI, Anthropic, Microsoft, Google, browser-vendor and W3C documentation;
- Ordnance Survey product documentation, technical specifications, licences and roadmaps;
- ONS, UK Statistics Authority, ONS Geography and NOMIS documentation and strategies;
- Cranfield University, Defra and LandIS Portal documentation;
- HM Land Registry documentation and licensing;
- OGC, ISO, IETF, OpenID Foundation and W3C standards;
- NCSC, Cabinet Office, DSIT, GDS, ICO and other authoritative UK public-sector sources;
- official repositories and release notes for geospatial software and formats.

For every material claim:

- provide an inline citation;
- record publication and retrieval dates;
- distinguish current, deprecated, preview, beta, draft and proposed material;
- identify conflicts between sources;
- state the confidence level;
- avoid presenting vendor marketing as independent evidence; and
- state where no authoritative answer is available.

Use current information as at the actual research date. Explicitly verify the final MCP specification, MCP Apps, Tasks, Enterprise-Managed Authorization, OpenAI integration requirements, ChatGPT Sites, WebMCP and all named geospatial standards rather than relying on remembered versions.

---

## 4. Architectural premise: the six-control governance spine

Use the following six-control spine as the primary governance view. It represents the route from human intention to authoritative action and evidence:

1. **Domain knowledge and semantics**
   - concepts, identifiers, relationships, vocabulary, metadata, catalogues and discovery;
   - OKF bundles and domain profiles;
   - authoritative versus derived knowledge;
   - temporal and geographic meaning;
   - uncertainty, scale and fitness for purpose.

2. **Authority, identity and policy**
   - human, agent, client and workload identity;
   - legal authority, organisational entitlement, licence and declared purpose;
   - authentication, authorisation and policy evaluation;
   - role, device posture, risk and context;
   - obligations, prohibitions and approval requirements.

3. **Durable workflow and human control**
   - deterministic processes and state transitions;
   - Arazzo or other explicit workflow definitions;
   - MCP Tasks and Multi Round-Trip Requests where appropriate;
   - human approval and challenge;
   - resumability, expiry, cancellation and rollback.

4. **MCP, APIs and events**
   - discovery and invocation through MCP;
   - OpenAPI, OGC API and AsyncAPI services;
   - gateways, routing, rate controls and protocol mediation;
   - browser and MCP-host presentation contracts;
   - service-to-service and event interactions.

5. **Authoritative systems, data and computation**
   - OS, ONS, NOMIS, LandIS, HMLR and other systems of record;
   - local authorised caches and replicas;
   - PostGIS, object storage, spatial processing and deterministic computation;
   - source-native semantics and provider constraints.

6. **Evidence, audit and assurance**
   - source and transformation provenance;
   - policy decisions and approvals;
   - tool calls and state changes;
   - outputs, computation receipts and attestations;
   - monitoring, evaluation, incidents, rollback and public transparency.

Identity, security, privacy, licensing, lifecycle control and accessibility must operate across all six controls, not as a single perimeter layer.

Also provide a separate deployable systems view showing presentation, control, execution/data and evidence planes. Explain how this deployment view maps to the six-control governance view.

Compare the present human-led process with a future governed agentic process. Both must use the same policy, authoritative-system and evidence spine; the agentic track must not acquire authority merely because an AI agent can call a tool.

---

## 5. Product definition and boundaries

Determine what the successor actually is. Evaluate whether it should be understood as:

- an MCP server;
- a federation of domain MCP servers;
- an MCP and policy gateway;
- a geospatial query and evidence service;
- an OKF-powered knowledge and capability catalogue;
- a human-facing geospatial exploration site;
- an agent-ready website;
- an integration platform;
- or a composition of these.

Define clear product boundaries and non-goals.

At minimum, test these hypotheses:

- OKF is the discovery, semantic, provenance and policy-description layer, not the ultimate runtime authority.
- MCP is the agent-facing discovery and invocation protocol, not the system of record or the evidence store.
- Arazzo or equivalent explicit workflow definitions govern multi-step processes; an LLM-generated plan alone is not a durable workflow.
- Geospatial operations that can be deterministic should be performed by tested geospatial software, not inferred by the language model.
- Human UI, MCP Apps and WebMCP are related but distinct presentation and interaction mechanisms.
- Public, PSGA-licensed and commercial access may require separate data planes or deployments, even where they share source code and policy models.
- The successor should expose a small, composable and stable capability surface rather than reproducing a catalogue of around a hundred narrowly divided tools.
- Provider-native APIs and data models must remain traceable even when a canonical internal query model is used.

Identify which hypotheses are supported, rejected or need qualification.

---

## 6. Users, agents and access tiers

Define personas and user journeys for at least:

- an anonymous member of the public;
- a local-government analyst;
- a central-government analyst;
- a PSGA-authorised user;
- a commercial customer;
- a data steward;
- a security or policy administrator;
- an application developer;
- an interactive human user;
- an AI agent acting for a known human;
- a service or scheduled workload acting without a human session;
- an auditor or investigator.

Model three access tiers:

### Tier A — Open

Public data, public metadata and public tools. No protected credentials or licensed cache content may reach the browser or static bundle.

### Tier B — PSGA and other public-sector entitlements

Data and operations available only to authorised organisations and users under applicable agreements. Access must consider role, organisation, purpose and device posture.

### Tier C — Commercial

Data or services requiring a commercial contract, subscription, quota or charge. The architecture must distinguish entitlement from payment and must not silently turn the operator into an unauthorised data reseller.

Treat **licence tier**, **security classification**, **personal-data status**, **query sensitivity** and **commercial entitlement** as separate dimensions. An open dataset can still be used in a sensitive query; a licensed dataset is not necessarily security-classified.

Evaluate whether these tiers should share:

- identity infrastructure;
- policy definitions;
- service code;
- metadata;
- databases;
- object stores;
- encryption keys;
- caches; and
- runtime deployments.

Prefer strong isolation where the risk of cross-tier leakage outweighs operational convenience.

---

## 7. OS, ONS, NOMIS, LandIS and HMLR landscape

### 7.1 Ordnance Survey

Investigate:

- OS OpenData, PSGA and commercial product structures;
- the current OS product roadmap and end-of-life programme;
- OS NGD, Select+Build, Features, Tiles, Downloads, Places, Names, Linked Identifiers, routing-related products and address products;
- authentication mechanisms, including API keys and OAuth client credentials;
- whether OS offers user-delegated OAuth or only project/service credentials for relevant APIs;
- quotas, rate limits, caching rights, retention, redistribution, derived-data constraints and attribution;
- current and planned formats, APIs and schemas;
- implications of storing PSGA or commercial data in a shared service;
- entitlement brokerage between an authenticated user and organisation-owned OS credentials.

Do not assume that replacing a browser-visible API key with an OAuth token automatically creates user-level delegated authority. Explain the distinction between upstream provider authentication and the platform’s own user and policy authorisation.

### 7.2 ONS and statistical geography

Investigate:

- current ONS data APIs and their roadmaps;
- the new ONS website or data-platform work;
- ONS Geography and the Open Geography Portal;
- NOMIS;
- the Reference Data Management Framework;
- geography codes, versions, successors, boundaries and lookups;
- API-by-default and metadata strategies;
- licensing, fair-use restrictions and bulk-download options;
- statistical disclosure, suppression and uncertainty;
- UK-wide differences involving Scotland and Northern Ireland;
- the interaction between geography definitions, statistics and time.

### 7.3 LandIS

Investigate:

- the 2026 open-access transition and exact licences;
- the current public portal;
- NATMAP, Soilscapes, National Soil Inventory, SOILSERIES, HORIZON and interpreted products;
- OGC API – Records support and any other machine interfaces;
- bulk access, download and service limitations;
- provenance, scale, uncertainty and fitness-for-purpose warnings;
- whether the portal offers sufficient machine access or whether a local open cache is justified;
- the published roadmap or contractual service horizon where evidence is available.

### 7.4 HM Land Registry worked example

Use the current `okf-LandRegistry` implementation as a worked domain example.

Show how the successor could allow a human or an AI to:

1. discover relevant HMLR datasets, services, APIs and constraints;
2. search and facet the catalogue;
3. view relationships in graph, timeline and map forms;
4. inspect a richly linked data card;
5. identify which questions can be answered from HMLR alone;
6. identify where OS, ONS or LandIS enrichment is appropriate;
7. distinguish open and protected operations;
8. invoke a safe, deterministic query;
9. receive provenance, licence, freshness and policy evidence with the result.

Do not expose ownership or address-level information beyond what is lawfully public and justified by the worked scenario.

### 7.5 Provider matrix

Produce a provider matrix covering:

- authority;
- geographic scope;
- datasets and services;
- identifiers;
- update frequency;
- API and download mechanisms;
- formats;
- authentication;
- access tier;
- licence;
- caching and redistribution;
- attribution;
- expected longevity;
- known changes;
- data-quality limitations;
- cost;
- recommended integration method.

---

## 8. Contemporary geospatial architecture

Assess the current GIS landscape and select a coherent, minimal architecture rather than listing technologies.

Cover:

- PostGIS and spatial indexing;
- DuckDB Spatial and embedded analytics;
- GeoParquet and GeoArrow;
- GeoPackage;
- GeoJSON and its appropriate size limits;
- FlatGeobuf;
- PMTiles and Mapbox Vector Tiles;
- Cloud Optimised GeoTIFF;
- Zarr where genuinely relevant;
- STAC;
- OGC API – Features, Records, Tiles, Maps, Processes, Coverages and connected standards;
- legacy WFS/WMS compatibility;
- pygeoapi, GeoServer or equivalent service implementations;
- Martin, pg_tileserv, TiTiler or equivalent delivery components;
- MapLibre, OpenLayers and appropriate 3D options;
- browser-side spatial processing, including DuckDB-Wasm where justified;
- coordinate-reference systems, transformations and axis-order hazards;
- simplification, generalisation and scale;
- temporal geospatial data;
- topology and network routing;
- spatial joins between statistical, address, land, soil and property data.

Recommend:

- canonical internal representations;
- external result formats;
- when to stream, paginate, tile or create a downloadable artefact;
- when live APIs are preferable to caches;
- when object storage is preferable to PostGIS;
- how source-native attributes and identifiers remain accessible;
- how the system represents uncertainty and fitness for purpose.

Give special attention to UPRN, BLPU, USRN, TOID, OSID, ONS geography codes and temporal identifier changes.

---

## 9. Mapping geospatial concepts to MCP

Use the current final MCP specification and current stable extensions.

Determine how the following should map to MCP:

- datasets and collections;
- schemas;
- coordinate systems;
- code lists;
- geographies;
- dataset versions;
- licences;
- provider status;
- map styles;
- saved selections;
- long-running jobs;
- deterministic analysis operations;
- downloadable results;
- interactive maps;
- workflow definitions;
- policy and provenance records.

For each, decide whether it belongs principally in:

- Tools;
- Resources;
- Prompts;
- Tasks;
- MCP Apps;
- an external API;
- an OKF bundle;
- or more than one surface with a stated canonical authority.

Address:

- stateless requests;
- `server/discover`;
- per-request client metadata;
- `Mcp-Method` and `Mcp-Name` routing;
- deterministic and cacheable catalogue ordering;
- `ttlMs` and cache scope;
- Multi Round-Trip Requests;
- explicit state handles;
- Tasks for genuinely long-running operations;
- current MCP Apps metadata and lifecycle;
- Enterprise-Managed Authorization;
- client metadata documents and current OAuth expectations;
- W3C Trace Context;
- deprecated roots, sampling, logging and legacy SSE;
- compatibility with current ChatGPT, Claude, VS Code, Codex and other major hosts;
- official SDK maturity.

Compare at least:

1. a Python implementation based on the current official MCP SDK and Python geospatial ecosystem;
2. a TypeScript implementation based on the current official MCP SDK;
3. a TypeScript MCP/control gateway with a Python geospatial execution service;
4. another architecture only if it materially improves simplicity, assurance or performance.

Make one clear recommendation. Avoid a multi-language or microservice architecture unless its benefits justify the additional operational and assurance burden.

---

## 10. Tool and workflow design

Design a small, composable capability model.

Separate:

- discovery;
- description;
- selection;
- retrieval;
- deterministic spatial operations;
- statistics;
- routing;
- rendering;
- export;
- provenance;
- workflow execution.

Consider whether a compact set of generic, schema-rich operations is safer and more usable than many provider-specific tools.

Every proposed tool must define:

- name and namespace;
- purpose;
- read-only or mutating status;
- input schema;
- output schema;
- pagination or artefact behaviour;
- provider dependencies;
- access tier;
- policy-relevant attributes;
- cost and performance characteristics;
- risks;
- error codes;
- provenance fields;
- fallback behaviour;
- example calls;
- test cases.

Design a progressive-disclosure strategy so an AI sees only the tools relevant to the user, task, entitlements and current stage. Tool discovery itself must be policy-filtered; an unauthorised client should not necessarily learn that a protected tool or dataset exists.

Use explicit workflows for multi-step operations. Show where Arazzo, MCP Tasks, MRTR and human approval apply. Do not treat an LLM’s transient plan as the authoritative workflow definition.

---

## 11. OKF’s role

Establish the precise role of Open Knowledge Format.

Investigate and distinguish:

- normative OKF specification;
- experimental extensions;
- domain profiles;
- OKF Explorer implementation conventions;
- generated bundle formats;
- HMLR, ONS and API-domain examples.

Assess whether OKF should describe:

- providers;
- datasets;
- APIs;
- MCP servers;
- MCP tools and resources;
- workflows;
- licences;
- access tiers;
- policy references;
- identity and entitlement requirements;
- data lineage;
- transformations;
- quality;
- uncertainty;
- trust and authority;
- freshness and staleness;
- computational receipts;
- verification and attestation;
- examples and evaluations.

Preserve and test the following developing OKF ideas:

- structured sources and provenance;
- generated, verified and authoritative actors;
- trust tiers;
- lifecycle status and `stale_after`;
- canonical identifiers;
- forward compatibility;
- progressive disclosure;
- separate human summaries, indexes and detailed logs;
- attestable computation including runtime, parameters, executor, receipt and attester;
- a clear distinction between verification and attestation.

Design a mapping between OKF records and:

- MCP resources and capability metadata;
- OGC API – Records;
- STAC;
- DCAT and GeoDCAT;
- JSON-LD or YAML-LD;
- W3C PROV;
- ODRL or another suitable policy and licence vocabulary;
- OpenAPI, AsyncAPI and Arazzo.

Avoid forcing all source metadata into a lowest-common-denominator model. Preserve extensions and source-native evidence.

Specify how one OKF-backed information pack can serve:

- the left-hand search and facet controls;
- the central results, map, graph and timeline views;
- the selected item’s right-hand data card;
- AI discovery and retrieval;
- source citation;
- policy evaluation;
- the Codex implementation pack.

---

## 12. Identity, authentication and delegated authority

Treat bring-your-own API keys as an undesirable development convenience, not the production access model.

Design identities for:

- the human user;
- the organisation;
- the AI host;
- the agent;
- the MCP client;
- the calling application;
- the service workload;
- the upstream provider account.

Show how the actor chain is preserved across:

**human → AI host → agent → MCP client → MCP gateway/server → geospatial service → upstream provider**

Evaluate:

- OpenID Connect;
- OAuth 2.1;
- authorisation code with PKCE;
- workload identity and client credentials;
- token exchange and on-behalf-of patterns;
- sender-constrained tokens using DPoP or mutual TLS where appropriate;
- resource indicators and audience restriction;
- rich or transaction-specific authorisation;
- token introspection and revocation;
- enterprise federation;
- MCP Enterprise-Managed Authorization;
- Microsoft Entra ID and Conditional Access;
- Keycloak or another open-source identity option;
- relevant AWS and Google identity services;
- continuous access evaluation or shared security signals;
- managed identities and workload identity federation.

Do not trust a device-posture value merely because the client supplied it. Explain which trusted identity or security component attests posture, how it reaches the policy decision point, how current it is and what happens when posture changes during an operation.

Define a machine-readable **authority context** containing at least:

- actor;
- subject;
- organisation;
- role;
- agent;
- AI host;
- client;
- workload;
- device identity and posture;
- action;
- resource;
- dataset and attributes;
- purpose;
- legal authority;
- licence entitlement;
- geography or resolution constraints;
- risk tier;
- requested output;
- budget or quota;
- evidence references;
- policy version;
- approval;
- decision;
- obligations;
- expiry;
- trace identifier.

Design short-lived, transaction-bound permits for sensitive or expensive operations. A permit should bind the authorised actor, agent, action, resources, purpose, constraints, policy version and expiry rather than becoming a general bearer credential.

---

## 13. ABAC and policy enforcement

Role and device posture are minimum attributes, not the whole access model.

Design ABAC or a justified combination of ABAC and relationship-based access control covering:

### Subject and actor attributes

- organisation;
- employment or membership;
- role;
- accreditation;
- clearance;
- contractual entitlement;
- user risk;
- agent and application identity.

### Device and environmental attributes

- managed or unmanaged device;
- compliance state;
- authentication strength;
- network or location;
- time;
- threat or session risk.

### Resource attributes

- provider;
- dataset;
- record, field or feature type;
- licence tier;
- security classification;
- personal-data status;
- geography;
- spatial resolution;
- temporal version;
- freshness;
- commercial cost.

### Action attributes

- discover;
- view;
- query;
- intersect;
- join;
- route;
- export;
- download;
- cache;
- redistribute;
- derive;
- publish.

### Context and purpose attributes

- declared purpose;
- legal authority;
- project;
- policy outcome;
- emergency status;
- intended audience;
- output destination;
- aggregate versus record-level use.

Compare policy engines and models such as:

- Open Policy Agent and Rego;
- Cedar and AWS Verified Permissions;
- OpenFGA;
- SpiceDB;
- Keycloak authorisation services;
- cloud-native alternatives.

Select one principal model, while retaining portability where practical.

Define:

- Policy Administration Point;
- Policy Information Points;
- Policy Decision Point;
- Policy Enforcement Points;
- decision cache;
- policy versioning;
- test suite;
- change approval;
- rollback;
- emergency deny;
- evidence retention.

Enforcement must be considered at:

- discovery and search;
- MCP capability listing;
- workflow initiation;
- tool invocation;
- upstream credential selection;
- provider request;
- cache read;
- cache write;
- attribute projection;
- map and tile generation;
- export;
- redistribution;
- derived output;
- audit access.

An allow decision may carry obligations such as:

- attribution;
- maximum feature count;
- reduced resolution;
- aggregation;
- masking;
- watermarking;
- no persistent export;
- human approval;
- rate or cost limit;
- specified retention;
- specified destination;
- additional audit.

---

## 14. Caching and licensed data

Design caching as a governed subsystem, not merely a performance optimisation.

Cover:

- live query cache;
- reference-data cache;
- boundary and code cache;
- tile cache;
- object and download cache;
- derived-result cache;
- per-user or per-organisation artefacts;
- durable licensed replicas.

Every cache entry should be traceable to:

- provider;
- dataset and version;
- source URI or package;
- retrieval time;
- licence;
- entitlement context;
- policy version;
- transformation;
- source checksum;
- expiry;
- staleness;
- permitted audience;
- permitted operations.

Assess:

- physical versus logical separation of open, PSGA and commercial data;
- separate encryption keys;
- separate service identities;
- namespace and cache-key design;
- entitlement-sensitive cache keys;
- prevention of cross-user and cross-tier contamination;
- deletion and licence withdrawal;
- provider update detection;
- policy-driven invalidation;
- cache poisoning;
- stale-data fallbacks;
- outage operation;
- cost and egress;
- derived-data licensing.

Compare PostGIS, object storage, CDN caches, embedded GeoParquet/DuckDB datasets and provider APIs for different data classes.

Recommend data-volume assumptions for:

- personal prototype;
- departmental pilot;
- multi-organisation service;
- national-scale service.

---

## 15. WebMCP and the agent-ready website

Research WebMCP from current W3C and browser-vendor sources.

Do not conflate it with the Model Context Protocol. Establish:

- current specification status;
- browser support;
- current API shape;
- declarative and imperative mechanisms;
- security and privacy work;
- origin, iframe and document lifecycle;
- user consent and visibility;
- Permissions Policy and CSP implications;
- authentication and agent identity;
- evaluation guidance;
- fallback requirements;
- the likelihood and impact of API change.

Compare:

| Mechanism | Primary purpose |
|---|---|
| OKF | Structured knowledge, discovery, provenance and policy description |
| WebMCP | Page-provided tools for browser-resident agents |
| MCP | Remote or local AI-host access to tools and resources |
| MCP Apps | Server-provided interactive UI within supporting MCP hosts |
| OpenAPI/OGC API | Direct application and data-service contracts |
| Arazzo | Explicit multi-step API workflow description |
| Static JSON/JSON-LD | Portable, scrape-free machine-readable publication |

Design an open-data proof of concept in which the HMLR or OKF Explorer site exposes safe read-only operations such as:

- search catalogue;
- apply facets;
- inspect record;
- retrieve relationships;
- select map features;
- obtain the evidence and provenance for the current view;
- export the selected public records.

The same site should remain useful to:

- ordinary browsers;
- screen readers;
- browser agents supporting WebMCP;
- agents that can read linked machine-readable files;
- MCP clients using the separate remote MCP service.

Do not expose PSGA or commercial credentials or protected operations through browser-side JavaScript. Privileged operations must remain server-side and require authenticated, policy-governed calls.

Define a fallback hierarchy that is better than scraping or copy-and-paste.

---

## 16. MCP Apps and human presentation

Assess the current MCP Apps extension and host support.

Design presentation contracts for:

- map;
- feature or place inspector;
- geography selector;
- statistical comparison;
- provenance and evidence viewer;
- policy decision explanation;
- export review;
- approval request.

Each capability must also have a deterministic non-UI result for clients that do not support MCP Apps.

Do not permit a widget to become an ungoverned alternate API. Widget requests must use the same policy enforcement and evidence model as non-visual tool calls.

Preserve useful lessons from the current MCP-Geo map fallback and structured-content work, but assess whether the existing widget implementations should be migrated or rebuilt.

---

## 17. Hosting and deployment study

Compare at least the following deployment families:

### ChatGPT Sites

Assess:

- actual availability to a UK Pro account at the research date;
- public and restricted sharing;
- Sign in with ChatGPT;
- server-side identity headers;
- environment variables and secrets;
- D1 storage;
- R2 object storage;
- storage and usage limits;
- outbound API calls;
- custom domains;
- WebMCP support;
- response-header and CSP control;
- long-running and streaming requests;
- background work;
- portability and source export;
- private networks;
- data and inference residency;
- suitability for open, PSGA and commercial tiers.

Conduct only an open or synthetic-data experiment. Do not treat Sites as a production protected-data platform unless official evidence supports every required control.

### Microsoft Azure

Consider:

- Container Apps or App Service;
- Azure Database for PostgreSQL with PostGIS;
- Blob Storage and CDN;
- Entra ID;
- Conditional Access and device compliance;
- managed identities;
- API Management;
- Key Vault;
- Front Door;
- Monitor and OpenTelemetry;
- UK-region availability.

### Google Cloud

Consider:

- Cloud Run;
- Cloud SQL for PostgreSQL/PostGIS;
- Cloud Storage and CDN;
- Identity Platform or IAP;
- IAM and workload identity;
- Secret Manager;
- Apigee where justified;
- logging, tracing and policy integration;
- UK-region availability.

### AWS

Consider:

- ECS/Fargate, App Runner or Lambda where appropriate;
- RDS/Aurora PostgreSQL with PostGIS;
- S3 and CloudFront;
- Cognito or external OIDC;
- IAM;
- Verified Permissions and Cedar;
- API Gateway;
- Secrets Manager;
- audit and UK-region options.

### Cloudflare and static hosting

Consider:

- Pages, Workers or Containers;
- R2;
- D1;
- Access and Zero Trust;
- Hyperdrive or external PostgreSQL;
- CDN and edge map delivery;
- limitations for full geospatial processing.

### Other simple platforms

Assess only where they offer a meaningful reduction in complexity without undermining identity, data residency, audit or operational control.

For each option provide:

- supported architecture;
- open/PSGA/commercial suitability;
- OAuth and OIDC support;
- ABAC and device-posture integration;
- PostGIS and object-storage support;
- caching capacity;
- secrets;
- network isolation;
- UK residency;
- audit;
- scalability;
- operational burden;
- portability;
- indicative costs at prototype, pilot and production scale;
- principal risks.

Compare:

1. one shared multi-tier deployment;
2. a public static/discovery plane plus a separate protected MCP/data plane;
3. separate open, PSGA and commercial deployments sharing source code and policy definitions;
4. federated deployments operated by participating organisations.

Make one recommendation for the initial implementation and one credible route to production.

Avoid Kubernetes unless the evidence demonstrates that the expected workload or organisational environment justifies it.

---

## 18. Governance, assurance and UK public-sector requirements

Research current requirements and guidance relating to:

- UK GDPR and the Data Protection Act;
- current UK data legislation;
- purpose limitation and data minimisation;
- DPIAs;
- equality impact and accessibility;
- records management;
- Freedom of Information;
- public-sector information and data licensing;
- government security classifications;
- NCSC Cloud Security Principles;
- NCSC Cyber Assessment Framework where applicable;
- Government Service Standard;
- Technology Code of Practice;
- Open Standards Principles;
- algorithmic transparency requirements;
- AI governance and assurance;
- procurement and supplier assurance;
- incident response;
- retention and deletion.

Do not assume every geospatial query is harmless. Address:

- address and property information;
- critical national infrastructure;
- vulnerable-person locations;
- aggregation and inference risk;
- sensitive operational queries;
- commercially sensitive activity;
- user location and search history.

Define governance controls including:

- service and tool registry;
- owner and steward;
- risk classification;
- approval gates;
- policy testing;
- monitoring and evaluation;
- model or agent restrictions;
- credential revocation;
- tool or server suspension;
- agent quarantine;
- kill switch;
- evidence freeze;
- rollback;
- decommissioning;
- public transparency record.

---

## 19. Provenance, evidence and audit

Design an evidence model that can answer:

- who requested the operation;
- which agent and host acted;
- under whose authority;
- for what declared purpose;
- from what device and risk context;
- which policy version allowed or denied it;
- which approval or transaction permit applied;
- which tools, services and data versions were used;
- what exact spatial and statistical operations occurred;
- which transformations and CRS changes were made;
- what was returned, redacted or withheld;
- what licence and attribution obligations apply;
- whether the result was verified or attested;
- how to reproduce or challenge it.

Assess W3C PROV, OpenTelemetry and relevant geospatial metadata standards.

Define a canonical audit event and a result-level evidence receipt. Include:

- immutable identifiers;
- hashes;
- timestamps;
- source versions;
- policy-decision references;
- trace context;
- transformation parameters;
- software and runtime versions;
- output artefact references;
- attester;
- retention classification.

Avoid logging secrets, complete access tokens or unnecessary personal and sensitive query content. Explain how audit usefulness is balanced with privacy and security.

---

## 20. Threat model

Produce a structured threat model covering at least:

- prompt injection through dataset descriptions, records or upstream content;
- tool poisoning and misleading metadata;
- confused-deputy attacks;
- agent identity substitution;
- stolen or replayed tokens;
- bearer-token leakage;
- overbroad scopes;
- false device-posture claims;
- policy bypass;
- provider-credential misuse;
- SSRF;
- arbitrary URL fetch;
- data and licence exfiltration;
- cross-tenant or cross-tier leakage;
- cache poisoning;
- stale or revoked entitlement;
- malicious geometries and pathological spatial queries;
- decompression and archive bombs;
- expensive-query denial of service;
- map or tile abuse;
- widget and WebMCP origin attacks;
- provenance spoofing;
- audit tampering;
- derived-data inference;
- supply-chain compromise;
- dependency and container vulnerabilities.

For each threat identify:

- asset;
- actor;
- path;
- likelihood;
- impact;
- preventive controls;
- detective controls;
- response;
- residual risk;
- test.

Use attack trees or data-flow-based threat modelling as appropriate.

---

## 21. Evaluation suite and worked scenarios

Harvest useful questions and failures from the current repository and create a new evaluation suite.

Include at least these scenarios:

1. An anonymous user discovers open boundary and statistics data.
2. An anonymous AI uses the public site without scraping.
3. A local-government analyst asks which current and historic geographies contain a coordinate.
4. A PSGA user on a compliant managed device requests protected OS detail.
5. The same user from an unmanaged or non-compliant device is denied or safely downgraded.
6. An agent acts on behalf of a named user with a short-lived transaction permit.
7. A service workload performs an approved cache refresh.
8. A commercial user receives only contractually entitled data.
9. A query combines HMLR, ONS and LandIS open data with full provenance.
10. A protected OS layer enriches an open result without leaking protected features into the public cache.
11. An upstream provider is unavailable and an approved cache is used with a freshness warning.
12. A provider licence or policy changes and affected caches and capabilities are invalidated.
13. An MCP host without Apps support receives a complete non-visual result.
14. A WebMCP-capable browser agent uses safe page tools.
15. A WebMCP-incapable agent follows the linked OKF or API surface.
16. A high-volume export triggers approval or denial.
17. A malicious record attempts prompt injection.
18. A malicious client attempts to claim false role or posture attributes.
19. A policy decision is challenged and reconstructed from evidence.
20. A tool or provider is suspended through an emergency control.

Evaluate:

- factual correctness;
- tool selection;
- policy compliance;
- licence compliance;
- provenance completeness;
- reproducibility;
- latency;
- cache behaviour;
- cost;
- accessibility;
- client interoperability;
- graceful degradation.

---

## 22. Naming the successor

The successor needs a new name because its purpose is broader than the existing MCP-Geo learning repository.

Generate at least 20 candidates and shortlist five.

The name should:

- suggest spatial knowledge, governed access or trustworthy action;
- remain suitable if MCP is later only one interface among several;
- not imply that the service is operated or endorsed by OS, ONS, HMLR, Defra or UK Government;
- avoid an unnecessarily narrow provider or technology reference;
- be pronounceable and memorable;
- work as a repository, package and service name;
- have no obvious conflicting geospatial, AI or software product;
- have reasonable namespace availability.

Check:

- GitHub;
- package registries relevant to the recommended stack;
- common web search usage;
- UK trademarks where proportionate;
- plausible domain names.

Recommend one name, explain its meaning and provide a safe working codename if final legal clearance would still be required.

---

## 23. Required conclusions and decisions

The research must make explicit decisions on:

1. the product’s identity and boundaries;
2. the six-control architecture;
3. the role of OKF;
4. MCP primitive mapping;
5. the tool and workflow model;
6. the current MCP protocol and SDK target;
7. the WebMCP adoption level;
8. the MCP Apps approach;
9. authentication and delegated authority;
10. ABAC and policy engine;
11. device-posture integration;
12. the three-tier access and cache model;
13. canonical geospatial storage and formats;
14. live API versus cache strategy;
15. hosting for the open demonstrator;
16. hosting path for protected production;
17. language and runtime;
18. repository reset and migration strategy;
19. minimum viable scope;
20. project name.

For every decision provide:

- options considered;
- evidence;
- benefits;
- disadvantages;
- risks;
- cost and complexity;
- reversibility;
- recommendation;
- confidence;
- conditions that would change the decision.

Do not end with several equally preferred architectures. Select a coherent default.

---

## 24. Interactive research pack

Produce or fully specify this structure:

```text
research-pack/
├── index.html
├── README.md
├── assets/
│   ├── css/
│   ├── js/
│   └── diagrams/
├── data/
│   ├── research.okf.json
│   ├── sources.json
│   ├── findings.json
│   ├── requirements.json
│   ├── decisions.json
│   ├── risks.json
│   ├── controls.json
│   ├── providers.json
│   ├── standards.json
│   ├── hosting-options.json
│   ├── tool-catalogue.json
│   ├── workflows.json
│   ├── evaluation-cases.json
│   └── name-candidates.json
├── report/
│   ├── 00-executive-decision.md
│   ├── 01-current-state-and-harvest.md
│   ├── 02-landscape.md
│   ├── 03-provider-analysis.md
│   ├── 04-target-architecture.md
│   ├── 05-okf-and-discovery.md
│   ├── 06-mcp-and-webmcp.md
│   ├── 07-identity-policy-and-licensing.md
│   ├── 08-data-cache-and-mapping.md
│   ├── 09-hosting.md
│   ├── 10-threat-model-and-assurance.md
│   ├── 11-evaluation.md
│   └── 12-roadmap-and-recommendation.md
├── architecture/
│   ├── context.mmd
│   ├── containers.mmd
│   ├── components.mmd
│   ├── six-control-spine.mmd
│   ├── open-tier-sequence.mmd
│   ├── protected-tier-sequence.mmd
│   ├── delegated-agent-sequence.mmd
│   ├── webmcp-sequence.mmd
│   └── evidence-flow.mmd
├── schemas/
│   ├── authority-context.schema.json
│   ├── policy-decision.schema.json
│   ├── evidence-receipt.schema.json
│   ├── provider.schema.json
│   ├── tool-profile.schema.json
│   └── workflow-profile.schema.json
└── codex/
    ├── CODEX_HANDOFF.md
    ├── PRD.md
    ├── TECHNICAL_SPEC.md
    ├── ARCHITECTURE_DECISIONS.md
    ├── IMPLEMENTATION_PLAN.md
    ├── BACKLOG.md
    ├── AGENTS.md
    ├── ACCEPTANCE_TESTS.md
    ├── MIGRATION_HARVEST.md
    ├── REPOSITORY_TREE.txt
    └── SITES_BUILD_PROMPT.md
```

The interactive site should provide:

- full-text search;
- facets by topic, organisation, maturity, authority, access tier, standard and recommendation;
- graph, timeline and map views;
- side-by-side option comparison;
- provider and hosting matrices;
- a selected-item data card;
- direct evidence links;
- visible confidence and maturity;
- architecture-diagram navigation;
- filtering of accepted, rejected and deferred decisions;
- export of selected records;
- accessible keyboard operation;
- responsive layout;
- WCAG 2.2 AA design.

Prefer relative links and portable assets. Avoid a mandatory server or build process for the published research pack unless a clear benefit justifies it.

Where OKF Explorer can provide this experience, create a conforming bundle and specify any Explorer changes required. Where the research environment cannot emit the complete static site, provide all data, schemas and the exact `SITES_BUILD_PROMPT.md` needed to create it.

---

## 25. Codex implementation handoff

The Codex pack must be sufficiently precise that Codex can create the new repository without redoing the architectural research.

It must include:

- product objective;
- users and journeys;
- scope and non-goals;
- selected stack;
- repository structure;
- component contracts;
- deployment topology;
- identity and policy flows;
- provider adapter interface;
- cache architecture;
- OKF profile;
- MCP tools, resources and workflows;
- WebMCP and MCP Apps boundaries;
- environment and secret model;
- local-development approach;
- CI/CD;
- infrastructure as code;
- observability;
- threat controls;
- test strategy;
- migration harvest;
- staged backlog;
- acceptance criteria;
- decision records.

Divide implementation into independently verifiable stages:

### Stage 0 — Repository and evidence foundation

New repository, governance files, architecture decisions, schemas, test harness and source ledger.

### Stage 1 — Open static discovery pack

OKF bundle, Explorer experience, public HMLR worked example, linked machine-readable files and optional safe WebMCP experiment.

### Stage 2 — Open MCP service

Current final MCP protocol, small read-only tool surface, provenance receipts, public data adapters and deterministic map fallbacks.

### Stage 3 — Identity and policy

OIDC/OAuth, trusted actor chain, policy engine, filtered discovery, transaction permits, decision evidence and test identities.

### Stage 4 — PSGA protected pilot

Organisation entitlement, OS credential broker, managed-device posture, separated protected cache and human approval for risky exports.

### Stage 5 — Commercial and multi-organisation model

Contract entitlement, quotas, cost controls, tenant isolation and commercial licensing safeguards.

### Stage 6 — Production assurance

Operational controls, red-team tests, performance, disaster recovery, transparency, accessibility, security review and deployment evidence.

Every stage must have entry criteria, deliverables, tests, exit criteria and rollback.

---

## 26. Work-mode assessment

Before the executive conclusion, assess the most effective combination of current OpenAI and development capabilities for completing the project.

Compare:

- Deep Research for current, cited evidence synthesis;
- GitHub-connected repository analysis;
- ChatGPT Sites for the public interactive research pack;
- Codex for repository creation and implementation;
- Codex Security for threat-model-informed scanning and later review;
- conventional notebooks or dashboards where quantitative comparison requires them.

Determine whether any newer capability replaces Deep Research for this commission.

Do not assume one tool must perform every stage. Recommend an integrated workflow and specify the artefact passed between stages.

---

## 27. Acceptance criteria

The research is complete only when:

- current official sources have been checked;
- repository commits and versions are recorded;
- facts, assumptions and recommendations are visibly distinct;
- the MCP final release and stable extensions are correctly reflected;
- WebMCP is neither dismissed nor treated as production-stable without evidence;
- OS, ONS, NOMIS, LandIS and HMLR are analysed separately;
- open, PSGA and commercial tiers are fully modelled;
- role and trusted device posture are enforced as minimum policy attributes;
- no production design depends on browser-supplied API keys;
- no secret or licensed data enters the public research pack;
- every protected operation has an attributable authority chain;
- discovery as well as invocation is policy-aware;
- caching is licence-aware and provenance-preserving;
- every material result can produce an evidence receipt;
- at least one coherent target architecture is selected;
- the hosting recommendation includes an exit strategy;
- the new name is researched and recommended;
- the interactive pack is portable;
- the machine-readable files validate;
- Mermaid or equivalent diagrams render;
- Codex can start implementation from the handoff without repeating the research;
- unresolved uncertainty is explicit rather than hidden.

End with:

1. a one-page executive recommendation;
2. the target architecture;
3. the recommended project name;
4. a “build now / prepare next / defer” table;
5. the first 30 days of implementation;
6. the top ten risks;
7. the exact artefact to give Codex first.