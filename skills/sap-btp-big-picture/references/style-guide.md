# Big Picture style guide

Derived from the SAP poster "SAP BTP Capabilities Reference Architecture for Best Transformation"
("The Big Picture", version 1.3) and the SAP BTP solution diagram guidelines
(sap.github.io/btp-solution-diagrams). The library encodes all values; this file explains them.

## 1. Page and grid (reference script, 5080 × 1760 px)

```
x 40-600    Hero "The Big Picture" + IT Operations persona
x 640-4500  Main poster
  y  80- 680  Band "SAP Applications and Processes" (deep blue)
               A toolchain (left) · SAP applications + agent loop · Joule capabilities · personas row
  y 650-1530  Band "SAP BTP" (bright blue)
               Cockpit · B · C · D · E blocks (y 700-1240) · benefit pills + deploy tags · Platform Foundation
  y 1500-1710 Band "Sources & Open Ecosystem" (pale blue): benefit pills + 3rd-party panel
x 4550-5040  Key Sites, Methodologies and Guidelines · legend
```

Bands overlap by ~30 px so the lower band covers the upper band's rounded corner, as on the poster.
Blocks are white cards with a value-statement column (185-195 px) on their right edge.

## 2. Palette

| Role | Colour | Where |
|---|---|---|
| Page background | #CFECFF | everything outside bands |
| Apps band | #016DD0 | SAP Applications and Processes |
| BTP band | #26A9FF | SAP BTP |
| Ecosystem band / group panels | #B8E3FF | Sources & Open Ecosystem, product groups |
| Soft panel | #E3F4FF / #D6EEFF | SAP applications card, cockpit, foundation sub-groups |
| Key sites panel | #75BCFE | right-hand panel |
| 3rd-party panel | #C9BCFF | lavender |
| Chip border / Joule | #0070F2 | chips, value statements, Joule diamond |
| Chip & value titles | #0040B0 | bold first lines |
| Benefit pills / badges | #C00FBE (gradient #E040E8 → #A100C2) | magenta |
| Persona & benefit connectors | #E26BE6 | light magenta |
| Fusion team line / agent loop | #5AB8FF | light blue |
| Technical arrows | #2C3E50 | deploy / run / process data |

Status overlay (customer variants only): live #188918 on #EBF5CB · planned #0070F2 dashed · evaluate
#E76500 dashed on #FFF3B8 · out #A9B4BE on #F5F6F7 with greyed text.

## 3. Element semantics

- **Capability block A-E** - magenta letter badge top-left, Joule diamond on the top edge where personas
  enter, title 20 px bold, subtitle 13 px. Letters are fixed: A toolchain, B app dev & automation, C custom
  business AI, D business data, E integration. Don't renumber when an area is dropped.
- **Value statement** - what the area delivers, bold dark blue in a white box beside the block. 1-3 lines.
- **Product group** - light panel with the product's official icon and name (SAP Build, SAP Business Data
  Cloud, SAP Integration Suite …). Dashed frame = logical grouping (AI Foundation, foundation sub-areas,
  on-premise).
- **Tile** - official service icon on a white halo + bold label; label-only when no official icon exists.
- **Chip** - capability or feature; `title=True` makes the first line the bold capability, the rest detail.
- **Benefit pill** (magenta) - the *why* of a connection; always sits on or beside a connector.
- **Tag** (white) - technical relation on a dark arrow ("Deploy and Run Applications").
- **Persona** - official `generic:User (Highlight)` icon on a white disc with magenta ring; pill = what the
  persona does. Personas connect to the Joule diamond of the area they use.
- **Agent loop** - light-blue loop around SAP applications with the LoB agents.

## 4. Typography

Arial (the poster uses SAP 72; draw.io users with 72 installed can switch the font globally). Band titles
19-30 px bold, block titles 20, group titles 13-15, tiles 12 bold, chips 11 (10.5 in dense lists), value
statements 11 bold, footer 11.

## 5. Quality checklist

- `update_icons.py --check` ran; icon commit is in the footer.
- `save()` reports 0 layout warnings and no unmatched status keys.
- Preview viewed section by section: no text touching borders, no pill covering a chip, connectors enter
  blocks at the Joule diamonds, no connector crossing a block's content.
- Every icon is official and labelled; no imitation logos.
- Status colours appear only where the user confirmed a status; legend lists exactly the statuses used.
- `references/our-conventions.md` rules applied.
