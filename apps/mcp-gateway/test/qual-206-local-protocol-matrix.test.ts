import assert from "node:assert/strict";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";
import test, { type TestContext } from "node:test";

import {
  InMemoryTransport,
  type JSONRPCMessage,
} from "@modelcontextprotocol/server";

import {
  openEvidenceReconciliationIndex,
  openPublicEvidenceLedger,
} from "@gis-ai-go/evidence";
import { createOnsDataApiAdapter } from "@gis-ai-go/provider-adapter-sdk";

import { loadCatalogueSnapshot } from "../src/catalogue-snapshot.js";
import {
  createGovernedCandidateAssembly,
  type GovernedCandidateAssembly,
  type GovernedCandidateOperation,
  type GovernedCandidateSuspension,
} from "../src/governed-assembly.js";
import {
  MCP_CATALOGUE_RECORD_URI_TEMPLATE,
  MCP_EVIDENCE_RECEIPT_URI_TEMPLATE,
  MCP_PROTOCOL_VERSION,
  MCP_PUBLIC_CATALOGUE_URI,
} from "../src/mcp-server.js";
import { startGovernedCandidateStdio } from "../src/mcp-stdio.js";

const SOURCE_CATALOGUE = fileURLToPath(
  new URL("../../../../artifacts/okf/", import.meta.url),
);
const SNAPSHOT = await loadCatalogueSnapshot(SOURCE_CATALOGUE, {
  now: new Date("2026-08-23T12:00:00.000Z"),
});
const META = Object.freeze({
  "io.modelcontextprotocol/protocolVersion": MCP_PROTOCOL_VERSION,
  "io.modelcontextprotocol/clientCapabilities": Object.freeze({}),
  "io.modelcontextprotocol/clientInfo": Object.freeze({
    name: "gis-ai-go-local-suspension-transcript",
    version: "1.0.0",
  }),
});

interface SuspensionScenario {
  readonly label: string;
  readonly lifecycle: {
    readonly discovery: "active" | "suspended";
    readonly invocation: "active" | "suspended";
    readonly reason: string;
  };
  readonly suspendedTools?: readonly GovernedCandidateOperation[];
  readonly expectedOperations: readonly GovernedCandidateOperation[];
  readonly expectedSuspensions: readonly GovernedCandidateSuspension[];
}

const ACTIVE_LIFECYCLE = Object.freeze({
  discovery: "active",
  invocation: "active",
  reason: "Exact local suspension transcript fixture.",
} as const);

const SCENARIOS = Object.freeze([
  {
    label: "provider-discovery",
    lifecycle: {
      discovery: "suspended",
      invocation: "active",
      reason: "Local discovery suspension fixture.",
    },
    expectedOperations: [
      "catalogue.search",
      "catalogue.describe",
      "evidence.inspect",
    ],
    expectedSuspensions: [
      { operation: "selection.resolve", source: "provider-discovery" },
      { operation: "data.query", source: "provider-discovery" },
    ],
  },
  {
    label: "provider-invocation",
    lifecycle: {
      discovery: "active",
      invocation: "suspended",
      reason: "Local invocation suspension fixture.",
    },
    expectedOperations: [
      "catalogue.search",
      "catalogue.describe",
      "selection.resolve",
      "evidence.inspect",
    ],
    expectedSuspensions: [
      { operation: "data.query", source: "provider-invocation" },
    ],
  },
  ...([
    ["catalogue.search", [
      "catalogue.describe",
      "selection.resolve",
      "data.query",
      "evidence.inspect",
    ]],
    ["catalogue.describe", [
      "catalogue.search",
      "selection.resolve",
      "data.query",
      "evidence.inspect",
    ]],
    ["selection.resolve", [
      "catalogue.search",
      "catalogue.describe",
      "data.query",
      "evidence.inspect",
    ]],
    ["data.query", [
      "catalogue.search",
      "catalogue.describe",
      "selection.resolve",
      "evidence.inspect",
    ]],
  ] as const).map(([operation, expectedOperations]) => ({
    label: `explicit-${operation}`,
    lifecycle: ACTIVE_LIFECYCLE,
    suspendedTools: [operation],
    expectedOperations,
    expectedSuspensions: [
      { operation, source: "explicit-tool-suspension" as const },
    ],
  })),
  {
    label: "explicit-evidence.inspect",
    lifecycle: ACTIVE_LIFECYCLE,
    suspendedTools: ["evidence.inspect"],
    expectedOperations: [
      "catalogue.search",
      "catalogue.describe",
      "selection.resolve",
    ],
    expectedSuspensions: [
      { operation: "data.query", source: "required-evidence-operation" },
      { operation: "evidence.inspect", source: "explicit-tool-suspension" },
    ],
  },
] satisfies readonly SuspensionScenario[]);

function nextMessage(transport: InMemoryTransport): Promise<JSONRPCMessage> {
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(
      () => reject(new Error("Timed out waiting for local suspension reply")),
      2_000,
    );
    transport.onmessage = (message) => {
      clearTimeout(timeout);
      resolve(message);
    };
  });
}

async function exchange(
  transport: InMemoryTransport,
  message: JSONRPCMessage,
): Promise<JSONRPCMessage> {
  const reply = nextMessage(transport);
  await transport.send(message);
  return reply;
}

function result(message: JSONRPCMessage): Record<string, unknown> {
  assert.equal("result" in message, true, JSON.stringify(message));
  if (!("result" in message)) return {};
  assert.equal(typeof message.result, "object");
  assert.notEqual(message.result, null);
  return message.result as Record<string, unknown>;
}

function error(message: JSONRPCMessage): Record<string, unknown> {
  assert.equal("error" in message, true, JSON.stringify(message));
  if (!("error" in message)) return {};
  return message.error as unknown as Record<string, unknown>;
}

function createScenarioAssembly(
  t: TestContext,
  scenario: SuspensionScenario,
): {
  readonly assembly: GovernedCandidateAssembly;
  readonly providerCalls: () => number;
} {
  const root = mkdtempSync(join(tmpdir(), "gis-ai-go-local-suspension-"));
  t.after(() => rmSync(root, { recursive: true, force: true }));
  const ledger = openPublicEvidenceLedger({
    rootDirectory: join(root, "ledger"),
    retentionDays: 365,
    now: () => new Date("2026-08-23T12:00:01.000Z"),
  });
  const reconciliationIndex = openEvidenceReconciliationIndex({
    rootDirectory: join(root, "reconciliation"),
    ledger,
    now: () => new Date("2026-08-23T12:00:02.000Z"),
  });
  let calls = 0;
  const adapter = createOnsDataApiAdapter({
    lifecycle: scenario.lifecycle,
    transport: async () => {
      calls += 1;
      throw new Error("A suspended STDIO call must not reach provider transport");
    },
    now: () => Date.parse("2030-01-01T00:00:00.000Z"),
  });
  return {
    assembly: createGovernedCandidateAssembly({
      snapshot: SNAPSHOT,
      evidenceLedger: ledger,
      reconciliationIndex,
      adapter,
      now: () => new Date("2026-08-23T12:00:00.000Z"),
      ...(scenario.suspendedTools === undefined
        ? {}
        : { suspendedTools: scenario.suspendedTools }),
    }),
    providerCalls: () => calls,
  };
}

test("keeps every governed suspension absent and uncallable over in-process STDIO", async (t) => {
  for (const [scenarioIndex, scenario] of SCENARIOS.entries()) {
    await t.test(scenario.label, async (t) => {
      const { assembly, providerCalls } = createScenarioAssembly(t, scenario);
      assert.equal(assembly.state, "candidate-unregistered");
      assert.equal(assembly.productionRegistration, false);
      assert.deepEqual(assembly.operations, scenario.expectedOperations);
      assert.deepEqual(assembly.suspensions, scenario.expectedSuspensions);

      const [clientTransport, serverTransport] =
        InMemoryTransport.createLinkedPair();
      await clientTransport.start();
      const handle = startGovernedCandidateStdio(assembly, {
        transport: serverTransport,
      });
      t.after(async () => {
        await handle.close();
        await clientTransport.close();
      });

      const idBase = scenarioIndex * 100;
      const discovery = result(await exchange(clientTransport, {
        jsonrpc: "2.0",
        id: idBase + 1,
        method: "server/discover",
        params: { _meta: META },
      }));
      assert.deepEqual(discovery.supportedVersions, [MCP_PROTOCOL_VERSION]);

      const listing = result(await exchange(clientTransport, {
        jsonrpc: "2.0",
        id: idBase + 2,
        method: "tools/list",
        params: { _meta: META },
      }));
      const listed = (listing.tools as { readonly name: string }[])
        .map(({ name }) => name)
        .sort();
      assert.deepEqual(listed, [...scenario.expectedOperations].sort());

      const resources = result(await exchange(clientTransport, {
        jsonrpc: "2.0",
        id: idBase + 3,
        method: "resources/list",
        params: { _meta: META },
      }));
      assert.deepEqual(
        (resources.resources as { readonly uri: string }[]).map(({ uri }) => uri),
        assembly.mcpResources.includes("catalogue.public")
          ? [MCP_PUBLIC_CATALOGUE_URI]
          : [],
      );

      const templates = result(await exchange(clientTransport, {
        jsonrpc: "2.0",
        id: idBase + 4,
        method: "resources/templates/list",
        params: { _meta: META },
      }));
      assert.deepEqual(
        (templates.resourceTemplates as { readonly uriTemplate: string }[])
          .map(({ uriTemplate }) => uriTemplate),
        [
          ...(assembly.mcpResources.includes("catalogue.record")
            ? [MCP_CATALOGUE_RECORD_URI_TEMPLATE]
            : []),
          ...(assembly.mcpResources.includes("evidence.receipt")
            ? [MCP_EVIDENCE_RECEIPT_URI_TEMPLATE]
            : []),
        ],
      );

      const validOperation = assembly.operations.some(
        (operation) => operation === "catalogue.search",
      )
        ? "catalogue.search"
        : "catalogue.describe";
      const valid = result(await exchange(clientTransport, {
        jsonrpc: "2.0",
        id: idBase + 5,
        method: "tools/call",
        params: {
          _meta: META,
          name: validOperation,
          arguments: validOperation === "catalogue.search"
            ? { query: "INSPIRE", limit: 1 }
            : { record_id: "LR-Q003" },
        },
      }));
      assert.equal(valid.isError, undefined);
      const structured = valid.structuredContent as Record<string, unknown>;
      assert.equal(structured.operation, validOperation);
      assert.deepEqual(valid.content, [{
        type: "text",
        text: JSON.stringify(structured),
      }]);

      for (const [offset, suspension] of assembly.suspensions.entries()) {
        assert.equal(listed.includes(suspension.operation), false);
        const rejected = error(await exchange(clientTransport, {
          jsonrpc: "2.0",
          id: idBase + 10 + offset,
          method: "tools/call",
          params: {
            _meta: META,
            name: suspension.operation,
            arguments: {},
          },
        }));
        assert.deepEqual(rejected, {
          code: -32_602,
          message: `Tool ${suspension.operation} not found`,
        });
      }
      assert.equal(providerCalls(), 0);
    });
  }
});
