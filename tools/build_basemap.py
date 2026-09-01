#!/usr/bin/env python3
"""Build the self-hosted dark basemap substrate for the interactive atlases.

    Natural Earth 1:50m  ->  docs/assets/basemap/land.geojson
                             docs/assets/basemap/admin1.geojson

**Role: cartographic substrate only.** Same doctrine as
`vendor/boundaries/PROVENANCE.md`: these boundaries are not evidence, are not
part of the claim corpus, and support no claim on any atlas page. They answer
"where is this" so a reader can recognise the ground a marker sits on. Every
claim stays attached to a case record, never to this geometry.

Why it exists: the interactive atlases previously drew their basemap from
`basemaps.cartocdn.com/dark_all`, which now returns HTTP 200 tiles stamped
"API KEY REQUIRED" instead of map imagery. A basemap the atlas does not control
is exactly the dependency this atlas documents. This substrate ships with the
site, needs no key, and has no usage policy to fall foul of (public domain).

Doctrine (see RECONCILIATION-2026-08-14.md):
  - Upstream is pinned by tag AND sha256. A changed upstream fails the build
    rather than silently redrawing the world.
  - Generation is total, not incremental: outputs are rebuilt from source every
    run, so a hand-edit is discarded on the next build and reported by --check.
  - Proposal-only: writes data files, never commits.

Usage:
    python3 tools/build_basemap.py            # write
    python3 tools/build_basemap.py --check    # exit 1 if output is stale
"""
import argparse
import gzip
import hashlib
import json
import math
import os
import sys
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(REPO, "docs", "assets", "basemap")
CACHE = os.path.join(REPO, ".cache", "natural-earth")

# Pinned upstream. Same distribution and tag already vendored for the static
# specimens (vendor/boundaries/PROVENANCE.md), so the whole repository draws
# its geography from one release.
NE_TAG = "v5.1.2"
NE_BASE = ("https://raw.githubusercontent.com/nvkelso/natural-earth-vector/"
           + NE_TAG + "/geojson/")
SOURCES = {
    "admin0": ("ne_50m_admin_0_countries.geojson",
               "3e458fc036ad0a66411f2c1e6cac49c5d7bfb81cb1123bc513b22511a2b7fdeb"),
    "admin1": ("ne_50m_admin_1_states_provinces.geojson",
               "69a0e06e640b2d505858ae1cb63034e4677f3000b35a98e16312932b98c426b9"),
}

# Admin-1 is drawn only where an atlas actually zooms into it. The US and water
# atlases zoom to z10-z12 over North America; nothing zooms into subnational
# Europe or Asia, so shipping those lines would be weight with no reader.
ADMIN1_ISO_A2 = ("US", "CA", "MX")

# Simplification. 0.01 deg is ~1.1 km: invisible at the zooms these atlases
# open at, and still a recognisable coastline at their maximum (z12).
TOLERANCE_DEG = 0.01
PLACES = 3          # ~110 m, matching the vendored static substrate
MIN_PART_DIAG = 0.1  # drop polygon parts smaller than this bbox diagonal


# ------------------------------------------------------------------ geometry
def _simplify(points, tol):
    """Douglas-Peucker. Iterative, so a 9000-vertex ring cannot blow the stack."""
    if len(points) < 3:
        return points
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    tol2 = tol * tol
    while stack:
        a, b = stack.pop()
        if b <= a + 1:
            continue
        x1, y1 = points[a]
        x2, y2 = points[b]
        dx, dy = x2 - x1, y2 - y1
        den = dx * dx + dy * dy
        far, idx = -1.0, -1
        for i in range(a + 1, b):
            x, y = points[i]
            if den == 0:
                d = (x - x1) ** 2 + (y - y1) ** 2
            else:
                t = ((x - x1) * dx + (y - y1) * dy) / den
                t = 0.0 if t < 0 else (1.0 if t > 1 else t)
                px, py = x1 + t * dx, y1 + t * dy
                d = (x - px) ** 2 + (y - py) ** 2
            if d > far:
                far, idx = d, i
        if far > tol2:
            keep[idx] = True
            stack.append((a, idx))
            stack.append((idx, b))
    return [p for p, k in zip(points, keep) if k]


def _ring(coords, tol):
    """Simplify, round, de-duplicate, re-close. None if it stops being a ring."""
    pts = _simplify([(c[0], c[1]) for c in coords], tol)
    pts = [[round(x, PLACES), round(y, PLACES)] for x, y in pts]
    out = [pts[0]]
    for p in pts[1:]:
        if p != out[-1]:
            out.append(p)
    if out[0] != out[-1]:
        out.append(out[0])
    return out if len(out) >= 4 else None


def _polygons(geometry):
    if geometry is None:
        return []
    if geometry["type"] == "Polygon":
        return [geometry["coordinates"]]
    if geometry["type"] == "MultiPolygon":
        return geometry["coordinates"]
    return []


def _reduce(feature, tol):
    """Strip properties, simplify, drop sub-pixel parts. None if nothing left."""
    parts, dropped = [], 0
    for poly in _polygons(feature.get("geometry")):
        xs = [p[0] for p in poly[0]]
        ys = [p[1] for p in poly[0]]
        if math.hypot(max(xs) - min(xs), max(ys) - min(ys)) < MIN_PART_DIAG:
            dropped += 1
            continue
        rings, ok = [], True
        for i, r in enumerate(poly):
            rr = _ring(r, tol)
            if rr is None:
                if i == 0:          # outer ring collapsed: part is gone
                    ok = False
                    break
                continue            # a hole collapsed: harmless, skip it
            rings.append(rr)
        if ok and rings:
            parts.append(rings)
    if not parts:
        return None, dropped
    return {"type": "Feature", "properties": {},
            "geometry": {"type": "MultiPolygon", "coordinates": parts}}, dropped


# --------------------------------------------------------------------- source
def _fetch(key):
    name, want = SOURCES[key]
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        os.makedirs(CACHE, exist_ok=True)
        url = NE_BASE + name
        sys.stderr.write("fetching %s\n" % url)
        with urllib.request.urlopen(url, timeout=180) as r, open(path, "wb") as f:
            f.write(r.read())
    got = hashlib.sha256(open(path, "rb").read()).hexdigest()
    if got != want:
        sys.stderr.write(
            "error: %s sha256 %s, expected %s\n"
            "       upstream changed, or the cache is corrupt. Delete\n"
            "       %s and re-run; if it still differs, the pin in this script\n"
            "       must be reviewed deliberately, not bumped.\n"
            % (name, got, want, path))
        sys.exit(2)
    return json.load(open(path, encoding="utf-8"))


# --------------------------------------------------------------------- build
def build():
    out = {}

    admin0 = _fetch("admin0")
    feats, dropped = [], 0
    for f in admin0["features"]:
        g, d = _reduce(f, TOLERANCE_DEG)
        dropped += d
        if g:
            feats.append(g)
    out["land.geojson"] = {"type": "FeatureCollection", "features": feats}
    sys.stderr.write("land:   %d countries, %d sub-pixel parts dropped\n"
                     % (len(feats), dropped))

    admin1 = _fetch("admin1")
    feats, dropped = [], 0
    for f in admin1["features"]:
        if f["properties"].get("iso_a2") not in ADMIN1_ISO_A2:
            continue
        g, d = _reduce(f, TOLERANCE_DEG)
        dropped += d
        if g:
            feats.append(g)
    out["admin1.geojson"] = {"type": "FeatureCollection", "features": feats}
    sys.stderr.write("admin1: %d %s divisions, %d sub-pixel parts dropped\n"
                     % (len(feats), "/".join(ADMIN1_ISO_A2), dropped))

    return {k: json.dumps(v, separators=(",", ":")) + "\n" for k, v in out.items()}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if the committed output is stale")
    args = ap.parse_args()

    built = build()
    stale = False
    for name, text in built.items():
        path = os.path.join(OUT_DIR, name)
        current = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if args.check:
            if current != text:
                sys.stderr.write("stale: %s\n" % os.path.relpath(path, REPO))
                stale = True
            continue
        if current == text:
            sys.stderr.write("unchanged: %s\n" % os.path.relpath(path, REPO))
            continue
        os.makedirs(OUT_DIR, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        gz = len(gzip.compress(text.encode()))
        sys.stderr.write("wrote %s (%.0f kB, %.0f kB gzipped)\n"
                         % (os.path.relpath(path, REPO), len(text) / 1000, gz / 1000))
    if args.check and stale:
        sys.stderr.write("run: python3 tools/build_basemap.py\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
