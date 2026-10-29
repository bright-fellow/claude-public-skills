"""Worked example: CMIS archive (easy archive) for SAP S/4HANA Cloud Public Edition,
active-active across two Azure availability zones, with DR to the paired region.
Run:  python examples/easy_archive_cmis_ha_azure.py [output_base]"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts"))
from btpdiagram import Diagram

out = sys.argv[1] if len(sys.argv) > 1 else "/mnt/user-data/outputs/easy-archive-cmis-ha-azure"
d = Diagram(1700, 1630,
            "CMIS-compliant archive with easy archive on Microsoft Azure – active-active high availability",
            "SAP S/4HANA Cloud Public Edition  ·  SAP Document Management service  ·  SAP Cloud Identity Services with Microsoft Entra ID  ·  easy archive CMIS Service  ·  Azure availability zones")

# ---- user + S/4HANA ----
d.icon("sap:End User", 40, 185, 36)
d.text(20, 226, ["Business", "user"], size=11, align="center", w=76, lh=13)
d.edge([(80, 203), (108, 203)])
d.num(94, 170, 1)
d.area(110, 110, 230, 220, "sap", "SAP S/4HANA Cloud", "Public Edition")
d.box(126, 176, 198, 60, ["Attachment service", "Storage category SCP-DM.100"], kind="sap_fill")
d.box(126, 250, 198, 60, ["Communication arrangement", "Outbound OAuth 2.0 to DMS"], kind="sap_fill")

# ---- SAP BTP ----
d.area(380, 110, 640, 220, "btp", "SAP BTP", "Subaccount · e.g. region EU10")
d.service(400, 175, 125, 130, "sap:SAP Document Management service", ["SAP Document", "Management service,", "integration option"])
d.service(557, 175, 125, 130, "sap:SAP Connectivity service", ["SAP Connectivity", "service"])
d.service(714, 175, 125, 130, "sap:SAP Destination service", ["SAP Destination", "service"])
d.service(871, 175, 125, 130, "sap:SAP Authorization and Trust Management service", ["SAP Authorization", "and Trust", "Management"])
d.edge([(324, 280), (360, 280), (360, 240), (398, 240)])
d.num(362, 212, 2)
d.edge([(525, 240), (555, 240)])
d.num(541, 218, 3)

# ---- Identity: SAP Cloud Identity Services (IAS) proxies Microsoft Entra ID ----
d.area(40, 370, 560, 190, "btp", "SAP Cloud Identity Services")
d.box(56, 420, 196, 120, ["Role mapping in IAS", "Entra group / app role", "→ IAS user group", "→ BTP role collection",
                          "→ S/4HANA business role"], kind="sap_fill")
d.service(290, 415, 125, 130, "sap:Identity Authentication", ["Identity", "Authentication", "(proxy IdP)"])
d.service(460, 415, 125, 130, "sap:Identity Provisioning", ["Identity", "Provisioning"])
d.edge([(320, 332), (320, 413)], "trust")          # S/4HANA trusts IAS
d.edge([(400, 332), (400, 413)], "trust")          # BTP subaccount trusts IAS
d.num(298, 352, "A")
d.edge([(458, 490), (417, 490)])                   # IPS -> IAS users/groups
d.num(583, 415, "D")

d.area(640, 370, 540, 190, "nonsap", "Microsoft Entra ID", "Corporate identity provider (Microsoft tenant)")
for cx, key, label in [(707, "azure:Enterprise Applications", ["Enterprise application", "SAP Cloud Identity Services"]),
                       (842, "azure:Groups", ["Security groups", "(role source)"]),
                       (977, "azure:App Registrations", ["App registration", "app roles → claims"]),
                       (1112, "azure:Multi Factor Authentication", ["Multifactor authentication", "Conditional Access"])]:
    d.icon(key, cx - 18, 425, 36, label=label, label_w=132)
d.num(1166, 372, "C")
d.edge([(638, 460), (587, 460)])                   # Entra -> IPS (Microsoft Graph)
d.edge([(352, 547), (352, 580), (707, 580), (707, 562)], "trust")   # IAS <-> Entra federation
d.pill(520, 580, "SAML 2.0 / OIDC · group & role claims")
d.num(730, 580, "B")

# tunnel from SAP Connectivity service to the Cloud Connector in Azure (passes between the identity areas)
d.edge([(619, 307), (619, 678)], start=True)
d.pill(619, 350, "TLS tunnel (outbound from CC)")
d.num(724, 350, 4)

with d.shift(0, 230):
    # ---- Microsoft Azure ----
    d.area(40, 380, 1140, 940, "nonsap", "Microsoft Azure",
           "Customer subscription · region e.g. West Europe · spoke virtual network across availability zones")

    # operations & protection
    d.box(60, 450, 340, 100, [], kind="nonsap")
    d.text(74, 458, ["Operations & protection"], size=12, bold=True)
    for cx, key, label in [(102, "azure:Monitor", ["Azure Monitor"]),
                           (187, "azure:Log Analytics Workspaces", ["Log Analytics", "workspace"]),
                           (272, "azure:Key Vaults", ["Azure", "Key Vault"]),
                           (357, "azure:Backup Vault", ["Backup vault", "(immutable)"])]:
        d.icon(key, cx - 16, 478, 32, label=label, label_w=84)

    # cloud connector pair on Azure VMs
    d.box(430, 450, 380, 100, [], kind="nonsap")
    d.text(444, 458, ["SAP Cloud Connector (HA pair)"], size=12, bold=True)
    d.icon("sap:Cloud Connector", 500, 480, 34, label=["Master (active)", "Azure VM · zone 1"], label_w=150)
    d.icon("sap:Cloud Connector", 686, 480, 34, label=["Shadow (standby)", "Azure VM · zone 2"], label_w=150)
    d.edge([(538, 497), (682, 497)], "heartbeat")

    d.box(850, 450, 310, 100, ["easy applications / CMIS clients", "easy invoice · easy contract · easy hr",
                               "On-prem via ExpressRoute / VPN"], kind="nonsap")
    d.num(1150, 452, 8)


    # load balancer
    d.box(60, 590, 1100, 64, ["Azure Load Balancer (Standard, internal)", "Zone-redundant frontend IP · health probes · no session affinity"],
          kind="nonsap", icon="azure:Load Balancers")
    d.edge([(620, 550), (620, 588)]); d.pill(620, 569, "CMIS 1.1 · HTTPS")
    d.edge([(1005, 550), (1005, 588)]); d.pill(1005, 569, "CMIS 1.1 · HTTPS")
    d.num(90, 590, 5)

    # zones
    d.area(60, 690, 520, 310, "teal", "Availability zone 1 – active")
    d.area(640, 690, 520, 310, "teal", "Availability zone 2 – active")
    VM, SQLVM = "azure:Virtual Machine", "azure:Azure SQL VM"
    d.box(75, 740, 230, 64, ["easy archive CMIS Service", "Azure VM · stateless"], icon=VM)
    d.box(335, 740, 230, 64, ["easy archive server", "Azure VM · active"], icon=VM)
    d.box(655, 740, 230, 64, ["easy archive server", "Azure VM · active"], icon=VM)
    d.box(915, 740, 230, 64, ["easy archive CMIS Service", "Azure VM · stateless"], icon=VM)
    d.box(335, 840, 230, 64, ["Metadata DB (primary)", "SQL Server AG on Azure VM", "Writes via AG listener"], icon=SQLVM)
    d.box(655, 840, 230, 64, ["Metadata DB (secondary)", "SQL Server AG on Azure VM", "Sync commit · auto-failover"], icon=SQLVM)
    d.box(75, 840, 230, 140, ["Singleton jobs – leader", "Retention expiry & deletion", "Indexing / OCR", "Leader election via DB lock"], kind="ops")
    d.box(915, 840, 230, 140, ["Singleton jobs – follower", "Takes over leadership", "when zone 1 fails"], kind="ops")

    d.edge([(190, 654), (190, 738)])
    d.edge([(1030, 654), (1030, 738)])
    d.edge([(305, 772), (333, 772)])
    d.edge([(915, 772), (887, 772)])
    d.num(553, 740, 6)
    d.edge([(450, 804), (450, 838)])
    d.edge([(770, 804), (770, 838)])
    d.edge([(565, 872), (655, 872)], "sync")
    d.num(610, 848, 7)
    # archive -> blob via private endpoints (side lanes)
    d.edge([(335, 790), (320, 790), (320, 1065), (333, 1065)])
    d.edge([(885, 790), (900, 790), (900, 1065), (887, 1065)])

    # zone-redundant storage, witness, backup
    d.box(335, 1030, 550, 70, ["Azure Blob Storage – immutable (WORM)", "Zone-redundant storage (ZRS): synchronous across 3 zones",
                               "Locked time-based retention + legal hold · private endpoints"], icon="azure:Storage Accounts")
    d.box(915, 1030, 245, 70, ["Cloud witness", "Storage account (ZRS)", "Quorum for SQL Server AG"], icon="azure:Storage Accounts")
    d.edge([(1030, 1028), (1030, 1002)], "heartbeat")
    d.box(60, 1030, 245, 70, ["Azure Backup", "Immutable Backup vault", "VM & SQL backups"], icon="azure:Backup Vault")
    d.edge([(190, 1002), (190, 1028)], "backup")

    # DR region
    d.edge([(610, 1100), (610, 1138)], "async")
    d.pill(610, 1119, "Async geo-replication · GZRS · AG async replica · ASR")
    d.area(60, 1140, 1100, 160, "dashed", "Paired Azure region – disaster recovery (optional)",
           "Asynchronous, RPO > 0 · activated manually after a regional outage")
    d.box(80, 1210, 340, 70, ["Blob Storage secondary", "GZRS / RA-GZRS geo-replica"], icon="azure:Storage Accounts")
    d.box(440, 1210, 340, 70, ["SQL Server AG async replica", "Azure SQL VM · manual failover"], icon=SQLVM)
    d.box(800, 1210, 340, 70, ["Azure Site Recovery", "Recovery Services vault", "Replicates app-tier VMs"], icon="azure:Recovery Services Vaults")

# flow panel + legend
d.flow_panel(1220, 110, 440, 940, [
    "# Identity & access",
    ("A", ["SAP S/4HANA and the SAP BTP subaccount trust", "SAP Cloud Identity Services – Identity", "Authentication (IAS), which proxies all logins."]),
    ("B", ["IAS forwards authentication to Microsoft Entra ID", "(SAML 2.0 / OIDC); Entra enforces MFA and", "Conditional Access – one SSO for all services."]),
    ("C", ["Entra sends security-group / app-role claims;", "IAS maps them to IAS user groups, which grant", "BTP role collections and S/4HANA business roles."]),
    ("D", ["Identity Provisioning reads users and groups from", "Entra ID (Microsoft Graph) and provisions them to", "IAS and S/4HANA business users."]),
    "# Document archiving",
    ["A business user attaches a document in SAP S/4HANA;", "the Attachment service stores it in storage", "category SCP-DM.100."],
    ["S/4HANA calls SAP Document Management service via", "a communication arrangement (technical OAuth 2.0", "client, not bound to the Entra user)."],
    ["DMS resolves the onboarded external repository", "(destination) and calls it through SAP", "Connectivity service."],
    ["The call runs through the TLS tunnel opened by the", "Cloud Connector VMs in the Azure VNet; the shadow", "in zone 2 takes over automatically."],
    ["The internal Azure Load Balancer (zone-redundant", "frontend) spreads CMIS 1.1 requests across the", "stateless CMIS Service VMs in both zones."],
    ["Any archive server writes metadata to the SQL", "Server AG primary (listener) and content to", "immutable Blob Storage via private endpoints;", "success only after synchronous commit."],
    ["SQL Server AG commits synchronously across zones", "(cloud witness); ZRS replicates Blob data across", "three zones. Singleton jobs run on the leader only."],
    ["easy applications and other CMIS clients use the", "same load balancer frontend directly."],
])
d.legend(1220, 1070)
d.footer("L2", "HA modes, SQL Server and Blob Storage support of easy archive to be confirmed with easy software. Technical OAuth clients are not federated via Entra ID.")
d.save(out, name="easy archive CMIS – active-active HA on Azure")
