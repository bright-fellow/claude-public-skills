import sys
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from btpdiagram import Diagram
out = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/outputs/diagram-L1-overview"
d = Diagram(1580, 780, "CMIS archive with easy archive on Microsoft Azure – overview",
            "High-level view (L1): main building blocks and integrations · details in the L2 deep dive")

d.icon("sap:End User", 40, 232, 36)
d.text(18, 272, ["Business", "users"], size=11, align="center", w=80, lh=13)
d.edge([(80, 250), (118, 250)])
d.box(120, 200, 220, 100, ["SAP S/4HANA Cloud", "Public Edition", "Document attachments"], kind="sap")
d.num(330, 202, 1)

d.area(380, 150, 270, 200, "btp", "SAP BTP", "Subaccount")
d.service(452, 200, 125, 130, "sap:SAP Document Management service", ["SAP Document", "Management service"])
d.edge([(342, 250), (450, 250)])

d.area(700, 150, 400, 330, "nonsap", "Microsoft Azure", "Customer subscription")
d.box(720, 210, 360, 70, ["easy archive (CMIS repository)", "Active-active across two availability zones"])
d.box(720, 300, 360, 70, ["Immutable archive storage", "WORM · zone-redundant · backup"])
d.box(720, 390, 360, 70, ["Disaster recovery", "Paired Azure region (optional)"], kind="ops")
d.edge([(579, 245), (718, 245)])
d.pill(648, 245, "CMIS 1.1 · tunnel")
d.num(648, 270, 2)
d.edge([(900, 280), (900, 298)])
d.num(1090, 302, 3)
d.edge([(900, 370), (900, 388)], "async")

d.area(120, 540, 980, 150, "pink", "Identity & access", "Single sign-on for all services")
d.box(160, 600, 360, 64, ["SAP Cloud Identity Services", "Identity Authentication (proxy IdP)"], kind="sap", icon="sap:Identity Authentication")
d.box(700, 600, 360, 64, ["Microsoft Entra ID", "Corporate IdP · groups → roles"], icon="azure:Enterprise Applications")
d.edge([(522, 632), (698, 632)], "trust")
d.edge([(310, 302), (310, 598)], "trust")
d.edge([(515, 352), (515, 598)], "trust")
d.num(1086, 542, "A")

d.flow_panel(1140, 110, 400, 420, [
    ("A", ["Users sign in once: SAP Cloud Identity", "Services proxies Microsoft Entra ID for", "S/4HANA and SAP BTP."]),
    ["S/4HANA stores document attachments via", "SAP Document Management service."],
    ["DMS writes them to easy archive on Azure", "over CMIS through a secure tunnel."],
    ["easy archive keeps them in immutable,", "zone-redundant storage; a paired region", "provides optional disaster recovery."],
])
d.legend(1140, 550, w=400)
d.footer("L1", "Deep dive (L2): easy-archive-cmis-ha-azure-L2-deep-dive.drawio")
d.save(out, name="easy archive CMIS – overview (L1)")
