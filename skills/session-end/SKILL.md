---
name: session-end
description: Clean session wrap-up. Commits, pushes, updates CLAUDE.md handoff notes, updates Linear. Use when finishing a session, switching projects, or wrapping up.
---

# Session End Skill

Run this before ending any session. It ensures nothing is left behind.

## Phase 0: Trigger check (avoid premature or duplicate runs)

1. **Wait for an explicit "done" signal.** Run only when the user clearly signals they are finished (e.g. "that's it", "I'm done", "wrapping up") — not at the first sign of wind-down conversation. If the user asks a follow-up after you start, the session wasn't over: defer and re-run later.
2. **Guard against re-entry — HARD stop, not a soft prompt.** If `/session-end` already completed once this session, first check for genuinely new work (new uncommitted changes or new commits since the last run). If there is none, emit exactly one line — *"session-end already completed this session — nothing to do"* — and exit. Do NOT re-run the commit/push/summary pass or re-emit a handoff summary. Only if there IS new work do you proceed, and then confirm with the user that this is a genuine second wrap-up. (Observed: the soft guard was repeatedly acknowledged-and-overridden, producing redundant full re-runs.)

## Phase 1: Code State Check

1. **Run `git status`** — check for uncommitted changes, untracked files, staged but uncommitted work.
2. **If dirty:**
   - If work is complete: stage and commit with conventional commit format.
   - If work is incomplete: commit with `wip(<ticket-id>): <description of what's done and what remains>`.
   - If work should be discarded: confirm with the user before `git stash` or `git checkout .`.
3. **Check for unpushed commits** — run `git log @{upstream}..HEAD --oneline 2>/dev/null`. If there are unpushed commits, push them.
4. **Confirm:** working tree is clean and branch is up to date with remote.

## Phase 2: CLAUDE.md Update

1. **Check for a project-specific CLAUDE.md rule first.** Some projects have a "never commit CLAUDE.md" convention. If the project's rules say not to commit it, update the file locally but SKIP the commit/push in this phase — surface that override now, not after you've already run the commit.
2. **Open `CLAUDE.md`** in the project root.
3. **Update these sections** (create them if they don't exist):

### Current Phase
State the current build phase and what specifically has been completed within it.

### Known Issues
List any bugs, failing tests, architectural decisions pending, or blockers.

### Last Session
```
**Date:** <today's date>
**Who:** <developer name or "Claude session">
**What was done:** <bullet list of what was built/changed/fixed>
**What's next:** <bullet list of the immediate next steps>
**Branch:** <current branch name>
**Blockers:** <any blockers, or "None">
**Claude session ID (reference only):** <id>  <!-- For manual `claude --resume <id>` if you need raw transcript context. /session-start does NOT auto-resume — it reads this CLAUDE.md instead. -->

```

### Known Gotchas
If any build, deploy, or environment gotchas were discovered this session, append them to a `## Known Gotchas` section in the project CLAUDE.md. Format each entry as:
```
- **<symptom>** → <root cause> → <fix>
```
These prevent Claude from rediscovering the same issues next session. Only add genuinely reusable knowledge — not one-off typos or transient errors.

### Paused UAT Interview (if applicable)
If a UAT interview was in progress when the session ended, capture the full state so it can be resumed:
```
**Ticket(s):** <ticket-id(s) being tested>
**Total questions:** <N>
**Completed:** <M of N>
**Results so far:**
  - Test 1: <description> → Pass
  - Test 2: <description> → Fail — "<user's notes>"
  - Test 3: <description> → Pass
**Remaining:**
  - Test 4: <description>
  - Test 5: <description>
  ...
```
This section is removed once the UAT interview is completed or the ticket is closed.

4. **Sweep for stale references before committing** — scan the handoff for outdated build numbers, PR states ("PR #1 open" after it merged), or "next task" lines that no longer match reality, and fix them. Handoff notes drift mid-session, not just at the end.
5. **Commit the CLAUDE.md update** — unless step 1's project override says not to — `git add CLAUDE.md && git commit -m "chore: update session handoff notes"`
6. **Push** if not already pushed.

## Phase 3: Linear Update

1. **If a ticket was being worked on:**
   - If work is complete: update status to `Done` or `In Review`. Add closing comment with: what was implemented, files changed, any follow-up items.
   - If work is incomplete: keep status as `In Progress`. Add comment with: what was done, what remains, estimated remaining effort, any blockers.
2. **If no ticket was being worked on:** skip this phase.

## Phase 4: Capture session friction

Record this session's friction for `/retro` to consolidate later. This is the **push** half of the memory loop, and it runs here — on this deliberate, visible wrap-up — rather than off a background hook (a closed or non-clean CLI exit, e.g. the VS Code plugin, can't be trusted to fire).

1. **Tell the user you're capturing**, e.g. "Capturing this session's friction (errors + a quick Sonnet pass)…", then **run it synchronously and wait for it to finish:**
   ```
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/retro-capture.py --session --semantic
   ```
   It finds this session's transcript automatically, appends mechanical friction (tool errors / failed commands) and a gated Sonnet semantic pass (repeated corrections, rework, stated preferences) to `~/.claude/insights/friction/<project-key>.md`, and prints a one-line summary. **This is a blocking, foreground call** — the semantic pass runs inline (a few seconds, hard-capped at 60s) and the command does not return until everything is written. **Never background it** (no `&`, no detach): `/session-end` must not report done while capture is still running.
2. **Show the user the summary line it printed**, then state it's complete — so they can see exactly what was captured (or that the session was clean) and know nothing is left running.

This does not change anything in the repo or CLAUDE.md; it only writes to the friction log that `/retro` reads. If the script is missing (`${CLAUDE_PLUGIN_ROOT}/scripts/retro-capture.py` not found), skip silently.

## Phase 5: Summary

Present a clean summary to the user:

```
Session Summary
───────────────
Branch: <branch name>
Commits: <number of commits this session>
Status: <clean / pushed / up to date>
CLAUDE.md: <updated / already current>
Linear: <ticket-id status updated / no ticket>
Friction: <captured: N errors + semantic / clean session>
Next steps: <1-2 sentence summary of what comes next>
```

## Key Principles

- **Nothing is left uncommitted.** WIP commits are fine. Lost work is not.
- **Nothing is left unpushed.** Local-only branches are invisible to your co-founder.
- **CLAUDE.md is the handoff note.** The next person (or the next Claude instance) should be able to pick up exactly where you left off by reading it.
- **Linear is the coordination layer.** If you worked on a ticket, update it. If you didn't, don't create noise.
- **This skill is fast.** It should take under 2 minutes. Don't turn it into a retrospective — that's what `/retro` is for.
