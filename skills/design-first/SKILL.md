---
name: design-first
description: Design and build features using vertical slices — core functionality first (UI + API + data working together), then broaden. Prevents the frontend-first trap where a polished UI gets built before the backend exists, leading to costly rewrites. Use when starting new screens, features, or UI overhauls.
---

# Design-First Skill

## Philosophy: Vertical Slices, Not Horizontal Layers

**The old way (frontend-first):** Wireframe all screens → lock the design → build all the backend → discover the data model doesn't fit → rewrite.

**The better way (vertical slices):** Identify the core user journey → design the UI AND data model together → build ONE thin slice through the entire stack (UI + API + data) → prove it works → broaden outward in slices.

Each slice delivers working frontend AND backend. You never have a beautiful UI with no backend, or a backend with no UI to test it through.

## Phase 1: Audit What Exists

1. **Inventory the design system** — which component library, shared components, theming/tokens, navigation patterns.
2. **Document the component palette** — available components with variants, custom components, gaps that need filling.
3. **Check existing screen patterns** — list rendering, form structure, loading/empty/error states, spacing/layout approach.
4. **Verify styling infrastructure** — confirm the styling system is correctly configured:
   - NativeWind: `tailwind.config.js` content paths include all relevant directories
   - Theme tokens: dark/light mode variants exist and are wired up
   - Fonts: custom fonts are loaded (e.g., in `app.json` or layout file)
   - If anything is missing or misconfigured, flag it BEFORE designing — not after implementation fails.
5. **Check existing backend patterns** — what data layer (Supabase, Firebase, API routes)? What auth? What existing schemas/tables? What patterns do existing API routes follow?

**Output:** A brief component inventory + backend/data layer summary shared with me. This is the palette for design.

## Phase 2: Core Flow Design

1. **Identify the core user journey** — the ONE critical path that defines the feature. Not every screen, not every edge case — the single most important thing the user does. Ask me if unclear.
2. **Wireframe the core flow only** (3-5 screens max) — real components, hardcoded mock data, navigation between them. Apply `/ux-design` principles to this flow (progressive disclosure layers, context preservation).
3. **Apply frontend-design for visual quality** — use the frontend-design skill for distinctive aesthetics and production-grade polish. Don't settle for generic.
4. **Sketch the data model alongside the wireframe:**
   - What tables/collections are needed?
   - What are the key fields and relationships?
   - What API endpoints will the UI call?
   - What does the request/response shape look like?
5. **Present both together** — the wireframe AND the data model/API sketch. These must make sense as a pair. If the UI shows data the API can't efficiently provide, or the API returns shapes that don't map to the UI, catch it now — not after implementation.
6. **Get approval** before proceeding.

## Phase 3: Vertical Slice — Core Flow End-to-End

Build the core flow as ONE working slice through the entire stack:

0. **Mockup is the source of truth.** Open the locked wireframe/mockup before writing any JSX. For each screen built in this slice:
   - Reference the mockup section by name in the implementation plan.
   - If the mockup is ambiguous, ASK — do not invent.
   - If your implementation diverges from the mockup mid-build (proportions, layout, copy, components used), STOP and flag the deviation.
   - "Close enough" is not close enough. Match it.
1. **Database/schema first** — create tables, migrations, types. Run migrations, verify schema.
2. **API routes next** — implement the endpoints the UI needs. Follow existing route patterns. Include basic validation and error handling.
3. **Wire UI to real data** — replace mock data with actual API calls. Keep the wireframe layout. If real data doesn't fit the wireframe, STOP and discuss — don't silently reshape.
4. **Prove it works** — the core journey should be testable end-to-end with real data flowing through.
5. **After each layer:** `npx tsc --noEmit`, `npm test`, confirm with me before moving to the next.
6. **Commit the working slice:** `git commit -m "feat(<ticket-id>): core flow working end-to-end"`

**Key rule:** Do NOT move to Phase 4 until the core flow works end-to-end. A working thin slice is worth more than a beautiful prototype with no backend.

## Phase 4: Broaden

Now add remaining screens, features, and edge cases — each as a vertical slice:

1. **Pick the next most important flow** — ask me if priority is unclear.
2. **For each new slice:**
   a. Wireframe the screens (using existing components). Apply `/ux-design` principles.
   b. Add any needed schema changes / API endpoints.
   c. Wire UI to real data.
   d. Verify end-to-end.
   e. Type check + tests.
3. **After each slice:** visual check, confirm with me before the next slice.
4. **If design needs to change based on what you learn:** explain why, get my approval, update the affected screens.

## Phase 5: Completion Checklist

- [ ] Core flow works end-to-end with real data
- [ ] All screens implemented as vertical slices (UI + API + data)
- [ ] No new components introduced without approval
- [ ] Existing component library used — no duplicate patterns
- [ ] Navigation works across all flows
- [ ] Loading, empty, error states implemented
- [ ] Dark mode works if supported — no hardcoded colours, all from theme tokens
- [ ] TypeScript typecheck passes
- [ ] All tests pass

## Key Principles

- **Vertical slices, not horizontal layers** — every increment delivers working frontend + backend
- **Core flow first** — prove the most important journey works before broadening
- **Data model alongside design** — catch frontend/backend mismatches before code is written
- **Use what exists** — the component inventory is your palette, not npm
- **One slice at a time** — verify each slice works before starting the next
- **Flag don't fix** — if design needs changing during implementation, discuss it
- **Pair with frontend-design and ux-design** — design-first handles the process and vertical slice ordering. frontend-design handles visual quality. ux-design handles information architecture and user navigation. Apply UX principles to each slice as you build it, not all upfront.
