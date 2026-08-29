import type { CatalogueBundle } from "@gis-ai-go/contracts";

import {
  executePageDescribe,
  executePageSearch,
  type PageToolResult,
} from "./catalogue-tools";

interface ToolExecuteOptions {
  readonly signal?: AbortSignal;
}

export interface WebMcpTool {
  readonly name: string;
  readonly title: string;
  readonly description: string;
  readonly inputSchema: Readonly<Record<string, unknown>>;
  readonly annotations: {
    readonly readOnlyHint: true;
    readonly untrustedContentHint: true;
  };
  readonly execute: (input: unknown, options?: ToolExecuteOptions) => Promise<PageToolResult>;
}

interface WebMcpModelContext {
  registerTool(
    tool: WebMcpTool,
    options?: { readonly signal?: AbortSignal },
  ): Promise<void>;
}

type WebMcpDocument = Document & {
  readonly modelContext?: WebMcpModelContext;
};

export const WEBMCP_TOOL_NAMES = [
  "explorer_search_catalogue",
  "explorer_describe_record",
] as const;

export const WEBMCP_TOOL_METADATA = Object.freeze({
  explorer_search_catalogue: Object.freeze({
    name: "explorer_search_catalogue",
    title: "Search the governed public catalogue",
    description:
      "Search validated GIS AI GO public catalogue metadata. Convert the user's " +
      "question to 1 to 10 relevant catalogue terms rather than passing the full " +
      "question. Optional governed facets are supported; the tool returns at most " +
      "five compact records and makes no provider call.",
    inputSchema: Object.freeze({
      type: "object",
      additionalProperties: false,
      required: ["query"],
      properties: {
        query: {
          type: "string",
          minLength: 1,
          maxLength: 256,
          description:
            "One to 10 public catalogue keywords, not the full user question; " +
            "for example, 'ONS statistics'. Do not include personal information.",
        },
        facets: {
          type: "object",
          additionalProperties: false,
          minProperties: 1,
          properties: {
            types: {
              type: "array",
              minItems: 1,
              maxItems: 5,
              uniqueItems: true,
              items: { enum: ["bundle", "dataset", "provider", "source", "workflow"] },
            },
            authority: {
              type: "array",
              minItems: 1,
              maxItems: 3,
              uniqueItems: true,
              items: {
                enum: ["derived", "project-authoritative", "source-authoritative"],
              },
            },
            access: {
              type: "array",
              minItems: 1,
              maxItems: 3,
              uniqueItems: true,
              items: { enum: ["planned-non-executing", "public", "public-metadata"] },
            },
            rights: {
              type: "array",
              minItems: 1,
              maxItems: 3,
              uniqueItems: true,
              items: { enum: ["metadata-citation", "open-with-conditions", "project-mit"] },
            },
            freshness: {
              type: "array",
              minItems: 1,
              maxItems: 2,
              uniqueItems: true,
              items: { enum: ["current", "review-required"] },
            },
            tags: {
              type: "array",
              minItems: 1,
              maxItems: 10,
              uniqueItems: true,
              items: { type: "string", minLength: 1, maxLength: 128 },
            },
          },
        },
        limit: { type: "integer", minimum: 1, maximum: 5, default: 5 },
      },
    }),
  }),
  explorer_describe_record: Object.freeze({
    name: "explorer_describe_record",
    title: "Describe one governed catalogue record",
    description:
      "Read one exact record from validated GIS AI GO public catalogue metadata, including its authority, rights, freshness, limitations and linked source records. Makes no provider call.",
    inputSchema: Object.freeze({
      type: "object",
      additionalProperties: false,
      required: ["record_id"],
      properties: {
        record_id: {
          type: "string",
          minLength: 1,
          maxLength: 512,
          description: "An exact source-native identifier returned by the search page tool.",
        },
      },
    }),
  }),
} as const);

export interface WebMcpRegistration {
  readonly status: "registered" | "unsupported";
  readonly toolNames: readonly string[];
  dispose(): void;
}

export interface RegisterWebMcpOptions {
  readonly document: Document;
  readonly bundle: CatalogueBundle;
  readonly onResult?: (result: PageToolResult) => void;
}

function createTools(
  bundle: CatalogueBundle,
  onResult?: (result: PageToolResult) => void,
): readonly WebMcpTool[] {
  const run = async (
    execute: () => PageToolResult,
    options?: ToolExecuteOptions,
  ): Promise<PageToolResult> => {
    // The Community Group draft supplies an execution AbortSignal. OpenAI Site
    // tools has also shipped a one-argument callback shape, so tolerate that host
    // while continuing to honour cancellation whenever a signal is supplied.
    options?.signal?.throwIfAborted();
    const result = execute();
    options?.signal?.throwIfAborted();
    onResult?.(result);
    return result;
  };
  const annotations = Object.freeze({
    readOnlyHint: true as const,
    untrustedContentHint: true as const,
  });
  return [
    {
      ...WEBMCP_TOOL_METADATA.explorer_search_catalogue,
      annotations,
      execute: (input, options) => run(() => executePageSearch(bundle, input), options),
    },
    {
      ...WEBMCP_TOOL_METADATA.explorer_describe_record,
      annotations,
      execute: (input, options) => run(() => executePageDescribe(bundle, input), options),
    },
  ];
}

export async function registerWebMcpTools(
  options: RegisterWebMcpOptions,
): Promise<WebMcpRegistration> {
  const candidateDocument = options.document as WebMcpDocument;
  const context = candidateDocument.modelContext;
  const view = candidateDocument.defaultView;
  if (
    context === undefined ||
    typeof context.registerTool !== "function" ||
    view === null ||
    view.top !== view
  ) {
    return { status: "unsupported", toolNames: [], dispose: () => undefined };
  }

  const activeView = view;
  const controller = new AbortController();
  let disposed = false;
  function handlePageHide(event: PageTransitionEvent): void {
    // A persisted pagehide moves this document into the back/forward cache. Its
    // registration remains valid when the same document is restored, whereas a
    // final navigation or close must remove the page-scoped tools.
    if (!event.persisted) dispose();
  }
  function dispose(): void {
    if (disposed) return;
    disposed = true;
    activeView.removeEventListener("pagehide", handlePageHide);
    controller.abort("The WebMCP page was closed or navigated away from.");
  }
  activeView.addEventListener("pagehide", handlePageHide);
  try {
    for (const tool of createTools(options.bundle, options.onResult)) {
      await context.registerTool(tool, { signal: controller.signal });
    }
  } catch (error) {
    dispose();
    throw error;
  }
  return { status: "registered", toolNames: WEBMCP_TOOL_NAMES, dispose };
}
