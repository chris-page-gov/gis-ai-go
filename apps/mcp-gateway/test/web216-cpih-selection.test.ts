import assert from "node:assert/strict";
import test from "node:test";
import { contentAddress } from "@gis-ai-go/evidence";
import {
  normaliseWeb216CpihQueryProposal,
  resolveWeb216CpihSelection,
  Web216CpihSelectionError,
} from "../src/web216-cpih-selection.js";

// Deliberately constructed synthetic correlation input, not a credential.
const KEY = ["gis-ai-go", "ik", "v1", "9".repeat(64)].join(":");

test("both exact periods resolve distinct non-authorising immutable proposals", () => {
  const january = resolveWeb216CpihSelection({ period: "2026-01" });
  const july = resolveWeb216CpihSelection({ period: "2026-07" });
  assert.notEqual(january.plan_id, july.plan_id);
  for (const plan of [january, july]) {
    assert.equal(plan.nature, "proposal-not-execution-authority");
    assert.equal(plan.authority.grants_execution, false);
    assert.equal(plan.authority.grants_provider_permission, false);
    assert.equal(plan.authority.requires_durable_receipt, true);
    assert.equal(plan.resource.cdid, "L522");
    assert.equal(plan.resource.dataset_id, "MM23");
    assert.equal(plan.measure.kind, "index-not-percentage");
    assert.equal(plan.measure.base_year, 2015);
    assert.equal(Object.isFrozen(plan.authority), true);
    assert.equal(Object.hasOwn(plan.resource, "edition"), false);
    assert.equal(Object.hasOwn(plan.resource, "version"), false);
  }
});

test("only explicit supported periods and closed source-independent arguments are accepted", () => {
  for (const input of [null, [], "2026-07", {}, { period: "latest" }, { period: "2026-08" },
    { period: "2026-07", url: "https://example.org" }, { period: "2026-07", authority: "allow" },
    { period: "2026-07", projection: {} }, { period: "2026-07", provider: "ons" }]) {
    assert.throws(() => resolveWeb216CpihSelection(input), Web216CpihSelectionError);
  }
});

test("consistent query proposals remain proposals and do not expose a caller policy slot", () => {
  const plan = resolveWeb216CpihSelection({ period: "2026-07" });
  const input = { period: "2026-07", selection_plan_id: plan.plan_id, idempotency_key: KEY };
  assert.deepEqual(normaliseWeb216CpihQueryProposal(input), input);
  assert.equal(Object.isFrozen(normaliseWeb216CpihQueryProposal(input)), true);
  for (const extra of ["authority", "policy", "provider_url", "capture_path", "result", "software"]) {
    assert.throws(() => normaliseWeb216CpihQueryProposal({ ...input, [extra]: "allow" }), Web216CpihSelectionError);
  }
});

test("foreign-period, missing and rehashed altered plans never match the server proposal", () => {
  const july = resolveWeb216CpihSelection({ period: "2026-07" });
  const january = resolveWeb216CpihSelection({ period: "2026-01" });
  const { plan_id: _old, ...core } = july;
  const altered = { ...core, resource: { ...core.resource, cdid: "D7G7" } };
  const forged = contentAddress("gis-ai-go:web216-cpih-selection-plan", "gis-ai-go.web216-cpih-selection-plan.v1", altered);
  for (const id of [january.plan_id, forged, "", null, "x".repeat(500)]) {
    assert.throws(() => normaliseWeb216CpihQueryProposal({
      period: "2026-07", selection_plan_id: id, idempotency_key: KEY,
    }), Web216CpihSelectionError);
  }
});

test("bad correlation keys and unsafe JSON fail without echoing supplied content", () => {
  const plan = resolveWeb216CpihSelection({ period: "2026-01" });
  for (const value of [null, "", "x".repeat(1000), 1, "invalid secret text", `gis-ai-go:ik:v1:${"0".repeat(64)}`]) {
    assert.throws(() => normaliseWeb216CpihQueryProposal({
      period: "2026-01", selection_plan_id: plan.plan_id, idempotency_key: value,
    }), (error: unknown) => error instanceof Web216CpihSelectionError && error.message === new Web216CpihSelectionError().message);
  }
  assert.throws(() => resolveWeb216CpihSelection({ get period() { throw Error("must not execute"); } }), Web216CpihSelectionError);
  assert.throws(() => resolveWeb216CpihSelection({ period: undefined }), Web216CpihSelectionError);
});
