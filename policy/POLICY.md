# Policy

Persistent rules that load at the start of every session. Copy this into your AI coding tool's instruction file and adapt to your stack.

---

## Non-Negotiable Rules

### Use Configured Integrations
When a project management integration is configured (e.g., via plugin, extension, or API connection), ALWAYS use it. Never install CLI tools, npm packages, or call APIs directly as a workaround. If the integration isn't connecting, help debug the connection — don't switch approaches.

### Use What Exists
Always use existing UI components, design systems, and frameworks already in the project before introducing new ones. Check what's already imported and used in nearby files first.

### Research Before Code
Before proposing solutions involving API integrations, technical approaches, or architectural decisions — research the actual codebase implementation AND relevant documentation first. Don't guess. If integrating a new service, verify it works with the project's current stack before writing any code.

### Stay In-Stack
When debugging build failures, stay within the project's established build workflow. Don't fall back to alternative build approaches as a workaround. Check dependency version compatibility with the current framework version first.

### UI Change Completeness
When making UI changes, update ALL screens and components that consume the modified styles/components — not just the component library. After UI changes, enumerate which screens use the changed components and confirm each is updated.

### Don't Touch What I Didn't Ask
Never remove or change elements I haven't asked you to change. If you think something else should change, ask first.

## Skills

### Turning a vague idea into a buildable ticket → Requirements
Research feasibility first, then define scope with testable acceptance criteria and explicit out-of-scope boundaries. Creates the ticket that Sprint picks up.

### Starting work on a ticket → Sprint
Pre-flight check → ticket pickup → research & plan (with my approval) → incremental implementation → quality gate & commit → UAT → merge with ticket update. Supports single-ticket and batch modes.

### Bug or issue found during testing → UAT
Testing report first (what was verified, what can be tested, what's blocked). Then triage: classify as bug, new feature, or documentation gap. Get my confirmation before fixing. New features go to backlog — don't scope-creep a testing session.

### New UI work → Design-First
Audit existing components → wireframe with real components → get my approval → lock the design → implement against it. The wireframe is the source of truth.

### Building screens or flows for information-dense apps → UX Design
Apply the UX framework before writing code: map progressive disclosure layers, check context preservation, apply scannable structure, ensure multiple navigation paths. Use alongside Design-First when building new UI.

### Finishing a session or switching projects → Session End
Commit all work, push to remote, update handoff notes, update ticket status. Never end a session with uncommitted changes or stale documentation.

### Reviewing and improving these skills → Retro
Only when I invoke it. Reviews recent session friction against current skills and policy, proposes specific updates. I approve every change before anything is applied.

## Session Discipline

### Never Leave Work Unfinished
When a session is ending — whether the user says "that's it", "thanks", "I'm done", or the conversation is wrapping up:

1. **Check for uncommitted changes** — run `git status`. If there are uncommitted changes, commit them or stash them. Never leave dirty state.
2. **Check for unpushed commits** — if the branch has commits not pushed to remote, push them. Work that only exists locally is work at risk.
3. **Update documentation** — set Current Phase, Known Issues, and Last Session sections to reflect the current state. This is the handoff note for the next session.
4. **Update tickets** — if a ticket was being worked on, add a closing comment and set the correct status.

If you cannot complete a feature in the current session, commit what you have with a `wip(<ticket-id>): <description>` message. WIP commits are fine. Uncommitted work is not.

## Manual Setup Documentation

When a project requires manual setup (cloud providers, API keys, OAuth, third-party services):

1. **One document per project** — create a `SETUP.md` in the project root. All setup instructions live here, nowhere else. Keep it updated.
2. **Write it plainly** — no assumed knowledge. Every click, every command, every screen. If someone has never seen the service console before, they should still be able to follow it.
3. **Step-by-step, numbered** — not paragraphs. Each action is its own numbered step with the expected outcome.
4. **`.env.example` with placeholders** — every project must have a `.env.example` committed to git with placeholder values so code reviews, CI, and tests can proceed without real credentials.
5. **Separate one-time from recurring** — clearly mark which steps are "do once when setting up" vs "do every time you pull" vs "do when deploying".

## Quality Gates
- Run the project's type checker after every meaningful change
- Run the project's test suite before any commit
- Conventional commits: `<type>(<ticket-id>): <description>`
- Feature branches: `feat/<ticket-id>-<short-description>`

## Project Management Audit Trail
When working on tickets, leave comments at: pickup, after plan approval, and at close with a summary of what was done.
