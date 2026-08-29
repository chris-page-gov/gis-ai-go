export function requiredElement<T extends HTMLElement>(selector: string): T {
  const candidate = document.querySelector<T>(selector);
  if (candidate === null) throw new Error(`Required page element is missing: ${selector}`);
  return candidate;
}

export function element<K extends keyof HTMLElementTagNameMap>(
  tagName: K,
  options: { readonly className?: string; readonly text?: string } = {},
): HTMLElementTagNameMap[K] {
  const node = document.createElement(tagName);
  if (options.className !== undefined) node.className = options.className;
  if (options.text !== undefined) node.textContent = options.text;
  return node;
}

export function definitionList(
  rows: readonly { readonly term: string; readonly description: string }[],
): HTMLDListElement {
  const list = element("dl", { className: "record-metadata" });
  for (const row of rows) {
    list.append(
      element("dt", { text: row.term }),
      element("dd", { text: row.description }),
    );
  }
  return list;
}
