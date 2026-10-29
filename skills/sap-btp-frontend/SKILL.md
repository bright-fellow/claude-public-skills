---
name: "sap-btp-frontend"
description: "Entry point for any SAP BTP frontend task (SAPUI5/OpenUI5, UI5 Web Components, webcomponents-react, CAP, Fiori): picks the stack, then routes to the deep skill. Holds CAP and Fiori guidance itself."
---

# SAP BTP Frontend (hub)

This skill decides *which* SAP frontend stack fits, then hands off to the skill that holds the depth. It owns CAP and Fiori design guidance directly. It does not repeat UI5 API detail; that lives in the sibling skills below.

## 1. Orient (before any code)

Settle these four from context; ask once only if a wrong guess would change the whole approach.

1. **UI framework**: classic SAPUI5/OpenUI5 or UI5 Web Components (vanilla or React).
2. **UI5 approach** (classic only): Fiori Elements (annotation-driven) or freestyle.
3. **Backend**: CAP Node.js, CAP Java, or an existing OData service.
4. **Floorplan**: see section 4.

## 2. Pick the output environment

| Where it runs | Classic SAPUI5 | UI5 Web Components | Horizon replica (CSS vars + 72 font) |
|---|---|---|---|
| Sandbox / Claude artifact / static HTML | Yes, CDN bootstrap `https://ui5.sap.com/resources/sap-ui-core.js` | **No** (no CDN, needs a bundler) | Yes, fastest for mockups |
| Local dev with npm (Vite/webpack) | Yes (`yo @sap/fiori`, `ui5 serve`) | Yes | Not needed |
| Coding agent with MCP | Use the MCP servers first (section 6) | Same | Same |

## 3. Route to the deep skill

Load the matching skill with the Skill tool and follow it. Load more than one if the task spans stacks.

| Task | Load |
|---|---|
| XML views, controllers, OData V2/V4 binding, routing, manifest.json, Fiori Elements, OPA5/QUnit, TypeScript in UI5, BAS/ui5 CLI | `sapui5` |
| `ui5-*` custom elements, vanilla/Angular/Vue, Horizon `--sap*` tokens, sandbox mockup strategy, SAPUI5 to WC equivalence | `ui5-webcomponents` |
| Anything React + UI5 (`@ui5/webcomponents-react`, ObjectPage, AnalyticalTable, FilterBar, ThemeProvider, v1 to v2 migration) | `ui5-webcomponents-react` |
| Custom adapter for SAP Cloud Integration | `sap-ci-custom-adapter` |
| Architecture diagram of the solution | `sap-btp-solution-diagrams` |

Decision tree when unsure:

```
Needs Fiori Launchpad, Fiori Elements or OData V4 deep binding? -> sapui5
React app?                                                      -> ui5-webcomponents-react
Other framework / standalone / lightweight?                     -> ui5-webcomponents
Mockup only?  sandbox -> Horizon replica (ui5-webcomponents mockup section) or SAPUI5 CDN
              npm     -> ui5-webcomponents(-react) + Vite
Still unclear -> ask about environment and deployment target
```

## 4. Fiori design guidance (owned here)

Principles: role-based, adaptive, simple (one primary action per screen), coherent (same icon = same action), delightful.

| Use case | Floorplan | Classic UI5 | Web Components |
|---|---|---|---|
| Browse and filter a list | List Report | FE template / `sap.ui.comp.smarttable` | `ui5-table` + filter bar |
| View/edit one object | Object Page | `sap.uxap.ObjectPageLayout` | `ui5-dynamic-page` / React `ObjectPage` |
| Step-by-step creation | Wizard | `sap.m.Wizard` | `ui5-wizard` |
| Overview with KPIs | Analytical List Page | FE ALP | custom |
| Side-by-side browsing | Flexible Column Layout | `sap.f.FlexibleColumnLayout` | `ui5-flexible-column-layout` |

Action placement: primary action top-right toolbar or footer; destructive actions always confirm; contextual actions in row or line-item toolbar; no Edit/Delete in the page header when a table is the main content. Theme is always Horizon (`sap_horizon`; `data-sap-ui-theme` for classic, `setTheme` for WC).

## 5. CAP guidance (owned here)

```
my-cap-app/
├── db/schema.cds      # domain model
├── srv/service.cds    # service definitions
├── srv/service.js     # custom handlers
├── app/               # UI5 apps
└── package.json / .cdsrc.json
```

- Services are cheap: one per use case, not per entity.
- Generic handlers first; custom code only for business logic via `srv.before/on/after`.
- `managed` for audit fields, `cuid` for UUID keys.
- Caret versions (`^`) for `@sap/cds`, never exact pins.

## 6. MCP servers: use first in coding contexts

If the session has SAP MCP tools, prefer them over static knowledge for version-accurate answers:

- **UI5 MCP** (`@ui5/mcp-server`, or the `SAPUI5_MCP_Server` tools on Andreas's computer): `get_api_reference`, `run_ui5_linter`, `run_manifest_validation`, `create_ui5_app`, `get_guidelines`.
- **CAP MCP** (`@cap-js/mcp-server`, or `SAP_CAP_MCP_Server`): `search_model` reads the real CDS model, `search_docs` for CAP docs.
- **Fiori MCP** (`@sap-ux/fiori-mcp-server`): Fiori Elements generation, annotation search, manifest edits.
- Community: `github.com/marianfoo/mcp-sap-docs` for unified SAP docs search.

Workflow: CAP MCP for the model, Fiori MCP for the FE skeleton, UI5 MCP to look up APIs and lint. Without MCP, if unsure of an API signature, say so and point to ui5.sap.com.

## 7. Tooling and delivery

Bootstrap:

```bash
npm install -g @sap/generator-fiori && yo @sap/fiori                       # classic SAPUI5
npm create vite@latest my-app -- --template @ui5/webcomponents-react-vite  # WC + React
cds init my-app && cd my-app && cds add approuter                         # CAP + UI5
```

Testing: QUnit + OPA5 (classic), Vitest/Jest + React Testing Library (WC React), `@sap/cds/test` (CAP). Lint: `@ui5/linter` (classic), ESLint (React).

BTP deployment checklist:

- [ ] `xs-security.json` with XSUAA scopes
- [ ] `mta.yaml` for MTA build
- [ ] App Router (`@sap/approuter`) and `xs-app.json` routes
- [ ] CSP: no `unsafe-eval`, no `unsafe-inline`
- [ ] Horizon theme, all strings in i18n
- [ ] OData services annotated for Fiori