# Build Insane Animated Websites — Full Setup Guide

## Setup — Connect Higgsfield MCP to AI

1. Sign up at Higgsfield AI (`https://higgsfield.ai/mcp`).
2. Copy MCP URL.
3. In settings, add custom connector and paste URL.
4. Complete quick auth flow.
5. All image/video models accessible directly (Nano Banana Pro for images, Seedance 2.0 for 4K video).

## Core Principle

**Generate visual assets first. Build site around them.**
Avoid placeholder images. Generating real assets first establishes exact dimensions, color palette, and visual weight.

## Iterative Feedback Loop

First render rarely final. Give specific, sequential feedback:
- Logo on two lines -> Make logo single line.
- Can angle wrong -> Face can directly to camera.
- Color transitions rough -> Improve flavor scroll transition.

---

## Build 1 — RISE Hydration Drink

### Overview
Animated marketing site for premium hydration drink brand.

### Tech Stack
- Single-page site: React, Vite, Tailwind CSS
- GSAP + ScrollTrigger (scroll animation)
- Three.js (r128 for 3D elements)
- Lenis (smooth scroll)
- Framer Motion (micro-interactions)

### Section Layout
1. Hero
2. Product Showcase
3. Seedance Video Reveal (Mid-scroll)
4. Ingredients / Benefits
5. Hydration Science
6. Flavor Spin Section
7. CTA / Footer

### Flavor Variants
- Berry (Red)
- Lime / Citrus (Green)
- Mango / Citrus (Orange)
- Blue Raspberry / Electrolyte (Blue)

### Asset Generation Workflow
1. Berry cluster hero image.
2. Master hero can: sleek look, condensation, studio lighting, gradient backdrop.
3. 4 flavor variants: image-to-image from master can (identical lighting/framing, distinct color identity).
4. Ingredient/particle imagery (electrolytes, fruit, water splashes) with background removed.
5. Abstract liquid and gradient background textures.
6. Cinematic hero video (Seedance 2.0 at 4K): slow-motion can with water burst, color-matched, loopable.

### Key Animations
- **3D Scroll:** Can rotates, tilts, and translates through scene on scroll with parallax background layers.
- **Mouse Tracking:** Hero elements and 3D can subtly track cursor position; custom animated cursor.
- **Interactive Particles:** Water droplets and ingredient particles react to cursor hover/proximity.
- **Flavor Spin Section:** Pinned section where scrolling spins can on vertical axis and morphs flavor color sequentially (Red -> Green -> Orange -> Blue). Can color crossfades at each turn, syncing background accent and text labels.
- **Mid-Scroll Video Reveal:** Video framed element scales/fades to full-bleed on scroll entry, plays splash animation, then releases scroll. Headline text split cleanly above and below video frame.

### Product Ad & Pre-Flight Check
1. Generate video of person drinking product, holding product toward camera with locked flavor identity.
2. Run clip through Virality Predictor to evaluate hook strength, attention curve, and retention risk.
3. Place video near page end, immediately before final CTA.

### Deployment
Deploy to production via Vercel.

---

## Build 2 — Zinho Automates

### Overview
Scrollytelling interactive narrative covering the origin story of an AI automation YouTube creator (@zinhoautomates).

### Tech Stack
- React, Vite, Tailwind CSS
- GSAP + ScrollTrigger (scrubbed, pinned scenes)
- Lenis (smooth scroll)
- Framer Motion (micro-interactions)
- Three.js (r128) for depth elements

### Rules for Personal Assets
- User photo stored locally in `public/` directory, used as static asset.
- Never run personal photo through generative image/video models.
- Generative tools build surrounding background, node convergence, particle halo, and world context.

### Story Scenes
1. **Cold Open:** Dark screen, single pulsing glowing node, typing terminal text. Cursor tracking adds micro-motion.
2. **The Spark:** Node branches into connected automation graph on scroll.
3. **Building in Public:** Graph morphs into YouTube play button shape composed of nodes. Stat counters increment on scroll (45K+ subscribers, 16K+ community members). Topic tags fly into view.
4. **The Stack:** Horizontal conveyor displaying core tool/theme cards lighting up sequentially.
5. **The Community:** Nodes multiply into interactive constellation representing community members; points react to cursor proximity.
6. **The Reveal (The Mission):** Abstract avatar dissolves into actual user photo. Surrounding nodes and energy lines converge toward photo, forming ambient halo. Seedance 4K video plays full-bleed in background.
7. **Invitation / CTA:** Animated logo mark resolves with ambient particle backdrop. Links to YouTube channel and community.

### Design Language
- Dark background with glowing neon accents.
- Scrubbed, reversible scroll progress tied to GSAP ScrollTrigger.
- Custom animated cursor and interactive ambient particle node system.

---

## Generic Template System

### Universal Workflow Rules
- Build fully animated site around pre-generated visual assets.
- Stack: React, Vite, Tailwind CSS, GSAP + ScrollTrigger, Three.js (r128), Lenis, Framer Motion.
- Real personal photos kept intact without generative modifications; environment built around photo.

### Variant Structure
- **Product / Brand Site:** Hero -> Product Showcase -> Video Reveal -> Features -> Story/Science -> Interactive Product Spin/Morph -> CTA.
- **Personal / Portfolio / Story Site:** Guided interactive documentary scroll through sequential pinned scenes (Cold Open -> Origin -> Stats -> Work/Stack -> Community -> Photo Reveal -> CTA).
