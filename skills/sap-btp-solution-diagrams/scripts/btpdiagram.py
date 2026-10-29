"""
btpdiagram - build SAP BTP solution diagrams (optionally with Microsoft Azure components)
and export them as an editable .drawio file (plus a PNG preview for self-checking only).

Styling follows the official SAP BTP solution diagram conventions as used in
github.com/SAP-archive/sap-btp-reference-architectures. Azure icons come from
github.com/dwarfered/azure-architecture-icons-for-drawio (Microsoft Azure architecture icons).

Usage (see examples/ for a complete diagram):

    import sys; sys.path.insert(0, "<skill>/scripts")
    from btpdiagram import Diagram
    d = Diagram(1700, 1200, "Title", "Subtitle")
    d.area(380, 110, 640, 220, "btp", "SAP BTP", "Subaccount")
    d.service(400, 175, 125, 130, "sap:SAP Document Management service", ["SAP Document", "Management service"])
    d.box(60, 450, 330, 100, ["Title", "sub line"], kind="nonsap", icon="azure:Virtual Machine")
    d.edge([(x1, y1), (x2, y2)], "flow")
    d.save("/mnt/user-data/outputs/my-diagram")   # writes my-diagram.drawio, preview PNG to /home/claude/preview/, prints warnings

All coordinates are absolute page pixels. Text never auto-wraps: pass one string per line.
"""
import json, os, html, difflib
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

# ---------------- palette (from the SAP reference .drawio files) ----------------
SAP_BLUE, SAP_FILL = "#0070F2", "#EBF8FF"
GREY, GREY_FILL, NONSAP = "#475E75", "#F5F6F7", "#6D7F91"
TEAL, TEAL_FILL = "#07838F", "#DAFDF5"
PINK, PINK_FILL = "#CC00DC", "#FFF0FA"
GREEN = "#188918"
TXT, SUB = "#1D2D3E", "#556B82"
FONT = "Arial"

AREA_KINDS = {  # stroke, fill, dashed
    "btp": (SAP_BLUE, SAP_FILL, False),      # SAP BTP subaccount / SAP-managed area
    "sap": (SAP_BLUE, "#FFFFFF", False),     # SAP application (S/4HANA etc.) as container
    "nonsap": (GREY, GREY_FILL, False),      # 3rd party / customer / hyperscaler (e.g. Microsoft Azure)
    "teal": (TEAL, TEAL_FILL, False),        # accent: zones, sites, regions
    "pink": (PINK, PINK_FILL, False),        # accent: trust / identity
    "dashed": (GREY, "#FFFFFF", True),       # logical grouping: VNet, optional/DR scope
}
BOX_KINDS = {
    "sap": (SAP_BLUE, "#FFFFFF", False),       # SAP product / service
    "sap_fill": (SAP_BLUE, SAP_FILL, False),   # sub-component inside an SAP box
    "nonsap": (NONSAP, "#FFFFFF", False),      # non-SAP component (incl. Azure services)
    "ops": (NONSAP, "#FFFFFF", True),          # operational function / optional
}
EDGE_KINDS = {  # color, dashed, dash, default start arrow, default end arrow
    "flow": (GREY, False, "", False, True),
    "sync": (GREEN, True, "6 4", True, True),
    "async": (SAP_BLUE, True, "6 4", False, True),
    "heartbeat": (GREY, True, "2 3", False, False),
    "backup": (GREY, True, "6 4", False, True),
    "trust": (PINK, False, "", True, True),
}
LEGEND_TEXT = {
    "flow": "Request flow",
    "sync": "Synchronous replication",
    "async": "Asynchronous replication (DR)",
    "heartbeat": "Heartbeat / quorum",
    "backup": "Backup",
    "trust": "Trust / authentication",
}


def _load(name):
    p = os.path.join(ASSETS, name)
    return json.load(open(p)) if os.path.exists(p) else {}


ICONS = {"sap": _load("sap_btp_icons.json"), "azure": _load("azure_icons.json")}


def resolve_icon(key):
    """'sap:Cloud Connector' or 'azure:Storage Accounts' -> (exact name, data URI). Case-insensitive,
    falls back to substring / fuzzy match and raises with suggestions if nothing fits."""
    lib, _, name = key.partition(":")
    if lib not in ICONS:
        raise KeyError(f"Icon key must start with 'sap:' or 'azure:' - got {key!r}")
    table = ICONS[lib]
    low = {k.lower(): k for k in table}
    if name.lower() in low:
        k = low[name.lower()]
        return k, table[k]["data"]
    subs = [k for k in table if name.lower() in k.lower()]
    if len(subs) == 1:
        return subs[0], table[subs[0]]["data"]
    sugg = subs[:10] or difflib.get_close_matches(name, list(table), n=8, cutoff=0.4)
    raise KeyError(f"No unique {lib} icon for {name!r}. Candidates: {sugg}. Use scripts/find_icon.py to search.")


def text_width(s, size, bold=False):
    """Rough Arial width estimate in px (good enough for overflow warnings)."""
    w = 0
    for ch in s:
        if ch in "il.,:;|'!·": w += 0.28
        elif ch in "mwMW": w += 0.85
        elif ch.isupper(): w += 0.68
        elif ch == " ": w += 0.28
        else: w += 0.55
    return w * size * (1.03 if bold else 1.0)


class Diagram:
    def __init__(self, width, height, title=None, subtitle=None):
        self.W, self.H = width, height
        self.cells = []
        self.used_edges = set()
        self.used_kinds = set()
        self.used_azure = False
        if title:
            self.text(40, 28, [title], size=20, bold=True, color=SAP_BLUE, w=width - 80)
        if subtitle:
            self.text(40, 58, [subtitle], size=12, color=SUB, w=width - 80)

    # ---------------- primitives ----------------
    def area(self, x, y, w, h, kind, title=None, subtitle=None, arc=24):
        stroke, fill, dashed = AREA_KINDS[kind]
        self.used_kinds.add(("area", kind))
        self.cells.append(dict(kind="rect", x=x, y=y, w=w, h=h, stroke=stroke, fill=fill, arc=arc,
                               dashed=dashed, lines=[], role="area"))
        if title:
            self.text(x + 16, y + 12, [title], size=16 if kind in ("btp", "nonsap", "sap") else 14, bold=True, w=w - 32)
        if subtitle:
            self.text(x + 16, y + 34 if kind in ("btp", "nonsap", "sap") else y + 32, [subtitle], size=12, color=SUB, w=w - 32)

    def box(self, x, y, w, h, lines, kind="nonsap", icon=None, icon_size=32, size=12, align=None):
        """Component box. First line bold, rest muted. With icon: icon left, text left-aligned."""
        stroke, fill, dashed = BOX_KINDS[kind]
        self.used_kinds.add(("box", kind))
        self.cells.append(dict(kind="rect", x=x, y=y, w=w, h=h, stroke=stroke, fill=fill, arc=16, dashed=dashed,
                               lines=lines, size=size, role="box",
                               align=align or ("left" if icon else "center"),
                               pad_left=(icon_size + 18) if icon else 0))
        if icon:
            self.icon(icon, x + 12, y + h / 2 - icon_size / 2, icon_size)

    def service(self, x, y, w, h, icon, label_lines, icon_size=40):
        """SAP BTP service tile: white box, icon top-center, label below (like the reference diagrams)."""
        self.box(x, y, w, h, [], kind="sap")
        self.icon(icon, x + w / 2 - icon_size / 2, y + 12, icon_size)
        self.text(x, y + 20 + icon_size, label_lines, size=11, align="center", w=w, lh=13)

    def icon(self, key, x, y, s=40, label=None, label_w=120):
        name, data = resolve_icon(key)
        if key.startswith("azure:"):
            self.used_azure = True
        self.cells.append(dict(kind="icon", key=key, name=name, data=data, x=x, y=y, s=s))
        if label:
            lines = label if isinstance(label, list) else [label]
            self.text(x + s / 2 - label_w / 2, y + s + 4, lines, size=11, align="center", w=label_w, lh=13)

    def text(self, x, y, lines, size=12, bold=False, color=TXT, align="left", w=400, lh=None):
        self.cells.append(dict(kind="text", x=x, y=y, lines=lines, size=size, bold=bold, color=color,
                               align=align, w=w, lh=lh or round(size * 1.3)))

    def edge(self, pts, kind="flow", start=None, end=None, width=1.5):
        color, dashed, dash, s0, e0 = EDGE_KINDS[kind]
        self.used_edges.add(kind)
        self.cells.append(dict(kind="edge", pts=pts, color=color, dashed=dashed, dash=dash,
                               start=s0 if start is None else start, end=e0 if end is None else end,
                               width=width, ekind=kind))

    def pill(self, cx, cy, label, w=None):
        w = w or (text_width(label, 10, True) + 18)
        self.cells.append(dict(kind="pill", x=cx - w / 2, y=cy - 9, w=w, h=18, label=label))

    def num(self, cx, cy, n):
        self.cells.append(dict(kind="num", cx=cx, cy=cy, n=n))

    # ---------------- layout helpers ----------------
    def shift(self, dx=0, dy=0):
        """Context manager: everything added inside the block is moved by (dx, dy). Handy to insert a new
        row into an existing layout:  with d.shift(0, 230): <unchanged code of the lower part>"""
        diagram = self

        class _Shift:
            def __enter__(self):
                self.start = len(diagram.cells)

            def __exit__(self, *exc):
                for c in diagram.cells[self.start:]:
                    for kx, ky in (("x", "y"), ("cx", "cy")):
                        if kx in c:
                            c[kx] += dx
                            c[ky] += dy
                    if "pts" in c:
                        c["pts"] = [(x + dx, y + dy) for x, y in c["pts"]]
        return _Shift()

    # ---------------- composite helpers ----------------
    def flow_panel(self, x, y, w, h, steps, title="Flow"):
        """steps: items are either a list of pre-wrapped lines (auto-numbered 1, 2, ...),
        a tuple (label, lines) for a custom marker such as "A", or a string "# Section" for a sub-heading."""
        self.cells.append(dict(kind="rect", x=x, y=y, w=w, h=h, stroke=GREY_FILL, fill=GREY_FILL, arc=0,
                               dashed=False, lines=[], role="area"))
        self.text(x + 20, y + 14, [title], size=16, bold=True)
        yy, n = y + 50, 0
        for s in steps:
            if isinstance(s, str):
                self.text(x + 20, yy, [s.lstrip("# ")], size=13, bold=True, color=SUB)
                yy += 26
                continue
            if isinstance(s, tuple):
                label, s = s
            else:
                n += 1
                label = n
            self.num(x + 32, yy + 7, label)
            self.text(x + 54, yy, s, size=12, w=w - 70, lh=15)
            yy += len(s) * 15 + 18
        if yy > y + h:
            print(f"WARNING flow panel content ({yy - y:.0f}px) exceeds panel height {h}px")
        return yy - y

    def legend(self, x, y, w=440, extra_boxes=None, labels=None):
        """Auto legend from the edge kinds and box/area kinds actually used.
        labels: optional {edge_kind: text} to override legend wording, e.g. {"async": "Content deployment"}."""
        rows = [k for k in EDGE_KINDS if k in self.used_edges]
        swatches = []
        if ("area", "btp") in self.used_kinds or ("box", "sap") in self.used_kinds:
            swatches.append(("sap", "SAP product / service"))
        if ("area", "nonsap") in self.used_kinds or ("box", "nonsap") in self.used_kinds:
            swatches.append(("nonsap_area", "Non-SAP / hyperscaler"))
        if ("area", "teal") in self.used_kinds:
            swatches.append(("teal", "Zone / site (active)"))
        if ("box", "ops") in self.used_kinds or ("area", "dashed") in self.used_kinds:
            swatches.append(("ops", "Operational / optional scope"))
        swatches += extra_boxes or []
        h = 40 + len(rows) * 24 + ((len(swatches) + 1) // 2) * 30 + 10
        self.cells.append(dict(kind="rect", x=x, y=y, w=w, h=h, stroke="#EAECEE", fill="#FFFFFF", arc=0,
                               dashed=False, lines=[], role="area"))
        self.text(x + 14, y + 10, ["Legend"], size=12, bold=True)
        ly = y + 38
        for k in rows:
            self.edge([(x + 16, ly), (x + 66, ly)], k)
            self.text(x + 76, ly - 8, [(labels or {}).get(k, LEGEND_TEXT[k])], size=11)
            ly += 24
        for i, (sk, label) in enumerate(swatches):
            sx = x + 16 + (i % 2) * (w / 2)
            sy = ly - 6 + (i // 2) * 30
            stroke, fill, dashed = {"sap": (SAP_BLUE, SAP_FILL, False), "nonsap_area": (GREY, GREY_FILL, False),
                                    "teal": (TEAL, TEAL_FILL, False), "ops": (NONSAP, "#FFFFFF", True),
                                    "pink": (PINK, PINK_FILL, False)}[sk]
            self.cells.append(dict(kind="rect", x=sx, y=sy, w=40, h=20, stroke=stroke, fill=fill, arc=8,
                                   dashed=dashed, lines=[], role="swatch"))
            self.text(sx + 48, sy + 3, [label], size=11, w=w / 2 - 60)
        return h

    def footer(self, level="L2", note=None, y=None):
        y = y or self.H - 54
        self.text(40, y, [f"Diagram level: {level}"], size=12, bold=True, color=GREY)
        attribution = ("Based on the SAP BTP solution diagram guidelines and icons"
                       + ("; Microsoft Azure architecture icons used per Microsoft terms." if self.used_azure else "."))
        self.text(40, y + 18, [attribution + (" " + note if note else "")], size=12, color=GREY, w=self.W - 80)

    # ---------------- checks ----------------
    def check(self):
        warn = []
        rects = [c for c in self.cells if c["kind"] == "rect"]
        boxes = [c for c in rects if c["role"] == "box"]
        for c in rects:
            if c["x"] < 0 or c["y"] < 0 or c["x"] + c["w"] > self.W or c["y"] + c["h"] > self.H:
                warn.append(f"rect at ({c['x']},{c['y']}) is outside the page {self.W}x{self.H}")
            for j, l in enumerate(c.get("lines") or []):
                size = c["size"] if j == 0 else c["size"] - 1
                avail = c["w"] - 16 - c.get("pad_left", 0)
                tw = text_width(l, size, j == 0)
                if tw > avail:
                    warn.append(f"text '{l}' (~{tw:.0f}px) overflows box {c['lines'][0]!r} (room {avail:.0f}px)")
            if c.get("lines"):
                need = len(c["lines"]) * c["size"] * 1.3 + 8
                if need > c["h"]:
                    warn.append(f"box {c['lines'][0]!r}: {len(c['lines'])} lines need ~{need:.0f}px, box is {c['h']}px high")
        for a, b in [(a, b) for i, a in enumerate(boxes) for b in boxes[i + 1:]]:
            if a["x"] < b["x"] + b["w"] and b["x"] < a["x"] + a["w"] and a["y"] < b["y"] + b["h"] and b["y"] < a["y"] + a["h"]:
                warn.append(f"boxes overlap: {a['lines'][:1] or a['x']} and {b['lines'][:1] or b['x']}")
        # edges through boxes that are neither start nor end
        for e in [c for c in self.cells if c["kind"] == "edge"]:
            p = e["pts"]
            for (x1, y1), (x2, y2) in zip(p, p[1:]):
                for b in boxes:
                    inside = lambda px, py: b["x"] < px < b["x"] + b["w"] and b["y"] < py < b["y"] + b["h"]
                    if inside(*p[0]) or inside(*p[-1]):
                        continue
                    for t in [i / 20 for i in range(1, 20)]:
                        if inside(x1 + (x2 - x1) * t, y1 + (y2 - y1) * t):
                            warn.append(f"edge {p[0]}->{p[-1]} crosses box {b['lines'][:1] or (b['x'], b['y'])}")
                            break
        return sorted(set(warn))

    # ---------------- emitters ----------------
    def to_drawio(self, name="Diagram"):
        out, i = [], 1
        for c in self.cells:
            i += 1
            k = c["kind"]
            if k == "rect":
                val = ""
                if c.get("lines"):
                    parts = []
                    for j, l in enumerate(c["lines"]):
                        l = escape(l)
                        parts.append(f"<b>{l}</b>" if j == 0 else f'<font color="{SUB}" style="font-size:{c["size"]-1}px">{l}</font>')
                    val = "<br>".join(parts)
                st = (f'rounded={1 if c["arc"] else 0};whiteSpace=wrap;html=1;strokeColor={c["stroke"]};fillColor={c["fill"]};'
                      f'arcSize={c["arc"]};absoluteArcSize=1;strokeWidth=1.5;fontFamily={FONT};fontSize={c.get("size", 12)};fontColor={TXT};'
                      f'align={c.get("align", "center")};verticalAlign=middle;spacingLeft={c.get("pad_left", 0)};'
                      + ("dashed=1;dashPattern=6 4;" if c["dashed"] else "")
                      + ("container=0;" if c["role"] == "area" else ""))
                out.append(f'<mxCell id="c{i}" value="{html.escape(val)}" style="{st}" vertex="1" parent="1"><mxGeometry x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" as="geometry"/></mxCell>')
            elif k == "text":
                inner = "<br>".join(escape(l) for l in c["lines"])
                if c["bold"]:
                    inner = f"<b>{inner}</b>"
                h = len(c["lines"]) * c["lh"] + 4
                st = (f'text;html=1;strokeColor=none;fillColor=none;align={c["align"]};verticalAlign=top;whiteSpace=wrap;'
                      f'fontFamily={FONT};fontSize={c["size"]};fontColor={c["color"]};spacing=0;')
                out.append(f'<mxCell id="c{i}" value="{html.escape(inner)}" style="{st}" vertex="1" parent="1"><mxGeometry x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{h}" as="geometry"/></mxCell>')
            elif k == "icon":
                st = f'shape=image;verticalLabelPosition=bottom;verticalAlign=top;imageAspect=0;aspect=fixed;image={c["data"]};'
                out.append(f'<mxCell id="c{i}" value="" tooltip="{html.escape(c["name"])}" style="{st}" vertex="1" parent="1"><mxGeometry x="{c["x"]}" y="{c["y"]}" width="{c["s"]}" height="{c["s"]}" as="geometry"/></mxCell>')
            elif k == "edge":
                p = c["pts"]
                st = (f'html=1;rounded=0;strokeColor={c["color"]};strokeWidth={c["width"]};'
                      f'endArrow={"blockThin" if c["end"] else "none"};endFill=1;endSize=4;'
                      f'startArrow={"blockThin" if c["start"] else "none"};startFill=1;startSize=4;'
                      + (f'dashed=1;dashPattern={c["dash"]};' if c["dashed"] else ""))
                wp = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in p[1:-1])
                wp = f'<Array as="points">{wp}</Array>' if wp else ""
                out.append(f'<mxCell id="c{i}" style="{st}" edge="1" parent="1"><mxGeometry relative="1" as="geometry">'
                           f'<mxPoint x="{p[0][0]}" y="{p[0][1]}" as="sourcePoint"/><mxPoint x="{p[-1][0]}" y="{p[-1][1]}" as="targetPoint"/>{wp}</mxGeometry></mxCell>')
            elif k == "pill":
                val = f'<font color="{GREY}" style="font-size:10px"><b>{escape(c["label"])}</b></font>'
                st = f"rounded=1;whiteSpace=wrap;html=1;arcSize=50;strokeColor={GREY};fillColor={GREY_FILL};strokeWidth=1.5;fontFamily={FONT};"
                out.append(f'<mxCell id="c{i}" value="{html.escape(val)}" style="{st}" vertex="1" parent="1"><mxGeometry x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" as="geometry"/></mxCell>')
            elif k == "num":
                val = f'<b><font color="#FFFFFF">{c["n"]}</font></b>'
                st = (f"ellipse;whiteSpace=wrap;html=1;aspect=fixed;gradientColor=#0057D2;strokeColor=none;gradientDirection=east;"
                      f"fillColor=#2395FF;fontFamily={FONT};fontSize=12;")
                out.append(f'<mxCell id="c{i}" value="{html.escape(val)}" style="{st}" vertex="1" parent="1"><mxGeometry x="{c["cx"]-11}" y="{c["cy"]-11}" width="22" height="22" as="geometry"/></mxCell>')
        body = "\n".join(out)
        return (f'<mxfile host="Electron" type="device"><diagram name="{html.escape(name)}" id="d1">'
                f'<mxGraphModel dx="{self.W}" dy="{self.H}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.W}" pageHeight="{self.H}" math="0" shadow="0">'
                f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n{body}\n</root></mxGraphModel></diagram></mxfile>')

    def to_svg(self):
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.W}" height="{self.H}" viewBox="0 0 {self.W} {self.H}" font-family="Arial, Helvetica, sans-serif">',
             '<defs><linearGradient id="ng" x1="0" x2="1"><stop offset="0" stop-color="#2395FF"/><stop offset="1" stop-color="#0057D2"/></linearGradient>']
        for col in {v[0] for v in EDGE_KINDS.values()}:
            o.append(f'<marker id="a{col[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 1L10 5L0 9z" fill="{col}"/></marker>')
        o.append('</defs><rect width="100%" height="100%" fill="#FFFFFF"/>')
        for c in self.cells:
            k = c["kind"]
            if k == "rect":
                da = ' stroke-dasharray="6 4"' if c["dashed"] else ""
                o.append(f'<rect x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" rx="{c["arc"]/2}" fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="1.5"{da}/>')
                if c.get("lines"):
                    n, lh = len(c["lines"]), c["size"] * 1.3
                    y0 = c["y"] + c["h"] / 2 - (n - 1) * lh / 2
                    if c["align"] == "left":
                        tx, anchor = c["x"] + 8 + c.get("pad_left", 0), "start"
                    else:
                        tx, anchor = c["x"] + c["w"] / 2, "middle"
                    for j, l in enumerate(c["lines"]):
                        if j == 0:
                            o.append(f'<text x="{tx}" y="{y0+j*lh}" text-anchor="{anchor}" dominant-baseline="central" font-size="{c["size"]}" font-weight="bold" fill="{TXT}">{escape(l)}</text>')
                        else:
                            o.append(f'<text x="{tx}" y="{y0+j*lh}" text-anchor="{anchor}" dominant-baseline="central" font-size="{c["size"]-1}" fill="{SUB}">{escape(l)}</text>')
            elif k == "text":
                anchor = {"left": "start", "center": "middle"}[c["align"]]
                x = c["x"] if c["align"] == "left" else c["x"] + c["w"] / 2
                for j, l in enumerate(c["lines"]):
                    fw = ' font-weight="bold"' if c["bold"] else ""
                    o.append(f'<text x="{x}" y="{c["y"]+c["size"]*0.9+j*c["lh"]}" text-anchor="{anchor}" font-size="{c["size"]}" fill="{c["color"]}"{fw}>{escape(l)}</text>')
            elif k == "icon":
                b64 = c["data"].split(",", 1)[1]
                o.append(f'<image x="{c["x"]}" y="{c["y"]}" width="{c["s"]}" height="{c["s"]}" href="data:image/svg+xml;base64,{b64}" xlink:href="data:image/svg+xml;base64,{b64}"/>')
            elif k == "edge":
                d = "M" + " L".join(f"{x} {y}" for x, y in c["pts"])
                da = f' stroke-dasharray="{c["dash"]}"' if c["dashed"] else ""
                m = f"url(#a{c['color'][1:]})"
                me = f' marker-end="{m}"' if c["end"] else ""
                ms = f' marker-start="{m}"' if c["start"] else ""
                o.append(f'<path d="{d}" fill="none" stroke="{c["color"]}" stroke-width="{c["width"]}"{da}{me}{ms}/>')
            elif k == "pill":
                o.append(f'<rect x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" rx="9" fill="{GREY_FILL}" stroke="{GREY}" stroke-width="1.5"/>')
                o.append(f'<text x="{c["x"]+c["w"]/2}" y="{c["y"]+c["h"]/2}" text-anchor="middle" dominant-baseline="central" font-size="10" font-weight="bold" fill="{GREY}">{escape(c["label"])}</text>')
            elif k == "num":
                o.append(f'<circle cx="{c["cx"]}" cy="{c["cy"]}" r="11" fill="url(#ng)"/>')
                o.append(f'<text x="{c["cx"]}" y="{c["cy"]}" text-anchor="middle" dominant-baseline="central" font-size="12" font-weight="bold" fill="#FFFFFF">{c["n"]}</text>')
        o.append("</svg>")
        return "\n".join(o)

    def save(self, base, name="Diagram", preview_dir="/home/claude/preview"):
        """Write the deliverable <base>.drawio. A PNG preview (for visual self-checking only, not for the
        user) is rendered to <preview_dir>/<basename>.png if cairosvg is installed. Returns layout warnings."""
        os.makedirs(os.path.dirname(os.path.abspath(base)), exist_ok=True)
        base = base[:-7] if base.endswith(".drawio") else base
        open(base + ".drawio", "w").write(self.to_drawio(name))
        png = None
        if preview_dir:
            os.makedirs(preview_dir, exist_ok=True)
            stem = os.path.join(preview_dir, os.path.basename(base))
            open(stem + ".svg", "w").write(self.to_svg())
            try:
                import cairosvg
                cairosvg.svg2png(url=stem + ".svg", write_to=stem + ".png")
                png = stem + ".png"
            except ImportError:
                print("cairosvg not installed (pip install cairosvg --break-system-packages) - PNG preview skipped")
        warns = self.check()
        for w in warns:
            print("WARNING", w)
        print(f"saved {base}.drawio - {len(warns)} layout warnings" + (f" - preview for checking: {png}" if png else ""))
        return warns
