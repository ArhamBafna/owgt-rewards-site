---
name: skool-guide-to-md
description: Convert raw text guide into generic AI markdown document and save to rewards/data/skool-communites/
---

## Steps

1. **Read Text**: Take user pasted text input.
2. **De-brand Text**: Replace `Claude` or other specific AI name -> `AI` (or generic AI term). Remove vendor lock details. Should not be AI-model specific. 
3. **Format Markdown**: Clean layout, headers, tables, codeblocks. Preserve all text verbatim (except de-branding AI, you can change).
5. **Humanize and Compress**: Run `C:\Users\bafna\.agents\skills\humanise-text\SKILL.md` and `C:\Users\bafna\.agents\skills\caveman\SKILL.md` skills on whole markdown (IMPORTANT!). Preserve details and the actual guide.
4. **Get Filename**: Extract main title from text. Convert spaces to dashes. End with `.md`.
5. **Save**: Write file to `rewards/data/skool-communites/<title-with-dashes>.md`.
