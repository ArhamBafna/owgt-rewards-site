### Name
The AI Research System: A Three-Phase Method

### Description
A systematic three-phase methodology for conducting high-quality, verifiable research using multiple AI models (Perplexity, Grok, Claude, ChatGPT) to avoid hallucinations and generate actionable insights.

### Content

The output quality of AI research is not determined by which model you use, but by whether you have a process at all. Using one model as your only source is using a single, fallible voice as your entire evidence base. 

A better approach is a three-phase process where each phase uses a different tool for a specific job: Gather, Analyze, and Output.

#### Phase 1: Gather
*The goal is source discovery, web research, market data, and current events. You are looking for sourced, traceable starting material, not AI opinions.*

- **Perplexity**: Search-first AI that always cites sources. It links every answer to the original source material.
  - *Best Practice*: Ask specific questions. Instead of "Tell me about competitor X", ask: "What has competitor X announced in the last 90 days? What do their recent job postings suggest about their strategic direction? Cite all sources."
- **Grok**: For real-time intelligence. Connected directly to X data. Use this to track fast-moving markets, competitor announcements, or regulatory developments that haven't been indexed by search engines yet.

*Phase 1 Output*: A set of raw, sourced notes, links, and data points ready for synthesis.

#### Phase 2: Analyze
*The goal is summarizing findings, identifying patterns, synthesizing across sources, extracting key points, and pressure-testing interpretations.*

- **Claude**: Built for long-form thinking, identifying patterns, and synthesizing across multiple sources.

**Key Synthesis Prompts for Claude:**
- **Research Synthesis**:
  > I have gathered the following research on [topic]. Synthesize it into a briefing of no more than one page covering: the three most important findings, what these findings mean for our business specifically, the key areas of uncertainty or conflicting evidence, and the one or two questions that still need to be answered before we can act with confidence. Research: [paste in your phase one notes]
- **Competitive Intelligence**:
  > Build me a competitive intelligence brief on [competitor]. Based on the following sources and what you know, cover: their current product positioning and how it has changed recently, pricing strategy and packaging, go-to-market approach and primary channels, known strengths and vulnerabilities, recent signals about their strategic direction, and one or two things they are likely to do next. Sources: [paste in your phase one notes]
- **Industry Trend Analysis**:
  > Analyze the following trends affecting [your industry]: [list what you found]. For each trend: how material it is likely to be in the next two to three years, whether it represents a threat or an opportunity for our business specifically, what leading companies in our space are doing in response, and what we should be doing now to either capitalize on or protect against it.

**Common Mistakes to Avoid:**
1. **Trusting first outputs**: Always ask Claude to identify the weakest assumption in its own analysis.
2. **Weak prompting**: Specificity separates useful synthesis from generic summaries.
3. **Shallow sourcing**: Phase two cannot fix poor data from phase one. Always verify factual claims against primary sources.

#### Phase 3: Output
*The goal is turning synthesized insights into a tailored deliverable (reports, memos, briefings).*

- **Claude**: Best for reports, memos, strategy documents, written briefs, and anything requiring voice and judgment.
- **ChatGPT**: Best for structured formats, data-heavy summaries, and content where pattern/completeness matters more than prose quality.

**The Output Prompt:**
> I have the following research that I need to present to [audience, leadership, board, client, team]: [describe or paste in your phase two synthesis]. Help me turn this into a narrative that: opens with the single most important finding, builds the supporting evidence in a logical sequence, explains what the data means for our strategy or decisions, and closes with a clear recommendation or call to action. The audience cares most about: [describe what matters to them]

### Category
Guides
### Tags
- Research
- Workflow
- Perplexity
- Claude
- ChatGPT
