# Reference content catalogue

What the reference poster (`examples/big_picture_reference.py`) contains, area by area, so a tailored Big
Picture can add, drop or re-status items knowingly. Exact status keys: run
`python examples/big_picture_reference.py --list-labels` (plain chips are keyed by their full text, title chips
by their bold first line, tiles by their joined label, groups by their title; matching is case-insensitive).

Source: SAP poster "SAP BTP Capabilities Reference Architecture for Best Transformation" (The Big Picture,
v1.3). Items marked *(interpretation)* were not readable as text on the poster and were rendered generically.

## SAP Applications and Processes (deep-blue band)
- **A - Best Integrated Toolchain for Transformation**
  - SAP Tools: SAP Signavio (Process Analysis & Design, BPM) · SAP LeanIX (Landscape Transparency, EAM) ·
    SAP Enable Now & WalkMe (Continuous Enablement & In-App Guidance) · SAP BTP (Extension & Innovation
    Platform) · SAP Cloud ALM (CALM)
  - Solution Extension Partner Tools: OpenText (Information Governance) · Syniti (Data Transformation) ·
    Tricentis (Quality Assurance by automated testing)
  - Benefits: "Continuously analyze, monitor and optimize landscape, data, and processes" (A ↔ SAP apps),
    "Optimize and understand processes and landscape together with SAP BTP" (A ↔ B)
- **SAP applications** with Business AI; LoB chips Finance, Supply Chain, HR, Spend, CX, Industries
  *(interpretation - the poster shows seven LoB product icons that are not in the official BTP icon set)*;
  agent loop: CX, Supply chain, HR, Spend, Finance agents.
- **Joule Capabilities**: Informational, Navigational, Transactional, Analytical; special: ABAP developer
  capabilities, SAP Joule for Consultants, Microsoft 365 Copilot bi-directional integration, SAP BTP Account
  Administration.
- **Personas** (fusion team): Developers → B · Business Users → B, D · Data & AI Engineers → C, D ·
  Enterprise Architects → E · IT Operations → A, BTP Cockpit.

## SAP BTP (bright-blue band)
- **SAP BTP Cockpit**: central web UI for administrators; manage resources, activate services, setup
  security, monitor consumption.
- **B - Best Appl. Development & Automation** (side-by-side clean core extensibility). Values: AI supported
  administration, development and automation; scalable factory for extension & app development.
  SAP Build: Code, Apps, Work Zone, Process Automation; pro code, low code, AI-powered extension, workspaces &
  sites, process automation & visibility, workflow; ABAP Development Tools, ABAP Cloud; SAP CAP (use case
  logic, data management, LLM plugins & SDKs, SAP Cloud SDK for AI). Benefit: add custom AI to apps and
  processes. Tag: Deploy and Run Applications.
- **C - Best Custom Business AI**. Values: scale AI responsibly; build reliable insights with AI; connect AI
  technologies with business data and processes. Joule Studio in SAP Build (Joule skills, AI agents).
  AI Foundation: AI Services (Translation Hub, Document Information Extraction, Data Attribute
  Recommendation); CAP LLM Plugin (anonymization, embedding, similarity search, chat completion, RAG);
  AI Lifecycle Management - AI Launchpad, AI Core / Generative AI Hub (central admin, prompt engineering,
  trust & security, prompt registry, orchestration: grounding, prompt templating, data masking, LLM access;
  deployment & delivery, foundation models access); Foundation Models (SAP built, e.g. ABAP code generation /
  explain). Benefit: combine quality business data with AI, apps, and processes. Tag: Deploy and Run AI with Data.
- **D - Best Business Data**. Values: intelligent applications; harmonized data model across SAP portfolio;
  managed enterprise-grade data & technology stack; TCO optimized scalable persistency; data products;
  connect and integrate without copying ("delta share"); data ready for AI and data science.
  SAP Business Data Cloud: BDC Cockpit; SAP Analytics Cloud (analytics & planning, data exploration,
  self-service BI, AI/prediction/simulation, MS Office add-in); intelligent applications (adaptive
  experiences, planning & simulations, partner applications); secure unified data sharing; SAP Datasphere,
  Business Warehouse (BW modernization, data provisioning cockpit, BW models), SAP Databricks (custom AI & ML,
  pro-code data engineering, Unity Catalog), AI Foundation (→ area C); data products in the SAP object store
  (SAP / BW / custom data products, data product generator). Benefit: connect and integrate processes,
  applications, and data. Tag: Process Data.
- **E - Best Integration** (side-by-side clean core integration). Values: any-to-any enterprise integration
  platform; holistic integration (synchronous, real-time, process driven). Channels: governments, SAP apps,
  3rd-party apps, B2B partners, cloud protocols. SAP Integration Suite: API Management, SAP Graph, Trading
  Partner Management, Cloud Integration, Integration Advisor, Open Connectors, (Advanced) Event Mesh,
  Migration Assessment & Tools; integration styles open / out-of-the-box / event based; on premises: Edge
  Integration Cell, PI/PO, S/4, Cloud Connector. Tag: Secure and transport.
- **Platform Foundation**: Runtimes (ABAP environment incl. custom code migration, Cloud Foundry, Kyma);
  Application Lifecycle Management (Task Center, Application Logging, CI/CD, Cloud Transport Management);
  Persistency, Data & AI/ML (SAP HANA Cloud with vector engine, data management, embedding model, knowledge
  graph engine, database AI/ML engine, tiered storage, multi model, advanced analytics); Security, Compliance
  & Connectivity (Identity Authentication, Identity Directory, Identity Provisioning, Connectivity, Custom
  Domain, Audit Log, Data Privacy Integration).

## Sources & Open Ecosystem (pale band)
3rd-party data, technologies and applications: cloud applications, solution extension partners, event
sources (plants, warehouses, logistics), cloud infrastructure, AI partners, data lakes / warehouses, data
providers. Benefits: technology partners; connect with foundation models (partner built); consume external
data; connect SAP landscape with 3rd-party applications and cloud services.

## Key Sites, Methodologies and Guidelines (right panel)
SAP Discovery Center (missions, reference architectures, BTP services, Business AI features) · SAP Business
Accelerator Hub (APIs, events, Graph, business objects, adapters, BAdIs, business object interfaces, CDS
views) · SAP Trust Center · architecture guidance (reference architectures, Integration Solution Advisory
Methodology, Application Extension Methodology, Data & Analytics Advisory Methodology). The poster's QR codes
are omitted *(interpretation: the card titled "Architecture guidance" carries an unreadable logo on the poster)*.
