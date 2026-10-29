# Capability map style guide

The skill's own poster style: an independent layout and an invented "lagoon & coral" palette. Only the icons
follow the SAP BTP solution diagram guidelines (sap.github.io/btp-solution-diagrams). The library encodes all
values; this file explains them.

## 1. Page and grid (reference script, 5080 × 1760 px)

```
x 40-600    Hero: organisation name ("Your Company" by default) with a short coral rule
x 640-4500  Main map
  y  80- 680  Band "Business applications & teams" (deep slate)
               A toolchain (left) · SAP applications card · Teams card · adoption summary
  y 650-1530  Band "SAP BTP" (teal)
               Cockpit · B · C · D · E areas (y 700-1240) · "runs on" arrows · Platform Foundation
  y 1500-1710 Band "Partners & data sources" (pale sage): 3rd-party panel
x 4550-5040  Learn more panel · legend
```

Bands overlap by ~30 px so the lower band covers the upper band's rounded corner. Areas are white cards with
a note column (185-195 px) on their right edge.

## 2. Palette

| Role | Colour | Where |
|---|---|---|
| Page background | #F3EFE6 | warm paper outside the bands |
| Apps band | #23394A | business applications & teams |
| BTP band | #2F7C78 | SAP BTP |
| Ecosystem band / group panels | #D5E7DF | partners & data sources, product groups |
| Soft panels | #EEF5F1 / #DCEAE4 / #F7FAF7 | applications & teams cards, cockpit, foundation sub-groups |
| Learn-more panel | #6E9A8C | right-hand panel |
| 3rd-party panel | #EED9C4 | sand |
| Chip and card border | #3A8A86 | chips, notes, areas |
| Chip and note titles | #1C4F55 | bold first lines |
| Accent: badges, rule, pills | #E0684F (badge gradient #EE8C74 → #C24E37) | coral |
| Light connectors | #E9A28F | relations between areas and the ecosystem |
| Technical arrows | #34444B | "runs on" |

Status overlay: live #188918 on #EBF5CB · planned #0064D9 dashed · evaluate #E76500 dashed on #FFF3B8 ·
out #A9B4BE on #F5F6F7 with greyed text. Themes (`assets/themes/*.json`) recolour every role above except the
status colours.

## 3. Element semantics

- **Capability area A-E** - coral letter badge top-left, title 20 px bold, muted subtitle 13 px. Letters are
  fixed: A toolchain, B apps & automation, C business AI, D business data & analytics, E integration. Don't
  renumber when an area is dropped.
- **Note** - one to three short lines on what the area is for, in your own words, in the column beside it.
- **Product group** - light panel with the product's official icon and name (SAP Build, SAP Business Data
  Cloud, SAP Integration Suite …). Dashed frame = logical grouping (AI Foundation, foundation sub-areas,
  on-premise).
- **Tile** - official service icon on a white halo + bold label; label-only when no official icon exists.
- **Chip** - capability or feature; `title=True` makes the first line the bold capability, the rest detail.
- **Tag** (white) - technical relation on a dark arrow ("runs on").
- **Accent pill** (optional, coral) - label on a connection; the reference map does not use it.
- **Teams card** - who works with the platform, one chip per team.
- **Adoption summary** - counts and lists live / planned / evaluate / out; draw it last.
- **Learn-more card** - a resource with a muted one-line description and its contents as small chips.

## 4. Typography

Arial. Band titles 19-30 px bold, area titles 20, group titles 13-15, tiles 12 bold, chips 11 (10.5 in dense
lists), notes 11 bold, footer 11.

## 5. Quality checklist

- `update_icons.py --check` ran; icon commit is in the footer.
- `save()` reports 0 layout warnings and no unmatched status keys.
- Preview viewed section by section: no text touching borders, no chip overlapping another, no connector
  crossing an area's content.
- Every icon is official and labelled; no imitation logos; no SAP brand colours or SAP poster wording.
- Status colours appear only where the user confirmed a status; legend and summary list exactly those.
- `references/our-conventions.md` rules applied.
