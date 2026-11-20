---
name: design-quality-gate
description: Use when building, reviewing, or polishing a website or application UI, including requests about spacing, typography, generic AI-generated design, responsiveness, accessibility, and visual consistency.
---
# Design quality gate

1. Read project design tokens, product goal and user-provided visual references. Do not replace brand identity with a fashionable default.
2. Audit hierarchy, copy, type scale, contrast, whitespace, grid, 4/8px rhythm where compatible, alignment, interaction states, semantic HTML and keyboard flow.
3. Render at desktop, tablet, mobile sizes; inspect actual browser screenshots and identify up to five concrete failures, with evidence.
4. Detect habitual AI patterns (generic purple gradients, repeated card grids, excessive glow, vague copy) **only when they weaken the product's intent**; never ban a valid brand choice by reflex.
5. Make the smallest targeted changes, preserve working interactions, and check no horizontal scroll, focus loss or content overlap.
6. If available, use **one** of Impeccable, Unslop or Taste for a review rather than automatically running all. Run Web Design Guidelines and Playwright checks independently where useful.
7. Keep before/after screenshots, test viewport dimensions, accessibility issues and remaining concerns.

**Definition of done:** browser-verified design, states and interactions; no unsupported claim of 'award-winning'.
