# Implementation plan

## Stage 0 — repository and evidence foundation

**Entry:** human authorises new repository and accepts D01–D20.  
**Deliver:** governance files, workspace, schemas, ADRs, source ledger, synthetic fixtures, CI, test harness, diagrams.  
**Tests:** schema/source/link/secret/SBOM/unit/diagram.  
**Exit:** exact commit and clean verification report.  
**Rollback:** revert/delete unshared new repository; MCP-Geo remains untouched.

## Stage 1 — open static discovery pack

**Entry:** Stage 0 approved; HMLR public-source/rights review.  
**Deliver:** OKF bundle, static Explorer, public HMLR example, linked machine files, optional read-only WebMCP.  
**Tests:** search/facets/map/graph/timeline/data card, integrity and WCAG.  
**Exit:** immutable published artefact receipt.  
**Rollback:** republish previous artefact.

## Stage 2 — open MCP service

**Entry:** Stage 1 approved; MCP host matrix.  
**Deliver:** gateway/execution boundary, first open adapters, receipts and non-App map fallback.  
**Tests:** protocol/provider/security/reproducibility/host.  
**Exit:** open read-only service candidate.  
**Rollback:** unregister/suspend remote service.

## Stages 3–6

Proceed exactly as described in [`../report/12-roadmap-and-recommendation.md`](../report/12-roadmap-and-recommendation.md), with a human gate after every stage.
