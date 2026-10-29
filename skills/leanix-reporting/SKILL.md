---
name: leanix-reporting
description: Expert reference for building custom reports with @leanix/reporting and @leanix/reporting-cli for SAP LeanIX EAM. Covers lx.init()/lx.ready() lifecycle, ReportConfiguration, facet filters and callbacks, GraphQL via lx.executeGraphQL(), Fact Sheet data, side panes, report state, metadata translation, and CLI scaffolding. Trigger whenever the user mentions @leanix/reporting, lx.init, lx.ready, lxr namespace, LeanIX custom report, LeanIX reporting framework, LeanIX facets, leanix-reporting-cli, lxr CLI, LeanIX Fact Sheet report, LeanIX GraphQL in reports, or asks to build, debug, or modify any custom report for SAP LeanIX EAM. Also trigger for LeanIX report features like bookmarks, table mode, side panes, dropdowns, view selectors, or state persistence — even without explicitly saying "custom report."
---

# LeanIX Custom Reporting Skill

This skill provides guidance for developing custom reports using the `@leanix/reporting` library for SAP LeanIX EAM.

## Overview

A LeanIX custom report consists of HTML, JavaScript, and CSS files loaded into an iframe inside the LeanIX application. The iframe communicates with the host application via `postMessage`. The `@leanix/reporting` library abstracts this communication and exposes a simple API for data fetching, host commands, and event handling.

**Key resources:**
- npm package: `@leanix/reporting`
- CLI: `@leanix/reporting-cli` (scaffolding, dev server, upload)
- TypeScript typings docs: https://leanix.github.io/leanix-reporting/
- Developer docs: https://docs-eam.leanix.net/reference/setup-custom-reports-project
- GitHub: https://github.com/leanix/leanix-reporting

---

## Installation & Project Setup

### CLI Installation
```bash
npm install -g @leanix/reporting-cli
```

### Scaffold a New Report
```bash
lxr init
```
The interactive scaffolder generates the project skeleton including `package.json` with `leanixReport` metadata:

```json
{
  "name": "My Custom Report",
  "version": "1.0.0",
  "leanixReport": {
    "id": "com.mycompany.my-report",
    "title": "My Custom Report",
    "defaultConfig": {}
  }
}
```

The `id` follows Java package naming convention (alphanumeric, underscores, dots).

### Install the Library
```bash
npm install @leanix/reporting --save
```

### CLI Commands
- `lxr init` — scaffold a new project
- `lxr start` — start dev server (opens report in LeanIX workspace)
- `lxr upload` — upload report to your workspace
- `lxr --help` / `lxr help [command]` — detailed help

---

## Core API: Initialization Lifecycle

Every report follows the same two-step lifecycle:

### Modern ES Module Usage (Recommended)
```typescript
import { lx, lxr } from "@leanix/reporting";

lx.init().then((setup: lxr.ReportSetup) => {
  // setup contains workspace info, permissions, saved state, etc.
  const config: lxr.ReportConfiguration = {
    // define facets, callbacks, etc.
  };
  lx.ready(config);
});
```

### Legacy Global Variable Usage
```javascript
import "@leanix/reporting";
// Now `lx` is a global object

lx.init().then(function (setupInfo) {
  var config = {};
  lx.ready(config);
});
```

### Lifecycle Explained

1. **`lx.init()`** — Notifies the host that the report wants to initialize. Returns a Promise resolved with a `ReportSetup` object containing workspace metadata, user info, permissions, locale, saved state, and more.

2. **`lx.ready(config)`** — Notifies the host that the report is ready. You pass a `ReportConfiguration` object that defines data requirements and callback functions. This is the interface between your code and the framework.

**Important types** (all under the `lxr` namespace):
- `lxr.ReportSetup` — init result with workspace/user context
- `lxr.ReportConfiguration` — the config object for `lx.ready()`
- `lxr.FactSheet` — Fact Sheet data structure
- `lxr.ReportFacetsConfig` — facet filter configuration

---

## ReportConfiguration Object

The config passed to `lx.ready()` is the primary interface to the framework. Key properties:

```typescript
const config: lxr.ReportConfiguration = {
  facets: [
    {
      key: "main",                          // unique facet key
      fixedFactSheetType: "Application",    // optional: lock to a FS type
      attributes: ["displayName", "description", "completion"],
      sorting: [{ key: "displayName", order: "asc" }],
      callback: (data) => { /* render report */ },
      facetFiltersChangedCallback: (filter) => { /* react to filter changes */ }
    }
  ],
  reportViewFactSheetType: "Application",   // optional: for view selector
  allowTableView: true,                     // enable table mode toggle
  menuActions: {
    showConfigure: true                     // show Settings button
  }
};
```

### Facet Callbacks

- **`callback(data)`** — Called when initial data is loaded. The `data` parameter contains the Fact Sheets matching the facet configuration.
- **`facetFiltersChangedCallback(filter)`** — Called whenever the user changes filters in the left panel. Use this to trigger re-fetching or re-rendering.

---

## Data Fetching

### Method 1: Facet Filters (Declarative)
Configure facets in the `ReportConfiguration` to declaratively request Fact Sheet data. The framework handles fetching and provides built-in filter UI, bookmarking, and table view for free.

### Method 2: GraphQL Queries (Imperative)
Use `lx.executeGraphQL()` for custom queries:

```javascript
const query = `{
  allFactSheets(factSheetType: Application) {
    edges {
      node {
        id
        name
        type
        description
        ... on Application {
          lifecycle { phases { phase startDate } }
          relApplicationToBusinessCapability {
            edges {
              node {
                factSheet { id name }
              }
            }
          }
        }
      }
    }
  }
}`;

const result = await lx.executeGraphQL(query);
// result.allFactSheets.edges contains the data
```

### Method 3: Combined
Use facets for the main data set (with built-in filtering) and `executeGraphQL` for supplementary data. Make GraphQL queries reactive to filter changes via `facetFiltersChangedCallback`.

### Method 4: `lx.getFactSheets()`
Convenience method to get all Fact Sheets from the GraphQL endpoint with specified attributes and facet selections:

```javascript
const response = await lx.getFactSheets(
  "Application",                    // factSheetType
  ["displayName", "completion"],    // attributes
  facetSelection,                   // filter definition
  pointsOfView                     // optional view config
);
```

---

## Key API Methods

### Data & Queries
- `lx.executeGraphQL(query, variables?)` — Execute custom GraphQL queries
- `lx.getFactSheets(type, attributes, facetSelection, pointsOfView, options?)` — Fetch Fact Sheets with filters
- `lx.proxyFetch(method, url, data?, options?)` — Make XHR requests through the parent's origin (GET, PUT, POST)

### UI & Navigation
- `lx.openSidePane(elements)` — Show an overlay side pane with provided elements
- `lx.openLink(factSheetId)` — Navigate to a Fact Sheet
- `lx.openFormModal(config)` — Open a modal form (e.g., for report settings)
- `lx.showSpinner()` / `lx.hideSpinner()` — Loading indicator
- `lx.showEditToggle()` / `lx.hideEditToggle()` — Toggle edit mode button
- `lx.navigateToRoute(route)` — Navigate within the LeanIX SPA
- `lx.openInNewTab(state, facetFilter, name?)` — Open report instance in new tab

### State & Metadata
- `lx.publishState(state)` — Persist internal report state (restored via `setup.savedState`)
- `lx.getFactSheetFieldMetaData(type, field)` — Get configured metadata for FS fields (colors, values)
- `lx.translateFieldValue(type, field, value)` — Translate FS field values to user's locale
- `lx.formatCurrency(value)` — Format number as currency per user locale
- `lx.hasPermissions(permissions)` — Check user workspace permissions

---

## Framework Features

The reporting framework provides these capabilities out of the box:

1. **Filterable Fact Sheets** — Configure facets to enable the standard LeanIX filter panel on the left
2. **Custom Dropdowns** — Display custom dropdown menus and get notified on selection changes
3. **View Selector** — Let users choose from available views for a Fact Sheet type; framework passes view info to your report
4. **Table View** — Toggle to a tabular representation of the current data (set `allowTableView: true`)
5. **Report State Persistence** — Save/restore internal state via `lx.publishState()` and `setup.savedState`
6. **Bookmarking** — Users can save filter combinations as named report bookmarks
7. **Translation** — Translate Fact Sheet types, fields, relations, and values to the user's language
8. **Currency Formatting** — Format numbers according to user's locale settings
9. **Field Metadata** — Access configured colors, icons, and metadata for FS fields to ensure visual consistency
10. **Side Pane** — Show detail panes with Fact Sheet info, context menus, and click handlers
11. **Error Propagation** — Errors in reports are propagated to the main application as toast notifications

---

## Typical Report Structure

```
my-report/
├── package.json          # Report metadata + leanixReport config
├── webpack.config.js     # Build config
├── src/
│   ├── index.html        # Report HTML shell
│   ├── index.js          # Entry point (init + ready)
│   ├── report.js         # Report logic class
│   └── assets/
│       └── main.css      # Styles
```

### Minimal index.js Pattern

```javascript
import "@leanix/reporting";
import "./assets/main.css";
import { MyReport } from "./report.js";

lx.init().then(function (setup) {
  const report = new MyReport(setup);
  const config = report.createConfig();
  lx.ready(config);
});
```

### Report Class Pattern

```javascript
export class MyReport {
  constructor(setup) {
    this.setup = setup;
  }

  createConfig() {
    return {
      facets: [
        {
          key: "main",
          attributes: ["displayName", "description"],
          callback: this.render.bind(this),
          facetFiltersChangedCallback: this.onFilterChange.bind(this)
        }
      ]
    };
  }

  render(data) {
    // Build your visualization from data
    const container = document.querySelector(".report-container");
    // ... render logic with Chart.js, D3, plain HTML, etc.
  }

  onFilterChange(filter) {
    // Re-fetch or re-render based on new filters
  }
}
```

---

## Visualization

The framework is **agnostic** about visualization libraries. Common choices:
- **Chart.js** — recommended in official tutorials for charts
- **D3.js** — for complex/custom visualizations
- **Tailwind CSS** — recommended for styling
- **Alpine.js** — lightweight reactivity (used in some official tutorials)
- **Vue.js** — for more complex report UIs
- Any other JS framework or vanilla JS

---

## Common Patterns & Best Practices

### Reactive GraphQL with Facet Filters
```javascript
facetFiltersChangedCallback: async (filter) => {
  const graphQLFilter = mapFacetFilterToGraphQL(filter);
  const data = await lx.executeGraphQL(query, { filter: graphQLFilter });
  renderChart(data);
}
```

### Using Report Settings Modal
```javascript
menuActions: { showConfigure: true },
configCallback: () => {
  lx.openFormModal({
    title: "Report Settings",
    fields: [
      { key: "factSheetType", label: "Fact Sheet Type", type: "SingleSelect", options: [...] }
    ],
    callback: (result) => { /* apply settings */ }
  });
}
```

### Publishing State for Bookmarks
```javascript
// After user makes a selection
lx.publishState({ selectedType: "Application", chartMode: "bar" });
// On init, restore from setup.savedState
const restored = setup.savedState || { selectedType: "Application", chartMode: "bar" };
```

### Getting Field Colors for Consistency
```javascript
const meta = lx.getFactSheetFieldMetaData("Application", "functionalSuitability");
const color = meta.values["perfect"].bgColor; // e.g., "#00B050"
```

---

## Development Workflow

1. `lxr init` — scaffold project
2. `npm install` — install dependencies
3. Add charting library: `npm install chart.js` (or d3, etc.)
4. Add CSS framework: follow Tailwind CSS setup if desired
5. `npm start` / `lxr start` — opens report in your LeanIX workspace browser tab
6. Develop iteratively with hot reload
7. `lxr upload` — deploy to workspace

---

## Troubleshooting & Notes

- Reports run in an **iframe** — no direct DOM access to the parent application
- The `lx` object is the single entry point for all framework communication
- All types are accessed via the `lxr` namespace when using TypeScript
- GraphQL schema is workspace-specific — use the **GraphiQL tool** (Help → Developer Tools → GraphQL Editor, admin access required) to explore available queries and mutations
- The `@deprecated` annotation in GraphQL schema eliminates need for API versioning
- Contact `support@leanix.net` for framework issues
- TypeScript typings: https://leanix.github.io/leanix-reporting/
- Code examples: https://github.com/leanix/leanix-reporting/tree/main/examples
