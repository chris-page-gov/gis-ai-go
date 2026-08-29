import { describe, expect, it, vi } from "vitest";

import {
  WEBMCP_TOOL_METADATA,
  WEBMCP_TOOL_NAMES,
  registerWebMcpTools,
  type WebMcpTool,
} from "../../src/webmcp-adapter";
import { catalogueFixture } from "./fixture";

describe("imperative WebMCP adapter", () => {
  it("registers exactly two static, read-only and untrusted page tools", async () => {
    const registered: WebMcpTool[] = [];
    const registrationSignals: AbortSignal[] = [];
    Object.defineProperty(document, "modelContext", {
      configurable: true,
      value: {
        registerTool: vi.fn(async (tool: WebMcpTool, options?: { signal?: AbortSignal }) => {
          registered.push(tool);
          if (options?.signal !== undefined) registrationSignals.push(options.signal);
        }),
      },
    });
    const onResult = vi.fn();
    const registration = await registerWebMcpTools({
      document,
      bundle: catalogueFixture(),
      onResult,
    });

    expect(registration.status).toBe("registered");
    expect(registration.toolNames).toEqual(WEBMCP_TOOL_NAMES);
    expect(registered.map(({ name }) => name)).toEqual(WEBMCP_TOOL_NAMES);
    expect(registered.every(({ annotations }) => annotations.readOnlyHint)).toBe(true);
    expect(registered.every(({ annotations }) => annotations.untrustedContentHint)).toBe(true);
    expect(registered[0]?.description).toBe(
      WEBMCP_TOOL_METADATA.explorer_search_catalogue.description,
    );
    expect(registered[0]?.description).not.toContain("Ignore previous instructions");

    const result = await registered[0]!.execute({ query: "ONS population", limit: 2 });
    expect(result.page_tool).toBe("explorer_search_catalogue");
    expect(onResult).toHaveBeenCalledOnce();

    const described = await registered[1]!.execute(
      { record_id: "provider:ons-data-api" },
      {},
    );
    expect(described.page_tool).toBe("explorer_describe_record");
    expect(onResult).toHaveBeenCalledTimes(2);

    const invocation = new AbortController();
    invocation.abort("The host cancelled this page-tool call.");
    await expect(
      registered[0]!.execute(
        { query: "ONS population", limit: 2 },
        { signal: invocation.signal },
      ),
    ).rejects.toThrow();

    registration.dispose();
    expect(registrationSignals).toHaveLength(2);
    expect(registrationSignals.every((signal) => signal.aborted)).toBe(true);
    delete (document as Document & { modelContext?: unknown }).modelContext;
  });

  it("leaves the manual application intact when the API is absent", async () => {
    delete (document as Document & { modelContext?: unknown }).modelContext;
    const registration = await registerWebMcpTools({
      document,
      bundle: catalogueFixture(),
    });
    expect(registration).toMatchObject({ status: "unsupported", toolNames: [] });
    expect(() => registration.dispose()).not.toThrow();
  });

  it("preserves registration through BFCache and aborts on final pagehide", async () => {
    const signals: AbortSignal[] = [];
    Object.defineProperty(document, "modelContext", {
      configurable: true,
      value: {
        registerTool: async (_tool: WebMcpTool, options?: { signal?: AbortSignal }) => {
          if (options?.signal !== undefined) signals.push(options.signal);
        },
      },
    });
    await registerWebMcpTools({ document, bundle: catalogueFixture() });
    window.dispatchEvent(new PageTransitionEvent("pagehide", { persisted: true }));
    expect(signals).toHaveLength(2);
    expect(signals.every((signal) => !signal.aborted)).toBe(true);

    window.dispatchEvent(new PageTransitionEvent("pagehide", { persisted: false }));
    expect(signals.every((signal) => signal.aborted)).toBe(true);
    delete (document as Document & { modelContext?: unknown }).modelContext;
  });
});
