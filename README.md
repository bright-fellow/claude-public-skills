# Claude Public Skills

A collection of [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills/overview) for
Claude (Claude.ai, Claude Code and the Claude Agent SDK). Each skill is a self-contained folder with a
`SKILL.md` (instructions + frontmatter) and any scripts, references and assets it needs.

## Skills

| Skill | What it does |
|---|---|
| [`business-explainer`](skills/business-explainer/SKILL.md) | Produces a narrated business explainer video in a clean flat-vector style: one off-screen British narrator (ElevenLabs via fal), unDraw illustrations, Lucide icon diagrams, animated stats and lists, ducked series theme. Renders a 1920×1080 MP4 plus a review sheet. |
| [`sap-btp-solution-diagrams`](skills/sap-btp-solution-diagrams/SKILL.md) | Creates SAP BTP solution diagrams / reference architectures in the official SAP BTP diagram style as editable draw.io (`.drawio`) files, with bundled SAP BTP service icons and Microsoft Azure architecture icons. Always delivers an L1 overview and an L2 deep dive. |

## Repository layout

```
skills/
├── business-explainer/
│   └── SKILL.md                     # instructions + embedded toolkit (scripts, CSS, JS, template)
└── sap-btp-solution-diagrams/
    ├── SKILL.md
    ├── scripts/
    │   ├── btpdiagram.py            # diagram library (writes .drawio, optional PNG preview)
    │   └── find_icon.py             # search the bundled icon libraries
    ├── assets/
    │   ├── sap_btp_icons.json       # 76 official SAP BTP service icons
    │   ├── azure_icons.json         # 627 Microsoft Azure architecture icons
    │   └── azure-icons-terms-of-use.pdf
    ├── references/
    │   ├── style-guide.md           # palette, element catalogue, layout grid
    │   └── azure.md                 # Azure icon usage rules + role-to-icon mapping
    └── examples/                    # L1/L2 example layouts (easy archive, Integration Suite)
```

## Installation

**Claude.ai** – zip a skill folder (e.g. `skills/sap-btp-solution-diagrams`) and upload it under
*Settings → Capabilities → Skills*.

**Claude Code** – copy or symlink the folder into your personal or project skills directory:

```bash
git clone https://github.com/bright-fellow/claude-public-skills.git
```

```bash
cp -r claude-public-skills/skills/* ~/.claude/skills/
```

(or into `<project>/.claude/skills/` to share the skills with a project).

## Notes per skill

### business-explainer

- The whole toolkit (`setup.sh`, `assets/*.css|js|html`, `scripts/*.py`) is embedded in `SKILL.md` as
  four-backtick code blocks tagged `file=<path>`; §0 of the skill extracts them to `~/.biz-explainer` and runs the
  setup. There are no separate asset files to install.
- Setup needs network access (npm for GSAP, Lucide and HyperFrames; Google Fonts for Inter; an optional
  Whisper model) and a headless Chrome/Chromium.
- Narration uses the paid `elevenlabs/tts/eleven-v4` endpoint on [fal](https://fal.ai); the skill always
  shows a cost estimate and waits for approval before generating audio.
- Illustrations come from [unDraw](https://undraw.co), downloaded by the user.

### sap-btp-solution-diagrams

- Pure Python, no network needed. `cairosvg` is optional and only used to render a PNG preview for
  self-checking (`pip install cairosvg`).
- Quick test:

  ```bash
  python3 skills/sap-btp-solution-diagrams/examples/easy_archive_L1_overview.py /tmp/easy-archive-L1
  ```

  This writes `/tmp/easy-archive-L1.drawio`, which opens in diagrams.net, draw.io desktop or the VS Code
  draw.io extension.
- Paths such as `/mnt/user-data/outputs/` and `/home/claude/preview/` in `SKILL.md` refer to the Claude.ai
  sandbox; adjust them when running elsewhere.

## Third-party content and licences

- **Microsoft Azure architecture icons** (`assets/azure_icons.json`) are © Microsoft and are bundled for
  use in architecture diagrams under Microsoft's terms (see
  [`azure-icons-terms-of-use.pdf`](skills/sap-btp-solution-diagrams/assets/azure-icons-terms-of-use.pdf)):
  use them in diagrams, training material and documentation; don't crop, distort or use them to represent
  your own product. Converted via
  [dwarfered/azure-architecture-icons-for-drawio](https://github.com/dwarfered/azure-architecture-icons-for-drawio).
- **SAP BTP icons** (`assets/sap_btp_icons.json`) and the diagram style follow SAP's public
  [BTP solution diagram guidelines](https://github.com/SAP-archive/sap-btp-reference-architectures).
  SAP and the SAP logo are trademarks of SAP SE.
- unDraw, Lucide, GSAP, Inter and HyperFrames used by `business-explainer` are fetched at setup time and
  are subject to their own licences.
