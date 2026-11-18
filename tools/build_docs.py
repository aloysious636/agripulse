"""Build AgriPulse_Documentation.pdf and .docx from the Markdown sources (needs pandoc + wkhtmltopdf).

Usage:  python tools/build_docs.py
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOC = ROOT / "documentation"
PARTS = ["01_TECHNICAL_DOCUMENTATION.md", "02_INSTALLATION.md", "03_USER_MANUAL.md", "04_DEFENCE_QUESTIONS.md"]
BREAK_BEFORE = ("# 11.", "# 13.", "# 14.", "# 15.", "# 17.", "# 23.", "# 24.", "# Appendix")

CSS = """
body{font-family:'Segoe UI',Arial,sans-serif;font-size:10.5pt;line-height:1.45;color:#22282b;max-width:none}
h1{color:#0f3d2a;border-bottom:2px solid #047857;padding-bottom:3px;margin-top:26px;font-size:19pt}
h2{color:#14532d;margin-top:18px;font-size:14pt} h3{color:#14532d;font-size:12pt}
table{border-collapse:collapse;width:100%;margin:8px 0;font-size:9pt;page-break-inside:auto} tr{page-break-inside:avoid}
th{background:#047857;color:#fff;text-align:left;padding:4px 6px} td{border:1px solid #cfd6cb;padding:4px 6px;vertical-align:top}
tr:nth-child(even) td{background:#f4f7f2}
code{background:#eef2ec;padding:1px 3px;border-radius:3px;font-size:9pt} pre{background:#f4f7f2;border:1px solid #cfd6cb;padding:8px;font-size:8.2pt;white-space:pre-wrap;page-break-inside:avoid}
img{max-width:100%;page-break-inside:avoid} figure{margin:10px 0;text-align:center;page-break-inside:avoid} figcaption{font-size:9pt;color:#5b6561}
header#title-block-header{text-align:center;margin:90px 0 60px;page-break-after:always} h1.title{border:0;font-size:30pt;color:#0f3d2a} p.subtitle{font-size:14pt;color:#047857}
nav#TOC{page-break-after:always} nav#TOC ul{list-style:none;padding-left:14px} nav#TOC>ul{padding-left:0}
"""


def combined(for_docx: bool) -> str:
    out = []
    for name in PARTS:
        text = (DOC / name).read_text(encoding="utf-8")
        text = re.sub(r"\A---\n.*?\n---\n", "", text, flags=re.S)           # drop per-file YAML
        out.append(text.strip())
    md = "\n\n".join(out)
    if for_docx:
        md = md.replace(".svg)", ".png)")
    else:
        for fig in ("![ERD 2 of 3", "![ERD 3 of 3", "![Flowchart 2", "![Flowchart 3", "![Flowchart 4", "![DFD Level 1"):
            md = md.replace(fig, f'<div style="page-break-before:always"></div>\n\n{fig}', 1)
        for marker in BREAK_BEFORE:
            md = md.replace(f"\n{marker}", f'\n\n<div style="page-break-before:always"></div>\n\n{marker}', 1)
    return md


def svg_to_png(tmp: Path) -> None:
    from PIL import Image
    png_dir = DOC / "diagrams"
    for svg in sorted((DOC / "diagrams").glob("*.svg")):
        width = re.search(r'width="(\d+)"', svg.read_text(encoding="utf-8")).group(1)
        raw = tmp / (svg.stem + "_raw.png")
        subprocess.run(["wkhtmltoimage", "--quiet", "--zoom", "1.4", "--width", width, "--format", "png", str(svg), str(raw)],
                       check=True, stderr=subprocess.DEVNULL)
        img = Image.open(raw).convert("RGB")
        bbox = Image.eval(img.convert("L"), lambda v: 255 if v < 250 else 0).getbbox()   # trim blank canvas
        if bbox:
            img = img.crop((0, 0, min(img.width, bbox[2] + 20), min(img.height, bbox[3] + 20)))
        img.quantize(colors=128, method=Image.Quantize.MEDIANCUT).save(png_dir / (svg.stem + ".png"), optimize=True)


def run(cmd, **kw):
    subprocess.run(cmd, check=True, **kw)


def main():
    for tool in ("pandoc", "wkhtmltopdf", "wkhtmltoimage"):
        if not shutil.which(tool):
            sys.exit(f"{tool} is required to build the documents")
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        svg_to_png(tmp)
        (tmp / "doc.css").write_text(CSS, encoding="utf-8")
        meta = ["--metadata", "title=AgriPulse — Smarter Livestock Management",
                "--metadata", "subtitle=Technical Documentation, Installation Guide, User Manual and Project Defence Guide",
                "--metadata", "lang=en"]
        # ---- PDF (via HTML, SVG diagrams)
        (DOC / "_build_pdf.md").write_text(combined(False), encoding="utf-8")
        html = DOC / "_build.html"
        run(["pandoc", str(DOC / "_build_pdf.md"), "-f", "markdown+pipe_tables+link_attributes+raw_html", "-t", "html5", "-s",
             "--toc", "--toc-depth=2", "--css", str(tmp / "doc.css"), "--embed-resources", "--resource-path", str(DOC), "-o", str(html), *meta])
        run(["wkhtmltopdf", "--quiet", "--enable-local-file-access", "--page-size", "A4", "--margin-top", "16mm", "--margin-bottom", "16mm",
             "--margin-left", "14mm", "--margin-right", "14mm", "--footer-center", "AgriPulse — page [page] of [topage]", "--footer-font-size", "8",
             str(html), str(DOC / "AgriPulse_Documentation.pdf")], stderr=subprocess.DEVNULL)
        # ---- DOCX (PNG diagrams)
        (DOC / "_build_docx.md").write_text(combined(True), encoding="utf-8")
        run(["pandoc", str(DOC / "_build_docx.md"), "-f", "markdown+pipe_tables+link_attributes", "-o", str(DOC / "AgriPulse_Documentation.docx"),
             "--toc", "--toc-depth=2", "--resource-path", str(DOC), *meta])
    for tmpfile in ("_build_pdf.md", "_build_docx.md", "_build.html"):
        (DOC / tmpfile).unlink(missing_ok=True)
    print("built:", ", ".join(p.name for p in (DOC / "AgriPulse_Documentation.pdf", DOC / "AgriPulse_Documentation.docx")))


if __name__ == "__main__":
    main()
