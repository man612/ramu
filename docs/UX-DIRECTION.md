# UX direction — Ramu website redesign

Status: implementation contract for issue #51. This document defines the direction to implement; it is not a visual mockup and does not change pack/runtime behavior by itself.

## Product goal

Ramu should feel like a small, deliberate learning tool: calm, clear, precise, and useful before it tries to look impressive.

The redesign must reduce decorative noise while making the actual product easier to understand and use. It should not imitate a generic AI landing page, SaaS dashboard template, or component-library demo.

The core idea stays unchanged: one course, one ChatGPT Project, with sources, instructions, context, materials, and assessment kept organized over time.

## Research references

The direction below borrows principles, not dependencies or a copied visual identity.

- shadcn/ui: open-code composition and strong defaults; recent Sera/Rhea directions show that typography, geometry, spacing, and density matter more than adding more decoration. <https://ui.shadcn.com/docs>
- Kumo UI: semantic color tokens, hairline surfaces, compact product density, resource-list patterns, accessible navigation, and disciplined typography. <https://kumo-ui.com/> and <https://kumo-ui.com/skill/>
- Vercel Web Interface Guidelines: keyboard-first flows, visible focus, target sizes, state design, and restrained interaction feedback. <https://vercel.com/design/guidelines>
- GitHub Primer: responsive layout, color, typography, and component foundations as one coherent system. <https://primer.style/product/getting-started/foundations/>
- GOV.UK Design System: constrained reading width, responsive spacing, predictable type scale, and content-first layouts. <https://design-system.service.gov.uk/styles/layout/>
- WCAG 2.2 / WAI-ARIA APG: focus visibility, focus not being obscured, keyboard operation, and accessible disclosure/accordion behavior. <https://www.w3.org/TR/WCAG22/> and <https://www.w3.org/WAI/ARIA/apg/>
- web.dev / MDN: responsive layouts, touch targets, input modalities, and `prefers-reduced-motion`. <https://web.dev/articles/responsive-web-design-basics> and <https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion>

No React migration is required to benefit from these references. Ramu remains a static catalog-driven HTML/CSS/JS site unless a separate product need justifies changing that architecture.

## Audit of the current site

The current site is functional and already has good foundations: semantic sections, catalog-driven content, a working setup flow, responsive styles, keyboard-aware controls, and reduced-motion handling.

The main problem is visual competition. Too many elements ask for attention at once:

- five decorative brand colors are used across the interface;
- large radii, pill controls, tinted cards, shadows, and different section backgrounds are all used together;
- the homepage stacks many marketing-style sections before the product flow is complete;
- the hero uses a fake phone/ChatGPT mockup instead of showing Ramu itself;
- many looping or decorative animations run simultaneously: floating elements, shimmer, ripple, parallax/tilt, moving arrows, animated logo bars, page progress, particles, and reveal effects;
- mobile keeps several desktop compositions and mainly stacks or shrinks them;
- the mobile dock adds persistent navigation even when the page itself already has a clear linear flow;
- setup is correct structurally, but four large cards make a task flow feel heavier than it is.

The redesign should therefore remove more than it adds.

## Design thesis

Working direction: **quiet editorial product UI**.

This means:

- product-like density rather than landing-page spectacle;
- typography and information hierarchy do most of the visual work;
- one restrained brand accent instead of decorative multi-color identity;
- surfaces are separated primarily by spacing and hairline borders;
- color communicates state or emphasis, not variety;
- motion explains changes rather than continuously decorating the page;
- mobile is designed task-first, not treated as a scaled-down desktop.

## Anti-slop rules

Do not introduce these patterns unless a concrete product requirement later justifies them:

- decorative gradients;
- glassmorphism as a visual theme;
- glowing cards or cursor-following radial effects;
- 3D/parallax product mockups;
- floating decorative badges or notes;
- huge headline text used mainly for impact;
- every section using a different tinted background;
- every action becoming a pill;
- multiple accent colors without semantic meaning;
- fake usage metrics, fake testimonials, or vanity counters;
- looping decorative animation;
- sparkle/particle/confetti effects;
- illustrations that do not explain product behavior;
- arbitrary icon sets mixed together;
- framework migration purely to obtain a design-system look.

## Visual system

### Color

Use a warm neutral canvas with graphite text and one muted sage accent.

Initial token direction:

```css
--bg: #f7f6f2;
--surface: #ffffff;
--surface-subtle: #f1f2ee;
--text: #1f231f;
--text-muted: #687068;
--border: #d9ded8;
--border-strong: #bdc5bd;
--accent: #4c6658;
--accent-strong: #354d41;
--accent-soft: #e7eee9;
--focus: #315fcb;
```

These values are starting points, not a promise that the implementation must keep each hex unchanged after contrast testing.

Semantic colors such as success, warning, and danger may exist, but only for states that actually carry that meaning. A course card does not need its own color identity.

Do not carry the current orange/gold/blue/plum palette into general decoration. Those colors may remain only where a future semantic need justifies them.

### Typography

Keep typography understated and functional. Do not add a decorative display font simply to make the site look more designed.

Preferred stack remains a system-friendly sans/Inter-style stack.

Target scale:

| Role | Desktop | Mobile | Weight |
|---|---:|---:|---:|
| Hero | 56–64px | 38–44px | 600 |
| Page title | 44–52px | 34–40px | 600 |
| Section heading | 32–40px | 28–32px | 600 |
| Subheading | 20–24px | 19–22px | 600 |
| Body | 16px | 16px | 400 |
| Product/control text | 14–15px | 15–16px for important touch controls | 400–500 |
| Caption/meta | 13–14px | 13–14px | 400–500 |

Avoid routine `font-weight: 800/850`, artificial letter spacing, and uppercase text except for very short metadata labels where it improves scanning.

Long reading text should stay around 60–75 characters per line. Product surfaces may be wider because they are scanned rather than read as prose.

### Spacing

Use a small, predictable scale instead of per-component custom values:

`4, 8, 12, 16, 24, 32, 48, 64, 96`.

Large vertical gaps should reduce on compact/mobile viewports rather than staying proportional to desktop.

Main desktop shell: approximately 1080–1160px maximum.

Long-form copy should use its own narrower measure instead of stretching across the shell.

### Geometry

Use only three common radii:

- 6px: small controls/tags;
- 8px: buttons/inputs/list rows;
- 12px: primary surfaces/dialog-like blocks.

Pills are reserved for true badges, statuses, or compact filters. Primary buttons do not need to be pills.

### Elevation

Default surface separation is:

1. canvas color;
2. white/subtle surface;
3. 1px hairline border.

Shadows are exceptional. Use one subtle elevation token for menus/popovers/sticky overlays that genuinely sit above content.

Do not place a shadow on every card.

## Core component set

The redesign should be expressible with a small vocabulary:

1. `Button` — primary, secondary, ghost; icon variant only when needed.
2. `Link` — text link with clear hover/focus behavior.
3. `Surface` — neutral container with optional border; not automatically a card.
4. `Badge` — semantic/status only.
5. `Pack picker` — accessible single-select control with loading/error/selected states.
6. `Resource row` — compact row for course/pack listings.
7. `Progress` — setup completion/progress only.
8. `Step navigation` — desktop sticky stepper; mobile compact progress/accordion relationship.
9. `Accordion/disclosure` — FAQ and mobile setup disclosures using native semantics or WAI-ARIA patterns.
10. `Notice` — info/warning/privacy/source freshness messages.
11. `Skeleton/loading state` — only when dynamic catalog loading materially benefits from it.
12. `Empty/error state` — explicit recovery path when catalog/manifest fetch fails.

Every component must define default, hover, focus-visible, active, disabled (when relevant), loading, and error/selected states where applicable.

## Homepage information architecture

The homepage should answer these questions in this order:

1. What is Ramu?
2. Why is it useful?
3. What can I do right now?
4. Is there already a pack for me?
5. How does the approach work?
6. What should I know before using it?

### Desktop homepage

Recommended structure:

```text
Header
  Ramu | Packs | How it works | Docs | GitHub | Setup

Hero
  Left: product statement + concise explanation + primary/secondary action
  Right: real Ramu pack/workspace preview, not a fake phone mockup

Two paths
  Browse available packs
  Create a Starter for another course

Pack browser
  Pack picker + compact resource/course rows

How it works
  Five RIZMA layers as a calm list/table/stack, not five decorative colored cards

What Ramu does / does not do
  Short product boundaries + source/currentness note

FAQ
  Only questions that unblock first use

Footer
```

### Hero

Keep the core message close to the existing copy because the product idea is already clear:

> Satu ChatGPT Project untuk tiap mata kuliah, supaya konteks belajarnya tetap rapi.

Do not use a full-height hero by default. The first viewport should expose both the product promise and a meaningful route into the product.

The visual counterpart should show Ramu itself. Example:

```text
UT · S1 Akuntansi · Semester 2
5 mata kuliah · 16 SKS

Akuntansi Keuangan Menengah I          3 SKS  →
Perpajakan                             3 SKS  →
Manajemen Keuangan                     3 SKS  →
...

[ Setup pack ]
```

This is more credible than an illustrative phone frame because it demonstrates the actual product surface.

### Two-path onboarding

Immediately after or inside the hero, expose two distinct paths:

- **Sudah ada pack** → browse/select a pack;
- **Belum ada pack** → create a Ramu Starter.

This prevents the UT reference implementation from being mistaken for the architectural boundary.

### Pack browser

Prefer a resource-list pattern over marketing cards.

A course row should prioritize scanability:

```text
EACC4101   Pengantar Akuntansi                    4 SKS   →
MKWN----   Pendidikan Agama           Pilih 1 · 3 SKS   →
```

On wide screens, metadata can occupy stable columns. On narrow screens, it stacks naturally without inventing a different information model.

## Setup information architecture

The setup flow is already correct conceptually. Preserve the four steps and the pack/course behavior.

### Desktop setup

Use a product layout rather than four giant cards:

```text
Header
Pack selector / active pack metadata

┌──────────────────────┬────────────────────────────────────┐
│ Setup                │ Step 2 of 4                        │
│                      │                                    │
│ ✓ Memory             │ Project Instructions               │
│ ● Instructions       │ Short explanation                  │
│ ○ Course pack        │                                    │
│ ○ Start              │ [ Copy instructions ]  View source │
│                      │                                    │
│ 2 / 4 complete       │ Secondary notices / context        │
└──────────────────────┴────────────────────────────────────┘
```

Desktop rules:

- sticky step navigation may remain, but it becomes simpler and narrower;
- content should be flat sections/surfaces, not oversized floating cards;
- one dominant action per step;
- instructions and course pack actions remain visible without decorative wrappers;
- progress must describe actual state, not decorate the page;
- notices use the same `Notice` component with semantic variants.

### Mobile setup

Mobile is a task flow, not the desktop layout stacked vertically.

Recommended order:

1. compact header: back + Ramu/Setup title;
2. active pack selector;
3. progress summary (`Langkah 2 dari 4` + progress bar);
4. current step content;
5. completed/upcoming steps as accessible disclosures;
6. current primary action near the content that requires it.

Do not keep the current three-item floating mobile dock by default. Persistent mobile chrome is justified only if it measurably reduces friction. If a sticky bottom action is used, it should expose only the current primary action and must never obscure keyboard focus/content.

Course selection on mobile should use full-width resource/disclosure rows with at least 44–48px touch targets and clear expanded state.

Horizontal breadcrumb-like chains such as `ChatGPT → Settings → ...` should wrap or become a vertical ordered path rather than shrink into tiny pills.

## Responsive model

Do not design for named devices. Design for content breakpoints.

Initial implementation targets:

- compact/mobile: `< 720px`;
- intermediate: `720–959px`;
- wide/product desktop: `>= 960px`.

These numbers can shift when the new layout is tested. A breakpoint exists because the content stops working, not because a particular device model exists.

### Wide desktop

- maximum content width around 1080–1160px;
- setup uses sidebar + main content;
- course list can use stable metadata columns;
- navigation is horizontal;
- hero uses two columns only while both columns remain meaningful.

### Intermediate/tablet

- hero may remain two columns only if the product preview stays legible; otherwise stack;
- setup sidebar may turn into a horizontal compact stepper or top progress summary;
- do not squeeze desktop columns until text becomes narrow or awkward.

### Mobile

- single primary reading/task column;
- 16px body text for important reading/input contexts;
- minimum primary touch target approximately 44–48px;
- 16px horizontal page padding minimum, usually 20px when space permits;
- no horizontal scroll for core flows;
- no interaction that depends on hover;
- avoid fixed UI unless it has a stronger task value than the screen space it consumes.

## Interaction and motion

Motion budget:

- control feedback: ~120–180ms;
- menus/disclosures: ~160–220ms;
- page/section transition when needed: <=240ms;
- no continuous decorative animation.

Keep:

- hover/focus state transitions;
- dropdown/accordion open/close;
- progress changes;
- copy-success feedback;
- subtle loading state where data is actually loading.

Remove from the redesign:

- rainbow page progress;
- animated logo bars;
- scroll reveal blur;
- floating phone/background;
- pointer-driven 3D tilt;
- pulsing chat send button;
- decorative ripple;
- hover lift on every card;
- radial cursor glow;
- animated marker underline;
- breathing arrows;
- progress shimmer;
- celebratory particles;
- decorative full-page enter wipe.

`prefers-reduced-motion: reduce` remains mandatory, but the normal experience should already be calm enough that accessibility is not achieved merely by disabling an otherwise over-animated interface.

## Accessibility contract

Implementation must preserve or improve:

- complete keyboard operation for all actions;
- visible `:focus-visible` state with sufficient contrast;
- sticky/fixed UI must not obscure the focused element;
- mobile interactive targets should generally be >=44px, with approximately 48px preferred for primary touch controls;
- semantic native elements are preferred over custom ARIA widgets;
- custom picker/listbox behavior must maintain expected keyboard and focus behavior;
- expanded/collapsed controls expose correct state;
- status must not be communicated by color alone;
- text and UI contrast must be verified against WCAG targets;
- zoom/reflow should not create horizontal scrolling for the primary flow;
- controls remain understandable without animation.

## Content rules

The site should sound like a product guide, not marketing copy.

Prefer:

- direct task language;
- short labels;
- sentence case;
- concrete descriptions;
- visible boundaries/uncertainty when relevant.

Avoid:

- hype words;
- AI buzzwords where a normal word is clearer;
- repeated explanation of the same concept across several sections;
- headings whose only job is visual drama;
- technical implementation details before they help first use.

## What remains unchanged

The redesign must not casually change these product contracts:

- catalog-driven pack discovery;
- manifest-driven course/setup data;
- Semester 2 remains the default entry point unless a separate product decision changes it;
- query/pack switching behavior;
- Project Instructions fetch/copy flow;
- course-pack download behavior and filename contract;
- local setup-progress persistence;
- choice-slot behavior for Semester 1 Religious Education;
- source/pack status semantics;
- English entry surface strategy;
- static deploy architecture;
- browser regression and validation gates.

## Implementation plan

### Phase 1 — foundations

- replace existing decorative palette with semantic tokens;
- establish type/spacing/radius/elevation scales;
- define focus/interaction states;
- remove decorative motion that is no longer part of the direction;
- keep existing DOM behavior working while tokens settle.

### Phase 2 — homepage structure

- rebuild hero around Ramu itself, not the phone mockup;
- expose Pack vs Starter entry paths;
- convert pack/course cards into resource-list patterns;
- simplify RIZMA presentation;
- compress or remove redundant marketing sections;
- keep trust/FAQ only where they help first use.

### Phase 3 — setup desktop

- convert giant card stack into a product-oriented step layout;
- retain progress, copy, download, course disclosures, and pack picker;
- normalize notices and action hierarchy.

### Phase 4 — mobile-specific UX

- remove desktop-only visual ideas instead of merely stacking them;
- design pack browsing and setup for touch first;
- replace the current mobile dock unless testing demonstrates that persistent navigation is still useful;
- test 360px, 390px, and 430px-class widths plus an intermediate/tablet width.

### Phase 5 — accessibility and regression

- keyboard test pack picker, disclosures, setup actions, and focus order;
- verify focus is not obscured by sticky UI;
- verify touch targets and reduced motion;
- extend Playwright to cover both a wide viewport and a representative mobile viewport;
- keep existing functional regression assertions.

### Phase 6 — identity completion

Only after the redesigned interface stabilizes:

- create the repository social preview image;
- align README hero/brand assets if needed without rewriting README structure;
- consider whether a dark appearance is useful. Do not add dark mode merely because design systems commonly provide it.

## Implementation acceptance criteria

The redesign is ready to merge only when:

- a first-time visitor can identify what Ramu is and reach Pack or Starter quickly;
- the homepage does not require decorative motion to feel intentional;
- the product still works with animation disabled;
- desktop and mobile each have an intentional layout, not only CSS stacking;
- no core action depends on hover;
- one course can still be selected, set up, copied, downloaded, and persisted through the existing flow;
- all pack variants and the Semester 1 choice slot still render correctly;
- keyboard use remains complete;
- focus states are visible and unobscured;
- browser regression runs at desktop and mobile viewport sizes;
- repo/static/site validation remains green;
- visual changes do not require React, a design-system runtime, or new build infrastructure without a separate justification.

## Short design review checklist

Before approving any redesign PR, ask:

1. Is this element helping comprehension or only adding decoration?
2. Could spacing, type, or border hierarchy solve this without another color/card?
3. Does this state still make sense on a 390px touch screen?
4. Does keyboard focus remain obvious?
5. Is the action hierarchy obvious without reading every paragraph?
6. Is any animation looping without communicating state?
7. Does the design still look like Ramu if the accent color is removed?
8. Is the product being shown directly, or replaced by a decorative mockup?
9. Did the change preserve catalog/setup/runtime contracts?
10. Would this still look deliberate if generated UI trends changed next year?
