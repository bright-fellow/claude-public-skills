import sys
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from btpdiagram import Diagram

out = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/outputs/integration-suite-ha-azure-rise"
d = Diagram(1700, 1540,
            "Highly available integration with SAP Integration Suite on Azure – S/4HANA Cloud, Salesforce and ECC in RISE",
            "SAP Integration Suite (two regions)  ·  Azure Front Door  ·  SAP Cloud Connector HA pair on Azure  ·  RISE with SAP (ECC 6.0 on NetWeaver 7.5)  ·  IAS + Microsoft Entra ID")

# ---------------- row 1: SaaS endpoints + identity ----------------
d.area(40, 110, 360, 150, "sap", "SAP S/4HANA Cloud", "Public Edition (SAP-managed SaaS)")
d.box(56, 176, 328, 68, ["Communication arrangements", "OData v4 / SOAP APIs · business events", "OAuth 2.0 client credentials / X.509"], kind="sap_fill")

d.area(440, 110, 320, 150, "nonsap", "Salesforce", "Sales Cloud (SaaS)")
d.box(456, 176, 288, 68, ["Salesforce APIs", "REST / SOAP / Bulk · Pub/Sub API", "OAuth 2.0 JWT bearer (connected app)"])

d.area(800, 110, 380, 150, "pink", "Identity & access", "IAS proxies Microsoft Entra ID")
d.icon("sap:Identity Authentication", 862, 172, 36, label=["Identity Authentication", "(proxy IdP)"], label_w=150)
d.icon("azure:Enterprise Applications", 1082, 172, 36, label=["Microsoft Entra ID", "enterprise application"], label_w=150)
d.edge([(902, 190), (1078, 190)], "trust")
d.num(1166, 112, "A")

# ---------------- row 2: global entry + transport ----------------
d.box(40, 300, 240, 64, ["Azure Front Door", "Custom domain · health probes", "Priority / weighted routing"],
      icon="azure:Front Door and CDN Profiles")
d.edge([(120, 262), (120, 298)])                       # S/4HANA -> Front Door (inbound to iFlows)
d.num(142, 280, 1)
d.num(268, 302, 2)

d.box(800, 300, 380, 64, ["SAP Cloud Transport Management", "CI/CD (Git): same iFlows, keystores and", "credentials deployed to both tenants"],
      kind="sap", icon="sap:SAP Cloud Transport Management")
d.num(1166, 302, 8)

# Front Door -> both tenants
d.edge([(120, 366), (120, 438)])
d.edge([(260, 366), (260, 420), (700, 420), (700, 438)])
# transport -> both tenants
d.edge([(990, 366), (990, 438)], "async")
d.edge([(798, 332), (560, 332), (560, 438)], "async")
# outbound calls from the active tenant
d.edge([(340, 438), (340, 262)])
d.pill(340, 385, "OData / SOAP")
d.num(362, 318, 3)
d.edge([(480, 438), (480, 262)])
d.pill(480, 385, "REST · Pub/Sub API")
d.num(502, 318, 4)

# ---------------- row 3: SAP BTP regions ----------------
def region(x0, title, sub, note):
    d.area(x0, 440, 550, 320, "btp", title, sub)
    d.service(x0 + 20, 505, 125, 130, "sap:SAP Integration Suite", ["SAP Integration Suite", "Cloud Integration ·", "API Management"])
    d.service(x0 + 200, 505, 125, 130, "sap:SAP Alert Notification service", ["SAP Alert", "Notification service"])
    d.service(x0 + 380, 505, 125, 130, "sap:SAP Connectivity service", ["SAP Connectivity", "service"])
    d.box(x0 + 20, 655, 340, 85, note, kind="sap_fill")

region(40, "SAP BTP – primary region", "Integration Suite tenant · active · multi-AZ (SAP-managed)",
       ["Stateful artefacts are per tenant", "JMS queues · data stores · variables", "Drain / replay on failover"])
region(630, "SAP BTP – secondary region", "Integration Suite tenant · active or hot standby",
       ["Identical content via transport / CI-CD", "Own tenant URL behind Front Door", "Same Cloud Connector location ID"])

# tunnels from both subaccounts to the Cloud Connector HA pair
d.edge([(482, 637), (482, 785), (300, 785), (300, 948)], start=True)
d.edge([(1072, 637), (1072, 800), (330, 800), (330, 948)], start=True)
d.pill(760, 822, "TLS tunnels (opened outbound by CC)")
d.num(875, 822, 5)

# ---------------- row 4: customer Azure hub ----------------
d.area(40, 840, 1140, 305, "nonsap", "Microsoft Azure – customer hub subscription",
       "Hub VNet · region e.g. West Europe · availability zones")
d.area(60, 900, 310, 135, "teal", "Availability zone 1")
d.area(400, 900, 310, 135, "teal", "Availability zone 2")
d.box(80, 950, 270, 64, ["SAP Cloud Connector – master", "Azure VM · active"], kind="sap", icon="sap:Cloud Connector")
d.box(420, 950, 270, 64, ["SAP Cloud Connector – shadow", "Azure VM · takes over automatically"], kind="sap", icon="sap:Cloud Connector")
d.edge([(350, 982), (420, 982)], "heartbeat")
d.box(740, 900, 420, 60, ["Azure Monitor + SAP Cloud ALM", "CC health · tunnel status · iFlow alerts"], icon="azure:Monitor")
d.box(740, 972, 420, 60, ["Azure Key Vault", "CC certificates · OAuth secrets · rotation"], icon="azure:Key Vaults")
d.box(60, 1060, 1100, 64, ["Azure Firewall (zone-redundant) in the hub VNet",
                           "Egress to SAP BTP and Front Door (FQDN rules) · UDRs to RISE via VNet peering"], icon="azure:Firewalls")
d.edge([(215, 1016), (215, 1058)])
d.edge([(555, 1016), (555, 1058)])

# ECC outbound (IDoc / SOAP) goes to the Front Door endpoint, never to a tenant URL
d.edge([(60, 1092), (24, 1092), (24, 332), (38, 332)])
d.num(24, 760, 7)

# ---------------- row 5: RISE ----------------
d.edge([(610, 1126), (610, 1198)], start=True)
d.pill(610, 1172, "VNet peering · RFC / IDoc / SOAP")
d.num(725, 1172, 6)
d.area(40, 1200, 1140, 270, "sap", "RISE with SAP – SAP ERP (ECC 6.0 EHP8 on NetWeaver 7.5)",
       "SAP-managed Azure subscription (SAP ECS) · HA / DR per RISE contract")
d.box(60, 1256, 1100, 56, ["SAP Web Dispatcher / message server (SAP-managed)",
                           "RFC load balancing via logon groups · HTTPS for SOAP and IDoc-XML"], kind="sap_fill")
d.area(60, 1330, 540, 125, "teal", "Availability zone 1")
d.area(640, 1330, 520, 125, "teal", "Availability zone 2")
d.box(80, 1370, 240, 64, ["ABAP application servers", "PAS · ASCS (clustered)"], kind="sap")
d.box(350, 1370, 230, 64, ["Database – primary", "SAP-managed HA"], kind="sap")
d.box(660, 1370, 230, 64, ["Database – secondary", "Synchronous replication"], kind="sap")
d.box(920, 1370, 220, 64, ["ABAP application servers", "AAS · ERS"], kind="sap")
d.edge([(280, 1314), (280, 1368)])
d.edge([(1030, 1314), (1030, 1368)])
d.edge([(320, 1402), (348, 1402)])
d.edge([(920, 1402), (892, 1402)])
d.edge([(582, 1402), (658, 1402)], "sync")

# ---------------- flow panel + legend ----------------
h = d.flow_panel(1220, 110, 440, 710, [
    "# Identity & access",
    ("A", ["Developers and admins sign in via IAS, which", "proxies Microsoft Entra ID; Entra groups map to", "Integration Suite role collections in both", "subaccounts. Technical OAuth clients / certificates", "are not federated."]),
    "# Message flow",
    ["S/4HANA Cloud sends events and outbound calls to", "the iFlow endpoints on the Front Door custom", "domain."],
    ["Front Door probes both tenants and routes to a", "healthy one: priority = active/standby, weighted =", "active-active for stateless iFlows."],
    ["The active tenant calls S/4HANA APIs directly", "(OData / SOAP) with the communication", "arrangement's OAuth client or X.509 certificate."],
    ["The Salesforce adapter calls REST / SOAP / Bulk", "APIs and subscribes to events via the Pub/Sub", "API (OAuth 2.0 JWT bearer)."],
    ["Calls to ECC use SAP Connectivity service and the", "Cloud Connector tunnel; both subaccounts are", "registered on the same HA pair (location ID)."],
    ["The Cloud Connector reaches ECC through the Azure", "Firewall and VNet peering into the RISE VNet", "(RFC via logon groups, IDoc, SOAP)."],
    ["ECC sends IDocs / SOAP messages via the Azure", "Firewall to the Front Door endpoint, so a region", "failover needs no change in ECC."],
    ["Transport management / CI-CD keeps both tenants", "identical; stateful artefacts (JMS, data stores)", "stay per tenant and are drained on failover."],
])
d.legend(1220, 840, labels={"async": "Content deployment (transport / CI-CD)"})
d.footer("L2", "RISE HA/DR options, Integration Suite availability in the chosen BTP regions and multi-tenant licensing to be confirmed with SAP.")
d.save(out, name="Integration Suite HA – S/4HANA Cloud, Salesforce, ECC in RISE on Azure")
