# Sprint

Execute a complete agile sprint cycle on one or more tickets — from pickup to production-ready commit. Supports single-ticket mode (default) and batch mode (multiple related tickets worked in parallel). Validates environment, researches before coding, implements with quality gates, maintains an audit trail, and commits clean work on a feature branch.

---

## Phase 0: Pre-Flight (DO NOT SKIP)

1. **Verify project management connectivity** — attempt to list projects or fetch a known ticket via your PM integration. If it fails: STOP. Tell me to check the connection. NEVER attempt workarounds.
2. **Verify project context** — confirm correct directory, correct stack, policy file loaded.
3. **Verify git state** — `git status`, confirm clean tree, confirm on main/default branch and up to date.
4. **Identify scope** — single ticket or batch? If batch: which tickets, their dependencies, any ordering constraints.

If any check fails, stop and report. Do not proceed.

## Phase 1: Ticket Pickup

### Single-Ticket Mode
1. Fetch the ticket from your project management tool — read title, description, acceptance criteria, labels, priority, blocking dependencies.
2. Update ticket status → `In Progress`
3. Add a ticket comment: "Starting work. Will update with approach before implementation."
4. Create feature branch: `git checkout -b feat/<ticket-id>-<short-description>`
5. **Push immediately:** `git push -u origin feat/<ticket-id>-<short-description>` — remote tracking from the start. Work that only exists locally is work at risk.

### Batch Mode
1. Fetch all tickets in the batch — read titles, descriptions, acceptance criteria, blocking dependencies.
2. Create a single feature branch for the batch: `git checkout -b feat/<batch-name>`
3. **Push immediately:** `git push -u origin feat/<batch-name>`
4. Update all ticket statuses → `In Progress`
5. Add pickup comment to each ticket noting the batch and sibling tickets.
6. Present the batch plan — which tickets, which can run in parallel, which are sequential. **Wait for approval before proceeding.**

## Phase 2: Research & Plan (BEFORE ANY CODE)

1. **Read the relevant codebase** — identify files, components, modules involved. Check existing patterns, imports, dependencies.
2. **If integrating a new API/service** — search official docs, verify compatibility with the current stack, check for known issues.
3. **Present a brief plan:** files that will change, approach, dependencies needed, risks.
   - In batch mode: group by ticket, identify shared files, flag potential conflicts.
4. **Wait for approval before writing any code.** One approval unlocks the full scope.
5. Add a ticket comment summarising the agreed approach.

## Phase 3: Implementation

1. **Implement in small increments** — one logical unit at a time. For UI: one screen at a time, confirm visually before moving on.
2. **Use existing components** — check nearby imports before introducing anything new.
3. **After each increment:** run the project's type checker, fix errors immediately.
4. **Rules:** don't change things outside the ticket scope. When updating a component library, update ALL consuming screens. If unsure, ask. Enumerate what changed after each increment.
5. **If blocked after 3 attempts:** STOP. Add ticket comment documenting the blocker. Report back.

## Phase 4: Quality Gate & Commit

After implementation is complete:

1. **Run full type check** — must be clean.
2. **Run linter** — must pass.
3. **Run full test suite** — all must pass.
4. **Add/update tests** for changes made — cover happy path + edge cases.
5. **Run full suite again** — all must pass.
6. **Self-review:** all acceptance criteria met, no unrelated changes, no debug code.
7. **Commit to the feature branch:** `git add <specific files> && git commit -m "<type>(<ticket-id>): <description>"`
8. **Push to remote:** `git push`

**IMPORTANT:** Commit after quality gates pass, BEFORE UAT. This ensures work is saved and the remote is current even if UAT surfaces issues. UAT fixes get their own commits.

**If tests fail after 3 fix attempts:** STOP. Add ticket comment documenting failures. Update status → `Blocked`. Stash changes. Report to me.

## Phase 5: UAT

**Applies to:** any user-facing change (UI, features, behaviour, notifications).
**Skip for:** pure refactors, CI/CD, docs-only, dependency updates with passing tests. State why if skipping.

1. Present a UAT checklist — each acceptance criterion mapped to a specific verification action.
2. If the app needs to be running, provide the exact command and what to check.
3. Wait for my confirmation on each item.
4. If issues found: classify using the UAT & Triage skill rules (bug vs feature vs docs gap).
5. **Fix bugs on the feature branch** — each fix gets its own commit.
6. **Push fixes to remote** after each commit.

## Phase 6: Close & Merge

Only after UAT passes (or is explicitly skipped):

1. **Update each ticket:** status → `Done`, closing comment with: what was implemented, files changed, test coverage, follow-up items.
2. **Report to me:** summary, branch name, commit hashes, any follow-up tickets needed.
3. **Wait for instruction to merge.** Do NOT merge automatically.
4. **On merge instruction:** `git checkout main && git merge feat/<branch> --no-ff && git push`

## Git Workflow

```
main ─────────────────────────────────────────── merge ── push
  \                                              /
   feat/branch ── commit(quality gate) ── push ── fix(UAT) ── push
```

- Feature branch created and pushed immediately at pickup
- Commit + push after quality gate (Phase 4) — before UAT
- UAT fixes committed + pushed individually (Phase 5)
- Merge to main only on user instruction (Phase 6)

## Key Principles

- **Research before code** — verify, don't guess
- **Use what exists** — existing frameworks, components, patterns
- **Incremental implementation** — small changes, verified often
- **Quality gates are mandatory** — type check + lint + tests, no exceptions
- **Commit early, push often** — commit after quality gate, not after UAT
- **Audit trail** — comments at pickup, plan, and close
- **Rollback safety** — feature branches + stash on failure
- **Escalate, don't block** — if stuck after 3 attempts, report back
- **I stay in control** — confirm plan before coding, confirm UAT before closing
- **User controls merge** — never merge to main without explicit instruction
