# Knowledge Library Organizer Specification

## Objective

You are organizing a large, messy knowledge library into a clean, human-friendly library that will later power a rewards website for newsletter subscribers.

Your goal is **not** to preserve the existing folder structure.

Your goal is to extract, improve organization, remove redundancy, and produce a high-quality library that is pleasant to browse.

Think in **knowledge objects**, not files.

Files are merely containers. The real value is the knowledge inside them.

Examples of knowledge objects include (but are not limited to):

* Prompts
* Tools
* Guides
* Frameworks
* Workflows
* Playbooks
* Checklists
* Cheat sheets
* Comparisons
* Reference material
* Resources

Whenever you analyze a file, ask:

> "What valuable knowledge exists inside this file?"

rather than

> "Where should this file go?"

---

# NON-NEGOTIABLE RULES

These rules override everything else.

## 1. Preserve the original data

Never modify, rename, delete, move, or overwrite anything inside the original `data` folder.

The original library is the source of truth.

Every change you make must happen inside a new copy.

---

## 2. Create a working copy

Before doing anything else:

Create a copy of the entire data folder.

Name it something similar to:

```
organized-data/
```

(Exact naming is not important.)

All modifications happen ONLY inside this copied folder.

The original data must remain untouched.

---

## 3. Optimize for quality over quantity

Never extract something simply because you technically can.

Instead ask:

> "Would a newsletter subscriber genuinely be happy to receive this?"

If the answer is no, don't include it.

The organized library should feel curated, not dumped.

A smaller, higher-quality library is preferred over a huge mediocre one.

---

## 4. Optimize for humans

The final library should be optimized for a human browsing folders.

Not for preserving the previous hierarchy.

Not for preserving original filenames.

Not for maximizing extracted content.

Everything should feel intuitive.

---

## 5. The suggested structure is NOT fixed

Any folder structure mentioned in this specification is only a starting point.

You have permission to:

* rename folders
* merge folders
* split folders
* create folders
* remove unnecessary folders
* reorganize hierarchy

whenever doing so significantly improves usability.

However:

Do **NOT** make changes merely for consistency or aesthetics.

Every structural change should have a clear usability benefit.

---

# PRIORITY ORDER

Whenever two instructions conflict, obey this order.

1. Never modify original data.
2. Optimize quality over quantity.
3. Preserve valuable information.
4. Improve organization.
5. Reduce duplication.
6. Improve readability.
7. Normalize formatting.
8. Improve naming.

---

# GENERAL PHILOSOPHY

The website should not feel like a folder of random internet downloads.

It should feel like a curated library.

Every item should have a reason to exist.

Every item should provide clear value.

Every folder should make intuitive sense.

Every file should be easy to browse.

---

# KNOWLEDGE EXTRACTION

Every source should be analyzed independently.

Extract reusable knowledge whenever appropriate.

Possible extracted objects include:

* prompts
* tools
* guides
* frameworks
* workflows
* comparisons
* references
* checklists
* playbooks
* cheat sheets

This list is not exhaustive.

If another reusable knowledge type naturally emerges, create it.

Do not force everything into existing folders.

---

# CREATE NEW KNOWLEDGE TYPES WHEN APPROPRIATE

Suppose you discover many items that clearly belong to a new category.

Examples:

* Frameworks
* Workflows
* Comparisons
* Playbooks
* Templates
* Reference Sheets

Create a new top-level folder if it improves organization.

Do not force unrelated content into "Guides."

Likewise, if only a single item exists today but it clearly deserves its own category and likely more items will exist later, creating a dedicated top-level folder is encouraged.

If something is truly unique and doesn't naturally belong anywhere, create an appropriate miscellaneous category rather than forcing it into the wrong one.

---

# DUPLICATES

Avoid duplicates everywhere.

The organized library should contain one canonical version whenever possible.

Duplicate files, prompts, tools, guides, or references should not exist unless there is meaningful value in keeping multiple versions.

---

# DUPLICATE PROMPTS

If two prompts are essentially identical:

Keep only the better version.

If two prompts share the same underlying purpose but contain complementary improvements that do not conflict:

Merge them into one improved standalone prompt.

If merging introduces ambiguity, conflicting instructions, or reduced clarity:

Do not merge.

Instead keep the strongest version.

---

# DUPLICATE TOOLS

If the same tool appears in:

* bookmarks
* PDFs
* Notion
* guides
* anywhere else

Create a single master entry.

Never create duplicate tool pages.

Merge useful information together.

---

# DUPLICATE GUIDES

If multiple guides communicate essentially the same thing:

Merge only if doing so creates a substantially better guide.

Otherwise preserve them separately.

---

# SOURCE ATTRIBUTION

Do NOT include source information anywhere inside organized-data.

Do not mention:

* original filename
* page number
* PDF name
* transcript name
* extraction source

The organized library should appear as a polished standalone collection.

---

# WEB RESEARCH

Minimal web research is permitted.

Only search when necessary to identify:

* what a tool is
* the correct homepage
* basic factual description

Do NOT perform deep research.

Do NOT rewrite content primarily using web knowledge.

The library should remain based on the original data.

---

# MARKDOWN

Everything produced should be Markdown.

Normalize formatting.

Use consistent headings.

Use clean spacing.

Use lists where appropriate.

Use fenced code blocks for prompts.

The goal is readability.

---

# FILE NAMES

Normalize filenames.

Use consistent naming conventions.

Avoid unnecessary punctuation.

Prefer short descriptive names.

Do not rename files merely for cosmetic reasons.

Only rename when the improvement is meaningful.

---

# README FILES

Every major folder should contain a concise README.md explaining:

* what belongs there
* naming conventions (if applicable)
* expected structure

These should remain brief.

Their purpose is navigation.

---

# MASTER INDEX

Create:

```
master.md
```

and

```
master.json
```

Both should index the organized library.

These indexes should make it easy to locate content later.

The JSON should prioritize machine readability.

The Markdown should prioritize human readability.

---

# RELATIONSHIPS

Whenever appropriate, create relationships between knowledge objects.

Examples:

* Prompt → Tool
* Prompt → Guide
* Guide → Framework
* Framework → Checklist
* Tool → Guide

Relationships should contain only names/titles.

Never include explanations inside relationships.

They exist only for navigation.

---

# CATEGORIES VS TAGS

These are different concepts.

Every item should have:

Category:

* one broad category

Tags:

* multiple specific searchable labels

Do not merge these fields together.

Categories organize.

Tags improve discovery.

# KNOWLEDGE OBJECT SCHEMAS

Everything extracted into the organized library should follow standardized schemas whenever applicable. Standardization improves consistency, browsing experience, and future website generation.

Do not force a schema onto content that clearly does not fit. These schemas are defaults, not rigid constraints.

---

# PROMPTS

Prompts should only be extracted if they provide meaningful standalone value.

Simply finding text that begins with "Prompt:" is NOT enough.

Ask:

* Can someone use this without reading the original document?
* Does this solve a meaningful problem?
* Would a newsletter subscriber appreciate receiving this?
* Does it save real time or improve results?

If the answer is no, leave it inside its parent document.

If making it standalone requires extensive invention, rewriting, or guessing, do not extract it.

---

## Prompt Quality Filter

Reject prompts that are clearly low-value.

Examples include:

* generic one-liners
* prompts users would naturally write themselves
* prompts with almost no context
* prompts with no obvious use case
* repetitive prompt templates
* obvious instructions
* extremely outdated prompts
* prompts whose only value comes from surrounding explanation

Prefer medium and high-quality prompts.

The organized library should feel curated.

---

## Prompt Schema

Every standalone prompt should contain:

### Title

Short.

Specific.

Descriptive.

---

### Description

Merge together:

* what it does
* when to use it
* how to use it

Write naturally.

Keep concise.

Only rewrite when necessary.

Preserve the original wording whenever it already makes complete logical sense.

---

### Prerequisites

Only include when genuinely required.

Examples:

* upload resume first
* provide company website
* attach screenshot
* include meeting transcript

If no prerequisites exist, omit the section entirely.

Do NOT write "None."

---

### Prompt

Always place inside a fenced code block.

Preserve wording wherever possible.

Only modify if necessary for:

* standalone usability
* logical consistency
* missing references
* broken context

Never rewrite simply for style.

---

### Category

One broad category.

Examples:

* Writing
* Coding
* Marketing
* Research
* Images
* Video
* Productivity
* Learning

These are examples only.

Create better categories if appropriate.

---

### Tags

Multiple searchable labels.

Include:

* topic
* task
* AI model (only if prompt truly depends on one)
* niche
* industry
* technique

Do not force unnecessary tags.

---

### Relationships

List only names.

Examples:

* Claude
* Cursor
* Cold Email Guide
* Prompt Engineering Basics

No explanations.

---

# TOOLS

The goal is one clean page per tool.

Never create duplicate tool entries.

Merge information naturally.

Do not include unnecessary marketing language.

---

## Tool Schema

### Name

Official name.

---

### Description

A concise paragraph explaining:

* what it is
* primary purpose
* common use cases

Keep useful.

Avoid unnecessary detail.

---

### URL

Prefer homepage.

If homepage lacks essential information:

Documentation may also be included.

GitHub may be included only when it is genuinely useful or represents the primary home of the project.

Ignore:

* Discord
* Twitter
* LinkedIn
* YouTube
* referral links

Normalize URLs whenever possible.

---

### Pricing

Only include when explicitly available inside the existing data.

Never research pricing.

If unavailable:

Simply omit the field.

Do not write:

* Unknown
* Not specified
* N/A

---

### Category

One broad category.

---

### Tags

Multiple searchable labels.

Examples:

* AI
* Open Source
* Image Generation
* Browser
* CLI
* MCP
* Automation

Generate tags automatically.

---

# GUIDES

Guides are intended to teach.

They should remain comprehensive.

Do not aggressively rewrite.

Do not summarize simply to make them shorter.

Preserve knowledge.

Improve usability.

---

## Guide Rules

Preserve:

* intent
* information
* logical flow

Improve only when doing so significantly increases readability.

Acceptable improvements:

* headings
* spacing
* bullet lists
* formatting
* organization
* removing repetition
* fixing obvious formatting mistakes

Avoid stylistic rewriting.

Do not rewrite for the sake of rewriting.

---

## Missing Information

If a guide lacks:

* title
* description

add one.

Keep concise.

Do not invent content beyond what the guide already teaches.

---

# FRAMEWORKS

A framework is not a guide.

Examples:

* decision systems
* evaluation systems
* planning systems
* thinking models

If multiple frameworks exist:

Create a dedicated Frameworks folder.

If only one exists but clearly deserves separation:

Creating a Frameworks folder is encouraged.

---

# WORKFLOWS

Workflows describe sequences of actions.

Examples:

* research workflow
* content workflow
* coding workflow

Do not force them into guides when they naturally function as workflows.

---

# PLAYBOOKS

Playbooks combine:

* strategy
* process
* decision making

Keep separate whenever beneficial.

---

# CHECKLISTS

Checklists should remain concise.

Convert paragraphs into checklists only when doing so clearly improves usability.

---

# COMPARISONS

Examples:

Claude vs GPT

Cursor vs Windsurf

ChatGPT vs Gemini

These should generally remain as standalone comparison resources.

Do not discard them merely because the individual tools have been extracted.

Comparisons provide unique value.

If multiple comparisons exist:

Create a Comparisons folder.

Otherwise they may live inside Miscellaneous or another appropriate knowledge type.

---

# CHEAT SHEETS

Preserve.

Improve formatting only.

Do not expand.

Do not rewrite.

---

# REFERENCE MATERIAL

Reference material includes:

* quick lookups
* tables
* terminology
* syntax references

Keep concise.

Improve formatting.

Avoid rewriting.

---

# MISCELLANEOUS KNOWLEDGE

Not every useful resource fits existing categories.

Rather than forcing something into the wrong folder:

Create an appropriate new category.

Examples include:

* timelines
* taxonomies
* glossaries
* collections
* templates
* examples
* resource packs

If only one truly unique object exists:

Miscellaneous is acceptable.

If several similar objects exist:

Create a dedicated category.

---

# DECISION PRINCIPLE

Never ask:

"What folder did this come from?"

Always ask:

"What type of knowledge is this?"

The answer determines where it belongs.

Folder of origin should have no influence on classification.

# EXTRACTION ALGORITHM

Every file should follow the same high-level workflow.

Never classify based on folder name alone.

Always analyze the content first.

---

# STEP 1 — UNDERSTAND THE FILE

Before extracting anything, determine:

* What is this?
* Why does it exist?
* What value does it provide?
* Is the file itself valuable?
* Or is the value contained only within smaller pieces?

Never begin extracting immediately.

Understand the entire file first.

---

# STEP 2 — IDENTIFY KNOWLEDGE OBJECTS

Identify every reusable knowledge object.

Possible objects include:

* prompts
* tools
* guides
* workflows
* frameworks
* playbooks
* comparisons
* cheat sheets
* checklists
* references
* templates

This list is intentionally open-ended.

Do not force objects into existing categories.

---

# STEP 3 — EVALUATE EACH OBJECT

For every object ask:

### Does it provide standalone value?

If no:

Keep it inside its parent resource.

Do not extract.

---

### Is it duplicated elsewhere?

If yes:

Merge intelligently.

Do not create another copy.

---

### Does extracting it reduce the value of the original resource?

If yes:

Extract the object.

AND preserve the original.

Example:

A PDF teaches AI Research.

Several prompts exist inside.

The prompts are useful individually.

However the PDF still teaches concepts, workflows and context.

Result:

Keep the guide.

Extract the prompts.

---

### If extracting everything leaves no meaningful educational value...

Do not preserve the parent resource.

Example:

A transcript that is almost entirely "Top 50 AI tools."

After extracting every useful tool:

If the transcript provides no additional learning:

Remove it from organized-data.

---

# STEP 4 — IMPROVE

Improve only when improvement has a purpose.

Never rewrite merely because you can.

Acceptable reasons:

* formatting
* readability
* headings
* organization
* standalone usability
* removing repetition

Do not change tone unnecessarily.

---

# STEP 5 — PLACE

After extraction, determine the best destination.

Never ask:

"What folder did this come from?"

Ask:

"What is this knowledge object?"

---

# PDF RULES

Every PDF should be treated individually.

Do not assume PDFs are guides.

Some are:

* prompt collections
* tool collections
* playbooks
* references
* cheat sheets
* workflows
* mixed resources

Understand the document before deciding.

---

## Mixed PDFs

Many PDFs contain several knowledge types.

Example:

AI Research System

Contains:

* explanations
* prompts
* workflows
* tools
* frameworks

Result:

Extract reusable standalone objects.

Keep the guide whenever educational value remains.

---

## Tool Lists

Example:

"50 AI Tools"

Extract:

individual tool entries.

Then ask:

Does the document still teach something?

If yes:

Keep it.

If no:

Remove the document from organized-data.

---

## Prompt Collections

Evaluate each prompt individually.

Never bulk import.

Every prompt must pass the quality filter.

---

## Cheat Sheets

Usually preserve.

Improve formatting only.

---

# SCHOOL GUIDES

Treat these primarily as guides.

Do not dismantle them unnecessarily.

Extract:

* prompts
* tools

only when they become genuinely useful standalone resources.

The guide remains unless extraction removes essentially all educational value.

---

# YOUTUBE TRANSCRIPTS

Never preserve raw transcripts.

Determine whether the knowledge deserves preservation.

---

## Educational Videos

Convert into a polished guide.

Not a transcript.

The guide should feel intentionally written.

Someone should be able to follow it from beginning to end.

Remove:

* filler
* greetings
* sponsor messages
* repeated explanations
* spoken language
* tangents

Preserve:

* ideas
* steps
* workflows
* recommendations

---

## Tool Showcase Videos

Example:

Top AI Tools.

Extract the tools.

Then determine whether any educational value remains.

If not:

Do not preserve the transcript.

---

## Prompt Videos

Extract prompts individually.

Only if they become valuable standalone prompts.

Otherwise keep them inside the guide if the surrounding explanation is essential.

---

# BOOKMARKS

Treat bookmarks as discovery rather than documentation.

Each bookmark should be classified.

---

## Delete Personal Resources

Examples include:

* ChatGPT conversations
* Gmail
* Google Docs
* Google Drive documents
* Calendar
* banking
* shopping
* personal dashboards
* school portals
* Discord invites
* unrelated Reddit pages

This list is illustrative.

Delete similar personal resources from organized-data.

Never touch the originals.

---

## Dead Links

Dead links should not remain inside the organized library.

Instead:

Move them into

archive/

dead-links/

This archive exists only for recovery.

They should not appear inside the main library.

---

## Useful Resources

Determine what each resource actually is.

Examples:

Tool

Documentation

Community

Tutorial

API

Library

MCP

CLI

Open Source Project

AI Website

Reference

Invent better categories whenever appropriate.

---

# GITHUB

Leave untouched.

Do not reorganize.

Do not classify.

Do not extract.

---

# SKILLS

Leave untouched.

Do not reorganize.

Do not classify.

Do not extract.

---

# NOTION

Extract reusable knowledge.

Especially:

* tools
* references

Merge duplicates.

Normalize formatting.

---

# PROMPT FOLDER

Treat this as the primary prompt source.

Still evaluate quality.

Do not assume every stored prompt deserves inclusion.

Run every prompt through the same quality filter used everywhere else.

Standardize every accepted prompt.

---

# TOOL DETECTION

Whenever a tool is mentioned:

Determine whether it deserves extraction.

A passing mention does not require a tool page.

Create tool entries only when the tool itself is presented as something useful.

---

# PROMPT DETECTION

Do not detect prompts using keywords.

Detect them semantically.

Some prompts may never contain the word "prompt."

Some text labeled "prompt" is not useful.

Judge based on usefulness.

---

# GUIDE DETECTION

A guide teaches someone how to accomplish something.

Examples:

How to create AI videos

How to automate research

How to build an MCP server

These generally deserve preservation.

---

# FRAMEWORK DETECTION

Frameworks organize thinking.

Examples:

decision matrices

evaluation systems

mental models

planning systems

Do not convert frameworks into guides simply because they contain steps.

---

# WORKFLOW DETECTION

A workflow explains execution order.

Examples:

research workflow

content pipeline

automation pipeline

coding workflow

Preserve separately whenever appropriate.

---

# COMPARISON DETECTION

Comparison resources remain useful even after extracting individual tools.

Do not discard them.

---

# REVIEW FOLDER

Sometimes classification is genuinely uncertain.

If confidence is too low:

Create an appropriate

needs-review/

or

miscellaneous/

location.

Choose whichever is more suitable.

Do not force uncertain content into the wrong category.

---

# HUMAN-FIRST TEST

Before finalizing any object ask:

If someone browsed this folder six months from now...

Would they immediately understand:

* what this is
* why it exists
* whether it's useful

If not:

Improve organization.

Not content.

---

# FINAL QUALITY TEST

Every item should earn its place.

If removing the item would not noticeably reduce the value of the library...

It probably shouldn't exist.

The finished library should feel intentionally curated rather than automatically generated.

# FOLDER ARCHITECTURE & ORGANIZATION

The following structure is **not a contract**.

It is a starting point.

Reorganize freely whenever doing so clearly improves usability.

Never preserve the original hierarchy simply because it already exists.

Optimize for a human browsing folders.

---

# DESIGN PRINCIPLES

The organized library should feel like a professionally curated knowledge base.

Not an archive.

Not a dump.

Not a backup.

Every folder should answer:

> "Why would someone intentionally browse here?"

If the answer is unclear, reorganize.

---

# PREFERRED STRUCTURE

A structure similar to the following is encouraged:

```text
organized-data/

README.md
master.md
master.json

Prompts/
Tools/
Guides/
Frameworks/
Workflows/
Playbooks/
Comparisons/
Reference/
Cheat Sheets/
Templates/
Resources/
Miscellaneous/
Archive/

README.md
```

Again:

This is only an example.

Create, merge or remove categories whenever appropriate.

---

# ARCHIVE

Archive is **not** a trash can.

Archive exists only for items intentionally excluded from the primary browsing experience.

Examples include:

* dead links
* deprecated resources
* uncertain legacy material

The Archive should remain small.

---

# MISCELLANEOUS

Miscellaneous should never become a dumping ground.

It exists for genuinely unique resources.

If multiple miscellaneous items naturally belong together, create a dedicated category instead.

---

# FOLDER READMEs

Every major folder should include a short README explaining:

Purpose

What belongs here

What generally does not belong here

Keep READMEs concise.

Do not repeat information from this specification.

---

# FILE ORGANIZATION

Avoid folders containing hundreds of files.

If a category grows naturally, introduce logical subcategories.

Example:

Prompts/

Writing/

Coding/

Marketing/

Research/

Video/

Images/

Automation/

Do not over-organize prematurely.

Create additional levels only when they genuinely improve navigation.

---

# FILE NAMING

Names should be:

Consistent

Short

Human-readable

Descriptive

Examples:

Good

```text
cold-email-generator.md
```

Bad

```text
Prompt #27 Final New Version Really Good.md
```

Avoid:

* version numbers
* duplicate suffixes
* unnecessary punctuation
* vague titles

---

# TITLE QUALITY

Titles should immediately explain the resource.

Good:

"Research Paper Summarizer"

Poor:

"Useful Prompt"

Good:

"Claude vs GPT for Coding"

Poor:

"Comparison"

---

# DESCRIPTION QUALITY

Descriptions should answer:

What is this?

Who benefits?

When should it be used?

Keep descriptions concise.

Do not repeat titles.

Avoid marketing language.

Avoid hype.

---

# CATEGORY QUALITY

Categories should remain broad.

Examples:

Writing

Coding

Marketing

Research

Learning

Business

Automation

Images

Video

Productivity

Avoid categories containing only one extremely niche item unless doing so clearly improves navigation.

---

# TAG QUALITY

Tags should improve discovery.

Good tags:

email

resume

claude

automation

cursor

image-generation

spreadsheet

workflow

Avoid:

* complete sentences
* duplicated category names
* unnecessary synonyms

Tags should be specific.

---

# RELATIONSHIPS

Relationships should strengthen navigation.

Examples:

Prompt:

Cold Email Generator

Relationships

Claude

Sales Writing Guide

Email Marketing Framework

Tool:

Claude

Guide:

Cold Outreach

Never invent relationships.

Only connect resources with obvious relevance.

---

# CONTENT CONSISTENCY

Resources covering similar subjects should look structurally similar.

This does NOT mean identical wording.

It means:

Consistent headings

Consistent spacing

Consistent Markdown

Consistent schemas

---

# MARKDOWN STANDARDS

Use:

Proper heading hierarchy

Bullet lists

Numbered lists where sequential

Tables only when clearly beneficial

Code fences for prompts

Horizontal rules where useful

Avoid:

Huge walls of text

Excessive nesting

Over-formatting

Emoji

Marketing callouts

---

# WRITING STYLE

Prefer:

Clear

Direct

Professional

Concise

Educational

Avoid:

Buzzwords

Sales language

Clickbait

Artificial enthusiasm

Corporate jargon

---

# WHAT NOT TO DO

Do not rewrite simply because wording could be slightly improved.

Do not rename simply for consistency.

Do not extract everything possible.

Do not preserve everything possible.

Do not optimize for quantity.

Do not force every resource into existing folders.

Do not create folders that exist only because they sounded like a good idea.

---

# DECISION FRAMEWORK

Whenever unsure, evaluate in this order:

1.

Is this genuinely valuable?

If no:

Exclude.

---

2.

Does it already exist elsewhere?

If yes:

Merge.

---

3.

Can someone understand it independently?

If no:

Keep inside parent.

---

4.

Does extracting it reduce the parent's educational value?

If yes:

Keep both.

---

5.

Does the parent still teach something after extraction?

If yes:

Preserve.

If no:

Remove from organized-data.

---

6.

Does an existing category naturally fit?

If yes:

Use it.

If no:

Create a better category.

---

# FINAL LIBRARY TEST

Imagine someone opens organized-data without seeing the original data folder.

They should never think:

"Where did this come from?"

Instead they should think:

"This feels like a well-designed knowledge library."

Every folder.

Every file.

Every extracted object.

Every guide.

Every prompt.

Every tool.

Should contribute toward that feeling.

---

# SUCCESS CRITERIA

The project is successful if:

✓ Original data remains untouched.

✓ Every modification occurred only inside organized-data.

✓ The library feels intentionally curated.

✓ Duplicate knowledge has been merged.

✓ Valuable knowledge has been preserved.

✓ Low-value content has been filtered out.

✓ Navigation is intuitive.

✓ Every resource has a clear purpose.

✓ Folder organization feels obvious.

✓ Standalone prompts are genuinely reusable.

✓ Guides remain educational.

✓ Tools are consolidated.

✓ Comparisons, frameworks, workflows and other unique knowledge types have appropriate homes.

✓ Category and Tags remain separate.

✓ Relationships improve navigation.

✓ README files make browsing effortless.

✓ master.md and master.json provide complete indexes.

The finished library should resemble a professionally maintained digital knowledge base rather than a collection of downloaded files.

# FINAL VALIDATION & DECISION LOG

Before considering the organization complete, perform a full review of the entire organized library.

Do **not** simply stop after processing every file.

Instead, perform at least one complete validation pass over the finished library.

Treat this as a quality assurance review.

---

# GLOBAL REVIEW

Re-evaluate the library as a whole.

Ask questions such as:

* Are there still duplicate resources?
* Are similar resources organized consistently?
* Does every folder make intuitive sense?
* Are any folders unnecessarily large?
* Are there folders that should be merged?
* Are there folders that should be split?
* Has any valuable content accidentally remained buried inside another resource?
* Has anything been extracted that should have remained in its parent resource?
* Have any low-value resources slipped through?
* Does every remaining item genuinely deserve its place?

If improvements are identified during this review, apply them before finishing.

---

# LIBRARY CONSISTENCY PASS

Verify that resources of the same type follow the same schema.

Examples:

All standalone prompts should use the Prompt schema.

All tools should use the Tool schema.

All guides should follow similar formatting.

Do not rewrite content merely to force consistency.

Consistency should improve usability, not reduce quality.

---

# DUPLICATE PASS

Perform one final duplicate detection pass across the entire library.

Look for duplicates that may have been introduced while processing different source files.

Merge or remove duplicates whenever appropriate.

---

# QUALITY PASS

Review every extracted resource again.

Remove any resource that no longer meets the quality standard.

Always prefer a smaller, higher-quality library over a larger collection containing mediocre content.

---

# NAVIGATION PASS

Browse the organized library mentally as if you were a first-time visitor.

Ask:

* Would I immediately understand this folder?
* Would I know where to find something?
* Are related resources grouped naturally?
* Is anything difficult to locate?

If navigation can be noticeably improved, reorganize before finishing.

---

# DECISION LOG

Create:

```text
decisions.md
```

This file is **not** part of the future website.

It exists solely to summarize the organizational decisions that were made.

Keep it concise.

Do **not** log every individual file.

Instead, summarize meaningful decisions.

Examples include:

* New categories created.
* Categories merged.
* Categories removed.
* Duplicate resources merged.
* Approximate number of low-quality prompts removed.
* New frameworks, workflows or miscellaneous categories created.
* YouTube transcripts converted into guides.
* Parent resources preserved because they retained educational value.
* Parent resources omitted because extraction captured all meaningful knowledge.
* Dead links archived.
* Significant normalization decisions.
* Any content placed into `needs-review`.
* Any assumptions made due to ambiguous content.

Do **not** mention original filenames, PDF names, transcript names, page numbers, or extraction sources.

The Decision Log should describe *what* changed and *why*, not *where it came from*.

---

# FINAL SUCCESS TEST

The project is complete only if all of the following are true:

✓ The original `data` folder remains completely untouched.

✓ All changes occurred only inside `organized-data`.

✓ The organized library feels intentionally curated rather than automatically generated.

✓ Every remaining resource provides meaningful value.

✓ Navigation is intuitive.

✓ Duplicate knowledge has been consolidated.

✓ Low-value content has been filtered out.

✓ Guides remain educational.

✓ Standalone prompts are genuinely reusable.

✓ Tools are consolidated into single canonical entries.

✓ Categories and tags are used consistently.

✓ Relationships improve discovery.

✓ Folder READMEs exist where appropriate.

✓ `master.md` and `master.json` accurately index the library.

✓ `decisions.md` summarizes the major organizational decisions.

Before finishing, ask yourself one final question:

> "If this library were published tomorrow as a premium newsletter reward, would I be proud of its quality?"

If the answer is not an unambiguous **yes**, continue refining the library before considering the task complete.

If you encounter an ambiguous decision that could significantly affect the quality of the final library, stop and ask for clarification instead of making irreversible assumptions at any stage in the process, using /grill-me. You can absolutely challenge my instructions where appropriate.

FOR WHOLE PROMPT: work iteratively:
Process one source (or one logical batch) at a time.

After each batch, ensure:

schemas remain consistent
duplicates are merged
master indexes are updated
relationships are updated

Then STOP and ask me for continuation to next batch.