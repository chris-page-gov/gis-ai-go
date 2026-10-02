import { afterEach, describe, expect, it, vi } from "vitest";
import { readDroppedFiles } from "../src/experience-drop";

interface Entry {
  name: string; isFile: boolean; isDirectory: boolean;
  file?: (success: (value: File) => void, failure: () => void) => void;
  createReader?: () => { readEntries: (success: (entries: Entry[]) => void, failure: () => void) => void };
}
function file(name: string, size = 1, path?: string) {
  const value = new File(["x"], name);
  Object.defineProperty(value, "size", { value: size });
  if (path) Object.defineProperty(value, "webkitRelativePath", { value: path });
  return value;
}
function leaf(name: string, size = 1): Entry {
  return { name, isFile: true, isDirectory: false, file: success => success(file(name, size)) };
}
function folder(name: string, batches: Entry[][]): Entry {
  return { name, isFile: false, isDirectory: true,
    createReader: () => {
      let offset = 0;
      return { readEntries: success => success(batches[offset++] ?? []) };
    } };
}
function transfer(entries: Entry[], files: File[] = []): DataTransfer {
  return { items: entries.map(entry => ({ kind: "file", webkitGetAsEntry: () => entry })), files } as unknown as DataTransfer;
}
afterEach(() => { vi.useRealTimers(); vi.restoreAllMocks(); });

describe("bounded browser folder descriptors", () => {
  it("preserves nested relative paths and all Shapefile siblings across directory batches", async () => {
    const root = folder("map", [[leaf("roads.shp"), leaf("roads.shx")],
      [leaf("roads.dbf"), folder("notes", [[leaf("readme.txt")]])], [leaf("roads.prj")]]);
    const result = await readDroppedFiles(transfer([root]));
    expect(result.paths).toEqual(["map/roads.shp", "map/roads.shx", "map/roads.dbf", "map/notes/readme.txt", "map/roads.prj"]);
    expect(result.files.map(value => value.name)).toEqual(["roads.shp", "roads.shx", "roads.dbf", "readme.txt", "roads.prj"]);
  });

  it("captures drop entries synchronously before directory callbacks return", async () => {
    let complete!: (entries: Entry[]) => void;
    const first = { name: "folder", isFile: false, isDirectory: true,
      createReader: () => ({ readEntries: (success: (entries: Entry[]) => void) => { complete = success; } }) };
    const getEntry = vi.fn(() => leaf("other.csv"));
    const data = { files: [], items: [{ kind: "file", webkitGetAsEntry: () => first }, { kind: "file", webkitGetAsEntry: getEntry }] } as unknown as DataTransfer;
    const pending = readDroppedFiles(data);
    expect(getEntry).toHaveBeenCalledTimes(1);
    complete([]);
    expect((await pending).paths).toEqual(["other.csv"]);
  });

  it("falls back to the FileList without directory support and keeps supplied relative paths", async () => {
    const values = [file("points.geojson"), file("roads.dbf", 1, "map/roads.dbf")];
    const result = await readDroppedFiles({ files: values, items: [] } as unknown as DataTransfer);
    expect(result.files).toEqual(values); expect(result.paths).toEqual(["points.geojson", "map/roads.dbf"]);
    const noMethods = { files: values, items: values.map(() => ({ kind: "file" })) } as unknown as DataTransfer;
    expect((await readDroppedFiles(noMethods)).paths).toEqual(result.paths);
  });

  it("handles mixed folder and directly dropped file descriptors without losing either", async () => {
    const extra = file("notes.txt");
    const data = { files: [extra], items: [
      { kind: "file", webkitGetAsEntry: () => folder("shape", [[leaf("area.shp")]]) },
      { kind: "file", getAsFile: () => extra }, { kind: "string" },
    ] } as unknown as DataTransfer;
    expect((await readDroppedFiles(data)).paths).toEqual(["shape/area.shp", "notes.txt"]);
  });

  it("rejects duplicate paths while permitting the same filename in different folders", async () => {
    await expect(readDroppedFiles(transfer([folder("map", [[leaf("same.csv")], [leaf("same.csv")]])]))).rejects.toThrow("duplicate file paths");
    await expect(readDroppedFiles(transfer([folder("map", []), folder("map", [])]))).rejects.toThrow("duplicate file paths");
    expect((await readDroppedFiles(transfer([folder("a", [[leaf("same.csv")]]), folder("b", [[leaf("same.csv")]])]))).paths)
      .toEqual(["a/same.csv", "b/same.csv"]);
  });

  it("rejects traversal, separators, controls and mismatched descriptor names", async () => {
    for (const name of ["..", ".", "", "a/b", "a\\b", "a\u0000b"]) {
      await expect(readDroppedFiles(transfer([leaf(name)]))).rejects.toThrow("unsupported name");
    }
    const mismatch = leaf("expected.shp"); mismatch.file = success => success(file("different.shp"));
    await expect(readDroppedFiles(transfer([mismatch]))).rejects.toThrow("changed");
    await expect(readDroppedFiles({ files: [file("data.csv", 1, "../data.csv")], items: [] } as unknown as DataTransfer)).rejects.toThrow("unsupported name");
  });

  it("allows 64 files but rejects a 65th file without returning a partial batch", async () => {
    expect((await readDroppedFiles(transfer([folder("map", [Array.from({ length: 64 }, (_, index) => leaf(`${index}.csv`))])]))).files).toHaveLength(64);
    await expect(readDroppedFiles(transfer([folder("map", [Array.from({ length: 65 }, (_, index) => leaf(`${index}.csv`))])]))).rejects.toThrow("64 files");
  });

  it("counts directories towards the 128-entry ceiling across batches", async () => {
    const children = Array.from({ length: 128 }, (_, index) => folder(`empty${index}`, []));
    expect((await readDroppedFiles(transfer([folder("map", [children.slice(0, 127)])]))).files).toEqual([]);
    await expect(readDroppedFiles(transfer([folder("map", [children.slice(0, 127), children.slice(127)])]))).rejects.toThrow("128 files and folders");
  });

  it("bounds both recursive and FileList relative paths to eight levels", async () => {
    let nested = leaf("data.csv");
    for (let index = 0; index < 7; index++) nested = folder(`f${index}`, [[nested]]);
    expect((await readDroppedFiles(transfer([nested]))).paths[0]?.split("/")).toHaveLength(8);
    await expect(readDroppedFiles(transfer([folder("too-deep", [[nested]])]))).rejects.toThrow("eight levels");
    await expect(readDroppedFiles({ files: [file("data.csv", 1, `${"f/".repeat(8)}data.csv`)], items: [] } as unknown as DataTransfer)).rejects.toThrow("eight levels");
  });

  it("enforces 20 MiB per file and 50 MiB in total using descriptors without content reads", async () => {
    const MiB = 1024 * 1024;
    const exact = await readDroppedFiles(transfer([leaf("one", 20 * MiB), leaf("two", 20 * MiB), leaf("three", 10 * MiB)]));
    expect(exact.files).toHaveLength(3);
    await expect(readDroppedFiles(transfer([leaf("large", 20 * MiB + 1)]))).rejects.toThrow("20 MiB");
    await expect(readDroppedFiles(transfer([leaf("one", 20 * MiB), leaf("two", 20 * MiB), leaf("three", 10 * MiB + 1)]))).rejects.toThrow("50 MiB");
  });

  it("ends a stalled directory callback after five seconds and ignores late results", async () => {
    vi.useFakeTimers();
    let complete!: (entries: Entry[]) => void;
    const root = folder("slow", []);
    root.createReader = () => ({ readEntries: success => { complete = success; } });
    const pending = readDroppedFiles(transfer([root]));
    const outcome = expect(pending).rejects.toMatchObject({ name: "TimeoutError" });
    await vi.advanceTimersByTimeAsync(5_000); await outcome;
    complete([leaf("late.csv")]);
    expect(vi.getTimerCount()).toBe(0);
  });

  it("bounds a stalled file callback and rejects an already elapsed deadline", async () => {
    vi.useFakeTimers();
    const root = leaf("slow.csv"); root.file = () => {};
    const outcome = expect(readDroppedFiles(transfer([root]))).rejects.toMatchObject({ name: "TimeoutError" });
    await vi.advanceTimersByTimeAsync(5_000); await outcome;
    vi.useRealTimers();
    vi.spyOn(performance, "now").mockReturnValueOnce(0).mockReturnValue(5_000);
    await expect(readDroppedFiles(transfer([]))).rejects.toMatchObject({ name: "TimeoutError" });
  });

  it("supports abort before enumeration and while a browser callback is pending", async () => {
    const controller = new AbortController(); controller.abort();
    const data = transfer([leaf("one.csv")]);
    await expect(readDroppedFiles(data, controller.signal)).rejects.toMatchObject({ name: "AbortError" });
    const running = new AbortController();
    let complete!: (file: File) => void;
    const entry = leaf("late.csv"); entry.file = success => { complete = success; };
    const pending = readDroppedFiles(transfer([entry]), running.signal);
    const outcome = expect(pending).rejects.toMatchObject({ name: "AbortError" });
    running.abort(); await outcome; complete(file("late.csv"));
  });

  it("explains unsupported directory APIs, invalid entries and browser read failures", async () => {
    const badEntries = [
      { name: "dir", isFile: false, isDirectory: true },
      { name: "dir", isFile: false, isDirectory: true, createReader: () => ({}) },
      { name: "file", isFile: true, isDirectory: false },
      { name: "unknown", isFile: false, isDirectory: false },
      { name: "both", isFile: true, isDirectory: true },
      { name: "file", isFile: true, isDirectory: false, file: (_ok: unknown, fail: () => void) => fail() },
      { name: "file", isFile: true, isDirectory: false, file: (ok: (value: unknown) => void) => ok(null) },
      { name: "dir", isFile: false, isDirectory: true, createReader: () => { throw Error("private raw failure"); } },
    ];
    for (const entry of badEntries) await expect(readDroppedFiles(transfer([entry as Entry]))).rejects.toThrow("browser could not read");
    await expect(readDroppedFiles({ items: [{ kind: "file", getAsFile: () => null }], files: [] } as unknown as DataTransfer)).rejects.toThrow("browser could not read");
  });
});
