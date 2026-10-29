"""Search the bundled icon libraries.

    python find_icon.py storage            # search both libraries
    python find_icon.py sql --lib azure    # only Azure
    python find_icon.py --list sap         # list every SAP BTP icon
    python find_icon.py --categories       # list Azure categories

Use the printed key (e.g. azure:Storage Accounts) with Diagram.icon()/box(icon=...)/service().
"""
import sys, argparse
sys.path.insert(0, __import__("os").path.dirname(__file__))
from btpdiagram import ICONS

ap = argparse.ArgumentParser()
ap.add_argument("terms", nargs="*")
ap.add_argument("--lib", choices=["sap", "azure"])
ap.add_argument("--list", choices=["sap", "azure"])
ap.add_argument("--categories", action="store_true")
a = ap.parse_args()

if a.categories:
    cats = {}
    for v in ICONS["azure"].values():
        cats[v["category"]] = cats.get(v["category"], 0) + 1
    for c, n in sorted(cats.items()):
        print(f"{c:30s} {n}")
    sys.exit()
libs = [a.list] if a.list else ([a.lib] if a.lib else ["sap", "azure"])
for lib in libs:
    for name, v in sorted(ICONS[lib].items()):
        if a.list or all(t.lower() in (name + " " + v.get("category", "")).lower() for t in a.terms):
            print(f"{lib}:{name}" + (f"   [{v['category']}]" if "category" in v else ""))
