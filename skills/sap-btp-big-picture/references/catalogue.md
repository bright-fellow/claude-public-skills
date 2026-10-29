# Reference content catalogue

What the reference capability map (`examples/big_picture_reference.py`) contains, area by area, so a tailored
map can add, drop or re-status items knowingly. Exact status keys: run
`python examples/big_picture_reference.py --list-labels` (plain chips are keyed by their full text, title chips
by their bold first line, tiles by their joined label, groups by their title; matching is case-insensitive).

The structure and wording are this skill's own. Product and capability names are SAP's public product names;
icons are the official SAP BTP solution-diagram icons (Apache-2.0).

## Business applications & teams (top band)
- **A - Transformation toolchain** (understand, plan and run the change)
  - SAP tools: SAP Signavio (Process Analysis & Design) · SAP LeanIX (Landscape Transparency) ·
    SAP Enable Now & WalkMe (Continuous Enablement) · SAP BTP (Extension & Innovation Platform) ·
    SAP Cloud ALM (CALM)
  - Partner tools (SAP solution extensions): OpenText (Information Governance) · Syniti (Data
    Transformation) · Tricentis (Test Automation)
- **SAP applications**: line-of-business chips Finance, Supply Chain, HR, Spend, CX, Industries
  (config: `apps_title`, `apps`).
- **Teams**: Developers, Business users, Data & AI engineers, Architects, IT operations, each with one line
  on what they do (config: `teams`).
- **Adoption summary**: counts and lists every status shown on the map; without statuses it shows a hint.

## SAP BTP (middle band)
- **SAP BTP Cockpit**: central web UI for administrators; manage resources, activate services, setup
  security, monitor consumption.
- **B - Apps & automation** (extend SAP without touching the core). SAP Build: Code, Apps, Work Zone, Process
  Automation; pro code, low code, AI-powered extension, workspaces & sites, process automation & visibility,
  workflow; ABAP Development Tools, ABAP Cloud; SAP CAP (use case logic, data management, LLM plugins & SDKs,
  SAP Cloud SDK for AI).
- **C - Business AI** (AI grounded in your business data). Joule Studio in SAP Build (Joule skills, AI
  agents). AI Foundation: AI services (Translation Hub, Document Information Extraction, Data Attribute
  Recommendation); CAP LLM Plugin (anonymization, embedding, similarity search, chat completion, RAG);
  AI lifecycle management - AI Launchpad, AI Core / Generative AI Hub (central admin, prompt engineering,
  trust & security, prompt registry, orchestration, deployment & delivery, foundation models access);
  foundation models (SAP built).
- **D - Business data & analytics** (one governed layer for data and analytics). SAP Business Data Cloud:
  BDC Cockpit; SAP Analytics Cloud (analytics & planning, data exploration, self-service BI, AI/prediction/
  simulation, MS Office add-in); intelligent applications; data sharing across all components; SAP Datasphere,
  Business Warehouse (BW modernization, data provisioning cockpit, BW models), SAP Databricks (custom AI & ML,
  pro-code data engineering, Unity Catalog), AI Foundation (→ area C); data products (SAP / BW / custom).
- **E - Integration** (SAP and non-SAP, cloud and on-premise). SAP Integration Suite: API Management, SAP
  Graph, Trading Partner Management, Cloud Integration, Integration Advisor, Open Connectors, (Advanced) Event
  Mesh, Migration Assessment & Tools; integration styles open / out-of-the-box / event based; on premises:
  Edge Integration Cell, PI/PO, S/4, Cloud Connector.
- Each area has a short **note column** in its own words and a "runs on" arrow to the foundation.
- **Platform Foundation**: Runtimes (ABAP environment incl. custom code migration, Cloud Foundry, Kyma);
  Application Lifecycle Management (Task Center, Application Logging, CI/CD, Cloud Transport Management);
  Persistency, Data & AI/ML (SAP HANA Cloud with vector engine, data management, embedding model, knowledge
  graph engine, database AI/ML engine, tiered storage, multi model, advanced analytics); Security, Compliance
  & Connectivity (Identity Authentication, Identity Directory, Identity Provisioning, Connectivity, Custom
  Domain, Audit Log, Data Privacy Integration).

## Partners & data sources (bottom band)
3rd-party data, technology and applications: cloud applications, solution extension partners, event sources
(plants, warehouses, logistics), cloud infrastructure, AI partners, data lakes / warehouses, data providers
(config: `ecosystem_title`, `ecosystem`).

## Learn more (right panel)
SAP Discovery Center (missions, reference architectures, BTP services, Business AI features) · SAP Business
Accelerator Hub (APIs, events, Graph, business objects, adapters, BAdIs, business object interfaces, CDS
views) · SAP Trust Center · architecture guidance (reference architectures, Integration Solution Advisory
Methodology, Application Extension Methodology, Data & Analytics Advisory Methodology).
