# Session End

Clean session wrap-up — ensures all work is committed, pushed, documented, and handed off before ending. Use when finishing a coding session, switching projects, or when the conversation is wrapping up. Prevents lost work, stale branches, and confusion for the next session.

---

## Phase 1: Code State Check

1. **Run `git status`** — check for uncommitted changes.
2. **If uncommitted changes exist:**
   - If the work is complete: stage and commit with a proper conventional commit message.
   - If the work is incomplete: commit with `wip(<ticket-id>): <description>`. WIP commits are fine. Uncommitted work is not.
3. **Check for unpushed commits:** `git log @{upstream}..HEAD`
   - If unpushed: `git push`
4. **Confirm clean state** — clean working tree, all commits pushed to remote.

## Phase 2: Documentation Update

1. **Update the project's instruction file** (policy file, project config, or equivalent) with:
   - **Current Phase** — where the work stands
   - **Known Issues** — anything broken, incomplete, or needing attention
   - **Last Session** — date, what was done, what's next, which branch, any blockers

This is the handoff note. The next session (which may be a different person or a different AI instance) reads this first.

## Phase 3: Project Management Update

1. **If a ticket was being worked on**, update its status and add a closing comment:
   - What was accomplished
   - What's remaining (if anything)
   - Branch name and latest commit
2. **If work is complete**, move to `Done` or `In Review` as appropriate.
3. **If work is incomplete**, leave at `In Progress` with a clear comment about what's left.

## Phase 4: Capture Session Friction

Record what went wrong this session so **Retrospective** can consolidate it later. This is the "push" half of the improvement loop — it runs here, on a deliberate wrap-up, not silently in the background.

1. **Append this session's friction to a per-project friction log** (a `friction.md` in the project, or wherever your tool keeps per-project notes):
   - **Mechanical** — failed commands, tool errors, anything that broke and had to be retried.
   - **Behavioural** — where the user corrected you, what was reworked, and any preference the user stated for next time. Summarise these yourself in a few terse bullets, using whatever model you're already running.
2. **Keep it short and honest.** A clean session logs little or nothing — don't invent friction.
3. **Tag the softer entries as unverified.** They're a model's read of the session; the next reader should weight them below the mechanical facts.

If nothing went wrong, say so and write nothing.

## Phase 5: Summary

Present a clean summary:
- Branch name and current state
- Commits made this session
- Ticket status
- Documentation state
- Friction captured (a count, or "clean session")
- Any next steps for the following session

## Key Principles

- **Takes under 2 minutes** — this is a checklist, not a retrospective
- **Never end with uncommitted work** — stash it, WIP-commit it, or finish it
- **Never end with unpushed commits** — work that only exists locally is work at risk
- **Always leave a handoff note** — the next session should never start confused
- **Capture friction, don't fix it** — logging the friction is this skill's job; consolidating it into your rules is Retro's. Don't blur the two.
