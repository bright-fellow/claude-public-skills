"""
bigpicture - build "SAP BTP Big Picture" capability posters (SAP BTP Capabilities Reference Architecture
for Best Transformation) as editable .drawio files, plus a PNG preview for self-checking.

Builds on the base skill `sap-btp-solution-diagrams`: icons (assets/sap_btp_icons.json, azure_icons.json),
resolve_icon() and text_width() are imported from its scripts/btpdiagram.py. Everything poster-specific
(colour bands, lettered capability blocks, chips, value statements, benefit pills, personas, Joule
markers, key-sites cards, status overlay) lives here.

    import sys; sys.path.insert(0, "<this skill>/scripts")
    from bigpicture import BigPicture
    bp = BigPicture(4400, 1480, "SAP BTP Capabilities Reference Architecture for Best Transformation")
    bp.band(640, 80, 3160, 500, "apps", "SAP Applications and Processes")
    bp.block(890, 620, 690, 370, "B", "Best Appl. Development & Automation", "(Side-by-side Clean Core extensibility)")
    bp.group(910, 700, 480, 260, "SAP Build", dashed_inner=True)
    bp.chip(930, 760, 140, 34, ["Pro Code", "Development"], status="live")
    bp.save("/mnt/user-data/outputs/acme-big-picture")

Coordinates are absolute page pixels. Text never wraps: pass one string per line.
"""
import os, sys, html, glob, json
from xml.sax.saxutils import escape


# ---------------- locate the base skill (sap-btp-solution-diagrams) ----------------
def _find_base():
    here = os.path.dirname(os.path.abspath(__file__))
    cands = [os.environ.get("BTP_DIAGRAM_SKILL", ""),
             os.path.join(here, "..", "..", "sap-btp-solution-diagrams"),
             "/mnt/skills/plugins/sap-btp-solution-diagrams",
             "/mnt/skills/user/sap-btp-solution-diagrams",
             os.path.expanduser("~/.claude/skills/sap-btp-solution-diagrams")]
    cands += glob.glob("/mnt/skills/*/sap-btp-solution-diagrams") + glob.glob("/mnt/skills/*/*/sap-btp-solution-diagrams")
    for c in cands:
        if c and os.path.exists(os.path.join(c, "scripts", "btpdiagram.py")):
            return os.path.abspath(c)
    raise ImportError("Base skill 'sap-btp-solution-diagrams' not found. Install it next to this skill or set "
                      "BTP_DIAGRAM_SKILL=<path to that skill folder>.")


BASE = _find_base()
sys.path.insert(0, os.path.join(BASE, "scripts"))
import btpdiagram  # noqa: E402  (base skill: 'sap:' and 'azure:' icon libraries, text width estimate)
from btpdiagram import text_width  # noqa: E402

# ---------------- official SAP BTP solution-diagram icon set (kept fresh by update_icons.py) ----------------
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import update_icons  # noqa: E402

ICON_DIR, ICON_MANIFEST = update_icons.active_set()
_official = json.load(open(os.path.join(ICON_DIR, update_icons.ICONS_FILE)))
OFFICIAL = {"btp": {k: v for k, v in _official.items() if v["category"] != "Generic"},
            "generic": {k: v for k, v in _official.items() if v["category"] == "Generic"}}


def resolve_icon(key):
    """'btp:SAP Build Code' / 'generic:User (SAP)' -> official SAP BTP solution-diagram icon set (preferred);
    'sap:...' / 'azure:...' -> the base skill's libraries. Exact, then unique substring, else KeyError with hints."""
    lib, _, name = key.partition(":")
    if lib not in OFFICIAL:
        return btpdiagram.resolve_icon(key)
    table = OFFICIAL[lib]
    low = {k.lower(): k for k in table}
    if name.lower() in low:
        k = low[name.lower()]
        return k, table[k]["data"]
    subs = [k for k in table if name.lower() in k.lower()]
    if len(subs) == 1:
        return subs[0], table[subs[0]]["data"]
    import difflib
    sugg = subs[:10] or difflib.get_close_matches(name, list(table), n=8, cutoff=0.4)
    raise KeyError(f"No unique {lib} icon for {name!r}. Candidates: {sugg}. Search with scripts/find_icon.py.")

# ---------------- palette (sampled from the SAP Big Picture poster) ----------------
PAGE_BG = "#CFECFF"        # light sky page background
APPS_BAND = "#016DD0"      # "SAP Applications and Processes" band (deep blue)
BTP_BAND = "#26A9FF"       # "SAP BTP" band (bright blue)
ECO_BAND = "#B8E3FF"       # "Sources & Open Ecosystem" band (pale blue)
KEYS_BAND = "#75BCFE"      # "Key Sites, Methodologies and Guidelines" panel
GROUP = "#B8E3FF"          # product group panel inside a block
GROUP_SOFT = "#E3F4FF"     # nested soft panel (e.g. BTP Cockpit, SAP applications card)
THIRD = "#C9BCFF"          # 3rd-party panel (lavender)
SAP_BLUE = "#0070F2"       # chip borders, Joule marker
TITLE_BLUE = "#0040B0"     # chip / value-statement titles
INK = "#1D2D3E"            # main text
SUB = "#556B82"            # secondary text
MAGENTA = "#C00FBE"        # benefit pills, badges
LINK = "#E26BE6"           # persona / benefit connectors (light magenta)
FUSION = "#5AB8FF"         # fusion-team line, agent loop
FLOW = "#2C3E50"           # deploy / run arrows
WHITE = "#FFFFFF"
FONT = "Arial"

BANDS = {  # fill, title colour, title size
    "apps": (APPS_BAND, WHITE, 26),
    "btp": (BTP_BAND, WHITE, 30),
    "ecosystem": (ECO_BAND, "#0A6ED1", 22),
    "keysites": (KEYS_BAND, WHITE, 19),
}

# ---------------- themes ----------------
# Every colour the poster uses belongs to a role. A theme maps roles to new colours; it is applied as a final
# recolouring pass over the .drawio and preview, so layouts never change with the theme. Themes live in
# assets/themes/<name>.json as {"role": "#RRGGBB"}; "sap" (empty) is the original poster palette.
ROLES = {
    "page": PAGE_BG, "apps_band": APPS_BAND, "btp_band": BTP_BAND, "eco_band": ECO_BAND, "keys_band": KEYS_BAND,
    "panel_soft": GROUP_SOFT, "panel_foundation": "#D6EEFF", "panel_light": "#F2F9FF", "third_party": THIRD,
    "border": SAP_BLUE, "chip_title": TITLE_BLUE, "accent": MAGENTA, "accent_light": "#E040E8",
    "accent_dark": "#A100C2", "accent_text": "#7A00B8", "connector": LINK, "fusion": FUSION, "flow": FLOW,
    "heading": "#0A6ED1", "joule_dark": "#0040B0", "hero_frame": "#A8DCFF", "halo": "#D9ECFF",
    "dashed_frame": "#9FD3FF", "tag_text": "#0A3E7A",
}
THEME_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "themes")


def load_theme(theme):
    """theme: None/'sap', a theme name from assets/themes, a path to a JSON file, or a {role: colour} dict.
    Returns {old_hex_upper: new_hex}."""
    if not theme or theme == "sap":
        return {}
    if isinstance(theme, str):
        path = theme if theme.endswith(".json") else os.path.join(THEME_DIR, theme + ".json")
        theme = json.load(open(path))
    unknown = set(theme) - set(ROLES) - {"_comment", "name", "persona_icon"}
    if unknown:
        raise ValueError(f"unknown theme roles {sorted(unknown)}; valid: {sorted(ROLES)}")
    return {ROLES[r].upper(): c for r, c in theme.items() if r in ROLES}


# status overlay for customer-specific Big Pictures: stroke, fill, text colour, dashed, legend text
STATUS = {
    "live": ("#188918", "#EBF5CB", INK, False, "In use / live"),
    "planned": ("#0064D9", "#FFFFFF", INK, True, "Planned / in implementation"),
    "evaluate": ("#E76500", "#FFF3B8", INK, True, "Under evaluation"),
    "out": ("#A9B4BE", "#F5F6F7", "#8396A8", False, "Not in scope"),
}

EDGES = {  # colour, width, dash, start arrow, end arrow
    "link": (LINK, 1.5, "", False, True),       # persona / benefit to block
    "both": (LINK, 1.5, "", True, True),        # two-way relation (A <-> SAP apps)
    "fusion": (FUSION, 2, "", False, False),    # fusion team line
    "agent": (FUSION, 1.5, "", False, True),    # agent loop around SAP applications
    "flow": (FLOW, 1.5, "", False, True),       # deploy / run / process data
    "flow2": (FLOW, 1.5, "", True, True),       # two-way technical relation
    "dotted": (LINK, 1.5, "2 3", False, True),  # information / guidance
    "dashed": (SAP_BLUE, 1, "4 3", False, False),
}


def _line(t, size=11, bold=False, color=INK):
    return (t, size, bold, color)


class BigPicture:
    def __init__(self, width, height, title=None, hero="The Big Picture", title_x=640, hero_box=True, status=None,
                 theme=None):
        """status: optional {label: 'live'|'planned'|'evaluate'|'out'} - customer overlay. Keys match the first
        line of a chip or the joined label of a tile (case-insensitive), e.g. {"SAP Build Apps": "live"}."""
        self.W, self.H = width, height
        self.recolor = load_theme(theme)
        self.persona_icon = "generic:User (Highlight)"
        if isinstance(theme, str) and theme != "sap":
            path = theme if theme.endswith(".json") else os.path.join(THEME_DIR, theme + ".json")
            self.persona_icon = json.load(open(path)).get("persona_icon", self.persona_icon)
        elif isinstance(theme, dict):
            self.persona_icon = theme.get("persona_icon", self.persona_icon)
        self.cells = []
        self.statuses = set()
        self.status_of = {k.lower(): v for k, v in (status or {}).items()}
        bad = {v for v in self.status_of.values() if v not in STATUS}
        if bad:
            raise ValueError(f"unknown status {bad}; use one of {list(STATUS)}")
        self.matched = set()
        self.used_current = False
        self.labels = []
        self.used_azure = False
        self.rect(0, 0, width, height, PAGE_BG, PAGE_BG, arc=0, role="page")
        if hero:
            if hero_box:  # the open parallelogram behind the hero title
                self.cells.append(dict(kind="hero", x=100, y=height * 0.30, w=480, h=230))
            self.text(60, height * 0.30 + 70, [hero], size=64, bold=True, color="#0A6ED1", w=560)
        if title:
            self.text(title_x, 26, [title], size=28, color="#0A6ED1", w=width - title_x - 40)

    # ---------------- primitives ----------------
    def rect(self, x, y, w, h, stroke, fill, arc=16, dashed=False, dash="6 4", sw=1.5, lines=None,
             align="center", valign="middle", pad=8, role="box", shape="rect"):
        self.cells.append(dict(kind="rect", x=x, y=y, w=w, h=h, stroke=stroke, fill=fill, arc=arc, dashed=dashed,
                               dash=dash, sw=sw, lines=lines or [], align=align, valign=valign, pad=pad,
                               role=role, shape=shape))

    def text(self, x, y, lines, size=12, bold=False, color=INK, align="left", w=400, lh=None):
        self.cells.append(dict(kind="text", x=x, y=y, lines=lines, size=size, bold=bold, color=color,
                               align=align, w=w, lh=lh or round(size * 1.25)))

    def icon(self, key, x, y, s=32, halo=True):
        """Official icon from the base skill's libraries, on a white halo circle like the poster."""
        name, data = resolve_icon(key)
        if key.startswith("azure:"):
            self.used_azure = True
        if halo:
            self.cells.append(dict(kind="ellipse", x=x - 5, y=y - 5, w=s + 10, h=s + 10, stroke="#D9ECFF", fill=WHITE, sw=1))
        self.cells.append(dict(kind="icon", name=name, data=data, x=x, y=y, s=s))

    def edge(self, pts, kind="link", label=None):
        color, width, dash, s0, e0 = EDGES[kind]
        self.cells.append(dict(kind="edge", pts=pts, color=color, width=width, dash=dash, start=s0, end=e0))

    def _status(self, label, status, alt=None):
        """Look up a status by label (and an alternative key, e.g. a chip's first line)."""
        self.labels.append(label)   # every label that can carry a status (see --list-labels)
        if status:
            return status
        for key in (label.lower(), (alt or "").lower()):
            if key and key in self.status_of:
                self.matched.add(key)
                return self.status_of[key]
        return None

    # ---------------- poster elements ----------------
    def band(self, x, y, w, h, kind, title, title_dy=14):
        """Full-width layer: 'apps' | 'btp' | 'ecosystem' | 'keysites'. Draw top to bottom; later bands overlap
        the rounded bottom of the previous one, as on the poster."""
        fill, tc, ts = BANDS[kind]
        self.rect(x, y, w, h, fill, fill, arc=48, role="band")
        self.text(x + 28, y + title_dy, [title], size=ts, bold=True, color=tc, w=w - 56)

    def block(self, x, y, w, h, letter, title, subtitle=None, joule=True, joule_dx=None):
        """Capability block (white card) with a magenta lettered badge and optional Joule diamond on top."""
        self.rect(x, y, w, h, SAP_BLUE, WHITE, arc=36, sw=2, role="block")
        self.text(x + 28, y + 24, [title], size=20, bold=True, w=w - 56)
        if subtitle:
            self.text(x + 28, y + 50, [subtitle], size=13, w=w - 56)
        self.badge(x + 4, y + 4, letter)
        if joule:
            self.joule(x + (joule_dx if joule_dx is not None else w / 2), y)

    def group(self, x, y, w, h, title=None, subtitle=None, icon=None, fill=GROUP, dashed=False, title_size=13,
              stroke=None, title_color=INK, status=None):
        """Product group panel (e.g. 'SAP Build', 'AI Foundation'). dashed=True draws a dashed blue frame.
        A status (explicit or from the status map, keyed by title) recolours the frame and adds a status dot."""
        status = self._status(title, status) if title else status
        sw = 1.5
        if status:
            stroke, _, _, dashed, _ = STATUS[status]
            sw = 2.5
            self.statuses.add(status)
        self.rect(x, y, w, h, stroke or (SAP_BLUE if dashed else fill), fill, arc=24, dashed=dashed, sw=sw,
                  role="group")
        if status:
            self.status_tag(x + w - 8, y - 9, status)
        tx = x + 14
        if icon:
            self.icon(icon, x + 14, y + 10, 26)
            tx = x + 52
        if title:
            self.text(tx, y + 12, [title], size=title_size, bold=True, color=title_color, w=w - (tx - x) - 10)
        if subtitle:
            self.text(tx, y + 12 + title_size * 1.3, [subtitle], size=11, color="#0A6ED1", w=w - (tx - x) - 10)

    def chip(self, x, y, w, h, lines, status=None, title=False, size=11, align="center", fill=WHITE):
        """White rounded capability chip with blue border. title=True: first line bold dark blue, rest plain.
        status: None | 'live' | 'planned' | 'evaluate' | 'out' (customer overlay; adds to the status legend)."""
        stroke, color, dashed = SAP_BLUE, INK, False
        lines = [lines] if isinstance(lines, str) else lines
        joined = " ".join(lines)
        status = self._status(lines[0], status, joined) if title else self._status(joined, status, lines[0])
        if status:
            stroke, fill, color, dashed, _ = STATUS[status]
            self.statuses.add(status)
        lines = [lines] if isinstance(lines, str) else lines
        rich = []
        for j, l in enumerate(lines):
            if title and j < int(title):
                rich.append(_line(l, size, True, TITLE_BLUE if status != "out" else color))
            else:
                rich.append(_line(l, size if not title else size - 0.5, False, color))
        self.rect(x, y, w, h, stroke, fill, arc=14, dashed=dashed, dash="5 3", sw=1.8, lines=rich, align=align,
                  role="chip")

    def tile(self, cx, y, lines, icon=None, status=None, w=150):
        """Product tile: official icon (if the base library has one) above a bold label. Without an icon the
        label alone is used - never draw imitation logos."""
        status = self._status(" ".join(lines), status)
        if icon:
            self.icon(icon, cx - 16, y, 32)
        ty = y + 44   # same label baseline with or without icon, so rows stay aligned
        color = STATUS[status][2] if status else INK
        self.text(cx - w / 2, ty, lines, size=12, bold=True, color=color, align="center", w=w, lh=15)
        if status:
            self.status_dot(cx + w / 2 - 14, ty + 6, status)

    def chips(self, x, y, w, items, cols=1, h=24, gap=8, gapy=6, title=False, size=11):
        """Grid of chips filling width w. items: str or list of lines (or (lines, status) tuples).
        Returns the y below the last row."""
        cw = (w - (cols - 1) * gap) / cols
        for i, it in enumerate(items):
            st = None
            if isinstance(it, tuple):
                it, st = it
            r, c = divmod(i, cols)
            self.chip(x + c * (cw + gap), y + r * (h + gapy), cw, h, it, status=st, title=title, size=size)
        rows = (len(items) + cols - 1) // cols
        return y + rows * (h + gapy) - gapy

    STATUS_TAG = {"live": "Live", "planned": "Planned", "evaluate": "Evaluate", "out": "Not in scope"}

    def status_tag(self, right, y, status):
        """Small status label sitting on a group's top edge, right-aligned at x=right."""
        stroke, fill, color, dashed, _ = STATUS[status]
        self.statuses.add(status)
        t = self.STATUS_TAG[status]
        w = text_width(t, 10, True) + 26
        self.rect(right - w, y, w, 20, stroke, stroke if status != "planned" else fill, arc=20, sw=1.5,
                  lines=[_line(t, 10, True, WHITE if status != "planned" else stroke)], role="label")

    def status_dot(self, cx, cy, status):
        stroke, fill, *_ = STATUS[status]
        self.statuses.add(status)
        self.cells.append(dict(kind="ellipse", x=cx - 6, y=cy - 6, w=12, h=12, stroke=stroke, fill=fill, sw=2))

    def current(self, x, y, w, h, title, lines=(), icon="generic:Third Party (Non-SAP)", label="Current solution"):
        """Non-SAP solution the organisation uses today for this capability (e.g. 'Microsoft Power Platform').
        Dark-grey frame, generic Non-SAP icon, small header label. Shown in the block's value column."""
        self.used_current = True
        self.rect(x, y, w, h, "#475E75", WHITE, arc=12, sw=2, role="current")
        self.rect(x + 10, y - 10, text_width(label, 10, True) + 26, 20, "#475E75", "#475E75", arc=20, sw=1,
                  lines=[_line(label, 10, True, WHITE)], role="label")
        tx = x + 12
        if icon:
            self.icon(icon, x + 10, y + 16, 24, halo=False)
            tx = x + 42
        titles = title if isinstance(title, list) else [title]
        self.text(tx, y + 16, titles, size=12, bold=True, w=w - (tx - x) - 8, lh=15)
        if lines:
            self.text(tx, y + 20 + 15 * len(titles), list(lines), size=11, color="#3A4A5C", w=w - (tx - x) - 8, lh=14)

    def value(self, x, y, w, h, lines):
        """Value statement (white box, bold dark-blue text) beside a block - 'Scale AI responsibly'."""
        lines = [lines] if isinstance(lines, str) else lines
        self.rect(x, y, w, h, SAP_BLUE, WHITE, arc=12, sw=2,
                  lines=[_line(l, 11, True, TITLE_BLUE) for l in lines], align="left", pad=12, role="value")

    def benefit(self, cx, cy, lines, w=None):
        """Magenta pill stating the benefit of a connection ('Add custom AI to apps and processes')."""
        lines = [lines] if isinstance(lines, str) else lines
        w = w or max(text_width(l, 12, True) for l in lines) + 36
        h = 14 * len(lines) + 14
        self.rect(cx - w / 2, cy - h / 2, w, h, MAGENTA, MAGENTA, arc=h, sw=1,
                  lines=[_line(l, 12, True, WHITE) for l in lines], role="pill")

    def tag(self, cx, cy, text, w=None):
        """White label on a technical arrow ('Deploy and Run Applications')."""
        w = w or text_width(text, 11) + 28
        self.rect(cx - w / 2, cy - 11, w, 22, WHITE, WHITE, arc=4, sw=1, lines=[_line(text, 11, False, "#0A3E7A")],
                  role="pill")

    def badge(self, x, y, letter):
        self.cells.append(dict(kind="badge", cx=x, cy=y, n=letter))

    def joule(self, cx, cy):
        """Joule diamond marker (Joule embedded in this capability area)."""
        self.cells.append(dict(kind="rhombus", x=cx - 12, y=cy - 13, w=24, h=26))

    def persona(self, cx, cy, name, pill=None, name_color=WHITE, pill_w=None, icon="theme"):
        """Persona: official generic user icon (Highlight variant = magenta accent) on a white disc, name below,
        optional magenta pill with what they do. icon=None draws a simple built-in glyph instead."""
        if icon == "theme":
            icon = self.persona_icon
        if icon:
            self.cells.append(dict(kind="ellipse", x=cx - 22, y=cy - 22, w=44, h=44, stroke=MAGENTA, fill=WHITE, sw=2.5))
            self.icon(icon, cx - 15, cy - 15, 30, halo=False)
        else:
            self.cells.append(dict(kind="person", cx=cx, cy=cy))
        self.text(cx - 110, cy + 26, [name], size=12, bold=True, color=name_color, align="center", w=220)
        if pill:
            lines = [pill] if isinstance(pill, str) else pill
            self.edge([(cx, cy + 44), (cx, cy + 58)], "link")
            self.benefit(cx, cy + 58 + (14 * len(lines) + 14) / 2, lines, w=pill_w)

    def keysite(self, x, y, w, h, title, tagline, items=None, cols=4):
        """Card in the 'Key Sites, Methodologies and Guidelines' panel. items = list of short labels."""
        self.rect(x, y, w, h, SAP_BLUE, "#F2F9FF", arc=18, sw=2, role="block")
        self.text(x + 20, y + 30, [title], size=15, bold=True, w=w - 40)
        tw = text_width(tagline, 10.5) + 24
        self.rect(x + w - tw - 16, y - 12, tw, 24, SAP_BLUE, WHITE, arc=24, sw=1.5,
                  lines=[_line(tagline, 10.5, False, TITLE_BLUE)], role="pill")
        if items:
            rows = (len(items) + cols - 1) // cols
            iw = (w - 40 - (cols - 1) * 8) / cols
            for i, it in enumerate(items):
                r, c = divmod(i, cols)
                self.rect(x + 20 + c * (iw + 8), y + 62 + r * 34, iw, 28, "#D9ECFF", WHITE, arc=8, sw=1,
                          lines=[_line(it, 10, False, INK)], role="chip")

    # ---------------- legend / footer ----------------
    def legend(self, x, y, w=420, show_status=True):
        rows = [("pill", "Benefit of a connection"), ("value", "Value statement"), ("badge", "Capability area"),
                ("joule", "Joule embedded")]
        if getattr(self, "used_current", False):
            rows.append(("current", "Current non-SAP solution"))
        st = [s for s in STATUS if s in self.statuses] if show_status else []
        h = 50 + 28 * (len(rows) + len(st)) + 24
        self.rect(x, y, w, h, "#EAECEE", WHITE, arc=12, sw=1, role="legend")
        self.text(x + 16, y + 12, ["Legend"], size=13, bold=True)
        ly = y + 42
        for kind, label in rows:
            if kind == "pill":
                self.rect(x + 16, ly - 8, 44, 16, MAGENTA, MAGENTA, arc=16, sw=1, role="swatch")
            elif kind == "value":
                self.rect(x + 16, ly - 8, 44, 16, SAP_BLUE, WHITE, arc=6, sw=2, role="swatch")
            elif kind == "current":
                self.rect(x + 16, ly - 8, 44, 16, "#475E75", WHITE, arc=6, sw=2, role="swatch")
            elif kind == "badge":
                self.badge(x + 38, ly, "A")
            else:
                self.joule(x + 38, ly)
            self.text(x + 74, ly - 8, [label], size=11)
            ly += 40 if kind in ("badge", "joule") else 28
        for s in st:
            stroke, fill, _, dashed, label = STATUS[s]
            self.rect(x + 16, ly - 8, 44, 16, stroke, fill, arc=6, dashed=dashed, dash="5 3", sw=1.8, role="swatch")
            self.text(x + 74, ly - 8, [label], size=11)
            ly += 26
        return h

    def footer(self, note=None, y=None, version=None):
        y = y or self.H - 40
        t = ("Based on the SAP BTP Capabilities Reference Architecture (\"The Big Picture\") and the SAP BTP "
             "solution diagram icons" + ("; Microsoft Azure icons used per Microsoft terms" if self.used_azure else "")
             + "." + (" " + note if note else ""))
        self.text(40, y, [t], size=11, color=SUB, w=self.W - 80)
        if version:
            self.text(self.W - 240, y, [version], size=11, color=SUB, align="left", w=200)

    # ---------------- checks ----------------
    def check(self):
        warn = []
        rects = [c for c in self.cells if c["kind"] == "rect"]
        for c in rects:
            if c["x"] < 0 or c["y"] < 0 or c["x"] + c["w"] > self.W + 0.5 or c["y"] + c["h"] > self.H + 0.5:
                warn.append(f"rect {c['role']} at ({c['x']:.0f},{c['y']:.0f}) is off the page")
            if c["lines"]:
                for t, size, bold, _ in c["lines"]:
                    tw = text_width(t, size, bold)
                    if tw > c["w"] - 2 * min(c["pad"], 8) - 4:
                        warn.append(f"text '{t}' (~{tw:.0f}px) overflows {c['role']} (w={c['w']:.0f})")
                need = sum(s * 1.25 for _, s, _, _ in c["lines"]) + 6
                if need > c["h"]:
                    warn.append(f"{c['role']} '{c['lines'][0][0]}' needs ~{need:.0f}px height, has {c['h']:.0f}")
        chips = [c for c in rects if c["role"] in ("chip", "value", "pill", "current")]
        for i, a in enumerate(chips):
            for b in chips[i + 1:]:
                if a["x"] < b["x"] + b["w"] and b["x"] < a["x"] + a["w"] and a["y"] < b["y"] + b["h"] and b["y"] < a["y"] + a["h"]:
                    warn.append(f"overlap: '{(a['lines'] or [('?',)])[0][0]}' and '{(b['lines'] or [('?',)])[0][0]}'")
        texts = [c for c in self.cells if c["kind"] == "text"]
        for t in texts:
            for l in t["lines"]:
                tw = text_width(l, t["size"], t["bold"])
                if tw > t["w"] + 2:
                    warn.append(f"free text '{l}' (~{tw:.0f}px) wider than its box ({t['w']:.0f})")
        return sorted(set(warn))

    # ---------------- emitters ----------------
    def _rich_html(self, lines):
        parts = []
        for t, size, bold, color in lines:
            s = escape(t)
            if bold:
                s = f"<b>{s}</b>"
            parts.append(f'<font color="{color}" style="font-size:{size}px">{s}</font>')
        return "<br>".join(parts)

    def to_drawio(self, name="Big Picture"):
        out, i = [], 1

        def cell(value, style, x, y, w, h, tooltip=None):
            nonlocal i
            i += 1
            tt = f' tooltip="{html.escape(tooltip)}"' if tooltip else ""
            out.append(f'<mxCell id="c{i}" value="{html.escape(value)}"{tt} style="{style}" vertex="1" parent="1">'
                       f'<mxGeometry x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" as="geometry"/></mxCell>')

        for c in self.cells:
            k = c["kind"]
            if k == "rect":
                st = (f'rounded={1 if c["arc"] else 0};whiteSpace=wrap;html=1;strokeColor={c["stroke"]};fillColor={c["fill"]};'
                      f'arcSize={c["arc"]};absoluteArcSize=1;strokeWidth={c["sw"]};fontFamily={FONT};fontColor={INK};'
                      f'align={c["align"]};verticalAlign={c["valign"]};spacing={c["pad"] if c["align"] == "left" else 2};'
                      + (f'dashed=1;dashPattern={c["dash"]};' if c["dashed"] else "")
                      + ("locked=1;" if c["role"] == "page" else ""))
                cell(self._rich_html(c["lines"]), st, c["x"], c["y"], c["w"], c["h"])
            elif k == "text":
                inner = "<br>".join(escape(l) for l in c["lines"])
                if c["bold"]:
                    inner = f"<b>{inner}</b>"
                st = (f'text;html=1;strokeColor=none;fillColor=none;align={c["align"]};verticalAlign=top;whiteSpace=wrap;'
                      f'fontFamily={FONT};fontSize={c["size"]};fontColor={c["color"]};spacing=0;')
                cell(inner, st, c["x"], c["y"], c["w"], len(c["lines"]) * c["lh"] + 4)
            elif k == "icon":
                st = f'shape=image;imageAspect=0;aspect=fixed;image={c["data"]};'
                cell("", st, c["x"], c["y"], c["s"], c["s"], tooltip=c["name"])
            elif k == "ellipse":
                cell("", f'ellipse;html=1;strokeColor={c["stroke"]};fillColor={c["fill"]};strokeWidth={c["sw"]};',
                     c["x"], c["y"], c["w"], c["h"])
            elif k == "hero":
                # open trapezoid behind the hero title, drawn as a closed polyline
                x, y, w, h = c["x"], c["y"], c["w"], c["h"]
                pts = [(x, y + h), (x, y), (x + w, y), (x + w - h, y + h), (x, y + h)]
                i += 1
                wp = "".join(f'<mxPoint x="{px}" y="{py}"/>' for px, py in pts[1:-1])
                out.append(f'<mxCell id="c{i}" style="html=1;rounded=0;endArrow=none;strokeColor=#A8DCFF;strokeWidth=18;" edge="1" parent="1">'
                           f'<mxGeometry relative="1" as="geometry"><mxPoint x="{pts[0][0]}" y="{pts[0][1]}" as="sourcePoint"/>'
                           f'<mxPoint x="{pts[-1][0]}" y="{pts[-1][1]}" as="targetPoint"/><Array as="points">{wp}</Array></mxGeometry></mxCell>')
            elif k == "rhombus":
                cell('<font color="#FFFFFF" style="font-size:12px"><b>✦</b></font>',
                     f'rhombus;html=1;strokeColor=#FFFFFF;strokeWidth=1.5;fillColor={SAP_BLUE};gradientColor=#0040B0;fontFamily={FONT};',
                     c["x"], c["y"], c["w"], c["h"], tooltip="Joule")
            elif k == "badge":
                cell(f'<b><font color="#FFFFFF" style="font-size:18px">{escape(str(c["n"]))}</font></b>',
                     f'ellipse;html=1;aspect=fixed;strokeColor=none;fillColor=#E040E8;gradientColor=#A100C2;gradientDirection=south;fontFamily={FONT};',
                     c["cx"] - 18, c["cy"] - 18, 36, 36)
            elif k == "person":
                cx, cy = c["cx"], c["cy"]
                cell("", f'ellipse;html=1;aspect=fixed;strokeColor=none;fillColor=#E040E8;gradientColor=#A100C2;',
                     cx - 22, cy - 22, 44, 44, tooltip="Persona")
                cell("", 'ellipse;html=1;aspect=fixed;strokeColor=none;fillColor=#FFFFFF;', cx - 16, cy - 16, 32, 32)
                cell("", f'ellipse;html=1;aspect=fixed;strokeColor={MAGENTA};strokeWidth=2.5;fillColor=none;', cx - 6, cy - 11, 12, 12)
                cell("", f'shape=mxgraph.basic.half_circle;html=1;strokeColor={MAGENTA};strokeWidth=2.5;fillColor=none;rotation=180;',
                     cx - 10, cy + 3, 20, 9)
            elif k == "edge":
                p = c["pts"]
                st = (f'html=1;rounded=0;strokeColor={c["color"]};strokeWidth={c["width"]};'
                      f'endArrow={"blockThin" if c["end"] else "none"};endFill=1;endSize=5;'
                      f'startArrow={"blockThin" if c["start"] else "none"};startFill=1;startSize=5;'
                      + (f'dashed=1;dashPattern={c["dash"]};' if c["dash"] else ""))
                wp = "".join(f'<mxPoint x="{x}" y="{y}"/>' for x, y in p[1:-1])
                wp = f'<Array as="points">{wp}</Array>' if wp else ""
                i += 1
                out.append(f'<mxCell id="c{i}" style="{st}" edge="1" parent="1"><mxGeometry relative="1" as="geometry">'
                           f'<mxPoint x="{p[0][0]}" y="{p[0][1]}" as="sourcePoint"/><mxPoint x="{p[-1][0]}" y="{p[-1][1]}" as="targetPoint"/>{wp}</mxGeometry></mxCell>')
        body = "\n".join(out)
        return (f'<mxfile host="Electron" type="device"><diagram name="{html.escape(name)}" id="bp1">'
                f'<mxGraphModel dx="{self.W}" dy="{self.H}" grid="0" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{self.W}" pageHeight="{self.H}" background="{PAGE_BG}" math="0" shadow="0">'
                f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>\n{body}\n</root></mxGraphModel></diagram></mxfile>')

    def to_svg(self):
        o = [f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{self.W}" height="{self.H}" viewBox="0 0 {self.W} {self.H}" font-family="Arial, Helvetica, sans-serif">',
             '<defs><linearGradient id="mg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E040E8"/><stop offset="1" stop-color="#A100C2"/></linearGradient>'
             '<linearGradient id="jg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0070F2"/><stop offset="1" stop-color="#0040B0"/></linearGradient>']
        for col in {v[0] for v in EDGES.values()}:
            o.append(f'<marker id="a{col[1:]}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1L10 5L0 9z" fill="{col}"/></marker>')
        o.append('</defs>')
        for c in self.cells:
            k = c["kind"]
            if k == "rect":
                da = f' stroke-dasharray="{c["dash"]}"' if c["dashed"] else ""
                rx = min(c["arc"] / 2, c["h"] / 2, c["w"] / 2)
                o.append(f'<rect x="{c["x"]}" y="{c["y"]}" width="{c["w"]}" height="{c["h"]}" rx="{rx}" fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="{c["sw"]}"{da}/>')
                if c["lines"]:
                    hs = [s * 1.25 for _, s, _, _ in c["lines"]]
                    y = c["y"] + c["h"] / 2 - sum(hs) / 2 if c["valign"] == "middle" else c["y"] + c["pad"]
                    if c["align"] == "left":
                        tx, anchor = c["x"] + c["pad"], "start"
                    else:
                        tx, anchor = c["x"] + c["w"] / 2, "middle"
                    for (t, size, bold, color), lh in zip(c["lines"], hs):
                        fw = ' font-weight="bold"' if bold else ""
                        o.append(f'<text x="{tx}" y="{y + lh / 2}" text-anchor="{anchor}" dominant-baseline="central" font-size="{size}"{fw} fill="{color}">{escape(t)}</text>')
                        y += lh
            elif k == "text":
                anchor = {"left": "start", "center": "middle"}[c["align"]]
                x = c["x"] if c["align"] == "left" else c["x"] + c["w"] / 2
                fw = ' font-weight="bold"' if c["bold"] else ""
                for j, l in enumerate(c["lines"]):
                    o.append(f'<text x="{x}" y="{c["y"] + c["size"] * 0.9 + j * c["lh"]}" text-anchor="{anchor}" font-size="{c["size"]}" fill="{c["color"]}"{fw}>{escape(l)}</text>')
            elif k == "icon":
                head, b64 = c["data"].split(",", 1)
                mime = head[5:].split(";")[0]
                o.append(f'<image x="{c["x"]}" y="{c["y"]}" width="{c["s"]}" height="{c["s"]}" href="data:{mime};base64,{b64}" xlink:href="data:{mime};base64,{b64}"/>')
            elif k == "ellipse":
                o.append(f'<ellipse cx="{c["x"] + c["w"] / 2}" cy="{c["y"] + c["h"] / 2}" rx="{c["w"] / 2}" ry="{c["h"] / 2}" fill="{c["fill"]}" stroke="{c["stroke"]}" stroke-width="{c["sw"]}"/>')
            elif k == "hero":
                x, y, w, h = c["x"], c["y"], c["w"], c["h"]
                o.append(f'<path d="M{x} {y + h} L{x} {y} L{x + w} {y} L{x + w - h} {y + h} Z" fill="none" stroke="#A8DCFF" stroke-width="18"/>')
            elif k == "rhombus":
                x, y, w, h = c["x"], c["y"], c["w"], c["h"]
                o.append(f'<path d="M{x + w / 2} {y} L{x + w} {y + h / 2} L{x + w / 2} {y + h} L{x} {y + h / 2} Z" fill="url(#jg)" stroke="#FFFFFF" stroke-width="1.5"/>')
                cx, cy, r = x + w / 2, y + h / 2, 5.5   # four-point Joule sparkle
                o.append(f'<path d="M{cx} {cy - r} Q{cx} {cy} {cx + r} {cy} Q{cx} {cy} {cx} {cy + r} Q{cx} {cy} {cx - r} {cy} Q{cx} {cy} {cx} {cy - r} Z" fill="#FFFFFF"/>')
            elif k == "badge":
                o.append(f'<circle cx="{c["cx"]}" cy="{c["cy"]}" r="18" fill="url(#mg)"/>')
                o.append(f'<text x="{c["cx"]}" y="{c["cy"]}" text-anchor="middle" dominant-baseline="central" font-size="18" font-weight="bold" fill="#FFFFFF">{escape(str(c["n"]))}</text>')
            elif k == "person":
                cx, cy = c["cx"], c["cy"]
                o.append(f'<circle cx="{cx}" cy="{cy}" r="22" fill="url(#mg)"/><circle cx="{cx}" cy="{cy}" r="16" fill="#FFFFFF"/>'
                         f'<circle cx="{cx}" cy="{cy - 5}" r="6" fill="none" stroke="{MAGENTA}" stroke-width="2.5"/>'
                         f'<path d="M{cx - 10} {cy + 12} A10 9 0 0 1 {cx + 10} {cy + 12}" fill="none" stroke="{MAGENTA}" stroke-width="2.5"/>')
            elif k == "edge":
                d = "M" + " L".join(f"{x} {y}" for x, y in c["pts"])
                da = f' stroke-dasharray="{c["dash"]}"' if c["dash"] else ""
                m = f"url(#a{c['color'][1:]})"
                me = f' marker-end="{m}"' if c["end"] else ""
                ms = f' marker-start="{m}"' if c["start"] else ""
                o.append(f'<path d="{d}" fill="none" stroke="{c["color"]}" stroke-width="{c["width"]}"{da}{me}{ms}/>')
        o.append("</svg>")
        return "\n".join(o)

    def _themed(self, text):
        if not self.recolor:
            return text
        import re
        return re.sub(r"#[0-9A-Fa-f]{6}\b", lambda m: self.recolor.get(m.group(0).upper(), m.group(0)), text)

    def save(self, base, name="Big Picture", preview_dir="/home/claude/preview"):
        """Write <base>.drawio (the deliverable) and a PNG preview for self-checking. Prints layout warnings."""
        unused = set(self.status_of) - self.matched
        for u in sorted(unused):
            print(f"WARNING status key {u!r} matched no chip or tile - check spelling against the catalogue")
        base = base[:-7] if base.endswith(".drawio") else base
        os.makedirs(os.path.dirname(os.path.abspath(base)) or ".", exist_ok=True)
        open(base + ".drawio", "w").write(self._themed(self.to_drawio(name)))
        png = None
        if preview_dir:
            os.makedirs(preview_dir, exist_ok=True)
            stem = os.path.join(preview_dir, os.path.basename(base))
            open(stem + ".svg", "w").write(self._themed(self.to_svg()))
            try:
                import cairosvg
                cairosvg.svg2png(url=stem + ".svg", write_to=stem + ".png")
                png = stem + ".png"
            except ImportError:
                print("cairosvg missing (pip install cairosvg --break-system-packages) - PNG preview skipped")
        warns = self.check()
        for w in warns:
            print("WARNING", w)
        print(f"saved {base}.drawio - {len(warns)} layout warnings" + (f" - preview: {png}" if png else ""))
        return warns
