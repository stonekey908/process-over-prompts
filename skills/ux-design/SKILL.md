# UX Design

Design intuitive user experiences for information-dense applications. Use when building screens, flows, navigation, or interactions where users must find, follow, and act on complex structured information without losing context.

---

## Core Philosophy: Nothing Hidden, Nothing Overwhelming

The central tension in information-dense apps: **all the information matters, but showing it all at once destroys usability.** The solution is never to hide information — it's to create a clear hierarchy so users can drill from overview to detail on their own terms.

Think of it like a building: lobby has a directory, each floor has a corridor, each corridor has doors. Everything is accessible. Nothing is hidden. But you're never standing in every room at once.

**GOLDEN RULE**: If a user has to ask "where did that go?" or "how do I get back?", the UX has failed.

## The Five UX Principles

Apply these in order when designing any screen or flow.

### 1. Progressive Disclosure (Show Depth, Not Width)

Never flatten complex information into one scrollable page. Layer it:

- **Layer 0 — Glanceable**: What is this? Is it relevant? (title, status, key metric). Visible without any interaction.
- **Layer 1 — Scannable**: Key content the user came for. Requires exactly ONE interaction (tap card, expand section, select tab).
- **Layer 2 — Full depth**: Everything else (history, cross-references, metadata, config). Reachable but never forced.

**Rules:**
- Transitions between layers must be animated and reversible
- Use expand/collapse with clear affordances (chevrons that rotate, section headers that highlight)
- NEVER use "Read more" as the only indicator — hint at what's underneath ("3 sub-items", "5 issues found")

**Before coding any screen, map this table:**

| Screen | Layer 0 (glance) | Layer 1 (one tap) | Layer 2 (drill deep) |
|--------|------------------|-------------------|----------------------|

If Layer 0 has more than 5-6 items, you're showing too much. If Layer 2 is empty, the screen isn't complex enough for this framework.

### 2. Persistent Context (Never Lose the Thread)

Users are almost always mid-task. If the app loses their place, they lose trust.

**Navigation:** Breadcrumbs mandatory on any screen more than one level deep. Sticky headers on scroll. Explicit back navigation (never rely solely on system gestures). Active state indicators in nav.

**State preservation:** Tab state, scroll position, filter state, and selection state must ALL persist across navigation. If the user switches views and returns, everything should be exactly as they left it.

**Cross-references:** Open references in overlays or slide-out panels — NOT full navigation. User reads, dismisses, returns to where they were. Provide "Open Full View" for those who want to navigate fully.

**Background processes:** Progress must remain visible even if the user navigates away. Minimisable to a notification/badge, restorable with full state.

### 3. Scannable Structure (Design for F-Pattern Reading)

Users aren't reading — they're scanning for the flag, the gap, the exception.

**Consistent card anatomy** (every card in the app follows this):
```
[Status indicator / colour]  [Category badge]
[Primary title — largest text]
[Secondary identifier — reference, ID, subtitle]
[Metadata row — date, count, score, type]
```

**Colour-coded status system:** Define colours ONCE, use EVERYWHERE. Green = good/complete, Amber = warning/review, Red = critical/error, Blue = informational, Grey = inactive. ALWAYS pair colour with text label or icon (accessibility).

**Numbers:** Use tabular/monospace figures for scores, percentages, counts. Every number should be clickable to reveal what's behind it. Never show an aggregate without a path to the detail.

**Section headers:** Descriptive, searchable labels ("Overdue Tasks by Priority" not "Section 3").

### 4. Forgiving Navigation (Multiple Paths to Everything)

Different users navigate differently. Never force a single path.

**Search:** Accessible from every screen (persistent or via keyboard shortcut). Intelligent (natural language, exact titles, IDs, partials). Results grouped by type with match highlighted.

**Browse:** Category/section browsing coexists with search — both first-class. Nav structure visible, not behind hamburger menus.

**Recents and favourites:** Recently viewed items prominently accessible (last 5-10). Users can pin/bookmark, accessible in ≤2 interactions from anywhere.

**Deep links:** Every significant item has a shareable URL that opens directly to it.

**Cross-view jumps:** Always provide "← Back to [origin]" after jumping between views.

### 5. Zero-Surprise Interactions

Every interaction should produce exactly the result the user predicted.

**Click behaviours:** Tapping a card opens it (always). Tapping a metric shows what's behind it. Tapping a cross-reference opens in context (overlay). Swipe actions must be discoverable AND reversible.

**Actions:** Primary actions visually prominent and labelled (not icon-only). Destructive actions require confirmation. Non-destructive actions are instant. After significant actions, show confirmation toast with undo.

**Loading:** Never blank screens. Skeleton screens matching the exact layout. Specific messages after 1 second ("Loading customer records..."). Stream progress for long operations.

**Empty states:** Suggest alternatives on empty search. Explain why and what to do when a section is empty. Never blank white space.

**Errors:** Specific messages with recovery paths. Preserve successful work in multi-step failures.

## Common Layout Patterns

### Master-Detail
List on left (fixed, filterable), detail on right (flexible). Selecting loads detail instantly. Both scroll independently.

### Multi-Panel Workspace
Sidebar nav (always visible) + navigation panel (collapsible) + main content (flexible) + context panel (on-demand). Floating elements slide over, never push layout.

### Tabbed Dashboard
Summary metrics (clickable → drill into items) + visualisations (clickable elements) + detail sections. Tabs persist scroll position. Drill-downs expand inline, not new pages.

### Card Grid / Directory
Sticky search and filters at top. Standard card anatomy. Entire card is click target. Grid responds to screen width.

## Processing and Upload Flows

- Multi-stage progress with specific real-time messages, not vague spinners
- Expandable processing log with timestamps
- Minimisable — user can continue using the app while processing runs
- On failure, preserve what succeeded
- On completion, show reconciliation summary

## The "4-Minute User" Test

Before shipping any screen:

1. Can they find it in under 15 seconds?
2. Can they understand it without reading a help doc?
3. Can they take action without asking how?
4. Do they ever lose their place?
5. Can they do all of this on their first visit?

If any answer is no, redesign.

## Accessibility Non-Negotiables

- All colour-coded statuses must also have text labels/icons
- Touch targets: minimum 44x44px on mobile
- Text must be resizable — no fixed pixel sizes for body text
- Screen reader labels on all interactive elements
- Keyboard navigation for the full app
- Visible focus indicators on all interactive elements

## How to Use This Skill

1. Map progressive disclosure layers (Layer 0/1/2 table) before writing code
2. Check context preservation — where am I, how did I get here, how do I get back?
3. Apply scannable structure — important info top-left, statuses colour-coded, cards follow anatomy, numbers clickable
4. Ensure multiple navigation paths — search, browse, recents, deep link, cross-references
5. Verify zero-surprise interactions — every tap does what the user expects
6. Run the "4-Minute User" test
