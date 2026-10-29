---
name: "sap-btp-solution-diagrams"
description: Create SAP BTP solution diagrams / reference architectures in the official SAP BTP diagram style (as in github.com/SAP-archive/sap-btp-reference-architectures) as editable draw.io (.drawio) files, including official SAP BTP service icons and Microsoft Azure architecture icons. Use this skill whenever the user asks to draw, diagram, visualize or "draw up" an architecture involving SAP (S/4HANA, SAP BTP, Integration Suite, Document Management, Cloud Connector, ArchiveLink/CMIS, SAP on Azure, RISE) or wants a diagram "in SAP style", "as a BTP solution diagram", "for diagrams.net/draw.io", or wants Azure components (VMs, Load Balancer, SQL, Blob Storage, availability zones, regions, Private Link) mixed into an SAP architecture - even if they only say "draw this up" after discussing an SAP architecture.
---

# SAP BTP solution diagrams (with Azure)

Produce architecture diagrams that look like SAP's official BTP solution diagrams and open cleanly in
diagrams.net. **The output is always a single `.drawio` file** – editable in diagrams.net, draw.io
desktop and the VS Code draw.io extension. Do not hand over SVG, PNG or other formats unless the user
explicitly asks for them; the user edits and exports from draw.io themselves.

`save()` also renders a PNG preview to `/home/claude/preview/` – that file is only for you to check the
layout visually before delivering; never copy it to the outputs folder.

Everything needed is bundled: `scripts/btpdiagram.py` (the library), `scripts/find_icon.py` (icon search),
`assets/sap_btp_icons.json` (76 official SAP BTP icons), `assets/azure_icons.json` (627 Microsoft Azure
architecture icons). No network access is required.

## Two levels: always an overview and a deep dive

Every architecture is delivered as **two .drawio files** unless the user asks for only one level:

| File | Level | Content |
|---|---|---|
| `<name>-L1-overview.drawio` | L0 / max L1 | Main building blocks only: products and platforms (e.g. "SAP S/4HANA Cloud", "SAP BTP", "SAP Integration Suite", "Microsoft Azure", "Microsoft Entra ID", "RISE with SAP"). No VMs, zones, subnets, databases, load balancers, protocols or ports; at most one line of qualifier per block ("Active-active across two zones"). Roughly 6–10 blocks, max 4 numbered steps plus identity letter, connectors only between blocks. |
| `<name>-L2-deep-dive.drawio` | L2+ | Every component: services, VMs, zones, networking, databases, replication, witness, backup, DR, protocol pills, full flow panel. |

Both share names, colours and step numbering where possible, so the overview reads as a zoomed-out
deep dive. Each footer references the other file. Build the deep dive first (it forces the design),
then derive the overview by collapsing components into their building block.

## Workflow

1. **Pin down the content first.** Pull components, flows and the diagram level from the conversation.
   Level L0 = marketecture, L1 = product boxes and main flows, L2 = services, protocols, HA/DR detail
   (default for architecture discussions). If a key fact is unknown (e.g. whether a vendor supports
   active-active), draw the proposed design and say so in the footer note rather than inventing certainty.
2. **Read the style guide** in `references/style-guide.md` (palette, element catalogue, layout grid,
   what goes into flow panel/legend). If Azure (or "hyperscaler", "SAP on Azure", zones, regions) is in
   scope, also read `references/azure.md` – it contains Microsoft's icon usage rules and a mapping of
   common architecture roles to Azure icons.
3. **Find icons** with `python scripts/find_icon.py <words>` (e.g. `find_icon.py sql --lib azure`).
   Only use icons that exist in the bundled libraries; use a plain box for anything without an icon.
   Never draw your own imitation of a vendor logo.
4. **Write layout scripts** in `/home/claude/` that import the library – one for the L2 deep dive, one
   for the L1 overview. Start from the examples and change content rather than starting blank:
   `examples/easy_archive_L2_deep_dive.py` / `examples/easy_archive_L1_overview.py` (S/4HANA → SAP BTP
   DMS → easy archive active-active on Azure, IAS proxying Entra ID) and
   `examples/integration_suite_L2_deep_dive.py` / `examples/integration_suite_L1_overview.py`
   (Integration Suite in two regions behind Azure Front Door, S/4HANA Cloud, Salesforce, Cloud
   Connector HA pair on Azure, ECC in RISE).
5. **Run it, then look at the preview PNG** (path printed by `save()`). `d.save(base)` prints layout warnings (text overflow, overlapping
   boxes, connectors crossing boxes, elements off-page). Fix every warning, then `view` the PNG and fix
   what the checker cannot see: step numbers covering labels, crowded areas, unbalanced whitespace,
   connectors that read ambiguously. Iterate until clean – a diagram with one overlapping label looks
   broken to an architect.
6. **Deliver only the `.drawio` files** (overview + deep dive) with `present_files` from `/mnt/user-data/outputs/`
   (e.g. `d.save("/mnt/user-data/outputs/<name>")` writes `<name>.drawio` there). In the reply, state briefly which decisions the diagram encodes that the
   user should verify, and that connectors are free-floating (they must be reattached if boxes are moved
   in diagrams.net).
7. **Changing an existing diagram**: edit the layout script and regenerate rather than patching the
   .drawio XML. To add a row, insert it and wrap everything below in `with d.shift(0, <height>):`.

## Library essentials

```python
import sys; sys.path.insert(0, "/mnt/skills/user/sap-btp-solution-diagrams/scripts")  # adjust to skill path
from btpdiagram import Diagram
d = Diagram(1700, 1200, "Title in SAP blue", "Subtitle: products in scope")
d.area(x, y, w, h, "btp" | "sap" | "nonsap" | "teal" | "pink" | "dashed", "Area title", "subtitle")
d.box(x, y, w, h, ["Bold title", "muted line", ...], kind="sap"|"sap_fill"|"nonsap"|"ops", icon="azure:Virtual Machine")
d.service(x, y, 125, 130, "sap:SAP Destination service", ["SAP Destination", "service"])   # BTP service tile
d.icon("sap:Cloud Connector", x, y, 34, label=["Master (active)"], label_w=150)
d.edge([(x1, y1), (x1, y2), (x2, y2)], "flow"|"sync"|"async"|"heartbeat"|"backup"|"trust")
d.pill(cx, cy, "CMIS 1.1 · HTTPS")      # protocol label sitting on a connector
d.num(cx, cy, 3)                        # step marker (digits or letters, e.g. "A"), matches the flow panel
d.flow_panel(1220, 110, 440, 720, ["# Section", ("A", ["lettered step"]), ["auto-numbered step", "..."], ...])
with d.shift(0, 230):                   # move a whole block, e.g. to insert a new row into an existing layout
    ...
d.legend(1220, 850, labels={"async": "Content deployment"})   # auto from what was used; optional wording overrides
d.footer("L2", "Assumptions / items to confirm")
d.save("/mnt/user-data/outputs/<name>")   # -> <name>.drawio (deliverable) + preview PNG in /home/claude/preview/
```

Things that are easy to get wrong:

- **Text never wraps.** Pass each line separately and keep lines short (box sub-lines ≈ 7 px per char
  at 11 px). The checker warns on overflow; shorten wording before widening boxes.
- **Connectors are point lists**, drawn orthogonally: route with L-bends through the gaps between boxes
  (keep 20–40 px lanes between columns for this). Arrowheads should stop 2 px before the target edge.
- **Draw order = z-order.** Add areas before the boxes inside them, boxes before their step numbers.
- **Coordinates are absolute.** Lay out on a mental 10 px grid; keep equal gaps between sibling boxes
  and mirror the two halves of symmetric designs (e.g. zone 1 / zone 2) so the HA story reads at a glance.

## Content conventions (why they matter)

SAP architects read these diagrams by colour before they read labels, so colour must carry meaning:
blue = SAP (BTP areas light blue, SAP services white with blue border), grey = everything non-SAP
(customer, partner, hyperscaler such as Microsoft Azure), teal = accent for zones/sites/regions,
pink = trust/identity, dashed = optional or operational scope. Numbered steps plus a "Flow" panel let
the diagram be presented without a speaker; a legend that only lists what is used keeps it honest.
Details and the full catalogue are in `references/style-guide.md`.

## Azure specifics (summary – details in references/azure.md)

- Put Azure inside a grey `nonsap` area titled "Microsoft Azure" (subscription/region as subtitle),
  availability zones or regions as `teal` areas, VNets / DR scope as `dashed` areas.
- Microsoft's terms: always label an Azure icon with the product name near it, never crop, rotate,
  flip or recolor icons, and only use an icon to represent that Microsoft product. Icons may be used in
  architecture diagrams and documentation (see `assets/azure-icons-terms-of-use.pdf`).
- The footer automatically credits the SAP and Azure icon sources when Azure icons are used.
