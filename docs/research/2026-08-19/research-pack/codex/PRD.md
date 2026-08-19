# Product requirements document: Locus Accord

## Problem

People and AI agents need to discover and combine authoritative UK geospatial/statistical knowledge and perform deterministic actions without losing provider semantics, identity, licence, policy, provenance or human control.

## Users

Anonymous public user; local/central-government analyst; PSGA user; commercial customer; data steward; policy/security administrator; developer; interactive human; delegated agent; scheduled workload; auditor/investigator.

## Outcomes

- find the right provider/dataset/version and understand alternatives;
- know authority, freshness, quality, uncertainty, rights and fitness;
- invoke a small deterministic action set under attributable authority;
- receive complete evidence and an accessible human view;
- deny, downgrade, approve, suspend, revoke and reconstruct operations.

## Scope

Stages 0–2: public/synthetic knowledge pack and read-only open MCP. Stages 3–6 are gated. The accepted requirements are canonical in [`../data/requirements.json`](../data/requirements.json).

## Success measures

25 evaluation cases; 100% policy/receipt/isolation/secret/accessibility critical gates; deterministic frozen-fixture repeatability; measured host interoperability; no protected bytes in public artefacts.

## Non-goals

System-of-record replacement; licence resale; browser keys; arbitrary fetch/code; autonomous legal/ownership/safety decisions; national-scale promise in the MVP.
