export const EXPERIENCE_TOOL_NAMES = ["experience_get_state", "experience_show_example", "experience_set_view", "experience_explain"] as const;
export const VIEWS = ["cards", "table", "evidence"] as const;
export type ExperienceView = typeof VIEWS[number];
export interface ExperienceActions {
  state(): unknown;
  show(featureId: string): unknown;
  view(view: ExperienceView): unknown;
  explain(conceptId: string): unknown;
}
interface Tool { name: string; title: string; description: string; inputSchema: object; annotations: object; execute(input: unknown): Promise<unknown> }
interface Context { registerTool(tool: Tool, options: { signal: AbortSignal }): void | Promise<void> }
const closed = (properties: object) => ({ type: "object", properties, required: Object.keys(properties), additionalProperties: false });
function argument(input: unknown, key?: string): string | undefined {
  if (!input || typeof input !== "object" || Array.isArray(input)) throw new Error("Use the documented input object.");
  const data = input as Record<string, unknown>;
  if (!key) { if (Object.keys(data).length) throw new Error("This tool takes no fields."); return; }
  if (Object.keys(data).length !== 1 || !Object.hasOwn(data, key) || typeof data[key] !== "string" || data[key].length > 150) throw new Error("Choose an identifier from the page state.");
  return data[key];
}
/** Page state only. No file contents, provider calls, code generation or remote writes. */
export async function registerExperienceTools(document: Document, actions: ExperienceActions) {
  const context = (document as Document & { modelContext?: Context }).modelContext;
  const view = document.defaultView;
  if (!context || !view || view.top !== view || typeof context.registerTool !== "function") return { status: "unsupported" as const, dispose: () => undefined };
  const lifecycle = new AbortController();
  const hide = (event: PageTransitionEvent) => { if (!event.persisted) dispose(); };
  const dispose = () => { lifecycle.abort(); view.removeEventListener("pagehide", hide); };
  view.addEventListener("pagehide", hide);
  const definitions = [
    { name: EXPERIENCE_TOOL_NAMES[0], title: "Read learning activity choices", key: undefined, schema: closed({}), description: "Read the selected learning example, available feature and concept identifiers, and current view. Returns no selected files, file contents or personal data.", run: () => actions.state() },
    { name: EXPERIENCE_TOOL_NAMES[1], title: "Show a learning example", key: "feature_id", schema: closed({ feature_id: { type: "string", maxLength: 150 } }), description: "Show the authored example for a feature identifier returned by experience_get_state. Changes the visible page and its learning help. Does not run the example or retrieve provider data.", run: (value?: string) => actions.show(value!) },
    { name: EXPERIENCE_TOOL_NAMES[2], title: "Change the learning view", key: "view", schema: closed({ view: { enum: VIEWS } }), description: "Change the visible example into step-by-step cards, a question table, or source and evaluation checks. This is a fixed accessible component choice, not arbitrary generated code or a live data chart.", run: (value?: string) => { if (!VIEWS.includes(value as ExperienceView)) throw new Error("Choose cards, table or evidence."); return actions.view(value as ExperienceView); } },
    { name: EXPERIENCE_TOOL_NAMES[3], title: "Explain a word beside the activity", key: "concept_id", schema: closed({ concept_id: { type: "string", maxLength: 150 } }), description: "Show a plain-language concept explanation in the always-available learning panel. Use a concept identifier returned by experience_get_state.", run: (value?: string) => actions.explain(value!) },
  ];
  try {
    for (const definition of definitions) await context.registerTool({ name: definition.name, title: definition.title, description: definition.description,
      inputSchema: definition.schema, annotations: { readOnlyHint: definition.key === undefined, untrustedContentHint: true },
      async execute(input) {
        try { lifecycle.signal.throwIfAborted(); return definition.run(argument(input, definition.key)); }
        catch { return { isError: true, code: "invalid-or-unavailable-page-action", message: "Read the current choices and use an exact identifier. No data request was made." }; }
      },
    }, { signal: lifecycle.signal });
    return { status: "registered" as const, dispose };
  } catch { dispose(); return { status: "failed" as const, dispose }; }
}
