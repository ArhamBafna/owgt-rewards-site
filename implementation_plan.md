# Goal Description

The objective is to manually correct the massive data extraction flaws and inconsistencies found in `organized-data`, strictly **without using Python scripts**. This includes fixing file naming conventions, recovering skipped bookmarks, extracting missing tools and prompts from PDFs, and fixing mangled AI skill files.

## User Review Required

> [!WARNING]
> This is a massive data entry and extraction task. Since Python scripts are forbidden, I will be manually extracting over 100 knowledge objects (tools, prompts, guides) by reading the raw files and using file-writing tools to create each Markdown file individually. This will take time and may require multiple sequential operations. Please confirm this is exactly how you want me to proceed.

## Open Questions

> [!IMPORTANT]
> 1. Do you want me to extract **all** 50+ missing tools from the PDFs, or just the most valuable ones? 
> 2. For the 40+ skipped bookmarks, should I process every single valid tool (e.g. Willow, DictaFlow) and create a full Markdown page for each?
> 3. Are PowerShell commands acceptable for simple file renaming (e.g., removing the `-md.md` suffix from the Skool guides), or do you want me to do that completely manually via IDE tools?

## Proposed Changes

### Skool Guides
- Fix the redundant `-md.md` suffix on all 8 files in `organized-data/Guides`.

### AI Skills
- Rename `aiethics-and.md` to `ai-ethics-and-governance.md`
- Rename `aipresentation.md` to `ai-presentation.md`
- Rename `aivideo-and-visual-content.md` to `ai-video-and-visual-content.md`
- Rename `ai-powered-processdocumentation.md` to `ai-powered-process-documentation.md`
- Extract the 2 missing AI skills from the "19 AI Skills" PDF (`ai-tool-evaluation-and-selection.md`, etc.).

### Missing Bookmarks
- Create new Tool/Guide files for missing items: Willow, DictaFlow, OpenWhispr, Bytez, Z-Image AI, Uncensored AI, Hunyuan Video, Radiant Shaders, AnimeJS, Uiverse, Hover.dev, React Bits, Bklit UI, TrustMRR, Starter Story, Namecheap/GitHub Education offers, etc.

### Missing PDF Tools & Prompts
- Read "41 AI Tools", "21 AI Tools", and "Tool Stack" PDFs. Create the missing ~50 tool files manually.
- Read the Claude Prompts PDFs. Create the missing ~21 prompt files manually.

## Verification Plan

### Automated Tests
- Run `hard_test.py` (already existing) to ensure no structural headers or lazy descriptions were introduced during the manual creation process.

### Manual Verification
- Verify that `master.md` and `master.json` are regenerated after all files are created to ensure the new objects are indexed.
- Verify total counts in `Tools`, `Prompts`, and `Learning` directories meet the expected numbers from the raw data.
