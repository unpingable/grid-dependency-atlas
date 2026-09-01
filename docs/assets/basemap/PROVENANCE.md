# Basemap substrate

`land.geojson`, `admin1.geojson`

**Role: cartographic substrate only.** Same doctrine as
`vendor/boundaries/PROVENANCE.md`. These boundaries are not evidence, are not
part of the claim corpus, and support no claim on any atlas page. They answer
"where is this" so a reader can recognise the ground a case marker sits on.
Every claim stays attached to a case record, never to this geometry.

Both files are **derived**. `tools/build_basemap.py` is the only writer;
`python3 tools/build_basemap.py --check` fails if either is stale.

| | |
|---|---|
| Source | Natural Earth 1:50m Admin 0 – Countries; Admin 1 – States/Provinces |
| Distribution | `nvkelso/natural-earth-vector`, tag **v5.1.2** |
| Upstream files | `geojson/ne_50m_admin_0_countries.geojson`, `geojson/ne_50m_admin_1_states_provinces.geojson` |
| Upstream sha256 | `3e458fc0…2b7fdeb`, `69a0e06e…98c426b9` — pinned in the builder; a changed upstream fails the build |
| Retrieved | 2026-08-31 |
| License | Public domain (Natural Earth terms of use). No API key, no rate limit, no attribution requirement — the pages credit Natural Earth anyway. |

Same release the static specimens already vendor in `vendor/boundaries/`, so the
whole repository draws its geography from one pinned upstream.

## Transform applied

1. `land.geojson`: all 235 countries with a surviving part. `admin1.geojson`:
   subnational divisions of US, CA, MX only — the only places any atlas zooms
   into far enough to want them.
2. All properties stripped. This substrate is not queried and carries no data;
   only its outline is drawn.
3. Douglas–Peucker at 0.01° (~1.1 km), then coordinates rounded to 3 dp
   (~110 m), matching the vendored static substrate.
4. Polygon parts with a bounding-box diagonal under 0.10° dropped (43 of 1620
   for admin 0, 6 of 175 for admin 1) — sub-pixel at every zoom these atlases
   allow.

## Why self-hosted

The interactive atlases drew their basemap from `basemaps.cartocdn.com/dark_all`
until 2026-08-31. CARTO moved that endpoint behind an API key and began
answering **HTTP 200** with PNGs stamped "API KEY REQUIRED" — so the atlas
rendered its evidence on a vendor error notice, and no code on the page could
detect it, because nothing had technically failed.

An atlas about dependence on infrastructure outside local control should not be
one of its own cases. This substrate ships with the site: no key, no quota, no
third-party origin, and a licence with no conditions attached.
