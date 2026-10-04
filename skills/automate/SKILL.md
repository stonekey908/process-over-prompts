---
name: automate
description: Autonomous development pipeline — chains skills from ticket pickup through implementation, testing, and commit. Three-tier escalation, mock layer, visual + functional UAT. Use after Linear tickets and wireframes are ready.
---

# Automate Skill

Chains existing skills into a fully autonomous pipeline. You invoke this after tickets are on Linear and wireframes are locked. It implements, tests, and commits — pausing only when it genuinely needs you.

**What it does:** Pre-flight → Implement → Mock Layer → SETUP.md → Visual UAT → Functional UAT → Report
**What it does NOT do:** Requirements (/requirements), wireframing (/design-first), merge to main (you control), real backend setup (pauses and documents)

## Escalation Model

Every decision during automation falls into one of three tiers:

| Tier | Risk | Action | Examples |
|------|------|--------|----------|
| **Auto-resolve** | Low, reversible | Decide + log to AUTOMATE-LOG.md | Component naming, file structure, test approach, import ordering, code formatting |
| **Queue + continue** | Medium, debatable | Best guess + `[DECISION-PENDING]` comment in code + log to AUTOMATE-LOG.md | Library choice between two valid options, where to place a shared component, UX micro-decision not in wireframe, animation approach |
| **Hard stop** | High, irreversible | Stop + `AskUserQuestion` | Auth provider choice, data deletion logic, contradictory acceptance criteria, security-sensitive decisions, choosing between fundamentally different architectures |

`[DECISION-PENDING]` markers in code are `grep`-able. Review the AUTOMATE-LOG.md at any time.

## Pause/Resume (applies to ALL phases)

**/automate can be paused at any point and resumed in a later session.**

**On pause** (user says stop/pause/done, or session is ending):
1. Immediately write `## Automate State` to the project's CLAUDE.md:
   ```
   ## Automate State
   **Status:** In Progress
   **Phase:** 3 of 7 (Mock Layer)
   **Tickets:** STO-610, STO-611, STO-612
   **Branch:** feat/automate-STO-610-612
   **Completed:**
     - Phase 1: Pre-flight ✓
     - Phase 2: Implementation ✓ (3/3 tickets)
     - Phase 3: Mock layer — 2/4 external deps mocked
   **Next action:** Create mock for Stripe webhook endpoint
   **Pending decisions:** 2 (see AUTOMATE-LOG.md)
   **Hard stops:** 0
   **Mock mode:** MOCK_MODE=true in .env.local
   ```
2. Commit: `wip(<ticket-ids>): automate paused at phase X`
3. Push to remote
4. Update Linear tickets with progress comment
5. Delegate to `/session-end` for standard wrap-up

**On resume** (user invokes `/automate` after `/session-start` detects state):
1. Read `## Automate State` from CLAUDE.md
2. Read AUTOMATE-LOG.md for detailed context (decisions, blockers, phase summaries)
3. Pick up at the exact next action — no re-reading tickets, no re-planning, no re-implementing completed work
4. Continue the pipeline from where it left off

**AUTOMATE-LOG.md** survives context window resets. Each phase writes a summary before transitioning to the next. Format:
```markdown
# Automate Decision Log

## Phase Summaries
- [2026-02-27 14:00] PHASE 1 COMPLETE — Platform: web (Next.js 14), 3 tickets, emulator: N/A, Playwright: will install
- [2026-02-27 14:30] PHASE 2 COMPLETE — 3/3 tickets implemented, 2 pending decisions, 0 hard stops

## Pending Decisions
- [2026-02-27 14:23] PHASE 2 — Used framer-motion for transitions (already in package.json). Alternative: react-spring. [DECISION-PENDING]

## Auto-Resolved
- [2026-02-27 14:10] Named component UserProfileCard following existing *Card pattern

## Hard Stops
(none)
```

## Phase 1: Pre-flight

1. **Verify Linear MCP** — call `mcp__linear` to fetch a ticket. If it fails: STOP. Tell the user to restart the CLI.
2. **Detect platform** from project config:
   - `app.json` or `app.config.js` → **Mobile** (Expo/React Native)
   - `next.config.js` or `next.config.ts` → **Web** (Next.js)
   - Both → **Cross-platform** (test both)
   - State the platform explicitly in AUTOMATE-LOG.md.
3. **Check git state** — clean tree, on `main` and up to date. Create feature branch: `feat/automate-<ticket-ids>`. Push immediately.
4. **Fetch all tickets** from Linear via MCP — read titles, descriptions, acceptance criteria, labels, blocking dependencies, wireframe references.
5. **Check for pre-launched emulator/simulator:**
   - iOS: `xcrun simctl list devices | grep Booted` — note which device
   - Android: `adb devices` — note which device
   - Web: N/A (Playwright handles its own browser)
   - If no device found and platform is mobile: note it, will attempt to boot in Phase 5 or fall back to semi-auto
6. **Check for `## Automate State` in CLAUDE.md** — if found, this is a **resume**. Skip to the recorded next action. Do not re-read tickets or re-plan.
7. **Create AUTOMATE-LOG.md** if it doesn't exist (use template above). Log pre-flight results.
8. **Update all ticket statuses** → In Progress. Add comment: "Starting autonomous implementation via /automate."

## Phase 2: Autonomous Implementation

This is the bulk of the work. Follow `/sprint` Phase 2-4 internals but with **auto-approved plans**.

0. **Locate the mockup for this ticket.** If a wireframe or design reference exists (Figma link, file in `docs/`, attached to the Linear ticket), open it and pin it as the visual contract. If no mockup exists for a UI ticket: log to AUTOMATE-LOG.md as `[DECISION-PENDING]` and use sensible defaults — don't invent a design. Phase 5 visual UAT will catch divergences but the goal is to not diverge in the first place.
1. **Research the codebase** — identify files, components, modules involved per ticket. Check existing patterns, imports, dependencies.
2. **Plan the approach** — files that will change, dependencies needed, risks. **Do NOT wait for user approval** — auto-approve and proceed. Log the plan to AUTOMATE-LOG.md.
3. **For independent tickets:** use sub-agents to implement in parallel (multi-ticket mode — see `/sprint`). For tickets with shared file dependencies: implement sequentially.
   - **Sub-agent file-scope boundaries:** each sub-agent must receive an explicit list of files/directories in scope. No two agents should write to the same file. If file conflicts are detected between tickets, serialize those tickets instead of parallelising. Use sub-agents for read-only exploration; keep writes in scoped agents that don't overlap.
4. **Implement in small increments** — one logical unit at a time. After each increment:
   a. Run type checker (`npx tsc --noEmit` or project equivalent) — fix immediately
   b. Run linter (`npm run lint`) — fix immediately
   c. Run test suite (`npm test`) — fix immediately
   d. **Write tests for new code in this increment** — happy path + at least one edge case. Run them. Must pass.
   e. Do NOT proceed to next increment until a-d pass
5. **Apply the escalation model** at every decision point:
   - Auto-resolve: decide and log
   - Queue + continue: best guess, `[DECISION-PENDING]` in code comment, log to AUTOMATE-LOG.md
   - Hard stop: `AskUserQuestion` and wait
6. **Commit after each ticket's quality gate passes:**
   - `git add <specific files> && git commit -m "feat(<ticket-id>): <description>"`
   - `git push` — keep remote current
7. **If blocked after 3 attempts** on any ticket: log the blocker to AUTOMATE-LOG.md, add Linear comment, skip the ticket, continue with others.
8. **Write phase summary** to AUTOMATE-LOG.md before moving to Phase 3.

## Phase 2.5: Integration Proof (DO NOT SKIP)

Before mocking and UAT, prove each ticket is plumbed end-to-end.

1. **For each ticket**, exercise ONE happy-path flow through the full stack:
   - User-facing trigger → API route → data layer → response → UI render
   - Capture the actual log/network output as evidence
2. **If the flow breaks at any layer:** that's a Phase 2 incompletion, not a Phase 5 finding. Return to Phase 2, fix it, re-prove.
3. **No ticket exits Phase 2.5 until its happy path runs end-to-end.** "Components render" is not enough. "Type-check passes" is not enough.
4. Log the integration proof per ticket to AUTOMATE-LOG.md.

This phase prevents the "every layer compiles individually but nothing actually works together" failure mode.

## Phase 3: Mock Layer

Detect external dependencies and create a full mock layer so the app runs offline.

1. **Scan for external dependencies:**
   - Read `.env.example` / `.env.local.example` for placeholder values
   - Scan code for API calls to external services (Supabase, Firebase, Stripe, Gemini, etc.)
   - Check `package.json` for SDK dependencies that need credentials
2. **Create `__mocks__/` directory structure:**
   ```
   __mocks__/
     services/        # Mock client per external service
       supabase.mock.ts
       stripe.mock.ts
     data/            # Realistic seed data (JSON fixtures)
       users.json
       documents.json
     index.ts         # Mock registry + isMockMode check
   ```
3. **Write the mock registry:**
   ```typescript
   // __mocks__/index.ts
   export const isMockMode = process.env.MOCK_MODE === 'true';
   ```
4. **Wire mock layer** in service files: `isMockMode ? mockClient : realClient`
5. **Mock data rules:**
   - Realistic data — real-looking names, dates, amounts. Never "test123" or "foo bar"
   - Every mock has a comment: `// MOCK: Replace with real <service>. See SETUP.md step N`
   - Mock responses match the expected schemas (same shape as real API responses)
6. **Add `MOCK_MODE=true`** to `.env.local` and `.env.example`
7. **Verify the app starts and runs** fully in mock mode. Fix any issues.
8. **Verify tests pass** against mocks (CI should pass without real services).
9. **Log** all detected dependencies and mock status to AUTOMATE-LOG.md.
10. **Commit:** `feat(<ticket-ids>): add mock layer for offline development`

## Phase 4: SETUP.md

Generate or update the project's SETUP.md following the CLAUDE.md manual setup rules.

1. **If SETUP.md doesn't exist:** create it. If it does: update it.
2. **Quick Start section** — must always work with mocks:
   ```markdown
   ## Quick Start (Just Run It)
   1. Open your terminal
   2. Run `cd /path/to/project`
   3. Run `cp .env.example .env.local` — creates your settings file (mock mode by default)
   4. Run `npm install` — wait for "added X packages"
   5. Run `npm run dev` — you should see "Ready on http://localhost:3000"
   6. Open http://localhost:3000 — the app runs with fake data
   ```
3. **Per-service setup sections** — one section per external dependency:
   - Written "like explaining to a 10-year-old" — no assumed knowledge
   - Numbered steps with expected outcome at each step
   - Each step has: what to do, what you'll see, what to do if it doesn't work
   - Each service section is independent (can set up Supabase without needing Stripe)
4. **Separate clearly:** "One-time setup" vs "Every time you pull" vs "Deploying"
5. **Keep `.env.example` in sync** with all required variables and clear placeholder names
6. **When a new dependency was added** during Phase 2/3 → add a new SETUP.md section
7. **Commit:** `docs(<ticket-ids>): generate/update SETUP.md with mock-to-real migration guide`

## Phase 5: Visual UAT

Automated screenshot capture and comparison against locked wireframes.

1. **Start the dev server:**
   - Mobile: `npx expo start`
   - Web: `npm run dev`
2. **Connect to emulator/browser:**
   - Mobile (iOS): use the booted simulator detected in Phase 1. If none: attempt `xcrun simctl boot "iPhone 16"`. If that fails: flag for semi-auto.
   - Mobile (Android): use the connected device from Phase 1. If none: attempt `emulator -avd <default>`. If that fails: flag for semi-auto.
   - Web: install Playwright if not present (`npx playwright install chromium`). Launch headless browser.
3. **Navigate each screen and capture screenshots:**
   - Web: use Playwright to navigate each route, capture via `page.screenshot({ path: '__screenshots__/<route>.png' })`
   - Mobile (iOS): navigate via deep links or vision-driven tap, capture via `xcrun simctl io booted screenshot __screenshots__/<screen>.png`
   - Mobile (Android): navigate via deep links or `adb shell input tap X Y`, capture via `adb exec-out screencap -p > __screenshots__/<screen>.png`
4. **Compare each screenshot against the locked wireframe** using Claude's vision analysis. Check for:
   - **Layout:** misaligned text, overlapping elements, cut-off content, inconsistent spacing
   - **Typography:** wrong font weight, text truncation without ellipsis, line height issues, font size inconsistency
   - **Components:** icons not vertically centered, inconsistent button padding, missing hover/pressed states, broken dark mode
   - **Responsiveness:** content not filling available width, unexpected horizontal scroll, elements pushed off-screen
5. **Grade each screen:**
   - **Match** — looks correct, no issues
   - **Minor deviation** — small differences that may be intentional → log as `[DECISION-PENDING]`
   - **Major deviation** — clearly wrong → attempt auto-fix, re-screenshot, verify
6. **Severity classification for issues found:**
   - **HIGH** → auto-fix attempt (up to 3 tries) → re-screenshot → verify. If can't fix: log as blocker.
   - **MED** → queue to AUTOMATE-LOG.md as `[DECISION-PENDING]`
   - **LOW** → log as auto-resolved, no action
7. **Fallback to semi-auto:** if Claude can't navigate somewhere (requires real auth, complex gestures, multi-step flows): flag it — "Can't reach Settings screen — requires authenticated session. Please navigate there and I'll capture the screenshot."
8. **Log all results** to AUTOMATE-LOG.md with screenshot file paths.
9. **Commit screenshots:** `test(<ticket-ids>): visual UAT screenshots`

## Phase 6: Functional UAT

Automated functional verification.

1. **Run full test suite:** `npm test` — all must pass.
2. **Run production build:** `npm run build` — must pass. Catches SSR, route export, and bundle errors.
3. **Exercise API routes** with mock data — verify responses match expected schemas.
4. **Test edge cases** from acceptance criteria:
   - Empty states (no data, first-time user)
   - Error states (network failure, invalid input, permission denied)
   - Boundary conditions (max length, zero, negative values)
5. **Verify loading states** render and resolve correctly.
6. **Verify RBAC/permissions** if applicable — test each role against each protected route.
7. **Check all `[DECISION-PENDING]` code paths** still work correctly.
8. **If failures found:** attempt auto-fix (up to 3 attempts per issue), run tests again, log outcome.
9. **Log all results** to AUTOMATE-LOG.md with pass/fail per acceptance criterion.
10. **Commit any fixes:** `fix(<ticket-ids>): <description> — found during functional UAT`
11. **Interactive UAT interview** — for any user-facing acceptance criterion, run the `/uat` Phase 2b interview format. Functional UAT in /automate is automated checks PLUS a Claude-led interview, not just automated checks.

## Phase 7: Report + Close

**This is the only mandatory checkpoint.** Everything before this runs autonomously.

1. **Generate summary report:**
   ```
   Automate Run Complete
   ─────────────────────
   Tickets: STO-610 ✓, STO-611 ✓, STO-612 ✗ (blocked — see below)
   Branch: feat/automate-STO-610-612
   Commits: 7

   Visual UAT:
     Dashboard: Match ✓
     Settings: Minor deviation (font weight) [DECISION-PENDING]
     Profile: Match ✓

   Functional UAT:
     Tests: 142 pass, 0 fail
     Build: Pass
     API routes: 8/8 pass
     Edge cases: 12/14 pass, 2 [DECISION-PENDING]

   Pending Decisions: 3 (see AUTOMATE-LOG.md)
   Mock Dependencies: Supabase, Stripe (see SETUP.md)
   Blocked Tickets: STO-612 — websocket pattern not in codebase, needs direction
   ```
2. **Present report to user.** Wait for sign-off.
3. **On sign-off:**
   - Update all completed Linear tickets → Done
   - Add closing comment to each: what was implemented, files changed, test coverage, follow-up items
   - Clean up AUTOMATE-LOG.md — move pending decisions to a "Review Needed" section at the top
   - Remove `## Automate State` section from CLAUDE.md (run is complete)
   - Branch is ready for merge instruction
4. **If user says "not done":** ask which phase to re-enter. Resume from there.
5. **User controls merge** — never merge to main without explicit instruction.

## Key Principles

- **Autonomous by default** — auto-approve plans, auto-resolve low-risk decisions, keep moving
- **Queue don't block** — medium-risk decisions get a best guess + [DECISION-PENDING], never stop the pipeline
- **Hard-stop only when irreversible** — security, data deletion, contradictory requirements
- **Commit early, push often** — after every ticket's quality gate, after mock layer, after UAT
- **Mock everything** — the app must run offline with realistic data. CI must pass without real services.
- **SETUP.md is the bridge** — from mock to real, written for a 10-year-old
- **One checkpoint** — Phase 7 report. Everything else is autonomous.
- **Pause anywhere** — state persists in CLAUDE.md, detail in AUTOMATE-LOG.md, resume is seamless
- **Platform-aware** — detect mobile vs web, use the right tools for each
- **Existing skills are building blocks** — /automate orchestrates, /sprint internals do the coding, /uat patterns inform testing. Don't reinvent.
- **User controls merge** — never merge to main without explicit instruction
- **Escalate, don't spin** — if blocked after 3 attempts, log it, skip it, continue with the rest
