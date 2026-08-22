### Name
The Code — Coding Hacks for AI Agents

### Description
A curated reference directory of practical hacks, configuration patterns, hooks, and workflows for developers building with AI coding agents including Claude Code, Codex, and Cursor.

### Category
Cheat Sheets

### URL
https://hackbook-chi.vercel.app/

### Content

#### Overview
A collection of high-impact tips, configuration recipes, prompting patterns, and automation hooks designed to accelerate developer workflows across modern AI coding agents (Claude Code, OpenAI Codex, and Cursor).

---

### Context & Configuration

#### 1. Pin a CLAUDE.md at Repo Root
- **Agent**: Claude Code
- **Concept**: A short `CLAUDE.md` is auto-loaded into every session for repo-specific style, build commands, and conventions the model cannot infer. Keep it under ~80 lines.
```markdown
# CLAUDE.md
## Commands
- `pnpm dev` — start dev server
- `pnpm test -- --watch` — TDD mode

## Conventions
- Server components by default; mark `"use client"` only when needed
- DB access via `src/db/queries/*` only — never inline SQL in routes

## Don't touch
- `generated/` (codegen output)
- `migrations/*.sql` (append-only)
```

#### 2. Auto-Generate a Tight CLAUDE.md with `/init`
- **Agent**: Claude Code
- **Concept**: An experimental `CLAUDE_CODE_NEW_INIT` flag rewrites `/init` to scan your stack, linters, and CI configuration, generating a concise ~60-line `CLAUDE.md` instead of bloated hundreds of lines.
```json
// .claude/settings.local.json
{
  "env": {
    "CLAUDE_CODE_NEW_INIT": "1"
  }
}
```
Run `/init` to trigger the stack scan.

#### 3. Layer `.cursor/rules/*.mdc` by Scope
- **Agent**: Cursor
- **Concept**: Per-folder `.mdc` rules with glob patterns prevent prompt bloat. The model only receives rules relevant to the active file being edited.
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

#### 4. Auto-Load Git Context at Session Start
- **Agent**: Claude Code
- **Concept**: Use a `SessionStart` hook to capture branch name and uncommitted diffs automatically into a context file so Claude starts every session fully oriented.
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

#### 5. Lock Down Claude Code's Stability Settings
- **Agent**: Claude Code
- **Concept**: Pin reasoning effort to high, disable 1M-token mode, deactivate adaptive thinking drift, and turn off auto-memory to prevent context bloat and hallucinated overrides.
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

#### 6. Feed Claude Code's Own Docs Map into Context
- **Agent**: Claude Code
- **Concept**: Point Claude directly to Anthropic's live docs index URL so it looks up official syntax instead of guessing from stale pre-training data.
```text
https://code.claude.com/docs/en/claude_code_docs_map.md
help me configure hooks
```

---

### Workflow & Task Management

#### 7. Shift+Tab into Plan Mode for Risky Changes
- **Agent**: Claude Code
- **Concept**: Plan Mode allows the agent to read, grep, and analyze code freely while blocking write/edit actions until you approve the implementation plan.
```text
# Toggle modes (Shift+Tab cycles)
1. Default       — full tools
2. Auto-accept   — skips approvals on allowed tools
3. Plan Mode     — read-only until you approve
```

#### 8. Fan Out Independent Searches with Parallel Subagents
- **Agent**: Claude Code
- **Concept**: Trigger multiple subagents in a single message to explore distinct codebase subsystems concurrently. Large grep outputs remain isolated within subagent contexts.
```javascript
// Run in parallel in a single assistant message
Agent({ subagent_type: "Explore", prompt: "Find auth middleware" })
Agent({ subagent_type: "Explore", prompt: "Find payment handlers" })
Agent({ subagent_type: "Explore", prompt: "Find error boundaries" })
```

#### 9. Codex: Split Tasks at Commit Boundaries
- **Agent**: Codex
- **Concept**: Planning quality degrades over large 5+ file edits. Structure prompts to target one atomic commit at a time (schema -> query -> route -> UI).
```text
# Prompt structure:
"Step 1: Add the comments table to schema.prisma + generate migration."
# Review & commit, then:
"Step 2: Add createComment + listComments in db/queries/comments.ts."
```

#### 10. Run Agents on Parallel Git Worktrees
- **Agent**: Claude Code, Codex, Cursor
- **Concept**: Run simultaneous agents in separate worktree directories on the same repository to avoid branch collisions and clobbered working directories.
```bash
git worktree add ../myapp-auth feat/auth
git worktree add ../myapp-billing feat/billing

# Open each in separate terminal / editor:
cd ../myapp-auth && claude
cd ../myapp-billing && claude

git worktree list
git worktree remove ../myapp-auth
```

#### 11. Resume or Fork Sessions
- **Agent**: Claude Code
- **Concept**: Persist long-running features across days using `--resume` or fork the session to experiment with alternative architectural approaches without losing progress.
```bash
claude --resume        # interactive session picker
claude --continue      # resume most recent session
claude -c -p "now add the email step"   # one-shot continuation
claude --continue --fork-session        # fork branch from current state
```

#### 12. Rewind Codex Sessions via Double-Tap Esc
- **Agent**: Codex
- **Concept**: In an empty composer, double-tap `Esc` to step backward through the chat history to edit prompt missteps and fork a clean path forward.
```text
Esc Esc          → edit previous message
Esc Esc Esc ...  → walk further back
Enter            → fork from this point
```

#### 13. Run Skills in Isolated Context (`context: fork`)
- **Agent**: Claude Code
- **Concept**: Add `context: fork` and `agent: Explore` to `SKILL.md` frontmatter to execute deep research in an isolated subagent, preventing main thread clutter.
```markdown
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

#### 14. Mid-Task Inquiries with `/btw`
- **Agent**: Claude Code
- **Concept**: Ask quick contextual questions in a side panel mid-turn without interrupting active tool runs or adding token weight to main history.
```text
/btw what was the name of that config file?
```

---

### Prompting & Specification

#### 15. Write a Spec File (`spec.md`) First
- **Agent**: Claude Code, Codex, Cursor
- **Concept**: Agents adhere significantly better to concrete markdown specification documents than conversational chat prompts.
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

#### 16. Enforce Proof in Status Updates
- **Agent**: Claude Code, Cursor
- **Concept**: Prevent hallucinated or premature task completion claims by requiring evidence in every status update.
```markdown
# CLAUDE.md / .cursorrules
Never say 'done' or 'working on it' unless the action has actually started.
Every status update must include proof — a process ID, file path, URL, or command output.
No proof = didn't happen.
```

#### 17. Make Claude Code Grill You Before Building
- **Agent**: Claude Code
- **Concept**: Matt Pocock's `/grill-me` prompt forces the model to interview you step-by-step through the design tree to resolve ambiguities before coding.
```markdown
Interview me relentlessly about every aspect of this plan until we reach a shared understanding.
Walk down each branch of the design tree resolving dependencies between decisions one by one.
If a question can be answered by exploring the codebase, explore the codebase instead.
For each question, provide your recommended answer.
```

#### 18. Structured TODO List Discipline
- **Agent**: Claude Code, Codex
- **Concept**: Require the model to draft and maintain a checked TODO list so execution progress is trackable and interceptable.
```text
Plan this as a checked TODO list first. Don't write code yet.
Once I approve the plan, work through items one at a time.
After each item, briefly say what you did and what's next.
```

#### 19. Pin Files Explicitly with `@` in Cursor
- **Agent**: Cursor
- **Concept**: Auto-retrieval often under-indexes multi-file refactors. Pin the entry point, interfaces/types, and consumer files directly.
```text
@src/auth/session.ts @src/auth/types.ts @app/api/me/route.ts

Refactor session reading to use the new SessionContext type.
Update all three files. Keep the existing cookie shape.
```

#### 20. Paste Screenshots for Visual & Layout Fixes
- **Agent**: Claude Code, Cursor
- **Concept**: Provide visual screenshots of UI bugs or Figma frames directly to leverage multimodal understanding rather than describing pixel offsets.

---

### Automation & Hooks

#### 21. Block Stop Until Tests Pass
- **Agent**: Claude Code
- **Concept**: Refuse completion if test suites fail by exiting with code 2 in a `Stop` hook.
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

#### 22. Auto-Format on Write / Edit (`PostToolUse`)
- **Agent**: Claude Code
- **Concept**: Automatically format touched files after tool execution so code conforms to project styling without manual intervention.
```json
// .claude/settings.json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{
        "type": "command",
        "command": "bun run format || true"
      }]
    }]
  }
}
```

#### 23. Secret Scanner via `UserPromptSubmit` Hook
- **Agent**: Codex
- **Concept**: Intercept prompt submission to scan for API key regex patterns, aborting before credentials leave the local machine.
```json
{
  "hooks": {
    "UserPromptSubmit": [{
      "hooks": [{
        "type": "command",
        "command": "jq -r .prompt | grep -qE 'sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{36}|AKIA[0-9A-Z]{16}' && printf '{\"continue\":false,\"stopReason\":\"possible secret detected\"}' || true"
      }]
    }]
  }
}
```

#### 24. Pre-Approve Read-Only Inspection Commands
- **Agent**: Claude Code
- **Concept**: Allowlist safe read operations to eliminate confirmation prompt fatigue while keeping write/destructive operations secured.
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

#### 25. Recurring Monitor and Loop Commands
- **Agent**: Claude Code
- **Concept**: Use `/loop` or the Monitor tool to stream logs and monitor builds/deploys in the background without burning active tokens on idle polling.
```bash
/loop 5m check if the deploy succeeded and report back
/loop 15m scan my error logs and flag anything new
```

#### 26. Dynamic Bang (`!`) Prefix in Commands & Skills
- **Agent**: Claude Code
- **Concept**: Inject live terminal output into custom slash commands and skills by prefixing commands with `!` inside backticks.
```markdown
# .claude/commands/pr-summary.md
---
name: pr-summary
description: Summarize changes in a pull request
agent: Explore
allowed-tools: Bash(gh *)
---
## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`
```

---

### Tools & Plugins

#### 27. Chrome DevTools MCP for Frontend Debugging
- **Agent**: Cursor
- **Concept**: Connect the Chrome DevTools MCP server to let Cursor open live pages, inspect console logs, and trace network requests directly.
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "chrome-devtools-mcp@latest"]
    }
  }
}
```

#### 28. Language Server (LSP) Plugins
- **Agent**: Claude Code
- **Concept**: Provide instant compiler diagnostics and type checks on file save.
```bash
/plugin install typescript-lsp@claude-plugins-official
/plugin install pyright-lsp@claude-plugins-official
/plugin install rust-analyzer-lsp@claude-plugins-official
/plugin install gopls-lsp@claude-plugins-official
```

#### 29. Code Simplifier Plugin
- **Agent**: Claude Code
- **Concept**: Strip unnecessary abstractions and boilerplate from freshly generated code to keep diffs concise and aligned with `CLAUDE.md`.
```bash
claude plugin install code-simplifier
```

#### 30. Token Optimization with RTK
- **Agent**: Claude Code
- **Concept**: Intercept CLI tool outputs through `rtk` to strip noisy output (passing tests, progress bars) and reduce token consumption by up to 70%.
```bash
cargo install --git https://github.com/rtk-ai/rtk
rtk init --global
rtk gain
```

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
