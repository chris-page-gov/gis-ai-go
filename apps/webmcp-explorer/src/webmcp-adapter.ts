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
      "Search validated GIS AI GO public catalogue metadata with bounded words and optional governed facets. Returns at most five compact records and makes no provider call.",
    inputSchema: Object.freeze({
      type: "object",
      additionalProperties: false,
      required: ["query"],
      properties: {
        query: {
          type: "string",
          minLength: 1,
          maxLength: 256,
          description: "Public catalogue terms only; do not include personal information.",
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

  const controller = new AbortController();
  let disposed = false;
  const dispose = (): void => {
    if (disposed) return;
    disposed = true;
    view.removeEventListener("pagehide", dispose);
    controller.abort("The WebMCP page was closed or navigated away from.");
  };
  view.addEventListener("pagehide", dispose, { once: true });
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
