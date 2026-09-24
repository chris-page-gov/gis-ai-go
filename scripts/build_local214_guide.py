#!/usr/bin/env python3
"""Render the fixed LOCAL-214 Markdown and vector figures; no private inputs."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote, urlsplit

from scripts.build_chronicle import INLINE, blocks, checked_path, svg

ROOT = Path(__file__).resolve().parents[1]
GUIDE = "docs/demonstrations/LOCAL-214_LOCAL_EDITION_WALKTHROUGH.md"
FIGURES = "docs/demonstrations/local214/figures.json"
EDITION = "v0.2.0-local.1"
PDF_NAME = "gis-ai-go-local214-walkthrough.pdf"
PUBLIC = "https://github.com/chris-page-gov/gis-ai-go"
PAGE_MARKER = "<!-- page -->"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def snapshot(root: Path, *, refresh: bool = False) -> dict[str, bytes]:
    names = [GUIDE, FIGURES, "scripts/build_local214_guide.py",
             "scripts/build_chronicle.py", "docs/chronicle/requirements-print.txt",
             "providers/ons/data-query-approved-cache.v1.json", "VERSION"]
    data = {name: checked_path(root, name).read_bytes() for name in names}
    figures = json.loads(data[FIGURES])
    if not isinstance(figures, dict) or len(figures) != 3:
        raise ValueError("The guide must contain its three maintained diagrams")
    for name, spec in figures.items():
        if (not re.fullmatch(r"[a-z-]+", name) or not 1 <= len(spec["steps"]) <= 5
                or any(len(row) != 2 or any(len(text) > 60 for text in row)
                       for row in spec["steps"])):
            raise ValueError("Diagram exceeds the A4 layout contract")
        relative = f"docs/demonstrations/local214/{name}.svg"
        path = checked_path(root, relative, allow_missing=refresh)
        generated = svg(spec)
        if refresh:
            path.write_bytes(generated)
        if path.read_bytes() != generated:
            raise ValueError("Run --refresh-figures for changed diagram sources")
        data[relative] = generated
    text = data[GUIDE].decode()
    parsed = list(parse(text))
    if {value[0] for kind, value in parsed if kind == "figure"} != set(figures):
        raise ValueError("Markdown and diagram inventory disagree")
    return data


def parse(text: str):
    # Reuse the tested restricted Markdown parser without changing its historic book.
    text = re.sub(r"\]\(local214/([a-z-]+)\.svg\)", r"](figures/\1.svg)", text)
    return blocks(text)


def link(target: str, revision: str) -> str:
    target = target.strip("<>")
    parsed = urlsplit(target)
    if parsed.scheme:
        if parsed.scheme != "https" or not parsed.netloc:
            raise ValueError("Guide links must use HTTPS or repository-relative paths")
        return target
    if parsed.netloc or parsed.query:
        raise ValueError("Unsupported guide link")
    relative = (ROOT / GUIDE).parent.joinpath(parsed.path).resolve()
    if not relative.is_relative_to(ROOT) or not relative.is_file():
        raise ValueError("Guide link is not an existing repository file")
    return f"{PUBLIC}/blob/{revision}/{quote(relative.relative_to(ROOT).as_posix())}" + (
        "#" + parsed.fragment if parsed.fragment else ""
    )


def inline(text: str, revision: str) -> str:
    result, last = [], 0
    for match in INLINE.finditer(text):
        result.append(html.escape(text[last:match.start()]))
        label, target, code, bold = match.groups()
        if target:
            result.append(f'<a href="{html.escape(link(target, revision), quote=True)}">'
                          f'{html.escape(label)}</a>')
        elif code:
            result.append(f'<font face="Courier">{html.escape(code)}</font>')
        else:
            result.append(f'<b>{html.escape(bold)}</b>')
        last = match.end()
    result.append(html.escape(text[last:]))
    return "".join(result)


def source_identity(root: Path) -> dict:
    if (root / "local214-source-identity.json").exists():
        from scripts.local214_package import verify
        identity = verify(root)
        return {"source_commit": identity["source_commit"], "source_state": "verified-source-archive"}
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root,
                            capture_output=True, text=True, check=True).stdout.strip()
    dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=all"], cwd=root,
                           capture_output=True, text=True, check=True).stdout
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("A full source revision is required")
    return {"source_commit": commit, "source_state": "development-uncommitted" if dirty else "clean-commit"}


def render(path: Path, data: dict[str, bytes], identity: dict) -> int:
    import reportlab
    from reportlab.graphics.shapes import Drawing, Line, PolyLine, Rect, String
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import mm
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate,
                                    Spacer, Table, TableStyle, XPreformatted)

    if reportlab.Version != "4.4.9":
        raise ValueError("Use the pinned reportlab 4.4.9 documentation dependency")
    width = 174 * mm
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("GuideBody", fontName="Helvetica", fontSize=10.5, leading=14,
                              spaceAfter=7, textColor=colors.HexColor("#203440")))
    styles.add(ParagraphStyle("GuideCell", parent=styles["GuideBody"], fontSize=9, leading=12,
                              spaceAfter=1))
    styles.add(ParagraphStyle("GuideCode", fontName="Courier", fontSize=8.5, leading=11,
                              spaceAfter=8, backColor=colors.HexColor("#f2f6f8"), borderPadding=5))
    styles.add(ParagraphStyle("GuideCaption", parent=styles["GuideBody"], fontSize=9, leading=12))
    styles["Heading1"].fontSize, styles["Heading1"].leading = 21, 26
    styles["Heading2"].fontSize, styles["Heading2"].leading = 16, 20
    figures = json.loads(data[FIGURES])
    revision = identity["source_commit"]

    def drawing(spec):
        height = 34 + len(spec["steps"]) * 52
        d = Drawing(width, height)
        ink, wash = colors.HexColor("#173a53"), colors.HexColor("#f2f6f8")
        d.add(String(width/2, height-15, spec["title"], fontName="Helvetica-Bold",
                     fontSize=13, textAnchor="middle", fillColor=ink))
        for i, (title, detail) in enumerate(spec["steps"]):
            y = height - 70 - i * 52
            d.add(Rect(8, y, width-16, 39, rx=4, fillColor=wash, strokeColor=ink))
            for text, offset, bold in ((title, 24, True), (detail, 10, False)):
                d.add(String(width/2, y+offset, text,
                             fontName="Helvetica-Bold" if bold else "Helvetica",
                             fontSize=10.5, textAnchor="middle", fillColor=ink))
            if i < len(spec["steps"])-1:
                d.add(Line(width/2, y-1, width/2, y-10, strokeColor=ink))
                d.add(PolyLine([width/2-3, y-7, width/2, y-10, width/2+3, y-7], strokeColor=ink))
        return d

    story = []
    for kind, value in parse(data[GUIDE].decode()):
        if kind == "heading":
            level, title = value
            story.append(Paragraph(inline(title, revision), styles[f"Heading{min(level, 3)}"]))
            if level == 1:
                for line in (f"Source: {revision}",
                             f"Build state: {identity['source_state']}; not a release attestation",
                             f"Guide source SHA-256: {digest(data[GUIDE])}"):
                    story.append(Paragraph(html.escape(line), styles["GuideCaption"]))
        elif kind == "paragraph" and value == PAGE_MARKER:
            story.append(PageBreak())
        elif kind in {"paragraph", "item", "ordered_item"}:
            number, text = value if kind == "ordered_item" else (None, value)
            prefix = f"{number}. " if number is not None else "&#8226; " if kind == "item" else ""
            story.append(Paragraph(prefix + inline(text, revision), styles["GuideBody"]))
        elif kind == "code":
            if any(len(line) > 90 for line in value.splitlines()):
                raise ValueError("Split long code lines in the maintained guide")
            story.append(XPreformatted(html.escape(value), styles["GuideCode"]))
        elif kind == "table":
            if len({len(row) for row in value}) != 1:
                raise ValueError("Ragged guide table")
            rows = [[Paragraph(inline(cell, revision), styles["GuideCell"])
                     for cell in row] for row in value]
            ratios = [0.39, 0.61] if value[0][0] == "Symptom" else [0.56, 0.44]
            table = Table(rows, colWidths=[width*ratio for ratio in ratios], repeatRows=1)
            table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e8eff3")),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#a5b6c0")),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]))
            story.extend([table, Spacer(1, 8)])
        elif kind == "figure":
            name, caption = value
            story.append(KeepTogether([drawing(figures[name]),
                                      Paragraph(html.escape(caption), styles["GuideCaption"])]))
    pages = 0

    def footer(canvas, doc):
        nonlocal pages
        pages = doc.page
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.drawString(18*mm, 11*mm, "GIS AI GO | LOCAL-214 | local evaluation guide")
        canvas.drawRightString(A4[0]-18*mm, 11*mm, str(doc.page))
        canvas.restoreState()

    def stable_canvas(*args, **kwargs):
        kwargs["invariant"] = 1
        return Canvas(*args, **kwargs)

    doc = SimpleDocTemplate(str(path), pagesize=A4, leftMargin=18*mm, rightMargin=18*mm,
                            topMargin=17*mm, bottomMargin=18*mm,
                            title="GIS AI GO: your first governed MCP journey", author="GIS AI GO")
    doc.build(story, onFirstPage=footer, onLaterPages=footer, canvasmaker=stable_canvas)
    return pages


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--refresh-figures", action="store_true")
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args()
    data = snapshot(ROOT, refresh=args.refresh_figures)
    identity = source_identity(ROOT)
    for kind, value in parse(data[GUIDE].decode()):
        if kind == "paragraph" and value != PAGE_MARKER:
            inline(value, identity["source_commit"])
    if args.check or args.output_dir is None:
        print(json.dumps({"guide_check": "pass", "diagrams": 3, "pdf_built": False}))
        return
    output = args.output_dir if args.output_dir.is_absolute() else ROOT / args.output_dir
    if ".." in output.parts or not output.is_relative_to(ROOT / "artifacts"):
        raise ValueError("Guide output must be beneath this checkout's ignored artifacts directory")
    output = checked_path(ROOT, output.relative_to(ROOT).as_posix(), allow_missing=True)
    output.mkdir(parents=True, exist_ok=False)
    pages = render(output / PDF_NAME, data, identity)
    if any(checked_path(ROOT, name).read_bytes() != content for name, content in data.items()):
        raise ValueError("Guide input changed during rendering; output is unpromoted")
    if source_identity(ROOT) != identity:
        raise ValueError("Source identity changed during rendering; output is unpromoted")
    manifest = {
        "schema": "gis-ai-go.local214-guide.v1", "edition": EDITION, **identity,
        "software_version": data["VERSION"].decode().strip(), "target_release": "0.2.0",
        "inputs": {name: digest(value) for name, value in sorted(data.items())},
        "outputs": {PDF_NAME: digest((output / PDF_NAME).read_bytes())},
        "pages": pages, "vector_diagrams": 3, "renderer": "reportlab-4.4.9",
        "release_attestation": False, "human_usability_acceptance": False,
    }
    (output / "guide-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"guide_check": "pass", "pdf_built": True, "pages": pages,
                      "source_state": identity["source_state"]}))


if __name__ == "__main__":
    main()
