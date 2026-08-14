# Vendored boundary substrate

`ne_50m_admin0_subset.geojson`

**Role: cartographic substrate only.** These boundaries are not evidence, are not part
of the claim corpus, and support no claim on any atlas page. They answer "where is this
country" so that a reader can recognise the shape a band is painted on. Every claim
remains attached to a country *name*, never to a geometry.

| | |
|---|---|
| Source | Natural Earth 1:50m Admin 0 – Countries |
| Distribution | `nvkelso/natural-earth-vector`, tag **v5.1.2** |
| Upstream file | `geojson/ne_50m_admin_0_countries.geojson` |
| Upstream sha256 | `3e458fc036ad0a66411f2c1e6cac49c5d7bfb81cb1123bc513b22511a2b7fdeb` |
| Retrieved | 2026-08-14 |
| License | Public domain (Natural Earth terms of use) |

## Transform applied

1. Subset to the 12 countries in the Hormuz corpus, keyed by `ISO_A3`.
2. Polygon parts with a bounding-box diagonal under 0.10 deg dropped (2 of 146 parts) —
   these are sub-pixel at any page width.
3. Coordinates rounded to 3 decimal places (~110 m).

The join from corpus country name to `ISO_A3` is declared explicitly in
`tools/build_specimen_hormuz.py` and fails the build if a corpus country has no mapping.

---

## `ne_50m_admin1_us_subset.geojson`

Same role, same distribution and tag.

| | |
|---|---|
| Source | Natural Earth 1:50m Admin 1 – States/Provinces |
| Distribution | `nvkelso/natural-earth-vector`, tag **v5.1.2** |
| Upstream file | `geojson/ne_50m_admin_1_states_provinces.geojson` |
| Upstream sha256 | `69a0e06e640b2d505858ae1cb63034e4677f3000b35a98e16312932b98c426b9` |
| Retrieved | 2026-08-14 |
| License | Public domain |

Transform: subset to the 6 US states in the insurance corpus by `name`; parts with
bounding-box diagonal under 0.10 deg dropped (3 of 38); coordinates
rounded to 3 dp. Joined to the corpus by state name, declared in
`tools/build_specimen_insurance.py`; the build fails if a corpus state has no boundary.
