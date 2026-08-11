---
name: click-to-convert-audit
description: >-
  Audit a landing page to assess how likely it is to convert traffic from
  Google Ads, and produce a prioritized, evidence-backed list of fixes. Use
  this whenever the user shares a landing page URL and asks whether it will
  convert, whether it's ready to run paid traffic to, or about Quality Score,
  landing page experience, message match, scent, or the post-click experience.
  Trigger it even when the user just pastes a URL and asks "will this convert?",
  "is this page good for Ads?", "why isn't my landing page converting?", "audit
  this page", "CRO audit", "am I wasting ad spend?", or shares ad copy and
  keywords alongside a page. Prefer this skill over a generic critique whenever
  Google Ads, PPC, paid search, or conversion of paid traffic is in play.
_agensi: "1c2db296-4e54-4cda-859f-ea4d3049a899"
---

# Landing Page Ads Conversion Audit (Generalist)

Estimate how well a landing page will convert Google Ads traffic and return
prioritized fixes. This is the generalist layer: durable, page-type-agnostic
rules. It applies to SaaS, e-commerce, lead magnets, and services alike.

Two principles govern everything:

1. **Caps override.** Some failures are not deductions you can average away.
   They invalidate the verdict entirely — because they corrupt trust, invite
   platform enforcement, or physically break the conversion mechanism. A broken
   foundation makes a beautiful page worthless, the same way a broken macro
   makes a polished financial model worthless.
2. **Copy is judged last and cannot rescue.** Excellent copy makes a
   functional, well-targeted page better. It never saves a broken or misaligned
   one. Audit in dependency order; do not critique persuasion on a page that
   fails an upstream gate.

## The honesty and detection model — read before producing anything

This skill audits what is observable from the fetched page (plus ad context if
given). It has NO access to the user's Google Ads account, no ability to run a
throttled mobile test, and no ability to actually submit a form. Label every
finding with one of three confidence levels, and never overstate:

- **CONFIRMED** — directly visible in the fetched page (e.g., the URL scheme is
  `http://`; an `http://` asset is referenced on an `https` page; no privacy
  policy link exists in the markup).
- **INFERRED** — a strong structural signal, not definitive (e.g., a single
  H1 with no category noun suggests a category-clarity problem).
- **UNVERIFIABLE** — cannot be settled by reading the page; needs a live tool,
  a real device, or account access.

**Tooling order: free public tool > connector > pre-flight flag.** If something
is checkable with a free public API (e.g. PageSpeed Insights for mobile speed),
the skill runs it ITSELF and reports real numbers — it does not ask for a
connector or downgrade the item to UNVERIFIABLE. A connector is only for
account-locked data (ad copy, keywords, real conversion tracking), because most
users have neither a connector nor a paid plan.

NEVER claim to read the account's Quality Score or Landing Page Experience
rating. NEVER claim to have measured load time or to have submitted the form.
You predict *direction* and you *flag* what you cannot see. Stating limits
plainly is what makes the audit credible.

## Step 0 — Determine the tier

- **Tier 1 (URL only):** run the full page read (Steps 2–6). Scent (Step 1)
  needs ad context, so note it as a ceiling: "Without the ad copy and keywords
  I can't judge scent — the single biggest driver of paid relevance."
- **Tier 2 (URL + ad context):** the user also gave ad headlines, keywords,
  match types, ad group theme, or campaign goal. Run Step 1 (scent) as well.

If the user is clearly running Ads but gave no ad context, DO NOT just ask them
to type it. Follow the guided intake in `references/intake.md`: ask the platform
first, then offer the easiest extraction path that fits — pull it via a
connected ads data source if one exists (zero manual work), else accept a
screenshot, a native copy/paste, or a filled template, in that order of
preference. If none is available, proceed Tier 1 and state the ceiling.

## Step 0.5 — CAPS: detect, then gate (do this FIRST, before any scoring)

Run the detectable checklist in `references/caps-and-hygiene.md`. Sort what you
find into three buckets:

- **Confirmed caps** — HARD STOP. Report the cap, why it overrides, and the
  fix. Do not issue a positive verdict. The three cap causes are: trust
  corruption (e.g., missing HTTPS on a data-collecting page), policy
  enforcement risk (deceptive elements — fake timers, bait-and-switch), and
  physical break (dead primary CTA).
- **Unverifiable caps** — the verdict becomes CONDITIONAL. These are the ones
  you cannot confirm by reading the page: conversion-tracking integrity (wired
  correctly, not double-counting, fires on submit not page load), real mobile
  load (LCP on a throttled connection), live form submission firing the
  thank-you, mixed content / insecure form endpoints if not visible in the
  fetched markup. Give the full read, but hold the verdict: "Not cleared for
  spend until you confirm: [list]," with the how-to-check steps from the
  reference. Any of these, if broken, overrides everything above.
- **Deductions** — carry forward into scoring (Steps 2–6). The page still runs;
  these tax it via Landing Page Experience and CPC. Note the special case of
  on-load interstitials: a heavy deduction with a mandatory immediate fix, just
  below a true cap (trivially removable, doesn't corrupt data).

## Step 1 — Handoff and scent (Tier 2 only)

The audit begins at the handoff: imagine clicking the ad on mobile. Evaluate
scent — the unbroken continuity of the visitor's expectation — across the three
axes in `references/scent.md`: intent promise (the core; supersedes phrasing),
lexical recognition (an accelerant that inverts into a doorway-page signal if
keywords are stuffed), and visual register (does the page feel like it came
from the same sender). Operational test: read the ad, look away, look at the
fold for two seconds; the page must obviously deliver the promised thing AND
feel like the same sender.

## Steps 2–6 — The page read

Once caps clear (or are flagged conditional), run the sequence in
`references/page-read-sequence.md`, IN ORDER, short-circuiting on upstream
gates:

2. **Five-second test** — category clarity first (what *is* this: software,
   store, download, person for hire — the gate everything sits behind), then
   next-step clarity. If category fails, the page is dead on arrival; report
   that and don't critique downstream copy nuance.
3. **Trust and proof** — presence, proportionality to the ask, specificity /
   verifiability, congruence and proximity. Generic unfalsifiable signals score
   near-zero, not "weak."
4. **Friction** — weighed against the visitor's intent stage. The same form is
   fine late and fatal early.
5. **Copy and objection handling** — last. It refines; it does not rescue.

## Step 7 — Synthesize and output (two formats, always both)

Rank fixes by impact × ease; lead with caps. Then produce BOTH outputs from
`references/report-template.md`, clearly separated, in this order:

1. **Human-readable** — short and table-first: verdict, one-line take, a status
   table (OK / FIX / STOP / VERIFY per area), and the top fixes. For a busy
   founder or marketer; keep it skimmable, no long prose. If the verdict is
   conditional, say so in the verdict line.
2. **AI-readable** — a **Cursor-ready markdown change brief** (the default agent
   format), ready to hand to Cursor or Claude Code. Each change names its layer
   (copy / ui / functionality / architecture / tracking / performance),
   location, current vs. target state, an imperative instruction, a rationale,
   and an acceptance check. The DO NOT TOUCH boundary sits at the top in
   language the agent can't miss. Tracking-integrity and form-submission items
   live in DO NOT TOUCH / Pre-flight, never as fabricated fixes. Emit the JSON
   variant only if the user asks or a non-agent consumer (dashboard) is targeted.
