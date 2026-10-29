"""Search all icon libraries available to the capability-map skill.

    python find_icon.py build            # search every library
    python find_icon.py ai --lib btp     # official SAP BTP service icons only
    python find_icon.py --list generic   # list a whole library (btp | generic | sap | azure)

Prefer 'btp:' (official SAP BTP solution-diagram service icons, refreshed via update_icons.py) and
'generic:' (official generic icons: SAP / Non-SAP / Highlight variants). 'sap:' and 'azure:' come from the
base skill sap-btp-solution-diagrams (Azure icons for hyperscaler content).
"""
import sys, os, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bigpicture
import btpdiagram

LIBS = {"btp": bigpicture.OFFICIAL["btp"], "generic": bigpicture.OFFICIAL["generic"],
        "sap": btpdiagram.ICONS["sap"], "azure": btpdiagram.ICONS["azure"]}
ap = argparse.ArgumentParser()
ap.add_argument("terms", nargs="*")
ap.add_argument("--lib", choices=list(LIBS))
ap.add_argument("--list", choices=list(LIBS))
a = ap.parse_args()
m = bigpicture.ICON_MANIFEST
print(f"# official set: commit {m.get('commit', '?')[:8]} ({m.get('commit_date', '?')[:10]}) from {bigpicture.ICON_DIR}")
for lib in ([a.list] if a.list else [a.lib] if a.lib else list(LIBS)):
    for name, v in sorted(LIBS[lib].items()):
        if a.list or all(t.lower() in (name + " " + v.get("category", "")).lower() for t in a.terms):
            print(f"{lib}:{name}" + (f"   [{v['category']}]" if v.get("category") else ""))
