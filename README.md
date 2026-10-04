# Process Over Prompts

A governance workflow for Claude Code, built from analysing real coding sessions and quantifying what went wrong. Agents don't replace process; they need it more than humans do.

This plugin is skills only. It installs no hooks, no MCP servers, and changes no settings.

## Install

```bash
claude plugin marketplace add stonekey908/process-over-prompts
claude plugin install process-over-prompts@stonekey908
```

Or inside a session: `/plugin marketplace add stonekey908/process-over-prompts`, then `/plugin install process-over-prompts`.

Skills are namespaced as `/process-over-prompts:sprint` and so on, but Claude Code also accepts the short form (`/sprint`) whenever the name is unambiguous. Update later with `claude plugin update process-over-prompts`.

## What you get

Ten skills covering the product development lifecycle:

| Skill | What it does |
|-------|-------------|
| `guide` | Quick-start to the workflow. Start here if unsure which skill to use. |
| `session-start` | Reads the CLAUDE.md handoff notes, checks git state, surfaces active Linear tickets |
| `requirements` | Turns a vague idea into a ticket with testable acceptance criteria |
| `design-first` | Vertical slices: UI + API + data working together before broadening |
| `ux-design` | UX framework for information-dense apps |
| `sprint` | Ticket workflow: pre-flight, plan with your approval, implement, test, UAT, commit |
| `automate` | Chains the skills into an autonomous pipeline with escalation points |
| `uat` | Testing with triage: bug, new feature, or docs gap |
| `session-end` | Commits, pushes, updates the CLAUDE.md handoff, updates Linear, captures session friction |
| `retro` | Reviews captured friction and proposes governance changes; you approve each one |

## How to use it

A normal day looks like this:

1. **Orient.** `/session-start` reads the handoff your last session left in `CLAUDE.md` and tells you where things stand.
2. **Define.** `/requirements` turns an idea into a scoped ticket. For UI work, `/design-first` and `/ux-design` shape the first slice.
3. **Build and test.** `/sprint` works the ticket with an approval gate before implementation. `/uat` triages what you find: bugs get fixed, new ideas go to the backlog.
4. **Wrap up.** `/session-end` commits, pushes, rewrites the `CLAUDE.md` handoff sections, updates the ticket, and captures the session's friction.
5. **Improve.** `/retro` (this project) or `/retro global` (every project on the machine) reads the captured friction and proposes concrete changes to your rules and to these skills. Nothing is applied without your approval.

You don't need every skill every session. Most sessions are `/session-start`, normal work, `/session-end`.

## The policy layer

The skills are the procedures. The policy layer is the set of rules the agent follows every session, and that lives in your own `CLAUDE.md`. `policy/POLICY.md` is a stack-agnostic starting point: copy it into `~/.claude/CLAUDE.md` and adapt it. Several skills assume its conventions (feature branches, conventional commits, tests before commit, use the configured ticketing integration).

## The memory loop

`session-end` and `retro` form a push/pull loop that makes the workflow improve itself from evidence rather than opinion:

- **Push.** At wrap-up, `session-end` runs `scripts/retro-capture.py --session --semantic`. The script reads this session's transcript and records mechanical friction (tool errors, failed commands) to `~/.claude/insights/friction/<project>.md`. If the session had at least three new turns, it also runs one semantic pass that summarises repeated corrections, rework, and stated preferences.
- **Pull.** `retro` first runs the same script with `--scan` as a safety net for sessions you forgot to wrap up, then reads every friction log and your `CLAUDE.md` files. At global scope it consolidates cross-project learnings into `~/.claude/insights/learned-rules.md`, with provenance and a ledger, and can propose edits to the skills themselves.

Friction logs are treated as untrusted data by both the script and the skill: the semantic output is sanitised, semantic entries are weighted below mechanical ones, and nothing derived from them is promoted without your explicit confirmation.

## What the plugin runs and where data goes

Everything stays on your machine. Nothing is sent to any third-party service.

- The skills are Markdown instructions. They run ordinary `git` commands and, where you have the Linear MCP connector configured, use it for ticket updates. The plugin bundles no MCP server.
- `scripts/retro-capture.py` is a Python 3 script with no third-party dependencies. It reads transcripts under `~/.claude/projects/`, writes under `~/.claude/insights/`, and keeps a small progress file there so nothing is counted twice. For the semantic pass it invokes your locally installed `claude` CLI once, in print mode with model `claude-sonnet-4-6`, hard-capped at 60 seconds. That call goes through your own Claude account like any other session. If the CLI is not on your PATH the pass is skipped and retried next time.

## Requirements

- Claude Code with `git`, `python3`, and the `claude` CLI on your PATH. The skills also load on claude.ai, but `session-end` and `retro` need a terminal.
- A `CLAUDE.md` in each project. `session-end` maintains four sections in it: Current Phase, Known Issues, Last Session, Known Gotchas. `session-start` reads them. The sections are created if missing.
- Optional: the Linear MCP connector for the ticket steps in `requirements`, `sprint`, and `session-end`. Without it those steps are skipped.

## Optional controls (bring your own hooks)

The plugin ships no hooks, so it never changes how your editor or shell behaves. If you want the controls layer, add these two to `~/.claude/settings.json` (or a project's `.claude/settings.json`). They only run `git` and `stat`:

- **Branch protection** refuses file edits while on `main`/`master`, so the agent creates a feature branch first.
- **Session-end guard** warns, when the session stops, about uncommitted changes, unpushed commits, and a `CLAUDE.md` that hasn't been updated this session.

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "timeout": 5,
            "command": "B=$(git branch --show-current 2>/dev/null); if [ \"$B\" = main ] || [ \"$B\" = master ]; then echo '{\"block\": true, \"message\": \"Cannot edit files on main/master. Create a feature branch first: git checkout -b feat/<ticket-id>-<description>\"}'; exit 2; fi"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "timeout": 10,
            "command": "D=$(git status --porcelain 2>/dev/null | head -20); if [ -n \"$D\" ]; then echo '⚠️  Uncommitted work:'; echo \"$D\"; echo 'Commit or stash before stopping.'; fi; A=$(git rev-list --count @{upstream}..HEAD 2>/dev/null); if [ -n \"$A\" ] && [ \"$A\" != 0 ]; then echo \"⚠️  $A commit(s) not pushed. Run: git push\"; fi; if [ -f CLAUDE.md ]; then M=$(stat -c %Y CLAUDE.md 2>/dev/null || stat -f %m CLAUDE.md 2>/dev/null); if [ $(( $(date +%s) - M )) -gt 7200 ]; then echo '⚠️  CLAUDE.md not updated this session. Run /session-end.'; fi; fi; if [ -z \"$D\" ]; then echo '✅ Working tree is clean.'; fi"
          }
        ]
      }
    ]
  }
}
```

The `stat` call tries the GNU form first and falls back to the BSD form, so the same snippet works on Linux and macOS.

## Folder structure

```
.claude-plugin/
├── plugin.json                   ← plugin manifest
└── marketplace.json              ← lets you install straight from this repo
skills/<name>/SKILL.md            ← the ten skills
policy/POLICY.md                  ← starting rules for your own CLAUDE.md
scripts/retro-capture.py          ← friction capture, run by /session-end and /retro
tests/                            ← regression tests for retro-capture.py
```

## Where this came from

I'm not a developer. I'm a product leader at a bank who runs CRM systems and started building apps with Claude Code. After a few months I analysed my own sessions: the agent jumped into the wrong approach before researching, sessions were lost to tooling discovered mid-task, and automated checks would have caught rounds of buggy code. The friction wasn't the model. It was the absence of process. So I applied what I already knew from enterprise IT: policy, procedures, controls, and segregation of duties, applied to an AI agent.

## Licence

MIT. Use it, adapt it, share it.
