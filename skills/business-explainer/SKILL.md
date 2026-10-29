---
name: "business-explainer"
description: "Produce a narrated business explainer video in clean flat-vector style: no on-screen characters or presenters, one British ElevenLabs narrator, unDraw illustrations the user downloads, icon diagrams, stats and lists that animate on the spoken word, ducked series theme. Use for business, process, product or concept explainer videos."
---

# Business explainer

A narrated explainer film in clean, modern flat-vector style. There are no presenters and no podcast set:
one off-screen narrator talks the topic through while the screen builds itself on the spoken words.
- **Illustrations**: unDraw scenes the user downloaded, recoloured to the brand, assembling bottom-up.
- **Diagrams**: process flows, hub-and-spoke, before/after cards, built from Lucide icons in tinted discs.
- **Numbers and lists**: count-up stats, bar comparisons, numbered key points, a key-term card.
- **Type**: Inter, with highlighter-marked key words; a chapter label top-left and a thin progress bar.

It is the flat-vector sibling of **watercolour-explainer** and keeps its signature hook, silent title card,
key-point summary, closing thought, series theme and teaser-first workflow. It drops the presenters, the lip
sync, the ink and watercolour, and the Q&A between two voices.

**Voice: one British ElevenLabs narrator**, "George" by default (`elevenlabs/tts/eleven-v4` on fal). Use
"Alice" if the user wants a female narrator.

**Audio is narrator and theme only.** No sound effects (whooshes, pops, clicks). Don't add them or offer them.

**Cost estimate before spending.** Before any paid generation, tell the user the model, the character count
and the estimated cost (§2c), and wait for their go-ahead. Everything else (art, rendering) is local and free.

Outputs:
- `out/<name>.mp4` (1920×1080, 30 fps, H.264 + AAC)
- `out/review_sheet.png` (every scene fully built)

It always starts with a ~60–90 s teaser in the final style. The full film is built only after the user has
judged the teaser. `X` = `~/.biz-explainer`. Work in one folder per film (`WORK`).

## 0. Install (once per machine/session)

Write this skill's embedded files and run the setup. The setup installs GSAP and Lucide icons from npm,
the Inter font, HyperFrames (the renderer) and finds a headless Chrome for it; it also fetches an offline
Whisper model from GitHub for pronunciation checks (optional).

```bash
python3 - "$SKILL_MD" ~/.biz-explainer <<'PY'
import os, re, sys
src, root = open(sys.argv[1]).read(), os.path.expanduser(sys.argv[2])
for path, body in re.findall(r"^````[a-z]* file=(\S+)\n(.*?)^````$", src, re.M | re.S):
    p = os.path.join(root, path); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w").write(body)
print("biz-explainer ->", root)
PY
bash ~/.biz-explainer/setup.sh
```

If Chrome can't be downloaded, point `HYPERFRAMES_BROWSER_PATH` at any installed Chrome or Chromium;
`bxlib.browser()` also finds Playwright's headless shell under `/opt/pw-browsers` automatically.

## 1. Brief

- **No characters on screen, no presenters, no podcast framing.** unDraw scenes may contain small generic
  figures; that is fine. They illustrate, they never host.
- **No series name or branding** by default: no channel name, series label, subtitle on the title card or
  branded sign-off. Never label the audience ("for business users"). If the user wants their company's
  look, put it in the brand tokens (§1b), not in the speech.
- **Depth**: beginner (analogies first) or deeper (more mechanism). It shapes the script only.
- **Length**:
  - teaser ~60–90 s (9–12 beats, 8–10 scenes);
  - full film 3–5 min (~450–700 words, 30–45 beats). George speaks at about 140 words per minute.
- **Format**: 16:9 at 1080p only.

### 1a. Series theme (fixed)

The theme music is the same one the watercolour series uses, kept in the user's private kit artifact
**https://claude.ai/artifact/KsRRfRczd8KqSBpMSDATPT** ("Watercolour Explainer kit"), path `audio/theme.mp3`.
At the start of every film:

```text
Artifact action=read, url=https://claude.ai/artifact/KsRRfRczd8KqSBpMSDATPT, path="audio/theme.mp3", out_dir=<scratchpad>/kit
cp <scratchpad>/kit/audio/theme.mp3 WORK/music.mp3
```

If the kit can't be read (another account, no access), ask the user for the link or the file. Generate a new
theme only when the user asks, with the prompt in watercolour-explainer §3d, and replace it in the kit.

### 1b. Brand tokens

All colour and type come from `tokens.css`. The default is a neutral indigo palette. For a company look,
copy `X/assets/tokens.css` to `WORK/tokens.css` and change the values:
- `--bx-accent` is the one brand colour: highlights, numbers, hub, connectors, and the colour unDraw art is
  recoloured to. Keep it saturated and readable on white.
- `--bx-tint` / `--bx-mark` are light versions of it (disc backgrounds, highlighter strokes);
  `--bx-accent-2` is the "good" colour, `--bx-risk` the "bad" one.
- A brand font: put the file in `WORK/fonts/` and point the `@font-face` at `fonts/<file>`.
- When the user names a company, the Brandfetch connector (`get_brand_data`) gives its colours and fonts.

## 2. Research and write the script

Research the topic first: current facts, numbers with their sources, common pitfalls, authoritative
sources (standards bodies, government advisories, vendor docs). Cite them in your reply. **Only show numbers
you can source**; label an illustrative figure as such on screen (`sub`).

Then write beats: one or two short sentences each, all spoken by the narrator. A beat with `show` starts a
new scene; beats without it continue the current scene.

- **Structure** (opening and closing are fixed, so every film feels the same):
  1. **Signature hook** (§2a): a cold-open question.
  2. **Signature title card**: theme intro and the topic, no speech.
  3. **The problem**: the situation the viewer recognises, in their terms.
  4. **The idea**: one practical analogy per idea ("an API is the front desk of an app").
  5. **How it works**: a flow of 3–5 steps.
  6. **Why it matters**: a sourced number, a before/after, or a hub of what it connects.
  7. **Where it goes wrong**, then a short practical checklist.
  8. **Key points** (§2a), then the **closing thought** (§2a) and the fixed end card.
- **Tone: professional and credible.** No gags, puns or jokey asides. Engagement comes from pace, one clear
  question per scene, and visuals that land on the word.
- **Accuracy over neat soundbites.** State nuance plainly.
- **Jargon**: spell out every acronym the first time it is spoken ("an API, short for Application Programming
  Interface") and show the full name on screen (`full` on a keyterm, or `body`). Make vague words concrete.
  Avoid endpoint, schema, OAuth and token, or translate them in one clause.
- **One scene, one message.** A scene's on-screen words are a headline and at most 3–4 short lines;
  the narration carries the rest. Change scene every 1–3 beats (about every 5–12 s).
- **Show the script to the user before voicing** when they are around, together with the cost estimate.

### 2a. Signature hook, key points and closing thought (every film)

**Hook (beat 1, scene `hook`)**: one concrete everyday business situation, then the question the film
answers, at most ~30 words: "<situation>. So <question>?" On screen: the question (≤ 60 characters, one key
word `*highlighted*`) and a short accent line (`sub`), cued on a word in the first half of the beat so it is
finished before the title card. The camera pushes in slowly by itself.

**Title card (beat 2, silent, `"min": 3.4`)**: scene `title` with "<Topic>" or "<Topic>, explained" alone
(≤ 28 characters). No subtitle, no series label. The camera eases back.

**Key points (right before the closing thought)**: "So, the key points." then 3–5 takeaways, one short
sentence each, in the order the film covered them. On screen: scene `list` with `kicker` "Key points", a
short `head`, and one item per takeaway (≤ 6 words each), each cued on its sentence. No new information.

**Closing thought**: one sentence that turns the film into something the viewer does or asks next time
("Next time two tools disagree about a customer, ask: …"). Not a summary, not a call to subscribe. On screen:
scene `quote` with one or two `*highlighted*` words, held at least 4 s (`min` on the beat).

**End card**: the narrator says "This was <topic>." Scene `end` with the topic and `"sub": "thanks for watching"`,
`"min": 3.0`. The theme's resolving outro plays under the closing thought and end card.

Never open with a greeting, an agenda or "in this video we will…".

### 2b. Script length check

`python3 X/scripts/voices.py cost WORK` prints the characters per line, the word count, the spoken length at
140 wpm and the voice cost. For a free layout preview before anything is paid for, use draft timing (§5).

### 2c. Cost estimate (always before spending)

Check the rate with fal `get_pricing` (`elevenlabs/tts/eleven-v4`), then tell the user:

| Item | Rate (Oct 2026) | Typical |
|---|---|---|
| Narration, Eleven v4 | $0.08 per 1,000 characters of `say` text | teaser ~900–1,200 chars ≈ $0.10; 4-min film ~3,800 chars ≈ $0.30 |
| Illustrations | free (the user's unDraw downloads) | — |
| Rendering | free (local) | ~3 min per minute of film |

Add a small buffer for re-voicing a line and name a stop limit (e.g. "I'll stop if anything heads past $0.50").
Wait for the go-ahead. AskUserQuestion works well here, with the script attached.

### 2d. Voicing (ElevenLabs on fal)

1. `python3 X/scripts/voices.py jobs WORK` prints the `submit_jobs` batches (8 lines per call, `index` = the
   beat number, voice from `script.json` `"voice"`). Send all the calls in one turn to
   `elevenlabs/tts/eleven-v4`. Re-voice single lines later with `--only 3,7`.
2. Collect with `wait_for_jobs` (up to 32 per call). Large replies are saved to files; pass them on:
   `python3 X/scripts/voices.py collect WORK <saved reply files…>` (merges into `WORK/eleven.json`).
3. `python3 X/scripts/voices.py build WORK --check` writes `audio/`, `voice_only.wav` and `timing.json` with
   exact word onsets, and prints what Whisper heard per line. Whisper writes numbers as digits and mishears
   some correct words; re-voice a line only for a real mispronunciation.

Write `say` text as it should be read. ElevenLabs reads acronyms, years and dates naturally ("API" is fine);
spell out anything that must be said a particular way.

## 3. Visuals

### 3a. unDraw illustrations (the user downloads them)

unDraw's license allows commercial use with no attribution, but **forbids automated downloading, scraping,
integrations, AI training, and redistributing the illustrations in packs**. So:
- Never fetch from undraw.co (no curl, no browser automation, no search-and-download). Ask the user to pick
  illustrations on undraw.co, download the SVGs and attach them (or drop them in `WORK/undraw/`).
  Suggest search words per scene ("Search unDraw for: *team collaboration*, *data processing*, *security*").
- Keep the files in the film folder. Don't publish them as a set (no kit artifact of unDraw files).
- Prepare each one: `python3 X/scripts/undraw.py WORK/undraw/<download>.svg WORK/art/<id>.svg`.
  It recolours unDraw's accent (`#6c63ff`, or the most used saturated colour) to `--bx-accent`, strips
  scripts and comments, adds a viewBox and namespaces ids. `--info` prints the colours; `--from #hex` sets the
  colour to replace if the user picked another colour on the site; `--ink #hex` remaps unDraw's dark ink.
- Use 2–4 illustrations in a teaser and 5–10 in a full film, for the scenes where a picture says more than
  a diagram (the problem, the idea, the example). Everything structural is a diagram (§3b).
- No suitable illustration? Use a diagram scene instead. Don't generate imitation unDraw art.

### 3b. Icons (Lucide, built in)

Diagram scenes use Lucide icon names (ISC licence, ~2,000 icons, e.g. `users`, `database`, `shield-check`,
`receipt`, `globe`, `mail`, `calendar`, `file-text`, `lock`, `zap`, `repeat`, `send`, `bar-chart-3`,
`building-2`, `handshake`, `workflow`, `cloud`, `bot`, `search`, `alert-triangle`, `check-circle`).
`build.py` warns about an unknown name and suggests close ones. List them with
`ls X/vendor/node_modules/lucide-static/icons | grep <word>`.

### 3c. Scene types (`show.type`)

Every scene can have `chapter` (the label top-left, e.g. `"02 · How it works"`; keep it the same across a
section). Text fields accept `*word*` for an accent highlight with a marker stroke. Cue fields are `at` or end
in `At` (§4).

| Type | Fields | Use for |
|---|---|---|
| `hook` | `question`, `sub`, `subAt` | beat 1 only |
| `title` | `title` (≤ 28 chars), `kicker` | beat 2 only, silent |
| `illustration` | `art`, `layout` `left`\|`right`\|`center`, `kicker`, `head`, `headAt`, `body`, `bodyAt`, `bullets` [{`text`, `at`}] (≤ 4), `artAt` | the problem, the idea, an example |
| `flow` | `head`, `nodes` [{`icon`, `label`, `sub`, `at`, `solid`}] (2–5), `numbered` | a process, steps, a journey |
| `hub` | `head`, `center` {`icon`, `label`, `at`}, `spokes` [{`icon`, `label`, `at`}] (3–8), `offset` | a platform and what it connects |
| `stat` | `value` (number counts up, string pops), `prefix`, `suffix`, `decimals`, `label`, `sub`, `valueAt`, `subAt`, `kicker`, `art` | one sourced number |
| `compare` | `head`, `bars` [{`label`, `value`, `at`, `highlight`}] (2–4), `prefix`, `suffix`, `max` | before/after, us vs average |
| `split` | `left` / `right` {`title`, `icon`, `tone` `risk`\|`good`\|`accent`\|`muted`, `at`, `lines` [text or {`text`, `at`}]}, `vs` | without vs with, myth vs fact |
| `list` | `kicker`, `head`, `headAt`, `items` [{`text`, `at`, `badge`}] (≤ 6), `check` | key points, checklist (`"check": true`) |
| `keyterm` | `term`, `full`, `definition`, `icon`, `kicker`, `termAt`, `fullAt`, `definitionAt` | a term the film leans on |
| `quote` | `text` (≤ 90 chars), `textAt` | the closing thought |
| `end` | `title`, `sub` | last beat only |
| `blank` | — | a breath between sections |

Limits that keep scenes readable (`build.py` warns past them): head ≤ 60 chars, bullet/list item/split line
≤ 46, node/spoke label ≤ 34, keyterm `term` ≤ 22, `definition` ≤ 110.

**Variety**: don't use the same scene type twice in a row; alternate pictures (illustration, stat with art)
with diagrams (flow, hub, split, compare). A full film typically has 2–3 flows, 1–2 hubs or splits,
1–3 stats or compares, one keyterm per new term, 5–10 illustrations.

## 4. script.json

```json
{
  "name": "api-teaser", "topic": "APIs", "voice": "George",
  "lead_in": 0.6, "gap": 0.4, "tail": 1.8,
  "beats": [
    {"say": "Your sales tool, your invoicing app and your website all hold the same customer. So how do they keep each other up to date?",
     "show": {"type": "hook", "question": "How do your apps *talk* to each other?", "sub": "And why it matters to the business", "subAt": "website"}},
    {"say": "", "min": 3.4, "show": {"type": "title", "title": "APIs, explained"}},
    {"say": "Every app keeps its data behind a front desk. An API, short for Application Programming Interface, is that front desk for software.",
     "show": {"type": "illustration", "art": "desk", "layout": "left", "chapter": "01 · The idea", "kicker": "The idea",
              "head": "A *front desk* for software", "headAt": "front desk",
              "bullets": [{"text": "Clear requests in", "at": "API"}, {"text": "Only the answer out", "at": "Interface"}]}},
    {"say": "One app asks a clear question, the API checks who is asking, and sends back only the answer.",
     "show": {"type": "flow", "chapter": "01 · The idea", "head": "How a request travels",
              "nodes": [{"icon": "send", "label": "Request", "sub": "a clear question", "at": "asks"},
                        {"icon": "shield-check", "label": "Check", "sub": "who is asking?", "at": "checks"},
                        {"icon": "database", "label": "Answer", "sub": "only what's needed", "at": "sends"}]}},
    {"say": "This was APIs, explained.", "min": 3.0, "show": {"type": "end", "title": "APIs, explained", "sub": "thanks for watching"}}
  ]
}
```

- `voice`: the ElevenLabs voice ("George" default, "Alice" female). `language` defaults to `"en"`.
- Per beat: `say`, optional `show`, `min` (seconds the beat lasts at least), `pause` (silence after it,
  default `gap`).
- **Cues**: `"word"` or `"two words"` (the first match from the scene's first beat on, case and punctuation
  ignored), `"word+0.4"` (positive offsets only), `"end"` (1 s before the scene leaves), or a number
  (seconds after the scene starts). Cue the word where the idea lands, not where it is first hinted.
  Elements without a cue appear in a short stagger as the scene opens.
- A scene runs from its beat's start (minus 0.15 s) to the next scene's start, then leaves in 0.4 s.

## 5. Build order (fix every WARN)

```bash
cp <kit>/audio/theme.mp3 WORK/music.mp3                     # §1a
python3 X/scripts/undraw.py WORK/undraw/<file>.svg WORK/art/<id>.svg   # per illustration (§3a)
python3 X/scripts/voices.py cost WORK                       # length + cost -> script + estimate to the user (§2c)
python3 X/scripts/voices.py draft WORK                      # FREE: estimated timing, silent
python3 X/scripts/build.py WORK                             # resolves cues -> WORK/film/, prints WARNs
python3 X/scripts/render.py WORK --preview                  # out/review_sheet.png in ~30 s: check layout now
#  -> after the go-ahead: voices.py jobs / fal submit_jobs / wait_for_jobs / voices.py collect (§2d)
python3 X/scripts/voices.py build WORK --check              # real timing.json + voice_only.wav
python3 X/scripts/build.py WORK                             # again: cues move with the real voice
python3 X/scripts/mix.py WORK                               # narrator + ducked theme -> narration.wav
python3 X/scripts/render.py WORK                            # review sheet + out/<name>.mp4 (run in background)
```

Check single moments with `npx hyperframes snapshot WORK/film --at 12.5,30 --no-end -o WORK/snaps`
(set `HYPERFRAMES_BROWSER_PATH` from `bxlib.browser()` if Chrome isn't found).

When you change `say` text, re-voice only the changed lines (`jobs --only`), then rerun from
`voices.py build`. When you change only `show` content or cues, rerun from `build.py`. Changing tokens or
art needs only `build.py` and a render.

## 6. Review, then hand over

Look at `out/review_sheet.png` and at a few mid-scene snapshots. Check that:
- every element appeared (nothing cut off, nothing hidden behind another);
- headlines fit in one or two lines; no text touches the frame edge or the chapter label;
- the art is recoloured to the accent and sits on its blob;
- numbers on screen are the sourced ones, illustrative ones say so;
- each scene's key element lands on its spoken word (watch the mp4 at the cue times);
- the audio is narrator and theme only;
- there is no series name, branding or audience label anywhere;
- the hook, title card, key points, closing thought and end card follow §2a.

Send the mp4 with SendUserFile, then say in a few lines what's in it and what it cost. For a teaser, say that
the full film follows once the style is approved and offer the full script for review first.

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Chrome Headless Shell is required` | set `HYPERFRAMES_BROWSER_PATH` to any Chrome/Chromium; `bxlib.browser()` finds Playwright's |
| `cue '…' not spoken in this scene` | copy the word from that scene's `say`; cues only search the scene's own beats |
| An element appears as the scene leaves | its cue word is at the very end of the scene: cue an earlier word or add `min` to the beat |
| unDraw art keeps its purple | the download used another colour: `undraw.py --info`, then `--from #hex` |
| Art appears all at once | the SVG has one big path; that's fine, or pick a richer illustration |
| `icon '…' not in Lucide` | use one of the suggested names |
| `timing.json is out of date` | beats were added or removed: rerun `voices.py build` (or `draft`) |
| Highlight marker invisible | `--bx-mark` too close to `--bx-bg` in a custom tokens.css |
| `wait_for_jobs` reply too large | it is saved to a file automatically; pass that file to `voices.py collect` |
| Some lines have no timestamps | `collect` takes the audio URL from `media`; timing for those lines is estimated |
| Word heard wrong in `--check` | rephrase in plain words, re-voice that line only |
| fal `balance_exhausted` | tell the user once with the billing link and stop; collect jobs already accepted |

## Embedded files (written to `~/.biz-explainer` by step 0)

````bash file=setup.sh
#!/usr/bin/env bash
# Business explainer toolkit setup (once per machine/session). Needs Node 22+, FFmpeg, Python 3 + Pillow + numpy.
set -e
X="$(cd "$(dirname "$0")" && pwd)"
# 1) GSAP (animation) + Lucide icons (ISC licence, 1,900+ flat line icons) from npm
mkdir -p "$X/vendor" && cd "$X/vendor"
[ -f package.json ] || echo '{"name":"bx-vendor","private":true}' > package.json
[ -d node_modules/gsap ] && [ -d node_modules/lucide-static ] || npm i -s gsap lucide-static
# 2) Inter (OFL) for all type
mkdir -p "$X/assets/fonts"
[ -s "$X/assets/fonts/Inter.ttf" ] || curl -sSLf -o "$X/assets/fonts/Inter.ttf" "https://raw.githubusercontent.com/google/fonts/main/ofl/inter/Inter%5Bopsz%2Cwght%5D.ttf"
# 3) HyperFrames (renderer) + a headless Chrome it can drive
npx -y hyperframes --version >/dev/null
python3 - <<'PY' || npx -y hyperframes browser ensure || echo "WARN no Chrome: set HYPERFRAMES_BROWSER_PATH to any Chrome/Chromium"
import sys, os; sys.path.insert(0, os.path.expanduser("~/.biz-explainer/scripts"))
from bxlib import browser; b = browser(); print("browser:", b); sys.exit(0 if b else 1)
PY
python3 -c "import numpy, PIL" 2>/dev/null || python3 -m pip install -q --break-system-packages numpy pillow
# 4) optional: offline Whisper for --check pronunciation (GitHub, not Hugging Face)
A=~/.cache/asr; mkdir -p "$A"
if [ ! -d "$A/sherpa-onnx-whisper-base.en" ]; then
  curl -sSLf -o "$A/w.tar.bz2" https://github.com/k2-fsa/sherpa-onnx/releases/download/asr-models/sherpa-onnx-whisper-base.en.tar.bz2 \
    && tar xjf "$A/w.tar.bz2" -C "$A" && rm -f "$A/w.tar.bz2" || echo "(Whisper model not fetched: --check will be skipped)"
fi
python3 -c "import sherpa_onnx, scipy" 2>/dev/null || python3 -m pip install -q --break-system-packages sherpa-onnx scipy || true
echo "business explainer toolkit ready in $X"
````

````css file=assets/tokens.css
/*
 * Business explainer brand tokens. Every scene reads ONLY these variables, so a new brand
 * is a new copy of this file (WORK/tokens.css overrides the default). Keep --bx-accent the
 * colour unDraw illustrations are recoloured to (undraw.py --accent), so art and diagrams match.
 */
@font-face {
  font-family: "Inter";
  src: url("fonts/Inter.ttf") format("truetype");
  font-weight: 100 900;
}
:root {
  --bx-font: "Inter", system-ui, sans-serif;
  --bx-weight-display: 800;
  --bx-weight-head: 700;
  --bx-weight-body: 450;
  --bx-tracking: -0.025em;

  --bx-bg: #f6f6fa;          /* page */
  --bx-surface: #ffffff;     /* cards */
  --bx-ink: #1d1b2f;         /* headlines, body */
  --bx-muted: #6b6a80;       /* secondary text */
  --bx-line: #d9d8e4;        /* connectors, tracks, dividers */
  --bx-accent: #5b4fe9;      /* the brand colour: highlights, numbers, hub */
  --bx-on-accent: #ffffff;
  --bx-accent-2: #14b8a6;    /* second series / positive */
  --bx-accent-3: #f59e0b;    /* third series / attention */
  --bx-risk: #ef4f5f;        /* pitfalls, "before", warnings */
  --bx-tint: #e9e7fd;        /* light accent wash: blobs, icon discs, highlights */
  --bx-mark: #d4cffc;        /* highlighter stroke behind *highlighted* words */
  --bx-tint-2: #d9f4f0;
  --bx-tint-3: #fdf0d8;
  --bx-shadow: 0 18px 50px rgba(29, 27, 47, 0.10);
  --bx-radius: 28px;
}
````

````css file=assets/bx.css
/* Business explainer: flat-vector scene styles. Colours and type come only from tokens.css. */
html, body { margin: 0; padding: 0; background: var(--bx-bg); }
#root { position: relative; width: 1920px; height: 1080px; overflow: hidden; background: var(--bx-bg);
  font-family: var(--bx-font); color: var(--bx-ink); font-weight: var(--bx-weight-body); }
#bx-clip { position: absolute; inset: 0; }
#bx-cam { position: absolute; inset: 0; transform-origin: 960px 520px; }
.bx-blob { position: absolute; border-radius: 50%; }
.bx-blob.b1 { width: 760px; height: 760px; left: 1420px; top: -330px; background: var(--bx-tint); }
.bx-blob.b2 { width: 620px; height: 620px; left: -300px; top: 700px; background: var(--bx-tint-2); }
.bx-dots { position: absolute; left: 1700px; top: 860px; width: 150px; height: 110px; opacity: .55;
  background-image: radial-gradient(var(--bx-accent) 3px, transparent 3.5px); background-size: 30px 30px; }

.bx-scene { position: absolute; inset: 0; visibility: hidden; }
.bx-abs { position: absolute; }
.bx-center { text-align: center; }

/* chapter label + progress */
#bx-label { position: absolute; left: 140px; top: 72px; font-size: 24px; font-weight: 700; letter-spacing: .14em;
  text-transform: uppercase; color: var(--bx-muted); display: flex; align-items: center; gap: 16px; white-space: nowrap; }
#bx-label::before { content: ""; width: 14px; height: 14px; border-radius: 50%; background: var(--bx-accent); }
#bx-progress { position: absolute; left: 0; bottom: 0; height: 8px; width: 1920px; background: var(--bx-accent);
  transform-origin: 0 50%; transform: scaleX(0); }

/* type */
.bx-display { font-weight: var(--bx-weight-display); letter-spacing: var(--bx-tracking); line-height: 1.04; }
.bx-head { font-weight: var(--bx-weight-head); letter-spacing: -0.015em; line-height: 1.12; }
.bx-kicker { font-size: 26px; font-weight: 700; letter-spacing: .14em; text-transform: uppercase; color: var(--bx-accent); }
.bx-muted { color: var(--bx-muted); }
.bx-accent { color: var(--bx-accent); }
.bx-w { display: inline-block; white-space: pre; }
.bx-hl { position: relative; isolation: isolate; display: inline-block; white-space: pre; color: var(--bx-accent); }
.bx-hl-bg { position: absolute; left: -0.08em; right: -0.08em; bottom: 0.04em; height: 0.38em; background: var(--bx-mark);
  border-radius: 0.1em; transform-origin: 0 50%; z-index: -1; }
.bx-hl-tx { position: relative; }

/* hook / title / end / quote */
.bx-hook-q { left: 160px; width: 1600px; top: 250px; font-size: 112px; text-align: center; }
.bx-hook-sub { left: 160px; width: 1600px; top: 700px; font-size: 46px; text-align: center; font-weight: 600; color: var(--bx-accent); }
.bx-title { left: 120px; width: 1680px; top: 360px; font-size: 168px; text-align: center; }
.bx-title-bar { left: 850px; top: 650px; width: 220px; height: 16px; border-radius: 8px; background: var(--bx-accent); transform-origin: 50% 50%; }
.bx-title-kicker { left: 160px; width: 1600px; top: 300px; text-align: center; }
.bx-shape { position: absolute; }
.bx-shape.circ { border-radius: 50%; }
.bx-shape.sq { border-radius: 18px; }
.bx-quote { left: 260px; width: 1400px; top: 330px; font-size: 72px; text-align: center; }
.bx-qmark { left: 900px; top: 140px; width: 120px; height: 120px; border-radius: 50%; background: var(--bx-tint);
  color: var(--bx-accent); font-size: 150px; font-weight: 800; line-height: 190px; text-align: center; }
.bx-end { left: 120px; width: 1680px; top: 390px; font-size: 120px; text-align: center; }
.bx-end-sub { left: 160px; width: 1600px; top: 560px; font-size: 44px; text-align: center; font-weight: 600; color: var(--bx-accent); }

/* illustration */
.bx-artbox { display: flex; align-items: center; justify-content: center; }
.bx-artbox svg { width: 100%; height: 100%; overflow: visible; }
.bx-artblob { border-radius: 50%; background: var(--bx-tint); }
.bx-text { display: flex; flex-direction: column; gap: 26px; }
.bx-text .bx-head { font-size: 64px; }
.bx-text .bx-body { font-size: 36px; line-height: 1.38; color: var(--bx-muted); }
.bx-bullets { display: flex; flex-direction: column; gap: 22px; margin-top: 6px; }
.bx-bullet { display: flex; gap: 22px; align-items: flex-start; font-size: 36px; line-height: 1.3; }
.bx-bullet i { flex: none; width: 16px; height: 16px; margin-top: 15px; border-radius: 50%; background: var(--bx-accent); }
.bx-caption { text-align: center; }
.bx-caption .bx-head { font-size: 60px; }
.bx-caption .bx-body { font-size: 34px; color: var(--bx-muted); margin-top: 14px; }

/* nodes: flow + hub */
.bx-node { position: absolute; display: flex; flex-direction: column; align-items: center; text-align: center; }
.bx-disc { border-radius: 50%; background: var(--bx-tint); color: var(--bx-accent); display: flex; align-items: center; justify-content: center; }
.bx-disc svg { width: 46%; height: 46%; }
.bx-disc.solid { background: var(--bx-accent); color: var(--bx-on-accent); }
.bx-node-label { font-weight: 700; color: var(--bx-ink); margin-top: 22px; line-height: 1.15; }
.bx-node-sub { color: var(--bx-muted); margin-top: 8px; line-height: 1.25; }
.bx-wires { position: absolute; left: 0; top: 0; width: 1920px; height: 1080px; overflow: visible; }
.bx-wires path { fill: none; stroke: var(--bx-line); stroke-width: 6; stroke-linecap: round; }
.bx-wires path.on { stroke: var(--bx-accent); }
.bx-wires polygon { fill: var(--bx-accent); }
.bx-badge { position: absolute; width: 50px; height: 50px; border-radius: 50%; background: var(--bx-accent); color: var(--bx-on-accent);
  font-weight: 800; font-size: 24px; display: flex; align-items: center; justify-content: center; border: 5px solid var(--bx-bg); }
.bx-sectionhead { left: 160px; width: 1600px; top: 160px; text-align: center; font-size: 56px; }

/* stat */
.bx-stat { display: flex; flex-direction: column; justify-content: center; }
.bx-stat-value { font-size: 230px; font-weight: 800; letter-spacing: -0.04em; line-height: 1; color: var(--bx-accent); white-space: nowrap; }
.bx-stat-label { font-size: 52px; font-weight: 700; line-height: 1.15; margin-top: 18px; }
.bx-stat-sub { font-size: 34px; color: var(--bx-muted); margin-top: 18px; line-height: 1.3; }

/* cards: compare, split, list */
.bx-card { position: absolute; background: var(--bx-surface); border-radius: var(--bx-radius); box-shadow: var(--bx-shadow); }
.bx-bars { display: flex; flex-direction: column; gap: 44px; }
.bx-bar-head { display: flex; justify-content: space-between; align-items: baseline; font-size: 36px; margin-bottom: 14px; }
.bx-bar-label { font-weight: 600; }
.bx-bar-value { font-weight: 800; font-size: 44px; color: var(--bx-ink); }
.bx-track { height: 34px; border-radius: 17px; background: var(--bx-bg); overflow: hidden; }
.bx-fill { height: 100%; border-radius: 17px; background: var(--bx-line); transform-origin: 0 50%; }
.bx-bar.hi .bx-fill { background: var(--bx-accent); }
.bx-bar.hi .bx-bar-value { color: var(--bx-accent); }
.bx-split-head { display: flex; align-items: center; gap: 26px; }
.bx-split-head .bx-disc { width: 104px; height: 104px; flex: none; }
.bx-split-title { font-size: 46px; font-weight: 700; line-height: 1.12; }
.bx-split-lines { display: flex; flex-direction: column; gap: 22px; margin-top: 40px; }
.bx-split-line { display: flex; gap: 20px; font-size: 36px; line-height: 1.32; }
.bx-split-line i { flex: none; width: 14px; height: 14px; margin-top: 15px; border-radius: 50%; background: currentColor; }
.tone-risk .bx-disc { background: #fde5e7; color: var(--bx-risk); }
.tone-risk .bx-split-line i { color: var(--bx-risk); }
.tone-good .bx-disc { background: var(--bx-tint-2); color: var(--bx-accent-2); }
.tone-good .bx-split-line i { color: var(--bx-accent-2); }
.tone-accent .bx-split-line i { color: var(--bx-accent); }
.tone-muted .bx-disc { background: var(--bx-bg); color: var(--bx-muted); }
.tone-muted .bx-split-line i { color: var(--bx-muted); }
.bx-vs { left: 905px; top: 505px; width: 110px; height: 110px; border-radius: 50%; background: var(--bx-ink); color: var(--bx-bg);
  font-size: 34px; font-weight: 800; display: flex; align-items: center; justify-content: center; }
.bx-list { display: flex; flex-direction: column; gap: 30px; }
.bx-item { display: flex; align-items: center; gap: 34px; font-size: 46px; font-weight: 600; line-height: 1.2; }
.bx-item .bx-num { flex: none; width: 76px; height: 76px; border-radius: 50%; background: var(--bx-tint); color: var(--bx-accent);
  font-size: 34px; font-weight: 800; display: flex; align-items: center; justify-content: center; }
.bx-item .bx-num svg { width: 40px; height: 40px; }
.bx-item .bx-num.now { background: var(--bx-accent); color: var(--bx-on-accent); }

/* keyterm */
.bx-term { font-size: 132px; }
.bx-term-full { font-size: 42px; font-weight: 600; color: var(--bx-accent); margin-top: 16px; }
.bx-term-def { font-size: 42px; line-height: 1.35; margin-top: 46px; color: var(--bx-ink); }
````

````javascript file=assets/bx.js
/*
 * Business explainer runtime: builds every scene from window.BX_DATA and returns ONE paused,
 * seekable GSAP timeline for HyperFrames. All times are absolute film seconds, already resolved
 * from the narrator's word timestamps by scripts/build.py. Deterministic: no clocks, no randomness.
 */
window.BX_BUILD = function () {
  const D = window.BX_DATA;
  const tl = gsap.timeline({ paused: true });
  const cam = document.getElementById("bx-cam");
  const stageEl = document.getElementById("bx-stage");
  const NS = "http://www.w3.org/2000/svg";

  const el = (tag, cls, text, parent) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    if (parent) parent.appendChild(n);
    return n;
  };
  const box = (parent, cls, x, y, w, h) => {
    const n = el("div", "bx-abs " + (cls || ""), null, parent);
    Object.assign(n.style, { left: x + "px", top: y + "px" });
    if (w != null) n.style.width = w + "px";
    if (h != null) n.style.height = h + "px";
    return n;
  };
  const icon = (name) => {
    const s = (D.icons || {})[name];
    return s || (D.icons || {})["circle"] || "";
  };
  const disc = (parent, size, iconName, solid) => {
    const d = el("div", "bx-disc" + (solid ? " solid" : ""), null, parent);
    d.style.width = d.style.height = size + "px";
    d.innerHTML = icon(iconName);
    return d;
  };
  // "*word*" = highlighted (accent colour + tint marker). Returns {words, hls} for animation.
  function rich(node, text) {
    const words = [], hls = [];
    String(text || "").split(/(\*[^*]+\*)/).forEach((part) => {
      if (!part) return;
      if (/^\*[^*]+\*$/.test(part)) {
        const h = el("span", "bx-hl", null, node);
        const bg = el("span", "bx-hl-bg", null, h);
        el("span", "bx-hl-tx", part.slice(1, -1), h);
        words.push(h); hls.push(bg);
      } else {
        part.split(/(\s+)/).forEach((w) => {
          if (!w) return;
          if (/^\s+$/.test(w)) node.appendChild(document.createTextNode(" "));
          else words.push(el("span", "bx-w", w, node));
        });
      }
    });
    return { words, hls };
  }
  const fadeUp = (n, t, d, dy) => tl.fromTo(n, { autoAlpha: 0, y: dy == null ? 26 : dy },
    { autoAlpha: 1, y: 0, duration: d || 0.5, ease: "power3.out" }, t);
  const pop = (n, t, d) => tl.fromTo(n, { autoAlpha: 0, scale: 0.6 },
    { autoAlpha: 1, scale: 1, duration: d || 0.55, ease: "back.out(1.8)" }, t);
  const revealWords = (r, t, step) => {
    r.words.forEach((w, i) => tl.fromTo(w, { autoAlpha: 0, y: 30 }, { autoAlpha: 1, y: 0, duration: 0.45, ease: "power3.out" }, t + i * (step || 0.06)));
    r.hls.forEach((h) => tl.fromTo(h, { scaleX: 0 }, { scaleX: 1, duration: 0.5, ease: "power2.out" }, t + r.words.length * (step || 0.06) * 0.6 + 0.2));
    return t + r.words.length * (step || 0.06);
  };
  const cue = (v, fb) => (typeof v === "number" ? v : fb);
  const num = (v, o) => {
    const dec = o.decimals || 0;
    let [i, f] = Math.abs(Number(v)).toFixed(dec).split(".");
    if (o.group !== false) i = i.replace(/\B(?=(\d{3})+(?!\d))/g, o.groupSep || ",");
    return (Number(v) < 0 ? "−" : "") + i + (f ? (o.decimalSep || ".") + f : "");
  };
  const countUp = (node, from, to, t, len, o) => {
    const steps = Math.max(10, Math.round(len * 24));
    for (let k = 0; k <= steps; k++) {
      const p = k / steps, e = 1 - Math.pow(1 - p, 3);
      tl.set(node, { textContent: num(from + (to - from) * e, o) }, t + p * len);
    }
  };

  // ---------- art: inline unDraw SVG that assembles itself bottom-up ----------
  function art(parent, id, x, y, w, h, t) {
    const b = box(parent, "bx-artbox", x, y, w, h);
    b.innerHTML = (D.art || {})[id] || "";
    const svg = b.querySelector("svg");
    if (!svg) return b;
    svg.removeAttribute("width"); svg.removeAttribute("height");
    svg.setAttribute("preserveAspectRatio", "xMidYMid meet");
    const shapes = Array.from(svg.querySelectorAll("path,rect,circle,ellipse,polygon,polyline,line"));
    const info = shapes.map((s, i) => {
      let bb = { y: 0, height: 0 };
      try { bb = s.getBBox(); } catch (e) {}
      return { s, key: bb.y + bb.height, i };
    }).sort((a, b) => b.key - a.key || a.i - b.i);
    const groups = 22, per = Math.ceil(info.length / groups) || 1;
    for (let g = 0; g * per < info.length; g++) {
      const part = info.slice(g * per, (g + 1) * per).map((o) => o.s);
      tl.fromTo(part, { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: 0.45, ease: "power2.out" }, t + g * 0.055);
    }
    return b;
  }
  function textBlock(parent, s, x, y, w, t0) {
    const tb = box(parent, "bx-text", x, y, w);
    let t = t0;
    if (s.kicker) { fadeUp(el("div", "bx-kicker", s.kicker, tb), t); t += 0.12; }
    if (s.head) { const h = el("div", "bx-head", null, tb); const r = rich(h, s.head); revealWords(r, cue(s.headAt, t), 0.05); }
    if (s.body) fadeUp(el("div", "bx-body", s.body, tb), cue(s.bodyAt, t + 0.5));
    if (s.bullets) {
      const bl = el("div", "bx-bullets", null, tb);
      s.bullets.forEach((bt, i) => {
        const row = el("div", "bx-bullet", null, bl);
        el("i", null, null, row);
        rich(el("span", null, null, row), bt.text);
        fadeUp(row, cue(bt.at, t + 0.7 + i * 0.35), 0.45, 0);
        tl.fromTo(row, { x: -24 }, { x: 0, duration: 0.45, ease: "power3.out" }, cue(bt.at, t + 0.7 + i * 0.35));
      });
    }
    return tb;
  }

  // ---------- scene builders: (container, scene, t0) ----------
  const B = {};
  B.hook = (c, s, t) => {
    const q = box(c, "bx-hook-q bx-display", 160, s.qTop || 250, 1600);
    const end = revealWords(rich(q, s.question), t + 0.15, 0.07);
    if (s.sub) fadeUp(box(c, "bx-hook-sub", 160, s.subTop || 700, 1600, null).appendChild(document.createTextNode(s.sub)) && c.lastChild, cue(s.subAt, end + 0.3));
    tl.fromTo(cam, { scale: 1 }, { scale: 1.06, duration: Math.max(2, s.end - s.start), ease: "none" }, s.start);
  };
  B.title = (c, s, t) => {
    tl.to(cam, { scale: 1, duration: 0.9, ease: "power2.inOut" }, s.start);
    if (s.kicker) fadeUp(box(c, "bx-title-kicker bx-kicker", 160, 300, 1600).appendChild(document.createTextNode(s.kicker)) && c.lastChild, t + 0.1);
    const ti = box(c, "bx-title bx-display", 120, 360, 1680);
    const end = revealWords(rich(ti, s.title), t + 0.25, 0.09);
    tl.fromTo(box(c, "bx-title-bar", 850, 650, 220, 16), { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.out" }, end + 0.1);
    [["circ", 300, 250, 64, "--bx-accent-3"], ["sq", 1540, 280, 54, "--bx-accent-2"], ["circ", 1580, 720, 34, "--bx-accent"],
     ["sq", 340, 760, 40, "--bx-tint"]].forEach(([k, x, y, z, col], i) => {
      const sh = box(c, "bx-shape " + k, x, y, z, z); sh.style.background = `var(${col})`;
      tl.fromTo(sh, { autoAlpha: 0, scale: 0, rotation: -40 }, { autoAlpha: 1, scale: 1, rotation: k === "sq" ? 18 : 0, duration: 0.6, ease: "back.out(2)" }, end + 0.15 + i * 0.1);
    });
  };
  B.illustration = (c, s, t) => {
    const L = s.layout || "left";
    if (L === "center") {
      const blob = box(c, "bx-artblob", 690, 170, 540, 540);
      tl.fromTo(blob, { scale: 0.3, autoAlpha: 0 }, { scale: 1, autoAlpha: 1, duration: 0.7, ease: "back.out(1.4)" }, t);
      art(c, s.art, 460, 150, 1000, 590, cue(s.artAt, t + 0.15));
      const cap = box(c, "bx-caption", 200, 780, 1520);
      if (s.head) revealWords(rich(el("div", "bx-head", null, cap), s.head), cue(s.headAt, t + 0.6), 0.05);
      if (s.body) fadeUp(el("div", "bx-body", s.body, cap), cue(s.bodyAt, t + 1.0));
      return;
    }
    const artX = L === "left" ? 120 : 980, txtX = L === "left" ? 1080 : 160;
    const blob = box(c, "bx-artblob", artX + 130, 230, 600, 600);
    tl.fromTo(blob, { scale: 0.3, autoAlpha: 0 }, { scale: 1, autoAlpha: 1, duration: 0.7, ease: "back.out(1.4)" }, t);
    art(c, s.art, artX, 190, 860, 680, cue(s.artAt, t + 0.15));
    const tb = textBlock(c, s, txtX, 0, 680, t + 0.3);
    tb.style.top = "0px"; tb.style.height = "1080px"; tb.style.justifyContent = "center";
  };
  B.flow = (c, s, t) => {
    if (s.head) revealWords(rich(box(c, "bx-sectionhead bx-head", 160, 170, 1600), s.head), cue(s.headAt, t + 0.1), 0.05);
    const n = s.nodes.length, D0 = s.size || (n > 4 ? 150 : 176), y = s.y || 400;
    const x0 = 180, x1 = 1740, step = (x1 - x0) / n;
    const wires = document.createElementNS(NS, "svg"); wires.setAttribute("class", "bx-wires"); c.appendChild(wires);
    const centers = [];
    s.nodes.forEach((nd, i) => {
      const cx = x0 + step * (i + 0.5); centers.push(cx);
      const node = box(c, "bx-node", cx - 170, y, 340);
      const d = disc(node, D0, nd.icon, nd.solid);
      const lab = el("div", "bx-node-label", null, node); lab.style.fontSize = (n > 4 ? 32 : 36) + "px"; rich(lab, nd.label);
      if (nd.sub) { const sb = el("div", "bx-node-sub", nd.sub, node); sb.style.fontSize = (n > 4 ? 25 : 28) + "px"; }
      if (s.numbered !== false) { const bd = el("div", "bx-badge", String(i + 1), node); bd.style.left = (170 + D0 * 0.32) + "px"; bd.style.top = "-6px"; pop(bd, cue(nd.at, t + 0.3 + i * 0.6) + 0.25, 0.4); }
      const tn = cue(nd.at, t + 0.3 + i * 0.6);
      pop(d, tn); fadeUp(lab, tn + 0.15, 0.45, 18);
      if (nd.sub) fadeUp(lab.nextSibling, tn + 0.3, 0.45, 14);
      if (i > 0) {
        const p = document.createElementNS(NS, "path");
        const xa = centers[i - 1] + D0 / 2 + 18, xb = cx - D0 / 2 - 30, yy = y + D0 / 2;
        p.setAttribute("d", `M${xa} ${yy} L${xb} ${yy}`); p.setAttribute("class", "on"); wires.appendChild(p);
        const len = xb - xa;
        const head = document.createElementNS(NS, "polygon");
        head.setAttribute("points", `${xb + 2},${yy - 13} ${xb + 22},${yy} ${xb + 2},${yy + 13}`); wires.appendChild(head);
        tl.fromTo(p, { autoAlpha: 0, attr: { "stroke-dasharray": len, "stroke-dashoffset": len } }, { autoAlpha: 1, attr: { "stroke-dashoffset": 0 }, duration: 0.45, ease: "power2.inOut" }, tn - 0.45);
        tl.fromTo(head, { autoAlpha: 0 }, { autoAlpha: 1, duration: 0.15 }, tn - 0.05);
      }
    });
  };
  B.hub = (c, s, t) => {
    if (s.head) revealWords(rich(box(c, "bx-sectionhead bx-head", 160, 150, 1600), s.head), cue(s.headAt, t + 0.1), 0.05);
    const cx = 960, cy = s.cy || 600, rx = s.rx || 600, ry = s.ry || 270, R = 230, r = 128;
    const wires = document.createElementNS(NS, "svg"); wires.setAttribute("class", "bx-wires"); c.appendChild(wires);
    const centre = box(c, "bx-node", cx - 170, cy - R / 2, 340);
    const cd = disc(centre, R, s.center.icon, true);
    const tc = cue(s.center.at, t + 0.2);
    pop(cd, tc, 0.7);
    if (s.center.label) {
      const cl = el("div", "bx-node-label", null, centre); cl.style.fontSize = "36px"; rich(cl, s.center.label);
      cl.style.position = "absolute"; cl.style.top = (R + 4) + "px"; cl.style.width = "340px"; fadeUp(cl, tc + 0.3);
    }
    const k = s.spokes.length;
    s.spokes.forEach((sp, i) => {
      const a = -Math.PI / 2 + (2 * Math.PI * (i + (s.offset == null ? 0.5 : s.offset))) / k;
      const x = cx + rx * Math.cos(a), y = cy + ry * Math.sin(a);
      const ts = cue(sp.at, tc + 0.6 + i * 0.35);
      const p = document.createElementNS(NS, "path");
      const ux = x - cx, uy = y - cy, L = Math.hypot(ux, uy);
      const ax = cx + (ux / L) * (R / 2 + 10), ay = cy + (uy / L) * (R / 2 + 10), bx = x - (ux / L) * (r / 2 + 10), by = y - (uy / L) * (r / 2 + 10);
      p.setAttribute("d", `M${ax} ${ay} L${bx} ${by}`); wires.appendChild(p);
      const len = Math.hypot(bx - ax, by - ay);
      tl.fromTo(p, { autoAlpha: 0, attr: { "stroke-dasharray": len, "stroke-dashoffset": len } }, { autoAlpha: 1, attr: { "stroke-dashoffset": 0 }, duration: 0.4, ease: "power2.out" }, ts - 0.25);
      const node = box(c, "bx-node", x - 150, y - r / 2, 300);
      pop(disc(node, r, sp.icon), ts);
      if (sp.label) {
        const lb = el("div", "bx-node-label", null, node); lb.style.fontSize = "28px"; lb.style.marginTop = "12px"; rich(lb, sp.label);
        fadeUp(lb, ts + 0.15, 0.4, 12);
      }
    });
  };
  B.stat = (c, s, t) => {
    const hasArt = !!s.art;
    if (hasArt) {
      const blob = box(c, "bx-artblob", 1110, 240, 580, 580);
      tl.fromTo(blob, { scale: 0.3, autoAlpha: 0 }, { scale: 1, autoAlpha: 1, duration: 0.7, ease: "back.out(1.4)" }, t);
      art(c, s.art, 980, 200, 840, 660, cue(s.artAt, t + 0.15));
    }
    const st = box(c, "bx-stat" + (hasArt ? "" : " bx-center"), hasArt ? 160 : 260, 0, hasArt ? 820 : 1400, 1080);
    if (!hasArt) st.style.alignItems = "center";
    if (s.kicker) fadeUp(el("div", "bx-kicker", s.kicker, st), t + 0.1);
    const v = el("div", "bx-stat-value", null, st);
    const tv = cue(s.valueAt, t + 0.25);
    if (typeof s.value === "number") {
      if (s.prefix) el("span", null, s.prefix, v);
      const dg = el("span", null, num(s.from || 0, s), v);
      if (s.suffix) el("span", null, s.suffix, v);
      fadeUp(v, tv, 0.4); countUp(dg, s.from || 0, s.value, tv, s.countDuration || 1.0, s);
    } else { v.textContent = (s.prefix || "") + s.value + (s.suffix || ""); pop(v, tv, 0.6); }
    if (s.label) fadeUp(rich(el("div", "bx-stat-label", null, st), s.label) && st.lastChild, tv + 0.35);
    if (s.sub) fadeUp(el("div", "bx-stat-sub", s.sub, st), cue(s.subAt, tv + 0.8));
  };
  B.compare = (c, s, t) => {
    const card = box(c, "bx-card", 310, 0, 1300); card.style.padding = "64px 80px";
    const nb = s.bars.length; const h = 150 + nb * 128 + (s.head ? 90 : 0);
    card.style.top = Math.round(560 - h / 2) + "px";
    tl.fromTo(card, { autoAlpha: 0, y: 40 }, { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, t);
    if (s.head) { const hd = el("div", "bx-head", null, card); hd.style.fontSize = "48px"; hd.style.marginBottom = "48px"; rich(hd, s.head); fadeUp(hd, t + 0.2); }
    const wrap = el("div", "bx-bars", null, card);
    const max = s.max || Math.max(...s.bars.map((b) => b.value));
    s.bars.forEach((b, i) => {
      const o = { ...s, ...b };
      const row = el("div", "bx-bar" + (b.highlight ? " hi" : ""), null, wrap);
      const hd = el("div", "bx-bar-head", null, row);
      el("div", "bx-bar-label", b.label, hd);
      const val = el("div", "bx-bar-value", null, hd);
      if (o.prefix) el("span", null, o.prefix, val);
      const dg = el("span", null, num(0, o), val);
      if (o.suffix) el("span", null, o.suffix, val);
      const tr = el("div", "bx-track", null, row);
      const fill = el("div", "bx-fill", null, tr); fill.style.width = Math.max(2, (100 * b.value) / max) + "%";
      const tb = cue(b.at, t + 0.5 + i * 0.45);
      fadeUp(row, tb, 0.4, 16);
      tl.fromTo(fill, { scaleX: 0 }, { scaleX: 1, duration: 0.9, ease: "power3.out" }, tb + 0.1);
      countUp(dg, 0, b.value, tb + 0.1, 0.9, o);
    });
  };
  B.split = (c, s, t) => {
    [[s.left, 160], [s.right, 1000]].forEach(([side, x], k) => {
      const nl = Math.max((s.left.lines || []).length, (s.right.lines || []).length);
      const ch = 300 + nl * 78, cy = Math.round(560 - ch / 2);
      const card = box(c, "bx-card tone-" + (side.tone || (k ? "accent" : "muted")), x, cy, 760, ch);
      card.style.padding = "64px 64px"; card.style.boxSizing = "border-box";
      const ts = cue(side.at, t + 0.15 + k * 1.2);
      tl.fromTo(card, { autoAlpha: 0, y: 50 }, { autoAlpha: 1, y: 0, duration: 0.6, ease: "power3.out" }, ts);
      const hd = el("div", "bx-split-head", null, card);
      disc(hd, 104, side.icon || "circle");
      rich(el("div", "bx-split-title", null, hd), side.title);
      const ls = el("div", "bx-split-lines", null, card);
      (side.lines || []).forEach((ln, i) => {
        const o = typeof ln === "string" ? { text: ln } : ln;
        const row = el("div", "bx-split-line", null, ls); el("i", null, null, row); rich(el("span", null, null, row), o.text);
        fadeUp(row, cue(o.at, ts + 0.45 + i * 0.3), 0.4, 14);
      });
    });
    if (s.vs !== false) {
      const vs = box(c, "bx-vs", 905, 495, 110, 110); vs.textContent = s.vs || "vs";
      pop(vs, cue(s.right.at, t + 1.35) - 0.2, 0.5);
    }
  };
  B.list = (c, s, t) => {
    const n = s.items.length;
    const blk = box(c, "bx-list", 330, 0, 1260);
    const h = (s.head ? 130 : 0) + (s.kicker ? 50 : 0) + n * 106;
    blk.style.top = Math.round(570 - h / 2) + "px";
    if (s.kicker) fadeUp(el("div", "bx-kicker", s.kicker, blk), t + 0.1);
    if (s.head) { const hd = el("div", "bx-head", null, blk); hd.style.fontSize = "64px"; hd.style.marginBottom = "20px"; revealWords(rich(hd, s.head), cue(s.headAt, t + 0.15), 0.05); }
    const rows = s.items.map((it, i) => {
      const row = el("div", "bx-item", null, blk);
      const b = el("div", "bx-num", null, row);
      if (s.check || it.check) b.innerHTML = icon("check"); else b.textContent = it.badge || String(i + 1);
      rich(el("div", null, null, row), it.text);
      return { row, b, t: cue(it.at, t + 0.6 + i * 0.5) };
    });
    rows.forEach((o, i) => {
      fadeUp(o.row, o.t, 0.45, 0); tl.fromTo(o.row, { x: -34 }, { x: 0, duration: 0.5, ease: "power3.out" }, o.t);
      tl.fromTo(o.b, { scale: 0.4 }, { scale: 1, duration: 0.5, ease: "back.out(2)" }, o.t);
      tl.set(o.b, { attr: { class: "bx-num now" } }, o.t);
      if (i > 0) tl.set(rows[i - 1].b, { attr: { class: "bx-num" } }, o.t);
    });
  };
  B.keyterm = (c, s, t) => {
    const blk = box(c, "bx-stat", 260, 0, 1400, 1080); blk.style.alignItems = "center"; blk.style.textAlign = "center";
    if (s.icon) pop(disc(blk, 150, s.icon), t + 0.1);
    if (s.icon) blk.lastChild.style.marginBottom = "36px";
    if (s.kicker) fadeUp(el("div", "bx-kicker", s.kicker, blk), t + 0.15);
    const tm = el("div", "bx-term bx-display", null, blk); revealWords(rich(tm, s.term), cue(s.termAt, t + 0.25), 0.08);
    if (s.full) fadeUp(el("div", "bx-term-full", s.full, blk), cue(s.fullAt, t + 0.7));
    if (s.definition) { const d = el("div", "bx-term-def", null, blk); rich(d, s.definition); fadeUp(d, cue(s.definitionAt, t + 1.1)); }
  };
  B.quote = (c, s, t) => {
    const qm = box(c, "bx-qmark", 900, 160, 120, 120); qm.textContent = "“"; pop(qm, t + 0.1);
    const q = box(c, "bx-quote bx-head", 260, s.top || 340, 1400);
    revealWords(rich(q, s.text), cue(s.textAt, t + 0.3), 0.06);
  };
  B.end = (c, s, t) => {
    const e = box(c, "bx-end bx-display", 120, 380, 1680);
    const end = revealWords(rich(e, s.title), t + 0.2, 0.09);
    if (s.sub) fadeUp(box(c, "bx-end-sub", 160, 560, 1600).appendChild(document.createTextNode(s.sub)) && c.lastChild, end + 0.3);
    tl.fromTo(box(c, "bx-title-bar", 850, 670, 220, 16), { scaleX: 0 }, { scaleX: 1, duration: 0.7, ease: "power3.out" }, end + 0.5);
  };
  B.blank = () => {};

  // ---------- background, label, progress ----------
  const DUR = D.duration;
  tl.fromTo(".bx-blob.b1", { x: 0, y: 0 }, { x: -60, y: 40, duration: DUR, ease: "sine.inOut" }, 0);
  tl.fromTo(".bx-blob.b2", { x: 0, y: 0 }, { x: 70, y: -30, duration: DUR, ease: "sine.inOut" }, 0);
  const lab = document.getElementById("bx-label");
  tl.set(lab, { autoAlpha: 0, textContent: "" }, 0);
  const prog = document.getElementById("bx-progress");
  const pShow = D.scenes.filter((s) => !["hook", "title", "end"].includes(s.type));
  if (D.progress !== false && pShow.length) {
    const p0 = pShow[0].start, p1 = pShow[pShow.length - 1].end;
    tl.fromTo(prog, { scaleX: 0 }, { scaleX: 1, duration: p1 - p0, ease: "none" }, p0);
    tl.to(prog, { autoAlpha: 0, duration: 0.4 }, p1);
  } else prog.style.display = "none";

  let cur = "";
  D.scenes.forEach((s, i) => {
    const c = el("div", "bx-scene", null, stageEl);
    c.dataset.scene = s.id;
    const t0 = s.start;
    tl.set(c, { visibility: "visible" }, t0);
    (B[s.type] || B.blank)(c, s, t0 + 0.05);
    if (i < D.scenes.length - 1 && !s.keep) {
      tl.to(c, { autoAlpha: 0, y: -24, duration: 0.4, ease: "power2.in" }, Math.max(t0 + 0.6, s.end - 0.42));
      tl.set(c, { visibility: "hidden" }, s.end);
    }
    const want = ["hook", "title", "end"].includes(s.type) ? "" : (s.chapter || "");
    if (want !== cur) {
      if (cur) tl.to(lab, { autoAlpha: 0, duration: 0.25 }, Math.max(0, t0 - 0.3));
      if (want) { tl.set(lab, { textContent: want }, t0); tl.fromTo(lab, { autoAlpha: 0, x: -16 }, { autoAlpha: 1, x: 0, duration: 0.45, ease: "power2.out" }, t0 + 0.05); }
      cur = want;
    }
  });
  tl.set({}, {}, DUR);
  return tl;
};
````

````html file=assets/template.html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <title>{{TITLE}}</title>
    <script src="gsap.min.js"></script>
    <link rel="stylesheet" href="tokens.css" />
    <link rel="stylesheet" href="bx.css" />
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-fps="{{FPS}}" data-duration="{{DURATION}}">
      <div id="bx-clip" class="clip" data-start="0" data-duration="{{DURATION}}" data-track-index="1">
        <div id="bx-cam">
          <div class="bx-blob b1"></div>
          <div class="bx-blob b2"></div>
          <div class="bx-dots"></div>
          <div id="bx-stage"></div>
        </div>
        <div id="bx-label"></div>
        <div id="bx-progress"></div>
      </div>
    </div>
    <script>
      window.BX_DATA = {{DATA_JSON}};
    </script>
    <script src="bx.js"></script>
    <script>
      window.__timelines = window.__timelines || {};
      window.__timelines["main"] = window.BX_BUILD();
    </script>
  </body>
</html>
````

````python file=scripts/bxlib.py
"""Shared helpers for the business explainer toolkit."""
import glob, json, os, re, shutil, wave
import numpy as np

ROOT = os.path.expanduser("~/.biz-explainer")
SR = 24000


def write_wav(path, x, sr=SR):
    x = np.clip(np.asarray(x, np.float32), -1, 1)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def read_wav(path):
    w = wave.open(path)
    return np.frombuffer(w.readframes(w.getnframes()), "<i2").astype(np.float32) / 32768


def est_words(say, dur):
    """Word onsets spread by character position (draft timing, or a line without timestamps)."""
    words = say.split(); out, pos, total = [], 0, max(1, len(say))
    for w in words:
        i = say.find(w, pos); out.append({"w": w, "t": round(dur * i / total, 3)}); pos = i + len(w)
    return out


def norm(w):
    return re.sub(r"[^a-z0-9%$€£]+", "", w.lower().replace("’", "'").replace("'", ""))


def accent_from_tokens(work):
    p = os.path.join(work, "tokens.css")
    if not os.path.exists(p): p = os.path.join(ROOT, "assets", "tokens.css")
    m = re.search(r"--bx-accent:\s*(#[0-9a-fA-F]{6})", open(p).read())
    return m.group(1) if m else "#5b4fe9"


def browser():
    if os.environ.get("HYPERFRAMES_BROWSER_PATH"): return os.environ["HYPERFRAMES_BROWSER_PATH"]
    cands = (glob.glob("/opt/pw-browsers/chromium_headless_shell-*/chrome-linux/headless_shell")
             + glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium_headless_shell-*/chrome-linux/headless_shell"))
             + glob.glob("/opt/pw-browsers/chromium-*/chrome-linux/chrome")
             + ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"]
             + [shutil.which(n) or "" for n in ("google-chrome", "chromium", "chromium-browser")])
    return next((c for c in cands if c and os.path.exists(c)), None)


def hf_env():
    env = dict(os.environ); b = browser()
    if b: env["HYPERFRAMES_BROWSER_PATH"] = b
    return env
````

````python file=scripts/voices.py
#!/usr/bin/env python3
"""Narration for the business explainer: one ElevenLabs narrator on fal (elevenlabs/tts/eleven-v4).

    python3 voices.py cost  WORK                 # characters per line + estimated cost
    python3 voices.py jobs  WORK [--only 3,7]    # submit_jobs input batches (8 per call), index = beat number
    python3 voices.py collect WORK REPLY_FILE...  # saved wait_for_jobs replies -> WORK/eleven.json (merges)
    python3 voices.py build WORK [--check]        # eleven.json -> audio/, voice_only.wav, timing.json
    python3 voices.py draft WORK                  # free: estimated timing + silence, for layout previews

timing.json word times are relative to each beat's start; build.py resolves scene cues from them.
--check transcribes every line with offline Whisper (sherpa-onnx, if installed) so you read what a listener hears.
"""
import json, os, subprocess, sys, tempfile, urllib.request
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bxlib import SR, write_wav, read_wav, est_words

RATE = 0.08  # USD per 1,000 characters, Eleven v4 on fal (Oct 2026) - confirm with get_pricing


def load(work):
    return json.load(open(f"{work}/script.json"))


def cost(work):
    S = load(work); n = 0
    for i, b in enumerate(S["beats"]):
        c = len((b.get("say") or "").strip()); n += c
        print(f"beat {i + 1:2d} {c:4d}  {(b.get('say') or '')[:80]}")
    words = sum(len((b.get("say") or "").split()) for b in S["beats"])
    print(f"\n{n} characters, {words} words (~{words / 140 * 60:.0f} s at 140 wpm) -> ~${n / 1000 * RATE:.2f} at ${RATE}/1k chars")


def jobs(work, only):
    S = load(work); voice = S.get("voice", "George"); out = []
    for i, b in enumerate(S["beats"]):
        say = (b.get("say") or "").strip()
        if not say or (only and i + 1 not in only): continue
        out.append({"index": i + 1, "input": {"text": say, "voice": voice, "language_code": S.get("language", "en"),
                                                  "output_format": "mp3_44100_192", "timestamps": True}})
    for k in range(0, len(out), 8):
        print(json.dumps(out[k:k + 8]))
    print(f"# {len(out)} lines in {(len(out) + 7) // 8} submit_jobs calls (endpoint elevenlabs/tts/eleven-v4)", file=sys.stderr)


def collect(work, files):
    p = f"{work}/eleven.json"; R = json.load(open(p)) if os.path.exists(p) else {}
    for f in files:
        t = open(f).read(); d = json.loads(t[t.index("{"):])
        for j in d.get("jobs", []):
            if j.get("status") != "completed":
                print("not completed:", j.get("index"), j.get("status")); continue
            if "result" in j and j["result"].get("audio"):
                R[str(j["index"])] = {"url": j["result"]["audio"]["url"], "timestamps": j["result"].get("timestamps")}
            elif j.get("media"):
                R[str(j["index"])] = {"url": j["media"][0]["url"], "timestamps": None}
    json.dump(R, open(p, "w"))
    print(len(R), "lines ->", p, "| without timestamps:", sorted((k for k, v in R.items() if not v["timestamps"]), key=int))


def words_from(ts, offset):
    chars, starts = [], []
    for ch in ts or []:
        chars += ch.get("characters", []); starts += ch.get("character_start_times_seconds", [])
    out, cur, t0 = [], "", None
    for c, s in zip(chars, starts):
        if c.isspace():
            if cur: out.append({"w": cur, "t": round(max(0.0, t0 - offset), 3)}); cur = ""
        else:
            if not cur: t0 = s
            cur += c
    if cur: out.append({"w": cur, "t": round(max(0.0, t0 - offset), 3)})
    return out


def asr():
    try:
        import sherpa_onnx as so
    except ImportError:
        print("(no sherpa-onnx: --check skipped)"); return None
    d = os.path.expanduser("~/.cache/asr/sherpa-onnx-whisper-base.en")
    if not os.path.isdir(d): print("(no Whisper model: --check skipped)"); return None
    return so.OfflineRecognizer.from_whisper(encoder=f"{d}/base.en-encoder.onnx", decoder=f"{d}/base.en-decoder.onnx",
                                             tokens=f"{d}/base.en-tokens.txt", num_threads=4)


def hear(rec, x):
    from scipy.signal import resample_poly
    s = rec.create_stream(); s.accept_waveform(16000, resample_poly(x, 2, 3).astype(np.float32))
    rec.decode_stream(s); return s.result.text.strip()


def assemble(work, line):
    """line(i, say) -> (samples, words). Lays the beats out with gaps and writes timing.json."""
    S = load(work)
    lead, gap, tail = float(S.get("lead_in", 0.6)), float(S.get("gap", 0.4)), float(S.get("tail", 1.8))
    os.makedirs(f"{work}/audio", exist_ok=True)
    t, chunks, beats = lead, [np.zeros(int(lead * SR), np.float32)], []
    for i, b in enumerate(S["beats"]):
        say = (b.get("say") or "").strip()
        x, words = line(i, say) if say else (np.zeros(0, np.float32), [])
        dur = len(x) / SR
        pause = float(b.get("pause", gap)) + max(float(b.get("min", 0)), dur) - dur
        write_wav(f"{work}/audio/beat_{i + 1:02d}.wav", x)
        beats.append({"i": i, "start": round(t, 3), "speech": round(dur, 3), "end": round(t + dur + pause, 3), "words": words})
        chunks += [x, np.zeros(int(pause * SR), np.float32)]
        print(f"beat {i + 1:2d} {t:6.2f}s {dur:5.2f}s  {say[:72]}")
        t += dur + pause
    chunks.append(np.zeros(int(tail * SR), np.float32))
    write_wav(f"{work}/voice_only.wav", np.concatenate(chunks))
    json.dump({"duration": round(t + tail, 3), "beats": beats}, open(f"{work}/timing.json", "w"), indent=1)
    print(f"narration {t + tail:.2f}s -> timing.json, voice_only.wav")


def build(work, check):
    R = json.load(open(f"{work}/eleven.json")); rec = asr() if check else None

    def line(i, say):
        r = R.get(str(i + 1))
        if not r: raise SystemExit(f"no ElevenLabs render for beat {i + 1}: submit it (voices.py jobs WORK --only {i + 1})")
        with tempfile.TemporaryDirectory() as d:
            try: subprocess.run(["curl", "-sSLf", "-o", f"{d}/a.mp3", r["url"]], check=True)
            except Exception: urllib.request.urlretrieve(r["url"], f"{d}/a.mp3")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{d}/a.mp3", "-ac", "1", "-ar", str(SR), f"{d}/a.wav"], check=True)
            x = read_wav(f"{d}/a.wav")
        nz = np.nonzero(np.abs(x) > 0.01)[0]
        s0 = max(0, nz[0] - int(0.03 * SR)) if len(nz) else 0
        s1 = nz[-1] + int(0.08 * SR) if len(nz) else len(x)
        x = x[s0:s1]
        words = words_from(r["timestamps"], s0 / SR) if r.get("timestamps") else est_words(say, len(x) / SR)
        if rec: print(f"          heard: {hear(rec, x)}")
        return x, words
    assemble(work, line)


def draft(work):
    def line(i, say):
        dur = max(0.8, len(say) / 13.5)  # ~140 wpm
        return np.zeros(int(dur * SR), np.float32), est_words(say, dur)
    assemble(work, line)
    print("DRAFT timing (silent): for layout previews only; voice the script before the real render")


if __name__ == "__main__":
    cmd, work = sys.argv[1], sys.argv[2]
    if cmd == "cost": cost(work)
    elif cmd == "jobs":
        only = set(int(x) for x in sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
        jobs(work, only)
    elif cmd == "collect": collect(work, sys.argv[3:])
    elif cmd == "build": build(work, "--check" in sys.argv)
    elif cmd == "draft": draft(work)
    else: raise SystemExit(__doc__)
````

````python file=scripts/undraw.py
#!/usr/bin/env python3
"""Prepare an unDraw illustration the user downloaded by hand: recolour it to the brand and clean it for animation.

    python3 undraw.py IN.svg WORK/art/ID.svg [--accent #hex] [--from #hex] [--ink #hex] [--info]

- unDraw's license allows commercial use without attribution, but forbids automated downloading, scraping,
  integrations, AI training and redistributing the illustrations in packs. So this toolkit NEVER fetches from
  undraw.co: the user downloads each SVG on the site and drops it in WORK/undraw/. Keep those files local;
  don't publish them as a pack (e.g. in a shared kit artifact).
- --accent: the brand colour (default: --bx-accent from WORK/tokens.css or the toolkit default).
- --from: the illustration's accent colour to replace (default: unDraw's #6c63ff; if absent, the most used
  saturated colour). --ink remaps unDraw's dark ink (#2f2e41, #3f3d56) to e.g. the token ink.
- --info prints the colour histogram only.
Also: strips scripts/handlers/comments, guarantees a viewBox, prefixes ids so two SVGs never clash.
"""
import collections, colorsys, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bxlib import accent_from_tokens

HEX = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


def full(h):
    h = h.lstrip("#").lower()
    return "#" + ("".join(c * 2 for c in h) if len(h) == 3 else h)


def sat(h):
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return colorsys.rgb_to_hls(r, g, b)[2]


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    src, dst = sys.argv[1], sys.argv[2]
    s = open(src, encoding="utf-8").read()
    hist = collections.Counter(full(m.group(0)) for m in HEX.finditer(s))
    if "--info" in sys.argv:
        for c, n in hist.most_common(): print(f"{c} {n:5d}  sat {sat(c):.2f}")
        return
    work = os.path.dirname(os.path.dirname(os.path.abspath(dst)))
    accent = full(arg("--accent", accent_from_tokens(work)))
    frm = arg("--from")
    if not frm:
        frm = "#6c63ff" if "#6c63ff" in hist else next((c for c, _ in hist.most_common() if sat(c) > 0.45), None)
    frm = full(frm) if frm else None
    # sanitise
    s = re.sub(r"<\?xml.*?\?>|<!--.*?-->|<!DOCTYPE.*?>", "", s, flags=re.S)
    s = re.sub(r"<script.*?</script>", "", s, flags=re.S | re.I)
    s = re.sub(r"\son\w+\s*=\s*(\"[^\"]*\"|'[^']*')", "", s)
    s = re.sub(r"(xlink:)?href\s*=\s*\"(?!#)[^\"]*\"", "", s)
    # viewBox
    m = re.search(r"<svg\b[^>]*>", s)
    tag = m.group(0)
    if "viewBox" not in tag:
        w = re.search(r'width="([\d.]+)', tag); h = re.search(r'height="([\d.]+)', tag)
        if w and h: s = s.replace(tag, tag[:-1] + f' viewBox="0 0 {w.group(1)} {h.group(1)}">', 1)
    # recolour
    n = 0
    if frm:
        s, n = re.subn(re.escape(frm), accent, s, flags=re.I)
        if len(frm) == 7 and frm[1::2] == frm[2::2]:  # short form too (#66f)
            s, n2 = re.subn("#" + frm[1::2] + r"\b", accent, s, flags=re.I); n += n2
    ink = arg("--ink")
    if ink:
        for c in ("#2f2e41", "#3f3d56"): s = re.sub(re.escape(c), full(ink), s, flags=re.I)
    # unique ids
    pre = re.sub(r"\W", "", os.path.splitext(os.path.basename(dst))[0]) + "_"
    ids = set(re.findall(r'\bid="([^"]+)"', s))
    for i in sorted(ids, key=len, reverse=True):
        s = s.replace(f'id="{i}"', f'id="{pre}{i}"').replace(f"#{i})", f"#{pre}{i})").replace(f'"#{i}"', f'"#{pre}{i}"')
    os.makedirs(os.path.dirname(os.path.abspath(dst)), exist_ok=True)
    open(dst, "w", encoding="utf-8").write(s.strip() + "\n")
    shapes = len(re.findall(r"<(path|rect|circle|ellipse|polygon|polyline|line)\b", s))
    print(f"{os.path.basename(dst)}: {shapes} shapes, accent {frm} -> {accent} ({n} uses)"
          + ("" if frm else "  WARN no accent colour found; run --info and pass --from"))


if __name__ == "__main__":
    main()
````

````python file=scripts/build.py
#!/usr/bin/env python3
"""script.json + timing.json -> WORK/film/ (a HyperFrames project), with every cue resolved to film seconds.

    python3 build.py WORK

A beat with "show" starts a new scene; the scene lasts until the next beat with "show".
Cue values (any key "at" or ending in "At"): "word" / "two words" (first match from the scene's first beat
on), "word+0.4" (positive offsets only), "end" (scene end - 1 s), or a number = seconds after the scene start.
Prints a scene table and WARN lines. Fix every WARN before rendering.
"""
import difflib, json, os, re, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bxlib import ROOT, norm

ICON_DIR = os.path.join(ROOT, "vendor", "node_modules", "lucide-static", "icons")
LIMITS = {"question": 60, "title": 28, "head": 60, "body": 140, "label": 34, "sub": 40, "text": 46, "term": 22,
          "full": 50, "definition": 110, "kicker": 32}
warns = []


def warn(m):
    warns.append(m); print("WARN", m)


def main(work):
    S = json.load(open(f"{work}/script.json")); T = json.load(open(f"{work}/timing.json"))
    beats, tb = S["beats"], T["beats"]
    if len(beats) != len(tb): raise SystemExit("timing.json is out of date: rerun voices.py (build or draft)")
    words = []  # (abs time, norm word, beat index)
    for i, b in enumerate(tb):
        for w in b["words"]: words.append((b["start"] + w["t"], norm(w["w"]), i))
    starts = [i for i, b in enumerate(beats) if b.get("show")]
    if not starts or starts[0] != 0: raise SystemExit("beat 1 must have a \"show\" scene")
    scenes, icons, arts = [], set(["circle", "check"]), set()
    for k, bi in enumerate(starts):
        nxt = starts[k + 1] if k + 1 < len(starts) else None
        s = dict(beats[bi]["show"]); s["id"] = s.get("id") or f"s{k + 1:02d}_{s.get('type')}"
        s["start"] = round(tb[bi]["start"] - (0.15 if bi else 0), 3)
        s["end"] = round(tb[nxt]["start"] - 0.15, 3) if nxt is not None else T["duration"]
        last = (nxt - 1) if nxt is not None else len(beats) - 1
        pool = [w for w in words if bi <= w[2] <= last]

        def resolve(v, where):
            if isinstance(v, (int, float)): return round(s["start"] + v, 3)
            if v == "end": return round(s["end"] - 1.0, 3)
            m = re.match(r"^(.*?)(?:\+([\d.]+))?$", str(v)); phrase, off = m.group(1), float(m.group(2) or 0)
            target = [norm(x) for x in phrase.split() if norm(x)]
            for j in range(len(pool) - len(target) + 1):
                if [pool[j + q][1] for q in range(len(target))] == target: return round(pool[j][0] + off, 3)
            spoken = " ".join(w[1] for w in pool)
            close = difflib.get_close_matches(" ".join(target), [" ".join(w[1] for w in pool[j:j + len(target)]) for j in range(len(pool))], 3, 0.6)
            warn(f"scene {s['id']}: cue '{v}' ({where}) not spoken in this scene; close: {close or '-'}; scene says: {spoken[:90]}")
            return None

        def walk(o, path):
            if isinstance(o, dict):
                for key in list(o):
                    v = o[key]
                    if (key == "at" or key.endswith("At")) and isinstance(v, (str, int, float)):
                        r = resolve(v, path + key)
                        if r is None: del o[key]
                        else:
                            o[key] = r
                            if r > s["end"] - 0.6: warn(f"scene {s['id']}: {path + key} lands {r - s['end']:+.1f}s from the scene end; it will barely show")
                    elif key == "icon" and isinstance(v, str): icons.add(v)
                    elif key == "art" and isinstance(v, str): arts.add(v)
                    elif isinstance(v, str) and key in LIMITS and len(v.replace("*", "")) > (90 if s["type"] == "quote" and key == "text" else LIMITS[key]):
                        warn(f"scene {s['id']}: {path + key} is {len(v)} chars (aim <= {LIMITS[key]}): '{v[:50]}'")
                    else: walk(v, path + key + ".")
            elif isinstance(o, list):
                for i, x in enumerate(o):
                    if isinstance(x, str) and path.endswith("lines.") and len(x) > 46: warn(f"scene {s['id']}: {path}{i} is {len(x)} chars (aim <= 46)")
                    walk(x, f"{path}{i}.")
        walk(s, "")
        for key, mx in (("nodes", 5), ("spokes", 8), ("items", 6), ("bars", 4), ("bullets", 4)):
            if len(s.get(key, [])) > mx: warn(f"scene {s['id']}: {len(s[key])} {key} (max {mx})")
        if s["end"] - s["start"] < 2.5: warn(f"scene {s['id']}: only {s['end'] - s['start']:.1f}s on screen")
        scenes.append(s)
    # icons and art
    icon_svgs, names = {}, sorted(f[:-4] for f in os.listdir(ICON_DIR)) if os.path.isdir(ICON_DIR) else []
    for n in sorted(icons):
        p = os.path.join(ICON_DIR, n + ".svg")
        if os.path.exists(p):
            icon_svgs[n] = re.sub(r"<!--.*?-->", "", open(p).read(), flags=re.S).strip()
        else:
            warn(f"icon '{n}' not in Lucide; close: {difflib.get_close_matches(n, names, 4, 0.5)}")
    art_svgs = {}
    for a in sorted(arts):
        p = os.path.join(work, "art", a + ".svg")
        if os.path.exists(p): art_svgs[a] = open(p, encoding="utf-8").read()
        else: warn(f"art '{a}' missing: run undraw.py on the user's download -> art/{a}.svg")
    # project
    film = os.path.join(work, "film"); os.makedirs(os.path.join(film, "fonts"), exist_ok=True)
    A = os.path.join(ROOT, "assets")
    for f in ("bx.js", "bx.css"): shutil.copy(os.path.join(A, f), film)
    shutil.copy(os.path.join(work, "tokens.css") if os.path.exists(os.path.join(work, "tokens.css")) else os.path.join(A, "tokens.css"), os.path.join(film, "tokens.css"))
    shutil.copy(os.path.join(ROOT, "vendor", "node_modules", "gsap", "dist", "gsap.min.js"), film)
    for f in os.listdir(os.path.join(A, "fonts")): shutil.copy(os.path.join(A, "fonts", f), os.path.join(film, "fonts"))
    if os.path.isdir(os.path.join(work, "fonts")):
        for f in os.listdir(os.path.join(work, "fonts")): shutil.copy(os.path.join(work, "fonts", f), os.path.join(film, "fonts"))
    data = {"duration": T["duration"], "progress": S.get("progress", True), "scenes": scenes, "icons": icon_svgs, "art": art_svgs}
    html = open(os.path.join(A, "template.html")).read()
    html = (html.replace("{{TITLE}}", S.get("topic", S.get("name", "Explainer"))).replace("{{FPS}}", str(S.get("fps", 30)))
            .replace("{{DURATION}}", f"{T['duration']:.3f}").replace("{{DATA_JSON}}", json.dumps(data).replace("</", "<\\/")))
    open(os.path.join(film, "index.html"), "w", encoding="utf-8").write(html)
    json.dump({"scenes": [{k: s[k] for k in ("id", "type", "start", "end")} for s in scenes]}, open(os.path.join(work, "plan.json"), "w"), indent=1)
    print(f"\n{'scene':24s} {'type':12s} {'start':>7s} {'end':>7s}  chapter")
    for s in scenes: print(f"{s['id']:24s} {s['type']:12s} {s['start']:7.2f} {s['end']:7.2f}  {s.get('chapter', '')}")
    print(f"\nfilm/index.html  {T['duration']:.1f}s, {len(scenes)} scenes, {len(icon_svgs)} icons, {len(art_svgs)} illustrations, {len(warns)} WARN")


if __name__ == "__main__":
    main(sys.argv[1])
````

````python file=scripts/mix.py
#!/usr/bin/env python3
"""Theme music under the narrator with automatic ducking -> WORK/narration.wav (what render.py muxes).

    python3 mix.py WORK [music.mp3] [--level 0.55]
Short film (fits the theme): music throughout, fuller in pauses, dipping whenever the narrator speaks.
Long film: theme intro under hook, title card and first narration beat, then faded out; the theme's last
22 s (its resolving outro) lands under the closing thought and end card; the middle is voice only.
Audio is narrator + theme only: no sound effects.
"""
import json, subprocess, sys
work = sys.argv[1]
music = next((a for a in sys.argv[2:] if a.endswith((".mp3", ".wav", ".m4a"))), f"{work}/music.mp3")
level = float(sys.argv[sys.argv.index("--level") + 1]) if "--level" in sys.argv else 0.55
T = json.load(open(f"{work}/timing.json")); D = T["duration"]
mdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", music],
                            capture_output=True, text=True).stdout)
if D > mdur + 5:
    intro_end = (T["beats"][2]["start"] if len(T["beats"]) > 2 else 15) + 6
    outro, at = 22.0, max(intro_end + 5, D - 22.0)
    bed = f"{work}/music_bed.wav"
    f = (f"[0:a]atrim=0:{intro_end + 3:.2f},afade=t=out:st={intro_end:.2f}:d=3,asetpts=N/SR/TB[a];"
         f"[1:a]atrim={mdur - outro:.2f}:{mdur:.2f},asetpts=N/SR/TB,afade=t=in:d=3,adelay={int(at * 1000)}|{int(at * 1000)}[b];"
         f"[a][b]amix=inputs=2:normalize=0:duration=longest,apad,atrim=0:{D:.2f}[out]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", music, "-i", music, "-filter_complex", f, "-map", "[out]", bed], check=True)
    music = bed
    print(f"long film: theme intro to {intro_end:.1f}s, outro from {at:.1f}s")
f = (f"[0:a]aresample=48000,asplit=2[v][key];[1:a]aresample=48000,volume={level},apad[m];"
     "[m][key]sidechaincompress=threshold=0.02:ratio=8:attack=40:release=500:makeup=1[md];"
     f"[v][md]amix=inputs=2:normalize=0:duration=first,afade=t=out:st={max(0, D - 2.5):.2f}:d=2.5,alimiter=limit=0.95[out]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{work}/voice_only.wav", "-i", music, "-filter_complex", f,
                "-map", "[out]", "-ac", "1", "-ar", "48000", f"{work}/narration.wav"], check=True)
print("mixed ->", f"{work}/narration.wav")
````

````python file=scripts/render.py
#!/usr/bin/env python3
"""Snapshot, review sheet, render and mux.

    python3 render.py WORK --preview         # review_sheet.png only (each scene fully built), ~20 s
    python3 render.py WORK [--quality looks] # full: silent HyperFrames render + narration.wav -> out/<name>.mp4

The review sheet shows every scene 0.7 s before it leaves (when everything in it has appeared).
Run the full render in the background: roughly 1-3 min per minute of film.
"""
import glob, json, os, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bxlib import hf_env
from PIL import Image, ImageDraw


def sheet(work):
    P = json.load(open(f"{work}/plan.json"))["scenes"]
    times = [round(max(s["start"] + 0.5, s["end"] - 0.7), 2) for s in P]
    snap = f"{work}/snaps"
    for f in glob.glob(f"{snap}/*"): os.remove(f)
    r = subprocess.run(["npx", "-y", "hyperframes", "snapshot", f"{work}/film", "--at", ",".join(map(str, times)), "--no-end",
                        "-o", snap], capture_output=True, text=True, env=hf_env())
    files = sorted(glob.glob(f"{snap}/frame-*.png"))
    if not files: raise SystemExit("snapshot failed:\n" + r.stdout[-1500:] + r.stderr[-1500:])
    cols, w, h = 3, 640, 360
    rows = (len(files) + cols - 1) // cols
    out = Image.new("RGB", (cols * w + (cols + 1) * 12, rows * (h + 34) + 12), "#222")
    d = ImageDraw.Draw(out)
    for k, (f, s) in enumerate(zip(files, P)):
        im = Image.open(f).convert("RGB").resize((w, h))
        x, y = 12 + (k % cols) * (w + 12), 12 + (k // cols) * (h + 34)
        out.paste(im, (x, y)); d.text((x + 4, y + h + 6), f"{k + 1}. {s['id']}  {s['start']:.1f}-{s['end']:.1f}s", fill="#ddd")
    os.makedirs(f"{work}/out", exist_ok=True); out.save(f"{work}/out/review_sheet.png")
    print("review sheet ->", f"{work}/out/review_sheet.png", f"({len(files)} scenes)")


def render(work, quality):
    S = json.load(open(f"{work}/script.json")); name = S.get("name", "explainer")
    os.makedirs(f"{work}/out", exist_ok=True)
    silent = f"{work}/out/{name}_silent.mp4"
    cmd = ["npx", "-y", "hyperframes", "render", f"{work}/film", "-o", silent, "--fps", str(S.get("fps", 30)), "--quality", quality, "--quiet"]
    r = subprocess.run(cmd, env=hf_env(), capture_output=True, text=True)
    if r.returncode or not os.path.exists(silent): raise SystemExit("render failed:\n" + r.stdout[-2000:] + r.stderr[-2000:])
    audio = f"{work}/narration.wav" if os.path.exists(f"{work}/narration.wav") else f"{work}/voice_only.wav"
    final = f"{work}/out/{name}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", audio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", final], check=True)
    os.remove(silent)
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", final], capture_output=True, text=True).stdout.strip()
    print(f"-> {final} ({float(d):.1f}s, audio: {os.path.basename(audio)})")


if __name__ == "__main__":
    work = sys.argv[1]
    sheet(work)
    if "--preview" not in sys.argv:
        render(work, sys.argv[sys.argv.index("--quality") + 1] if "--quality" in sys.argv else "looks")
````
