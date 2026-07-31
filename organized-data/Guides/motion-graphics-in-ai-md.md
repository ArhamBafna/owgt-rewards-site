### Name
Motion Graphics with AI — Full Setup & Workflow Guide

### Description
A 3-step workflow for creating custom, high-quality motion graphics directly inside your AI workspace using an MCP connector.

### Content

Create custom, high-quality motion graphics directly inside your AI workspace using an MCP connector and structured prompt templates.

---

## Quick Start

#### What You Need
- **Higgsfield AI Account:** Sign up on their site.
- **AI Tool / Coding Assistant:** Fitted with custom Higgsfield MCP connector.

#### 3-Step Workflow
1. **Generate Prompt:** Describe style and topic to main AI Chat.
2. **Build with AI Coding Assistant:** Paste prompt into AI Coding Assistant. Tell it "Build it".
3. **Save Output:** Get final video folder.

---

## Part 1: One-Time Setup

1. Make account on Higgsfield.
2. Copy custom MCP URL inside Higgsfield.
3. Open AI Settings $\rightarrow$ Customize $\rightarrow$ Add Custom Connector $\rightarrow$ paste MCP URL.
4. Finish simple auth flow.

MCP setup done. Image and video models now ready inside AI Coding Assistant.

---

## Part 2: Prompt Generator (AI Chat Template)

Use template inside main AI Chat. Fill in brackets to make prompt for AI Coding Assistant.

#### Master Prompt Generator

```text
You are writing a single, self-contained build prompt that I will paste into my AI Coding Assistant, which has the Higgsfield MCP connected. The AI will use that prompt to generate a complete narrated motion-graphics video end to end.

TOPIC: [your topic]
TARGET LENGTH: [e.g. 90 seconds]
VISUAL STYLE: [describe the look in concrete nouns — materials, textures, palette, line quality, camera behavior]

Write the build prompt so it contains all of the following, explicitly:

1. STYLE BIBLE
   - A locked style description written so that shot 40 looks identical to shot 1
   - Color palette with specific hex values
   - Texture and material rules
   - Typography rules for on-screen text
   - Camera and motion rules (what moves, what never moves)
   - An explicit "never do this" list to prevent style drift

2. SCRIPT
   - A complete voiceover script, written to be spoken, at the target length
   - Broken into numbered beats
   - Every factual claim marked with [FACT] so I can verify before render

3. SHOT LIST
   - One entry per beat: shot number, duration, what's on screen, what the VO says over it
   - Each shot's image/video generation prompt written out in full
   - The style bible referenced or restated in every single shot prompt

4. ON-SCREEN TEXT
   - Exact wording for every label, number, arrow annotation, and caption
   - Placement notes

5. AUDIO
   - Voiceover generation instructions including tone, pace, and voice character
   - Timing notes so VO and visuals land together

6. ASSEMBLY
   - Instructions to write all assets and the final video to a clearly named local folder

Output the build prompt only. No preamble, no explanation, no commentary. I am pasting it directly into the AI Coding Assistant.
```

---

## Part 3: Style Recipes

Drop recipes into `VISUAL STYLE:` field in generator.

#### Vox-Style Paper Cutout
Paper-cutout collage. Old photos with coarse halftone dots, rough paper edges, soft drop shadow. Elements look like real layers. Hand-drawn arrows in one accent color. Flat muted background, warm paper texture. Data shown as cut-paper bar charts and dotted maps. Text: bold condensed sans, lowercase. Camera: slow 2D pushes and slides. Elements snap in on beat. No 3D, no gradients, no lens flares, no glow.

#### Bright Cartoon
Bright cartoon. Thick outlines, flat colors, high saturation: orange, teal, pink, yellow on clean light background. Round friendly characters, exaggerated shapes. Bouncy motion with squash, stretch, overshoot. Text: chunky round sans. Camera: fast whip transitions, pop-in reveals, bounce on settle. No realistic textures, no dark colors, no slow moves.

#### Whiteboard Doodle
Whiteboard doodle. Clean white board, black dry-erase marker with wobble and variable line weight, drawn on live. One or two accent marker colors for arrows. Simple stick figures and box diagrams. Text: hand-written marker style. Camera: slow pans across wide board, pushes on details. No extra color fills, no photos, no gradients.

#### Pixel Art
Pixel art, 16-bit style. Fixed pixel grid, zero sub-pixel movement. 16 color limit. Dithering for shading. Readable sprites. Text: bitmap font, pixel-perfect, no anti-aliasing. Motion: low frame rate step animation. Camera: hard cuts, grid scrolls. No smooth motion, no modern effects.

#### Isometric Flat Vector
Isometric flat vector. 30-degree isometric view across all shots. Flat colors with soft shadows, no gradients. Muted palette: dusty blue, soft coral, warm grey, one main accent color. Buildings, devices built as blocks. Text: clean geometric sans. Camera: slow isometric drift. No perspective distortion, no complex lighting.

---

#### Custom Style Interrogator Prompt

Not sure about visual style? Run prompt in main AI Chat first:

```text
I want to develop a signature motion-graphics style for my channel. I'm going to describe what I have in mind loosely, and I want you to interrogate it into something precise and reproducible.

Here's the vague version: [describe it however it comes out — references, vibes, half-formed ideas]

Ask me the questions you need to pin down: materials and textures, exact palette, line quality, how things enter and exit frame, camera behavior, typography, and what the style must never do.

Then output a single VISUAL STYLE paragraph, written in concrete physical nouns rather than adjectives, specific enough that a generation model produces the same look on shot 1 and shot 40. Include an explicit "never" list.
```

---

## Part 4: AI Coding Assistant Command

After making prompt in AI Chat, run command in AI Coding Assistant:

```bash
Take that prompt and build it.
```

#### Advanced Command (More Control)
```bash
Take that prompt and build it. Before generating anything, show me the shot list and wait for my approval. Then generate all shots, lock the style reference across every one, generate the voiceover, time the blocks so audio and visuals land together, and write the finished project plus every individual asset to ./[project-name]/
```

---

## Part 5: Extra Workflows

#### Language Translation
```text
Make a version of this video in Spanish. Regenerate the voiceover with a native-sounding delivery in the same tone and pace as the original, retime the blocks to fit the new audio length, translate all on-screen text and re-render the affected shots, and keep the visual style byte-for-byte identical. Write it to ./[project-name]-es/
```

#### Motion Graphic Overlays
```text
I need individual motion-graphic elements to composite over footage I already recorded. Not a full video.

VISUAL STYLE: [paste a style recipe]

Generate these as standalone assets with transparent backgrounds where possible:
1. [e.g. an animated arrow pointing down-left, drawing on over 0.6s, holding, then drawing off]
2. [e.g. a bar chart building from zero to three bars labeled 2019, 2022, 2025]
3. [e.g. a lower-third name plate that slides in from frame left]

For each: specify duration, output at 1080p or higher, and write to ./elements/ with descriptive filenames.
```

#### Product Explainer Video
```text
Build a product explainer video.

PRODUCT: [name and what it actually does]
AUDIENCE: [who's watching and what they currently believe]
THE ONE THING THEY SHOULD UNDERSTAND AFTER WATCHING: [single sentence]
LENGTH: [e.g. 60 seconds]
VISUAL STYLE: [paste a style recipe]

Structure: open on the problem as the audience experiences it, show the mechanism of the solution visually rather than describing it, close on the outcome. No feature lists. Every claim marked [FACT] for my verification.
```

#### Course Lesson Video
```text
Build a course lesson video.

CONCEPT: [what you're teaching]
LEARNER STARTS KNOWING: [prerequisite level — be honest]
LEARNER SHOULD BE ABLE TO DO AFTER: [concrete capability]
LENGTH: [e.g. 4 minutes]
VISUAL STYLE: [paste a style recipe]

Structure it around the one thing learners typically get wrong about this concept. Build the visual metaphor early and return to it. Every claim marked [FACT].
```

---

## Part 6: Two Big Mistakes

#### Mistake 1: Fact Check After Render
Text and numbers on screen look authoritative. Wrong numbers mean re-rendering whole shots. Check facts first.

**Pre-Render Fact-Check Prompt:**
```text
Here is my script. Every claim marked [FACT] needs verification before I render a single frame.

For each one: state whether it's accurate, cite the source, give me the correct figure if it's wrong, and flag anything that's technically true but misleading in context.

Be blunt. I'd rather kill a claim now than regenerate a shot later.

[paste script]
```

#### Mistake 2: Using Default Stock Presets
Presets make videos look generic. Use **Custom Style Interrogator** to build unique look.

---

## Part 7: Alternate Web App Workflow

No AI Coding Assistant? Use Web App:
1. Make prompt in main AI Chat.
2. Open **Higgsfield Explainer** web tool.
3. Paste prompt and pick preset (Pixel Art, Claymotion, Papercraft, Cartoon, Whiteboard, Flat Vector).

### Category
Guides

### Tags
- Skool
- Community
- Guide
