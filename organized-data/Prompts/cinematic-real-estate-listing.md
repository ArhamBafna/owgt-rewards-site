### Name
Cinematic Real Estate Listing Video

### Description
A master prompt for generating cinematic real estate listing videos using Higgsfield and Claude.

### Prompt
```text
The ONE thing you customize for every listing is the WALKTHROUGH:

you describe how the camera should move through the place. Write that

first (Step 1), then paste the full prompt (Step 2).

================================================================

STEP 1 — WRITE YOUR WALKTHROUGH (how it should go)

================================================================

Describe the camera's route as ONE continuous move, in the order you

want to show the home. This is what makes each video custom. Call out:

- where it starts (outside, the front door, or a key room)

- the order of rooms, and how it moves between them (glide, turn, rise, descend)

- where the furniture unfolds into place

- where to slow down (the selling features: kitchen, view, primary suite)

- how it ends (a hero shot, or back where it started)

Keep it one flowing path. The model follows it as a single continuous shot.

>>> WRITE YOURS HERE:

[ ........................................................... ]

EXAMPLE (Oliver's apartment) — copy this style:

"Start just outside the front door and push in through the entrance.

Glide into the kitchen as the furniture and decor unfold into place.

Continue out into the living room. Turn to the right and look up toward

the staircase, then rise up the stairs. As you reach the top, let the

upstairs interior unfold into place. Drift over toward the desk and

computer setup, then move out over the edge of the landing and descend

back down into the living room to finish."

================================================================

STEP 2 — THE PROMPT (paste into Claude, attach your photo, drop your walkthrough in)

================================================================

Use Higgsfield to create a cinematic real estate listing video from

this photo. Model: Kling 3.0, highest quality mode (pro or 4k), then

upscale the result.

WALKTHROUGH (how the camera should move — paste your Step 1 here):

[ your walkthrough goes here ]

SHOT: one continuous, smooth cinematic walkthrough that follows the

walkthrough above. Slow luxurious motion, seamless forward movement,

subtle parallax, shallow depth of field, decelerating to reveal each

room.

FIDELITY (critical, do not break): stay faithful to the reference

photo. Preserve the exact architecture, layout, furniture, materials,

colors, and proportions shown. Do NOT add, remove, move, or invent

rooms, furniture, windows, doors, or objects. Keep every straight line

straight: no warping or bending of walls, doorframes, counters, or

windows.

LOOK: premium architectural film grade, high dynamic range, natural

realistic textures, soft cinematic color. Golden hour warmth outside

easing into a soft interior glow. Calm, aspirational, expensive.

MOTION FEEL: steady, slow, luxurious. No shaky cam, no fast cuts, no

snap zooms.

FURNITURE REVEAL (marketing flourish, ON by default): as the camera

enters each space, have the furniture and decor elegantly fold/assemble

into place, then settle into the final furnished look.

(Toggle OFF for a fully faithful flythrough when the agent wants exact.)

NEGATIVE / AVOID: no people, no text, no logos, no watermarks, no

warping, no distorted or bending lines, no extra or invented rooms,

no cartoon or fake CGI look, no flicker, no morphing walls.

================================================================

TWO WAYS TO BUILD IT (pick based on the listing)

================================================================

A. ONE CONTINUOUS WALKTHROUGH (the wow factor):

   One generation that follows your whole path. Best when you have a

   strong main photo and want the cinematic, flowing reveal. Anchor it

   with a start photo (and an end photo if you have one).

B. ROOM BY ROOM, THEN STITCH (max accuracy):

   Run the prompt once per real listing photo, give each clip a short

   one-room walkthrough (e.g. "push into the kitchen and slow on the

   island"), then stitch the clips in this order:

   exterior -> entry -> living -> kitchen -> primary bedroom -> bath -> standout feature.

   Use this when the agent needs it to match the real home exactly.

Exterior/aerial beat (either mode): use the REAL exterior photo as the

start frame, OR a real Google Earth Studio aerial of the actual address.

NEVER use an AI-invented exterior.

================================================================

TWEAKABLES (give the buyer control)

================================================================

- Speed: slow & luxurious  OR  energetic & modern

- Time of day / light: golden hour / bright airy daylight / twilight / cozy evening glow

- Furniture: unfold-in (stylized, default)  OR  static (faithful/accurate)

- Mood: calm luxury / vibrant modern / cozy & warm

- Aspect ratio: 16:9 (YouTube + website)  OR  9:16 (Reels / TikTok / Stories)

- Clip length: 5s or 10s

- Quality: Kling 3.0 pro or 4k, then upscale_video

================================================================

QUALITY STEP

================================================================

After it generates, run upscale_video for the final resolution bump.

This is the fix for "I wanted higher quality."
```

### Category
Video

### Tags
- Video
- Prompt
- Real Estate
