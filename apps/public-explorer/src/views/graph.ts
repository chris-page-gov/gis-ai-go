import { element, link, svgElement } from "../dom";
import type { CatalogueRecord, GraphEdge, GraphModel, GraphNode } from "../types";

export interface GraphNavigation {
  readonly hrefForRecord: (recordId: string | null) => string;
  readonly selectRecord: (recordId: string | null) => void;
}

interface PositionedNode {
  readonly node: GraphNode;
  readonly x: number;
  readonly y: number;
}

function recordLink(
  record: GraphNode,
  navigation: GraphNavigation,
): HTMLAnchorElement {
  const node = link(record.title, navigation.hrefForRecord(record.id));
  node.addEventListener("click", (event) => {
    if (
      event.defaultPrevented ||
      event.button !== 0 ||
      event.metaKey ||
      event.ctrlKey ||
      event.shiftKey ||
      event.altKey
    ) {
      return;
    }
    event.preventDefault();
    navigation.selectRecord(record.id);
  });
  return node;
}

function visualEdges(model: GraphModel): readonly GraphEdge[] {
  return model.edges.filter(
    (edge) => !edge.selfReference && edge.from !== edge.to,
  );
}

function positions(nodes: readonly GraphNode[]): readonly PositionedNode[] {
  const columns = nodes.length <= 4 ? 2 : 3;
  const columnWidth = 260;
  const rowHeight = 120;
  return nodes.map((node, index) => ({
    node,
    x: 30 + (index % columns) * columnWidth,
    y: 30 + Math.floor(index / columns) * rowHeight,
  }));
}

function clippedLabel(value: string): string {
  return value.length > 33 ? `${value.slice(0, 30)}…` : value;
}

function renderGraphVisual(model: GraphModel): HTMLElement {
  const wrapper = element("div", { className: "visual-panel" });
  wrapper.append(
    element("p", {
      className: "hint",
      text: "Visual evidence graph. The complete relationship list follows.",
    }),
  );
  const positioned = positions(model.nodes);
  const byId = new Map(positioned.map((item) => [item.node.id, item]));
  const columns = model.nodes.length <= 4 ? 2 : 3;
  const rows = Math.max(1, Math.ceil(model.nodes.length / columns));
  const svg = svgElement("svg", {
    "aria-hidden": "true",
    focusable: "false",
    role: "presentation",
    viewBox: `0 0 ${columns * 260 + 30} ${rows * 120 + 30}`,
  });

  for (const edge of visualEdges(model)) {
    const from = byId.get(edge.from);
    const to = byId.get(edge.to);
    if (from === undefined || to === undefined) {
      continue;
    }
    svg.append(
      svgElement("line", {
        class: "graph-edge",
        x1: String(from.x + 95),
        y1: String(from.y + 32),
        x2: String(to.x + 95),
        y2: String(to.y + 32),
      }),
    );
  }

  for (const item of positioned) {
    const group = svgElement("g", {
      class: `graph-node${item.node.explicitlyIncluded ? " graph-node--match" : ""}`,
      transform: `translate(${item.x} ${item.y})`,
    });
    group.append(
      svgElement("rect", { height: "66", rx: "0", width: "190", x: "0", y: "0" }),
    );
    const title = svgElement("text", { class: "graph-label", x: "10", y: "25" });
    title.textContent = clippedLabel(item.node.title);
    const kind = svgElement("text", { class: "graph-label", x: "10", y: "49" });
    kind.textContent = `${item.node.type}${item.node.explicitlyIncluded ? " — match" : " — source context"}`;
    group.append(title, kind);
    svg.append(group);
  }
  wrapper.append(svg);
  return wrapper;
}

function relatedNodes(
  nodeId: string,
  edges: readonly GraphEdge[],
  direction: "from" | "to",
): readonly string[] {
  const values = edges
    .filter((edge) => edge[direction] === nodeId)
    .map((edge) => (direction === "from" ? edge.to : edge.from));
  return [...new Set(values)].sort();
}

function relationList(
  label: string,
  relatedIds: readonly string[],
  nodesById: ReadonlyMap<string, GraphNode>,
  navigation: GraphNavigation,
): HTMLDivElement {
  const container = element("div");
  container.append(element("h4", { text: label }));
  if (relatedIds.length === 0) {
    container.append(element("p", { text: "None" }));
    return container;
  }
  const list = element("ul");
  for (const recordId of relatedIds) {
    const record = nodesById.get(recordId);
    const item = element("li");
    if (record === undefined) {
      item.textContent = recordId;
    } else {
      item.append(recordLink(record, navigation));
    }
    list.append(item);
  }
  container.append(list);
  return container;
}

function renderAdjacency(model: GraphModel, navigation: GraphNavigation): HTMLElement {
  const section = element("section");
  section.setAttribute("aria-labelledby", "adjacency-heading");
  section.append(
    element("h3", { id: "adjacency-heading", text: "Complete relationship list" }),
    element("p", {
      className: "hint",
      text: "“Cites” means the catalogue record names that source in sourceRefs. Identity self-references are not relationships and are omitted.",
    }),
  );
  const list = element("ol", { className: "adjacency-list" });
  const nodesById = new Map(model.nodes.map((node) => [node.id, node]));
  const edges = visualEdges(model);
  for (const node of model.nodes) {
    const item = element("li");
    const heading = element("h4");
    heading.append(recordLink(node, navigation));
    item.append(
      heading,
      element("p", {
        text: `${node.type}; ${node.explicitlyIncluded ? "catalogue match" : "supporting source context"}. ID: ${node.id}`,
      }),
      relationList("Cites", relatedNodes(node.id, edges, "from"), nodesById, navigation),
      relationList("Cited by", relatedNodes(node.id, edges, "to"), nodesById, navigation),
    );
    list.append(item);
  }
  section.append(list);
  return section;
}

export function renderGraphView(
  model: GraphModel,
  _records: readonly CatalogueRecord[],
  navigation: GraphNavigation,
): HTMLElement {
  const section = element("section");
  section.setAttribute("aria-labelledby", "view-heading-graph");
  section.append(
    element("h2", { id: "view-heading-graph", text: "Evidence graph" }),
    element("p", {
      text: "The graph shows only source relationships explicitly recorded in the catalogue. Shared publishers and topics do not create edges.",
    }),
  );
  if (model.nodes.length === 0) {
    section.append(
      element("div", { className: "empty-state" }, [
        element("h3", { text: "No graph records found" }),
        element("p", { text: "Change or clear the search and filters to see relationships." }),
      ]),
    );
    return section;
  }
  section.append(
    element("p", {
      text: `${model.nodes.filter((node) => node.explicitlyIncluded).length} catalogue matches and ${
        model.nodes.filter((node) => !node.explicitlyIncluded).length
      } supporting source records.`,
    }),
    element("div", { className: "visual-and-alternative" }, [
      renderGraphVisual(model),
      renderAdjacency(model, navigation),
    ]),
  );
  return section;
}
