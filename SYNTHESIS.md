# Infrastructure Dependency Atlas — Synthesis Memo

**Draft. Not for publication. March 2026.**

## Thesis

Places where local customers are exposed to infrastructure decisions made
outside their own effective political control.

"Effective" is load-bearing. The failure mode is not always cross-state. It
can be cross-level-of-government (Jackson), cross-agency (Washington Aqueduct),
cross-market (PJM), or cross-watershed (Toledo, Colorado River). What unifies
the cases is that the people who bear the consequences do not control the
decisions that produce them.

## What we found

15 cases across four utility types (electricity, gas, water, sewer), drawn
from public filings, regulatory proceedings, federal reports, and journalism.
The schema — a flat record with case metadata, a `control_layer` field, and
sourced evidence — survived all 15 without modification.

## The control layers

The `control_layer` field turned out to be the conceptual spine. It answers:
**where does the outside actor actually hold the knife?**

Eight layers emerged:

| Layer | What it means | Example |
|-------|--------------|---------|
| `wholesale_contract` | Local utility buys power/water from an outside supplier who can decline to renew | Tahoe / NV Energy |
| `balancing` | Local customers sit inside a balancing authority governed from another state | PacifiCorp California |
| `transmission` | The physical wires or pipes are owned/planned by an outside entity | Michigan UP, Entergy/NOLA |
| `market_governance` | A regional market operator's rules or errors directly set local prices | Delmarva/PJM, PJM data center spillover |
| `pipeline_capacity` | Interstate pipeline allocation determines local gas/electricity availability | ISO-NE, Aquidneck Island |
| `supply` | Upstream production, funding, or pollution decisions control local service | Texas Uri, TVA Elliott, Jackson, Toledo |
| `treatment` | A cross-jurisdictional treatment facility or trunk line is the single path | Potomac Interceptor |
| `basin_allocation` | Interstate water allocation rules determine local supply | Colorado River |

These are not all the same kind of thing. They split roughly into:

- **Contractual/market**: wholesale_contract, market_governance
- **Physical network**: transmission, pipeline_capacity, treatment
- **Governance/allocation**: balancing, basin_allocation
- **Upstream dependency**: supply (production, funding, pollution)

That four-way split might be more useful than listing eight layers flat. Or it
might not. The cases will tell us once we try to explain them to a reader.

## Recurring patterns

### 1. Data center demand as an accelerant

Data center load growth appears as a trigger or aggravating factor in at least
four electricity cases:

- **Tahoe**: NV Energy withdrawing supply citing "own resource needs"; northern
  Nevada market described as "extremely competitive" due to data centers.
- **PJM spillover**: Virginia data centers drove 833% capacity price increase,
  socialized across 13 states.
- **Michigan UP**: Wisconsin data center buildout driving $1.3B+ in transmission
  costs potentially socialized to UP ratepayers.
- **ISO-NE**: Not directly data-center-driven, but the gas-electric coupling
  that makes New England vulnerable is the same mechanism that will intensify
  as large loads grow.

The pattern is not "AI turned off grandma's lights." It is: **new large loads
expose and amplify preexisting dependency structures.** The dependencies were
always there. The loads made them visible.

This deserves its own trigger class, not just a note in individual cases.

### 2. The abstraction-layer failure

In almost every case, the affected customers did not know about their exposure
until the dependency broke or became expensive. Tahoe residents probably did
not know they were in the NV Energy balancing authority. Delmarva customers did
not know PJM's capacity auction model had a bug. Newport residents did not know
their gas came through a Canadian-owned pipeline regulated by FERC.

The common experience is: **infrastructure works invisibly until it doesn't,
and when it fails, customers discover they have no lever to pull.** The
political geography they thought they lived in (their state, their city, their
utility) turns out to be a fiction layered over a different operational reality.

### 3. Scale invariance

The cases range from 18,000 people (Aquidneck Island) to 67 million (PJM
footprint) to 40 million (Colorado River basin). The pattern operates at every
scale. A small island community and a 13-state regional market can both be
exposed to the same structural problem: decisions made elsewhere, consequences
borne locally.

This is important for framing. This is not a story about small forgotten
places. It is also not exclusively a story about giant regional systems. It is
a story about a structural pattern that appears wherever infrastructure
geography and political geography diverge.

### 4. Regulatory fragmentation as a feature

In several cases, the dependency is not a bug but a designed outcome of
regulatory structure:

- PJM's capacity market is supposed to produce efficient regional pricing.
  The fact that it socializes Virginia data center costs to Ohio ratepayers
  is a feature of the market design, not a malfunction.
- MISO's transmission planning is supposed to optimize across its footprint.
  The fact that the Michigan UP depends on Wisconsin infrastructure is a
  consequence of joining a regional organization.
- The Colorado River Compact was designed to allocate water across states.
  The fact that downstream cities are exposed to upstream refusal is the
  compact working as intended.

The uncomfortable conclusion is that these dependencies are often the *point*
of the regional structure. The problem is not that the system is broken. The
problem is that the system works for some participants and not others, and the
ones it doesn't work for have limited recourse.

## Scope decisions

### Jackson is in scope

Jackson, MS is not cross-state. It is cross-level-of-government: a city
dependent on state-level funding and regulatory decisions that were actively
hostile. If the thesis is "outside effective political control," Jackson
qualifies. The city's residents could not vote out the governor or the state
legislature that withheld funds. Excluding it would amputate one of the most
important failure modes.

### Gas-electric coupling is one class, not two

Texas Uri and TVA Elliott are both cases where upstream gas supply failure
caused downstream electricity failure. The control layer is `supply` in both
cases. ISO-NE and Aquidneck Island are `pipeline_capacity` — the gas exists
but can't get there. These are different mechanisms but the same thesis: local
electricity or heating customers exposed to gas-sector decisions outside their
control.

They belong in the same atlas under different control layers, not in separate
projects.

### "Resolved" cases still matter

Texas Uri is marked `resolved` (legislatively). Aquidneck Island is `resolved`
(infrastructure upgrades). They still belong because:

1. They demonstrate the pattern.
2. "Resolved" is often aspirational — a 2025 Texas audit found ongoing
   winterization compliance problems.
3. Readers need to see that this has happened before, not just that it's
   happening now.

### What's NOT in scope

- General infrastructure disrepair (e.g., Flint, MI lead pipes) unless there
  is a clear cross-jurisdictional dependency.
- Natural disasters that overwhelm any system regardless of structure.
- Rate disputes that are purely internal to one utility's territory.
- International dependencies (though the Canadian ownership of Algonquin is
  notable, the regulatory dependency is on FERC, not Canada).

The test is: **could local political action have prevented or mitigated this?**
If the answer is "no, because the decision was made elsewhere," it's in scope.

## Proposed trigger taxonomy

The cases suggest a small set of recurring triggers:

| Trigger | Description |
|---------|-------------|
| `supplier_withdrawal` | Upstream supplier declines to continue arrangement |
| `demand_shock` | Large new loads (data centers, industrial) tighten supply/price |
| `extreme_weather` | Cold/heat/flood exposes preexisting structural vulnerability |
| `modeling_error` | Market operator's planning or auction model produces wrong result |
| `infrastructure_failure` | Physical collapse or capacity limit reached |
| `funding_withholding` | Higher-level government withholds resources from lower level |
| `allocation_dispute` | Interstate or inter-entity allocation rules expire or fail |
| `regulatory_gap` | No authority has jurisdiction over the relevant decision |

Most cases have a primary trigger and one or more aggravating factors.

## What this wants to be

Two products:

1. **A written piece** (essay, feature, or report) that introduces the concept,
   walks through 4–5 anchor cases, and names the pattern. This is the thing
   that makes people understand why the map matters.

2. **An interactive map** that operationalizes the concept: shows where the
   dependencies are, what kind they are, what happened, and who's exposed.
   This is the thing that makes the essay concrete and explorable.

The essay without the map is abstract. The map without the essay is
"miscellaneous utility weirdness." Together, they're a product.

## Specialized observatories

Some infrastructure patterns are best explained at atlas scale and best tracked
by specialized observatories. The atlas identifies a recurring structure across
substrates. A specialist tracker operationalizes one instance of it.

Track Data Centers (trackdatacenters.com) is the first clean example of this
relationship. It maps proposed U.S. data-center projects as a live civic
object — not industry rumor mulch, not retrospective analysis, but permits in
flight at the county level. Place-first, proposal-level, immediately usable to
someone showing up at a zoning board meeting.

The atlas should not become this. Building a thinner version of a sharper
instrument would dilute both. But the existence of an observatory like this is
itself evidence for one of the atlas's recurring claims: **"cloud" is a
euphemism until someone maps the land, water, power, and tax footprint.** The
tracker is that mapping, already in progress.

The division of labor:

- The atlas explains the pattern
- The specialist instrument shows where the pattern is filing permits

This is a reusable category. Other substrates already have fragments of it:
grid-interconnection queue trackers exist in regional form, subsea cable
incidents are logged by the industry, interstate water compacts are tracked by
basin commissions. Where specialists exist, the atlas's job is to name the
structural class and hand off. Where they don't, the atlas's role is more
load-bearing.

The handoff is the point, not an embarrassment.

## Open questions

1. **Should the map show static exposure or only documented events?**
   Static exposure (every cross-state BA mismatch) would be comprehensive
   but noisy. Event-only would be cleaner but incomplete. Probably: events
   as primary layer, structural exposure as secondary/background.

2. **Is there a meaningful severity ordering?**
   The crude answer is affected_population_est * confidence. The honest answer
   is that 18,000 people without heat for a week is arguably worse than 67
   million people paying $21/month more. Severity is multidimensional.

3. **How does this update?**
   An atlas of 15 cases can be a one-shot publication. An atlas that grows
   needs a maintenance model. This probably wants to be a one-shot with a
   clear invitation for contributions, not a live tracker (yet).

4. **Who is the audience?**
   Journalists covering energy/infrastructure. Regulators who think in
   jurisdictions. Advocates who need evidence. Residents who want to
   understand why their bills went up or their water went out. The essay
   serves the first three; the map serves all four.
