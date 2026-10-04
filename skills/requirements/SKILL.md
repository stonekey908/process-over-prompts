---
name: requirements
description: Turn a vague idea into a Linear ticket with clear acceptance criteria. Researches feasibility, defines scope, creates the ticket. Use before /sprint or /design-first.
---

# Requirements Skill

Take something fuzzy ("I want the app to show weather") and turn it into something buildable — a Linear ticket with clear scope, acceptance criteria, and enough context that `/sprint` can pick it up without guessing.

## Phase 1: Understand the Intent

1. **Listen to what the user wants.** It might be:
   - A vague idea ("something like a settings page")
   - A specific feature ("add push notifications for weather alerts")
   - A problem ("users can't find their saved items")
   - A reference ("make it work like how Spotify does playlists")

2. **If the idea is broad or creative**, use brainstorming to explore the problem space before narrowing scope. This prevents jumping to the first solution and ensures the best approach surfaces.

3. **Ask clarifying questions** — but only the ones that matter:
   - Who is this for? (which user, which context)
   - What's the trigger? (when does the user need this)
   - What does success look like? (how do we know it's working)
   - What's explicitly out of scope? (what are we NOT building)

4. **Don't over-interview.** If the user has a clear picture, move on. If they're vague, ask just enough to define the edges. Three good questions beat ten mediocre ones.

## Phase 2: Research Feasibility

Before writing anything down as a commitment, check what's actually possible:

1. **Check the existing codebase:**
   - Is there anything similar already built? (don't reinvent)
   - What components, services, or patterns would this touch?
   - Are there architectural constraints? (e.g., Expo Go limitations, Firebase plan limits)

2. **Check external dependencies:**
   - If it needs an API, does the API exist and work with our stack?
   - If it needs a new library, is it compatible with the current Expo SDK?
   - If it needs device capabilities, does Expo Go support them?

3. **Flag risks early:**
   - "This would require ejecting from Expo Go" = major flag
   - "This API has rate limits that might affect UX" = worth noting
   - "This touches the auth flow which is fragile" = call it out

4. **Present feasibility findings to the user.** If something isn't feasible as described, suggest alternatives before writing the ticket.

## Phase 3: Define Scope

1. **Write a clear problem statement:** One or two sentences. What problem does this solve, for whom, in what context?

2. **Define acceptance criteria.** Each one must be:
   - **Testable** — you can verify it by looking at the app or running a test
   - **Specific** — "weather displays correctly" is bad. "Current temperature, condition icon, and location name are visible on the home screen without scrolling" is good.
   - **Independent** — each criterion can be verified on its own

3. **Define what's out of scope.** Be explicit. "This ticket does NOT include: push notifications, historical weather data, or multiple location support." This prevents scope creep during `/sprint`.

4. **Identify dependencies:**
   - Does this need another ticket completed first?
   - Does this need a design decision? (→ maybe `/design-first` before `/sprint`)
   - Does this need external setup? (API keys, service accounts)

5. **Suggest a size estimate.** Based on the feasibility research:
   - Small (single screen, no new dependencies, straightforward)
   - Medium (multiple files, new integration, some complexity)
   - Large (new feature area, multiple screens, architectural changes)
   - If Large → suggest breaking into smaller tickets

## Phase 3.5: Sprint Structure (MANDATORY — Linear Nomenclature)

**Sprints are the unit of sequencing.** Every ticket created or modified through this skill MUST be assigned to exactly one sprint. No exceptions.

### Sprint Nomenclature — Single Source of Truth

- **Term:** `sprint`. Never `wave`, `slice`, `batch`, `phase`, `tranche`, or any synonym anywhere in Linear. If a previous ticket uses a different term, treat it as a bug and align it to `sprint` when you touch it.
- **Mechanism:** Linear **labels**, formatted `sprint-N` (e.g., `sprint-1`, `sprint-2`, `sprint-3`). NEVER put sprint numbers in ticket titles. NEVER use a custom field or description tag — always a label.
- **Cardinality:** Exactly **one** `sprint-N` label per ticket. Never zero (orphaned). Never two (split across sprints). If a ticket is moving between sprints, the old label is removed in the same operation that adds the new one — both must never coexist on the ticket.

### Sprint Assignment Rules

1. **Upfront chunking:** Before creating any tickets in Phase 4, break the full body of work into sprints. Present the sprint plan (sprint number → one-line goal → tickets) and wait for explicit user approval. No ticket is created without a sprint already assigned to it.
2. **Never orphan a new ticket:** When the user adds a new requirement mid-stream — scope expansion, ticket split, follow-up filing, anything — the new ticket MUST inherit a `sprint-N` label before it leaves this skill. Default to the parent ticket's sprint; if the new work clearly belongs to a different sprint, propose which one and confirm before creating.
3. **Retain structure on edits:** When editing existing tickets (re-titling, adjusting acceptance criteria, re-scoping, splitting), the existing sprint label is preserved untouched unless the user explicitly asks to move it.
4. **Moving between sprints is atomic:** "Move STO-123 to sprint 3" means remove `sprint-2` AND add `sprint-3` in the same `save_issue` call. Never leave both attached, even momentarily. Confirm with the user before reassigning.
5. **No silent corrections:** If you encounter an existing ticket that violates these rules (no sprint label, sprint in title, multiple sprints), flag it to the user and propose a fix — do not silently rewrite.

### Sprint Plan Presentation Format

```
Sprint 1 — <one-line goal>
  - <ticket title 1>
  - <ticket title 2>

Sprint 2 — <one-line goal>
  - <ticket title 3>
  - <ticket title 4>
```

Wait for explicit approval on the chunking before any tickets are created.

## Phase 4: Create the Ticket

1. **Create a Linear ticket** via MCP with:
   - **Title:** Clear, action-oriented. "Add weather display to home screen" not "Weather feature". **Never include a sprint number, slice, or wave reference in the title.**
   - **Description:** Problem statement, approach summary from feasibility research, any technical notes
   - **Acceptance criteria:** The testable list from Phase 3
   - **Out of scope:** Explicitly stated
   - **Sprint label (MANDATORY):** Exactly one `sprint-N` label from the agreed sprint plan in Phase 3.5. Never zero. Never multiple. Verify after creation that exactly one is attached.
   - **Other labels:** Appropriate project labels (component, area, type, etc.) — never overlap with the sprint label.
   - **Priority:** Based on user input
   - **Dependencies:** Linked as blocking relationships if applicable

2. **If the feature needs design work**, also create a linked design ticket and note that `/design-first` should run before `/sprint`.

3. **If the feature is too large**, create an epic/parent ticket with sub-tickets, each independently buildable and testable.

4. **Present the ticket to the user for review.** They may want to adjust scope, priority, or acceptance criteria before it goes into the backlog.

## Key Principles

- **Feasibility before commitment** — don't write tickets for things that can't be built in the current stack
- **Testable acceptance criteria** — if you can't verify it, you can't ship it
- **Explicit scope boundaries** — what's out of scope matters as much as what's in
- **Right-size tickets** — a ticket that takes more than one `/sprint` session is too big, break it up
- **Sprint structure is sacred** — every ticket gets exactly one `sprint-N` label, assigned upfront, retained on every edit, swapped (never duplicated) when moved between sprints. Term is always `sprint`, mechanism is always a Linear label, never the title.
- **The user defines value** — you research and structure, they decide what matters
- **Use brainstorming freely** — when ideas are broad, creative, or ambiguous, explore the problem space before narrowing. The requirements skill structures the output; brainstorming enriches the input.
