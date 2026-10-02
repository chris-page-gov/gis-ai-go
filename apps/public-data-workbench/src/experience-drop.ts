/** Browser-only file descriptors: no contents are uploaded, persisted or fetched. */
const MAX_FILES = 64;
const MAX_ENTRIES = 128;
const MAX_DEPTH = 8;
const MAX_FILE_BYTES = 20 * 1024 * 1024;
const MAX_TOTAL_BYTES = 50 * 1024 * 1024;
const DEADLINE_MS = 5_000;

interface DropEntry {
  name: string;
  isFile: boolean;
  isDirectory: boolean;
  file?: (success: (file: File) => void, failure: () => void) => void;
  createReader?: () => { readEntries?: (success: (entries: DropEntry[]) => void, failure: () => void) => void };
}
interface Root { entry?: DropEntry; file?: File; }

function aborted() { return new DOMException("Reading the dropped files was cancelled.", "AbortError"); }
function expired() { return new DOMException("Reading the dropped folder took more than five seconds. Try a smaller folder.", "TimeoutError"); }
function unsupported() { return new Error("This browser could not read the dropped folder. Choose its files together, or use a browser that supports folder drops."); }
function segment(value: unknown): string {
  if (typeof value !== "string" || value.length === 0 || value.length > 255 ||
    value === "." || value === ".." || /[/\\\u0000-\u001f\u007f]/u.test(value)) {
    throw new Error("A dropped file or folder has an unsupported name.");
  }
  return value;
}
function relativePath(file: File): string {
  const path = file.webkitRelativePath || file.name;
  const parts = path.split("/");
  if (parts.length > MAX_DEPTH) throw new Error("Choose a folder no more than eight levels deep.");
  return parts.map(segment).join("/");
}
function boundedList<T>(list: ArrayLike<T> | undefined, maximum: number): T[] {
  if (list === undefined) return [];
  if (!Number.isSafeInteger(list.length) || list.length < 0 || list.length > maximum) {
    throw new Error(`The drop contains too many items. Choose at most ${maximum}.`);
  }
  return Array.from(list);
}

/**
 * Preserve relative paths, including a dropped folder's name, for sibling matching.
 * A depth of eight includes the root name and final filename. Browser callbacks
 * cannot be cancelled, but late results are ignored after cancellation/deadline.
 */
export async function readDroppedFiles(dataTransfer: DataTransfer, signal?: AbortSignal): Promise<{ files: File[]; paths: string[] }> {
  const deadline = performance.now() + DEADLINE_MS;
  const check = () => {
    if (signal?.aborted) throw aborted();
    if (performance.now() >= deadline) throw expired();
  };
  check();

  // Capture all drag-store references synchronously while the drop event permits
  // access. Do not return to the browser before getAsEntry/getAsFile has run.
  const fallback = boundedList(dataTransfer.files, MAX_FILES);
  const items = boundedList(dataTransfer.items, MAX_ENTRIES);
  const roots: Root[] = [];
  let fileItems = 0;
  for (const item of items) {
    check();
    if (item?.kind !== "file") continue;
    fileItems++;
    let entry: DropEntry | null = null;
    try {
      const getEntry = item.webkitGetAsEntry;
      if (typeof getEntry === "function") entry = getEntry.call(item) as DropEntry | null;
    } catch { throw unsupported(); }
    if (entry !== null) roots.push({ entry });
    else {
      let file: File | null = null;
      try { if (typeof item.getAsFile === "function") file = item.getAsFile(); } catch { throw unsupported(); }
      if (file !== null) roots.push({ file });
      else if (fallback.length !== items.filter(value => value?.kind === "file").length) throw unsupported();
    }
  }
  if (roots.some(root => root.entry?.isDirectory) && roots.length !== fileItems) throw unsupported();
  if (roots.length !== fileItems || roots.length === 0) {
    if (fileItems > 0 && fallback.length === 0) throw unsupported();
    roots.splice(0, roots.length, ...fallback.map(file => ({ file })));
  }

  const files: File[] = [], paths: string[] = [], names = new Set<string>();
  let visited = 0, totalBytes = 0;
  function unique(path: string) {
    if (names.has(path)) throw new Error("The drop contains duplicate file paths. Choose each file or folder once.");
    names.add(path);
  }
  function visit() {
    check();
    if (++visited > MAX_ENTRIES) throw new Error("The folder contains more than 128 files and folders. Choose a smaller folder.");
  }
  function retain(file: File, path: string) {
    check();
    if (!(file instanceof File) || !Number.isSafeInteger(file.size) || file.size < 0) throw unsupported();
    if (files.length >= MAX_FILES) throw new Error("Choose at most 64 files at a time.");
    if (file.size > MAX_FILE_BYTES) throw new Error("Each file must be no larger than 20 MiB.");
    if (totalBytes + file.size > MAX_TOTAL_BYTES) throw new Error("The selected files must total no more than 50 MiB.");
    totalBytes += file.size; files.push(file); paths.push(path);
  }
  async function callback<T>(start: (success: (result: T) => void, failure: () => void) => void): Promise<T> {
    check();
    return new Promise<T>((resolve, reject) => {
      let done = false;
      const finish = (error?: Error, value?: T) => {
        if (done) return;
        done = true; clearTimeout(timer); signal?.removeEventListener("abort", cancel);
        if (error) reject(error); else resolve(value as T);
      };
      const cancel = () => finish(aborted());
      const timer = setTimeout(() => finish(expired()), Math.max(0, deadline - performance.now()));
      signal?.addEventListener("abort", cancel, { once: true });
      try {
        check();
        start(value => {
          try { check(); finish(undefined, value); } catch (error) { finish(error as Error); }
        }, () => finish(unsupported()));
      } catch (error) { finish(error instanceof DOMException ? error : unsupported()); }
    });
  }
  async function walk(entry: DropEntry, parent: string, depth: number): Promise<void> {
    visit();
    if (depth > MAX_DEPTH) throw new Error("Choose a folder no more than eight levels deep.");
    if (!entry || typeof entry !== "object" || typeof entry.isFile !== "boolean" ||
      typeof entry.isDirectory !== "boolean" || entry.isFile === entry.isDirectory) throw unsupported();
    const name = segment(entry.name), path = parent ? `${parent}/${name}` : name;
    unique(path);
    if (entry.isFile) {
      if (typeof entry.file !== "function") throw unsupported();
      const file = await callback<File>((success, failure) => entry.file!(success, failure));
      if (!(file instanceof File)) throw unsupported();
      if (file.name !== name) throw new Error("A dropped file changed while its folder was being read. Drop the folder again.");
      retain(file, path); return;
    }
    if (typeof entry.createReader !== "function") throw unsupported();
    let reader;
    try { reader = entry.createReader(); } catch { throw unsupported(); }
    if (!reader || typeof reader.readEntries !== "function") throw unsupported();
    for (;;) {
      const batch = await callback<DropEntry[]>((success, failure) => reader.readEntries!(success, failure));
      if (!Array.isArray(batch)) throw unsupported();
      if (batch.length === 0) break;
      if (visited + batch.length > MAX_ENTRIES) throw new Error("The folder contains more than 128 files and folders. Choose a smaller folder.");
      for (const child of batch) await walk(child, path, depth + 1);
    }
  }
  for (const root of roots) {
    check();
    if (root.entry) await walk(root.entry, "", 1);
    else if (root.file) { visit(); const path = relativePath(root.file); unique(path); retain(root.file, path); }
    else throw unsupported();
  }
  check();
  return { files, paths };
}
