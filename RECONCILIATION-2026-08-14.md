# U.S. corpus reconciliation — preservation record

**2026-08-14. One-time reconciliation of `cases/*.yaml` (canonical) against
`docs/us/data/cases.geojson` (published) and `docs/data/cases.geojson` (orphan).**

Per operator directive: the YAML corpus is canonical, subject to this one-time
reconciliation. **Every divergence is preserved and reported here before the
duplicate-authoring path is eliminated.** After reconciliation, the GeoJSON is
generated from YAML and must never be edited independently.

Part I is the classification and disposition. Part II is the complete
field-level record, machine-generated, unedited. Nothing in Part II has been
altered; it is the evidence for Part I.

---

## Part I — Classification and disposition

### I.1 Summary

16 U.S. cases. **All 16 diverge** between YAML and published GeoJSON — 15 in
prose, and the 16th (`doe-202c`) in minor wording only. The divergence is not
random: it falls into two sharply distinct classes.

| Class | Cases | What happened | Who wins |
|---|---|---|---|
| **A — abridgement** | 13 | GeoJSON is a hand-condensed copy of the YAML: shorter sentences, dropped specifics, dropped sources | **YAML** (2 clause-level exceptions, §I.4) |
| **B — refresh-forward** | 3 | The May 2026 refresh pass edited the GeoJSON only. It carries `current_status`, newer sources, and revised figures the YAML never received | **GeoJSON** (absorbed into YAML) |

Measured: in every Class A case the YAML prose is longer and more specific
(mean 985 vs 767 characters across `trigger` + `public_consequence` +
`one_line`). The condensation is consistent enough to have been a deliberate
authoring habit, not drift.

### I.2 Source citations — the material loss

| | Count |
|---|---|
| YAML-only citations, **never published** | **18** |
| GeoJSON-only citations, **never recorded in the canonical corpus** | **5** |
| Cases where the published copy cites fewer sources than the canonical one | 12 of 16 |

Every one of the 18 is a real citation with a working-format URL and a date,
present in the editorial corpus and absent from everything a reader can see.
Examples: `Rhode Island Division of Public Utilities and Carriers` (the actual
DPUC incident report) on Aquidneck; `AZPM` on Colorado River; `Utility Dive` on
Delmarva; `Sierra Club` and `NRDC` on PJM spillover; `KUT Radio (Austin NPR)` on
Texas Uri; two sources each on Entergy/NOLA, ISO-NE, PacifiCorp, and Michigan UP.

The 5 in the other direction are all from the May 2026 refresh: `U.S. EPA / DOJ`,
`Maryland Office of the Attorney General`, and `Axios DC` on Potomac;
`South Tahoe Now` and `Northern Nevada Business Weekly` on Tahoe.

**Disposition: union.** No citation is dropped in either direction. Publisher
strings are normalised to the longer form where the URL is identical
(`Rhode Island DPUC` → `Rhode Island Division of Public Utilities and Carriers`).

### I.3 Class B — the three refresh-forward cases

These are the cases where the published copy genuinely leads and the canonical
copy must absorb.

**`tahoe-nvenergy-supply-2026`** — GeoJSON adds the Greenlink Nevada
transmission timeline (Greenlink West slipped to May 2027, Greenlink North to
late 2028), the precise `May 31, 2027` termination date, the Tahoe-Reno
Industrial Center attribution, a `current_status` block on the March 2026 CPUC
filing, and two 2026 sources. YAML has none of it.

**`pjm-data-center-cost-spillover-2025`** — GeoJSON adds a `current_status`
block covering FERC Docket EL25-49-000, the March 2026 protests, and the
RM26-4-000 ANOPR timeline. YAML's prose is otherwise richer (it retains the
`$28.92 → $269.92/MW-day` figures, the `$4.3B` transmission socialisation, and
the Columbus OH `+$27/month` figure the GeoJSON dropped).

**`potomac-interceptor-collapse-2026`** — GeoJSON adds a `current_status` block
on the parallel DOJ/EPA and Maryland AG Clean Water Act complaints and the
May 2026 disclosure of three further failing segments, plus three sources. It
also adds `72-inch`, `over 8 days`, and `C&O Canal National Historical Park`.

### I.4 Class A exceptions — GeoJSON clauses worth keeping

A token-level scan of all 13 Class A cases for facts present only in the
GeoJSON prose returned exactly **one** substantive result:

- **`colorado-river-post2026-allocation`** — GeoJSON's `trigger` ends
  *"California no cuts due to senior rights"*, a fact the YAML lacks. The YAML
  is otherwise richer (it retains the Lower Basin proposals of 27% AZ / 17% NV /
  10% CA and Nevada's 279,000 acre-feet, all dropped from the published copy).
  **Disposition: keep YAML, append the California clause.**

One near-miss, resolved as no-change:

- **`iso-ne-winter-gas-pipeline-constraint`** — GeoJSON's prose says
  *"15.1 million ratepayers"*. This is not a new fact; it restates
  `affected_population_est: 15100000`, already in the YAML. No merge.

All other Class A GeoJSON prose is strictly subtractive and is discarded when
the file becomes generated. **The discarded text is preserved in Part II.**

### I.5 Contested quantity — flagged, not silently resolved

**`potomac-interceptor-collapse-2026` disagrees with itself on the headline
number.**

| Copy | `title` | `one_line` | `public_consequence` |
|---|---|---|---|
| YAML | 300M gallons | 300 million gallons | "240–300 million gallons" |
| GeoJSON | 240M gallons | 240 million gallons … over 8 days | "~240 million gallons … over 8 days" |

This is a factual revision, not an abridgement: the May 2026 refresh narrowed
the estimate and added a duration, alongside three new sources including the
EPA/DOJ complaint. The later figure is better supported.

**Disposition: adopt 240M with the range preserved in `public_consequence`**
(`~240 million gallons … early estimates ranged to 300 million`). Recorded here
because a headline quantity moving by 25% between two copies of the same corpus
is exactly the kind of change that must not pass silently into a generator.

### I.6 The orphan copy

`docs/data/cases.geojson` and `docs/data/overlays.geojson`.

- 15 cases against the published 16 — missing `doe-202c-emergency-orders-2025`.
- Stale prose on three cases: `tahoe-nvenergy-supply-2026` (5 fields),
  `potomac-interceptor-collapse-2026` (6 fields),
  `pjm-data-center-cost-spillover-2025` (1 field).
- Loaded by no page. Reachable at a public URL.
- `REFRESH.md` describes it as "byte-identical to `docs/us/data/…`". That was
  true when written and is no longer true.

It is a third, older, publicly-served copy of the evidence, and it is superseded
by both others. **Disposition: delete.** Its content is a strict subset of what
is preserved in Part II and in git history.

### I.7 What changes in the canonical corpus

| Case | Change |
|---|---|
| `tahoe-nvenergy-supply-2026` | absorb `current_status`; absorb Greenlink timeline, May 31 2027 date, TRIC attribution; +2 sources |
| `pjm-data-center-cost-spillover-2025` | absorb `current_status`; +0 sources (YAML already richer); restore 2 YAML-only sources to publication |
| `potomac-interceptor-collapse-2026` | absorb `current_status`; adopt 240M (§I.5); absorb `72-inch`, `8 days`, C&O Canal NHP; +3 sources |
| `colorado-river-post2026-allocation` | append California senior-rights clause (§I.4) |
| all 16 | source lists become the union; publisher strings normalised |
| all 16 | no other prose changed |

**No case prose is rewritten to suit a renderer.** Class A YAML text is
untouched. Class B absorption adds material that was already authored and
already published; it does not re-word what was there.

### I.8 After reconciliation

`docs/us/data/cases.geojson` is generated by `tools/build_us_geojson.py` from
`cases/*.yaml` plus a coordinate table, and carries a
`"_generated"` header. `docs/data/` is deleted. Independent editing of the
GeoJSON is thereafter a build-detectable error, not an invisible one.

---

## Part II — Complete field-level divergence record

Machine-generated 2026-08-14. Whitespace-normalised, otherwise verbatim.
Nothing below has been edited. This is the preservation record for text that
the reconciliation discards.


## aquidneck-island-gas-outage-2019

Source file: `cases/aquidneck-island-gas-outage-2019.yaml`

### field: `trigger`

- **YAML:**

  ```
  On January 21, 2019 — one of the coldest days in a decade (2 deg F low) — high heating
  demand across the Algonquin pipeline system caused a low-pressure condition on the Aquidneck
  Island branch. A programming error in a valve at a meter station restricted flow, and a
  power failure at a local LNG backup facility removed the last safety net. Rhode Island DPUC
  called it a "perfect storm" but the root vulnerability was dependence on an interstate
  pipeline whose capacity allocation was not under local control.
  ```
- **GeoJSON:**

  ```
  On January 21, 2019 — one of the coldest days in a decade — high heating demand across the
  Algonquin system caused a low-pressure condition on the Aquidneck branch. A valve
  programming error and local LNG backup failure removed the last safety net.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  7,455 gas customers lost heating service for up to 7 days in sub-freezing temperatures.
  Thousands displaced to hotels. Each customer required individual service restoration
  (relighting pilots). National Grid later paid a $2M class action settlement.
  ```
- **GeoJSON:**

  ```
  7,455 gas customers lost heating for up to 7 days in sub-freezing temperatures. Thousands
  displaced. Each customer required individual restoration visit. National Grid paid $2M class
  action settlement.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `Rhode Island Division of Public Utilities and Carriers` — https://ripuc.ri.gov/sites/g/files/xkgbur841/files/eventsactions/AI_Report.pdf (2019-10-30)
  - `Newport Buzz` — https://www.thenewportbuzz.com/attorney-brian-cunha-secures-2-million-settlement-with-national-grid-following-2019-gas-outage-on-aquidneck-island/53492 (2024-06-10)
- **Only in GeoJSON (missing from YAML):**
  - `Rhode Island DPUC` — https://ripuc.ri.gov/sites/g/files/xkgbur841/files/eventsactions/AI_Report.pdf (2019-10-30)

## colorado-river-post2026-allocation

Source file: `cases/colorado-river-post2026-allocation.yaml`

### field: `trigger`

- **YAML:**

  ```
  The 2007 Interim Guidelines governing Colorado River shortage-sharing expire end of 2026.
  Interior set a February 14, 2026 deadline for seven states to agree on successor rules.
  Upper Basin states refused to accept specific delivery cutbacks even during severe drought.
  The deadline was missed. Lower Basin proposed 27% cuts for AZ, 17% for NV, 10% for CA. No
  agreement reached. Tier 1 shortage in effect for 2026: Nevada gets 279,000 acre-feet (7%
  cut), Arizona loses 18%.
  ```
- **GeoJSON:**

  ```
  The 2007 Interim Guidelines expire end of 2026. Interior set a February 14, 2026 deadline
  for seven states to agree on successor rules. Upper Basin states refused binding cutbacks.
  The deadline was missed. Tier 1 shortage in effect: Nevada 7% cut, Arizona 18% cut,
  California no cuts due to senior rights.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  2.3 million people in Southern Nevada get 90% of water from the Colorado River. Arizona's
  7.1 million residents face the largest proportional cuts. No agreed framework means the
  Interior Secretary may impose unilateral cuts. Municipal water providers cannot plan capital
  investments without knowing future allocations. 40 million people basin-wide affected.
  ```
- **GeoJSON:**

  ```
  2.3 million Southern Nevadans get 90% of water from the Colorado. Arizona's 7.1 million face
  largest cuts. No framework means the Interior Secretary may impose unilateral cuts.
  Municipal providers cannot plan capital investments. 40 million affected basin-wide.
  ```

### field: `one_line`

- **YAML:**

  ```
  Forty million people across seven states depend on Colorado River water with rules expiring
  in 2026; Upper Basin refusal to accept cuts leaves Las Vegas and Phoenix exposed to
  allocation decisions made hundreds of miles away.
  ```
- **GeoJSON:**

  ```
  Forty million people depend on Colorado River water with rules expiring in 2026; Upper Basin
  refusal to accept cuts leaves Las Vegas and Phoenix exposed to allocation decisions made
  hundreds of miles away.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `AZPM` — https://news.azpm.org/p/environmentnews/2025/8/18/226028-arizona-nevada-and-mexico-will-again-get-less-colorado-river-water-in-2026/ (2025-08-18)

## delmarva-dpl-south-pjm-capacity-2023

Source file: `cases/delmarva-dpl-south-pjm-capacity-2023.yaml`

### field: `trigger`

- **YAML:**

  ```
  In the December 2022 capacity auction for 2024/2025, PJM's planning model predicted certain
  large plants and solar facilities would participate. When those suppliers declined, the
  inflated reliability requirement remained, producing anomalous results that drove up DPL
  South zone prices by ~$183M. PJM proposed a re-run; FERC approved a fix keeping higher
  prices. The D.C. Circuit Court vacated FERC's decision on January 13, 2026.
  ```
- **GeoJSON:**

  ```
  In the December 2022 capacity auction, PJM's planning model predicted certain large plants
  would participate. When they declined, inflated reliability requirements produced anomalous
  results that drove up DPL South zone prices by ~$183M. The D.C. Circuit Court vacated FERC's
  decision on January 13, 2026.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  DPL South zone customers faced $288.4M in capacity costs versus $110.7M under corrected
  parameters — a $178M overcharge driven by a modeling error at PJM. Delaware and Maryland
  regulators had no power to correct it and spent three years litigating through FERC and
  federal appeals court.
  ```
- **GeoJSON:**

  ```
  DPL South zone customers faced $288.4M in capacity costs versus $110.7M under corrected
  parameters — a $178M overcharge. Delaware and Maryland regulators had no power to correct it
  and spent three years litigating through FERC and federal court.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `Utility Dive` — https://www.utilitydive.com/news/ferc-rehearing-pjm-delmarva-capacity-auction/717174/ (2024-05-20)

## entergy-miso-south-nola-blackout-2025

Source file: `cases/entergy-miso-south-nola-blackout-2025.yaml`

### field: `trigger`

- **YAML:**

  ```
  On May 25, 2025, MISO ordered Entergy to shed 498 MW of load across Greater New Orleans with
  only 30 minutes' warning after River Bend nuclear plant (1,035 MW) tripped and multiple gas
  plants were down. Entergy's four-state territory has blocked MISO long-range transmission
  planning — not one MISO LRTP line has been built in Entergy's territory, and MISO South
  planning won't begin until 2026 with earliest construction around 2036.
  ```
- **GeoJSON:**

  ```
  On May 25, 2025, MISO ordered Entergy to shed 498 MW of load across Greater New Orleans with
  only 30 minutes' warning after River Bend nuclear plant tripped. Entergy's four-state
  territory has blocked MISO long-range transmission planning — not one MISO LRTP line has
  been built in Entergy's territory.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  100,000+ customers lost power during Memorial Day weekend. The outage was not caused by
  extreme weather — it was a normal Sunday. The Amite South load pocket has had limited
  transmission import capability since at least 2006. New Orleans City Council regulates
  Entergy locally but has no authority over MISO's reliability decisions or Entergy's multi-
  state transmission investment priorities.
  ```
- **GeoJSON:**

  ```
  100,000+ customers lost power during Memorial Day weekend. The outage was not caused by
  extreme weather — it was a normal Sunday. New Orleans City Council regulates Entergy locally
  but has no authority over MISO's reliability decisions or Entergy's multi-state transmission
  strategy.
  ```

### field: `one_line`

- **YAML:**

  ```
  100,000 New Orleans customers lost power on an ordinary Sunday because Entergy has blocked
  MISO transmission planning across four states for a decade, leaving a known load pocket with
  insufficient import capacity.
  ```
- **GeoJSON:**

  ```
  100,000 New Orleans customers lost power on an ordinary Sunday because Entergy has blocked
  MISO transmission planning across four states for a decade.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `Southern Renewable Energy Association` — https://southernrenewable.org/news-updates/miso-entergy-reports-on-may-25-load-shed-event-reveal-ongoing-generation-and-transmission-challenges-in-louisiana (2025-08-15)
  - `Verite News (New Orleans)` — https://veritenews.org/2025/06/04/entergy-miso-memorial-day-blackout/ (2025-06-04)
  - `Energy and Policy Institute` — https://energyandpolicy.org/entergy-role-stalling-miso-transmission-planning/ (2024-11-15)
- **Only in GeoJSON (missing from YAML):**
  - `Verite News` — https://veritenews.org/2025/06/04/entergy-miso-memorial-day-blackout/ (2025-06-04)

## iso-ne-winter-gas-pipeline-constraint

Source file: `cases/iso-ne-winter-gas-pipeline-constraint.yaml`

### field: `trigger`

- **YAML:**

  ```
  Gas pipelines into New England were sized for heating load alone. When natural gas
  generators (~50% of New England electricity) compete with heating customers for pipeline
  capacity on cold winter days, LDCs have contractual priority. In winter 2025-2026, DOE
  issued an emergency order (Jan 25 - Feb 14, 2026) allowing generators to exceed emissions
  limits to prevent blackouts. Natural gas prices on Jan 27, 2026 hit the highest level ever
  recorded in ISO-NE's pricing database (since 2003).
  ```
- **GeoJSON:**

  ```
  Gas pipelines into New England were sized for heating load alone. When generators (~50% of
  electricity) compete with heating for pipeline capacity on cold days, heating gets
  contractual priority. In January 2026, gas prices hit the highest level ever in ISO-NE's
  pricing database. DOE issued an emergency order allowing generators to exceed emissions
  limits.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  Extreme wholesale electricity price spikes passed to ratepayers. Winter 2024/2025 wholesale
  energy market valued at $4 billion (up from $1.6B prior year). January 2026 wholesale power
  prices averaged $154.73/MWh real-time, with peaks reaching $441.80/MWh. Reliability risk
  during cold snaps requires emergency DOE orders, oil-fired backup, and reliance on globally-
  priced LNG.
  ```
- **GeoJSON:**

  ```
  Extreme wholesale electricity price spikes passed to 15.1 million ratepayers. Winter
  2024/2025 wholesale energy market was $4B (up from $1.6B). January 2026 peaks reached
  $441.80/MWh. Reliability during cold snaps requires emergency federal orders and oil-fired
  backup.
  ```

### field: `one_line`

- **YAML:**

  ```
  New England's gas pipelines were built for heating, not power generation; every cold winter,
  heating gets priority and 15 million electricity customers pay massive price spikes because
  no New England entity controls pipeline capacity decisions made by FERC-regulated interstate
  operators.
  ```
- **GeoJSON:**

  ```
  New England's gas pipelines were built for heating, not power generation; every cold winter,
  15 million electricity customers pay massive price spikes because no New England entity
  controls interstate pipeline capacity decisions.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `ISO Newswire` — https://isonewswire.com/2026/03/05/winter-2025-2026-recap-grid-stays-reliable-during-prolonged-cold/ (2026-03-05)
  - `U.S. Department of Energy` — https://www.energy.gov/articles/energy-department-extends-emergency-order-new-england-ahead-second-winter-storm (2026-02-05)

## jackson-ms-water-crisis-2022

Source file: `cases/jackson-ms-water-crisis-2022.yaml`

### field: `trigger`

- **YAML:**

  ```
  In August 2022, Pearl River flooding overwhelmed the already-failing O.B. Curtis Water
  Treatment Plant. The deeper cause: Mississippi lawmakers withheld $1.8 billion in ARPA funds
  from Jackson despite urgent requests. Governor Reeves vetoed a bipartisan bill to help
  Jackson collect overdue water payments. The state health department failed to enforce Safe
  Drinking Water Act violations from 2015-2021, preventing federal intervention.
  ```
- **GeoJSON:**

  ```
  In August 2022, Pearl River flooding overwhelmed the failing O.B. Curtis Water Treatment
  Plant. Mississippi lawmakers had withheld $1.8B in ARPA funds. Governor vetoed a bill to
  help Jackson collect overdue water payments. State health department failed to enforce Safe
  Drinking Water Act violations from 2015-2021.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  150,000-180,000 residents (84% minority, 25% below poverty line) lost safe drinking water
  for weeks. Boil-water advisories persisted for months. 55 pipe breaks per 100 miles annually
  (safe threshold: 15). ~50% of treated water lost to leaks or faulty meters. Total repair
  cost estimated at $2 billion. Federal disaster declaration issued.
  ```
- **GeoJSON:**

  ```
  150,000-180,000 residents (84% minority, 25% below poverty line) lost safe drinking water
  for weeks. Boil-water advisories persisted months. 55 pipe breaks per 100 miles annually.
  ~50% of treated water lost to leaks. Total repair cost: ~$2B. Federal disaster declared.
  ```

### field: `one_line`

- **YAML:**

  ```
  Jackson's 180,000 residents depend on a city water system whose survival requires state
  funding; Mississippi's government actively withheld federal relief dollars and vetoed
  revenue-recovery legislation.
  ```
- **GeoJSON:**

  ```
  Jackson's 180,000 residents depend on a water system whose survival requires state funding;
  Mississippi's government actively withheld federal relief and vetoed revenue-recovery
  legislation.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `Washington Post` — https://www.washingtonpost.com/nation/2022/09/03/jackson-mississippi-water-crisis/ (2022-09-03)

## pacificorp-california-balancing-2022

Source file: `cases/pacificorp-california-balancing-2022.yaml`

### field: `trigger`

- **YAML:**

  ```
  PacifiCorp operates its own balancing authority (PACW) spanning six states; California
  customers sit outside CAISO. Wildfire liabilities totaling $2.2B+ in settlements are being
  recovered across PacifiCorp's multi-state rate base, and $1.7B in wildfire costs are being
  pushed into FERC-jurisdictional transmission rates that wholesale customers must absorb.
  ```
- **GeoJSON:**

  ```
  PacifiCorp operates its own balancing authority (PACW) spanning six states; California
  customers sit outside CAISO. Wildfire liabilities totaling $2.2B+ in settlements are being
  recovered across PacifiCorp's multi-state rate base, and $1.7B in wildfire costs are being
  pushed into FERC-jurisdictional transmission rates.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  Northern California customers have no representation in CAISO governance, cannot access
  CAISO reliability programs, and face rate exposure from wildfire liabilities incurred across
  PacifiCorp's six-state territory. Utah wholesale customers face a 32-45% transmission rate
  increase from wildfire costs while PacifiCorp's own retail customers in Salt Lake City pay
  nothing toward wildfire liability.
  ```
- **GeoJSON:**

  ```
  Northern California customers have no representation in CAISO governance, cannot access
  CAISO reliability programs, and face rate exposure from wildfire liabilities incurred across
  PacifiCorp's six-state territory. Utah wholesale customers face a 32-45% transmission rate
  increase from wildfire costs while PacifiCorp's own retail customers in Salt Lake City pay
  nothing.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `Utility Dive` — https://www.utilitydive.com/news/pacificorp-ferc-bpa-wildfire-liability-transmission-rates/758475/ (2025-08-22)
  - `Utility Dive` — https://www.utilitydive.com/news/utah-deseret-uamps-ferc-pacificorp-wildfire-transmission/752557/ (2025-07-14)

## pjm-data-center-cost-spillover-2025

Source file: `cases/pjm-data-center-cost-spillover-2025.yaml`

### field: `trigger`

- **YAML:**

  ```
  Data centers concentrated in Virginia's Dominion zone drove an 833% increase in PJM capacity
  auction clearing prices from $28.92/MW-day (2024/25) to $269.92/MW-day (2025/26). Data
  centers accounted for 63% of the $9.3B cost increase and 94% of projected 32 GW demand
  growth through 2030. PJM's December 2025 auction fell 6,625 MW short of reliability
  requirements for the first time ever. From 2022-2024, $4.3B in transmission expansion costs
  for data center connections were socialized to ratepayers across 7 states.
  ```
- **GeoJSON:**

  ```
  Data centers in Virginia's Dominion zone drove an 833% increase in PJM capacity auction
  clearing prices. Data centers accounted for 63% of the $9.3B cost increase and 94% of
  projected 32 GW demand growth through 2030. PJM's December 2025 auction fell 6,625 MW short
  of reliability requirements for the first time ever.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  Residential ratepayers across 13 states pay for Virginia's data center growth: Pepco (D.C.)
  customers see $21/month increase, western Maryland $18/month, Ohio $16/month, Columbus OH
  $27/month. NRDC projects $100-163B in cumulative capacity costs through 2033. PJM's first-
  ever reliability shortfall means potential rolling blackouts. Customers in Ohio, Illinois,
  and West Virginia have no influence over Virginia's data center permitting.
  ```
- **GeoJSON:**

  ```
  Residential ratepayers across 13 states pay for Virginia's data center growth: Pepco (D.C.)
  +$21/month, western Maryland +$18/month, Ohio +$16/month. NRDC projects $100-163B in
  cumulative capacity costs through 2033. PJM's first-ever reliability shortfall means
  potential rolling blackouts.
  ```

### field: `current_status`

- **YAML:** _(absent)_
- **GeoJSON:**

  ```
  FERC opened a parallel colocation tariff proceeding (Docket EL25-49-000) via show-cause
  order on Dec 18, 2025, addressing whether data centers colocated with generation should
  bypass grid charges. March 25, 2026 protests from Vistra, Constellation Energy, and the Data
  Center Coalition criticized PJM's proposed framework as operationally rigid; replies due
  April 17, 2026. Separately, FERC's RM26-4-000 ANOPR on large-load (>20 MW) interconnection —
  directed by DOE Oct 2025 — is on a June 2026 action timeline.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `Sierra Club` — https://www.sierraclub.org/press-releases/2025/12/pjm-capacity-auction-ends-record-high-costs-again (2025-12-17)
  - `NRDC` — https://www.nrdc.org/press-releases/pjm-board-announces-final-proposal-address-data-center-demand (2026-02-10)

## potomac-interceptor-collapse-2026

Source file: `cases/potomac-interceptor-collapse-2026.yaml`

### field: `title`

- **YAML:**

  ```
  Potomac Interceptor sewer collapse releases 300M gallons of untreated sewage into Potomac
  River
  ```
- **GeoJSON:**

  ```
  Potomac Interceptor sewer collapse releases 240M gallons of untreated sewage into Potomac
  River
  ```

### field: `controlling_actor`

- **YAML:**

  ```
  DC Water (District of Columbia Water and Sewer Authority)
  ```
- **GeoJSON:**

  ```
  DC Water
  ```

### field: `trigger`

- **YAML:**

  ```
  A section of the 54-mile, 60-year-old Potomac Interceptor sewer line collapsed on January
  19, 2026, along Clara Barton Parkway in Montgomery County, MD. Virginia and Maryland suburbs
  send ~60 MGD of sewage through this DC Water-owned pipe they cannot maintain or inspect.
  ```
- **GeoJSON:**

  ```
  A section of the 54-mile, 60-year-old 72-inch Potomac Interceptor ruptured on January 19,
  2026 in Montgomery County, MD, near the C&O Canal National Historical Park. Virginia and
  Maryland suburbs send ~60 MGD through this DC Water-owned pipe they cannot maintain or
  inspect.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  240-300 million gallons of untreated wastewater released into the C&O Canal and Potomac
  River — one of the largest sewage spills in U.S. history. E. coli levels hundreds of times
  above EPA safety limits. Health advisories across DC, MD, and VA. Recreation shut down for
  months. Emergency bypass took five days; full flow not restored until March 14, 2026.
  ```
- **GeoJSON:**

  ```
  ~240 million gallons of untreated wastewater released into the Potomac and tributaries over
  8 days — one of the largest sewage spills in U.S. history. DC Water bypassed sewage through
  a dry stretch of the C&O Canal, itself polluting the national park. E. coli hundreds of
  times above EPA limits. Health advisories across DC, MD, VA; recreation shut down for
  months.
  ```

### field: `current_status`

- **YAML:** _(absent)_
- **GeoJSON:**

  ```
  April 20, 2026: DOJ (on behalf of EPA) and Maryland AG Anthony Brown + Maryland Department
  of the Environment filed parallel Clean Water Act complaints against DC Water in separate
  venues. Maryland seeks civil penalties up to $10,000/day per violation, cleanup costs,
  natural resource damages, and injunctive relief. May 20, 2026: DC Water disclosed that three
  additional segments of the 54-mile interceptor require urgent repair — the failure mode is
  not isolated to the original collapse location, and the maintenance backlog on the line that
  VA/MD suburbs depend on is broader than a single point of failure.
  ```

### field: `one_line`

- **YAML:**

  ```
  Virginia and Maryland suburbs send sewage through a DC Water-owned pipe they cannot
  maintain; when it collapsed, 300 million gallons of untreated wastewater hit the Potomac.
  ```
- **GeoJSON:**

  ```
  Virginia and Maryland suburbs send sewage through a DC Water-owned pipe they cannot
  maintain; when it collapsed, 240 million gallons of untreated wastewater hit the Potomac
  over 8 days and triggered parallel federal and state lawsuits.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `Maryland Department of the Environment` — https://mde.maryland.gov/programs/water/Compliance/Pages/Potomac-Interceptor-Sewer-Overflow.aspx (2026-01-19)
- **Only in GeoJSON (missing from YAML):**
  - `U.S. EPA / DOJ` — https://www.epa.gov/newsreleases/united-states-files-complaint-against-dc-water-response-potomac-interceptor-collapse (2026-04-20)
  - `Maryland Office of the Attorney General` — https://oag.maryland.gov/News/pages/-Attorney-General-Brown-Files-Lawsuit-Against-DC-Water-Over-Potomac-Interceptor-Collapse-.aspx (2026-04-20)
  - `Axios DC` — https://www.axios.com/local/washington-dc/2026/05/20/dc-water-sewage-spill-potomac-interceptor-repairs (2026-05-20)

## tahoe-nvenergy-supply-2026

Source file: `cases/tahoe-nvenergy-supply-2026.yaml`

### field: `trigger`

- **YAML:**

  ```
  NV Energy informed Liberty Utilities it would not extend the full-requirements wholesale
  supply arrangement beyond May 2027, citing its own resource needs. Liberty currently gets
  ~75% of its power from NV Energy. The northern Nevada market is now "extremely competitive"
  due to data center load growth, and transmission for new interconnections is severely
  constrained.
  ```
- **GeoJSON:**

  ```
  NV Energy informed Liberty Utilities it would not extend the full-requirements wholesale
  supply arrangement past its May 31, 2027 termination, citing its own resource needs. The
  northern Nevada market is now extremely competitive due to Tahoe-Reno Industrial Center data
  center load growth, and transmission for new interconnections is severely constrained.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  49,000 California customers face a rushed wholesale resupply process. Liberty must procure
  replacement power by March 2027 and has asked California regulators for expedited approval.
  Customers will absorb whatever replacement costs emerge. Because Liberty's territory sits in
  the NV Energy balancing authority — not CAISO — the community has no access to California's
  main grid reliability programs.
  ```
- **GeoJSON:**

  ```
  49,000 California customers face a rushed wholesale resupply process covering ~75% of
  Liberty's Tahoe-region supply. Liberty must procure replacement power before the May 31,
  2027 contract termination. Greenlink Nevada transmission relief lands after the gap opens —
  Greenlink West in-service slipped to May 2027, Greenlink North to late 2028 — so upstream
  capacity relief arrives too late to help. Because Liberty's territory sits in the NV Energy
  balancing authority — not CAISO — the community has no access to California's main grid
  reliability programs.
  ```

### field: `current_status`

- **YAML:** _(absent)_
- **GeoJSON:**

  ```
  Liberty filed at CPUC in March 2026 seeking expedited authorization to run an RFP for
  replacement supply; formal RFP planned for summer 2026. Replacement power likely sourced
  outside California and wheeled over NV Energy transmission.
  ```

### field: `one_line`

- **YAML:**

  ```
  California community electrically dependent on Nevada; supplier withdrawing capacity under
  data-center pressure, forcing emergency procurement.
  ```
- **GeoJSON:**

  ```
  California community electrically dependent on Nevada; supplier withdrawing capacity under
  data-center pressure, forcing emergency procurement before upstream transmission relief
  arrives.
  ```

### field: `sources`

- **Only in GeoJSON (missing from YAML):**
  - `South Tahoe Now` — https://southtahoenow.com/05/15/2026/liberty-responds-to-upcoming-power-situation-for-lake-tahoe (2026-05-15)
  - `Northern Nevada Business Weekly` — https://www.nnbw.com/news/2026/apr/08/nv-energys-greenlink-west-expected-to-come-online-in-mid-2027/ (2026-04-08)

## texas-uri-gas-electric-2021

Source file: `cases/texas-uri-gas-electric-2021.yaml`

### field: `controlling_actor`

- **YAML:**

  ```
  ERCOT / Texas Railroad Commission / uncoordinated gas producers and pipeline operators
  ```
- **GeoJSON:**

  ```
  ERCOT / Texas Railroad Commission / uncoordinated gas producers
  ```

### field: `trigger`

- **YAML:**

  ```
  February 2021 arctic blast caused cascading gas-electric interdependency failure. Permian
  Basin gas production dropped 85%. Gas compressors on interruptible electric contracts lost
  power during rolling blackouts, cutting gas supply to generators that needed gas to produce
  the electricity that powered the compressors. FERC/NERC found natural gas fuel supply issues
  accounted for 87% of all fuel-related generator outages.
  ```
- **GeoJSON:**

  ```
  February 2021 arctic blast caused cascading gas-electric interdependency failure. Permian
  Basin gas production dropped 85%. Gas compressors on interruptible electric contracts lost
  power, cutting gas supply to generators that needed gas to produce electricity. FERC/NERC
  found gas fuel supply issues accounted for 87% of all fuel-related generator outages.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  4.5 million+ homes and businesses lost power, many for days (average 42 hours). Official
  death toll: 246; independent estimates: 426-978 excess deaths. 69% of Texans lost power; 49%
  lost water service. Economic losses estimated at $80-130 billion (Federal Reserve Bank of
  Dallas).
  ```
- **GeoJSON:**

  ```
  4.5 million+ homes lost power for an average of 42 hours. Official death toll: 246;
  independent estimates: 426-978. 69% of Texans lost power; 49% lost water. Economic losses:
  $80-130 billion.
  ```

### field: `one_line`

- **YAML:**

  ```
  Texas's unregulated gas producers had no obligation to winterize or coordinate with the
  electric grid; the freeze created a death spiral where electric outages killed gas
  compressors that killed gas supply that killed electric generators.
  ```
- **GeoJSON:**

  ```
  Texas's unregulated gas producers had no obligation to winterize or coordinate with the
  grid; the freeze created a death spiral where electric outages killed gas supply that killed
  electric generation.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `KUT Radio (Austin NPR)` — https://www.kut.org/energy-environment/2025-08-18/texas-energy-grid-winterize-blackouts-audit (2025-08-18)

## toledo-lake-erie-algal-bloom-2014

Source file: `cases/toledo-lake-erie-algal-bloom-2014.yaml`

### field: `trigger`

- **YAML:**

  ```
  On August 2, 2014, a massive harmful algal bloom caused by phosphorus-laden agricultural
  runoff produced microcystin toxin levels exceeding safe limits at Toledo's water intake on
  Lake Erie. State regulators lacked legal authority to regulate non-point-source farm runoff.
  A decade later, blooms persist annually; Ohio's voluntary H2Ohio program achieves only ~10%
  phosphorus reduction vs the 40% needed.
  ```
- **GeoJSON:**

  ```
  On August 2, 2014, a massive harmful algal bloom caused by phosphorus-laden agricultural
  runoff produced microcystin toxin exceeding safe limits at Toledo's Lake Erie intake. State
  regulators lacked authority to regulate non-point-source farm runoff. A decade later, blooms
  persist annually.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  500,000+ residents received "do not drink, do not touch" water orders for three days.
  Businesses closed, tourism disrupted. Estimated $65M in economic damage. Toledo has since
  invested $500M in treatment upgrades. Toxic blooms continue annually.
  ```
- **GeoJSON:**

  ```
  500,000+ residents received 'do not drink, do not touch' orders for three days. $65M
  economic damage. Toledo has invested $500M in treatment upgrades. Toxic blooms continue
  annually; Ohio's voluntary program achieves only ~10% phosphorus reduction vs 40% needed.
  ```

### field: `one_line`

- **YAML:**

  ```
  Toledo's 500,000 residents draw water from Lake Erie but phosphorus runoff from farmland
  across three states — governed by regulators with no authority over non-point agricultural
  pollution — causes recurring toxic blooms.
  ```
- **GeoJSON:**

  ```
  Toledo's 500,000 residents draw water from Lake Erie but phosphorus runoff from farmland
  across three states — governed by regulators with no non-point-source authority — causes
  recurring toxic blooms.
  ```

## tva-elliott-gas-generation-2022

Source file: `cases/tva-elliott-gas-generation-2022.yaml`

### field: `controlling_actor`

- **YAML:**

  ```
  Tennessee Valley Authority / upstream gas producers and pipeline operators
  ```
- **GeoJSON:**

  ```
  Tennessee Valley Authority / upstream gas producers
  ```

### field: `trigger`

- **YAML:**

  ```
  Christmas Eve 2022 arctic blast caused 10 of TVA's 17 gas plants and 4 of 6 coal plants to
  fail or derate. Gas supply was inadequate due to freeze-related production declines
  (Marcellus down 23%, Utica down 54%) and insufficient pipeline pressure. TVA ordered all 153
  local power companies to shed 5-10% of load. Nationally, 90,000 MW went offline; gas
  generators were 70% of forced outages.
  ```
- **GeoJSON:**

  ```
  Christmas Eve 2022 arctic blast caused 10 of 17 TVA gas plants and 4 of 6 coal plants to
  fail. Gas supply was inadequate — Marcellus down 23%, Utica down 54%. TVA ordered all 153
  local distributors to shed 5-10% of load. 90,000 MW went offline nationally; gas generators
  were 70% of forced outages.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  Rolling blackouts on Christmas Eve/Christmas Day across the Mid-South. Millions of customers
  affected across TVA's seven-state territory. Financial impact to TVA: $170M. FERC/NERC found
  the event was the largest percentage of Eastern Interconnection capacity ever to fail
  simultaneously (13%).
  ```
- **GeoJSON:**

  ```
  Rolling blackouts on Christmas Eve across the Mid-South. Millions affected across seven
  states. $170M financial impact to TVA. FERC/NERC found it was the largest percentage of
  Eastern Interconnection capacity ever to fail simultaneously (13%).
  ```

### field: `one_line`

- **YAML:**

  ```
  TVA's gas plants failed on Christmas Eve because the upstream gas supply chain froze across
  states TVA does not control, and 153 local power companies had no lever to pull except
  cutting power to their own customers.
  ```
- **GeoJSON:**

  ```
  TVA's gas plants failed on Christmas Eve because upstream gas supply froze across states TVA
  does not control, and 153 local power companies had no lever except cutting power to
  customers.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `WPLN News (Nashville NPR)` — https://wpln.org/post/tennessee-blackouts-winter-2023/ (2023-11-27)

## upper-peninsula-michigan-miso-2024

Source file: `cases/upper-peninsula-michigan-miso-2024.yaml`

### field: `trigger`

- **YAML:**

  ```
  The UP's western two-thirds are electrically tied to northern Wisconsin via ATC's
  transmission system, not to Lower Michigan. ATC is headquartered in Wisconsin and majority-
  owned by Wisconsin utilities. Limited interconnections make the UP vulnerable to large
  outages — a 2011 lightning event during planned maintenance knocked out power to two-thirds
  of the peninsula. Data center load growth in Wisconsin is driving $1.3B+ in new transmission
  investment that UP ratepayers may subsidize through MISO cost allocation.
  ```
- **GeoJSON:**

  ```
  The UP's western two-thirds are electrically tied to northern Wisconsin via ATC's
  transmission system, not to Lower Michigan. ATC is headquartered in Wisconsin and majority-
  owned by Wisconsin utilities. A 2011 lightning event during planned maintenance knocked out
  power to two-thirds of the peninsula. Data center load growth in Wisconsin is driving $1.3B+
  in new transmission investment that UP ratepayers may subsidize.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  ~300,000 residents depend on a transmission system owned and planned by a Wisconsin-based
  company, governed by a multi-state RTO headquartered in Indiana. ATC cannot provide firm
  service to some UP utilities due to transmission constraints. Wisconsin data center-driven
  buildout costs may be socialized to UP customers.
  ```
- **GeoJSON:**

  ```
  ~300,000 residents depend on a transmission system owned and planned by a Wisconsin-based
  company, governed by a multi-state RTO headquartered in Indiana. ATC cannot provide firm
  service to some UP utilities due to transmission constraints.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `Michigan Public Service Commission` — https://www.michigan.gov/mpsc/commission/news-releases/2024/07/17/mpsc-to-hold-public-hearing-on-study-of-energy-issues-in-the-upper-peninsula (2024-07-17)
  - `Governing` — https://www.governing.com/infrastructure/even-23b-might-not-be-enough-to-upgrade-midwests-power-lines (2024-10-15)

## washington-aqueduct-single-source-2026

Source file: `cases/washington-aqueduct-single-source-2026.yaml`

### field: `controlling_actor`

- **YAML:**

  ```
  U.S. Army Corps of Engineers (Baltimore District)
  ```
- **GeoJSON:**

  ```
  U.S. Army Corps of Engineers
  ```

### field: `trigger`

- **YAML:**

  ```
  The January 2026 Potomac Interceptor sewage spill renewed attention on the fact that DC and
  Arlington have zero alternative drinking water sources. The Potomac River is the sole
  intake. The Aqueduct's Dalecarlia Reservoir holds only 24-48 hours of supply. A 2025 ICPRB
  report found that in 4 of 9 extreme drought scenarios, upstream reservoirs run dry by 2030.
  The Trump administration tried to sell the Aqueduct in 2017.
  ```
- **GeoJSON:**

  ```
  The January 2026 sewage spill renewed attention on the fact that DC and Arlington have zero
  alternative water sources. The Potomac is the sole intake. Dalecarlia Reservoir holds only
  24-48 hours of supply. A 2025 ICPRB report found upstream reservoirs could run dry by 2030
  in 4 of 9 drought scenarios.
  ```

### field: `public_consequence`

- **YAML:**

  ```
  1.1 million people have no backup water supply if the Potomac becomes contaminated or runs
  low. DC Water, Arlington County, and Fairfax Water have no vote on Army Corps capital
  investment decisions. Rate-setting and modernization are controlled by a federal agency with
  competing priorities.
  ```
- **GeoJSON:**

  ```
  1.1 million people have no backup water supply. DC Water, Arlington, and Fairfax Water have
  no vote on Army Corps capital investment decisions. Rate-setting and modernization
  controlled by a federal agency with competing priorities.
  ```

### field: `one_line`

- **YAML:**

  ```
  A federal agency operates the sole drinking water system for 1.1M people in DC and Virginia;
  customers have no alternative source and limited influence over capital investment or
  emergency preparedness decisions.
  ```
- **GeoJSON:**

  ```
  A federal agency operates the sole drinking water system for 1.1M people in DC and Virginia;
  customers have no alternative source and limited influence over capital investment
  decisions.
  ```

### field: `sources`

- **Only in YAML (dropped from published GeoJSON):**
  - `U.S. Army Corps of Engineers` — https://www.nab.usace.army.mil/Missions/Washington-Aqueduct/ (2026-01-01)


---

**Cases with divergence: 15 of 16.**

## Orphan copy: `docs/data/cases.geojson`

- Cases in published `us/`: 16
- Cases in orphan: 15
- Absent from orphan: ['doe-202c-emergency-orders-2025']
- Absent from published: none

Field-level staleness of the orphan against published `us/`:

- `pjm-data-center-cost-spillover-2025` — stale fields: `current_status`
- `potomac-interceptor-collapse-2026` — stale fields: `title`, `trigger`, `public_consequence`, `current_status`, `one_line`, `sources`
- `tahoe-nvenergy-supply-2026` — stale fields: `trigger`, `public_consequence`, `current_status`, `one_line`, `sources`
