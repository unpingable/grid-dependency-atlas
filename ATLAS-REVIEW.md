# Atlas Review — what these sites currently are

**Review date: 2026-08-14. Reviewer pass over `grid-dependency-atlas`,
`intake-composition-atlas`, `governor-atlas`. Findings only — no code changed.**

This document answers "what is this?" before anything answers "what should it
look like?" Companion documents: [ATLAS-DESIGN-GRAMMAR.md](ATLAS-DESIGN-GRAMMAR.md)
(proposed grammar) and [ATLAS-MIGRATION-PLAN.md](ATLAS-MIGRATION-PLAN.md) (path).

---

## 0. Method and what was measured

Read: all 10 HTML pages in `docs/`, all 11 GeoJSON datasets, all 16 case YAMLs,
`README.md`, `SYNTHESIS.md`, `TAXONOMY.md`, `CASES.md`, `REFRESH.md`,
`PROVENANCE.md`, `schema.yaml`; the sibling repos' schemas, build tooling, and
splash pages; `strategicallyempty.com`.

Measured mechanically (scripts, not impressions):

- CSS/JS line-level duplication across the nine map pages
- GeoJSON property-key coverage per atlas
- YAML ↔ GeoJSON field-by-field divergence for all 16 U.S. cases
- citation counts, unique URLs, unique publishers, bare-domain rate
- HTTP status for a 42-URL sample (25% of unique citations)
- source-date recency per atlas against today

Every number in this document came from one of those passes.

---

## 1. Inventory

### 1.1 The family

Three repositories, published as three separate GitHub Pages sites, sharing a
thesis shape ("populations exposed to decisions made outside their effective
control") and explicitly cross-referencing each other.

| Repo | Site | Substrate | Renderer | Build |
|---|---|---|---|---|
| `grid-dependency-atlas` | `unpingable.github.io/grid-dependency-atlas/` | Physical & digital infrastructure | 9 hand-written MapLibre pages + 1 splash | **none** |
| `intake-composition-atlas` | `unpingable.github.io/intake-composition-atlas/` | Federal data intake / composition | Cytoscape graph + editorial splash | `tools/build.py` + `tools/lint.py` |
| `governor-atlas` | (docs/ present) | Agent Governor as a claimdocs case | `graph.html` + index | `claimdocs.yml` manifest |

These have **drifted into independent products**, and the drift is not
symmetric. `intake-composition-atlas` is a generation ahead on evidence
architecture and a generation behind on reach (2 cases vs 85 features).
`grid-dependency-atlas` is the reverse. `governor-atlas` is a third thing —
self-documentation of the tooling — and is out of scope for this review beyond
noting it shares the receipts vocabulary.

**The most important inventory finding is not in this repo.** The evidence model
the redesign brief asks for — typed claims, receipts, derivation, refusal —
already exists, fully specified and machine-enforced, in
`intake-composition-atlas/schema.yaml`. See §3.4.

### 1.2 The nine atlases in this repo

| Atlas | Route | Features | Geometry | Vocabulary | Newest source |
|---|---|---|---|---|---|
| U.S. Infrastructure | `us/` | 16 | Point + 32 overlay polygons | `utility_type`, `control_layer`, `status`, `confidence` | 2026-05-20 (86d) |
| Hormuz Energy | `hormuz/` | 12 | Country polygons | `stress_band`, `confidence` | 2026-03-26 (141d) |
| Maritime Chokepoints | `chokepoints/` | 5 | Point | `status`, no confidence | 2026-03-11 (156d) |
| Insurance | `insurance/` | 6 | State polygons | `stress_band`, `confidence` | 2026-01-01 (225d) |
| Fertilizer-to-Food | `fertilizer/` | 12 | Country polygons | `stress_band`, `confidence` | 2026-03-30 (137d) |
| Water Basins | `water/` | 8 | Point | `category`, no confidence | 2026-01-09 (217d) |
| Grid Equipment | `grid-equipment/` | 7 | Point | `category`, `severity`, no confidence | 2025-10-01 (317d) |
| Subsea Cables | `subsea/` | 9 | Point | `category`, no confidence, no severity | 2026-01-01 (225d) |
| Cloud / CDN | `cloud/` | 10 | Point | `category`, `severity`, no confidence | 2025-12-01 (256d) |

85 case features, 177 citations, 166 unique URLs, 131 distinct publishers.

### 1.3 Frameworks, pipeline, deployment

- **Framework:** none. Ten standalone HTML files, each carrying its own
  `<style>` and `<script>` inline.
- **Only runtime dependency:** `maplibre-gl@4.1.2` from unpkg (CSS + JS), plus
  CARTO `dark_all` raster tiles. No SRI hashes, no local fallback, no vendoring.
- **Build system:** none. No `package.json`, no `Makefile`, no `tools/`, no
  `.github/`. Nothing generates anything. Every count, label, and legend on
  every page is hand-typed.
- **Data pipeline:** none. GeoJSON is hand-authored and hand-edited in place.
  `cases/*.yaml` exists for the U.S. atlas only and feeds nothing.
- **Deployment:** GitHub Pages serving `/docs` from `main`. No `.nojekyll`
  (the sibling repo has one). Push is publish.
- **Tests / checks:** none, in any form.

`REFRESH.md` names five primitives a tool *would* implement (`count-derive`,
`schema-check`, `drift-check`, `splash-generate`, `readme-atlas-table`) and
implements zero. It is an honest document about an unbuilt thing, and it is
also the best existing spec for what the build step should do.

### 1.4 What is clearly related vs. what has drifted

**Related, tightly:** the nine map pages. They are the same file, cloned eight
times, with vocabulary substituted. Of ~289 CSS lines per page, **129 are
byte-identical across all nine**. Of ~227 JS lines per page, **66 are identical
across all nine**. `showPanel`, `hidePanel`, `applyFilters`, `updateFilterCount`,
`isMobile`, the drag-to-dismiss handler, and the entire mobile drawer CSS are
copy-pasted nine times. This is not a shared component library with
customization. It is a fork tree with no trunk.

**Drifted:** the splash page (`docs/index.html`) is a different product from
the pages it links to — a card grid with no map, no data binding, and hand-typed
statistics. The `intake-composition-atlas` splash is a different product again,
and a better one (§5.4).

---

## 2. Current product grammar

### 2.1 The recurring page structure

Every atlas page except the splash is the same three-zone application shell:

```
┌────────────────────────────────────────────────────────┐
│ header: ← Atlas · H1 · subtitle (one editorial line)   │
├────────────────────────────────────────────────────────┤
│ filters: 2–3 <select> dropdowns  ·  count  ·  legend   │
├──────────────────────────────────────┬─────────────────┤
│                                      │  panel (420px)  │
│   MapLibre canvas                    │  placeholder    │
│   colored dots or choropleth         │    ↓ on click   │
│                                      │  badge          │
│                                      │  H2 title       │
│                                      │  italic one_line│
│                                      │  meta-row ×3    │
│                                      │  field ×4–6     │
│                                      │  sources        │
└──────────────────────────────────────┴─────────────────┘
```

The panel is a **flat property dump**. Every field renders as
`LABEL-IN-CAPS / value`, at the same size, weight, and color, in schema order.
There is no hierarchy inside the panel: `Trigger`, `Public Consequence`,
`Who Controls`, `Sources` are typographically equal. The reader is given a
record, not an argument.

### 2.2 Visual conventions that exist

Consistent across all ten pages, and genuinely a system even though nothing
enforces it:

- Near-black ground `#0a0a0a`, panel `#111`, hairline borders `#222`
- Body text `#e0e0e0` / `#ccc`, labels `#666`, muted notes `#444`–`#555`
- A stable six-color semantic palette: amber `#f5a623`, violet `#bd7dff`,
  cyan `#4fc3f7`, green `#66bb6a`, red `#ef5350`, yellow `#fdd835`
- Uppercase 11px letterspaced field labels
- Tinted-background badges (dark hue + saturated foreground) for enum values
- System sans throughout; no serif, no display face, one weight axis
- Mobile: panel becomes a slide-up drawer at ≤900px, with drag-to-dismiss

That palette is a real asset. It is applied inconsistently — `#f5a623` means
"electricity" in `us/`, "outage" in `cloud/`, and "medium confidence" in
`hormuz/` — but the *set* is coherent and worth keeping.

### 2.3 How claims, evidence and uncertainty are currently represented

| Element | How it appears | Problem |
|---|---|---|
| **Claim** | `one_line`, styled italic under the title | Italic is the only marker; not distinguished from description |
| **Observation** | `hormuz_oil_pct: 92`, `reserve_days: 45` | Rendered as bare text, no unit, no source attached to the *number* |
| **Derived metric** | `stress_band: already_stressed` | **Derivation is documented nowhere.** See §4.1 |
| **Interpretation** | `rationing_capacity`, `alternative_supply`, `mitigation` | Rendered identically to observations. Reader cannot tell them apart |
| **Caveat** | one static line in the empty-state; one italic line under the overlay legend | Disappears the moment a case is selected — visible only when nothing is |
| **Provenance** | `sources[] {publisher, url, date}` as a `<br>`-joined link list at panel bottom | Not attached to any specific claim; 10% point at homepages (§4.3) |
| **Time window** | — | **Nothing. No date is rendered anywhere on any page.** See §4.2 |
| **Denominator / sample** | — | Percentages appear without stated bases |
| **Confidence** | `confidence` enum + `confidence_note`, in 4 of 9 atlases | Good primitive, half-deployed, and it rates the *inputs* not the *band* |

The single sharpest observation about the current product: **the caveat is
shown only when there is nothing to caveat.** `"Absence of a marker does not
mean absence of dependency"` lives in the empty state. Click any case and it
vanishes. The boundary condition is displayed exclusively to readers who have
not yet encountered a claim.

### 2.4 Where the UI reads as the wrong genre

**Reads as dashboard, should read as atlas:**

- Filter dropdowns in a toolbar with a live result count (`"6 of 16 cases"`) is
  a data-explorer affordance. It implies the reader should slice a dataset. The
  underlying corpus is 5–16 curated cases, each individually authored. Nothing
  here needs faceted search; it needs a table of contents.
- `card-stat` pills — `16 cases`, `4 utility types`, `9 control layers` — are
  KPI tiles. They quantify the corpus, not the world. "9 control layers" is a
  fact about the schema.
- Status pills (`Active crisis`, `3 disrupted`, `Active retreat`) hand-typed
  into the splash HTML are a status board with no backing signal. The commit
  history shows these were already once removed as "decorative Live pills"
  (`986d79c`) and have re-accreted in a different form.

**Reads as documentation:** the panel's label/value stack is a spec sheet.

**Reads as notebook:** nothing, and that is a genuine strength — there is no
"here is my analysis pipeline" residue anywhere.

**Reads as atlas, correctly:** the U.S. overlay mode. Showing "geography of
consequence" in red against "geography of control" in dashed cyan, on the same
frame, is the one moment in the entire product where the *composition itself
carries the argument*. It is the best idea in the codebase and it is used in
one of nine atlases.

### 2.5 The composition problem

Nine of nine pages are `map + inspector`. That layout makes one implicit
promise: *the geography is the point, and the panel annotates it.*

For `us/` that promise is true. For `chokepoints/` it is true — narrow water is
literally the subject. For `hormuz/`, `insurance/`, and `fertilizer/` it is
**false and actively misleading**: a choropleth paints an ordinal severity band
across a country's full land area, so Bangladesh's stress reads as a smaller
claim than Australia's would, and the visual weight of each claim is set by
national land area rather than by anything in the data. For `cloud/` and
`subsea/`, the map is close to decorative — "AWS us-east-1" as a dot in
Virginia carries almost no information that the sentence beside it does not.

The map is the composition because the map was the first thing built, not
because nine subjects all turned out to be cartographic.

---

## 3. Content and evidence model

### 3.1 Is the content structured enough to support an editorial renderer?

**Yes for the spine; no for the argument.** Every feature reliably carries
`title`, `one_line`, `sources[]`, and a category enum. That is enough to
generate: a page title, a thesis line, a claim list, and a receipts section —
i.e. rungs 1 and 4 of the target hierarchy — for all 85 features, today, with
no re-authoring.

What is *not* structured: everything between them. The middle of every case is
2–5 free-prose paragraphs (`trigger`, `public_consequence`, `dependency`,
`consequence`, `who_controls`, `current_status`, `mitigation`) whose field names
differ per atlas and whose epistemic status is uniform-by-omission.

**Reproducibility is not at risk from a renderer change** — there is nothing
generated to reproduce. Every artifact is hand-authored. A renderer can only
improve this position, because a renderer creates the first derived layer and
therefore the first thing a check can verify.

### 3.2 Where provenance is machine-readable

**Machine-readable today:** `sources[].publisher`, `.url`, `.date`;
`confidence` enum (4/9 atlases); `date_surfaced` (1/9 atlases); `status` enum.

**Trapped in prose:** the actual evidentiary basis. `confidence_note` —
`"Citizens data public; depopulation program documented; ProPublica
investigation on arbitration"` — is three receipts, three claim types, and one
retrieval caveat compressed into a semicolon-delimited string that no tool can
read. Every atlas has a dozen of these. This is the highest-yield structuring
target in the corpus: the information already exists and is already correct;
it is only unparseable.

**Absent entirely:** retrieval date (when *we* looked), archive URL, the quoted
or paraphrased basis, and any binding of a specific source to a specific claim.
A case with two sources and five prose paragraphs offers no way to know which
sentence rests on which document.

### 3.3 Do the natural distinctions exist in the material?

They exist in the *content* and are erased by the *schema*. Taking Hormuz /
Philippines as the specimen:

| Brief's category | Present? | In the data as |
|---|---|---|
| **Observation** | yes | `hormuz_oil_pct: 92`, `reserve_days: 45`, `gen_fossil_pct: 76` |
| **Derived metric** | yes, **undeclared** | `stress_band: already_stressed` — from what, by what rule, unstated |
| **Interpretation** | yes, **unmarked** | `rationing_capacity: "Low. Limited state capacity…"` |
| **Claim** | yes | `one_line` |
| **Caveat** | partial | `confidence_note`, prose, page-level only |
| **Source / provenance** | yes, weak | `sources[]`, unbound to claims |
| **Time window** | **no** | `current_status` is present-tense with no as-of |
| **Denominator / sample** | **no** | "92% of oil" — of imports? of consumption? by volume or value? |
| **Confidence / status** | yes, 4/9 | `confidence` + `status` |

Three of nine dimensions are missing outright; two more exist but are not
distinguished from their neighbours. Crucially, **no new research is needed for
five of them.** Observation/derived/interpreted is a re-typing of fields that
already exist. Time window is derivable from `max(sources[].date)` today.

### 3.4 The sibling repo already solved this

`intake-composition-atlas/schema.yaml` defines, and `tools/lint.py` enforces:

- **Four claim types** — `documented` (a public record states it),
  `authorized` (a legal instrument permits it, no evidence it occurs),
  `inferred` (composition makes it derivable; **requires** a non-empty
  `derivation` naming parent claims; depth-1 cap), `speculative` (incentive
  analysis only; excluded from default view; max 2 per case).
- **Receipts as first-class files** — `receipts/<id>.yaml` with `kind`, `url`,
  `archived`, `retrieved` (required), and `basis` (paraphrase + pinpoint cite).
  Shared across claims. `id` referenced, never inlined.
- **Eligible-receipt-kind gating** — a `documented` claim cannot rest on a
  statute; third-party journalism is explicitly "leads-only, never
  `agency_statement`."
- **`contestation` blocks required** on the edge types where standing matters.
- **Staleness windows** — 90 days for observed artifacts, 365 default; linter
  warns.
- **Build refuses on lint error.** Proposal-only: writes data, never commits.

And it renders that discipline: the splash carries a **"What this refuses to
claim"** block and a four-swatch claim-type key *above* the cases.

That is the target evidence model, already ratified, already enforced, in the
same author's hand, one directory over. The grid atlas should not invent a
second one.

The gap in the other direction is real too: the intake atlas hides its method
behind `<details class="method"><summary>What this is, precisely</summary>` —
progressive disclosure applied to exactly the content the brief says must stay
visible.

---

## 4. Aging and inconsistency

Separated deliberately into **product debt** (costs the reader something) and
**harmless age** (costs nothing; leave it).

### 4.1 Product debt — evidence integrity

**(a) `stress_band` has no stated derivation. Three atlases, 30 features.**

The dominant visual encoding of `hormuz/`, `insurance/`, and `fertilizer/` — the
thing that colors the map — is an ordinal severity band assigned per feature.
There is no formula, threshold table, input list, or methodology note anywhere
in the repo or on the site. `confidence_note` rates the *inputs*; nothing rates
the *assignment*. A reader looking at five stress bands across twelve countries
cannot learn what separates band 2 from band 3.

This is the most visually assertive claim on the site and the least documented
one. It is a `derived` claim presented in the register of an observation.

**(b) 15 of 16 U.S. cases have divergent YAML and GeoJSON prose.**

`REFRESH.md` flags this as affecting three cases. Measured, it affects fifteen,
and the divergence is not formatting:

```
toledo  YAML: "...governed by regulators with no authority over
               non-point agricultural pollution..."
        GEO : "...governed by regulators with no non-point-source authority..."

uri     YAML sources: [FERC, Texas Comptroller, KUT Radio (Austin NPR)]
        GEO  sources: [FERC, Texas Comptroller]
```

The GeoJSON is a separately hand-condensed edit of the YAML. **The published
copy is the lossy one, and in at least one case it silently drops a source.**
Two hand-maintained parallel copies of the same evidence, diverging, with no
check. This is the worst structural problem in the repo.

**(c) `docs/data/` is a stale orphan that contradicts its own documentation.**

`REFRESH.md` calls `docs/data/cases.geojson` "byte-identical" to `us/data/`.
It is not, and has not been for some time: it has 15 cases to `us/`'s 16
(missing DOE 202(c)) and carries superseded prose for Tahoe, PJM spillover, and
Potomac. Nothing loads it. It is 44KB of publicly-served, wrong, older evidence.

**(d) 10% of citations point at a homepage, not a document.**

18 of 177. Concentrated: **insurance 7/12, subsea 9/18.** `ProPublica →
propublica.org`, `NPR → npr.org`, `UN News → news.un.org`, `The Register →
theregister.com`. These are attributions, not citations — they cannot be
checked, and they will never 404, which makes them invisible to link-checking.

**(e) Link rot is beginning.** A 42-URL sample (25% of unique citations):
1 hard 404 (`wabe.org`), 1 connection failure (`docs.nrel.gov`), 1 rate-limit,
7 bot-blocks (403/401 — Reuters, FERC, IEA, NRDC; likely live for humans). No
`archived` field exists anywhere, so nothing degrades gracefully.

### 4.2 Product debt — the site cannot say when

**No date is rendered anywhere, on any page, in any state.** Not a build date,
not a source date, not a review date. `date_surfaced` exists in the U.S. data
and is never displayed.

Meanwhile:

- Hormuz says `"Declared national energy emergency"` in present tense; its
  newest source is **141 days old**.
- The splash hand-types `Active crisis`, `3 disrupted`, `Active retreat`,
  `Active shortage` as static strings.
- Grid-equipment's newest source is **317 days old**; cloud's, 256.

`REFRESH.md` deferred `freshness-render` on the correct principle — "a
freshness stamp that isn't refreshed is worse than no stamp." But the
conclusion drawn was wrong. The honest stamp is not `last_reviewed` (which
requires discipline the project doesn't have); it is **`max(sources[].date)`**,
which is 100% derivable from committed data today, cannot drift, and cannot
overstate. "Evidence current to 2026-03-26" is both true and useful. The
deferral blocked the wrong artifact.

### 4.3 Product debt — structure

**(f) Nine-way fork with no trunk.** 129 identical CSS lines and 66 identical JS
lines per page × 9. Any fix — the a11y gaps below, a date stamp, a caveat that
survives selection — must be applied nine times or not at all. This is why the
overlay idea (the best thing in the product) exists in exactly one atlas.

**(g) Accessibility.** Per page: **zero** `<label for>` (filter `<label>`
elements are not associated with their `<select>`s), zero `alt`, zero
`<noscript>`, exactly one `aria-` attribute (the mobile close button), and one
`<h2>` — which is populated by JS, so the document outline is empty until a
click. The MapLibre canvas is the entire content surface with no text
alternative. Drag-to-dismiss is touch-only with no keyboard equivalent. Nothing
renders without JS: a reader with JS disabled, or a crawler, sees a header and
three empty dropdowns.

**(h) The `stress_band` choropleth is the wrong mark** (§2.5). Ordinal severity
on country polygons encodes magnitude as land area.

**(i) Overlay polygons are authored geometry in an observed register.** 32
hand-drawn polygons, median 11 vertices, representing things like "NV Energy
service territory" and "PacifiCorp 6-State Service Territory." They sit on a
survey-grade basemap in the same visual layer as real coastlines. The caveat
("Boundaries are approximate") is 11px italic, and it renders only when an
overlay is on screen. The polygons are a legitimate *derived/illustrative*
claim; the presentation does not say so.

### 4.4 Harmless age — leave it

- **`maplibre-gl@4.1.2`** (latest 6.3.0, two majors behind). It works. Nothing
  in the atlas uses anything 5.x or 6.x added. Version-chasing buys nothing.
  *But:* pin + vendor it locally, because unpkg with no SRI and no fallback is
  an availability and integrity risk for a site whose entire claim is
  auditability. Vendor at 4.1.2, don't upgrade.
- **Inline `<style>`/`<script>`** — correct for a no-build site; the problem is
  duplication, not inlining. Extraction to shared files fixes it without adding
  a bundler.
- **`SYNTHESIS.md` marked "Draft. Not for publication. March 2026."** — an
  honest working document, correctly labeled, doing its job. Not debt.
- **The `cases/*.yaml` schema itself.** Nine control layers over 16 cases,
  extended once, deliberately. Sound.
- **No `.nojekyll`.** Costs nothing today. Add it when a `_`-prefixed path
  appears.
- **`PROVENANCE.md` dated 2026-03-27.** Says what it is. Refresh when the
  authorship story changes, not on a timer.
- **Missing `og:url` on four pages, `og:url` pointing at the root from `us/`.**
  Cosmetic; fix in passing, don't schedule.

---

## 5. Reference-site analysis — `strategicallyempty.com`

A single-question site: *when does the U.S. Strategic Petroleum Reserve hit
zero?* Linear scroll, twelve sections, no navigation menu.

### 5.1 What makes it work

1. **The headline is the answer, not the topic.** `"The U.S. Strategic
   Petroleum Reserve will run dry on … days from today."` — a falsifiable claim
   in the H1 position, with the number in it.
2. **One question governs every section.** Twelve sections, all answering
   sub-questions of the same question. Nothing is present because it was
   available.
3. **Section titles are findings.** `"From 2019 to zero"`, `"The cliff, up
   close"`, `"How fast is it draining?"` — each names what the chart shows
   before you look at it.
4. **Annotation replaces interaction.** `"At the peak of the crisis the reserve
   was losing nearly 10 million barrels a week."` sits on the figure. No hover
   required. `"Every previous emergency shows up as a barely visible dent"` —
   the caption tells you what to see in the shape, then names Desert Storm,
   Katrina, Libya on the marks.
5. **The method is a visible section with a real title.** `"Methodology &
   honesty"` — not a footnote, not a `<details>`, not a tooltip. It opens with
   the actual formula in one sentence: *"current SPR level ÷ average draw over
   the last four weekly reports, projected forward from the latest report date.
   Nothing more."*
6. **The caveat is quotable.** `"This is a countdown, not a prophecy."` The
   limit of the claim is stated as memorably as the claim.
7. **Measurement and projection are visually distinct.** Solid lines for EIA
   weekly reports; dashed red for extrapolation. Observed and derived do not
   share an ink.
8. **Sources are identified precisely enough to re-run.** `"EIA series
   EMM_EPMR_PTE_NUS_DPG"` plus API endpoints — not "EIA."
9. **Restraint under pressure.** Black, white, red, one dashed line. A doom
   countdown rendered without a single red-alert affordance. The gravity comes
   from the number.
10. **Depth is stacked, not hidden.** Skim the top metrics; read the section
    titles; read the captions; read the method; open the data table. Each layer
    is on the page, in order, and none is behind a control.

### 5.2 Borrow

Claim-in-the-H1 · one governing question per page · findings as section titles ·
on-figure annotation instead of tooltips · methodology as a titled visible
section opening with the formula · a quotable limit-of-claim · distinct ink for
measured vs projected · precise-enough-to-re-run source identity · stacked
depth · restraint.

### 5.3 Do not borrow

- **The countdown / live-ticker device.** It works because one deterministic
  arithmetic operation on one weekly government series drives it. The atlas has
  no such series; a ticker would be theater. (`986d79c` already removed
  decorative "Live" pills once — the same instinct.)
- **The single-page monolith.** SPR is one subject. The atlas is 85 cases
  across 9 substrates; it needs a corpus structure, not one long scroll.
- **The specific palette and type.** Light ground, red/white/black. The atlas's
  dark ground and six-hue semantic palette are already good and already coherent.
- **Its uncertainty posture.** "No confidence intervals; the calculation is
  deterministic" is correct for SPR and wrong for the atlas, where the central
  quantities are judgments. The atlas needs *more* uncertainty apparatus than
  the reference, not the same amount.
- **The subject-driven fatalism.** "Runs dry on date X" is a legitimate frame
  for a depleting reserve. Structural dependency has no zero date.

### 5.4 Nearer reference, in-family

`intake-composition-atlas/docs/index.html` already implements six of the ten
borrowables: kicker → serif claim-headline → dek → three-beat mechanism figure →
**"What this refuses to claim:"** → four-swatch claim-type key → cases → method.
`"You can see the form. You can't see the join."` is exactly the H1-as-claim
move. The grid atlas splash, next to it, is a card grid.

The migration target is closer than it looks. It is largely *"apply the sibling
repo's grammar to the larger corpus"* — not an invention.

---

## 6. Verdict

**What is working and must be preserved:** the thesis and its cross-substrate
discipline; the nine-layer `control_layer` taxonomy; the dark semantic palette;
the overlay idea (consequence vs. control on one frame); the editorial voice in
`one_line` and the case prose; `SYNTHESIS.md` as the authored argument; the
`confidence` + `confidence_note` primitive; the explicit handoff-to-specialists
posture; `REFRESH.md`'s primitive decomposition.

**What is broken, in priority order:**

1. Two diverging hand-maintained copies of the U.S. evidence (§4.1b), plus a
   third stale orphan copy being served (§4.1c).
2. The primary visual claim of three atlases has no stated derivation (§4.1a).
3. The site cannot say when anything was true (§4.2).
4. Caveats are shown only in the absence of claims (§2.3).
5. Nine-way fork prevents any fix from landing once (§4.3f).
6. Provenance is unbound to claims, 10% uncheckable, 0% archived (§4.1d–e).
7. The map is the default composition for subjects that are not cartographic
   (§2.5).

**The through-line:** this is an *evidence* project rendered in an *explorer*
grammar. The explorer grammar makes claims easy to display and hard to
qualify — so the qualifications went into the empty state, the derivations went
nowhere, and the dates went missing. The redesign is not cosmetic. Fixing the
grammar is what makes the evidence sayable.

Proposed grammar: [ATLAS-DESIGN-GRAMMAR.md](ATLAS-DESIGN-GRAMMAR.md).
Path: [ATLAS-MIGRATION-PLAN.md](ATLAS-MIGRATION-PLAN.md).
