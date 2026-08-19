export type DomChild = Node | string | null | undefined | false;

export interface ElementOptions {
  readonly className?: string;
  readonly id?: string;
  readonly text?: string;
}

export function appendChildren(parent: Node, children: readonly DomChild[]): void {
  for (const child of children) {
    if (child === null || child === undefined || child === false) {
      continue;
    }
    parent.appendChild(child instanceof Node ? child : document.createTextNode(child));
  }
}

export function element<K extends keyof HTMLElementTagNameMap>(
  tagName: K,
  options: ElementOptions = {},
  children: readonly DomChild[] = [],
): HTMLElementTagNameMap[K] {
  const node = document.createElement(tagName);
  if (options.className !== undefined) {
    node.className = options.className;
  }
  if (options.id !== undefined) {
    node.id = options.id;
  }
  if (options.text !== undefined) {
    node.textContent = options.text;
  }
  appendChildren(node, children);
  return node;
}

export function svgElement<K extends keyof SVGElementTagNameMap>(
  tagName: K,
  attributes: Readonly<Record<string, string>> = {},
): SVGElementTagNameMap[K] {
  const node = document.createElementNS("http://www.w3.org/2000/svg", tagName);
  for (const [name, value] of Object.entries(attributes)) {
    node.setAttribute(name, value);
  }
  return node;
}

export function link(label: string, href: string, className?: string): HTMLAnchorElement {
  const node = element("a", className === undefined ? { text: label } : { className, text: label });
  node.href = href;
  return node;
}

export function button(label: string, className?: string): HTMLButtonElement {
  const node = element(
    "button",
    className === undefined ? { text: label } : { className, text: label },
  );
  node.type = "button";
  return node;
}

export interface DefinitionRow {
  readonly term: string;
  readonly description: DomChild | readonly DomChild[];
}

export function definitionList(
  rows: readonly DefinitionRow[],
  className = "metadata-list",
): HTMLDListElement {
  const list = element("dl", { className });
  for (const row of rows) {
    list.append(element("dt", { text: row.term }));
    const description = element("dd");
    appendChildren(
      description,
      Array.isArray(row.description) ? row.description : [row.description as DomChild],
    );
    list.append(description);
  }
  return list;
}

export function bulletList(
  values: readonly string[],
  className?: string,
): HTMLUListElement {
  const list = element("ul", className === undefined ? {} : { className });
  for (const value of values) {
    list.append(element("li", { text: value }));
  }
  return list;
}

const dateOnlyFormatter = new Intl.DateTimeFormat("en-GB", {
  day: "numeric",
  month: "long",
  timeZone: "UTC",
  year: "numeric",
});

const dateTimeFormatter = new Intl.DateTimeFormat("en-GB", {
  day: "numeric",
  hour: "2-digit",
  hour12: false,
  minute: "2-digit",
  month: "long",
  timeZone: "Europe/London",
  timeZoneName: "short",
  year: "numeric",
});

export function formatDate(value: string): string {
  const parsed = /^\d{4}-\d{2}-\d{2}$/.test(value)
    ? new Date(`${value}T00:00:00Z`)
    : new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }
  return /^\d{4}-\d{2}-\d{2}$/.test(value)
    ? dateOnlyFormatter.format(parsed)
    : dateTimeFormatter.format(parsed);
}

export function time(value: string): HTMLTimeElement {
  const node = element("time", { text: formatDate(value) });
  node.dateTime = value;
  return node;
}

export function recordHeadingId(recordId: string): string {
  return `record-heading-${encodeURIComponent(recordId)}`;
}

export function viewHeadingId(view: string): string {
  return `view-heading-${encodeURIComponent(view)}`;
}

export function humaniseToken(value: string): string {
  return value
    .split(/[-_]/u)
    .filter(Boolean)
    .map((part) => `${part.charAt(0).toUpperCase()}${part.slice(1)}`)
    .join(" ");
}

export function setCurrentPage(linkNode: HTMLAnchorElement, current: boolean): void {
  if (current) {
    linkNode.setAttribute("aria-current", "page");
  } else {
    linkNode.removeAttribute("aria-current");
  }
}

export function setStatus(node: HTMLElement, message: string): void {
  node.textContent = message;
}
