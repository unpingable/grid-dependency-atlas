# Infrastructure Dependency Atlas

**Places where local customers are exposed to infrastructure decisions made
outside their own effective political control.**

An atlas of documented cases where the geography of political accountability
diverges from the geography of infrastructure control — across electricity,
gas, water, and sewer systems in the United States.

## What this is

A curated collection of cases where:

- A retail utility territory sits inside a balancing authority governed from
  another state
- A wholesale supply contract can be terminated by an actor with different
  priorities
- A regional market operator's rules or errors directly set local prices
- An interstate pipeline's capacity allocation determines local availability
- A cross-jurisdictional trunk line or treatment facility is the single path
- An interstate allocation regime leaves downstream communities exposed

Each case is documented with: the dependency, who controls it, how it crosses
political boundaries, what happened, and why normal people should care.

## Live map

**[unpingable.github.io/grid-dependency-atlas](https://unpingable.github.io/grid-dependency-atlas/)**

## Structure

```
schema.yaml          # Event schema
CASES.md             # Case index table
SYNTHESIS.md         # Thesis, patterns, scope decisions
TAXONOMY.md          # Cross-cutting tags and facets
cases/               # 15 individual case files (YAML)
docs/                # GitHub Pages site (MapLibre map)
```

## Current cases (15)

| Utility | Cases |
|---------|-------|
| Electricity | Tahoe/NV Energy, PacifiCorp CA, Michigan UP, Delmarva/PJM, PJM data center spillover, Entergy/NOLA |
| Gas | ISO-NE winter, Texas Uri, Aquidneck Island, TVA Elliott |
| Water | Washington Aqueduct, Colorado River, Jackson MS, Toledo |
| Sewer | Potomac Interceptor |

## Provenance

This project is human-directed and AI-assisted. See [PROVENANCE.md](PROVENANCE.md).

## License

Apache 2.0. See [LICENSE](LICENSE).
