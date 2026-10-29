"""Reference capability map - "Your Company" big picture of SAP BTP.

An independent poster layout (own structure, wording and palette) that maps SAP BTP capabilities in five areas
(A toolchain, B apps & automation, C business AI, D business data, E integration) on a platform foundation, using
the official SAP BTP solution-diagram icons. Start every capability map from this script: change content, drop
areas, or pass a status overlay; the adoption summary at the top counts and lists the statuses.

    python big_picture_reference.py                                   # generic map ("Your Company")
    python big_picture_reference.py out/acme-map --status acme_status.json --customer "ACME AG"

The status JSON maps chip/tile labels (see --list-labels or references/catalogue.md) to live | planned | evaluate | out.
"""
import sys, os, json, argparse
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from bigpicture import BigPicture, GROUP_SOFT, INK, BORDER, THIRD, TITLE_INK  # noqa: E402

W, H = 5080, 1760


DEFAULT_APPS = ["Finance", "Supply Chain", "HR", "Spend", "CX", "Industries"]
DEFAULT_TEAMS = [["Developers", "apps & extensions"], ["Business users", "low-code & self-service"],
                 ["Data & AI engineers", "data products & models"], ["Architects", "landscape & integration"],
                 ["IT operations", "run, secure, monitor"]]
DEFAULT_ECOSYSTEM = [["3rd party", "Cloud Applications"], ["Solution Extensions", "Partners"],
                     ["Event Sources", "e.g. plants, warehouses, logistics"], "Cloud Infrastructure",
                     "AI Partners", "Data Lakes / Warehouses", ["3rd party", "Data Providers"]]
CURRENT_BOX = {"B": (1560, 195), "C": (2500, 185), "D": (3530, 185), "E": (4280, 185)}  # note-column x, width


def build(out, status=None, customer=None, version=None, note=None, list_labels=False, config=None):
    """config (optional dict, e.g. loaded from a landscape JSON) may set: title, hero, theme, status,
    apps_title, apps, teams, ecosystem_title, ecosystem, current {area: {title, lines}}, note, version, customer."""
    cfg = dict(config or {})
    status = {**cfg.get("status", {}), **(status or {})}
    customer = customer or cfg.get("customer")
    version = version or cfg.get("version")
    note = note or cfg.get("note")
    org = customer or "Your Company"
    title = cfg.get("title") or f"{org} – SAP BTP Capability Map"
    bp = BigPicture(W, H, title, status=status, theme=cfg.get("theme"), hero=cfg.get("hero", org))

    # ================= bands =================
    bp.band(640, 80, 3860, 600, "apps", "Business applications & teams")
    bp.band(640, 650, 3860, 880, "btp", "SAP BTP", title_dy=12)
    bp.band(640, 1500, 3860, 210, "ecosystem", "Partners & data sources")
    bp.band(4550, 250, 490, 820, "keysites", "Learn more")

    # ================= A: toolchain =================
    bp.block(700, 150, 940, 410, "A", "Transformation toolchain", "Understand, plan and run the change")
    bp.group(720, 220, 900, 190, "SAP tools")
    heads = ["SAP Signavio", "SAP LeanIX", "SAP Enable Now & WalkMe", "SAP BTP"]
    chips = [["Process Analysis & Design", "model and mine processes"],
             ["Landscape Transparency", "architecture inventory"],
             ["Continuous Enablement", "in-app help & training"],
             ["Extension & Innovation Platform", "build, integrate, analyse"]]
    for i, (hd, ch) in enumerate(zip(heads, chips)):
        x = 735 + i * 220.5
        bp.text(x, 252, [hd], size=13, bold=True, color=TITLE_INK, align="center", w=208)
        bp.chip(x, 274, 208, 48, ch, title=1)
    bp.chip(735, 334, 870, 42, ["Cloud Application Lifecycle Management (CALM)", "SAP Cloud ALM"], title=True)
    bp.icon("btp:SAP Cloud ALM", 760, 340, 30, halo=False)
    bp.group(720, 422, 900, 126, "Partner tools (SAP solution extensions)")
    heads = ["OpenText", "Syniti", "Tricentis"]
    chips = [["Information Governance", "documents, archiving, compliance"],
             ["Data Transformation", "migration & data quality"],
             ["Test Automation", "risk-based, end-to-end testing"]]
    for i, (hd, ch) in enumerate(zip(heads, chips)):
        x = 735 + i * 294
        bp.text(x, 454, [hd], size=13, bold=True, align="center", w=282)
        bp.chip(x, 474, 282, 62, ch, title=True)

    # ================= business applications + teams =================
    bp.edge([(1642, 212), (1698, 212)], "both")
    bp.rect(1700, 150, 1560, 125, GROUP_SOFT, GROUP_SOFT, arc=24, role="group")
    bp.text(1724, 164, [cfg.get("apps_title", "SAP applications")], size=20, bold=True, w=700)
    apps = cfg.get("apps", DEFAULT_APPS)
    bp.chips(1724, 206, 1512, apps, cols=len(apps), h=44, title=True)
    bp.rect(3300, 150, 1180, 125, GROUP_SOFT, GROUP_SOFT, arc=24, role="group")
    bp.text(3324, 164, ["Teams"], size=20, bold=True, w=400)
    teams = cfg.get("teams", DEFAULT_TEAMS)
    bp.chips(3324, 206, 1132, teams, cols=len(teams), h=44, title=True)

    # ================= SAP BTP cockpit =================
    bp.group(670, 860, 200, 230, "SAP BTP Cockpit", fill=GROUP_SOFT, stroke=BORDER)
    bp.chip(682, 896, 176, 40, ["Central web-based UI", "for BTP administrators"], title=True)
    bp.chips(700, 950, 150, ["Manage resources", "Activate services", "Setup security", "Monitor consumption"], h=24)
    bp.edge([(872, 980), (898, 980)], "flow2")

    # ================= B: apps & automation =================
    bp.block(900, 700, 870, 540, "B", "Apps & automation", "Extend SAP without touching the core")
    bp.value(1560, 712, 195, 44, ["Low-code to pro-code", "on one platform"])
    bp.value(1560, 764, 195, 44, ["Automate workflows", "across systems"])
    bp.group(920, 820, 625, 400, "SAP Build", icon="btp:SAP Build")
    for cx, ic, lab in [(1000, "btp:SAP Build Code", ["SAP Build", "Code"]),
                        (1150, "btp:SAP Build Apps", ["SAP Build", "Apps"]),
                        (1290, "btp:SAP Build Work Zone", ["SAP Build", "Work Zone"]),
                        (1450, "btp:SAP Build Process Automation", ["SAP Build", "Process Automation"])]:
        bp.tile(cx, 862, lab, icon=ic)
    bp.chip(930, 948, 140, 36, ["Pro Code", "Development"])
    bp.chip(1078, 948, 272, 36, "Low Code Development")
    bp.chip(1360, 948, 175, 36, ["Process Automation &", "Process Visibility"])
    bp.chip(930, 992, 280, 36, ["AI-powered Extension &", "App Development"])
    bp.chip(1218, 992, 132, 36, ["Workspaces &", "Sites"])
    bp.chip(1360, 992, 175, 36, ["Workflow", "Management"])
    bp.chip(930, 1048, 220, 40, ["ABAP Development Tools", "(ADT for Eclipse)"], title=True)
    bp.chip(930, 1096, 220, 40, ["ABAP Cloud", "Clean-core ABAP extensions"], title=True)
    bp.group(1160, 1040, 375, 170, "SAP CAP", "Cloud Application Programming Model",
             icon="btp:SAP Cloud Application Programming Model", fill="#FFFFFF", stroke=BORDER)
    bp.chips(1172, 1100, 351, ["Use Case Logic", "LLM Plugins & SDKs", "Data Management", "SAP Cloud SDK for AI"],
             cols=2, h=26, gapy=8)

    # ================= C: business AI =================
    bp.block(1800, 700, 900, 540, "C", "Business AI", "AI grounded in your business data")
    bp.value(2500, 712, 185, 40, ["Use AI where", "the data lives"])
    bp.value(2500, 760, 185, 40, ["Govern models,", "prompts and costs"])
    bp.value(2500, 808, 185, 40, ["Prebuilt services", "before custom AI"])
    bp.group(1820, 756, 670, 56, "Joule Studio in SAP Build", icon="btp:Joule Studio", fill="#EEF5F1", title_size=14)
    bp.chip(2200, 770, 130, 28, "Build Joule skills")
    bp.chip(2338, 770, 125, 28, "Build AI agents")
    bp.group(1820, 824, 670, 400, "AI Foundation", fill="#F7FAF7", dashed=True)
    bp.group(1835, 852, 640, 124, "AI Services (prebuilt)")
    for cx, ic, lab in [(1990, "btp:SAP Translation Hub", ["SAP Translation", "Hub"]),
                        (2170, "btp:Document Information Extraction", ["Document Information", "Extraction"]),
                        (2350, "btp:Data Attribute Recommendation", ["Data Attribute", "Recommendation"])]:
        bp.tile(cx, 880, lab, icon=ic, w=180)
    bp.group(1835, 988, 300, 132, "CAP LLM Plugin")
    bp.chips(1849, 1016, 272, ["Anonymization", "Embedding", "Similarity Search", "Chat Completion", "RAG Response"],
             cols=2, h=24)
    bp.chip(1835, 1130, 300, 42, ["Foundation Models (SAP built)", "e.g. ABAP code generation"], title=True)
    bp.group(2145, 988, 330, 224, "AI Lifecycle Management")
    bp.icon("btp:SAP AI Launchpad", 2160, 1016, 26, halo=False)
    bp.text(2192, 1022, ["AI Launchpad"], size=12, bold=True, w=110)
    bp.icon("btp:SAP AI Core", 2312, 1016, 26, halo=False)
    bp.text(2344, 1022, ["AI Core · Gen AI Hub"], size=12, bold=True, w=132)
    bp.chips(2159, 1052, 302, ["Central AI Admin", "Prompt Engineering", "Trust & Security", "Prompt Registry",
                               "Orchestration", "Deployment & Delivery"], cols=2, h=26, gapy=6)
    bp.chip(2159, 1150, 302, 26, "Foundation Models Access")
    bp.edge([(2137, 1151), (2157, 1163)], "flow2")

    # ================= D: business data =================
    bp.block(2730, 700, 1000, 540, "D", "Business data & analytics", "One governed layer for data and analytics")
    vy = 712
    for lines, h in [("Planning & analytics", 30), (["Governed data", "products"], 40),
                     (["Share data", "without copies"], 40), (["Bring BW along", "step by step"], 40),
                     (["Ready for AI", "and data science"], 40)]:
        bp.value(3530, vy, 185, h, lines)
        vy += h + 8
    bp.group(2750, 756, 770, 474, "SAP Business Data Cloud", icon="btp:SAP Business Data Cloud")
    bp.chip(2765, 800, 115, 84, ["Business", "Data Cloud", "Cockpit"], title=3, fill="#EEF5F1")
    bp.group(2890, 796, 615, 92, "SAP Analytics Cloud", icon="btp:SAP Analytics Cloud", fill=GROUP_SOFT)
    bp.chips(2904, 836, 587, [["Analytics &", "Planning"], ["Data", "Exploration"], ["Self-Service BI", "& Dashboards"],
                              ["AI, Prediction,", "Simulation"], ["MS Office", "Add-in"]], cols=5, h=36)
    bp.text(2765, 902, ["Intelligent Applications"], size=12, bold=True, color=TITLE_INK, w=200)
    bp.chips(2950, 896, 555, ["Adaptive experiences", "Planning & simulations", "Partner applications"], cols=3, h=26)
    bp.rect(2765, 930, 740, 24, GROUP_SOFT, GROUP_SOFT, arc=6, sw=1, role="label",
            lines=[("Data sharing across all components", 12, True, INK)])
    bp.group(2765, 962, 220, 196, "SAP Datasphere", "Discover, share and model", icon="btp:SAP Datasphere",
             fill=GROUP_SOFT)
    bp.chips(2777, 1014, 196, ["Spaces (Finance, Sales, ...)", "Data Marketplace & Catalog",
                               "SAP managed & analytic models", "Customize Data Products",
                               "Semantics Onboarding (BW)", "Integrate & manage data"], h=20, gapy=4, size=10.5)
    sub = [("Business Warehouse", "BW modernization",
            ["BW Modernization", ["Data Provisioning", "Cockpit"], "BW Models"]),
           ("SAP Databricks", "Data eng. & AI/ML", ["Custom AI & ML", ["Pro-Code Data", "Engineering"], "Unity Catalog"]),
           ("AI Foundation", "AI operating system", None)]
    for i, (t, s, items) in enumerate(sub):
        x = 2993 + i * 174
        bp.group(x, 962, 166, 196, t, s, fill=GROUP_SOFT)
        if items:
            bp.chips(x + 12, 1006, 142, items, h=36, gapy=8)
        else:
            bp.rect(x + 12, 1010, 142, 56, BORDER, "#FFFFFF", arc=12, dashed=True, dash="3 3", sw=1.5, role="chip",
                    lines=[("→ See AI Foundation", 11, True, TITLE_INK), ("in area C", 11, False, INK)])
    bp.group(2765, 1166, 740, 58, fill=GROUP_SOFT)
    bp.text(2777, 1172, ["Data products"], size=12, bold=True, w=170)
    bp.text(2777, 1190, ["SAP object store", "(SAP + customer managed)"], size=10, color="#3A4A5C", w=170, lh=13)
    bp.chips(2960, 1180, 535, ["SAP Data Products", "BW Data Products", "Custom Data Products"], cols=3, h=32,
             title=True)

    # ================= E: integration =================
    bp.block(3760, 700, 720, 540, "E", "Integration", "SAP and non-SAP, cloud and on-premise")
    bp.value(4280, 712, 185, 40, ["APIs, events and", "B2B in one suite"])
    bp.value(4280, 760, 185, 40, ["Hybrid: cloud", "and on-premise"])
    bp.text(3780, 780, ["Connects SAP apps · 3rd-party apps · B2B partners · public sector · APIs & events"],
            size=10, color="#3A4A5C", w=490)
    bp.group(3780, 800, 490, 432, "SAP Integration Suite", icon="btp:SAP Integration Suite")
    for i, t in enumerate([["Open", "integration"], ["Out-of-the-box", "integration"], ["Event based", "integration"]]):
        bp.chip(3788, 860 + i * 100, 112, 36, t, fill="#F7FAF7")
    bp.edge([(3840, 898), (3840, 958)], "dashed")
    bp.edge([(3840, 998), (3840, 1058)], "dashed")
    tiles = [[("btp:API Management", ["API", "Management"]), ("btp:Graph", ["SAP Graph", "navigate data graph"]),
              ("btp:Trading Partner Management", ["Trading Partner", "Management"])],
             [("btp:Cloud Integration", ["Cloud", "Integration"]), ("btp:Integration Advisor", ["Integration", "Advisor"]),
              ("btp:Open Connectors", ["Open", "Connectors"])],
             [("btp:Advanced Event Mesh", ["(Advanced)", "Event Mesh"]),
              ("btp:Migration Assessment", ["Migration Assessment", "& Tools"])]]
    for r, row in enumerate(tiles):
        for c, (ic, lab) in enumerate(row):
            wide = lab[0] == "Migration Assessment"   # nudged right so it clears the Event Mesh status dot
            bp.tile(3965 + c * 120 + (20 if wide else 0), 846 + r * 100, lab, icon=ic, w=150 if wide else 120)
    bp.group(3792, 1146, 466, 78, "On premises", fill="#F5F6F7", dashed=True, title_size=11)
    bp.icon("btp:Edge Integration Cell", 3806, 1176, 28, halo=False)
    bp.text(3842, 1174, ["Edge Integration Cell", "on-prem to on-prem"], size=11, bold=False, w=140, lh=14)
    bp.chip(3990, 1176, 56, 28, "PI/PO")
    bp.chip(4054, 1176, 56, 28, "S/4")
    bp.icon("btp:Cloud Connector", 4140, 1160, 28, halo=False)
    bp.text(4120, 1192, ["Cloud", "Connector"], size=10.5, bold=True, align="center", w=68, lh=13)

    # ================= areas -> foundation =================
    for tx in (1560, 2520, 3470, 4300):
        bp.edge([(tx, 1242), (tx, 1306)], "flow")
        bp.tag(tx, 1272, "runs on")

    # ================= platform foundation =================
    bp.group(670, 1308, 3810, 180, "Platform Foundation", title_size=15)
    bp.group(690, 1338, 730, 140, "Runtimes", fill="#DCEAE4", dashed=True)
    for cx, ic, lab in [(815, "btp:SAP BTP, ABAP environment", ["ABAP Environment"]),
                        (1065, "btp:SAP BTP, Cloud Foundry runtime", ["Cloud Foundry Runtime"]),
                        (1300, "btp:SAP BTP, Kyma runtime", ["Kyma Runtime"])]:
        bp.tile(cx, 1360, lab, icon=ic, w=200)
    bp.chip(705, 1428, 165, 28, "Custom Code Migration")
    bp.chip(878, 1428, 60, 28, "ABAP")
    bp.chip(950, 1428, 230, 28, "Java, Node.js, Python, Buildpacks")
    bp.chip(1195, 1428, 210, 28, "Managed Kubernetes")
    bp.group(1440, 1338, 760, 140, "Application Lifecycle Management", fill="#DCEAE4", dashed=True)
    for cx, ic, lab in [(1560, "btp:SAP Task Center", ["SAP Task", "Center"]),
                        (1735, "btp:SAP Application Logging Service for SAP BTP", ["Application", "Logging"]),
                        (1915, "btp:SAP Continuous Integration and Delivery", ["Continuous Integration", "and Delivery"]),
                        (2095, "btp:SAP Cloud Transport Management", ["Cloud Transport", "Management"])]:
        bp.tile(cx, 1372, lab, icon=ic, w=170)
    bp.group(2220, 1338, 1070, 140, "Persistency, Data & AI/ML", fill="#DCEAE4", dashed=True)
    bp.tile(2300, 1372, ["SAP HANA", "Cloud"], icon="btp:SAP HANA Cloud", w=120)
    bp.chips(2390, 1366, 150, ["Vector Engine", "Data Management", "Embedding Model"], h=28, gapy=8)
    bp.chip(2550, 1366, 160, 46, ["Knowledge", "Graph Engine"], title=2)
    bp.chip(2550, 1420, 160, 46, ["Database", "AI/ML Engine"], title=2)
    bp.chip(2720, 1366, 200, 100, ["Tiered Storage", "HANA Spark, HANA Cloud DB,", "HANA Data Lake Files"], title=True)
    bp.chip(2930, 1366, 345, 46, ["Multi Model", "Spatial, ML, Vector, Graph, JSON, Relational"], title=True)
    bp.chip(2930, 1420, 345, 46, ["Advanced Analytics", "GenAI, ML, Predictive, Information Modelling"], title=True)
    bp.group(3310, 1338, 1150, 140, "Security, Compliance & Connectivity", fill="#DCEAE4", dashed=True)
    for i, (ic, lab) in enumerate([("btp:SAP Identity Authentication", ["Identity", "Authentication"]),
                                   ("btp:SAP Identity Directory", ["Identity", "Directory"]),
                                   ("btp:SAP Identity Provisioning", ["Identity", "Provisioning"]),
                                   ("btp:SAP Connectivity Service", ["Connectivity", "Service"]),
                                   ("btp:SAP Custom Domain Service", ["Custom", "Domain"]),
                                   ("btp:SAP Audit Log Service", ["Audit", "Log"]),
                                   ("btp:SAP Data Privacy Integration", ["Data Privacy", "Integration"])]):
        bp.tile(3400 + i * 160, 1372, lab, icon=ic, w=150)

    # ================= partners & data sources =================
    bp.rect(1600, 1590, 1900, 100, THIRD, THIRD, arc=20, role="group")
    bp.text(1616, 1600, [cfg.get("ecosystem_title", "3rd-party data, technology and applications")], size=14,
            bold=True, w=900)
    eco = cfg.get("ecosystem", DEFAULT_ECOSYSTEM)
    bp.chips(1616, 1630, 1868, eco, cols=len(eco), h=44, gap=12, title=True)
    bp.edge([(1598, 1640), (1300, 1640), (1300, 1492)], "link")
    bp.edge([(2100, 1588), (2100, 1492)], "link")
    bp.edge([(3000, 1588), (3000, 1492)], "link")
    bp.edge([(3502, 1640), (4000, 1640), (4000, 1492)], "link")

    # ================= learn more =================
    bp.keysite(4570, 320, 450, 140, "SAP Discovery Center", "Missions, services and reference architectures",
               ["Missions", "Reference Architectures", "SAP BTP Services", "SAP Business AI Features"], cols=2)
    bp.keysite(4570, 492, 450, 208, "SAP Business Accelerator Hub", "Ready-made APIs, events and integration content",
               ["APIs", "Events", "Graph", "Business Objects", "Adapters", "Business Add-Ins (BAdIs)",
                "Business Object Interfaces", "CDS Views"], cols=2)
    bp.keysite(4570, 732, 450, 66, "SAP Trust Center", "Security, data protection and compliance")
    bp.keysite(4570, 830, 450, 210, "Architecture guidance", "Methodologies for architects and developers",
               ["Reference Architectures", "SAP Integration Solution Advisory Methodology",
                "SAP Application Extension Methodology", "SAP Data & Analytics Advisory Methodology"], cols=1)

    # current non-SAP solutions, bottom of each area's note column
    for area, c in cfg.get("current", {}).items():
        x, w = CURRENT_BOX[area]
        lines = c.get("lines", [])
        h = 30 + 15 * len(c["title"] if isinstance(c["title"], list) else [c["title"]]) + 14 * len(lines)
        bp.current(x, 1226 - h, w, h, c["title"], lines)

    bp.legend(4550, 1300, w=490)
    bp.summary(1700, 300, 2780, 262)   # last: counts every status drawn above
    m = __import__("bigpicture").ICON_MANIFEST
    bp.footer(note=(note or "") + f" Icon set: SAP BTP solution diagrams, commit {m.get('commit', '?')[:8]} "
              f"({m.get('commit_date', '?')[:10]}).", y=H - 36, version=version)
    if list_labels:
        print("\n".join(dict.fromkeys(bp.labels)))
        return []
    return bp.save(out, name=title)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out", nargs="?", default="/home/claude/out/sap-btp-capability-map")
    ap.add_argument("--status", help="JSON file {label: live|planned|evaluate|out}")
    ap.add_argument("--customer", help="organisation name for the title and hero (default: Your Company)")
    ap.add_argument("--version")
    ap.add_argument("--list-labels", action="store_true", help="print every label that accepts a status, then exit")
    ap.add_argument("--config", help="landscape JSON (theme, title, apps, teams, ecosystem, current, status ...)")
    a = ap.parse_args()
    build(a.out, json.load(open(a.status)) if a.status else None, a.customer, a.version, list_labels=a.list_labels,
          config=json.load(open(a.config)) if a.config else None)
