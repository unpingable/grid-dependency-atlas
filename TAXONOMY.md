# Case Taxonomy — Cross-cutting tags

Each case can carry multiple tags. These are facets, not categories.

## By dependency subtype

### Cross-state
Affected customers in State A, controlling actor in State B.
- Tahoe / NV Energy (CA customers, NV supplier)
- PacifiCorp California (CA customers, OR-based utility, 6-state BA)
- Michigan UP (MI customers, WI-based transmission, IN-based RTO)
- Delmarva / PJM (DE/MD customers, PA-based market operator)
- PJM Data Center Spillover (13 states paying for VA load growth)
- ISO-NE Gas Constraint (6 states dependent on TX/AB pipeline operators)
- Aquidneck Island (RI customers, Canadian-owned FERC-regulated pipeline)
- TVA Elliott (7 states dependent on gas from PA/WV/OH/Gulf)
- Colorado River (7 states, Lower Basin exposed to Upper Basin decisions)
- Toledo (OH customers, pollution from OH/IN/MI watershed)
- DOE 202(c) (11 MISO states absorbing one Michigan utility's compliance cost)

### Cross-level-of-government
Local government dependent on state or federal decisions.
- Jackson, MS (city dependent on state funding decisions)
- Washington Aqueduct (DC/Arlington dependent on federal Army Corps)
- Entergy/NOLA (city council regulates local utility but has no authority over MISO or Entergy corporate)
- DOE 202(c) (utilities and states overridden by federal executive on retirement decisions)

### Contractual
Dependency encoded in a contract that can be terminated or repriced.
- Tahoe / NV Energy (wholesale supply contract not renewed)
- Washington Aqueduct (wholesale water arrangement with Army Corps)

### Physical-network
Dependency runs through physical wires, pipes, or trunk lines.
- Michigan UP (ATC transmission)
- Entergy/NOLA (Amite South load pocket, insufficient import capacity)
- ISO-NE Gas (pipeline sizing)
- Aquidneck Island (pipeline branch)
- Potomac Interceptor (trunk sewer line)

### Market-governance
Dependency is mediated through a regional market operator's rules or design.
- Delmarva / PJM (auction modeling error)
- PJM Data Center Spillover (capacity price socialization)
- PacifiCorp CA (FERC transmission rate allocation for wildfire costs)
- DOE 202(c) (downstream RTO cost-allocation mechanism is what spreads the federal order's bill across 11 states)

### Federal-override
Federal executive directive countermands utility, state, or market decisions.
- DOE 202(c) (Section 202(c) emergency orders override planned retirements)

### Scarcity/allocation
Dependency is about who gets how much of a limited resource.
- Colorado River (basin-wide shortage sharing)
- ISO-NE Gas (pipeline capacity allocation between heating and generation)
- Tahoe (NV Energy reallocating capacity to own needs)

### Demand-shock aggravated
New large loads exposed or amplified a preexisting dependency.
- Tahoe (data center load in northern Nevada)
- PJM Data Center Spillover (Virginia data centers)
- Michigan UP (Wisconsin data center buildout)
- ISO-NE Gas (growing generation demand on fixed pipeline capacity)

## By primary trigger

| Trigger | Cases |
|---------|-------|
| supplier_withdrawal | Tahoe |
| demand_shock | PJM spillover, Michigan UP |
| extreme_weather | Texas Uri, TVA Elliott, Aquidneck Island, ISO-NE |
| modeling_error | Delmarva/PJM |
| infrastructure_failure | Potomac Interceptor, Entergy/NOLA |
| funding_withholding | Jackson MS |
| allocation_dispute | Colorado River |
| regulatory_gap | Toledo, PacifiCorp CA |
| federal_directive | DOE 202(c) |

## By utility type

| Type | Count | Cases |
|------|-------|-------|
| Electricity | 7 | Tahoe, PacifiCorp, Michigan UP, Delmarva, PJM spillover, Entergy/NOLA, DOE 202(c) |
| Gas-electric | 4 | ISO-NE, Texas Uri, Aquidneck, TVA Elliott |
| Water | 4 | Washington Aqueduct, Colorado River, Jackson, Toledo |
| Sewer | 1 | Potomac Interceptor |
