"""Generate documentation diagrams (SVG) with the standard library.

* ERD is generated from the real SQLAlchemy metadata, so it always matches the schema.
* Use-case, data-flow and flowchart diagrams are drawn from small declarative descriptions.
Run:  python tools/make_diagrams.py
"""
import html
import sys
import tempfile
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
OUT = ROOT / "documentation" / "diagrams"
OUT.mkdir(parents=True, exist_ok=True)

FOREST, EMERALD, SOFT, LINE, TEXT = "#0f3d2a", "#047857", "#ecfdf5", "#9aa89f", "#22282b"
FONT = 'font-family="Segoe UI, Arial, sans-serif"'


def esc(s):
    return html.escape(str(s), quote=True)


def svg_doc(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" {FONT}>'
            f'<title>{esc(title)}</title><rect width="{w}" height="{h}" fill="#ffffff"/>'
            '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{FOREST}"/></marker></defs>{body}</svg>')


def text(x, y, s, size=12, anchor="middle", weight="normal", fill=TEXT):
    return f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}">{esc(s)}</text>'


def wrapped(cx, cy, s, width_chars, size=12, weight="normal", fill=TEXT):
    lines = textwrap.wrap(s, width_chars) or [""]
    y0 = cy - (len(lines) - 1) * (size + 3) / 2 + size / 3
    return "".join(text(cx, y0 + i * (size + 3), ln, size, weight=weight, fill=fill) for i, ln in enumerate(lines))


def head(x, y, ang, color=FOREST, size=10):
    import math
    bx, by = x - size * math.cos(ang), y - size * math.sin(ang)
    px, py = -math.sin(ang) * size * 0.4, math.cos(ang) * size * 0.4
    return f'<polygon points="{x:.1f},{y:.1f} {bx + px:.1f},{by + py:.1f} {bx - px:.1f},{by - py:.1f}" fill="{color}"/>'


def line(x1, y1, x2, y2, arrow=True, dash=False, color=FOREST):
    d = ' stroke-dasharray="5,4"' if dash else ""
    m = ' marker-end="url(#arr)"' if arrow else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="1.6"{d}{m}/>'


# ======================================================================= ERD (from metadata)
ERD_GROUPS = [
    ("Reference & settings", "#6b7280", ["species", "breeds", "production_categories", "animal_groups", "farm_settings"]),
    ("Core", "#047857", ["animals", "weight_records", "notifications"]),
    ("Breeding", "#be185d", ["heat_records", "breeding_records", "pregnancy_records", "birth_records"]),
    ("Health & management", "#1d4ed8", ["health_records", "treatment_records", "vaccination_records", "mortality_records", "routine_tasks"]),
    ("Nutrition", "#b45309", ["feed_items", "stock_movements", "feeding_records", "feeding_schedules", "rations", "ration_items"]),
    ("Production & finance", "#7c3aed", ["production_records", "lactation_records", "slaughter_records", "financial_transactions"]),
]


def draw_erd(tables, groups, stubs, filename, title, note):
    """Draw selected groups as table boxes. ``stubs`` are tables defined in another diagram (header-only, dashed)."""
    W, GAP, ROW, HEAD, TOP = 250, 70, 16, 26, 78
    colors = {t: c for _, c, ts in ERD_GROUPS for t in ts}
    boxes, body = {}, [text(20, 30, title, 17, "start", "bold", FOREST), text(20, 50, note, 11.5, "start", fill="#5b6561")]
    columns = ([("Defined in another diagram", "#9ca3af", stubs)] if stubs else []) + list(groups)
    for ci, (gname, gcolor, names) in enumerate(columns):
        x, y = 20 + ci * (W + GAP), TOP + 20
        body.append(text(x + W / 2, TOP + 8, gname, 13, weight="bold", fill=gcolor))
        is_stub = bool(stubs) and ci == 0
        for name in names:
            t = tables[name]
            color = colors[name]
            if is_stub:
                h = HEAD + 22
                boxes[name] = (x, y, W, h)
                body.append(f'<rect x="{x}" y="{y}" width="{W}" height="{h}" rx="6" fill="#f9fafb" stroke="{color}" stroke-width="1.6" stroke-dasharray="6,4"/>')
                body.append(f'<rect x="{x}" y="{y}" width="{W}" height="{HEAD}" rx="6" fill="{color}" opacity="0.85"/>')
                body.append(text(x + W / 2, y + 17, name, 13, weight="bold", fill="#fff"))
                body.append(text(x + W / 2, y + HEAD + 15, "(full definition in the diagram where it belongs)", 10, fill="#6b7280"))
                y += h + 26
                continue
            pk = [c for c in t.columns if c.primary_key]
            fk = [c for c in t.columns if c.foreign_keys and not c.primary_key]
            rest = [c for c in t.columns if c not in pk and c not in fk and c.name not in ("created_at", "updated_at")]
            shown = (pk + fk + rest)[:9]
            hidden = len(t.columns) - len(shown)
            h = HEAD + (len(shown) + (1 if hidden > 0 else 0)) * ROW + 8
            boxes[name] = (x, y, W, h)
            body.append(f'<rect x="{x}" y="{y}" width="{W}" height="{h}" rx="6" fill="#fff" stroke="{color}" stroke-width="1.6"/>')
            body.append(f'<rect x="{x}" y="{y}" width="{W}" height="{HEAD}" rx="6" fill="{color}"/>')
            body.append(text(x + W / 2, y + 17, name, 13, weight="bold", fill="#fff"))
            for i, c in enumerate(shown):
                ty = y + HEAD + 14 + i * ROW
                tag = "PK" if c.primary_key else ("FK" if c.foreign_keys else ("U" if c.unique else ""))
                body.append(text(x + 8, ty, tag, 10, "start", "bold", color))
                body.append(text(x + 32, ty, f"{c.name}{'*' if not c.nullable and not c.primary_key else ''}", 11.5, "start"))
                body.append(text(x + W - 8, ty, str(c.type).split("(")[0].lower(), 10.5, "end", fill="#6b7280"))
            if hidden > 0:
                body.append(text(x + 32, y + HEAD + 14 + len(shown) * ROW, f"… +{hidden} more columns", 11, "start", fill="#6b7280"))
            y += h + 26
    edges, n_edges = [], 0
    for name in boxes:
        t = tables[name]
        if stubs and name in stubs:
            continue
        targets = {fkc.column.table.name for fkc in t.foreign_keys}
        for tgt in targets:
            if tgt not in boxes:
                continue
            n_edges += 1
            sx, sy, sw, sh = boxes[name]
            c = colors[name]
            if tgt == name:
                edges.append(f'<path d="M{sx + sw},{sy + 30} C{sx + sw + 45},{sy + 30} {sx + sw + 45},{sy + 60} {sx + sw},{sy + 60}" fill="none" stroke="{c}" stroke-width="1.3" marker-end="url(#arr)"/>')
                continue
            tx, ty, tw, th = boxes[tgt]
            x1, x2 = (sx + sw, tx) if tx > sx else ((sx, tx + tw) if tx < sx else (sx + sw, tx + tw))
            y1, y2 = sy + sh / 2, ty + th / 2
            mid = (x1 + x2) / 2 if tx != sx else x1 + 60
            edges.append(f'<path d="M{x1},{y1} C{mid},{y1} {mid},{y2} {x2},{y2}" fill="none" stroke="{c}" stroke-width="1.3" opacity="0.6" marker-end="url(#arr)"/>')
    width = 40 + len(columns) * (W + GAP) - GAP
    height = max(b[1] + b[3] for b in boxes.values()) + 40
    (OUT / filename).write_text(svg_doc(width, height, "".join(edges) + "".join(body), title), encoding="utf-8")
    return len(boxes) - len(stubs or []), n_edges


def make_erd():
    import warnings
    warnings.filterwarnings("ignore")
    from app import create_app
    from app.extensions import db
    app = create_app(data_dir=tempfile.mkdtemp(), config_overrides={"TESTING": True})
    with app.app_context():
        tables = db.metadata.tables
        assert {t for _, _, ts in ERD_GROUPS for t in ts} == set(tables)
        note = "PK primary key · FK foreign key · U unique · * required · up to 9 columns shown per table"
        g = {n: (n, c, ts) for n, c, ts in ERD_GROUPS}
        n_fk = sum(len(t.foreign_keys) for t in tables.values())
        draw_erd(tables, ERD_GROUPS, [], "erd.svg", "AgriPulse — Entity Relationship Diagram (full, generated from the live database schema)", note)
        draw_erd(tables, [g["Reference & settings"], g["Core"], g["Breeding"]], [], "erd_1_core.svg",
                 "ERD 1 of 3 — Reference data, animals and breeding", note)
        draw_erd(tables, [g["Health & management"], g["Production & finance"]], ["animals", "animal_groups", "species"], "erd_2_health_production.svg",
                 "ERD 2 of 3 — Health, management, production and finance", note)
        draw_erd(tables, [g["Nutrition"]], ["animals", "animal_groups", "species"], "erd_3_nutrition.svg",
                 "ERD 3 of 3 — Nutrition and feeding", note)
        (OUT / "erd_print.svg").unlink(missing_ok=True)
        return len(tables), n_fk


# ======================================================================= use case
def make_usecase():
    actors = [("Farmer /\nFarm manager", 70, 300), ("Extension officer /\nStudent (view & report)", 70, 560)]
    cases = ["Register & manage animals", "Record breeding & births", "Manage health & vaccination", "Schedule routine activities",
             "Manage feeds & feeding", "Record production", "Monitor growth & weights", "View farm calendar",
             "Receive alerts & reminders", "Record income & expenses", "Generate reports (PDF / CSV)", "Configure settings & species", "Back up & restore data"]
    pos = {c: (400 + (i % 2) * 320, 135 + (i // 2) * 125) for i, c in enumerate(cases)}
    body = [text(20, 28, "AgriPulse — Use Case Diagram", 18, "start", "bold", FOREST),
            f'<rect x="230" y="50" width="660" height="920" rx="14" fill="{SOFT}" stroke="{EMERALD}" stroke-width="2"/>',
            text(560, 76, "AgriPulse (offline desktop system)", 14, weight="bold", fill=EMERALD)]
    viewer = ["Receive alerts & reminders", "View farm calendar", "Generate reports (PDF / CSV)", "Monitor growth & weights"]
    for c in cases:                                   # connectors first: ellipse fills then hide any crossings
        cx, cy = pos[c]
        body.append(f'<line x1="96" y1="285" x2="{cx - 138}" y2="{cy}" stroke="{FOREST}" stroke-width="1" opacity="0.5"/>')
    for c in viewer:
        cx, cy = pos[c]
        body.append(f'<line x1="96" y1="545" x2="{cx - 138}" y2="{cy}" stroke="#b45309" stroke-width="1.3" stroke-dasharray="5,3"/>')
    for c in cases:
        cx, cy = pos[c]
        body.append(f'<ellipse cx="{cx}" cy="{cy}" rx="140" ry="40" fill="#fff" stroke="{EMERALD}" stroke-width="1.6"/>')
        body.append(wrapped(cx, cy, c, 22, 12.5))
    for name, x, y in actors:
        body.append(f'<circle cx="{x}" cy="{y - 32}" r="14" fill="#fff" stroke="{FOREST}" stroke-width="2"/>'
                    f'<path d="M{x},{y - 18} L{x},{y + 22} M{x - 24},{y - 6} L{x + 24},{y - 6} M{x},{y + 22} L{x - 18},{y + 52} M{x},{y + 22} L{x + 18},{y + 52}" stroke="{FOREST}" stroke-width="2" fill="none"/>')
        for k, ln in enumerate(name.split("\n")):
            body.append(text(x, y + 74 + k * 15, ln, 12, weight="bold"))
    body.append(text(560, 950, "Solid lines: full access (single-user desktop application).  Dashed lines: read / report-oriented use.", 11, fill="#5b6561"))
    (OUT / "use_case.svg").write_text(svg_doc(920, 990, "".join(body), "Use case diagram"), encoding="utf-8")


# ======================================================================= DFD
def entity(x, y, w, h, label):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="{FOREST}" stroke-width="2"/>' + wrapped(x + w / 2, y + h / 2, label, 16, 12.5, "bold")


def process(cx, cy, r, num, label):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{SOFT}" stroke="{EMERALD}" stroke-width="2"/>'
            + text(cx, cy - r + 20, num, 12, weight="bold", fill=EMERALD) + wrapped(cx, cy + 6, label, 14, 11.5, "bold"))


def store(x, y, w, h, label):
    return (f'<line x1="{x}" y1="{y}" x2="{x + w}" y2="{y}" stroke="{FOREST}" stroke-width="2"/><line x1="{x}" y1="{y + h}" x2="{x + w}" y2="{y + h}" stroke="{FOREST}" stroke-width="2"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#f8faf7" stroke="none"/>' + wrapped(x + w / 2, y + h / 2, label, 22, 11.5))


def labelled_flow(x1, y1, x2, y2, label_x, label_y, lines, color=FOREST):
    """Straight flow with explicit arrowhead; label lines are written at fixed, hand-chosen positions."""
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    out = (f'<line x1="{x1}" y1="{y1}" x2="{x2 - 9 * math.cos(ang):.1f}" y2="{y2 - 9 * math.sin(ang):.1f}" stroke="{color}" stroke-width="1.6"/>'
           + head(x2, y2, ang, color, 11))
    for i, ln in enumerate(lines):
        out += text(label_x, label_y + i * 14, ln, 11.5, fill="#2b3a33")
    return out


def box_entity(x, y, w, h, lines):
    out = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#fff" stroke="{FOREST}" stroke-width="2"/>'
    y0 = y + h / 2 - (len(lines) - 1) * 8 + 4
    return out + "".join(text(x + w / 2, y0 + i * 16, ln, 12.5, weight="bold") for i, ln in enumerate(lines))


def make_dfd():
    b = [text(20, 28, "AgriPulse — Data Flow Diagram, Level 0 (context)", 18, "start", "bold", FOREST),
         f'<circle cx="480" cy="300" r="125" fill="{SOFT}" stroke="{EMERALD}" stroke-width="2.5"/>',
         text(480, 238, "0", 14, weight="bold", fill=EMERALD)]
    for i, ln in enumerate(["AgriPulse", "offline livestock", "management", "system"]):
        b.append(text(480, 275 + i * 19, ln, 14, weight="bold"))
    b += [box_entity(20, 240, 190, 120, ["Farmer /", "farm manager"]),
          box_entity(740, 60, 200, 110, ["Extension officer,", "student, veterinarian", "(report recipients)"]),
          box_entity(740, 410, 200, 110, ["Local file system", "(backups, exports,", "photographs)"])]
    b.append(labelled_flow(210, 275, 357, 275, 283, 245, ["farm records,", "settings, requests"]))
    b.append(labelled_flow(357, 335, 210, 335, 283, 355, ["dashboard, alerts,", "calendar, results"]))
    b.append(labelled_flow(572, 213, 740, 125, 596, 150, ["PDF / CSV reports", "and printouts"]))
    b.append(labelled_flow(572, 385, 740, 445, 672, 385, ["backup .zip,", "photographs"]))
    b.append(labelled_flow(740, 490, 548, 408, 612, 482, ["restore file"]))
    b.append(text(20, 560, "Level 0 shows the whole system as one process; Level 1 (next figure) breaks it into eight processes and eight data stores.", 11, "start", fill="#5b6561"))
    (OUT / "dfd_level0.svg").write_text(svg_doc(980, 585, "".join(b), "DFD level 0"), encoding="utf-8")

    # ---- Level 1: Gane-Sarson style, three columns so no flow crosses a box
    procs = [("1.0", "Manage animals & groups"), ("2.0", "Manage breeding & births"), ("3.0", "Manage health & routine tasks"),
             ("4.0", "Manage nutrition, production & growth"), ("5.0", "Record farm finance"), ("6.0", "Generate alerts & calendar"),
             ("7.0", "Produce reports & exports"), ("8.0", "Maintain settings, backup & restore")]
    PX, PW, PH, Y0, DY = 400, 270, 62, 110, 100
    py = {n: Y0 + i * DY for i, (n, _) in enumerate(procs)}
    LX, RX, SW, SH = 30, 830, 250, 54
    stores = {  # id: (label, side, y-centre)
        "D1": ("D1  Animals & groups", "L", py["1.0"]), "D2": ("D2  Breeding, pregnancy & birth records", "L", py["2.0"] + 20),
        "D3": ("D3  Health, vaccination & task records", "L", py["3.0"] + 30), "D8": ("D8  Species parameters & settings", "L", py["8.0"]),
        "D4": ("D4  Feed, feeding & ration records", "R", py["4.0"] - 38), "D5": ("D5  Production & weight records", "R", py["4.0"] + 38),
        "D6": ("D6  Financial transactions", "R", py["5.0"] + 20), "D7": ("D7  Notifications", "R", py["6.0"])}
    b = [text(20, 28, "AgriPulse — Data Flow Diagram, Level 1", 18, "start", "bold", FOREST),
         text(PX + PW / 2, 62, "Processes", 13, weight="bold", fill=EMERALD), text(LX + SW / 2, 62, "Data stores", 13, weight="bold", fill=FOREST),
         text(RX + SW / 2, 62, "Data stores", 13, weight="bold", fill=FOREST)]
    # (process, store, mode) mode: w = writes, r = reads, rw = reads and writes
    links = [("1.0", "D1", "rw"), ("1.0", "D8", "r"), ("2.0", "D2", "rw"), ("2.0", "D1", "r"), ("2.0", "D8", "r"), ("3.0", "D3", "rw"), ("3.0", "D1", "r"),
             ("4.0", "D4", "rw"), ("4.0", "D5", "rw"), ("4.0", "D1", "r"), ("5.0", "D6", "rw"), ("6.0", "D7", "rw"), ("6.0", "D2", "r"), ("6.0", "D3", "r"),
             ("6.0", "D4", "r"), ("8.0", "D8", "rw")]
    for pn, sid, mode in links:
        label, side, sy = stores[sid]
        x1, x2 = (LX + SW, PX) if side == "L" else (PX + PW, RX)
        y1, y2 = (sy, py[pn]) if side == "L" else (py[pn], sy)
        import math
        ang = math.atan2(y2 - y1, x2 - x1)
        # direction: left store -> process is a READ; process -> right store is a WRITE
        to_process, to_store = ("r", "w") if side == "L" else ("w", "r")
        dash = ' stroke-dasharray="5,4"' if mode == "r" else ""
        b.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{FOREST}" stroke-width="1.4"{dash} opacity="0.8"/>')
        reads, writes = mode in ("r", "rw"), mode in ("w", "rw")
        if side == "L":
            if reads: b.append(head(x2, y2, ang))                    # store -> process
            if writes: b.append(head(x1, y1, ang + math.pi))         # process -> store
        else:
            if writes: b.append(head(x2, y2, ang))                   # process -> store
            if reads: b.append(head(x1, y1, ang + math.pi))          # store -> process
    for n, label in procs:
        y = py[n]
        b.append(f'<rect x="{PX}" y="{y - PH / 2}" width="{PW}" height="{PH}" rx="10" fill="{SOFT}" stroke="{EMERALD}" stroke-width="2"/>'
                 f'<rect x="{PX}" y="{y - PH / 2}" width="44" height="{PH}" rx="10" fill="{EMERALD}"/>' + text(PX + 22, y + 5, n, 13, weight="bold", fill="#fff")
                 + wrapped(PX + 44 + (PW - 44) / 2, y, label, 24, 12, "bold"))
    for sid, (label, side, sy) in stores.items():
        x = LX if side == "L" else RX
        b.append(f'<rect x="{x}" y="{sy - SH / 2}" width="{SW}" height="{SH}" fill="#f8faf7" stroke="none"/>'
                 f'<line x1="{x}" y1="{sy - SH / 2}" x2="{x + SW}" y2="{sy - SH / 2}" stroke="{FOREST}" stroke-width="2"/>'
                 f'<line x1="{x}" y1="{sy + SH / 2}" x2="{x + SW}" y2="{sy + SH / 2}" stroke="{FOREST}" stroke-width="2"/>'
                 f'<line x1="{x}" y1="{sy - SH / 2}" x2="{x}" y2="{sy + SH / 2}" stroke="{FOREST}" stroke-width="2"/>'
                 + wrapped(x + SW / 2, sy, label, 30, 11.5))
    b.append(text(PX + PW / 2, py["7.0"] + 3, "", 1))
    b.append(f'<rect x="{PX}" y="{py["7.0"] - PH / 2}" width="{PW}" height="{PH}" rx="10" fill="none" stroke="none"/>')
    b.append(text(RX + SW / 2, py["7.0"] - 6, "Reports read all record stores D1–D6", 11.5, fill="#2b3a33"))
    b.append(text(RX + SW / 2, py["7.0"] + 10, "(not drawn, to keep the diagram readable)", 10.5, fill="#6b7280"))
    b.append(f'<line x1="{PX + PW}" y1="{py["7.0"]}" x2="{RX - 10}" y2="{py["7.0"]}" stroke="{FOREST}" stroke-width="1.4" stroke-dasharray="5,4"/>' + head(PX + PW, py["7.0"], 3.14159))
    b.append(text(PX + PW / 2, py["8.0"] + 60, "", 1))
    b.append(text(20, 960, "Solid arrows: data written (arrowhead at the store) and/or read. Dashed arrows: read-only. External entities are shown in the Level 0 diagram.", 11, "start", fill="#5b6561"))
    (OUT / "dfd_level1.svg").write_text(svg_doc(1110, 985, "".join(b), "DFD level 1"), encoding="utf-8")


# ======================================================================= flowcharts
def make_flow(filename, title, steps):
    """steps: (kind, text, side_text|None); kind: start/end/proc/dec/io."""
    W, CX, GAPY = 620, 230, 34
    y = 70
    body = [text(20, 28, title, 17, "start", "bold", FOREST)]
    prev = None
    for kind, label, side in steps:
        h = 74 if kind == "dec" else 44
        top, bot, cy = y, y + h, y + h / 2
        if prev is not None:
            body.append(line(CX, prev, CX, top))
        if kind in ("start", "end"):
            body.append(f'<rect x="{CX - 90}" y="{top}" width="180" height="{h}" rx="22" fill="{FOREST}"/>' + wrapped(CX, cy, label, 24, 12, "bold", "#fff"))
        elif kind == "dec":
            body.append(f'<polygon points="{CX},{top} {CX + 170},{cy} {CX},{bot} {CX - 170},{cy}" fill="#fffbeb" stroke="#b45309" stroke-width="1.8"/>' + wrapped(CX, cy, label, 25, 11.5))
        elif kind == "io":
            body.append(f'<polygon points="{CX - 130},{bot} {CX - 105},{top} {CX + 135},{top} {CX + 110},{bot}" fill="{SOFT}" stroke="{EMERALD}" stroke-width="1.6"/>' + wrapped(CX, cy, label, 34, 11.5))
        else:
            body.append(f'<rect x="{CX - 130}" y="{top}" width="260" height="{h}" rx="6" fill="{SOFT}" stroke="{EMERALD}" stroke-width="1.6"/>' + wrapped(CX, cy, label, 36, 11.5))
        if side:
            sx = CX + (170 if kind == "dec" else 135)
            body.append(line(sx, cy, sx + 60, cy))
            body.append(text(sx + 30, cy - 6, "No" if kind == "dec" else "", 11, weight="bold", fill="#b45309"))
            body.append(f'<rect x="{sx + 60}" y="{cy - 24}" width="190" height="48" rx="6" fill="#fff5f5" stroke="#b91c1c" stroke-width="1.5"/>' + wrapped(sx + 155, cy, side, 28, 11))
        if kind == "dec":
            body.append(text(CX + 12, bot + 16, "Yes", 11, "start", "bold", EMERALD))
        prev, y = bot, bot + GAPY
    (OUT / filename).write_text(svg_doc(W + 260, y + 10, "".join(body), title), encoding="utf-8")


def make_flows():
    make_flow("flow_register_animal.svg", "Flowchart 1 — Register an animal", [
        ("start", "Start: Animals ▸ Register animal", None), ("io", "Enter tag, species, sex, breed, dates, weights, parents, photo", None),
        ("dec", "Required fields present and valid (dates, numbers, ranges)?", "Show field errors; nothing saved"),
        ("dec", "Tag number unique (case-insensitive)?", "Reject duplicate tag"),
        ("dec", "Breed matches species; parents have right sex, species, age?", "Show parent / breed error"),
        ("dec", "Photo is a real PNG/JPEG/GIF/WebP under 5 MB?", "Reject upload; nothing saved"),
        ("proc", "Save animal in one transaction; assign internal ID AP-000001", None),
        ("proc", "Store photo under a random file name", None),
        ("proc", "Weight entered? create dated weight record · Price entered? create linked 'Animal purchases' expense", None),
        ("proc", "Refresh alerts (missing info, breeding due…)", None), ("end", "Show animal profile", None)])
    make_flow("flow_breeding.svg", "Flowchart 2 — Breeding cycle and automatic calculations", [
        ("start", "Start: record heat / service", None), ("io", "Record service: animal, date, method, sire, cost", None),
        ("dec", "Female, born before service, no confirmed pregnancy?", "Show error; nothing saved"),
        ("proc", "Expected delivery = service date + species gestation days (or manual override)", None),
        ("proc", "Calendar + alerts: pregnancy check due (species days), expected delivery", None),
        ("io", "Record pregnancy examination", None),
        ("dec", "Result = Pregnant?", "Status Open → animal becomes 'due for service' after rest period"),
        ("proc", "Status = Pregnant; countdown alerts (Critical ≤ 3 days, High ≤ window)", None),
        ("io", "Record birth: alive, dead, weights", None),
        ("dec", "Counts plausible for the species?", "Show error; nothing saved"),
        ("proc", "Link to service → status Delivered; recompute indicators (intervals, litter size)", None),
        ("end", "Register offspring from the birth record", None)])
    make_flow("flow_notifications.svg", "Flowchart 3 — Notification generation (no duplicates)", [
        ("start", "Trigger: save a record, open dashboard / alerts", None), ("proc", "Evaluate every enabled rule against live database records", None),
        ("proc", "Build candidate alerts, each with a stable key (rule + record id)", None),
        ("dec", "Key already stored?", None),
        ("proc", "Create new alert (or update text, level and due date in place)", None),
        ("dec", "Stored alert no longer a candidate?", None),
        ("proc", "Auto-resolve it (user-resolved ones are removed so they can recur)", None),
        ("dec", "User marked it resolved while condition persists?", None),
        ("proc", "Keep hidden — no duplicate is created", None), ("end", "Unread badge and Notifications page updated", None)])
    make_flow("flow_backup_restore.svg", "Flowchart 4 — Backup and restore", [
        ("start", "Backup: Settings ▸ Backup & restore", None), ("proc", "Take consistent snapshot using SQLite online backup API", None),
        ("proc", "Zip: database + manifest + photographs; write to backup folder", None), ("proc", "Prune old backups beyond the keep limit", None),
        ("io", "Restore: choose a backup or upload a .zip", None),
        ("dec", "Valid zip, AgriPulse manifest, safe file names, integrity_check OK, schema not newer?", "Reject; current data untouched"),
        ("proc", "Create safety backup of current data", None), ("proc", "Close connections, atomically replace database, restore photos", None),
        ("proc", "Run schema upgrade for older backups", None), ("end", "Restored — data persists after restart", None)])


if __name__ == "__main__":
    n, fks = make_erd()
    make_usecase(); make_dfd(); make_flows()
    print(f"diagrams written to {OUT} (ERD: {n} tables, {fks} foreign keys)")
