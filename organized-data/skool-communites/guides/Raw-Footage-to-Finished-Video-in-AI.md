# Raw Footage to Finished Video — AI Setup & Workflow Guide

Turn raw video clips into captioned, scored, motion-graphic edited final videos directly inside your AI workspace. No Premiere or terminal experience needed.

---

## Overview

### What You Are Building
A single AI setup that takes a raw clip and outputs a captioned, scored, motion-graphic edited video.

### How It Works
- `video-use`: Free open-source skill that reads transcript, finds cut points, and runs the main edit.
- `HyperFrames`: Code-based graphic generator called by `video-use` when visual elements are needed. You only talk to `video-use`.

---

## Setup (One-Time)

1. Copy the `video-use` link from community files.
2. Paste link into AI Code tab and prompt:
   "Read install file first, install repo, set up FFmpeg, register skill, and prompt me for my key when needed."
3. Paste ElevenLabs API key when prompted during first edit run.

---

## Workflow

### 1. Rough Cut
Put raw video into project folder and prompt:
"Start new project for raw clip and make rough cut."

AI uses Scribe for word-level timestamps, flags filler words and pauses, shows cut plan, and waits for approval.

Fix-it prompts:
- "Add a bit more padding before that sentence."
- "Remove the word 'basically' at start of line."

> [!IMPORTANT]
> Lock rough cut before adding graphics to avoid timing misalignment later.

---

### 2. Graphics
Open new chat for graphics phase and prompt:
"Plan motion graphic for each segment, then build."

Refinement prompts:
- "Use primary brand orange instead of default blue."
- "Place logo PNG on intro graphic."
- "Slow down entrance animation speed."

Each tweak only re-renders affected section.

---

### 3. Captions
Prompt:
"Add captions using existing transcript."

Generated using existing Scribe timestamps.

---

### 4. Music
Point AI to audio file and set volume level (recommended **-22 to -23 dB** for background voice balance):
"Add background music using this track at -22 dB."

---

### 5. Export
Prompt:
"Export final video."

Final file saves to downloads directory; source project folder remains intact.

---

## Summary Prompt Reference

| Phase | Command / Prompt |
| :--- | :--- |
| **Setup** | `"Read install file first, install repo, set up FFmpeg, register skill, and prompt me for key when needed."` |
| **Rough Cut** | `"Start new project for raw clip and make rough cut."` |
| **Graphics** | `"Plan motion graphic for each segment, then build."` |
| **Captions** | `"Add captions using existing transcript."` |
| **Export** | `"Export final video."` |

---

## Key Notes

- Word-level Scribe timestamps give accurate cut placement.
- Use natural language prompts for edits instead of manual timeline trimming.
