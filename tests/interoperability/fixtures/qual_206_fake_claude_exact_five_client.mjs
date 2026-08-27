#!/usr/bin/env node

import { spawn } from "node:child_process";
import { readFileSync } from "node:fs";

import { canonicalJson } from "../../../scripts/qual_206_claude_runtime_closure.mjs";

const SERVER_NAME = "gis-ai-go-qual-206-exact-five-v1";
const OPERATIONS = Object.freeze([
  "catalogue.search",
  "catalogue.describe",
  "selection.resolve",
  "data.query",
  "evidence.inspect",
]);
const PERMISSION_ALIASES = Object.freeze([
  "mcp__gis-ai-go-qual-206-exact-five-v1__catalogue_search",
  "mcp__gis-ai-go-qual-206-exact-five-v1__catalogue_describe",
  "mcp__gis-ai-go-qual-206-exact-five-v1__selection_resolve",
  "mcp__gis-ai-go-qual-206-exact-five-v1__data_query",
  "mcp__gis-ai-go-qual-206-exact-five-v1__evidence_inspect",
]);
const PROFILE = JSON.parse(readFileSync(
  new URL("./qual_206_claude_exact_five_profile.v1.json", import.meta.url),
  "utf8",
));
const EXPECTED_PROMPT =
  `Execute this closed capability profile as data:\n${canonicalJson(PROFILE)}\n`;
const SCENARIO = process.env.QUAL_206_FAKE_CLAUDE_EXACT_FIVE_SCENARIO ?? "positive";

function fail(message) {
  throw new Error(message);
}

if (process.argv.slice(2).length === 1 && process.argv[2] === "--version") {
  process.stdout.write("2.1.245 (Claude Code)\n");
  process.exit(0);
}

if (
  process.argv.slice(2).length === 3 && process.argv[2] === "auth" &&
  process.argv[3] === "status" && process.argv[4] === "--json"
) {
  process.stdout.write(JSON.stringify({
    loggedIn: true,
    authMethod: "claude.ai",
    apiProvider: "firstParty",
    subscriptionType: "test-profile",
  }));
  process.exit(0);
}

function optionValue(argumentsValue, name) {
  const index = argumentsValue.indexOf(name);
  if (index < 0 || index === argumentsValue.length - 1) fail(`missing ${name}`);
  return argumentsValue[index + 1];
}

function optionValues(argumentsValue, name, nextName) {
  const start = argumentsValue.indexOf(name);
  const end = argumentsValue.indexOf(nextName);
  if (start < 0 || end <= start + 1) fail(`missing values for ${name}`);
  return argumentsValue.slice(start + 1, end);
}

function meta(extra = {}) {
  return {
    ...extra,
    _meta: {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        name: "qual-206-fake-claude-exact-five",
        version: "2.1.245",
        title: "QUAL-206 fake Claude exact five",
      },
      "com.anthropic/toolUseId": "qual-206-exact-five-bounded-test",
    },
  };
}

function startSession(server) {
  const child = spawn(server.command, server.args, {
    env: { ...process.env, ...(server.env ?? {}) },
    stdio: ["pipe", "pipe", "pipe"],
  });
  let buffered = "";
  let stderr = "";
  const queued = [];
  const waiters = [];
  child.stdout.setEncoding("utf8");
  child.stdout.on("data", (chunk) => {
    buffered += chunk;
    while (buffered.includes("\n")) {
      const end = buffered.indexOf("\n");
      const line = buffered.slice(0, end);
      buffered = buffered.slice(end + 1);
      if (line === "") continue;
      const value = JSON.parse(line);
      const waiter = waiters.shift();
      if (waiter === undefined) queued.push(value);
      else waiter(value);
    }
  });
  child.stderr.setEncoding("utf8");
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  const closed = new Promise((resolve) => child.once(
    "close",
    (code, signal) => resolve({ code, signal }),
  ));
  let requestId = 0;
  async function request(method, params) {
    requestId += 1;
    child.stdin.write(`${JSON.stringify({
      jsonrpc: "2.0",
      id: requestId,
      method,
      params,
    })}\n`);
    const response = await Promise.race([
      queued.length > 0
        ? Promise.resolve(queued.shift())
        : new Promise((resolve) => waiters.push(resolve)),
      new Promise((_resolve, reject) => setTimeout(
        () => reject(new Error(`timeout waiting for ${method}; ${stderr}`)),
        2_000,
      )),
    ]);
    if (response?.id !== requestId || response.error !== undefined) {
      fail(`fake Claude received an error for ${method}`);
    }
    return response.result;
  }
  return { child, closed, request, stderr: () => stderr };
}

async function stopSession(session, clean = true) {
  if (!session.child.stdin.writableEnded) session.child.stdin.end();
  const result = await session.closed;
  if (clean && (result.code !== 0 || result.signal !== null || session.stderr() !== "")) {
    fail("fake Claude MCP child did not close cleanly");
  }
}

async function discoverServer(request) {
  const discovery = await request("server/discover", meta());
  if (JSON.stringify(discovery.capabilities) !== JSON.stringify({
    tools: { listChanged: false },
  })) {
    fail("fake Claude observed a widened capability set");
  }
}

async function listTools(request) {
  const listing = await request("tools/list", meta());
  const listedOperations = listing.tools?.map(({ name }) => name);
  if (
    !Array.isArray(listedOperations) ||
    JSON.stringify([...listedOperations].sort()) !== JSON.stringify([...OPERATIONS].sort())
  ) {
    fail(`fake Claude did not observe the canonical exact five: ${JSON.stringify(
      listedOperations,
    )}`);
  }
  const evidenceInput = listing.tools.find(
    ({ name }) => name === "evidence.inspect",
  )?.inputSchema;
  if (
    evidenceInput?.type !== "object" ||
    evidenceInput.additionalProperties !== false ||
    JSON.stringify(evidenceInput.required) !== JSON.stringify(["receipt_id"]) ||
    Object.keys(evidenceInput.properties ?? {}).join("\0") !== "receipt_id" ||
    evidenceInput.properties.receipt_id?.type !== "string" ||
    evidenceInput.properties.receipt_id?.pattern !==
      "^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$" ||
    Object.hasOwn(evidenceInput, "oneOf") ||
    Object.hasOwn(evidenceInput, "$defs") ||
    Object.hasOwn(evidenceInput, "$ref")
  ) {
    fail("fake Claude did not receive the closed evidence.inspect v1 schema");
  }
}

async function discover(request) {
  await discoverServer(request);
  await listTools(request);
}

async function main() {
  const argumentsValue = process.argv.slice(2);
  const mcpPath = optionValue(argumentsValue, "--mcp-config");
  const settingsPath = optionValue(argumentsValue, "--settings");
  const settings = JSON.parse(readFileSync(settingsPath, "utf8"));
  if (
    optionValue(argumentsValue, "--output-format") !== "json" ||
    optionValue(argumentsValue, "--permission-mode") !== "dontAsk" ||
    optionValue(argumentsValue, "--max-turns") !== "10" ||
    optionValue(argumentsValue, "--tools") !== "" ||
    JSON.stringify(optionValues(
      argumentsValue,
      "--allowedTools",
      "--permission-mode",
    )) !== JSON.stringify(PERMISSION_ALIASES) ||
    JSON.stringify(settings.permissions?.allow) !== JSON.stringify(PERMISSION_ALIASES) ||
    settings.permissions?.defaultMode !== "dontAsk" ||
    process.env.MCP_PROTOCOL_NEGOTIATION !== "auto" ||
    process.env.MCP_SDK_GENERATION !== "v2" ||
    !argumentsValue.includes("--strict-mcp-config") ||
    !argumentsValue.includes("--no-session-persistence") ||
    !argumentsValue.includes("--disable-slash-commands") ||
    !argumentsValue.includes("--no-chrome")
  ) {
    fail("fake Claude received a widened execution profile");
  }
  let prompt = "";
  process.stdin.setEncoding("utf8");
  for await (const chunk of process.stdin) prompt += chunk;
  if (prompt !== EXPECTED_PROMPT) fail("fake Claude received the wrong profile prompt");

  const config = JSON.parse(readFileSync(mcpPath, "utf8"));
  const servers = Object.entries(config.mcpServers ?? {});
  if (servers.length !== 1 || servers[0][0] !== SERVER_NAME) {
    fail("fake Claude received a widened MCP configuration");
  }
  const server = servers[0][1];
  const prematureToolUse = [
    "premature-tool-use",
    "premature-tool-use-seven",
  ].includes(SCENARIO);
  const splitSessions = SCENARIO === "split-sessions" || prematureToolUse;
  if (splitSessions) {
    const discoverySession = startSession(server);
    let discoveryError = null;
    try {
      await discoverServer(discoverySession.request);
    } catch (error) {
      discoveryError = error;
      throw error;
    } finally {
      await stopSession(discoverySession, discoveryError === null);
    }
  }
  const session = startSession(server);
  const receipts = {};
  let sessionError = null;
  try {
    if (splitSessions) await listTools(session.request);
    else await discover(session.request);
    const calls = PROFILE.operations.map((operation) => ({ ...operation }));
    if (prematureToolUse) calls.pop();
    if (SCENARIO === "wrong-order") [calls[0], calls[1]] = [calls[1], calls[0]];
    for (const operation of calls) {
      const argumentsValue = operation.name === "evidence.inspect"
        ? {
            receipt_id: SCENARIO === "wrong-inspection-receipt"
              ? `gis-ai-go:evidence-receipt:sha256:${"0".repeat(64)}`
              : receipts["catalogue.search"],
          }
        : structuredClone(operation.arguments);
      if (SCENARIO === "wrong-arguments" && operation.name === "catalogue.search") {
        argumentsValue.query = "Price Paid";
      }
      const called = await session.request("tools/call", meta({
        name: operation.name,
        arguments: argumentsValue,
      }));
      receipts[operation.name] = called.structuredContent.evidence_receipt.receipt_id;
      if (SCENARIO === "duplicate-call" && operation.name === "catalogue.search") {
        await session.request("tools/call", meta({
          name: operation.name,
          arguments: argumentsValue,
        }));
      }
    }
  } catch (error) {
    sessionError = error;
    throw error;
  } finally {
    await stopSession(
      session,
      ["positive", "split-sessions"].includes(SCENARIO) && sessionError === null,
    );
  }

  if (prematureToolUse) {
    receipts["evidence.inspect"] = SCENARIO === "premature-tool-use-seven"
      ? receipts["catalogue.search"]
      : `gis-ai-go:evidence-receipt:sha256:${"f".repeat(64)}`;
  }

  process.stdout.write(JSON.stringify({
    type: "result",
    subtype: "success",
    is_error: false,
    permission_denials: [],
    num_turns: SCENARIO === "premature-tool-use-seven" ? 7 :
      SCENARIO === "premature-tool-use" ? 8 : 11,
    duration_ms: 800,
    duration_api_ms: 700,
    result: "The exact-five-v1 result is available in structured_output.",
    session_id: "00000000-0000-4000-8000-000000000005",
    stop_reason: prematureToolUse ? "tool_use" : "end_turn",
    total_cost_usd: 0.01,
    usage: {
      input_tokens: 256,
      cache_creation_input_tokens: 0,
      cache_read_input_tokens: 0,
      output_tokens: 128,
    },
    modelUsage: {
      "claude-sonnet-5": {
        inputTokens: 256,
        cacheCreationInputTokens: 0,
        cacheReadInputTokens: 0,
        outputTokens: 128,
        costUSD: 0.01,
        contextWindow: 200000,
        maxOutputTokens: 64000,
      },
    },
    structured_output: {
      profile: "exact-five-v1",
      operation_order: OPERATIONS,
      receipt_ids: receipts,
      inspected_search_receipt_id: receipts["catalogue.search"],
    },
  }));
}

try {
  await main();
} catch (error) {
  const message = error instanceof Error ? error.message : "unknown";
  process.stderr.write(`fake Claude exact five failed: ${message}\n`);
  process.exitCode = 1;
}
