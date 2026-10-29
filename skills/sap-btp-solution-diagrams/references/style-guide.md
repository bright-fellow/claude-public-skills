# SAP BTP solution diagram style guide

Derived from the .drawio sources in github.com/SAP-archive/sap-btp-reference-architectures
(e.g. Application-to-Application Integration, Architecting multi-region resiliency, Secure
connectivity with SAP Private Link service). The library encodes all of this; this file explains the
choices so you can compose new diagrams consistently.

## Contents
1. Palette
2. Element catalogue
3. Page layout
4. Flow panel, legend, footer
5. Diagram levels
6. Quality checklist

## 1. Palette

| Role | Stroke | Fill | Library |
|---|---|---|---|
| SAP BTP area / SAP-managed | #0070F2 | #EBF8FF | `area(..., "btp")` |
| SAP application container (S/4HANA etc.) | #0070F2 | #FFFFFF | `area(..., "sap")` |
| SAP service / product box | #0070F2 | #FFFFFF | `box(kind="sap")`, `service()` |
| Sub-component inside SAP box | #0070F2 | #EBF8FF | `box(kind="sap_fill")` |
| Non-SAP area (customer, partner, hyperscaler) | #475E75 | #F5F6F7 | `area(..., "nonsap")` |
| Non-SAP component | #6D7F91 | #FFFFFF | `box(kind="nonsap")` |
| Accent: zones, sites, regions | #07838F | #DAFDF5 | `area(..., "teal")` |
| Accent: trust / identity | #CC00DC | #FFF0FA | `area(..., "pink")`, `edge(kind="trust")` |
| Optional / operational scope | #475E75 dashed | #FFFFFF | `area(..., "dashed")`, `box(kind="ops")` |
| Text / secondary text | #1D2D3E / #556B82 | – | automatic |
| Step markers | gradient #2395FF → #0057D2, white bold digit | | `num()` |

Stroke width 1.5 everywhere; corner radius 8 px on boxes (arcSize 16) and 12 px on areas (arcSize 24);
font Arial; area titles 16 px bold, nested area titles 14 px bold, box titles 12 px bold, sub-lines 11 px.

Connectors (`edge` kinds): `flow` solid #475E75 with arrow; `sync` dashed green #188918 both ends;
`async` dashed SAP blue; `heartbeat` dotted grey no arrows; `backup` dashed grey; `trust` solid pink.
Protocol/technology labels sit on connectors as grey pills (`pill`): "HTTPS", "OData/REST", "CMIS 1.1".

## 2. Element catalogue

- **Service tile** (`service`): 125×130 white box, 40 px icon top-centre, 2–3 line label. Use for BTP
  services inside the BTP area, in a row with equal gaps.
- **Component box** (`box`): title + up to 3 sub-lines. With `icon=` the icon sits left (32 px) and text
  is left-aligned – use for hyperscaler services (VM, database, storage, load balancer).
- **Container areas** (`area`): max three nesting levels (e.g. Azure → zone → box). Title top-left.
- **Actors**: `sap:End User`, `sap:Desktop, Mobile`, `sap:Application Clients` icons with a text label.
- **Icon groups** inside a box: several `icon(..., label=...)` calls spaced evenly (see "Operations &
  protection" in the example).

## 3. Page layout

A proven grid for landscape diagrams (1700 px wide):

```
y=28  Title (20px, SAP blue)              |
y=58  Subtitle (products in scope)        |
y=110 ┌ user ┐┌ SAP app ┐┌ SAP BTP area ┐ | x=1220..1660  Flow panel (steps)
      └──────┘└─────────┘└──────────────┘ |
y=380 ┌ customer / hyperscaler area ───┐  | Legend below the flow panel
      │ row: supporting components     │  |
      │ row: entry (LB / gateway)      │  |
      │ row: two mirrored zones/sites  │  |
      │ row: shared data / witness     │  |
      │ row: DR / optional scope       │  |
      └────────────────────────────────┘  |
footer: "Diagram level: L2" + attribution + assumptions
```

- Flow goes top → bottom (or left → right); never make the reader follow arrows upward except for
  explicit responses.
- Leave 20–40 px lanes between columns for connectors; mirrored layouts (zone 1 / zone 2) make
  symmetry and redundancy obvious.
- Put step numbers on a box's top-right corner or beside a connector, never on text.
- Pills sit centred on vertical connectors in the gap between two areas/rows.

## 4. Flow panel, legend, footer

- Flow panel: one step per numbered marker in the diagram, same numbers, 1–2 sentences each, written
  as what happens ("S/4HANA calls ..."), pre-wrapped at ~50 characters.
- Legend: `legend()` lists only connector kinds and colours actually used. Add `extra_boxes` for
  special swatches.
- Footer: diagram level, attribution (automatic), and a short note of assumptions or items to confirm
  with vendors – this is where uncertainty belongs.

## 5. Diagram levels

- **L0** – capabilities / marketecture, no protocols.
- **L1** – products and main integrations, simple arrows, few numbers.
- **L2** – services, protocols (pills), HA/DR mechanics, numbered flow. Default for technical design.

## 6. Quality checklist (before delivering)

- `save()` reports 0 warnings.
- Preview PNG viewed: no label covered by a number, pill or arrowhead; no text touching borders.
- Every icon has a nearby text label with the product/service name.
- Colours follow the SAP / non-SAP rule; teal used only for zones/sites/regions.
- Numbers in the diagram match the flow panel one-to-one.
- Assumptions are stated in the footer note.
