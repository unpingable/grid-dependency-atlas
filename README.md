# Infrastructure Dependency Atlas

**Places where local populations are exposed to infrastructure decisions made
outside their effective political control.**

Same thesis, different substrates. Nine maps across physical infrastructure,
energy chokepoints, maritime chokepoints, financial governance, agricultural
inputs, water basins, grid equipment, subsea cables, and digital infrastructure.

## Live site

**[unpingable.github.io/grid-dependency-atlas](https://unpingable.github.io/grid-dependency-atlas/)**

## Atlases

| Atlas | Cases | Scope |
|-------|-------|-------|
| [U.S. Infrastructure](https://unpingable.github.io/grid-dependency-atlas/us/) | 16 cases | Electricity, gas, water, sewer — domestic dependency mismatches |
| [Hormuz Energy](https://unpingable.github.io/grid-dependency-atlas/hormuz/) | 12 countries | Energy stress bands under Strait of Hormuz disruption |
| [Maritime Chokepoints](https://unpingable.github.io/grid-dependency-atlas/chokepoints/) | 5 straits | Global dependency on narrow transit geometry |
| [Insurance Dependency](https://unpingable.github.io/grid-dependency-atlas/insurance/) | 6 states | Insurer exit as hidden governance layer over housing |
| [Fertilizer-to-Food](https://unpingable.github.io/grid-dependency-atlas/fertilizer/) | 12 countries | Chokepoint → fertilizer → planting → yield → food insecurity |
| [Water Basins](https://unpingable.github.io/grid-dependency-atlas/water/) | 8 cases | Where consumption happens is not where hydrological control sits |
| [Grid Equipment](https://unpingable.github.io/grid-dependency-atlas/grid-equipment/) | 7 cases | Long-lead transformers, single-vendor steel, physical limits of replacement |
| [Subsea Cables](https://unpingable.github.io/grid-dependency-atlas/subsea/) | 9 cases | Landing concentration, corridor chokepoints, single-cable fragility, repair bottleneck |
| [Cloud / CDN](https://unpingable.github.io/grid-dependency-atlas/cloud/) | 10 cases | Digital infrastructure concentration and sovereignty gaps |

## Structure

```
schema.yaml          # Event schema (U.S. cases)
CASES.md             # U.S. case index table
SYNTHESIS.md         # Thesis, patterns, scope decisions
TAXONOMY.md          # Cross-cutting tags and facets
cases/               # individual U.S. case files (YAML)
docs/                # GitHub Pages site
  index.html         # Splash page (routes to all 9 maps)
  us/                # U.S. infrastructure map + data
  hormuz/            # Hormuz energy chokepoint map + data
  chokepoints/       # Maritime chokepoints map + data
  insurance/         # Insurance dependency map + data
  fertilizer/        # Fertilizer-to-food stress map + data
  water/             # Water basin dependency map + data
  grid-equipment/    # Grid equipment dependency map + data
  subsea/            # Subsea cable dependency map + data
  cloud/             # Cloud/CDN dependency map + data
```

## The invariant

Across all eight atlases, the same pattern:

1. Dependency centralizes invisibly before it centralizes politically
2. Control accumulates at the point where distant users cannot meaningfully negotiate
3. Different sectors keep rediscovering the same chokepoint logic
4. Abstraction does not eliminate chokepoints — it concentrates them somewhere else

## Provenance

This project is human-directed and AI-assisted. See [PROVENANCE.md](PROVENANCE.md).

## License

Apache 2.0. See [LICENSE](LICENSE).
