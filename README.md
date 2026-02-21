# Process Over Prompts

A governance framework for AI coding agents — structured as four layers borrowed from enterprise IT governance.

## What This Is

A ready-to-use set of skills and rules for AI-assisted development, structured as four governance layers:

| Layer | What it does | How it works |
|-------|-------------|-------------|
| **Policy** | Rules the agent follows every session | A persistent instruction file that loads automatically at session start |
| **Procedures** | Step-by-step workflows for defined tasks | Skill documents you invoke when needed |
| **Controls** | Quality gates that catch mistakes | Checks that run before every commit |
| **Segregation of Duties** | Agent proposes, human approves | Built into every skill at key decision points |

## The Skills

Seven skills covering the full product development lifecycle:

| Skill | What it does |
|-------|-------------|
| **Requirements** | Takes a vague idea → researches feasibility → creates a well-structured ticket with testable acceptance criteria |
| **Sprint** | Full ticket workflow: pre-flight → pickup → research & plan (with your approval) → implement → quality gate & commit → UAT → merge. Supports single-ticket and batch modes. |
| **UAT & Triage** | Structured testing report (what was verified, what you can test, what's blocked), then proper triage: bug, new feature, or docs gap? Bugs get fixed. Features go to backlog. No scope creep. |
| **Design-First** | Wireframe with real components → get a clickable prototype → lock the design → implement against it. The wireframe is the source of truth. |
| **UX Design** | UX framework for information-dense apps: progressive disclosure, persistent context, scannable structure, forgiving navigation, zero-surprise interactions |
| **Session End** | Clean wrap-up: commit, push, update handoff docs, update tickets. Never end with uncommitted work or stale documentation. |
| **Retrospective** | Reviews recent session friction against current skills and rules. Proposes specific improvements. You approve each change. |

The flow: **Requirements** → **Design-First** + **UX Design** → **Sprint** → **UAT** → **Session End** → **Retro**

Or: **define what to build → design it → build it → test it → wrap up → improve how you work.**

## How to Use This

### Option 1: Use the skills as prompt templates

The simplest approach. Open any skill file in `skills/`, copy the content, and paste it into your AI coding tool at the start of a session. The skill documents are written as instructions any AI coding agent can follow.

### Option 2: Use your tool's persistent instruction system

Most AI coding tools support a persistent instruction file that loads every session. Copy `policy/POLICY.md` into whatever your tool uses for this. Copy skills into your tool's skill or prompt system if it has one, or keep them as paste-in templates.

## Folder Structure

```
process-over-prompts/
├── README.md
├── LICENSE
│
├── policy/
│   └── POLICY.md                    ← Global rules (adapt to your tool's config)
│
└── skills/
    ├── sprint/SKILL.md              ← Full ticket workflow (single + batch)
    ├── requirements/SKILL.md        ← Idea → structured ticket
    ├── uat/SKILL.md                 ← Testing report + triage
    ├── design-first/SKILL.md        ← Wireframe before logic
    ├── ux-design/SKILL.md           ← UX framework for complex apps
    ├── session-end/SKILL.md         ← Clean session wrap-up
    └── retro/SKILL.md               ← Improve your own process
```

## How It Works Day-to-Day

You don't invoke every skill every session. Most of the time you just work normally — your policy file protects you in the background.

When you want the full structured workflow, use the skill that fits:

- Working through a ticket? → **Sprint**
- New idea that needs scoping? → **Requirements**
- Finished building, need to test? → **UAT**
- Starting a new screen? → **Design-First**
- Done for the day? → **Session End**
- Want to improve your setup? → **Retro**

Think of it like a workshop: safety goggles are always on (policy). Power tools are on the wall (skills). You grab the one you need.

## License

MIT — use it, adapt it, share it.
