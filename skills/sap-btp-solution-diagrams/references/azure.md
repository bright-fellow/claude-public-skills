# Microsoft Azure components in SAP BTP solution diagrams

Icons: Microsoft Azure architecture icons, packaged for draw.io by
github.com/dwarfered/azure-architecture-icons-for-drawio, bundled as `assets/azure_icons.json`
(627 icons, key = cleaned icon title, with category). Search: `python scripts/find_icon.py <words> --lib azure`
or list categories with `--categories`.

## Microsoft usage rules (assets/azure-icons-terms-of-use.pdf)

- Permitted in architecture diagrams, training materials and documentation.
- Label every icon with the full product name close to it (but not overlapping).
- Do not crop, flip, rotate, distort or recolor icons; the library places them unmodified.
- Use an icon only to represent the Microsoft product it was designed for – never for the customer's
  or a third-party product (e.g. do not use the Azure VM icon to represent "easy archive"; show the
  product as a box and state "Azure VM" in its sub-line with the VM icon, as in the example).

## Containers in the SAP style

| Azure scope | Library call |
|---|---|
| Azure tenant / subscription / region | `area(..., "nonsap", "Microsoft Azure", "Subscription · region")` |
| Availability zone, or region in a multi-region design | `area(..., "teal", "Availability zone 1 – active")` |
| Virtual network, DR region, optional scope | `area(..., "dashed", ...)` |
| On-premises data centre | `area(..., "nonsap", "Customer data centre")` |

Keep SAP-managed things (BTP, RISE/S/4HANA Cloud) in blue even when they run on Azure infrastructure –
the colour tells who operates it, not where it runs.

## Role → icon mapping (verified keys)

| Role | Icon key |
|---|---|
| Virtual machine (app server, Cloud Connector host) | `azure:Virtual Machine` |
| Availability set | `azure:Availability Sets` |
| Internal / public L4 load balancer | `azure:Load Balancers` |
| L7 gateway / WAF | `azure:Application Gateways`, `azure:Web Application Firewall Policies(WAF)` |
| Global entry | `azure:Front Door and CDN Profiles`, `azure:Traffic Manager Profiles` |
| SQL Server on Azure VM (Always On AG) | `azure:Azure SQL VM` |
| Azure SQL Database / Managed Instance | `azure:SQL Database`, `azure:SQL Managed Instance` |
| PostgreSQL / MySQL | `azure:Azure Database PostgreSQL Server`, `azure:Azure Database MySQL Server` |
| Blob / storage account (incl. immutable WORM, cloud witness) | `azure:Storage Accounts` |
| Private endpoint / Private Link | `azure:Private Endpoints`, `azure:Private Link` |
| Virtual network / firewall / DNS | `azure:Virtual Networks`, `azure:Firewalls`, `azure:DNS Zones` |
| Hybrid connectivity | `azure:ExpressRoute Circuits`, plus VPN gateway via `find_icon.py vpn` |
| Monitoring | `azure:Monitor`, `azure:Log Analytics Workspaces` |
| Secrets / certificates | `azure:Key Vaults` |
| Backup / DR | `azure:Backup Vault`, `azure:Recovery Services Vaults` |
| Entra ID (the icon set has no generic "Entra ID" icon – show Entra ID as a grey `nonsap` area and use feature icons inside) | `azure:Enterprise Applications`, `azure:App Registrations`, `azure:Groups`, `azure:Users`, `azure:Multi Factor Authentication`, `azure:Entra Identity Roles and Administrators`, `azure:Entra Privleged Identity Management` (sic) |

For SAP BTP services that connect to Azure use the SAP icons (`sap:SAP Private Link service`,
`sap:SAP Connectivity service`, `sap:Cloud Connector`).

## Identity pattern: SAP Cloud Identity Services proxying Microsoft Entra ID

- Blue `btp` area "SAP Cloud Identity Services" with tiles `sap:Identity Authentication` (proxy IdP) and
  `sap:Identity Provisioning`, plus a `sap_fill` box listing the role mapping chain
  (Entra group / app role → IAS user group → BTP role collection / S/4HANA business role).
- Grey `nonsap` area "Microsoft Entra ID" with Enterprise application, Security groups, App registration
  (app roles → claims) and MFA / Conditional Access icons.
- `trust` edges (pink, both arrowheads): every SAP application / BTP subaccount → IAS, and IAS ↔ Entra ID
  with a pill such as "SAML 2.0 / OIDC · group & role claims". Provisioning (Microsoft Graph → Identity
  Provisioning → IAS / S/4HANA) uses normal `flow` edges.
- Number identity steps with letters (A, B, C…) and document steps with digits; group them in the flow
  panel with "# Identity & access" / "# ..." section headings.
- State in flow text or footer that technical OAuth clients (communication arrangements, service keys)
  are not federated through Entra ID – architects often ask.

## HA / DR patterns worth drawing explicitly

- **Zone-redundant active-active**: two mirrored `teal` zone areas under one load balancer box; stateless
  tiers in both zones; database as primary + synchronous secondary (`sync` edge) with a witness
  (`heartbeat` edge); zone-redundant storage (ZRS) as one box spanning below the zones.
- **Regional DR**: a `dashed` area for the paired region, fed by a single `async` edge with a pill that
  names the mechanisms (GZRS, async AG replica, Azure Site Recovery). State RPO > 0 in its subtitle.
- **Backup** is separate from replication: an immutable Backup vault with a `backup` edge – replication
  copies corruption and ransomware, backup does not.

State vendor-support assumptions (e.g. "SQL Server and Blob Storage support of <product> to be confirmed")
in the footer note instead of silently implying support.
