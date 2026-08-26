#!/usr/bin/env node

import { spawn } from "node:child_process";
import { readFileSync } from "node:fs";

const EXPECTED_PROMPT =
  "Search the public catalogue for INSPIRE and return the first record with its " +
  "inline evidence receipt.\n";
const EXPECTED_PERMISSION_TOOL =
  "mcp__gis-ai-go-qual-206-host-002__catalogue_search";
const SCENARIO = process.env.QUAL_206_FAKE_CLAUDE_SCENARIO ?? "positive";

function fail(message) {
  throw new Error(message);
}

if (process.argv.slice(2).length === 1 && process.argv[2] === "--version") {
  process.stdout.write("2.1.245 (Claude Code)\n");
  process.exit(0);
}

if (
  process.argv.slice(2).length === 3 &&
  process.argv[2] === "auth" && process.argv[3] === "status" &&
  process.argv[4] === "--json"
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

function meta(extra = {}) {
  return {
    ...extra,
    _meta: {
      "io.modelcontextprotocol/protocolVersion": "2026-07-28",
      "io.modelcontextprotocol/clientCapabilities": {},
      "io.modelcontextprotocol/clientInfo": {
        name: "qual-206-fake-claude",
        version: "2.1.245",
        title: "QUAL-206 fake Claude",
      },
      "com.anthropic/toolUseId": "qual-206-bounded-test",
    },
  };
}

function responseReader(stream) {
  let buffered = "";
  const queued = [];
  const waiters = [];
  stream.setEncoding("utf8");
  stream.on("data", (chunk) => {
    buffered += chunk;
    while (true) {
      const newline = buffered.indexOf("\n");
      if (newline < 0) break;
      const line = buffered.slice(0, newline);
      buffered = buffered.slice(newline + 1);
      if (line.length === 0) continue;
      const value = JSON.parse(line);
      const waiter = waiters.shift();
      if (waiter === undefined) queued.push(value);
      else waiter.resolve(value);
    }
  });
  return () => {
    const value = queued.shift();
    if (value !== undefined) return Promise.resolve(value);
    return new Promise((resolve, reject) => waiters.push({ resolve, reject }));
  };
}

function startSession(server) {
  const child = spawn(server.command, server.args, {
    env: { ...process.env, ...(server.env ?? {}) },
    stdio: ["pipe", "pipe", "pipe"],
  });
  let stderr = "";
  child.stderr.setEncoding("utf8");
  child.stderr.on("data", (chunk) => { stderr += chunk; });
  const nextResponse = responseReader(child.stdout);
  const closed = new Promise((resolve) => {
    child.once("close", (code, signal) => resolve({ code, signal }));
  });
  let requestId = 0;
  async function request(method, params) {
    requestId += 1;
    child.stdin.write(`${JSON.stringify({
      jsonrpc: "2.0",
      id: requestId,
      method,
      params,
    })}\n`);
    let timeout;
    try {
      const response = await Promise.race([
        nextResponse(),
        new Promise((_resolve, reject) => {
          timeout = setTimeout(() => reject(new Error(
            `timeout waiting for ${method}; child stderr: ${stderr}`,
          )), 2_000);
        }),
      ]);
      if (response.id !== requestId || response.error !== undefined) {
        fail(`fake Claude received an error for ${method}`);
      }
      return response.result;
    } finally {
      if (timeout !== undefined) clearTimeout(timeout);
    }
  }
  return Object.freeze({ child, closed, request, stderr: () => stderr });
}

async function stopSession(session, requireClean) {
  if (!session.child.stdin.writableEnded) session.child.stdin.end();
  const completion = await session.closed;
  if (
    requireClean &&
    (completion.code !== 0 || completion.signal !== null || session.stderr() !== "")
  ) {
    fail("fake Claude MCP child did not close cleanly");
  }
}

async function useSession(server, action, requireClean = true) {
  const session = startSession(server);
  try {
    return await action(session.request);
  } finally {
    await stopSession(session, requireClean);
  }
}

async function discover(request) {
  await request("server/discover", meta());
  const listing = await request("tools/list", meta());
  if (
    !Array.isArray(listing.tools) || listing.tools.length !== 1 ||
    listing.tools[0].name !== "catalogue.search"
  ) {
    fail("fake Claude did not observe the one-tool catalogue projection");
  }
}

async function main() {
  const argumentsValue = process.argv.slice(2);
  const mcpPath = optionValue(argumentsValue, "--mcp-config");
  const settingsPath = optionValue(argumentsValue, "--settings");
  const settings = JSON.parse(readFileSync(settingsPath, "utf8"));
  if (
    optionValue(argumentsValue, "--output-format") !== "json" ||
    optionValue(argumentsValue, "--permission-mode") !== "dontAsk" ||
    optionValue(argumentsValue, "--max-turns") !== "2" ||
    optionValue(argumentsValue, "--tools") !== "" ||
    optionValue(argumentsValue, "--allowedTools") !== EXPECTED_PERMISSION_TOOL ||
    settings.permissions?.defaultMode !== "dontAsk" ||
    JSON.stringify(settings.permissions?.allow) !==
      JSON.stringify([EXPECTED_PERMISSION_TOOL]) ||
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
  if (prompt !== EXPECTED_PROMPT) fail("fake Claude received the wrong corpus prompt");
  if (SCENARIO === "hanging-descendant") {
    const descendant = spawn(process.execPath, ["-e", "setInterval(() => {}, 1000)"], {
      stdio: ["ignore", "inherit", "inherit"],
    });
    descendant.unref();
    process.exit(0);
  }

  const config = JSON.parse(readFileSync(mcpPath, "utf8"));
  const servers = Object.entries(config.mcpServers ?? {});
  if (servers.length !== 1 || servers[0][0] !== "gis-ai-go-qual-206-host-002") {
    fail("fake Claude received a widened MCP configuration");
  }
  const server = servers[0][1];
  await useSession(server, discover);

  let structured = null;
  if (SCENARIO !== "no-call") {
    const operation = SCENARIO === "wrong-operation"
      ? "catalogue.describe"
      : "catalogue.search";
    const argumentsObject = SCENARIO === "wrong-query"
      ? { query: "Price Paid", limit: 1 }
      : { query: "INSPIRE", limit: 1 };
    const requireClean = !["second-call", "wrong-operation", "wrong-query"].includes(SCENARIO);
    structured = await useSession(server, async (request) => {
      await discover(request);
      const called = await request("tools/call", meta({
        name: operation,
        arguments: argumentsObject,
      }));
      if (SCENARIO === "second-call") {
        await request("tools/call", meta({
          name: "catalogue.search",
          arguments: { query: "INSPIRE", limit: 1 },
        }));
      }
      return called.structuredContent;
    }, requireClean);
    if (SCENARIO === "cross-session-second-call") {
      await useSession(server, async (request) => {
        await discover(request);
        await request("tools/call", meta({
          name: "catalogue.search",
          arguments: { query: "INSPIRE", limit: 1 },
        }));
      }, false);
    }
  }
  const record = structured?.data?.records?.[0];
  const output = {
    type: "result",
    subtype: "success",
    is_error: false,
    permission_denials: [],
    num_turns: 3,
    duration_ms: 400,
    duration_api_ms: 300,
    result: "The governed catalogue result is available in structured_output.",
    session_id: "00000000-0000-4000-8000-000000000001",
    stop_reason: "end_turn",
    total_cost_usd: 0.002,
    usage: {
      input_tokens: 128,
      cache_creation_input_tokens: 0,
      cache_read_input_tokens: 0,
      output_tokens: 64,
    },
    modelUsage: {
      "claude-sonnet-5": {
        inputTokens: 128,
        cacheCreationInputTokens: 0,
        cacheReadInputTokens: 0,
        outputTokens: 64,
        costUSD: 0.002,
        contextWindow: 200000,
        maxOutputTokens: 64000,
      },
    },
    structured_output: {
      record_id: record?.id ?? "hmlr:dataset:inspire-index-polygons",
      title: record?.title ?? "Index polygons spatial data (INSPIRE)",
      receipt_id:
        SCENARIO === "wrong-output" || structured === null
          ? `gis-ai-go:evidence-receipt:sha256:${"0".repeat(64)}`
          : structured.evidence_receipt.receipt_id,
    },
  };
  process.stdout.write(JSON.stringify(output));
}

try {
  await main();
} catch (error) {
  const message = error instanceof Error ? error.message : "unknown";
  process.stderr.write(`fake Claude failed: ${message}\n`);
  process.exitCode = 1;
}
