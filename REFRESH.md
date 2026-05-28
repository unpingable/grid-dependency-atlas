# Atlas Refresh Workflow

**Draft. Framing doc, not a ratified process. 2026-04-22.**

Names the refresh workflow for this atlas today, names the primitives that
future tooling would operate on, and pins the constraints any automation
must respect.

Adopts by reference the doctrine in `~/git/agent_gov/docs/document_registers.md`
(brutalist/operating split) and `visual_registers.md` (state wins; refusal
visible; compress, don't widen).

## Why this exists

The atlas is human-curated. Cases age. Stats drift. The splash and README
carry hand-edited counts that need to match the underlying GeoJSONs. Today
the only enforcement is human attention, and known drift already exists.

A refresh workflow doc is the first step toward shifting enforcement into
tooling without losing the governance boundary — humans ratify cases and
editorial claims; tooling cannot publish claims the evidence doesn't support.

## Source-of-truth graph

**Authoritative (source):**

- `docs/<atlas>/data/<name>.geojson` — canonical per-atlas dataset.
  One file per atlas (US has two: `cases.geojson` + `overlays.geojson`).
  Filename is not uniform across atlases:
  - Point atlases: `cases.geojson` (us, cloud, subsea, grid-equipment, water)
  - Region atlases: `countries.geojson` / `states.geojson` / `chokepoints.geojson`
    (hormuz, fertilizer, insurance, chokepoints)

**Derived (should be generated, not authored):**

- `docs/<atlas>/index.html` — per-atlas case counts, empty-state text,
  legend totals. Currently hand-edited; this is the drift surface.
- `docs/index.html` — splash cards: case counts, category counts, stat pills.
- `README.md` — atlas table: case counts per row.

**Editorial (human-authored, not derivable):**

- Per-case `title`, `one_line`, `dependency`, `consequence`, etc. in GeoJSONs.
- Atlas subtitles, thesis lines, splash description copy.
- `SYNTHESIS.md`, `TAXONOMY.md`, `CASES.md`, `PROVENANCE.md`.

The refresh workflow governs the **source → derived** edge. Editorial
content is out of scope.

## Manual refresh (current)

To update one atlas:

1. Edit `docs/<atlas>/data/*.geojson`. Keep schema consistent across
   Features — the JS reads property names directly.
2. Update hardcoded counts in `docs/<atlas>/index.html` (placeholder copy,
   empty-state text, occasionally legend totals).
3. Update splash card in `docs/index.html` (`card-stat` spans for that atlas).
4. Update `README.md` atlas table row for that atlas.
5. Commit and push to `main`. GitHub Pages rebuilds from `/docs`.

**Known drift as of 2026-04-22:**

- Fertilizer count: splash says `11 countries`, README says `12 countries`.
  One or both is wrong.
- No check for schema divergence across Features within a single GeoJSON.

## Primitives

Small units a tool could operate on independently. Each has a clear input,
clear output, and clear failure mode.

### `count-derive`
- **Input:** a per-atlas GeoJSON
- **Output:** total count, category counts, severity counts
- **Consumed by:** splash card, README row, atlas placeholder copy
- **Failure mode:** GeoJSON unreadable or missing

### `schema-check`
- **Input:** a per-atlas GeoJSON
- **Output:** list of property keys missing from any Feature vs the modal
  schema; list of Features with extra keys
- **Failure mode today:** silent inconsistency

### `drift-check`
- **Input:** repo working tree
- **Output:** list of places where derived values disagree with source
  (splash count != GeoJSON feature count, README vs splash mismatch, etc.)
- **Runs:** pre-commit candidate; scheduled-check candidate

### `splash-generate`
- **Input:** manifest of atlases (name, route, tag color, counts, world-state
  label if any)
- **Output:** the cards block in `docs/index.html`
- **Failure mode today:** hand-edits drift from data

### `readme-atlas-table`
- **Input:** same manifest + per-atlas scope line
- **Output:** the atlas table block in `README.md`

### `freshness-render` (deferred)
- **Requires:** per-case `last_reviewed` or per-atlas `last_reviewed` in GeoJSONs
- **Output:** visible timestamp in the UI
- **Blocked on:** the tooling that actually keeps `last_reviewed` honest.
  Adding the field without keeping it fresh would be a rule-#2 widening
  — visual state not mapped to real state.

## Doctrine constraints (non-negotiable)

From the visual-registers doctrine:

1. **Automation cannot widen claims the evidence doesn't support.** A
   freshness stamp that isn't refreshed is worse than no stamp. A count
   generator that silently skips malformed Features is worse than a broken
   build.
2. **Refusal must remain visible.** If a check fails, the tool surfaces
   the failure on the next edit path — not buries it.
3. **Proposal-only by default.** Automation prepares diffs; humans ratify.
   No auto-commit of atlas content changes. Derived/generated classes
   (counts from GeoJSON) can be auto-applied safely; editorial claims
   cannot.
4. **GeoJSON is source-of-truth.** Generated splash and README are
   subordinate renderings. If they disagree with GeoJSON, they are wrong.

## Nightshift hooks (future)

`~/git/scheduler` / nightshift is currently geared toward alert workflows
via nq, not arbitrary scheduled tasks. When arbitrary scheduling arrives,
the natural atlas hooks would be:

- **Scheduled `drift-check`** — daily or weekly. Surfaces divergence as an
  alert. No write access to the repo.
- **Scheduled source-polling (later, Governor-integrated)** — check primary
  sources for per-case updates; prepare proposal diffs for human review.
  Requires Governor's proposal-only pipeline to exist first.

Not in scope yet. This doc exists so that when the tooling is ready, the
atlas-side workflow is already named and the primitives are already named.

## Out of scope

- Editorial content (thesis lines, subtitles, per-case prose).
- Visual design of the atlas pages.
- The GeoJSON schema itself — that's TAXONOMY / case schema work.
- Running the tooling. This doc describes the workflow a tool would
  implement. It does not implement it.
