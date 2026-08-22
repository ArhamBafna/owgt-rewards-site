### Name
The Code — 50+ Coding Agent Hacks

### Description
A curated directory of 50 practical hacks, configuration patterns, hooks, and workflows for developers building with AI coding agents including Claude Code, Codex, and Cursor.

### Category
Cheat Sheets

### URL
https://hackbook-chi.vercel.app/

### Content

#### Overview
A complete, curated directory of 50 practical hacks, prompts, workflows, and configuration recipes for developers building with Claude Code, OpenAI Codex, and Cursor.

---

### Context & Configuration

#### 1. Pin a CLAUDE.md at repo root
- **Agent(s)**: Claude Code
- **Summary**: A short CLAUDE.md is auto-loaded into every session — use it for repo-specific style, scripts, and gotchas the model can't infer.
- **Details**: Claude Code reads CLAUDE.md from the working directory on every turn. Keep it under ~80 lines: build/test commands, naming conventions, files to avoid, and any non-obvious invariants. It beats memory entries because it's checked into git and applies to every contributor.
```markdown
# CLAUDE.md
## Commands
- \`pnpm dev\` — start dev server
- \`pnpm test -- --watch\` — TDD mode

## Conventions
- Server components by default; mark \`"use client"\` only when needed
- DB access via \`src/db/queries/*\` only — never inline SQL in routes

## Don't touch
- \`generated/\` (codegen output)
- \`migrations/*.sql\` (append-only)
```
- **Source**: https://docs.claude.com/en/docs/claude-code/memory

#### 2. Layer .cursor/rules/*.mdc by scope
- **Agent(s)**: Cursor
- **Summary**: Per-folder .mdc rules with globs beat one giant .cursorrules — the model only sees what's relevant to the file it's editing.
- **Details**: Cursor's modern rule system lets you scope rules with a `globs:` frontmatter field. Put TS conventions in `rules/typescript.mdc` (globs: **/*.ts), API patterns in `rules/api.mdc` (globs: app/api/**), etc. Smaller, more relevant prompts → fewer hallucinated patterns.
```markdown
---
description: API route conventions
globs: app/api/**/*.ts
alwaysApply: false
---
- Validate inputs with zod at the top of the handler
- Return NextResponse.json — never raw Response
- Errors: throw ApiError(status, code, message)
```
- **Source**: https://docs.cursor.com/context/rules

#### 3. Lock down Claude Code's unstable behavior
- **Agent(s)**: Claude Code
- **Summary**: Disable 1M context, adaptive thinking, and auto-memory in settings — and pin the subagent model to Sonnet — for noticeably more reliable runs.
- **Details**: Many users have noticed quality dips driven by bloated context, override settings, and stale auto-memory burning tokens. Ex-Meta/Microsoft engineer Kun Chen shared a settings block that locks these down: hard-pin effort to high, kill the 1M-token mode, switch off adaptive thinking, and disable auto-memory. Restart Claude Code after saving.
```json
// ~/.claude/settings.json
{
  "effortLevel": "high",
  "env": {
    "CLAUDE_CODE_DISABLE_1M_CONTEXT": "1",
    "CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING": "1",
    "CLAUDE_CODE_DISABLE_AUTO_MEMORY": "1",
    "CLAUDE_CODE_SUBAGENT_MODEL": "sonnet"
  }
}
```
- **Source**: https://x.com/kunchenguid

#### 4. Auto-load git context at session start
- **Agent(s)**: Claude Code
- **Summary**: A `SessionStart` hook can dump `git status` to a known file so Claude always knows your branch and uncommitted changes without you typing it.
- **Details**: Claude Code loads CLAUDE.md but doesn't know what branch you're on or what's changed since the last session. You end up typing 'check git status' every time. A `SessionStart` hook fixes this once: it captures git state on session start and on `/clear`, so you can dive straight into work.
```json
// .claude/settings.json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "git status > /tmp/claude-git-context.txt && echo 'Development context loaded'"
      }]
    }]
  }
}
```
- **Source**: https://docs.claude.com/en/docs/claude-code/hooks

#### 5. Feed Claude Code's own docs into context
- **Agent(s)**: Claude Code
- **Summary**: Anthropic publishes a docs map at `claude_code_docs_map.md` — paste the URL and Claude grounds answers in current docs instead of stale training data.
- **Details**: Claude Code ships features faster than its training data updates, so questions about hooks or new flags often get a confidently-wrong answer. Anthropic keeps a markdown map of every docs page at a stable URL. Paste it inline with your question and Claude fetches the map, finds the right page, and answers from real docs.
```bash
https://code.claude.com/docs/en/claude_code_docs_map.md
help me configure hooks
```
- **Source**: https://x.com/dani_avila7

#### 6. Auto-generate a tight CLAUDE.md with /init
- **Agent(s)**: Claude Code
- **Summary**: An experimental `CLAUDE_CODE_NEW_INIT` flag rewrites `/init` to scan your stack, linters, and CI — producing a 60-line CLAUDE.md instead of 400.
- **Details**: Most CLAUDE.md files are written by hand even though Claude can infer most of the content from source. Daniel San surfaced an experimental flag that switches `/init` to a scanning mode: tech stack, linters, CI config — Claude proposes them and you approve before anything is written. His repo went from 458 lines to 68. Still experimental, expect it to change.
```json
// .claude/settings.local.json
{
  "env": {
    "CLAUDE_CODE_NEW_INIT": "1"
  }
}

// Then:
/init
```
- **Source**: https://x.com/dani_avila7

---

### Workflow & Task Management

#### 7. Shift+Tab into Plan Mode for risky changes
- **Agent(s)**: Claude Code
- **Summary**: Plan Mode lets Claude read freely but blocks writes — perfect for discussing approach before any file is touched.
- **Details**: Press Shift+Tab to cycle into Plan Mode. The agent can Read, Grep, and run safe Bash but can't Edit or Write. You get a plan you can approve, redirect, or throw out — without unwinding half-applied changes. Use it for refactors, migrations, or any task where 'measure twice' matters.
```bash
# Toggle modes (Shift+Tab cycles)
1. Default       — full tools
2. Auto-accept   — skips approvals on allowed tools
3. Plan Mode     — read-only until you approve
```
- **Source**: https://docs.claude.com/en/docs/claude-code/overview

#### 8. Fan out independent searches with subagents
- **Agent(s)**: Claude Code
- **Summary**: Spawn multiple Explore agents in one message — they run in parallel and keep their giant tool results out of your main context.
- **Details**: When you need three different searches (auth flow, payment flow, error handling), invoke three Agent tool calls in a single message. They run concurrently and each returns a summary instead of dumping every grep result into the parent conversation. Faster and cheaper.
```json
// All three run in parallel — single assistant message
Agent({ subagent_type: "Explore", prompt: "Find auth middleware" })
Agent({ subagent_type: "Explore", prompt: "Find payment handlers" })
Agent({ subagent_type: "Explore", prompt: "Find error boundaries" })
```
- **Source**: https://docs.claude.com/en/docs/claude-code/sub-agents

#### 9. Codex: split tasks at natural commit boundaries
- **Agent(s)**: Codex
- **Summary**: Codex CLI works best when each task ends in a commitable diff. Don't ask it to 'build the whole feature' — chunk by commit.
- **Details**: The agent's planning quality drops off above ~5 file changes. Frame each task as 'one commit's worth of work': add the schema, then the query, then the route, then the UI. You'll review smaller diffs and the model will stay on-rails.
```bash
# Instead of:
"Build the comments feature."

# Try:
"Step 1: add the comments table to schema.prisma + migration."
# Review, commit. Then:
"Step 2: add createComment + listComments in db/queries/comments.ts."
```
- **Source**: https://github.com/openai/codex

#### 10. Run agents on parallel worktrees, not branches
- **Agent(s)**: Claude Code, Codex, Cursor
- **Summary**: git worktree gives each agent its own checkout — no stash/switch dance, no clobbered uncommitted work.
- **Details**: If you run two agents in one repo on different tasks, one will trash the other's working tree. `git worktree add ../repo-feat-x feat/x` gives you a parallel directory pointing at the same git history. Open one editor per worktree, run one agent per editor.
```bash
git worktree add ../myapp-auth feat/auth
git worktree add ../myapp-billing feat/billing

# Each is a real checkout — open in its own editor + agent
cd ../myapp-auth && claude
cd ../myapp-billing && claude

git worktree list    # see them all
git worktree remove ../myapp-auth   # when shipped
```
- **Source**: https://git-scm.com/docs/git-worktree

#### 11. claude --resume to pick up yesterday's thread
- **Agent(s)**: Claude Code
- **Summary**: Sessions persist locally — `claude --resume` lists prior conversations so you can continue a long-running task days later.
- **Details**: Long features often span multiple days. Don't re-prime context every morning. `claude --resume` shows a picker; choose the right session and the full history is back. Pair with a CLAUDE.md that captures decisions so even a fresh session is well-grounded.
```bash
claude --resume        # interactive picker
claude --continue      # resume the most recent session
claude -c -p "now add the email step"   # one-shot continuation
```
- **Source**: https://docs.claude.com/en/docs/claude-code/cli-reference

#### 12. Spawn parallel subagents for code review
- **Agent(s)**: Codex
- **Summary**: Reviewing your own code with the agent that wrote it just rubber-stamps decisions — explicitly delegate to parallel subagents, each with a different lens.
- **Details**: When the same Codex context that wrote the code reviews it, the reviewer just nods along. OpenAI's docs recommend fanning out to parallel subagents with separate context windows. Use the words 'spawn' or 'delegate in parallel' explicitly — Codex won't parallelize on its own. Drop to gpt-5.4-mini for the subagents to keep costs low.
```bash
Review this branch with parallel subagents.

Spawn one subagent for security risks,
one for test gaps,
and one for maintainability.

Use gpt-5.4-mini for the subagents.
```
- **Source**: https://developers.openai.com/codex

#### 13. Rewind a Codex session by double-tapping Esc
- **Agent(s)**: Codex
- **Summary**: Double-tap Esc with an empty composer to edit your previous message — keep tapping to walk further back, Enter to fork a new branch from there.
- **Details**: Codex CLI has a hidden fix for conversations that go off the rails: with an empty composer, double-tap Esc to enter edit mode on your last message. Keep hitting Esc to walk further back through the transcript. Edit the prompt where things went south and press Enter — Codex forks a new thread from that point and discards everything after.
```bash
Esc Esc          → edit previous message
Esc Esc Esc ...  → walk further back
Enter            → fork from this point
```
- **Source**: https://github.com/openai/codex

#### 14. Promote any session into a reusable slash command
- **Agent(s)**: Claude Code
- **Summary**: After running a workflow once, ask Claude to 'save what we just did into a new skill' — it writes the markdown and you get a slash command for free.
- **Details**: If you find yourself repeating the same prompt sequence — pulling Hacker News articles, generating a changelog, running a release checklist — promote it. Meta engineer John Kim runs the workflow once, then asks Claude to save it as a skill. Claude generates the markdown in `.claude/skills/` and registers a slash command. Extending it later is the same conversational move.
```bash
# Run the workflow once, then:
"Save what we just did into a new skill called fetch-hackernews"

# Later, extend it without editing files:
"Extend this fetch-hackernews skill to also pull from
 Apple developer news"

# Now /fetch-hackernews works from any session.
```
- **Source**: https://docs.claude.com/en/docs/claude-code/overview

#### 15. Run skills in isolated context with `context: fork`
- **Agent(s)**: Claude Code
- **Summary**: Adding `context: fork` and `agent: Explore` to a skill's frontmatter runs it in a subagent — your main thread only sees the final summary.
- **Details**: Without isolation, every tool call inside a skill lands in your main context window. A research skill that reads 20 files clutters the conversation. Two lines of YAML frontmatter — `context: fork` and `agent` — push the skill into a subagent with its own context. `agent: Explore` is read-only and optimized for codebase navigation; you can also use Plan, general-purpose, or any custom agent.
```bash
# .claude/skills/deep-research/SKILL.md
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```
- **Source**: https://x.com/lydiahallie

#### 16. Collapse the PR ritual into one /pr command
- **Agent(s)**: Cursor
- **Summary**: Diff → commit → push → open PR is the same six commands every time. A `.cursor/commands/pr.md` file makes it `/pr`.
- **Details**: Cursor's Head of Education shared a tiny custom command that handles the whole PR ritual. Drop a markdown file at `.cursor/commands/pr.md` describing the steps. Type `/pr` in chat and the agent runs git diff, writes a commit message from the changes, pushes, and uses `gh pr create` to open the PR.
```bash
# .cursor/commands/pr.md
Create a pull request for the current changes.

1. Look at the staged and unstaged changes with \`git diff\`
2. Write a clear commit message based on what changed
3. Commit and push to the current branch
4. Use \`gh pr create\` to open a pull request with title/description
5. Return the PR URL when done
```
- **Source**: https://docs.cursor.com/chat/overview

#### 17. Ask side questions mid-task with /btw
- **Agent(s)**: Claude Code
- **Summary**: Mid-refactor and need to check something? `/btw` answers in a side panel without interrupting the main task or polluting context.
- **Details**: Previously you had to cancel the active response or wait for it to finish before asking 'wait, which config is it reading?'. `/btw` answers from current session context in a side panel — no tool calls, no extra file reads, no entry in conversation history. Dismiss with Space or Escape.
```bash
/btw what was the name of that config file?
```
- **Source**: https://x.com/_trq212

#### 18. Fork a Claude Code session to try a different approach
- **Agent(s)**: Claude Code
- **Summary**: `/fork` branches from the current point so you can experiment without losing context — both threads run independently.
- **Details**: Mid-session you want to try a different approach but don't want to lose your context or pollute the thread with failed attempts. `/fork` branches from the exact point. The same flag works from the CLI when resuming. If the new direction doesn't pan out, close the fork and the original is untouched.
```bash
# In an active session:
/fork

# Or from CLI:
claude --continue --fork-session
```
- **Source**: https://docs.claude.com/en/docs/claude-code/overview

---

### Prompting & Specification

#### 19. Project slash commands as reusable prompts
- **Agent(s)**: Claude Code
- **Summary**: Drop a markdown file in .claude/commands/ and it becomes /your-command — perfect for repeatable workflows.
- **Details**: Anything in `.claude/commands/<name>.md` becomes `/<name>` in the CLI. The file body is the prompt. Use it for code review checklists, release prep, migration writers, anything you'd otherwise paste from Notion. Frontmatter `argument-hint` and `$ARGUMENTS` make them parameterizable.
```markdown
---
description: Generate a migration from a schema diff
argument-hint: <table-name>
---
Look at the current schema for $ARGUMENTS in src/db/schema.ts.
Compare to the latest migration in migrations/.
Write the next migration file. Forward + rollback. Be conservative
with NOT NULL on existing columns.
```
- **Source**: https://docs.claude.com/en/docs/claude-code/slash-commands

#### 20. Pin files to Cursor chat with @ before asking
- **Agent(s)**: Cursor
- **Summary**: @-mention 2-3 representative files before your question — Cursor's retrieval is good but explicit is better for refactors.
- **Details**: For one-off questions, Cursor's auto-context is fine. For multi-file refactors, it under-pulls. Type `@` and pin the entry point, the type definitions, and one usage site. Hit rate on cross-file edits goes way up.
```bash
@src/auth/session.ts @src/auth/types.ts @app/api/me/route.ts

Refactor session reading to use the new SessionContext type.
Update all three files. Keep the existing cookie shape.
```
- **Source**: https://docs.cursor.com/chat/overview

#### 21. Write the spec, then ask the agent to implement
- **Agent(s)**: Claude Code, Codex, Cursor
- **Summary**: A 30-line spec.md beats a 3-line prompt every time — agents follow written specs better than free-form chat.
- **Details**: Drop a `spec.md` next to the code. List: goal, acceptance criteria, files to touch, things to NOT touch, and the test you want passing. Then ask the agent to implement against the spec. You'll catch design issues before code is written and the agent has a checklist it can self-verify against.
```markdown
# spec.md — Add rate limiting

## Goal
Per-user 60 req/min on /api/* — return 429 with Retry-After.

## Acceptance
- [ ] middleware.ts intercepts /api/*
- [ ] Redis-backed (use existing src/redis.ts)
- [ ] Test: 61st req in a minute returns 429
- [ ] Existing /api/health stays unlimited

## Don't touch
- auth middleware (separate concern)
- /api/webhooks (provider retries need no limit)
```
- **Source**: https://docs.claude.com/en/docs/claude-code/overview

#### 22. Paste UI screenshots to pin down design intent
- **Agent(s)**: Claude Code, Cursor
- **Summary**: Drop a screenshot of the broken state (or the Figma frame) directly into the chat — agents are way better at vision-grounded UI work.
- **Details**: Describing 'the button is slightly misaligned' wastes tokens and your time. Cmd+Shift+4 the region, paste it in, and the agent can see the exact pixel issue. Same for matching a Figma comp — paste the frame, ask for a faithful implementation, iterate on diffs of screenshots.
```bash
# Workflow
1. Cmd+Shift+Ctrl+4 (macOS) — copy region to clipboard
2. Paste into Claude Code / Cursor chat
3. "Match this layout. Use existing Tailwind tokens.
    The dev server is running at :3000."
4. Agent edits, you screenshot the result, paste again
   "Closer — the gap above the title should be 24px not 16px"
```
- **Source**: https://docs.claude.com/en/docs/claude-code/overview

#### 23. Force a TODO list before non-trivial work
- **Agent(s)**: Claude Code, Codex
- **Summary**: Open with 'plan this as a TODO list first, then execute' — the agent self-decomposes and you get a checkpoint to redirect.
- **Details**: Without a plan, agents tunnel into the first plausible solution. Asking for a TODO list up front forces them to enumerate the work, which surfaces bad assumptions early. Bonus: the list is visible in the UI as it executes, so you can stop them mid-task instead of waiting for the wrong wall of code.
```bash
Plan this as a checked TODO list first. Don't write code yet.

Once I approve the plan, work through items one at a time.
After each item, briefly say what you did and what's next.

Task: migrate the user profile page from Pages Router to App Router.
```
- **Source**: https://docs.claude.com/en/docs/claude-code/overview

#### 24. Pull live shell output into slash commands with !
- **Agent(s)**: Claude Code
- **Summary**: Prefix a shell command with ! inside a `.claude/commands/*.md` file and Claude runs it first, then injects the output as context.
- **Details**: Most people think slash commands are static. They're not — the `!` prefix makes them dynamic. T3 Chat's Theo Browne shared a `pr-summary` command that pulls the live diff, comment thread, and changed files automatically. Works with any shell command: test results, logs, schema dumps.
```bash
# .claude/commands/pr-summary.md
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !\`gh pr diff\`
- PR comments: !\`gh pr view --comments\`
- Changed files: !\`gh pr diff --name-only\`

## Your task
Summarize this pull request...
```
- **Source**: https://x.com/theo

#### 25. Crank up reasoning with /effort high
- **Agent(s)**: Claude Code
- **Summary**: Claude has been under-allocating thinking on hard tasks — `/effort high` (or `max` on Opus) plus `showThinkingSummaries` brings the deep analysis back.
- **Details**: After analyzing 17,000+ thinking blocks, an AMD engineer found Claude was skipping ahead and editing code before fully processing the problem. PM Paweł Huryn's three fixes: run `/effort high`, set `showThinkingSummaries: true`, and pin a CLAUDE.md rule against editing unread code. For nuclear control, set `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` in env.
```bash
# In Claude Code:
/effort high       # any model
/effort max        # Opus, hard debugging

# ~/.claude/settings.json
{ "showThinkingSummaries": true }

# CLAUDE.md
"Research the codebase before editing.
 Never change code you haven't read."
```
- **Source**: https://docs.claude.com/en/docs/claude-code/overview

#### 26. Embed live shell output into Claude Code skills
- **Agent(s)**: Claude Code
- **Summary**: The same `!` backtick syntax that works in slash commands also works in `SKILL.md` — your skills become live, not static.
- **Details**: Skills are normally static, which means a lot of manual copy-paste for diffs and logs. Claude Code engineer Lydia Hallie showed that `!` backtick syntax works inside SKILL.md too — Claude runs the command and substitutes the output before processing. Stick to read-only commands (cat, grep, gh pr view) so a skill can't mutate state.
```bash
# .claude/skills/pr-summary/SKILL.md
---
name: pr-summary
description: Summarize changes in a pull request
---

- PR diff: !\`gh pr diff\`
- PR comments: !\`gh pr view --comments\`
- Changed files: !\`gh pr diff --name-only\`

Summarize this pull request...
```
- **Source**: https://x.com/lydiahallie

#### 27. Make Claude Code grill you before building
- **Agent(s)**: Claude Code
- **Summary**: Matt Pocock's `/grill-me` skill walks down the design tree question by question, surfacing every hidden assumption before a single line is written.
- **Details**: By default Claude jumps straight to building, then 20 minutes in you discover it missed half your requirements. The `/grill-me` skill (three lines!) flips this: it interviews you relentlessly about every aspect of the plan, suggesting answers where things are obvious and drilling down into the tough calls. Run it before starting any non-trivial feature.
```bash
# Install
npx skills@latest add mattpocock/skills/grill-me

# Or hand-roll: .claude/skills/grill-me/SKILL.md
"""
Interview me relentlessly about every aspect of this plan
until we reach a shared understanding. Walk down each branch
of the design tree resolving dependencies between decisions
one by one.

If a question can be answered by exploring the codebase,
explore the codebase instead.

For each question, provide your recommended answer.
"""
```
- **Source**: https://x.com/mattpocockuk

#### 28. Stop agents from faking progress — demand proof in every status update
- **Agent(s)**: Claude Code, Cursor
- **Summary**: Agents love to say 'on it!' or 'done!' when nothing has actually run. Bind every status update to a process ID, file path, URL, or command output.
- **Details**: By default, agents give confident status updates whether the action worked or not — you won't catch silent failures until you check by hand. Tech founder Cathryn Lavery shared a one-line rule that fixes it: every claim must come with proof. Paste it into `CLAUDE.md` (project) or `~/.claude/CLAUDE.md` (global) for Claude Code, or `.cursorrules` for Cursor. Now 'building' becomes 'started build, pid 41822, branch feat/auth, step: tsc.'
```markdown
# CLAUDE.md   /   ~/.claude/CLAUDE.md   /   .cursorrules

Never say 'done' or 'working on it' unless the action has
actually started. Every status update must include proof —
a process ID, file path, URL, or command output.

No proof = didn't happen.
A false completion is worse than a delayed honest answer.
```
- **Source**: https://x.com/cathrynlavery

---

### Automation & Hooks

#### 29. Block Stop until tests pass with a hook
- **Agent(s)**: Claude Code
- **Summary**: A Stop hook can refuse to end the turn if tests fail, looping the model back until the work is actually green.
- **Details**: Stop hooks run when the agent thinks it's done. Exit code 2 + a stderr message tells the model 'no, keep going.' Pair with a fast test runner so the loop is tight. The model literally cannot ship broken code.
```json
// .claude/settings.json
{
  "hooks": {
    "Stop": [{
      "matcher": "",
      "hooks": [{
        "type": "command",
        "command": "pnpm test --run || echo 'tests failing — fix before stopping' >&2 && exit 2"
      }]
    }]
  }
}
```
- **Source**: https://docs.claude.com/en/docs/claude-code/hooks

#### 30. Run Claude Code headless in CI for triage
- **Agent(s)**: Claude Code
- **Summary**: `claude -p` is non-interactive — wire it into CI to auto-label issues, draft PR descriptions, or first-pass review failing tests.
- **Details**: The `-p` flag takes a prompt and exits when done. With `--output-format json` you get structured results. Use it as a GitHub Action that runs on `issues.opened` to add labels, summarize the repro, and link related code. It's not a replacement for human review — it's the intern that does triage at 3am.
```bash
# .github/workflows/triage.yml
- run: |
    claude -p "Read issue #\${{ github.event.issue.number }}.
    Look at related code. Output JSON:
    { labels: string[], summary: string, suspect_files: string[] }" \\
      --output-format json > triage.json
    gh issue edit \${{ github.event.issue.number }} \\
      --add-label "$(jq -r '.labels | join(",")' triage.json)"
```
- **Source**: https://docs.claude.com/en/docs/claude-code/sdk

#### 31. Allowlist read-only commands to kill prompt fatigue
- **Agent(s)**: Claude Code
- **Summary**: Add `Bash(ls:*)`, `Bash(rg:*)`, `Bash(git status:*)` etc to settings — the agent stops asking permission for safe inspection.
- **Details**: Default permissions ask before every Bash call. After a week you'll know which commands you always approve (read-only stuff: ls, cat, grep/rg, git status, git diff, jq). Pre-approve them in settings and you save dozens of clicks per session. Keep destructive commands (rm, git push --force, anything write) gated.
```json
// .claude/settings.json
{
  "permissions": {
    "allow": [
      "Bash(ls:*)",
      "Bash(rg:*)",
      "Bash(git status:*)",
      "Bash(git diff:*)",
      "Bash(git log:*)",
      "Bash(jq:*)",
      "Bash(pnpm test:*)"
    ]
  }
}
```
- **Source**: https://docs.claude.com/en/docs/claude-code/settings

#### 32. Watch background tasks with the Monitor tool
- **Agent(s)**: Claude Code
- **Summary**: The Monitor tool replaces the old `/loop` workaround — Claude streams stdout from a background process and only spends tokens when an error appears.
- **Details**: Tracking background tasks used to mean running `/loop` over and over to check for errors, burning API calls. Claude Code PM Noah Zweben replaced that pattern with a built-in Monitor tool. A single prompt starts your dev server and watches stdout — zero tokens while everything is healthy, instant intervention when a stack trace shows up.
```bash
Start my dev server and use the Monitor tool to watch for errors.
```
- **Source**: https://x.com/noahzweben

#### 33. Get notified when Claude Code finishes a task
- **Agent(s)**: Claude Code
- **Summary**: Drop `.wav` files into `~/.claude/hooks/` and let Claude wire up SessionStart/Notification/Stop hooks so you don't hover over the terminal.
- **Details**: Long-running tasks burn time when you alt-tab away and check back too late. Sound cues for SessionStart, UserPromptSubmit, Notification, and Stop fix it. Drop your `.wav` files in `~/.claude/hooks/` and ask Claude to configure the hooks — it edits `settings.json` for you. Anthropic engineer Delba famously uses Warcraft peon sounds.
```bash
# Drop your sound files first:
~/.claude/hooks/session-start.wav
~/.claude/hooks/notification.wav
~/.claude/hooks/stop.wav

# Then in any session:
"Set up Claude Code hooks to play sounds on
 SessionStart, UserPromptSubmit, Notification, and Stop.
 Use the .wav files in ~/.claude/hooks/."
```
- **Source**: https://docs.claude.com/en/docs/claude-code/hooks

#### 34. Block API keys from leaking via a UserPromptSubmit hook
- **Agent(s)**: Codex
- **Summary**: A pre-submit hook can grep your prompt for secret patterns and refuse to send if it finds one — safer than relying on memory.
- **Details**: Codex sends prompts directly to the model, so accidentally pasting a secret means it leaves your machine. Add a `UserPromptSubmit` hook that scans for OpenAI, GitHub, and AWS key patterns. If a match is found, the prompt is blocked with a `stopReason` instead of being sent.
```json
// Codex config (format may vary by setup)
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "jq -r .prompt | grep -qE 'sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|AKIA[0-9A-Z]{16}' && printf '{\\"continue\\":false,\\"stopReason\\":\\"possible secret detected\\"}' || true"
      }]
    }]
  }
}
```
- **Source**: https://developers.openai.com/codex

#### 35. Kill permission spam with /fewer-permission-prompts
- **Agent(s)**: Claude Code
- **Summary**: Boris Cherny's skill scans your session history for safe Bash and MCP commands that always trigger prompts, then suggests an allowlist.
- **Details**: Most devs end up running `--dangerously-skip-permissions` to silence the spam. The Claude Code creator shared a proper fix: a skill that mines your session history for the safe commands you've approved over and over, then proposes an allowlist you can paste into settings. Best run after a few days of work so there's enough history to mine.
```bash
/fewer-permission-prompts
```
- **Source**: https://x.com/bcherny

#### 36. Monitor deploys without leaving Claude Code
- **Agent(s)**: Claude Code
- **Summary**: `/loop 5m check if the deploy succeeded` runs a recurring prompt in the background while you stay focused on real work.
- **Details**: Tab-switching between Claude Code and your CI dashboard while a pipeline crawls is a focus-killer. `/loop` runs a recurring prompt at any interval (seconds, minutes, hours, days). Skip the interval and it defaults to 10 minutes. Tasks are session-scoped and expire after three days, so a forgotten loop won't run forever.
```bash
/loop 5m check if the deploy succeeded and report back
/loop 20m /review-pr 1234
/loop check the build status   # defaults to 10m
```
- **Source**: https://docs.claude.com/en/docs/claude-code/overview

#### 37. Run @codex review on every pull request
- **Agent(s)**: Codex
- **Summary**: Enable Codex in your repo settings, comment `@codex review`, and it leaves inline comments like a teammate. `@codex fix it` opens a patch PR.
- **Details**: PR reviews bottleneck shipping, and missing tests slip to production. Codex can act as a first-pass reviewer directly in GitHub. Once enabled in repo settings, comment `@codex review` to get inline feedback. `@codex fix it` kicks off a cloud task that patches the code and pushes a commit. Customize what it flags via an `AGENTS.md` at repo root — Codex applies the closest one to each changed file.
```bash
# AGENTS.md (at repo root or in any subdir)
## Review guidelines
- Flag typos and grammar issues as P0 issues.
- Flag potential missing documentation as P1 issues.
- Flag missing tests as P1 issues.

# In a PR comment:
@codex review
@codex fix it
```
- **Source**: https://developers.openai.com/codex

#### 38. Configure Cursor's YOLO mode with a scoped allowlist
- **Agent(s)**: Cursor
- **Summary**: Don't just toggle YOLO mode — write a scoped prompt that whitelists tests and builds, deny destructive commands. Auto-runs without prompts.
- **Details**: Cursor pauses for permission on every test or build, killing the build-fix-build loop. YOLO mode lets the agent execute autonomously, but plain YOLO is too permissive. Settings → Features → YOLO mode has a prompt field where you scope which commands are auto-allowed. Add a deny list for `rm -rf` and migrations to keep it safe.
```json
// In Cursor: Settings → Features → YOLO mode
// (the scoped prompt field)
"any kind of tests are always allowed like vitest, npm test,
 nr test, etc. also basic build commands like build, tsc, etc.
 creating files and making directories (like touch, mkdir, etc)
 is always ok too"

// Deny list: rm -rf, db migrations, anything destructive
```
- **Source**: https://docs.cursor.com/chat/overview

#### 39. Schedule jobs in the cloud with /schedule
- **Agent(s)**: Claude Code
- **Summary**: `/schedule` registers a recurring task that runs in Anthropic's cloud — no more 'my laptop closed and the job died.'
- **Details**: Scheduled tasks used to require your laptop stay awake, which made them basically useless. The new `/schedule` command runs them in the cloud. Connected MCP servers (Slack, GitHub) work seamlessly inside the scheduled prompt — Claude figures out the right cron expression from your description.
```bash
/schedule a daily job that looks at all PRs shipped since
yesterday and update our docs based on the changes.
Use the Slack MCP to message #docs-update with the changes
```
- **Source**: https://x.com/noahzweben

#### 40. Run prompts on repeat with scheduled tasks
- **Agent(s)**: Claude Code
- **Summary**: `/loop 15m scan my error logs and flag anything new` runs in the background while your session stays focused. Bare prose works for one-offs.
- **Details**: Scheduled tasks let you fire prompts on an interval without stealing focus. `/loop <interval> <prompt>` covers seconds, minutes, hours, days. Skip the interval, defaults to 10m. For one-off reminders skip `/loop` entirely and just describe what you need. Tasks only run while Claude Code is active — for true persistence, leave a session open on a server or wire an external cron job.
```bash
/loop 5m check if the deployment is healthy
/loop 15m scan my error logs and flag anything new
/loop 30m check if CI passed on main

# One-off:
remind me at 3pm to push the release branch
```
- **Source**: https://docs.claude.com/en/docs/claude-code/overview

#### 41. Auto-format Claude Code's output with a PostToolUse hook
- **Agent(s)**: Claude Code
- **Summary**: A `PostToolUse` hook on Write/Edit fires your formatter every time Claude touches a file — no more manual prettier/eslint runs before push.
- **Details**: Claude usually writes clean code, but the last 10% of formatting inconsistencies means you're still running your formatter by hand before you can push. Claude Code creator Boris Cherny shared a `PostToolUse` hook that triggers automatically on every Write or Edit. Drop it in `.claude/settings.json` for one project or `~/.claude/settings.json` for global. The `|| true` keeps a transient formatter failure from crashing the session.
```json
// .claude/settings.json   (or ~/.claude/settings.json)
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "bun run format || true"
          }
        ]
      }
    ]
  }
}
```
- **Source**: https://x.com/bcherny

---

### Tools & Plugins

#### 42. Add an MCP server in one command
- **Agent(s)**: Claude Code
- **Summary**: Wire up Notion, Linear, Postgres, or any MCP server with `claude mcp add` — no config file editing required.
- **Details**: MCP turns external services into first-class tools. The CLI `claude mcp add` writes the config for you. Scope it to `--scope user` for personal tools (Notion) or `--scope project` for team tools (a staging DB). The model gets typed access and you skip the copy-paste-from-docs ritual.
```bash
claude mcp add postgres-staging \\
  --scope project \\
  --env DATABASE_URL=$STAGING_URL \\
  -- npx -y @modelcontextprotocol/server-postgres

claude mcp list   # see what's wired up
```
- **Source**: https://docs.claude.com/en/docs/claude-code/mcp

#### 43. Debug frontend bugs with the Chrome DevTools MCP
- **Agent(s)**: Cursor
- **Summary**: Google's Chrome DevTools MCP gives Cursor a live Chrome instance — it can click, read the console, and pull network requests instead of guessing from screenshots.
- **Details**: Frontend debugging in Cursor often hits a dead end: you paste an error, the agent tries to fix it, but it can't see the network tab, the console, or the actual UI. Wire up the Chrome DevTools MCP in Settings → MCP → New MCP Server, then ask Cursor to open the page and check itself. The agent navigates, clicks, and reads source-mapped stack traces to pinpoint the exact line.
```json
// In Cursor: Settings → MCP → New MCP Server
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}

// Then in chat:
"My checkout button isn't firing. Open localhost:3000,
 click it, and tell me what's wrong."
```
- **Source**: https://github.com/ChromeDevTools/chrome-devtools-mcp

#### 44. Catch type errors before commit with LSP plugins
- **Agent(s)**: Claude Code
- **Summary**: Language Server plugins give Claude live diagnostics after every save — type errors and unused imports get fixed before you even read the diff.
- **Details**: Claude's code often hides type errors, unused imports, or missing return types that look fine at a glance. LSP plugins run a real language server alongside the agent: the moment a file is saved, the server flags issues so Claude can fix them in the same turn. Pick your language and install — make sure the language-server binary is also on your system.
```bash
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
/plugin install rust-analyzer-lsp@claude-plugins-official
/plugin install gopls-lsp@claude-plugins-official

# Run /plugin and open the Discover tab for the full list.
```
- **Source**: https://docs.claude.com/en/docs/claude-code/plugins

#### 45. Turn Figma frames into code with Codex
- **Agent(s)**: Codex
- **Summary**: Codex's built-in Figma + Playwright skills pull design context from MCP, generate matching code, and iterate in a real browser until pixels line up.
- **Details**: Designers hand off Figma frames; engineers spend hours translating spacing, tokens, and layout. Codex's bundled Figma and Playwright skills automate the loop: it pulls exact node info from Figma, generates code using your existing design-system tokens, then opens a real browser to verify. Both skills are built in — nothing to install.
```bash
Implement this Figma design in the current project
using the Figma skill.

Requirements:
- Start with \`get_design_context\` for the exact node or frame.
- Run \`get_screenshot\` for the exact variant before coding.
- Reuse the existing design system components and tokens.
- Make the page responsive on desktop and mobile.

Validation:
- Use Playwright to check that the UI matches the reference
  and iterate until it does.
```
- **Source**: https://developers.openai.com/codex

#### 46. Skill-route blocked URLs through Gemini
- **Agent(s)**: Claude Code
- **Summary**: Claude's WebFetch hits 403s on Reddit. A custom skill detects the failure, opens a tmux Gemini session, and pulls the page through it.
- **Details**: WebFetch returns 403 on sites like Reddit, stalling research mid-session. Ex-Google engineer YK packaged a workaround as a Claude Code skill: when WebFetch fails on a known-blocked domain, the skill spins up a tmux Gemini session, runs the query, and captures the output. Skills load on demand, so it only costs tokens when actually triggered.
```bash
# Install Gemini CLI and auth
npm install -g @google/gemini-cli
gemini  # run once to auth with your Google account

# Add the skill
mkdir -p ~/.claude/skills/reddit-fetch
curl -o ~/.claude/skills/reddit-fetch/SKILL.md \\
  https://raw.githubusercontent.com/ykdojo/claude-code-tips/main/skills/reddit-fetch/SKILL.md
```
- **Source**: https://github.com/ykdojo/claude-code-tips

#### 47. Audit your Claude Code permissions with cc-safe
- **Agent(s)**: Claude Code
- **Summary**: After weeks of approvals, your settings file is a minefield. `cc-safe` flags commands that could delete files, run as admin, or escalate access.
- **Details**: Every approval persists in your settings file. After a while you have a long list of auto-approved commands you've stopped scrutinizing — and one Reddit user lost their entire home directory because of a typo'd shell command. `cc-safe` scans your projects folder and surfaces dangerous entries across every subfolder in one pass.
```bash
npx cc-safe ~/projects
```
- **Source**: https://github.com/ykdojo/claude-code-tips

#### 48. Strip needless abstractions with code-simplifier
- **Agent(s)**: Claude Code
- **Summary**: Claude often adds unrequested abstractions. The official `code-simplifier` plugin refactors recent changes against your CLAUDE.md conventions.
- **Details**: Generated code looks plausible but adds layers you didn't ask for, making review harder. Anthropic shipped a `code-simplifier` plugin that takes a final pass: it reads your CLAUDE.md, follows your conventions, and focuses only on recently modified files. Run it at the end of each session.
```bash
# Install
claude plugin install code-simplifier
# Restart Claude Code, then in any session:
"use the code simplifier agent to clean up my recent changes"
```
- **Source**: https://x.com/bcherny

#### 49. Share Claude Code sessions as HTML replays
- **Agent(s)**: Claude Code
- **Summary**: `claude-replay` turns your `~/.claude/projects/*.jsonl` transcripts into a self-contained HTML player with speed controls and chapter bookmarks.
- **Details**: Sharing AI coding sessions is awkward — screencasts are bulky, raw transcripts are unreadable. `claude-replay` converts session logs into one HTML file you can email, embed, or host. Interactive player with speed controls, collapsible tool calls, and chapter bookmarks. Secret redaction is on by default but review before publishing — file paths and tool outputs are embedded.
```bash
npx claude-replay ~/.claude/projects/<your-project>/session-id.jsonl \\
  -o replay.html
```
- **Source**: https://github.com/es617/claude-replay

#### 50. Cut Claude Code's token usage by 70% with rtk
- **Agent(s)**: Claude Code
- **Summary**: Most context is noise — passing tests, progress bars, verbose logs. `rtk` is a CLI proxy that compresses command output before it hits the window.
- **Details**: Every command Claude runs dumps its full output into context. Half-hour sessions hit 150K tokens, mostly noise. `rtk` is a Rust CLI proxy that intercepts every command Claude executes and compresses the output before it lands. Sessions that peaked at 150K tokens now sit around 45K. Run `rtk gain` to see your savings.
```bash
# Requires Rust
cargo install --git https://github.com/rtk-ai/rtk

# Wire into Claude Code
rtk init --global

# Check savings any time:
rtk gain
```
- **Source**: https://github.com/rtk-ai/rtk

### Tags
- AI Coding
- Claude
- CLI
- Coding
- Developer Tools
- Prompt
- Workflow
- Best Practices
- Automation
- IDE
