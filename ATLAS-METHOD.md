# Atlas publication QA loop

**2026-08-14.** How the three migrated atlases were produced, and why the
process is worth keeping. Companion to [ATLAS-REVIEW.md](ATLAS-REVIEW.md),
[ATLAS-DESIGN-GRAMMAR.md](ATLAS-DESIGN-GRAMMAR.md) and
[ATLAS-MIGRATION-PLAN.md](ATLAS-MIGRATION-PLAN.md).

This is not a redesign process. It is a publication QA loop that happens to
produce pages.

---

## The loop

```
corpus audit  →  build the page  →  cold read  →  repair  →  encode the
                                                            recurrence as an
                                                            invariant
```

1. **Corpus audit.** Mechanical, before any design decision. Field coverage,
   nulls, semantic consistency of numeric fields, citation targets, source
   dates, prose claims against the structured record. Scripts, not impressions.
2. **Build the page.** Overbuilt on purpose: make every gap the audit found
   visible, and accept that this overshoots.
3. **Cold read.** A reader who has not seen the corpus, the repository, or the
   previous atlas. See below — this is the stage that carries the loop.
4. **Repair.** Fix what the cold read found, including the parts that are
   embarrassing.
5. **Encode the recurrence.** If the same class of mistake appears twice, it
   stops being a lesson and becomes a check that fails the build.

---

## Why the cold reader is the load-bearing stage

> **The cold reader isn't there merely to catch old defects. It catches defects
> introduced by the repair itself.**
>
> Audit without adversarial rereading just gives you a more sophisticated way to
> be confidently wrong.

Every specimen in this project acquired *new* defects during the pass that was
fixing its old ones. Not typos — claims:

- The Hormuz reserve chart put seven figures on one axis against one 60-day
  reference line while its own caption explained that five of them counted
  different quantities. The prose disclaimed the comparison; the picture kept
  making it, and the picture wins.
- The insurance page opened by stating the corpus "never records what period
  either number covers," then said sixty lines later that Colorado's prose gives
  "over 6 years (2019–2024)." It also ran a section headed "Most of these
  numbers are not in the corpus" about numbers that are in the corpus, in prose,
  and labelled a current count plus an undated peak "the one real series."
- The cloud timeline's caption said event bars were "drawn to the longest
  duration their own prose states." Every bar was hardcoded to the same width.
  That figure's entire thesis was *do not visually claim more than the evidence
  supports.*

None of these were caught by the author. All were caught immediately by a
reviewer with no investment in the implementation's internal story, who simply
observed that the caption said one thing and the pixels said another.

**Practical requirements.** The reviewer must not be told what is being hunted —
no mention of registers, epistemics, the atlas, or prior failure modes. Rotate
both the model and the question wording between runs; a reviewer that has seen
the shape twice is no longer cold. Ask for a first-time reader's summary, what
they will remember tomorrow, where the page asserts more than it supports, what
reads as implementation rather than subject, and any internal contradiction.

---

## The recurring failure this project has

Named because it appeared three times and will appear again:

> Discover an epistemic defect → build immaculate apparatus for describing the
> defect → leave the actual subject unrendered in the corpus.

Concretely: Hormuz shipped a first draft with `current_status` rendered for
**0 of 12** countries. Insurance shipped with `insurer_exits`,
`regulatory_response` and `mortgage_impact` all at **0 of 6**. Both pages
described the *shape* of their corpus in detail while omitting what the corpus
said about the world.

This is now a build failure. `atlas_core.require_subject_fields()` fails any
build in which a substantial prose field renders for zero records. On its first
run it caught three further suppressed Hormuz fields (`alternative_supply`,
`gen_mix_summary`, `rationing_capacity`) and three in cloud, before a human saw
either page.

A field may legitimately be partially rendered — quoting five of twelve is an
editorial choice. Zero is different: zero means the corpus said something and
the page never repeated it.

---

## Evidence that the loop finds real defects rather than applying one critique

Three atlases produced three unrelated failure classes. The third could not
have been the first two in disguise: cloud has no numeric fields at all.

| Atlas | Defect class | Shape of it |
|---|---|---|
| **Hormuz** | **Missingness** concealed by confident presentation | Five of twelve countries publish no reserve figure; the choropleth painted all twelve identically. `reserve_days` also meant different things per row — strategic oil, foreign-owned storage, a range flattened to a point. |
| **Insurance** | **False comparability** — the field name lies | `rate_change_pct` is one column with six semantics. Louisiana records "highest rate increase in the nation: 58%"; Colorado records "highest cumulative rate increase in the nation: 76.6% over 6 years." Both are true only if they measure different things, which the corpus never says. |
| **Cloud** | **Tense collapse** — time absent from the schema | Four cases are events that ended (49 minutes, 7 hours, 15 hours); six are conditions that persist. No date field exists. `severity: demonstrated \| structural` is an evidential-mode axis wearing a magnitude's name, and it inverts: the structural claims are more consequential and less directly demonstrated. |

A fourth atlas may well produce a fourth class. That is the point of running it
again rather than assuming the taxonomy is closed.

---

## What the loop is not for

- **It is not a refresh.** It finds defects in how a corpus represents itself,
  not in whether the corpus is current. Stale sources, dead links and figures
  that disagree with their own citations are a separate workstream, and holding
  a migration until that workstream finishes couples two unrelated jobs.
- **It does not rewrite case prose.** Every specimen reproduces the corpus's
  editorial voice verbatim. Where a page found a prose figure it could not
  verify, it said so and left the figure alone.
- **It does not impose a page shape.** `atlas_core` shares mechanism only. The
  three migrated atlases have three different compositions: Hormuz turns on
  missing measurement, insurance opens on a contradiction, cloud is a timeline
  with no map at all. If a fourth wants the same shape as one of these, that is
  the moment to consider promoting shape — not before.
