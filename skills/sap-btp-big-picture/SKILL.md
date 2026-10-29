---
name: "sap-btp-big-picture"
description: Create a "Your Company" big picture of SAP BTP - an SAP BTP capability map poster (A transformation toolchain, B apps & automation, C business AI, D business data & analytics, E integration, platform foundation, partners & data sources, learn-more panel, adoption summary) - as an editable draw.io file with the official, always up-to-date SAP BTP solution-diagram icons, either generic or tailored to an organisation with a live / planned / evaluate / out-of-scope status overlay. Use whenever the user asks for a big picture, BTP capability map, BTP landscape poster, "where do we stand on BTP", BTP adoption/heat map, target picture or capability overview across BTP. For a single solution or integration architecture use sap-btp-solution-diagrams instead.
---

# SAP BTP big picture (capability map)

Produces an SAP BTP **capability map poster** - "Your Company" big picture - as **one editable `.drawio`
file** (diagrams.net, draw.io desktop, VS Code extension). The layout, wording and "lagoon & coral" palette
are this skill's own; it is not a copy of any SAP poster. Only the **official SAP BTP solution-diagram icons**
(github.com/SAP/btp-solution-diagrams, Apache-2.0) and SAP product names come from SAP, and the footer says
the map is independent and not endorsed by SAP.

It builds on the base skill **sap-btp-solution-diagrams**: same delivery rules (drawio only, preview PNG is
for self-checking and never delivered), same layout-checker approach, and its `sap:` / `azure:` icon libraries
stay available.

**Before anything else read `references/our-conventions.md`.** It holds the team's own rules and overrides
every default in this file and in the style guide where they conflict.

## Workflow

1. **Refresh the icons** (every run, takes a second):
   `python scripts/update_icons.py --check`
   It compares the upstream commit with the icon set in use and, if SAP has published new or redrawn icons,
   downloads them into a cache (`~/.cache/sap-btp-big-picture/`, override with `BIGPICTURE_ICON_CACHE`) and
   prints what was added / removed / redrawn. The library always loads the newer of cache and bundled set.
   Offline it says so and continues with the bundled set - mention that in the reply. If icons were removed
   or renamed, fix the affected `btp:` keys (the build fails with candidate names) or add the new upstream
   file name to `FIX` in `update_icons.py`.
2. **Pin down the variant.**
   - *Generic* ("show me the big picture"): run `examples/big_picture_reference.py` unchanged - the hero
     reads "Your Company".
   - *Organisation map* (most requests): `--customer "<name>"` puts the name in the hero and title. Collect per
     capability whether it is **live**, **planned**, **evaluate** or **out** of scope - from the conversation,
     an uploaded inventory, or LeanIX if connected. Write a status JSON keyed by labels from
     `python examples/big_picture_reference.py --list-labels` (example: `examples/customer_status_example.json`).
     Anything unmentioned stays neutral; never guess a status - list unknowns in the footer note instead.
     The adoption summary at the top counts and lists every status automatically.
   - *Tailored content* (extra products, dropped areas, customer systems): copy the reference script and edit
     it; keep the area letters A-E so maps stay comparable.
   - *Landscape config* (preferred for an organisation's own map): one JSON holding theme, title, hero,
     applications and teams chips, ecosystem chips, *current solution* boxes per area and statuses - see
     `examples/our_landscape.json`. Keep the organisation's landscape there, not in code.
3. **Build**: `python examples/big_picture_reference.py <out> --config landscape.json` (or `--status s.json
   --customer "ACME AG" --version "v0.1"`), or your edited copy. `save()` prints layout warnings and
   unmatched status keys.
4. **Check**: fix every warning, then view the preview PNG (`/home/claude/preview/<name>.png`, crop sections
   with PIL - the page is 5080 px wide). Look for text touching borders, overlaps, connectors over labels.
5. **Deliver** only the `.drawio` (send it with the file tool; copy to `/mnt/user-data/outputs/` where that
   convention applies). In 2-4 lines say: which variant, which statuses are encoded and need confirming, icon
   set commit/date, and that connectors are free-floating in draw.io (reattach when moving boxes).

## Library (`scripts/bigpicture.py`)

```python
import sys; sys.path.insert(0, "<this skill>/scripts")
from bigpicture import BigPicture
bp = BigPicture(5080, 1760, "ACME AG – SAP BTP Capability Map", hero="ACME AG", status={"SAP Build Apps": "live"})
bp.band(x, y, w, h, "apps" | "btp" | "ecosystem" | "keysites", "Band title")
bp.block(x, y, w, h, "B", "Apps & automation", "Extend SAP without touching the core")  # white card + letter badge
bp.value(x, y, 185, 40, ["Low-code to pro-code", "on one platform"])               # note column beside an area
bp.group(x, y, w, h, "SAP Build", icon="btp:SAP Build", dashed=False)             # product group (status-able)
bp.tile(cx, y, ["SAP Build", "Apps"], icon="btp:SAP Build Apps")                  # official icon + label
bp.chip(x, y, w, h, ["Pro Code", "Development"], title=False)                    # capability chip (status-able)
bp.chips(x, y, w, [...], cols=2, h=24)                                            # chip grid
bp.benefit(cx, cy, ["Label on", "a connection"])                                  # optional accent pill
bp.tag(cx, cy, "runs on"); bp.edge(pts, "link"|"both"|"flow"|"flow2"|"soft"|"dotted"|"dashed")
bp.keysite(x, y, w, h, "SAP Discovery Center", "one muted line", [items], cols=2)  # learn-more card
bp.current(x, y, w, h, ["Microsoft", "Power Platform"], ["Extensions today"])        # non-SAP solution in use
bp.legend(x, y); bp.summary(x, y, w, h)  # summary last: counts and lists the statuses drawn
bp.footer(note, version=...); bp.save("/path/name")
# theme: BigPicture(..., theme="brand-red") recolours by role at save time (assets/themes/*.json, roles in ROLES)
```

Icon keys: `btp:<service>` (official service icons, preferred), `generic:<name> (SAP|Non-SAP|Highlight)`
(official generic icons), `sap:` / `azure:` (base skill). Search: `python scripts/find_icon.py <words>`.

Rules that are easy to get wrong:
- **Only official icons.** No icon in the set → label-only tile or chip. Never draw or imitate product logos
  (SAP Signavio, LeanIX, WalkMe, Databricks, partner logos are text only).
- **Keep it independent.** Write notes, subtitles and labels in your own words; do not reproduce SAP posters,
  slides or marketing copy, and do not add SAP brand colours or SAP-specific markers.
- **Text never wraps** - one string per line; shorten wording before widening boxes.
- **Draw order = z-order**: band → block → group → chips; badges come with the block; summary and legend last.
- **Themes recolour, they don't re-layout**: a theme JSON maps colour roles (`ROLES` in bigpicture.py) to
  new colours. Status colours are never themed.
- **Status colours are reserved** (green live, blue dashed planned, orange dashed evaluate, grey out); do not
  use them for anything else, and only use statuses the user confirmed.

## References
- `references/our-conventions.md` - team rules, read first, they win.
- `references/style-guide.md` - palette, grid, element semantics, quality checklist.
- `references/catalogue.md` - what the reference map contains per area.
- `assets/LICENSE-btp-solution-diagrams.txt` - Apache-2.0 licence of the official icon set; keep it with the skill.
