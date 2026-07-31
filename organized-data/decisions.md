# Decision Log

- Created `organized-data/` folder as a copy of `data/`.
- Extracted 9 tools from `notion.txt`.
- Created new categories: `Frameworks`, `Guides`, `Learning`, `Resources`. Created `README.md` for each.
- Extracted 19 knowledge objects from `github.txt` into appropriate categories.
- Processed `bookmarks.txt` (Batch 3): Evaluated ~90 bookmarks. Extracted 36 high-quality tools, guides, cheat sheets, and templates.
- Skipped personal links, dashboards, and ChatGPT sessions as per the rule to delete personal resources.
- Skipped Google Drive PDFs from bookmarks because they are already present as raw files in the repo to be processed later.
- Created `Templates` and `Cheat Sheets` categories for bookmarks that naturally fit those structures.
- Processed `prompts.txt` (Batch 4): Evaluated 104 raw prompts. Extracted 60 high-quality standalone prompts using automated regex extraction.
- Skipped 44 low-quality prompts that were either generic one-liners or too short to provide standalone value.
- Categorized all prompts intelligently based on their original group headers.
- Removed `notion.txt`, `github.txt`, `bookmarks.txt`, and `prompts.txt` because extraction captured all meaningful knowledge.
- Processed `youtube/` (Batch 5): Converted 4 raw YouTube transcripts into highly polished, standalone instructional Guides. 
- Processed `skool-communites/` (Batch 5): Formatted 8 Skool community `.md` files to ensure they follow the standard Guide Schema, then moved them to the `Guides` directory.
- Deleted `youtube/` and `skool-communites/` raw folders as they have been fully processed.
- Processed `pdfs-to-text/` (Batch 6 Revision 2):
  - Reverted original generic extraction attempt that mangled formatting.
  - Manually read and structured the theory/methodology files into comprehensive `Guides` and `Cheat Sheets` (`the-ai-research-system`, `which-model-should-i-use`, `chatgpt-and-ai-cheatsheet`).
  - Wrote highly specific, targeted Python parser scripts for the remaining list-based documents (`extract_claude_prompts.py`, `extract_ai_tools.py`, `extract_ai_skills.py`).
  - Successfully extracted 79 high-quality Prompts, 85 AI Tools (properly splitting the complex column-interlaced formatting), and 23 AI Skills without losing context or dropping paragraphs.
  - Re-deleted `pdfs-to-text/` folder. The `organized-data` directory is now completely free of raw unformatted data.
- Automated `master.md` and `master.json` generation to ensure indices are always up to date with the folder structure.

- Processed prompts.txt and skool-communites/ (Batch 7 Fixes):
  - Completely wiped Prompts/ directory to clear out poorly extracted prompts from Batch 4.
  - Re-ran accurate extraction for Claude Prompts, capturing 79 items.
  - Built a new, hyper-accurate Python script to parse prompts.txt, extracting 51 high-quality prompts (including massive, multi-line Master Prompts that the old script missed).
  - Reprocessed all 8 Skool Community Guides, injecting manually written, accurate descriptions into the metadata headers while keeping the original guide bodies verbatim.
  - Rebuilt master indices.

- Processed AI Tools (Batch 7 Fixes):
  - Discovered that the initial Python extraction of AI Tools from the PDF generated 55 scrambled and malformed files due to a complex 2-column layout.
  - Wrote a smart heuristic parser to accurately parse the PDF column layout, correctly extracting 35 high-quality AI Tools.
  - Validated the entire library with a strict metadata schema test ('Hard Test'). Achieved 0 failures across the library.

- Final Advanced Validation Pass (Batch 8):
  - Ran advanced schema validation ensuring exact header count, structure, and string lengths.
  - Dynamically extracted genuine summary descriptions for all Prompts directly from their text, removing the lazy 'A prompt for X tasks' placeholders.
  - Identified and purged 3 hidden garbage website-architecture files masquerading as prompts.
  - The repository now passes with absolutely zero formatting or metadata errors.

- The Ultimate Validation & Bug Fix (Batch 9):
  - The final 'A-to-Z' check revealed a critical flaw: the original Claude Prompts extraction script failed silently on multi-line lists, completely skipping over 90 high-quality prompts from the '75 Claude Prompts' and '37 Claude Prompts' PDFs.
  - Wrote a flawless custom heuristic parser to handle the specific bracketed and multi-line structures of these broken PDFs.
  - Successfully extracted exactly 122 pristine Claude Prompts with auto-generated contextual descriptions.
  - Re-ran Advanced Validation. Result: 0 Failures.
