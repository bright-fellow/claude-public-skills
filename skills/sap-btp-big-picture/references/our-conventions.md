# Our conventions (team rules - these override every default)

Read this file before building. Where a rule here conflicts with SKILL.md, the style guide or the reference
script, **this file wins**.

## Branding & colours
- Always build with `"theme": "brand-red"` (`assets/themes/brand-red.json`):
  - **#DC0000 brand red** only for accents: area badges A–E, the hero rule, connectors, headings.
  - **#FFFFFF white** is the main colour: page background, capability blocks, chips.
  - **Shades of grey** for structure: bands (#3C3C3C / #6E6E6E / #E6E6E6), panels, borders, text.
- Status colours (live green, planned blue dashed, evaluate orange dashed, not in scope grey tag) are *not*
  themed - they must stay distinguishable from the brand red. Never use red to mean a status.
- No other colours. Do not recolour official SAP icons.

## Our landscape (default content for our capability map)
Source of truth: `examples/our_landscape.json` - build with
`python examples/big_picture_reference.py <out> --config examples/our_landscape.json`.
Keep it updated when the landscape changes instead of editing the script.
- **SAP ERP** (live): Sales, Fulfillment, SCM, Finance, Controlling (CO) - shown in the SAP applications card.
- **Salesforce** - CRM (live, non-SAP). **PTC** - PLM (live, non-SAP).
- **Microsoft Azure** - business warehouse and AI solution (live) → SAP Datasphere, Business Warehouse,
  SAP Databricks and AI Foundation are "Not in scope"; Azure appears as *Current solution* in areas C and D.
- **Microsoft Power Platform** - extensions today (live) → *Current solution* in area B.
- **SAP BTP for SAP-centric extensions** - adoption to be decided → SAP Build, SAP CAP, ABAP Cloud = "Evaluate".
- Not yet stated (leave neutral, list in the footer as open points until confirmed): SAP ERP release
  (ECC or S/4HANA), integration platform between Salesforce / PTC and SAP ERP, analytics front end.

## Content rules
- Non-SAP systems are shown with the *Current solution* box (`bp.current`) in the value column of the area
  they cover, and as chips in the ecosystem panel - never inside SAP product groups.
- Only set a status the business has stated; everything else stays neutral.

## Branding & title
- Title: "SAP BTP Capability Map – Our Landscape" (replace with company name once confirmed).
- Hero text: "Your Company" until the company name is confirmed.

## Delivery
- File name: `our-sap-btp-capability-map-v<version>.drawio`; version and date in the footer (`"version"` in the config).
- Deliver only the .drawio.
