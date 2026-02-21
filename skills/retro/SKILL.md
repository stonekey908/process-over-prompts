# Retrospective

Review recent session performance against current skills and policy, identify friction patterns, and propose specific updates. Only runs when manually invoked. Proposes changes — never applies them without explicit approval.

---

## Phase 1: Gather Evidence

1. **Identify what to review.** Ask the user:
   - Specific sessions or a time range?
   - A particular project or all projects?
   - Any specific friction they've noticed?

2. **Read the current governance stack:**
   - Policy file (global and project-level)
   - All skill documents
   - Automation config (hooks, git hooks)

3. **If session data exists** (reports, logs, insights), read it and extract:
   - Top friction types and counts
   - Satisfaction patterns
   - Recurring failure modes
   - Tool errors

4. **If no data exists**, ask the user to describe:
   - What kept going wrong?
   - What worked well?
   - Any patterns across sessions?

## Phase 2: Analyse Gaps

Compare evidence against the current governance stack. For each friction pattern, classify it:

### Already Addressed
- A rule or skill step exists that should have prevented this
- **Question:** Is the rule unclear? Being ignored? Needs strengthening?

### Not Addressed
- No rule or skill step covers this friction
- **Question:** Should this become a policy rule, a new skill step, a new hook, or is it an edge case?

### Partially Addressed
- A related rule exists but doesn't fully cover the case
- **Question:** Expand the existing rule or add a new one alongside it?

**Present the analysis as a table:**

| Friction Pattern | Count/Severity | Current Coverage | Gap Type | Proposed Fix |
|-----------------|---------------|-----------------|----------|-------------|

## Phase 3: Propose Changes

For each gap, draft the specific change. Group by target:

### Policy Changes
- New rules (with exact wording)
- Rules to modify (before → after)
- Rules to remove if no longer relevant

### Skill Changes
- New steps in existing skills (which skill, which phase, where)
- Steps to modify (before → after)
- New skills to create (rare — only if a whole new workflow is needed)

### Automation Changes
- New hooks or git checks to add
- Existing automation to modify
- Automation to remove if causing friction

### Out of Scope
- Tooling/environment friction (integration bugs, dependency issues) — can't be fixed by governance
- Model capability issues — note but don't try to process-engineer around
- One-off issues not worth codifying

**For each change, state:** what friction it addresses, why current setup doesn't cover it, any risk the change introduces.

## Phase 4: Review and Apply

**Present ALL changes to the user. Apply nothing until explicitly approved.**

1. Walk through each — user may approve, modify, or reject individually
2. Apply approved changes to the relevant files
3. Confirm revised wording before applying modifications
4. Note rejection reasons (useful for future retros)

**After applying:**
- Show summary of what changed and which files were modified
- Commit: `git commit -m "chore: update governance stack from retro"`
- Note any changes that need testing in the next session

## Key Principles

- **Evidence first** — every change must trace to observed friction, not theory
- **You decide** — this skill proposes, you approve. Nothing is auto-applied.
- **Minimal changes** — prefer tightening existing rules over adding new ones. Governance bloat is real.
- **Don't over-engineer** — one occurrence is an anecdote, five is a pattern worth addressing
- **Remove as well as add** — if a rule causes friction or is outdated, propose removing it
- **Track what you changed** — commit messages create a changelog of your governance evolution
