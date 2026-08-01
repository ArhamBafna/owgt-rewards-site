### Name
ChatGPT & AI Cheatsheet

### Description
A complete, dense reference guide for AI prompting, covering universal formulas, techniques, writing styles, and common workflows. 

### Content

#### The Universal Prompt Formula
> Act as **[ROLE]**, perform **[TASK]**, in **[FORMAT]**
> *Example:* "Act as a senior copywriter, write 5 cold-email subject lines for a SaaS launch, in a numbered list with hooks bolded."

#### 1. Roles
Who should the AI pretend to be?
Marketer, Copywriter, SEO specialist, Consultant, Coder, Editor, Analyst, Recruiter, Teacher, Translator, Interviewer, Trainer, CFO, Designer. Or specific people: *"Act like Hormozi / Bezos / Naval"*

#### 2. Tasks
What do you want it to do?
Write caption, Blog post, Email sequence, Sales copy, Product desc, Video script, SEO keywords, Summarize, Translate, Outline, Analyze, Brainstorm, Critique, Refactor.

#### 3. Output Formats
How should the answer look?
Bullet list, Numbered list, Table, CSV, JSON, Markdown, HTML, Summary, Outline, Step-by-step, Pros vs Cons, Tweet thread, Script, Email.

#### Prompting Techniques
- **Zero-shot**: Just ask. No examples. Use for simple, well-known tasks.
- **One-shot**: Give one example before the ask. Sets tone fast.
- **Few-shot**: 3–5 examples. Best for matching a specific style or pattern.
- **Chain-of-Thought**: Add "think step by step." Forces reasoning before the answer.
- **Tree-of-Thought**: "Brainstorm 5 approaches, evaluate each, then pick the best."
- **Role-play**: "You are X." Locks tone, vocabulary, and POV.
- **Chained prompts**: Output of prompt 1 becomes input to prompt 2. Compounds quality.
- **Instructional**: Explicit steps. "First do A, then B, then return C."

#### Clone Your Voice Workflow
1. Paste 2–3 samples of your writing.
2. Ask: *"Analyze the tone and style. Output a bullet-pointed style guide."*
3. Save that style guide as a reusable system prompt.
4. Use it: *"Rewrite [text] using the style guide above."*

#### Chained Workflow (SEO Blog Post)
1. Generate an SEO outline for keyword [topic].
2. Write 10 persuasive headlines from that outline.
3. Draft subheadings for each section.
4. Surface 30 keywords to weave in naturally.
5. Write 15 CTAs.
6. Combine winners into a full draft.
7. Rewrite in the voice of [role / brand].

#### Midjourney Prompt Builder
1. **Prep**: *"I'll give you formatting examples for Midjourney."*
2. **Format**: Paste the Midjourney structure (subject, style, lighting, camera, params).
3. **Samples**: Drop in 2–3 high-quality MJ prompts.
4. **Context**: *"Now generate 5 prompts for [scene]."*
5. **Ship**: Copy → paste into Midjourney.

#### Pro Tips Most People Miss
- Ask for output as CSV or JSON to paste straight into Sheets or code.
- Ingredients > recipes. Feed it your raw data and let it cook.
- Make it argue with itself: *"Now critique that answer harshly."*
- Always fact-check with a second engine (Perplexity, Claude, Gemini).
- *"Ask me 5 questions before answering"* dramatically improves output.
- Save your best prompts as reusable templates.
- For long tasks, ask for a plan first, then approve before execution.

#### AI Glossary
- **Prompt**: The instructions you give the AI.
- **Input**: Text, image, or file you provide.
- **Output**: What the AI gives back.
- **Token**: A chunk of text (~4 chars). Models bill by token.
- **Context**: Everything the model can "see" right now.
- **LLM**: Large Language Model (e.g., GPT-4, Claude, Gemini).
- **Temperature**: Creativity dial. Low = safe, high = wild.
- **Hallucination**: When the AI invents facts confidently.
- **RAG**: Retrieval-Augmented Generation — pulls in real data.

#### When to Use What
- **ChatGPT**: Drafts, brainstorming
- **Claude**: Long docs, analysis, code
- **Perplexity**: Facts + sources
- **Midjourney**: Images
- **Runway / Kling**: Video

### Category
Cheat Sheets

### Tags
- ChatGPT
- Prompting
- Workflow
