# Atlas Design Grammar

**Candidate, not ratified. 2026-08-14.** A shared grammar for atlas pages across
`grid-dependency-atlas` and its siblings. Companion to
[ATLAS-REVIEW.md](ATLAS-REVIEW.md) (what exists) and
[ATLAS-MIGRATION-PLAN.md](ATLAS-MIGRATION-PLAN.md) (how to get there).

This is a grammar, not a skin. Most of it is about **what a page is allowed to
assert and how it must qualify the assertion.** The visual rules exist to make
those distinctions visible; they are downstream.

---

## 1. Five governing rules

**R1 — One question per page.** A page states one question and answers it. The
answer appears above the fold, in the H1 and the sentence beneath it. Everything
else on the page is evidence for, qualification of, or derivation from that
answer. If a second question is interesting, it is a second page.

**R2 — Every assertion declares its register.** Each claim on a page is
`observed`, `derived`, `interpreted`, or `refused` (§2). The register is visible
to the reader without interaction. A page that cannot classify an assertion may
not publish it.

> **R2a — the register system is infrastructure, not the subject.** Added
> 2026-08-14 after a cold read of the Hormuz specimen: *"the page is written to
> survive hostile review rather than to be read."* Marks travel beside claims;
> the definitions, the refusal block, and the derivation rules belong at audit
> depth, not above the first finding. A page must not announce its epistemology
> before the reader knows why they should care. If a reader finishes and has
> learned more about the repository than about the subject, the grammar has been
> displayed rather than used.

**R3 — Qualification travels with the claim.** A boundary condition, denominator,
observation window, or confidence marker renders adjacent to the thing it
qualifies, at readable size, in the default state. Never in an empty state,
never behind hover, never inside `<details>`, never only in a footer.

**R4 — Annotation before interaction.** If the point can be made by writing it on
the figure, write it on the figure. Interaction is permitted only to reveal
*more* material, never to reveal the point.

**R4a — Never encode an order the source does not have.** A sorted axis, a
severity ramp, or a shared reference line asserts commensurability. If the
underlying values are not the same quantity, the visual makes the claim the prose
is disclaiming, and the disclaimer loses. Split the figure instead. *(Firing
case: the Hormuz reserve chart put seven figures on one axis against one 60-day
line while the caption explained that five of them counted different things.)*

**R5 — Derived values show their rule.** Anything the atlas computes or assigns —
a band, a rank, a score, a drawn boundary — carries its inputs and its rule at
the point of display, and the full rule appears in the page's Method section. An
assignment with no stated rule is not publishable. *(This rule alone would have
caught the `stress_band` gap.)*

---

## 2. The register system

Two orthogonal axes. Do not collapse them.

### 2.1 Register — who produced the assertion

| Register | Definition | Required fields | Ink |
|---|---|---|---|
| `observed` | A value or fact read off a source document. | ≥1 `receipt`; `unit`; `as_of`; `denominator` if a ratio | Full-strength semantic hue, solid |
| `derived` | Computed or assigned by the atlas from observed inputs. | `inputs[]` (claim ids); `rule` (one sentence); **no receipt of its own** | Same hue, dashed outline / hatched fill, never solid |
| `interpreted` | Authored judgment. Legitimate, publishable, and not evidence. | `basis` (what it reasons from); named as authored | No hue. Serif prose, left rule, no fill |
| `refused` | A claim the atlas explicitly declines to make. | `why` | Muted, but **rendered** — never omitted |

A `derived` value may not carry a citation. Citing a source under a value the
atlas computed is the specific failure this axis exists to prevent.

`refused` is not decoration. `intake-composition-atlas` already ships it
("*What this refuses to claim:*"), and the empty region of a map is a finding
(§ the atlas's own "absence of a marker" caveat, promoted from empty state to
first-class content).

### 2.2 Standing — what kind of record supports an observation

Adopted from `intake-composition-atlas/schema.yaml`, unchanged. Applies only to
`observed` claims.

`documented` (a public record states it) · `authorized` (an instrument permits
it; no evidence it occurs) · `inferred` (composition makes it derivable;
requires `derivation`) · `speculative` (incentive analysis only; excluded from
default view; max 2 per page).

Receipt-kind eligibility, the "third-party journalism is leads-only" rule, and
the staleness windows (90d observed artifacts / 365d default) come with it.

**Do not fork this.** One vocabulary across the family, defined in one place.

### 2.3 The claim record

```yaml
- id: c-hormuz-ph-oil
  register: observed
  standing: documented
  text: "92% of Philippine crude imports transit Hormuz"
  value: 92
  unit: percent
  denominator: "crude oil imports by volume, 2025 calendar year"
  as_of: 2026-03-24
  receipts: [r-hormuz-ph-doe]

- id: c-hormuz-ph-band
  register: derived
  text: "Philippines: least margin of the twelve"
  inputs: [c-hormuz-ph-oil, c-hormuz-ph-reserve, c-hormuz-ph-genmix]
  rule: "reserve_days below 60 AND chokepoint import share above 75% AND no
          pipeline alternative → band 1 of 5"
  confidence: high
  confidence_basis: "All three inputs from first-party or IEA reporting."

- id: c-hormuz-ph-capacity
  register: interpreted
  text: "State capacity to administer prolonged rationing is thin."
  basis: "Typhoon-season grid stress record; 4-day government work weeks
          adopted within three weeks of the emergency declaration."
```

Fields are additive to the existing GeoJSON properties. Nothing above requires
re-researching a single case — it requires **re-typing what is already written**.

---

## 3. Page hierarchy

The canonical order. A page may omit a rung; it may not reorder them.

```
1  MASTHEAD        atlas · question-as-title · one-sentence answer · evidence window
2  ANSWER          the current state in 2–4 sentences. registers marked inline.
3  PRIMARY FIGURE  the one figure that carries the answer. annotated on the mark.
4  INTERPRETATION  what it means. authored, visibly authored.
5  ADDITIONAL EVIDENCE   further figures / the case list. each with its own finding-title.
6  BOUNDARY        what this does not show. what would change the answer.
7  METHOD          the rule, in one sentence, then the detail.
8  RECEIPTS        every source, what it supports, when retrieved, archive link.
```

Rungs 6–8 are the audit floor and are **always present, always visible, never
collapsed**. A page with no boundary conditions has not been reviewed.

### 3.1 Reading-depth contract

| Depth | Reader gets | Delivered by |
|---|---|---|
| **20 s** | The question, the answer, the shape of the evidence, how old it is | Rungs 1 + 3's title + the annotation on the primary figure |
| **3 min** | The reasoning, the main qualification, what would change it | Rungs 2, 4, 6, and the figure footers |
| **Full audit** | Every claim's register, rule, denominator, window, and source | Rungs 5, 7, 8 and per-claim markers throughout |

Nothing in a shallower depth may be *contradicted* by a deeper one. The 20-second
read must be a true summary, not a hook the audit walks back. This is the
strongest constraint in the document.

### 3.2 Two page types, not one

**Overview page** (one per atlas) — the full hierarchy above. Rung 5 is the case
index. One per substrate: nine of these.

**Case page** (one per case) — the same hierarchy at case scale. Question is the
case's question; primary figure is the case's mechanism (often the
consequence-vs-control pair); receipts are that case's sources. 85 of these.

Case pages are **real URLs with real content in the HTML**. The current
inspector-panel model has no addressable case, nothing to link to, nothing to
cite, and nothing without JS. Every case becoming a citable page is the single
largest gain available.

---

## 4. Component vocabulary

Twelve primitives. Adding a thirteenth requires deleting one.

| Component | Purpose | Rules |
|---|---|---|
| `masthead` | Kicker, question-title, answer, evidence window | Title is the claim, not the topic. Window is `max(receipt.as_of)`, auto-derived, always rendered |
| `claim` | An inline assertion | Carries a register marker and receipt refs. Never bare |
| `figure` | The evidence unit | Finding-title + mark + on-mark annotation + footer strip (§5) |
| `annotation` | Text on a figure | Names what to see. Placed on the mark, leader line if needed. Not a tooltip |
| `interpretation` | Authored reasoning | Serif, left rule, byline-adjacent. Visibly not data |
| `boundary` | Limits of the claim | A section with a heading. One quotable sentence first |
| `method` | The rule | Opens with the rule in one sentence. Then detail. Never collapsed |
| `receipts` | Source table | publisher · document title · retrieved · archived · supports (claim ids) |
| `refusal` | What is not claimed | Rendered. Usually near the masthead |
| `case-index` | Corpus navigation | A reading list with one-line claims. **Not** filter dropdowns |
| `figure/map` | Geography *as a figure* | A map is one mark type among several, sized and placed like any figure |
| `register-key` | Legend for §2 | Once per page, near the top, four swatches |

**`case-index` replaces the filter toolbar.** Faceting 5–16 authored cases is
dashboard furniture. A list with a claim per line is faster to read, works
without JS, is linkable, and is honest about corpus size. Facets return only if
a corpus passes ~100 cases, and then as an index page, not a toolbar.

**`figure/map` is a demotion and it is the point.** The map stops being the
application shell and becomes a figure that must earn its place like any other.
Where geography is the argument (`us/` overlays, `chokepoints/`) it stays large
and central. Where it is not (`hormuz/`, `insurance/`, `cloud/`, `subsea/`) a
ranked chart, a flow diagram, or a table communicates more per pixel.

---

## 5. Figure rules

Every figure carries a **footer strip** — small, monospaced apparatus, always
present, never hidden:

```
WINDOW 2026-01-01 → 2026-03-26   ·   n = 12 of 12 countries assessed
DENOM  crude imports by volume   ·   OBSERVED (IEA, national DOEs)  ·  DERIVED band
```

Rules:

1. **Title states the finding**, not the variable. "Four countries have under
   sixty days" — not "Reserve days by country."
2. **Annotate the mark**, don't legend it. Label the two or three marks that
   carry the argument, in place.
3. **Observed and derived use different ink.** Solid vs. dashed/hatched. A
   figure mixing the two must show both treatments in its key.
4. **Denominators are stated on the figure.** A percentage with no stated base
   is not publishable.
5. **The window is on the figure.** Not just in the masthead.
6. **n and the universe are stated.** "12 of 12 assessed" is different from "12."
7. **No chart without a finding.** If the figure has no annotation because there
   is nothing to point at, it is a table. Ship the table.
8. **Authored geometry is drawn as authored.** Hand-drawn service territories
   and jurisdiction footprints get a hatched fill and a dashed edge — never the
   same treatment as basemap coastlines — and the figure footer says
   `DERIVED · approximate footprint, not physical routing`.

---

## 6. Typographic and color grammar

The register split does double duty as the type split. This is what earns
"aggressive but restrained hierarchy" without adding decoration.

**Two families:**

- **Serif** (`Newsreader`, already used by `intake-composition-atlas`) — argument.
  Question-titles, answers, interpretation, boundary prose. The reader learns
  serif = a human is talking.
- **System sans** — apparatus. Labels, values, table content, figure footers,
  receipts, register markers.

**Scale** — five sizes, no more:

| Role | Size | Family |
|---|---|---|
| Question-title | 40–46px / 1.08 | serif 600 |
| Section / finding-title | 22–26px | serif 600 |
| Answer, interpretation, boundary | 18–19px / 1.55 | serif 400 |
| Body, figure labels | 14–15px | sans |
| Apparatus: markers, footers, receipts | 11–12px, 0.08em tracking | sans 700 caps / mono |

**Color** — keep the existing palette (`#f5a623` `#bd7dff` `#4fc3f7` `#66bb6a`
`#ef5350` `#fdd835` on `#0a0a0a`) with two new constraints:

1. **One hue, one meaning, atlas-wide.** Today `#f5a623` means electricity in
   `us/`, outage in `cloud/`, medium-confidence in `hormuz/`. Fix the mapping in
   one shared token file and let per-atlas categories draw from it.
2. ~~**Hue is reserved for observed data.**~~ **Amended 2026-08-14 — this rule
   was too doctrinaire and is withdrawn.** It was written to make the page's ink
   track its epistemics: where there is colour, there is a measurement. Applied
   to the Hormuz specimen it produced a full-page map rendered in near-uniform
   grey, communicating almost nothing but hatch-vs-no-hatch — principle
   defeating utility. **Replacement:** semantic status constrains visual
   *rhetoric*, not visual *availability*. Interpreted classes may use restrained
   **categorical** colour, provided (a) the figure states plainly what the fill
   encodes, and (b) the palette is not a gradient unless the underlying values
   are genuinely ordered. A gradient asserts ranking; that assertion needs the
   same evidence as any other.

**Chrome budget:** no card backgrounds, no border-radius above 3px, no shadows,
no gradients. Structure comes from rules, space, and type. The existing
`border-radius: 10px` cards on the splash go.

---

## 7. Explicit anti-patterns

Rejected, with the atlas-specific reason:

- **Filter toolbars over authored corpora** — implies a dataset to slice; there
  are 5–16 authored cases.
- **KPI pills counting the corpus** — "9 control layers" is a fact about the
  schema, not the world.
- **Hand-typed status strings** ("Active crisis") — a status board with no
  backing signal. Status is `derived` from data with an `as_of`, or it is absent.
- **Caveats in empty states** — the current failure mode exactly: the boundary
  condition is shown only to readers who have not yet seen a claim.
- **`<details>` around methodology** — the sibling repo does this today; the
  method section is the deliverable, not the appendix.
- **Tooltips carrying qualification** — unavailable on touch, unprintable,
  unlinkable, invisible to search.
- **Choropleth for ordinal severity** — encodes magnitude as land area.
- **A single application shell for all nine atlases** — nine substrates do not
  share a composition; they share a *grammar*. Shared primitives, per-atlas
  composition.
- **Map-by-default** — geography must earn the frame.
- **Interaction as the reveal** — if a click is required to learn the point, the
  point was not written down.

---

## 8. Shared vs. site-specific

**Shared** (one definition, family-wide): the register system §2; the claim
record; the receipt record; the page hierarchy §3; the twelve primitives §4; the
figure footer contract §5; type scale and color tokens §6; the evidence-window
derivation; the accessibility floor (§9).

**Site-specific** (per atlas, deliberately): which figure is primary; the
category vocabulary and its hue assignments; the mark type; whether a map is a
figure at all; the editorial voice; the derivation rules for that atlas's bands.

The failure mode to avoid is a single shell that makes all nine look the same.
The grammar should let a chokepoint atlas be map-first and an insurance atlas be
chart-first while a reader recognizes both as the same publication — the way two
articles in the same newspaper share a typeface and a citation style but not a
layout.

---

## 9. Accessibility floor

Non-negotiable, and mostly free at build time:

- Content in the HTML, not assembled by JS. Case pages must be readable and
  crawlable with scripting off.
- Real heading outline (`h1` → `h2` per rung) present in source.
- Every control labelled (`<label for>`), every figure with a text alternative
  that states the finding, every interactive element keyboard-reachable.
- Figure meaning never carried by hue alone — pair with shape, dash, or label.
- Contrast ≥ 4.5:1 for body text. The current `#666` labels on `#111` fail; the
  `#444` notes fail badly.

---

## 10. What this grammar does not decide

Visual identity beyond the constraints above (specific serif, exact spacing
scale, mark styling) is deferred until the specimen in
[ATLAS-MIGRATION-PLAN.md](ATLAS-MIGRATION-PLAN.md) has been built against real
material and read. Test the grammar first; style it once it is known to work.
