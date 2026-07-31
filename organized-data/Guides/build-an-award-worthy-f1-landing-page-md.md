### Name
Build an Award-Worthy F1 Landing Page

### Description
Step-by-step instructions for using AI Web Builder and AI Media Generator to scaffold a premium Formula 1 landing page with cinematic visuals.

### Content

## Step 1 — Build the Landing Page in AI Web Builder

Open your AI Web Builder and paste the prompt below. It will scaffold the entire site — hero section, gallery, animations, responsive design — all in about two minutes.

### Prompt #1 — Initial Landing Page Build:
> Create a premium landing page for Formula 1 driver Lewis Hamilton. Include a full-screen hero section with space for a background video element and bold headline text overlay. Add a gallery/showcase section, a stats section with career highlights, a quote section, and a call-to-action section. Use a dark color scheme with racing-inspired accents. Typography should be clean and modern. All sections should have smooth scroll-triggered animations. Make it fully responsive.

Preview the result. The layout will be solid, but the visuals will still look generic. That's what we fix next.

---

## Step 2 — Generate Premium Visuals in AI Media Generator

This is what separates a template from a professional site. AI Media Generator has two tools we'll use:
* **Cinema Studio** — for 360° camera movements (like a car reveal)
* **Road Rush model** — trained specifically on racing footage

### Cinema Studio — Hero Shot
#### Prompt #2 — 360° Car Shot:
> Dramatic 360-degree rotation around a Formula 1 car, studio lighting, dark background, cinematic, high detail

### Gallery Images
#### Prompt #3 — Helmet Close-Up:
> Close-up of an F1 racing helmet, dramatic studio lighting, dark background, sharp detail, cinematic

#### Prompt #4 — Steering Wheel POV:
> F1 steering wheel from driver's POV, cockpit view, carbon fiber detail, professional lighting

#### Prompt #5 — Wide Track Shot:
> Wide shot of a Formula 1 car on track, motion blur background, golden hour lighting, cinematic composition

### Road Rush — Dynamic Racing Video
#### Prompt #6 — Racing Video:
> Dynamic footage of a Formula 1 car at high speed, low camera angle, aggressive motion blur, camera tracking the car, broadcast-quality racing shot

---

## Step 3 — Convert Video to Frames

AI Web Builder can't process video directly, so we convert it to image frames:
1. Go to an online video converter (e.g., ezgif.com)
2. Select **Video to JPG**
3. Upload your hero video
4. Download the folder of sequential JPG frames

---

## Step 4 — Add Visuals to the Website

Upload your generated AI assets into the AI Web Builder (create a folder called `"assets"`), then use this prompt:

### Prompt #7 — Integrating Visuals:
> Integrate the uploaded assets into the website. Use the hero-frames folder as a background video sequence in the hero section with text overlay. Place the gallery images in a three-column grid layout with hover effects. Ensure the hero text has enough contrast to be readable over the video.

---

## Step 5 — Iterate and Polish

This is where you go from "good enough" to award-worthy. Use these prompts one at a time:

### Prompt #8 — Typography Change:
> Change the headline fonts to a bolder, more angular typeface that communicates speed and aggression. Think racing brand typography — punchy, not safe.

### Prompt #9 — Hover Effects:
> Update the gallery card hover effects. Instead of a basic scale-up, add a smooth lift animation where the card rises with a soft drop shadow, like it's accelerating off the page. Make the transition smooth and premium-feeling.

### Prompt #10 — Dark/Light Mode Toggle:
> Add a dark and light mode toggle to the website. Dark mode should feel edgy and sporty with deep blacks, fitting the F1 aesthetic. Light mode should use a cream background for a softer but still sporty look. The transition between modes should be fluid, not abrupt. Include a toggle button in the header.

### Prompt #11 — CTA Button Glow:
> Add a subtle glow effect to the main call-to-action button and make the hover transition faster. It should feel urgent, like you're about to hit the throttle.

---

## Step 6 — Deploy with GitHub + Netlify

1. In your AI Web Builder, click **Publish to GitHub** — it creates a repo and pushes your code.
2. Go to **Netlify** → connect your GitHub account.
3. Select the repository → click **Deploy**.
4. Netlify builds, optimizes, sets up CDN + SSL (~40 seconds).
5. Your site is live with a URL.

To update: make changes in AI Web Builder → push to GitHub → Netlify auto-redeploys. No FTP, no cPanel.

> **Note:** This workflow works for any niche — luxury brands, fitness, tech startups. Swap the visuals and prompts for your niche and follow the same framework.

### Category
Guides

### Tags
- Skool
- Community
- Guide
