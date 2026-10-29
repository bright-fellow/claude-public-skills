"""Rebuild assets/sap_official_icons.json from the official SAP BTP Solution Diagrams repository
(https://github.com/SAP/btp-solution-diagrams, Apache-2.0) - the icon set documented at
https://sap.github.io/btp-solution-diagrams/docs/btp_guideline/diagr_comp/icons/

    python update_icons.py --check     # freshness check: compare upstream HEAD with the icon set in use (fast,
                                       # no download) and refresh automatically if upstream has moved
    python update_icons.py             # force a refresh from GitHub
    python update_icons.py --repo /path/to/btp-solution-diagrams   # build from an existing checkout
    python update_icons.py --bundle    # write into the skill's own assets/ (maintainers; skill folder must be writable)

Where the refreshed set goes: the skill folder is often read-only once installed, so refreshes are written to
a cache ($BIGPICTURE_ICON_CACHE or ~/.cache/sap-btp-big-picture/). bigpicture.py loads whichever set is newer
(cache or bundled) and falls back to the bundled set when offline. Every set carries a manifest with the
upstream commit, so a refresh prints which icons were added, removed or redrawn.

Takes the size-M draw.io libraries: every service icon set (foundational, integration suite, app dev &
automation, data & analytics, AI, BTP SaaS, "all") plus the generic icons (SAP / Non-SAP / Highlight).
"""
import json, re, os, sys, glob, html, base64, urllib.parse, subprocess, tempfile
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_URL = "https://github.com/SAP/btp-solution-diagrams.git"
BUNDLED = os.path.normpath(os.path.join(HERE, "..", "assets"))
CACHE = os.environ.get("BIGPICTURE_ICON_CACHE") or os.path.expanduser("~/.cache/sap-btp-big-picture")
ICONS_FILE, MANIFEST = "sap_official_icons.json", "icons_manifest.json"
CATS = {"00": "Foundational", "01": "Integration Suite", "02": "App Dev & Automation", "04": "Data & Analytics",
        "05": "AI", "06": "BTP SaaS", "99": "Other service"}
FIX = {  # file slugs whose automatic title-casing reads badly
    "sap-btp_abap-environment": "SAP BTP, ABAP environment",
    "sap-business-ai-platform_abab_environment_sd": "SAP BTP, ABAP environment",  # upstream rename (Oct 2026), typo is SAP's
    "sap-btp-cloud-foundry-runtime": "SAP BTP, Cloud Foundry runtime", "sap-btp_cloud-foundry-runtime": "SAP BTP, Cloud Foundry runtime",
    "sap-btp_kyma-runtime": "SAP BTP, Kyma runtime", "sap-identity-provisoning": "SAP Identity Provisioning",
    "joule studio": "Joule Studio", "sap-business-accelerator- hub": "SAP Business Accelerator Hub",
    "sap-s4hana-for-microsoft-teams": "SAP S/4HANA for Microsoft Teams", "oauth-20-on-sap-btp": "OAuth 2.0 on SAP BTP",
    "sap-cloud-alm": "SAP Cloud ALM", "api-management": "API Management", "sap-ai-core": "SAP AI Core",
    "sap-ai-launchpad": "SAP AI Launchpad", "cloud-connector": "Cloud Connector", "sap-ui-theme-designer": "SAP UI Theme Designer",
    "sap-cloud-application-programming-model": "SAP Cloud Application Programming Model",
    "sap-build-work-zone advanced-edition": "SAP Build Work Zone, advanced edition",
    "sap-html5-application-repository-service-for-sap-btp": "SAP HTML5 Application Repository service",
    "sap-s4hana-cloud-for-intelligent-intercompany-reconciliation": "SAP S/4HANA Cloud for intelligent intercompany reconciliation",
}
SMALL = {"and", "for", "of", "on", "as", "a", "the", "to", "with"}
UP = {"sap": "SAP", "btp": "BTP", "api": "API", "abap": "ABAP", "ai": "AI", "ui5": "UI5", "pki": "PKI", "fhir": "FHIR",
      "ase": "ASE", "gui": "GUI", "alm": "ALM", "hana": "HANA", "s4hana": "S/4HANA", "html5": "HTML5"}


def load(f):
    s = open(f, encoding="utf-8").read()
    body = re.search(r"<mxlibrary>(.*)</mxlibrary>", s, re.S).group(1)
    return json.loads(re.sub(r"<!--.*?-->", "", body, flags=re.S))


def entries(f):
    """(file title, image data URI) for every image shape in a draw.io library."""
    out = []
    for e in load(f):
        title = e.get("title") or ""
        if "xml" in e:
            x = e["xml"]
            root = ET.fromstring(html.unescape(x) if x.lstrip().startswith("&lt;") else x)
            for c in root.iter("mxCell"):
                m = re.search(r"image=(data:image/[^;,]+(?:;base64)?,[^;]*)", c.get("style") or "")
                if m:
                    out.append((title or (c.get("value") or ""), m.group(1)))
                    break
        elif e.get("data"):
            out.append((title, e["data"]))
    return out


def clean_data(data):
    head, _, body = data.partition(",")
    mime = head[5:].split(";")[0]
    if ";base64" in head or re.fullmatch(r"[A-Za-z0-9+/=\s]+", body[:300]):
        b = re.sub(r"\s", "", body)
        raw = base64.b64decode(b + "=" * (-len(b) % 4))
    else:
        raw = urllib.parse.unquote(body).encode()
    # draw.io's own data-URI form (no ';base64' marker) for SVG, standard form for PNG
    return (f"data:{mime}," if mime == "image/svg+xml" else f"data:{mime};base64,") + base64.b64encode(raw).decode()


def service_name(raw):
    m = re.match(r"(\d+)-(.*?)(?:[_ ]sd)?(?:\.svg)?$", raw.strip())
    if not m:
        bare = re.sub(r"(?:[_ ]sd)?(?:\.svg)?$", "", raw.strip())
        return FIX.get(bare) or FIX.get(bare + "_sd") or re.sub(r"\s+", " ", raw).strip(), None
    sid, slug = m.groups()
    slug = slug.replace("sap-cloud-identity_", "")
    if slug in FIX:
        return FIX[slug], sid
    ws = re.split(r"[- _]+", slug)
    return " ".join(UP.get(w.lower()) or (w if i and w in SMALL else w[:1].upper() + w[1:]) for i, w in enumerate(ws)), sid


def generic_name(raw):
    n = re.sub(r"[- ]?Size [SM]$", "", raw.strip()).strip(" -")
    if n == "AI Agent M":
        return "AI Agent (SAP)"
    m = re.match(r"(.*?)[ -](Highlight|Non-SAP|SAP)$", n)
    return f"{m.group(1)} ({m.group(2)})" if m else n


def read_manifest(folder):
    try:
        return json.load(open(os.path.join(folder, MANIFEST)))
    except (OSError, ValueError):
        return {}


def active_set():
    """(folder, manifest) of the icon set bigpicture.py will load: the newer of cache and bundled."""
    best = (BUNDLED, read_manifest(BUNDLED))
    cm = read_manifest(CACHE)
    if cm and os.path.exists(os.path.join(CACHE, ICONS_FILE)) and cm.get("commit_date", "") > best[1].get("commit_date", ""):
        best = (CACHE, cm)
    return best


def remote_head():
    r = subprocess.run(["git", "ls-remote", REPO_URL, "HEAD"], capture_output=True, text=True, timeout=60)
    if r.returncode != 0 or not r.stdout:
        raise RuntimeError(r.stderr.strip() or "git ls-remote returned nothing")
    return r.stdout.split()[0]


def build(repo, out_dir):
    lib = os.path.join(repo, "assets", "shape-libraries-and-editable-presets", "draw.io")
    icons = {}
    for f in sorted(glob.glob(os.path.join(lib, "20-02-*", "*-02-*size-M.xml"))):
        cat = CATS.get(os.path.basename(os.path.dirname(f)).split("-")[2], "Other service")
        for raw, data in entries(f):
            name, sid = service_name(raw)
            if name not in icons:
                icons[name] = {"data": clean_data(data), "category": cat, "id": sid, "source": raw}
            elif icons[name]["category"] == "Other service" and cat != "Other service":
                icons[name]["category"] = cat
    for f in glob.glob(os.path.join(lib, "20-03-generic-icons", "*size-M*.xml")):
        for raw, data in entries(f):
            icons.setdefault(generic_name(raw), {"data": clean_data(data), "category": "Generic", "source": raw})
    git = lambda *a: subprocess.run(["git", "-C", repo, *a], capture_output=True, text=True).stdout.strip()
    manifest = {"source": REPO_URL, "commit": git("rev-parse", "HEAD") or "unknown",
                "commit_date": git("log", "-1", "--format=%cI") or "", "icon_count": len(icons),
                "license": "Apache-2.0 (SAP SE and btp-solution-diagrams contributors)"}
    # diff against the set currently in use
    old_dir, old_m = active_set()
    try:
        old = json.load(open(os.path.join(old_dir, ICONS_FILE)))
    except (OSError, ValueError):
        old = {}
    os.makedirs(out_dir, exist_ok=True)
    json.dump(icons, open(os.path.join(out_dir, ICONS_FILE), "w"))
    json.dump(manifest, open(os.path.join(out_dir, MANIFEST), "w"), indent=2)
    cats = {}
    for v in icons.values():
        cats[v["category"]] = cats.get(v["category"], 0) + 1
    print(f"wrote {len(icons)} icons (commit {manifest['commit'][:8]}, {manifest['commit_date'][:10]}) to {out_dir}: {cats}")
    if old:
        added = sorted(set(icons) - set(old))
        removed = sorted(set(old) - set(icons))
        changed = sorted(k for k in set(icons) & set(old) if icons[k]["data"] != old[k]["data"])
        print(f"vs previous set ({old_m.get('commit', '?')[:8]}): +{len(added)} new, -{len(removed)} removed, "
              f"{len(changed)} redrawn")
        for label, lst in (("NEW", added), ("REMOVED", removed), ("REDRAWN", changed)):
            if lst:
                print(f"  {label}: " + ", ".join(lst))
        if removed:
            print("  -> icon keys used in layout scripts may need updating (bigpicture warns on unknown keys).")


def fetch(out_dir):
    tmp = tempfile.mkdtemp()
    subprocess.run(["git", "clone", "-q", "--depth", "1", "--filter=blob:none", "--sparse", REPO_URL, tmp], check=True)
    subprocess.run(["git", "-C", tmp, "sparse-checkout", "set", "assets"], check=True)
    build(tmp, out_dir)


def check():
    folder, m = active_set()
    where = "bundled" if folder == BUNDLED else "cache"
    print(f"icon set in use: {where} - commit {m.get('commit', '?')[:8]} from {m.get('commit_date', '?')[:10]}, "
          f"{m.get('icon_count', '?')} icons")
    try:
        head = remote_head()
    except Exception as e:  # offline / proxy blocked: keep working with what we have
        print(f"could not reach GitHub ({e}); continuing with the {where} set")
        return
    if head == m.get("commit"):
        print("up to date with github.com/SAP/btp-solution-diagrams")
    else:
        print(f"upstream has moved to {head[:8]} - refreshing into {CACHE}")
        fetch(CACHE)


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--check" in args:
        check()
    elif "--repo" in args:
        build(args[args.index("--repo") + 1], BUNDLED if "--bundle" in args else CACHE)
    else:
        fetch(BUNDLED if "--bundle" in args else CACHE)
