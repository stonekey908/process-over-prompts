---
name: session-start
description: Start or resume a coding session. Reads CLAUDE.md handoff notes, checks git state, surfaces active Linear tickets, picks up where the last session left off.
---

# Session Start Skill

Run this at the start of any session. It reads the handoff notes that `/session-end` wrote and gets you oriented — fast.

## Phase 1: Orient

1. **Read `CLAUDE.md`** in the project root.
2. **Extract the handoff sections** — look for: Current Phase, Known Issues, Last Session.
3. **If Last Session exists:** note the date, what was done, what's next, which branch, and any blockers.
4. **If no handoff sections exist:** note this — the project may be new or `/session-end` hasn't been run yet.

## Phase 2: Environment Check

1. **Run `git status`** — check for uncommitted changes, untracked files.
2. **Run `git branch`** — confirm which branch you're on.
3. **If the working tree is dirty:**
   - Check if changes look like WIP from a crashed session.
   - Flag to the user: "Found uncommitted changes — want to commit, stash, or continue working on them?"
4. **If the branch doesn't match the Last Session branch:** note the discrepancy.
5. **Check for unpulled changes** — run `git fetch && git status` to see if remote is ahead.
6. **Read Known Gotchas** — if the project CLAUDE.md has a `## Known Gotchas` section, read it. These are build/deploy/environment issues discovered in previous sessions. Keep them in mind during implementation to avoid repeating solved problems.
7. **Quick Build Health Check** — if the project has a type-check command (e.g., `npx tsc --noEmit`), run it. If there's a known build or dev-server command in CLAUDE.md or `package.json`, verify it works. Report any failures alongside the session summary. Do NOT attempt fixes — just flag them so the user knows before starting sprint work. Keep this under 30 seconds.
8. **Verify MCP connectivity** — attempt one read-only MCP call (e.g., list Linear teams). If it fails:
   - Report the error clearly: "Linear MCP is not responding — [error message]"
   - Do NOT proceed with ticket-based work. Flag it so I can fix the config/keys before we waste the session.
   - Common causes: expired API key, wrong working directory, server not configured.

## Phase 2b: Check for Paused Sessions

Check CLAUDE.md for any of these paused state sections. Report all that are found.

### Paused /automate Run
1. **Look for an "Automate State" section** in CLAUDE.md.
2. **If found:** present the paused state — current phase (X of 7), tickets, pending decisions count, next action.
3. **Tell the user:** "Paused /automate run found — Phase X of 7, N pending decisions. Invoke `/automate` to resume."

### Paused UAT Interview
1. **Look for a "Paused UAT Interview" section** in the CLAUDE.md handoff notes.
2. **If found:** present the paused state — ticket(s), how many questions completed, results so far, how many remain.
3. **Ask the user:** "You have a paused UAT interview for [ticket-id] ([M of N] complete). Want to resume it now, or work on something else?"
4. **If they want to resume:** jump directly to `/uat` interview mode, starting from the first remaining question. Carry forward all previous answers — do NOT re-ask completed questions.
5. **If they don't:** note it and move on. The paused state stays in CLAUDE.md until the interview is completed or the ticket is closed.

### Paused Setup Walkthrough
1. **Look for a "Setup Walkthrough" section** in CLAUDE.md.
2. **If found:** present the paused state — which service, which step, what's completed, what remains.
3. **Tell the user:** "Paused setup walkthrough found — [service] step [X of Y]. Say 'walk me through setup' to resume."

## Phase 3: Linear Context

1. **Check Linear for in-progress tickets** on this project using MCP tools.
2. **If tickets are found:** list ticket ID, title, and status.
3. **If no tickets:** note "No active tickets — ready for `/sprint` or `/requirements`."

## Phase 4: Ready

Present a clean summary to the user:

```
Session Ready
─────────────
Project: <project name from CLAUDE.md or directory name>
Branch: <current branch>
Git: <clean / dirty — details if dirty>
Last session: <date> — <1-line summary of what was done>
Next steps: <from Last Session handoff, or "No handoff notes found">
Active tickets: <ticket-id: title (status)> or "None"
Blockers: <from Last Session, or "None noted">
```

Then ask: **"What are we working on today?"**

## Key Principles

- **This skill is read-only.** It never commits, pushes, or modifies files. It only reads and reports.
- **It complements `/session-end`.** Session-end writes the handoff. Session-start reads it. They're a pair.
- **Flag problems, don't fix them.** Dirty working tree? Mismatched branch? Tell the user. Let them decide.
- **This skill is fast.** Under 1 minute. Don't turn it into a deep-dive — that's what `/sprint` research phase is for.
- **No handoff notes? That's fine.** Not every project has been through `/session-end`. Just report what's available and move on.
