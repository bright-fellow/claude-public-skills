import sys
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from btpdiagram import Diagram
out = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/outputs/diagram-L1-overview"
d = Diagram(1580, 900, "Highly available integration with SAP Integration Suite – overview",
            "High-level view (L1): main building blocks and integrations · details in the L2 deep dive")

d.box(40, 120, 300, 80, ["SAP S/4HANA Cloud", "Public Edition"], kind="sap")
d.area(380, 110, 340, 110, "pink", "Identity & access")
d.icon("sap:Identity Authentication", 430, 148, 32, label=["SAP Cloud Identity", "Services"], label_w=130)
d.icon("azure:Enterprise Applications", 628, 148, 32, label=["Microsoft", "Entra ID"], label_w=110)
d.edge([(466, 164), (624, 164)], "trust")
d.box(760, 120, 300, 80, ["Salesforce", "Sales Cloud"])

d.box(40, 250, 220, 60, ["Global entry", "Azure Front Door"], icon="azure:Front Door and CDN Profiles")
d.edge([(150, 202), (150, 248)])
d.num(172, 225, 1)
d.edge([(150, 312), (150, 358)])
d.edge([(300, 358), (300, 202)])                     # outbound to S/4HANA APIs
d.edge([(550, 222), (550, 358)], "trust")
d.num(572, 290, "A")
d.edge([(910, 358), (910, 202)], start=True)          # Salesforce APIs / events
d.num(932, 280, 2)

d.area(40, 360, 1020, 170, "btp", "SAP Integration Suite", "Two SAP BTP regions · identical content")
d.box(80, 420, 400, 80, ["Primary region", "Active tenant"], kind="sap", icon="sap:SAP Integration Suite")
d.box(620, 420, 400, 80, ["Secondary region", "Active or hot standby"], kind="sap", icon="sap:SAP Integration Suite")
d.edge([(482, 460), (618, 460)], "async")

d.area(40, 580, 1020, 110, "nonsap", "Microsoft Azure", "Customer hub network")
d.box(300, 612, 500, 64, ["Secure connectivity", "SAP Cloud Connector (HA pair) · firewall"], kind="sap", icon="sap:Cloud Connector")
d.edge([(550, 532), (550, 610)], start=True)
d.num(572, 560, 3)

d.box(40, 740, 1020, 70, ["SAP ERP (ECC 6.0 on NetWeaver 7.5)", "RISE with SAP · SAP-managed on Azure · HA across zones"], kind="sap")
d.edge([(550, 678), (550, 738)], start=True)

d.flow_panel(1100, 110, 440, 440, [
    ("A", ["Developers and admins sign in via SAP Cloud", "Identity Services, which proxies Microsoft", "Entra ID."]),
    ["S/4HANA reaches Integration Suite through one", "global entry (Azure Front Door); Integration", "Suite calls S/4HANA APIs directly."],
    ["Integration Suite exchanges data and events with", "Salesforce via its APIs."],
    ["ECC in RISE is connected through the Cloud", "Connector HA pair in the customer's Azure hub;", "either region can reach it."],
])
d.legend(1100, 570, labels={"async": "Content deployment (transport / CI-CD)"})
d.footer("L1", "Deep dive (L2): integration-suite-ha-azure-rise-L2-deep-dive.drawio")
d.save(out, name="Integration Suite HA – overview (L1)")
