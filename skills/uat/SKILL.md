# UAT & Triage

Run user acceptance testing on completed work, triage findings as bugs or new features, implement fixes with regression testing, and update documentation. Use after implementation is complete or when issues are reported that need classifying before fixing.

---

## Phase 1: Setup

1. **Confirm what's being tested** — which ticket(s), what acceptance criteria, what screens/flows to verify.
2. **Present a structured UAT checklist:**
   - Each acceptance criterion mapped to a specific action
   - Edge cases worth checking (empty states, error states, offline)
   - Regression areas — screens/flows that weren't changed but could be affected
3. The user walks through the app and reports findings.

## Phase 2: Testing Report (MANDATORY)

After running automated checks, present a **Testing Report** with three clear sections. This ensures the user knows exactly what was verified, what they can test, and what's blocked.

### 2a. Static Verification (tested without running the app)

List everything verified through code analysis:
- Type checking — pass/fail
- Linting — pass/fail with any issues found
- Code review against acceptance criteria — verified by reading code
- Constraint review — verified against project rules and policies

### 2b. Functional Testing (what the user CAN test right now)

For each testable flow, provide step-by-step instructions:
- **What to do**: exact commands and actions
- **What to look for**: expected visual/behavioural outcome
- **Known limitations**: what's mocked, stubbed, or using placeholder data

### 2c. Cannot Test Yet (blocked by external dependencies)

For each untestable area, explain:
- **What**: the feature/flow
- **Why**: the missing prerequisite
- **When**: what needs to happen before it can be tested

**Always provide this report.** Never leave the user guessing what they can verify and what they can't.

## Phase 3: Triage (THE CRITICAL STEP)

When an issue is reported, **do not jump to fixing it.** Classify it first:

### Bug
- Feature doesn't match acceptance criteria
- Something previously working is now broken (regression)
- Crash, error, or clearly wrong behaviour
- **Action:** Reopen original ticket OR create bug ticket linked to it. Add description of expected vs actual behaviour.

### New Feature
- Feature works as specified but could be better
- "It would be nice if..." or "I expected it to also..."
- A UX gap not covered in the original ticket
- **Action:** Create a NEW ticket with description, why it surfaced, priority suggestion, label `discovered-in-uat`. Do NOT implement during this session.

### Documentation Gap
- Feature works but isn't explained well, or help text is missing/misleading
- **Action:** Create docs/UX ticket OR add to current ticket scope if minor.

**Present the classification and get confirmation before proceeding.**

## Phase 4: Fix Bugs Only

For items triaged as bugs:

1. Reopen or update the ticket with bug details.
2. Implement the fix — targeted change, minimal scope.
3. Run quality gates: typecheck and tests.
4. Regression test: re-verify original acceptance criteria AND related screens. If bug was in a shared component, check ALL consumers.
5. Present the fix for re-testing.

For items triaged as new features: the ticket is created, it goes to backlog, it gets prioritised. Do NOT implement.

## Phase 5: Commit & Document

Only when all fixes are confirmed passing:

1. Add/update unit tests covering the bugs found — every fix gets a regression test.
2. Update relevant docs (README, inline comments, component docs, CHANGELOG if applicable).
3. Commit: `fix(<ticket-id>): <what was fixed> — found during UAT of <original-ticket>`
4. Push to remote immediately after commit.
5. Update tickets: bug tickets → Done with summary, original ticket → comment with UAT results, new feature tickets → remain in backlog.

## Key Principles

- **Triage before you fix** — not everything found in testing is a bug
- **New features go to backlog** — no scope creep during testing
- **Regression test everything** — the fix for bug A must not create bug B
- **Always provide a testing report** — never leave the user guessing what they can verify
- **The user decides** — classification, priority, and "done" are product decisions
