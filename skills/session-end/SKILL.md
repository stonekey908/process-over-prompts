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

## Phase 4: Summary

Present a clean summary:
- Branch name and current state
- Commits made this session
- Ticket status
- Documentation state
- Any next steps for the following session

## Key Principles

- **Takes under 2 minutes** — this is a checklist, not a retrospective
- **Never end with uncommitted work** — stash it, WIP-commit it, or finish it
- **Never end with unpushed commits** — work that only exists locally is work at risk
- **Always leave a handoff note** — the next session should never start confused
