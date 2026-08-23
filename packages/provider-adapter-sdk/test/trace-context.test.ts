import assert from "node:assert/strict";
import test from "node:test";

import {
  normaliseW3CTraceContext,
  w3cTraceId,
} from "../src/index.js";

const TRACE_ID = "7123456789abcdef0123456789abcdef";
const TRACE = Object.freeze({
  traceparent: `00-${TRACE_ID}-89abcdef01234567-ff`,
  tracestate: "\t,0gov@uk=public-read ,ons=weekly-deaths, ",
});

test("validates and copies bounded W3C Trace Context Level 2", () => {
  const validated = normaliseW3CTraceContext(TRACE, TRACE_ID);
  assert.deepEqual(validated, TRACE);
  assert.notEqual(validated, TRACE);
  assert.equal(Object.isFrozen(validated), true);
  assert.equal(w3cTraceId(validated), TRACE_ID);

  for (const flags of ["00", "01", "02", "03", "fe"] as const) {
    assert.equal(
      normaliseW3CTraceContext({
        traceparent: `00-${TRACE_ID}-89abcdef01234567-${flags}`,
        tracestate: "",
      }).traceparent.endsWith(flags),
      true,
    );
  }
});

test("rejects invalid, ambiguous and hostile Trace Context", () => {
  for (const candidate of [
    null,
    [],
    new Proxy(TRACE, {}),
    { traceparent: `ff-${TRACE_ID}-89abcdef01234567-01` },
    { traceparent: `00-${"0".repeat(32)}-89abcdef01234567-01` },
    { traceparent: `00-${TRACE_ID}-${"0".repeat(16)}-01` },
    { traceparent: `00-${TRACE_ID}-89abcdef01234567-0F` },
    { traceparent: `${TRACE.traceparent}\n` },
    { traceparent: TRACE.traceparent, tracestate: "govuk=one, govuk=two" },
    { traceparent: TRACE.traceparent, tracestate: ",".repeat(32) },
    { traceparent: TRACE.traceparent, tracestate: "@govuk=invalid" },
    { traceparent: TRACE.traceparent, tracestate: `govuk=${"x".repeat(257)}` },
    { traceparent: TRACE.traceparent, tracestate: " ".repeat(513) },
    { traceparent: TRACE.traceparent, tracestate: "GovUK=uppercase" },
    { traceparent: TRACE.traceparent, tracestate: "govuk=value\n" },
    { traceparent: TRACE.traceparent, tracestate: "govuk=one", baggage: "not-allowed" },
  ]) {
    assert.throws(() => normaliseW3CTraceContext(candidate), /Trace Context|trace/u);
  }
  assert.throws(
    () => normaliseW3CTraceContext(TRACE, "8123456789abcdef0123456789abcdef"),
    /traceparent/u,
  );

  let getterCalls = 0;
  const accessor = Object.defineProperty({}, "traceparent", {
    enumerable: true,
    get: () => {
      getterCalls += 1;
      return TRACE.traceparent;
    },
  });
  assert.throws(() => normaliseW3CTraceContext(accessor), /Trace Context/u);
  assert.equal(getterCalls, 0);
});
