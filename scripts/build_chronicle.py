#!/usr/bin/env python3
"""Build the public chronicle from a fixed allowlist; never ingest private evidence.

HTML, SVG and CSV use the standard library. Optional A4 PDF uses the separately
pinned reportlab documentation dependency. Markdown support is deliberately small:
headings, paragraphs, lists, tables, fences, links and single-image paragraphs.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import json
import os
import re
import stat
import subprocess
import tempfile
import textwrap
from datetime import datetime
from pathlib import Path
from urllib.parse import quote
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/chronicle"
BASELINE = "6c76c92a18da779766f8d49acbbd7dbbd31abb97"
PUBLIC = "https://github.com/chris-page-gov/gis-ai-go"
CHAPTERS = (
    "README.md", "NARRATIVE.md", "LEARNING_PATH.md", "AGENT_HISTORY.md",
    "CLAUDE_RETROSPECTIVE.md", "CODE_REVIEW.md", "GUIDANCE_REVIEW.md",
    "LOCAL_COMPLETION_PLAN.md", "IMPROVEMENT_PLAN.md", "EVIDENCE_METHOD.md",
    "reviews/RUNTIME_REVIEW.md", "reviews/ASSURANCE_AND_UI_REVIEW.md",
)
DATA_NAMES = ("data/commits.csv", "data/claims.json", "data/agent-census.csv", "data/agent-census.json",
              "data/claude-observations.csv", "data/claude-observations.json", "reviews/ASSURANCE_SOURCE_INVENTORY.json")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def checked_path(root: Path, relative: str, *, allow_missing: bool = False) -> Path:
    """Reject links and special files before any source read or output write."""
    parts = Path(relative).parts
    if Path(relative).is_absolute() or ".." in parts or not parts:
        raise ValueError("Path is outside the declared root")
    current = root
    if root.is_symlink() or not root.is_dir():
        raise ValueError("Root must be a real directory")
    for index, part in enumerate(parts):
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            if allow_missing:
                continue
            raise
        if stat.S_ISLNK(mode) or not (stat.S_ISDIR(mode) or stat.S_ISREG(mode)):
            raise ValueError("Links and special files are not admitted")
        if index < len(parts) - 1 and not stat.S_ISDIR(mode):
            raise ValueError("Parent must be a directory")
    return current


def source_bytes(relative: str) -> bytes:
    # Walk from the canonical checkout, including docs/ and chronicle/ themselves.
    path = checked_path(ROOT, "docs/chronicle/" + relative)
    if not path.is_file():
        raise ValueError("Source must be a regular file")
    return path.read_bytes()


def validate_output(directory: Path, names: list[str]) -> None:
    if not directory.exists():
        return
    if directory.is_symlink() or not directory.is_dir():
        raise ValueError("Output must be a real directory")
    children = list(directory.iterdir())
    if not children:
        return
    expected = set(names) | {"manifest.json"}
    if {p.name for p in children} != expected:
        raise ValueError("Output inventory differs; select a new empty output directory")
    for child in children:
        if not stat.S_ISREG(child.lstat().st_mode):
            raise ValueError("Output links or special files are not admitted")
    previous = json.loads((directory / "manifest.json").read_text())
    if previous.get("format") != "gis-ai-go-chronicle-build-v1" or set(previous.get("outputs", {})) != set(names):
        raise ValueError("Existing directory is not a complete chronicle build")
    if any(digest((directory / name).read_bytes()) != previous["outputs"][name] for name in names):
        raise ValueError("Previous output bytes changed; select a new empty output directory")


def anchor(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def url(target: str, source: str) -> str:
    target = target.strip("<>")
    if target.startswith(("https://", "http://", "mailto:")):
        return target
    if target.startswith("#"):
        return "#" + anchor(source) + "--" + target[1:]
    path, _, fragment = target.partition("#")
    resolved = (SOURCE / source).parent.joinpath(path).resolve()
    if not resolved.is_relative_to(ROOT):
        raise ValueError("Source link escapes repository")
    relative = resolved.relative_to(ROOT).as_posix()
    book_relative = resolved.relative_to(SOURCE).as_posix() if resolved.is_relative_to(SOURCE) else None
    if book_relative in CHAPTERS:
        return "#" + anchor(book_relative) + ("--" + fragment if fragment else "")
    if book_relative and (book_relative.startswith("data/") or book_relative == "reviews/ASSURANCE_SOURCE_INVENTORY.json"):
        return quote(Path(book_relative).name)
    return f"{PUBLIC}/blob/{BASELINE}/{quote(relative)}" + ("#" + fragment if fragment else "")


INLINE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)|`([^`]+)`|\*\*([^*]+)\*\*")


def inline(text: str, source: str, pdf: bool = False) -> str:
    result, last = [], 0
    for match in INLINE.finditer(text):
        result.append(html.escape(text[last:match.start()]))
        label, target, code, bold = match.groups()
        if target:
            href = html.escape(url(target, source), quote=True)
            # PDF internal destinations are omitted; the chapter remains in its TOC.
            result.append(html.escape(label) if pdf and href.startswith("#") else
                          f'<a href="{href}">{html.escape(label)}</a>')
        elif code:
            tag = 'font face="Courier"' if pdf else "code"
            end = "font" if pdf else "code"
            result.append(f"<{tag}>{html.escape(code)}</{end}>")
        else:
            result.append(f"<b>{html.escape(bold)}</b>")
        last = match.end()
    result.append(html.escape(text[last:]))
    return "".join(result)


def blocks(text: str):
    lines, i = text.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith("```"):
            rows, i = [], i + 1
            while i < len(lines) and not lines[i].startswith("```"):
                rows.append(lines[i]); i += 1
            if i == len(lines):
                raise ValueError("Unclosed code fence")
            yield "code", "\n".join(rows)
        elif match := re.match(r"^(#{1,6}) (.*)", line):
            yield "heading", (len(match[1]), match[2])
        elif match := re.fullmatch(r"!\[([^\]]*)\]\(figures/([a-z-]+)\.svg\)", line):
            yield "figure", (match[2], match[1])
        elif line.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [x.strip() for x in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", x) for x in cells):
                    rows.append(cells)
                i += 1
            i -= 1
            yield "table", rows
        elif match := re.match(r"^\s*(?:([-*])|(\d+)[.)]) (.*)", line):
            parts = [match[3]]
            while i + 1 < len(lines) and re.match(r"^\s{2,}\S", lines[i + 1]):
                i += 1; parts.append(lines[i].strip())
            yield ("ordered_item", (int(match[2]), " ".join(parts))) if match[2] else ("item", " ".join(parts))
        else:
            parts = [line.strip()]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(
                r"^(#{1,6} |```|\||!\[|\s*(?:[-*]|\d+[.)]) )", lines[i + 1]
            ):
                i += 1; parts.append(lines[i].strip())
            yield "paragraph", " ".join(parts)
        i += 1


def svg(spec: dict) -> bytes:
    height = 78 + 90 * len(spec["steps"])
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="640" height="{height}" viewBox="0 0 640 {height}" role="img">',
             f'<title>{html.escape(spec["title"])}</title>',
             f'<desc>{html.escape(spec["description"])}</desc>',
             '<rect width="100%" height="100%" fill="white"/>',
             f'<text x="320" y="30" text-anchor="middle" font-family="sans-serif" font-size="21" font-weight="bold" fill="#173a53">{html.escape(spec["title"])}</text>']
    for i, (title, detail) in enumerate(spec["steps"]):
        y = 54 + i * 90
        parts += [f'<rect x="24" y="{y}" width="592" height="67" rx="7" fill="#f2f6f8" stroke="#426477" stroke-width="2"/>',
                  f'<text x="320" y="{y+25}" text-anchor="middle" font-family="sans-serif" font-size="19" font-weight="bold" fill="#173a53">{html.escape(title)}</text>',
                  f'<text x="320" y="{y+49}" text-anchor="middle" font-family="sans-serif" font-size="16" fill="#253a45">{html.escape(detail)}</text>']
        if i < len(spec["steps"]) - 1:
            parts += [f'<path d="M320 {y+70} V{y+84} M314 {y+79} L320 {y+85} L326 {y+79}" fill="none" stroke="#426477" stroke-width="2"/>']
    return ("\n".join(parts) + "\n</svg>\n").encode()


def commit_ledger() -> bytes:
    raw = subprocess.run(["git", "log", "--reverse", "--format=%H%x09%cI%x09%s", BASELINE],
                         cwd=ROOT, capture_output=True, text=True, check=True).stdout
    result = io.StringIO(newline="")
    writer = csv.writer(result, lineterminator="\n")
    writer.writerow(["commit", "recorded_at_london", "subject", "source_url"])
    for line in raw.splitlines():
        sha, stamp, subject = line.split("\t", 2)
        stamp = datetime.fromisoformat(stamp.replace("Z", "+00:00")).astimezone(ZoneInfo("Europe/London")).isoformat()
        writer.writerow([sha, stamp, subject, f"{PUBLIC}/commit/{sha}"])
    return result.getvalue().encode()


def build_html(chapters: list, figures: dict) -> str:
    css = """body{font:18px/1.55 system-ui,sans-serif;color:#203440;background:#f4f6f8;margin:0}
main{max-width:900px;margin:auto;padding:2rem 3rem;background:white}a{color:#005a83}
h1,h2,h3{line-height:1.2;color:#173a53}section{margin:4rem 0}code,pre{font-size:.85em}
pre{white-space:pre-wrap;background:#f2f6f8;padding:1rem}table{border-collapse:collapse;width:100%;font-size:.85em}
td,th{border:1px solid #adbac3;padding:.45rem;text-align:left;vertical-align:top;overflow-wrap:anywhere}
figure{margin:1.5rem 0}svg{max-width:100%;height:auto}p,li{overflow-wrap:anywhere}
nav{border:1px solid #adbac3;padding:1rem}header p{font-size:1.1rem}
@page{size:A4;margin:18mm}@media print{body{background:white;font-size:11pt}main{padding:0}
section{break-before:page}figure,pre{break-inside:avoid}nav{display:none}a{color:inherit}h2,h3{break-after:avoid}}"""
    output = ['<!doctype html><html lang="en-GB"><head><meta charset="utf-8">',
              '<meta name="viewport" content="width=device-width,initial-scale=1">',
              '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; img-src data:; base-uri \'none\'; form-action \'none\'">',
              '<title>How we built GIS AI GO - Volume 1</title><style>' + css + '</style></head><body><main>',
              '<header><h1>How we built GIS AI GO</h1><p>Volume 1 · Review edition · 14 September 2026</p></header>',
              '<nav aria-label="Chapters"><ol>']
    for name, text in chapters:
        title = text.splitlines()[0].lstrip("# ")
        output.append(f'<li><a href="#{anchor(name)}">{html.escape(title)}</a></li>')
    output.append('</ol></nav>')
    for name, text in chapters:
        output.append(f'<section id="{anchor(name)}">')
        in_list = None
        heading_counts = {}
        for kind, data in blocks(text):
            list_tag = "ul" if kind == "item" else "ol" if kind == "ordered_item" else None
            if in_list and list_tag != in_list:
                output.append(f"</{in_list}>"); in_list = None
            if kind == "heading":
                level, title = data
                slug = anchor(title)
                count = heading_counts.get(slug, 0)
                heading_counts[slug] = count + 1
                ident = anchor(name) + "--" + slug + (f"-{count}" if count else "")
                output.append(f'<h{min(level+1,6)} id="{ident}">{inline(title,name)}</h{min(level+1,6)}>')
            elif kind in ("paragraph", "item", "ordered_item"):
                if list_tag and not in_list:
                    output.append(f"<{list_tag}>"); in_list = list_tag
                number, value = data if kind == "ordered_item" else (None, data)
                tag = "li" if list_tag else "p"
                attribute = f' value="{number}"' if number is not None else ""
                output.append(f'<{tag}{attribute}>{inline(value,name)}</{tag}>')
            elif kind == "code":
                output.append('<pre><code>' + html.escape(data) + '</code></pre>')
            elif kind == "table":
                output.append('<table>')
                for i, row in enumerate(data):
                    tag = "th" if i == 0 else "td"
                    output.append('<tr>' + ''.join(f'<{tag}>{inline(cell,name)}</{tag}>' for cell in row) + '</tr>')
                output.append('</table>')
            elif kind == "figure":
                key, alt = data
                output.append('<figure>' + svg(figures[key]).decode() + f'<figcaption>{html.escape(alt)}</figcaption></figure>')
        if in_list:
            output.append(f"</{in_list}>")
        output.append('</section>')
    output.append('</main></body></html>\n')
    return "\n".join(output)


def build_pdf(path: Path, chapters: list, figures: dict) -> None:
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_LEFT
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.pdfgen.canvas import Canvas
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle, KeepTogether
    from reportlab.platypus.tableofcontents import TableOfContents
    from reportlab.graphics.shapes import Drawing, Rect, String, Line, PolyLine

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="Body", fontName="Helvetica", fontSize=10.5, leading=14.5,
                              spaceAfter=7, textColor=colors.HexColor("#203440"), splitLongWords=True))
    styles.add(ParagraphStyle(name="Cell", parent=styles["Body"], fontSize=8, leading=10, spaceAfter=2))
    styles.add(ParagraphStyle(name="Mono", parent=styles["Body"], fontName="Courier", fontSize=8, leading=10))
    styles["Heading1"].fontSize = 23; styles["Heading1"].leading = 28
    styles["Heading2"].fontSize = 15; styles["Heading2"].leading = 19
    styles["Heading3"].fontSize = 12; styles["Heading3"].leading = 16
    width = A4[0] - 36 * mm
    story = [Paragraph("How we built GIS AI GO", styles["Title"]), Spacer(1, 12*mm),
             Paragraph("Volume 1: from research to a local MCP candidate", styles["Heading2"]),
             Paragraph("Autonomous coding under human governance", styles["Heading2"]),
             Spacer(1, 12*mm), Paragraph("Review edition · 14 September 2026", styles["Body"]),
             Paragraph("Baseline: " + BASELINE, styles["Mono"]),
             Paragraph("Canonical sources, methodology and limitations are included in this volume. Private source records remain local.", styles["Body"]),
             PageBreak(), Paragraph("Reading route", styles["Heading1"])]
    contents = TableOfContents()
    contents.levelStyles = [ParagraphStyle(name="Contents", parent=styles["Body"], rightIndent=20)]
    story.append(contents)

    def drawing(spec):
        scale = width / 640
        height = (78 + 90 * len(spec["steps"])) * scale
        d = Drawing(width, height)
        def txt(x, y, text, size, bold=False):
            d.add(String(x*scale, height-y*scale, text, fontName="Helvetica-Bold" if bold else "Helvetica",
                         fontSize=size*scale, textAnchor="middle", fillColor=colors.HexColor("#173a53")))
        txt(320, 30, spec["title"], 21, True)
        for i,(title,detail) in enumerate(spec["steps"]):
            y=54+i*90
            d.add(Rect(24*scale,height-(y+67)*scale,592*scale,67*scale,rx=7*scale,
                       fillColor=colors.HexColor("#f2f6f8"),strokeColor=colors.HexColor("#426477")))
            txt(320,y+25,title,19,True); txt(320,y+49,detail,16)
            if i<len(spec["steps"])-1:
                d.add(Line(320*scale,height-(y+70)*scale,320*scale,height-(y+84)*scale))
                d.add(PolyLine([314*scale,height-(y+79)*scale,320*scale,height-(y+85)*scale,326*scale,height-(y+79)*scale]))
        return d

    for name,text in chapters:
        story.append(PageBreak())
        for kind,data in blocks(text):
            if kind=="heading":
                level,title=data
                heading = Paragraph(inline(title,name,True),styles[f"Heading{min(level,3)}"])
                if level == 1:
                    heading.chapter_name = name
                story.append(heading)
            elif kind in ("paragraph","item","ordered_item"):
                number,value=data if kind=="ordered_item" else (None,data)
                prefix=f"{number}. " if number is not None else "&#8226; " if kind=="item" else ""
                story.append(Paragraph(prefix+inline(value,name,True),styles["Body"]))
            elif kind=="code":
                for line in data.splitlines():
                    for wrapped in textwrap.wrap(line,90,replace_whitespace=False,drop_whitespace=False) or [""]:
                        story.append(Paragraph(html.escape(wrapped).replace(" ","&#160;"),styles["Mono"]))
                story.append(Spacer(1,5))
            elif kind=="table":
                if len({len(row) for row in data}) != 1:
                    raise ValueError("Ragged Markdown table")
                rows=[[Paragraph(inline(cell,name,True),styles["Cell"]) for cell in row] for row in data]
                table=Table(rows,colWidths=[width/len(data[0])]*len(data[0]),repeatRows=1,hAlign="LEFT")
                table.setStyle(TableStyle([("VALIGN",(0,0),(-1,-1),"TOP"),("BACKGROUND",(0,0),(-1,0),colors.HexColor("#e8eff3")),
                                           ("GRID",(0,0),(-1,-1),0.3,colors.HexColor("#a5b6c0")),("LEFTPADDING",(0,0),(-1,-1),5),
                                           ("RIGHTPADDING",(0,0),(-1,-1),5),("TOPPADDING",(0,0),(-1,-1),5),("BOTTOMPADDING",(0,0),(-1,-1),5)]))
                story.extend([table,Spacer(1,8)])
            elif kind=="figure":
                story.append(KeepTogether([drawing(figures[data[0]]),Spacer(1,5),
                                          Paragraph(html.escape(data[1]),styles["Body"]),Spacer(1,8)]))

    def footer(canvas, doc):
        canvas.saveState(); canvas.setFont("Helvetica",8); canvas.setFillColor(colors.HexColor("#426477"))
        canvas.drawString(18*mm,11*mm,"GIS AI GO · Volume 1 · review edition")
        canvas.drawRightString(A4[0]-18*mm,11*mm,str(doc.page)); canvas.restoreState()
    def stable_canvas(*args,**kwargs):
        kwargs["invariant"]=1
        return Canvas(*args,**kwargs)
    class ChronicleDocument(SimpleDocTemplate):
        def afterFlowable(self, flowable):
            name = getattr(flowable, "chapter_name", None)
            if name:
                key = anchor(name)
                self.canv.bookmarkPage(key)
                self.canv.addOutlineEntry(flowable.getPlainText(), key, 0, False)
                self.notify("TOCEntry", (0, flowable.getPlainText(), self.page, key))

    doc=ChronicleDocument(str(path),pagesize=A4,rightMargin=18*mm,leftMargin=18*mm,
                          topMargin=18*mm,bottomMargin=20*mm,title="How we built GIS AI GO - Volume 1",
                          author="GIS AI GO",pageCompression=1)
    doc.multiBuild(story,onFirstPage=footer,onLaterPages=footer,canvasmaker=stable_canvas)


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=Path("artifacts/chronicle"))
    parser.add_argument("--pdf",action="store_true")
    parser.add_argument("--refresh-source-assets",action="store_true")
    args=parser.parse_args()
    input_names = (*CHAPTERS, "figures.json", "requirements-print.txt", *DATA_NAMES[1:])
    snapshot = {name: source_bytes(name) for name in input_names}
    script_bytes = Path(__file__).read_bytes()
    figures=json.loads(snapshot["figures.json"])
    assets={"data/commits.csv":commit_ledger(),**{f"figures/{key}.svg":svg(value) for key,value in figures.items()}}
    for name,data in assets.items():
        path=checked_path(ROOT, "docs/chronicle/" + name, allow_missing=args.refresh_source_assets)
        if args.refresh_source_assets:
            path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(data)
        elif not path.exists() or path.read_bytes()!=data:
            raise ValueError(f"Regenerate source asset: {name}")
        snapshot[name] = data
    chapters=[(name,snapshot[name].decode()) for name in CHAPTERS]
    requested = args.output if args.output.is_absolute() else ROOT / args.output
    if ".." in requested.parts or not requested.is_relative_to(ROOT / "artifacts"):
        raise ValueError("Output must be beneath this checkout's artifacts directory")
    output=checked_path(ROOT,requested.relative_to(ROOT).as_posix(),allow_missing=True)
    inputs={"docs/chronicle/"+name:digest(data) for name,data in snapshot.items()}
    inputs["scripts/build_chronicle.py"]=digest(script_bytes)
    names=["index.html", *[Path(name).name for name in DATA_NAMES]]+(["how-we-built-gis-ai-go-volume-1.pdf"] if args.pdf else [])
    validate_output(output,names)
    output.parent.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="chronicle-stage-",dir=output.parent) as temp:
        stage=Path(temp)
        (stage/"index.html").write_text(build_html(chapters,figures))
        for name in DATA_NAMES:
            (stage/Path(name).name).write_bytes(snapshot[name])
        if args.pdf:
            build_pdf(stage/"how-we-built-gis-ai-go-volume-1.pdf",chapters,figures)
        manifest={"format":"gis-ai-go-chronicle-build-v1","schema_version":1,"baseline":BASELINE,"edition":"review-2026-09-14",
                  "inputs":inputs,"outputs":{name:digest((stage/name).read_bytes()) for name in names},
                  "public_projection_review":"required-before-publication","attested":False}
        (stage/"manifest.json").write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n")
        if any(source_bytes(name) != data for name,data in snapshot.items()) or Path(__file__).read_bytes() != script_bytes:
            raise ValueError("Source changed during rendering; repeat the build from stable inputs")
        validate_output(output,names)
        output.mkdir(parents=True,exist_ok=True)
        for name in [*names,"manifest.json"]:
            os.replace(stage/name,output/name)
    print(json.dumps({"chapters":len(chapters),"diagrams":len(figures),"pdf":args.pdf,"baseline":BASELINE}))


if __name__=="__main__":
    main()
