---
name: sprint
description: Execute a sprint on Linear tickets — pickup, plan with approach options, implement in vertical slices, quality gates, UAT, commit. Supports single-ticket and multi-ticket parallel modes.
---

# Sprint Skill

Supports two execution modes:
- **Single-ticket** (default) — one ticket, one branch, straightforward flow
- **Multi-ticket** — batch of related tickets from the same `sprint-N`, parallel sub-agents, batch-level approval

The skill detects which mode based on input. One ticket = single mode. Multiple tickets = multi-ticket mode.

**Linear nomenclature:** Sprints are represented as `sprint-N` Linear labels (see the `/requirements` skill for the full rules). Never use `wave`, `slice`, `batch`, or any other term in ticket titles, comments, or branch names. Every ticket this skill touches must already carry exactly one `sprint-N` label — if it doesn't, flag it to the user before proceeding.

## Phase 0: Pre-Flight (DO NOT SKIP)

1. **Verify Linear MCP** — call `mcp__linear` to list projects or fetch a ticket. If it fails: STOP. Tell me to restart the CLI. NEVER attempt workarounds.
2. **Verify project context** — confirm correct directory (`package.json`, `app.json`), correct stack, CLAUDE.md loaded.
3. **Verify git state** — `git status`, confirm clean tree, confirm branch is `main` and up to date.
4. **Identify scope** — single ticket or multi-ticket? If multi-ticket: which tickets, their shared `sprint-N` label, their dependencies, their parent epics. Confirm all tickets in scope share the same sprint label — if they don't, ask the user before bundling them.

If any check fails, stop and report. Do not proceed.

## Phase 1: Ticket Pickup

### Single-Ticket Mode
1. Fetch the ticket from Linear via MCP — read title, description, acceptance criteria, labels, priority, blocking dependencies.
2. Update Linear status → `In Progress`
3. Add Linear comment: "Starting work. Will update with approach before implementation."
4. Create feature branch: `git checkout -b feat/<ticket-id>-<short-description>`
5. **Push immediately:** `git push -u origin feat/<ticket-id>-<short-description>` — remote tracking from the start.

### Multi-Ticket Mode
1. Fetch all tickets in the batch from Linear via MCP — read titles, descriptions, acceptance criteria, labels, blocking dependencies. Confirm they all share the same `sprint-N` label.
2. Create a single feature branch for the batch, named after the sprint: `git checkout -b feat/sprint-N-<short-description>` (e.g., `feat/sprint-3-auth-flows`)
3. **Push immediately:** `git push -u origin feat/sprint-N-<short-description>` — remote tracking from the start.
4. Update all ticket statuses → `In Progress`
5. Add pickup comment to each ticket: "Starting as part of sprint-N batch. Parallel execution with [list sibling ticket IDs]."
6. Present the batch plan — which tickets (all from the same `sprint-N`), which sub-agents run in parallel, which are sequential. **Wait for approval before proceeding.**

## Phase 2: Research & Plan (BEFORE ANY CODE)

1. **Identify the platform and stack** — check `app.json`, `package.json`, or project config to determine: mobile (iOS/Android/both) or web? What framework version (Expo SDK, Next.js, etc.)? What styling system (NativeWind, Tailwind, styled-components)? State these explicitly in the plan. All subsequent advice must target the correct platform.
2. **Read the relevant codebase** — identify files, components, modules involved. Check existing patterns, imports, dependencies.
3. **If integrating a new API/service** — search official docs, verify compatibility with the project's stack, check SDK version issues.
4. **Present 2-3 architectural approaches with tradeoffs** — for any task involving architecture, infrastructure, integration, or non-trivial implementation decisions. Include: approach name, how it works, pros, cons. For straightforward tasks (simple bug fix, minor UI tweak), a single brief plan is fine.
5. **Plan work as vertical slices** — each increment should deliver working frontend + backend, not "all API routes then all UI". State the slice order explicitly. For backend-only or UI-only tickets, standard incremental approach is fine.
   - In multi-ticket mode: group by ticket, map parallel vs sequential execution, identify shared file conflicts.
6. **Timebox this phase.** Simple bug fix → 2-3 minutes research. Medium feature → 10 minutes max. Complex architecture → cap at 15% of expected effort. If you're still exploring after the timebox, present what you know and ask for direction — don't keep digging.
7. **Wait for approval before writing any code.** One approval unlocks the full scope.
8. Add Linear comment to each ticket summarising the agreed approach.

## Phase 3: Implementation

### Single-Ticket Mode
1. **Implement in vertical slices** — each increment delivers working functionality end-to-end. For features with UI + backend: schema/data → API route → UI wired to real data → verify. Never build all UI first and wire up later. For UI-only or backend-only work: one logical unit at a time, confirm before moving on.
2. **Use existing components** — check nearby imports before introducing anything new.
3. **Leverage coding plugins freely** — TDD, systematic-debugging, verification-before-completion, brainstorming, and other available plugins complement this workflow. Use them as the situation calls for — they handle coding discipline, these skills handle process structure.
4. **After each increment:**
   a. Run `npx tsc --noEmit` (or project equivalent) — fix type errors immediately.
   b. If UI change: list every screen/component that consumes what you changed. Verify each one.
   c. If styling change: confirm the styling system config is in place (NativeWind config, Tailwind content paths, theme tokens).
   d. Do NOT present the increment to me until a-c pass.
5. **Rules:** don't change things outside the ticket scope. When updating a component library, update ALL consuming screens. If unsure, ask. Enumerate what changed after each increment.
6. **When you hit an unexpected error or are investigating a bug:** STOP coding and investigate. Check actual error output, logs, data, and current state before attempting a fix or forming a hypothesis. Do not guess at root causes — read the evidence first. If logs are inaccessible, say so immediately. One minute of investigation saves ten minutes of wrong fixes. This applies to ALL investigation work, not just build errors.
   - **When a tool/command is permission-denied, hook-denied, or gate-blocked:** STOP after ONE retry — never loop. Immediately inspect the actual blocker (the hook script's exit behavior, a hung helper process, the classifier's stated reason) — evidence before hypothesis — then surface it to the user with exactly what to approve. Do not generate speculative explanations across repeated retries (observed: 8+ blind retries on a hook-blocked `git commit`). A blocked gate is a question for the user, not a problem to route around. The durable fix for a recurring block is a deterministic hook, not a retry loop.
7. **Parallelise independent work within a ticket.** If the ticket contains multiple independent tasks (e.g., an API route and a UI component that don't share state, or tests for separate modules), spin up sub-agents to work on them concurrently rather than sequentially. Each sub-agent follows the same rules: type-check after each increment, stay in scope, escalate after 3 failed attempts. The orchestrating agent resolves any conflicts before moving to Phase 4.

### Multi-Ticket Mode — Parallel Execution
**Sub-agents execute tickets concurrently. Each sub-agent follows these rules:**

1. Pick up their ticket(s) — read the full description and acceptance criteria.
2. Implement in small increments — one logical unit at a time.
3. Use existing components — check nearby imports before introducing anything new.
4. After each increment: run type checker, fix errors immediately.
5. Don't change things outside the ticket scope.
6. Run tests after implementation.
7. **If blocked after 3 attempts:** stop, add Linear comment documenting the blocker, report back.

**Sub-agent scoping rules:**
- **Bounded file scope:** give each sub-agent an explicit list of directories/files to examine. Don't let agents explore the whole codebase — scope them to what's relevant for their ticket.
- **Reads are parallel, writes are exclusive:** sub-agents can read overlapping files, but no two sub-agents should write to the same file. If file conflicts exist, serialize those tickets.
- **Use sub-agents for exploration, orchestrator for writes:** when a ticket needs codebase research before implementation, spawn a read-only sub-agent to analyse and report back, then implement in the main agent or a write-scoped sub-agent.
- **If you isolate parallel work in git worktrees:** a fresh worktree has no `node_modules` — run the project's install (`bun install` / `npm install`) before the quality gate, or type-check and tests fail on missing-module errors. Run the merge from the MAIN checkout, never from inside the worktree (`git checkout main` errors with "already used by worktree"). Reap the worktree when done so a stale session doesn't bite the next run.
- **Do NOT edit `CLAUDE.md` (or other shared top-level handoff files) inside a parallel worktree.** When siblings complete the same day, `CLAUDE.md` is the #1 merge-conflict collision point — every ticket editing the same paragraphs guarantees an abort → resolve → re-gate → redo round on each merge. Leave all handoff/`CLAUDE.md` updates to the single serialized `/session-end` in the main checkout after the branches land.
- **Fresh worktree branches have no upstream:** `git log @{upstream}..HEAD` errors with "no upstream configured" — use `git log main..HEAD` (or set `@{push}`) to inspect commits ahead of main.

**The orchestrating agent:**
- Monitors sub-agent progress
- Resolves cross-ticket conflicts (merge conflicts, shared file edits)
- Ensures all tickets complete before proceeding

## Phase 4: Quality Gate & Commit

After implementation is complete (all tickets in multi-ticket mode):

1. **Run full type check:** `npx tsc --noEmit` (or project equivalent) — must be clean.
2. **Run linter:** `npm run lint` — must pass.
3. **Run full test suite:** `npm test` — all must pass.
4. **Add/update tests for ALL new code** — follow existing patterns, cover happy path + edge cases. This is a hard gate: no commit advances to Phase 5 without tests for new logic. If a change is genuinely test-exempt (config, copy, types), state the reason in the commit body.
5. **Run full suite again** — all must pass.
6. **Self-review:** all acceptance criteria met per ticket, no unrelated changes, no debug code. Use verification-before-completion discipline — run all checks and confirm output before claiming "done".
7. **Commit to the feature branch:**
   - Single: `git add <specific files> && git commit -m "<type>(<ticket-id>): <description>"`
   - Multi-ticket: `git add <specific files> && git commit -m "<type>(<ticket-ids>): <description>"`
8. **Push to remote:** `git push` — keep the feature branch current after every commit.

**IMPORTANT:** Commit after quality gates, BEFORE UAT. This ensures work is saved and the remote is current even if UAT finds issues. UAT fixes get their own commits.

**If tests fail after 3 fix attempts:** STOP. Add Linear comment documenting failures. Update status → `Blocked`. Stash changes. Report to me.

## Phase 5: UAT

**Applies to:** any user-facing change (UI, features, behaviour, notifications).
**Skip for:** pure refactors, CI/CD, docs-only, dependency updates with passing tests. State why if skipping.

1. **Delegate to `/uat` Phase 2b interview mode.** Never present a flat checklist and ask the user to "report back" — always ask one `AskUserQuestion` at a time with contextual options that describe THIS test's likely outcomes (not generic Pass/Fail).
2. If app needs to be running, provide the exact command and what to check.
3. Wait for my confirmation on each item.
4. If issues found: follow `/uat` triage rules (bug vs feature vs docs gap).
5. **Fix bugs on the feature branch** — each fix gets its own commit: `fix(<ticket-id>): <description> — found during UAT`
6. **Push fixes to remote** after each commit.

## Phase 6: Close & Merge

Only after UAT passes (or is explicitly skipped):

1. **Code review:** For substantial changes (new features, architectural shifts, multi-file refactors), run code-review before merge. Minor fixes and single-file changes can skip this.
2. **Update Linear for each ticket:**
   - Status → `Done`
   - Closing comment: what was implemented, files changed, test coverage, follow-up items
3. **Report to me:** summary, branch name, commit hashes, any follow-up tickets needed.
4. **Wait for user instruction to merge.** Do NOT merge automatically.
5. **Run production build:** `npm run build` (or project equivalent) — must pass before merge. This catches framework-specific errors (SSR, route exports, bundle issues) that type-checking and tests miss.
6. **On merge instruction:** `git checkout main && git merge feat/<branch-name> --no-ff -m "merge: <branch-name> into main" && git push`
6. **If ending the session after this:** run `/session-end` to update CLAUDE.md handoff notes.

## Git Workflow Summary

```
main ─────────────────────────────────────────── merge ── push
  \                                              /
   feat/branch ── commit(quality gate) ── push ── fix(UAT) ── push
```

- Feature branch created and pushed immediately at pickup
- Commit + push after quality gate (Phase 4)
- UAT fixes committed + pushed individually (Phase 5)
- Merge to main + push only on user instruction (Phase 6)
- Remote is always current — no "14 unpushed commits" situations

## Key Principles

- **Research before code** — verify, don't guess
- **Use what exists** — existing frameworks, components, patterns
- **Incremental implementation** — small changes, verified often
- **Quality gates are mandatory** — type check + lint + tests after every meaningful change, no exceptions
- **Commit early, push often** — feature branch commits after quality gate, not after UAT
- **Audit trail on Linear** — comments at pickup, plan, and close
- **Rollback safety** — feature branches + stash on failure
- **Parallelise by default** — whenever independent tasks exist (within a ticket or across a multi-ticket batch), use sub-agents to work concurrently. Sequential is the fallback, not the default.
- **Escalate, don't block** — if stuck after 3 attempts, report back; don't spin
- **I stay in control** — confirm plan before coding, confirm UAT before closing
- **User controls merge** — never merge to main without explicit instruction
- **Conventional commits** — `<type>(<ticket-id>): <description>`
- **Feature branches** — `feat/<ticket-id>-<description>` (single) or `feat/sprint-N-<description>` (multi-ticket batch)
- **Sprint nomenclature is enforced** — `sprint-N` labels only; never `wave`, `slice`, `batch`, or any synonym in Linear or branch names. See `/requirements` for the full rules.
- **Plugins are complementary, not constrained** — these skills structure the process (when to pick up, plan, commit, test, merge). Coding plugins (TDD, debugging, brainstorming, frontend-design, code-review) handle how you code and should be used freely throughout. The skills don't gate or restrict plugin use — they encourage it.
