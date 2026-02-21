# Requirements

Turn a vague idea, feature request, or problem statement into a well-structured ticket with clear acceptance criteria. Use before Sprint — this creates the ticket that Sprint picks up.

---

## Phase 1: Understand the Intent

1. **Listen to what the user wants.** It might be:
   - A vague idea ("something like a settings page")
   - A specific feature ("add push notifications for weather alerts")
   - A problem ("users can't find their saved items")
   - A reference ("make it work like how Spotify does playlists")

2. **Ask clarifying questions** — but only the ones that matter:
   - Who is this for? (which user, which context)
   - What's the trigger? (when does the user need this)
   - What does success look like? (how do we know it's working)
   - What's explicitly out of scope? (what are we NOT building)

3. **Don't over-interview.** If the user has a clear picture, move on. Three good questions beat ten mediocre ones.

## Phase 2: Research Feasibility

Before writing anything down as a commitment, check what's actually possible:

1. **Check the existing codebase:**
   - Is there anything similar already built?
   - What components, services, or patterns would this touch?
   - Are there architectural constraints?

2. **Check external dependencies:**
   - If it needs an API, does the API exist and work with the stack?
   - If it needs a new library, is it compatible?
   - If it needs device capabilities, does the current framework support them?

3. **Flag risks early:**
   - Framework limitations (e.g., "this would require ejecting from the managed workflow")
   - API constraints (rate limits, pricing, auth complexity)
   - Fragile areas ("this touches the auth flow which is complex")

4. **Present feasibility findings.** If something isn't feasible as described, suggest alternatives before writing the ticket.

## Phase 3: Define Scope

1. **Write a clear problem statement.** One or two sentences — what problem, for whom, in what context.

2. **Define acceptance criteria.** Each one must be:
   - **Testable** — you can verify it by looking at the app or running a test
   - **Specific** — "weather displays correctly" is bad. "Current temperature, condition icon, and location name are visible on the home screen without scrolling" is good.
   - **Independent** — each criterion can be verified on its own

3. **Define what's out of scope.** Be explicit. "This ticket does NOT include: push notifications, historical data, or multi-location support." Prevents scope creep during Sprint.

4. **Identify dependencies:**
   - Does this need another ticket first?
   - Does this need a design decision? (→ Design-First before Sprint)
   - Does this need external setup? (API keys, service accounts)

5. **Suggest a size estimate:**
   - Small (single screen, no new dependencies, straightforward)
   - Medium (multiple files, new integration, some complexity)
   - Large (new feature area, multiple screens, architectural changes)
   - If Large → suggest breaking into smaller tickets

## Phase 4: Create the Ticket

1. **Create a ticket** in your project management tool with:
   - **Title:** Clear, action-oriented. "Add weather display to home screen" not "Weather feature"
   - **Description:** Problem statement, approach summary, technical notes
   - **Acceptance criteria:** The testable list from Phase 3
   - **Out of scope:** Explicitly stated
   - **Labels:** Appropriate project labels
   - **Priority:** Based on user input
   - **Dependencies:** Linked as blocking relationships if applicable

2. **If the feature needs design work**, create a linked design ticket and note that Design-First should run before Sprint.

3. **If the feature is too large**, create a parent ticket with sub-tickets, each independently buildable and testable.

4. **Present the ticket for review.** The user may adjust scope, priority, or acceptance criteria before it enters the backlog.

## Key Principles

- **Feasibility before commitment** — don't write tickets for things that can't be built in the current stack
- **Testable acceptance criteria** — if you can't verify it, you can't ship it
- **Explicit scope boundaries** — what's out of scope matters as much as what's in
- **Right-size tickets** — a ticket that takes more than one Sprint session is too big, break it up
- **The user defines value** — you research and structure, they decide what matters
