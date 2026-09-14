export interface Actions {
  find(input: unknown, signal?: AbortSignal): Promise<unknown>;
  select(input: unknown, signal?: AbortSignal): Promise<unknown>;
  retrieve(input: unknown, signal?: AbortSignal): Promise<unknown>;
  inspect(input: unknown, signal?: AbortSignal): Promise<unknown>;
}
interface PageTool {
  name: string; title: string; description: string; inputSchema: object;
  annotations: { readOnlyHint: boolean; untrustedContentHint: true };
  execute(input: unknown, options?: { signal?: AbortSignal }): Promise<unknown>;
}
interface Context { registerTool(tool: PageTool, options: { signal: AbortSignal }): void | Promise<void>; }
const closed = (properties: object) => ({ type: "object", properties, required: Object.keys(properties), additionalProperties: false });
export const PAGE_TOOL_DEFINITIONS = [
  { name: "workbench_find_data", title: "Find public dataset candidates", action: "find",
    description: "Search seven frozen OKF-led metadata records using 1 to 10 English keywords, not a full question. Updates the visible matches. No provider call or data-retrieval authority. Do not submit personal information.",
    inputSchema: closed({ query: { type: "string", minLength: 1, maxLength: 256, pattern: "^[ -~]+$" } }) },
  { name: "workbench_review_cpih_selection", title: "Review a captured CPIH selection", action: "select",
    description: "Ask the fixed local MCP server for a non-authorising January or July 2026 CPIH L522/MM23 plan and stage it visibly on the page. No observation or durable receipt yet. Returns its selection plan ID.",
    inputSchema: closed({ period: { enum: ["2026-01", "2026-07"] } }) },
  { name: "workbench_retrieve_cpih_and_store_receipt", title: "Retrieve captured CPIH and store its receipt", action: "retrieve",
    description: "Complete the exact selection already reviewed on this page through the fixed local MCP server. Returns one captured index level, not an inflation percentage, and persists a claim and receipt. Repeated calls use this page's same request key. No live provider call. Updates the visible evidence desk before returning.",
    inputSchema: closed({ selection_plan_id: { type: "string", pattern: "^gis-ai-go:web216-cpih-selection-plan:sha256:[0-9a-f]{64}$", maxLength: 128 } }) },
  { name: "workbench_inspect_receipt", title: "Inspect an existing captured CPIH receipt", action: "inspect",
    description: "Read an existing captured CPIH result and its durable receipt through the local MCP server. Displays that original evidence on the page; does not issue a new inspection receipt or contact a provider.",
    inputSchema: closed({ receipt_id: { type: "string", pattern: "^gis-ai-go:evidence-receipt:sha256:[0-9a-f]{64}$", maxLength: 128 } }) },
] as const;
const registrations = new WeakMap<Document, () => void>();

export async function registerPageTools(document: Document, actions: Actions) {
  registrations.get(document)?.();
  const context = (document as Document & { modelContext?: Context }).modelContext;
  const view = document.defaultView;
  if (!view || view.top !== view || !context || typeof context.registerTool !== "function") {
    return { status: "unsupported" as const, dispose: () => undefined };
  }
  const lifecycle = new AbortController();
  const hide = (event: PageTransitionEvent) => { if (!event.persisted) dispose(); };
  const dispose = () => { lifecycle.abort(); view.removeEventListener("pagehide", hide); registrations.delete(document); };
  registrations.set(document, dispose); view.addEventListener("pagehide", hide);
  try {
    for (const definition of PAGE_TOOL_DEFINITIONS) await context.registerTool({
      name: definition.name, title: definition.title, description: definition.description,
      inputSchema: definition.inputSchema,
      // All tools change visible page state; only retrieval changes durable server state.
      annotations: { readOnlyHint: false, untrustedContentHint: true },
      async execute(input, options) {
        try {
          const signal = options?.signal ? AbortSignal.any([options.signal, lifecycle.signal]) : lifecycle.signal;
          signal.throwIfAborted();
          return await actions[definition.action](input, signal);
        } catch {
          return { isError: true, code: "operation-not-completed", message: "The page operation was rejected, cancelled or unavailable. No success is claimed. Inspect the page status and use the documented exact inputs." };
        }
      },
    }, { signal: lifecycle.signal });
    return { status: "registered" as const, dispose };
  } catch { dispose(); return { status: "failed" as const, dispose }; }
}
