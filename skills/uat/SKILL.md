---
name: uat
description: User acceptance testing with triage. Classifies findings as bugs, new features, or docs gaps. Fixes bugs with regression tests, sends features to backlog. Use after implementation or when issues need classifying.
---

# UAT & Triage Skill

## Phase 1: Setup

1. **Confirm what's being tested** — which ticket(s), what acceptance criteria, what screens/flows to verify.
2. **Present a structured UAT checklist:**
   - Each acceptance criterion mapped to a specific verification action
   - Edge cases worth checking (empty states, error states, offline)
   - Regression areas — screens/flows that weren't changed but could be affected
3. The user walks through the app and reports findings.

## Phase 2: Testing Report (MANDATORY)

After running automated checks, present a **Testing Report** with three clear sections:

### 2a. Static Verification (what was tested without running the app)

List everything verified through code analysis:
- Type checking (`tsc --noEmit` or project equivalent) — pass/fail
- Linting — pass/fail with any issues found
- Code review of acceptance criteria — verified by reading code
- Security/constraint review — verified against CLAUDE.md rules
- Schema/type alignment — verified types match data layer
- Theme/dark mode audit — verify no hardcoded colours outside theme tokens, check both light and dark mode rendering, confirm theme context values (radius, spacing, font size) propagate to affected components
- Production build (`npm run build` or equivalent) — pass/fail. Catches SSR, route export, and bundle errors that type-checking misses.

### 2b. Functional Testing — Interview Mode (MANDATORY — never a flat checklist)

**STOP. Before drafting anything in Phase 2b, answer this to yourself: "Is my next message going to be an `AskUserQuestion` call?" If no, you are violating the skill — convert it now.**

Interview mode is non-negotiable for every functional test in this phase. One `AskUserQuestion` per turn, with test-specific options that describe what the user will actually see for THIS test. No exceptions for "quick checks", "obvious tests", "the user already knows the app", or "I'll just list these few". If you catch yourself drafting a bulleted to-do list for the user, you've already slipped — stop the draft and turn the first item into an `AskUserQuestion`.

**Red Flags — STOP and Switch to Interview Mode**

| Thought | Reality |
|---|---|
| "Just give the user the list to test" | No. Use AskUserQuestion, one test at a time. |
| "Pass/Fail is enough for the options" | No. Each option must describe what the user actually sees. |
| "I'll batch a few questions together" | No. One question per turn. |
| "This test is too simple to need an interview" | No. Simple tests still go through AskUserQuestion. |
| "The user said 'continue' so I can run the rest as a list" | No. 'Continue' means the next question, not the next batch. |
| "I'll summarise remaining tests and let them report back" | No. That IS a flat checklist. Ask the next question. |
| "I already know the answer — I'll just note it as passed" | No. The user answers, not you. Ask. |

**Present each test as an interactive interview question using `AskUserQuestion`.** This is the default for all functional testing — do not dump a checklist and ask the user to report back.

**How it works:**

1. Compile the full list of test items from acceptance criteria, edge cases, and regression areas.
2. **Ask the user if they're ready to start the interview.** Provide the total question count so they know the scope.
3. Present each test **one at a time** using `AskUserQuestion` with **test-specific options that describe concrete outcomes for that particular test.** Do NOT use generic Pass/Fail labels — write options that describe what the user will actually see.
   - **Options must be contextual:** each test gets 2-4 options describing the realistic outcomes for that specific flow. One option is the happy path, the others describe the most likely failure modes for that feature.
   - **The user always has a free-format "Other" option** (provided automatically by `AskUserQuestion`) for anything the predefined options don't cover.
   - Think about what could go wrong for THIS test and make those the options.
4. For each test question, include in the option descriptions:
   - **What to do**: step-by-step instructions to perform the test
   - **What to look for**: what each outcome looks like in practice
   - **Known limitations**: what's mocked or stubbed
5. If the user selects a failure/partial option or writes free-text, follow up with another `AskUserQuestion` if you need more detail to triage.
6. **Track all answers as you go** — maintain a running tally. **Every question must include the tally in its text**, e.g., "Test 4/12 — 2 pass, 1 fail, 0 skip so far". The user should always know where they are and what the running score is without asking.
7. **Auto-save progress every 3 questions.** After every 3rd completed answer, write the current state to the project's CLAUDE.md `## Paused UAT Interview` section (same format as pause — see below). This is a **checkpoint save**, not a pause — continue asking the next question immediately after saving. This protects against session crashes, context window limits, or unexpected disconnections. The user doesn't need to be told about checkpoint saves — just do them silently.
8. **Context window protection.** If the conversation is getting long (system compression is happening, or you've been running for many turns), proactively save the full UAT state to CLAUDE.md before continuing. Better to save too often than to lose progress.
   - **After every 10 completed questions:** write a cumulative progress summary to CLAUDE.md (not just a checkpoint — include all results so far, running tallies, and any issues found). This acts as a full restore point if the session needs to continue in a new conversation.
   - **If context window is approaching limits:** proactively offer to pause and resume in a new session rather than rushing through remaining tests with degraded quality. Say: "We're approaching context limits — want to pause and resume fresh, or push through the remaining N tests?"
9. After all questions: compile results into a **UAT Results Summary** showing pass/fail/partial/skip counts and listing every item with its result and any user notes.

**Example interview questions:**

Test for a dashboard screen:
```
Question: "Test 1/8 — 0 pass, 0 fail: Open the dashboard — does the document list load?"
Header: "UAT"
Options:
  - "All documents visible with correct titles and statuses"
    → Run `npm run dev`, navigate to /dashboard. You should see your uploaded documents listed.
  - "Dashboard loads but the list is empty or documents are missing"
    → The page renders but the table/list has no rows or is missing some expected entries.
  - "Dashboard shows an error or blank screen"
    → The page fails to load entirely — white screen, error message, or spinner that never resolves.
  - "Can't test — app won't start or page won't load"
    → Something is blocking you from even reaching this screen.
```

Test for a form submission:
```
Question: "Test 4/8 — 2 pass, 1 fail: Submit the upload form with a valid PDF"
Header: "UAT"
Options:
  - "Upload completes, file appears in list with 'extracting' status"
    → Click Upload, select a PDF under 10MB. Progress bar should appear, then the file shows in the document list.
  - "Upload appears to work but file doesn't appear in the list"
    → No error shown, but the document list doesn't update after upload.
  - "Upload fails with an error message"
    → An error toast, modal, or inline error appears during or after upload.
  - "Upload button is disabled or form won't submit"
    → You can't even trigger the upload action.
```

**Key rule:** Never reuse the same set of options across different tests. Each test's options should reflect what could specifically go right or wrong for THAT feature.

**If the user needs to pause** (says "I need to go", "let's stop here", "pause", etc.):
- Acknowledge immediately — don't try to squeeze in one more question.
- Record the current state: which questions were completed, what the answers were, which questions remain.
- Write the full state to the project's CLAUDE.md `## Paused UAT Interview` section (same format as the auto-save checkpoints, but this time tell the user).
- Tell the user: "UAT progress saved — you can resume with `/session-start` next time."
- Note: if auto-save checkpoints have been running (step 7 above), the last checkpoint means at most 2 answers could be lost on a crash. On explicit pause, save is always exact.

### 2c. Cannot Test Yet (blocked by external dependencies)

For each untestable area, explain:
- **What**: The feature/flow that can't be tested
- **Why**: The missing prerequisite (e.g., "Firebase project not created", "API key not configured")
- **When**: What needs to happen before it can be tested
- **Workaround**: Any dev-mode bypass that was added

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
- **Action:** Create NEW Linear ticket with description, why it surfaced, priority suggestion, label `discovered-in-uat`. Do NOT implement during this session.

### Documentation Gap
- Feature works but isn't explained well, or help text is missing/misleading
- **Action:** Create docs/UX ticket OR add to current ticket scope if minor.

**Present the classification to me and get confirmation before proceeding.**

## Phase 4: Fix Bugs Only

For items triaged as bugs:

1. Reopen or update the Linear ticket with bug details.
2. **Investigate before fixing** — use systematic-debugging: reproduce the issue, identify the root cause, understand why it happened, then fix. Don't patch symptoms.
3. Implement the fix — targeted change, minimal scope.
4. Run quality gates: type checker and test suite must pass.
5. Regression test: re-verify original acceptance criteria AND related screens. If bug was in a shared component, check ALL consumers.
6. **Verify the fix** — run verification-before-completion: confirm the fix actually resolves the issue with evidence, not assumptions. Then present for re-testing.

For items triaged as new features: the ticket is created, it goes to backlog, it gets prioritised. Do NOT implement.

## Phase 5: Commit & Document

Only when I confirm all fixes pass:

1. Add/update unit tests covering the bugs found — every fix gets a regression test.
2. Update relevant docs (README, inline comments, component docs, CHANGELOG if applicable).
3. Commit: `fix(<ticket-id>): <what was fixed> — found during UAT of <original-ticket>`
4. Push to remote immediately after commit.
5. Update Linear: bug tickets → Done with summary, original ticket → comment with UAT results, new feature tickets → remain in backlog.

## Key Principles

- **Triage before you fix** — not everything found in testing is a bug
- **New features go to backlog** — no scope creep during testing
- **Regression test everything** — the fix for bug A must not create bug B
- **Always provide a testing report** — never leave the user guessing what they can verify
- **I decide** — classification, priority, and "done" are product decisions
- **Use available plugins freely** — systematic-debugging for root cause investigation, verification-before-completion before claiming a fix works. These complement the triage process, not replace it.
