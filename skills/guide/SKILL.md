---
name: guide
description: Quick-start guide to all skills and workflow. Use when onboarding, unsure which skill to use, or need a refresher.
---

# Guide — How This Workflow Works

## The Short Version

You have 10 skills that fall into a natural flow:

```
Bookends:     /session-start ←→ /session-end
Planning:     /requirements → /design-first + /ux-design
Building:     /sprint
Testing:      /uat
Special:      /automate (full autonomy mode)
Meta:         /guide, /retro
```

You don't have to remember which skill to use — Claude will suggest the relevant one when it recognises the situation. You can always ignore the suggestion and just work directly.

## Which Skill Do I Use?

The main decision is between `/design-first` and `/sprint`:

| You want to... | Run this | Why |
|----------------|----------|-----|
| Build a feature with meaningful UI | `/design-first` | Designs core flow (UI + data model together), builds it as a vertical slice end-to-end, then broadens |
| Work on a ticket (backend-only or minor UI) | `/sprint` | Full cycle: pickup → plan with options → implement in vertical slices → test → commit |
| Automate a batch of tickets end-to-end | `/automate` | Chains skills into an autonomous pipeline. Special case — not for every session |

**Rule of thumb:** If the ticket involves designing new screens, use `/design-first`. If the screens already exist or there's no UI, use `/sprint`. Both build vertical slices (frontend + backend together) — the difference is whether you need a design phase.

## All Skills

| You want to... | Run this | What it does |
|----------------|----------|-------------|
| Start a new session or resume work | `/session-start` | Reads CLAUDE.md handoff notes, checks git state, surfaces active Linear tickets. Takes under 1 minute |
| Turn a vague idea into a ticket | `/requirements` | Researches feasibility, defines scope, creates a Linear ticket with testable acceptance criteria |
| Build a feature with meaningful UI | `/design-first` | Audits existing components + backend, designs core flow with data model, builds vertical slices end-to-end, then broadens |
| Think through UX for complex screens | `/ux-design` | Applies progressive disclosure, persistent context, scannable structure. Used alongside `/design-first` — applied per slice as you build |
| Work on a ticket (backend-only or minor UI) | `/sprint` | Full cycle: pre-flight → pickup → present approach options → implement in vertical slices → test → UAT → commit |
| Run the full pipeline autonomously | `/automate` | Chains skills into an autonomous pipeline. Use after tickets + wireframes are ready |
| Test completed work | `/uat` | Structured testing with interview mode, triages findings as bugs vs new features vs docs gaps. Includes dark mode/theme verification |
| Finish a session | `/session-end` | Commits, pushes, updates CLAUDE.md handoff notes, updates Linear. Takes 2 minutes |
| Improve the workflow itself | `/retro` | Reviews recent friction, proposes governance updates. You approve every change |

## Common Workflows

### "I'm picking up where I left off"
1. `/session-start` — reads the handoff, checks git state, shows active tickets

### "I have an idea for a feature"
1. `/requirements` — turns it into a buildable ticket
2. `/design-first` + `/ux-design` — designs and builds the core flow first, then broadens
3. More tickets? → `/sprint` for backend-only or minor UI work

### "I have a ticket ready to go"
- Has meaningful UI? → `/design-first`
- Backend-only or minor UI? → `/sprint`

### "I just want to fix bugs / do quick work"
- Just start working — no skill needed. Claude will suggest `/uat` or `/sprint` if relevant, but won't block you.

### "Something isn't working right"
1. `/uat` — classifies the issue (bug vs feature vs docs gap)
2. If bug: fixes it with regression tests
3. If feature: creates a backlog ticket — no scope creep

### "I have tickets and wireframes ready — build it all"
1. `/automate` — autonomous pipeline: implements all tickets, creates mock layer, generates SETUP.md, runs visual + functional UAT, presents a report at the end
2. You can pause at any time and resume with `/session-start` → `/automate`

### "I'm done for the day"
1. `/session-end` — ensures nothing is left uncommitted or unpushed

## Rules That Always Apply

These are enforced globally across every project (from `~/.claude/CLAUDE.md`):

- **MCP First** — use Linear/Notion MCP tools, never CLI workarounds
- **Use What Exists** — check existing components before introducing new ones
- **Research Before Code** — read the codebase and docs before proposing solutions
- **Confirm Approach** — present 2-3 options with tradeoffs for non-trivial decisions before coding
- **Vertical Slices** — build features end-to-end (schema → API → UI), never all-frontend-then-backend
- **Stay In-Stack** — don't fall back to alternative build approaches
- **UI Change Completeness** — update ALL consuming screens after component changes
- **Don't Touch What I Didn't Ask** — ask first if you think something else should change

## Quality Gates (Every Commit)

1. Type checker passes (`npx tsc --noEmit` or project equivalent)
2. Test suite passes (`npm test` or project equivalent)
3. Conventional commit format: `<type>(<ticket-id>): <description>`
4. Work happens on feature branches, never main/master

## Project-Specific vs Global

- **Global skills** (`~/.claude/skills/`) — available in every project automatically
- **Global rules** (`~/.claude/CLAUDE.md`) — apply everywhere, merged with project rules
- **Global hooks** (`~/.claude/settings.json`) — branch protection, type checking, stop warnings
- **Project CLAUDE.md** — extends the global rules with project-specific context (tech stack, architecture, conventions)
- **Project skills** (`<project>/.claude/skills/`) — override global skills of the same name when a project needs different behaviour

## Manual Setup Requirements

Some projects need manual setup (Firebase, Supabase, API keys, etc.). Each project documents this in a `SETUP.md` file with:
- Step-by-step instructions written plainly
- `.env.example` with placeholder values so tests and code reviews work without real credentials
- Which steps are one-time vs recurring

## Getting Started on a New Project

1. Check if the project has a `CLAUDE.md` — read it for project-specific context
2. Check if the project has a `SETUP.md` — follow manual setup steps
3. Check if the project has `.env.example` — copy to `.env.local` and fill in real values
4. Run `/guide` (this skill) if you need a refresher on the workflow
5. Run `/design-first` or `/sprint` to pick up your first ticket
