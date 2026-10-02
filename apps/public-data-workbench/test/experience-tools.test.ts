import { describe, expect, it, vi } from "vitest";
import { registerExperienceTools } from "../src/experience-tools";

describe("learning page tools", () => {
  it("validates closed inputs, changes visible state and never exposes the file pane", async () => {
    const tools: { name: string; execute(input: unknown): Promise<unknown> }[] = [];
    const state = { feature: "places", view: "cards", concept: "point" };
    Object.defineProperty(document, "modelContext", { configurable: true, value: { registerTool(tool: typeof tools[number]) { tools.push(tool); } } });
    const actions = { state: () => ({ ...state }), show: vi.fn((id: string) => { if (id !== "places") throw new Error(); state.feature = id; return state; }),
      view: vi.fn((value: "cards" | "table" | "evidence") => { state.view = value; return state; }), explain: vi.fn((id: string) => { if (id !== "point") throw new Error(); state.concept = id; return state; }) };
    const registration = await registerExperienceTools(document, actions);
    expect(registration.status).toBe("registered"); expect(tools).toHaveLength(4);
    expect(await tools[0]!.execute({})).toEqual(state);
    expect(await tools[2]!.execute({ view: "table" })).toMatchObject({ view: "table" });
    expect(await tools[2]!.execute({ view: "<script>" })).toMatchObject({ isError: true });
    expect(await tools[1]!.execute({ feature_id: "places", url: "https://example.org" })).toMatchObject({ isError: true });
    expect(actions.show).not.toHaveBeenCalled();
    expect(await tools[1]!.execute({ feature_id: "unknown" })).toMatchObject({ isError: true });
    expect(await tools[3]!.execute({ concept_id: "point" })).toMatchObject({ concept: "point" });
    window.dispatchEvent(new PageTransitionEvent("pagehide", { persisted: true }));
    expect(await tools[0]!.execute({})).toEqual(state);
    registration.dispose(); expect(await tools[0]!.execute({})).toMatchObject({ isError: true });
    Reflect.deleteProperty(document, "modelContext");
  });
  it("keeps the manual page usable without a host or after partial registration failure", async () => {
    const actions = { state: () => ({}), show: () => ({}), view: () => ({}), explain: () => ({}) };
    expect((await registerExperienceTools(document, actions)).status).toBe("unsupported");
    let signal: AbortSignal | undefined;
    Object.defineProperty(document, "modelContext", { configurable: true, value: { registerTool(_tool: unknown, options: { signal: AbortSignal }) { signal = options.signal; throw new Error("unavailable"); } } });
    expect((await registerExperienceTools(document, actions)).status).toBe("failed"); expect(signal?.aborted).toBe(true);
    Reflect.deleteProperty(document, "modelContext");
  });
});
