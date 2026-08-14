#!/usr/bin/env python3
"""Generate the U.S. atlas GeoJSON from the canonical YAML evidence corpus.

    cases/*.yaml      -> docs/us/data/cases.geojson
    overlays/us.yaml  -> docs/us/data/overlays.geojson

Doctrine (see RECONCILIATION-2026-08-14.md):
  - `cases/*.yaml` is canonical. The GeoJSON is DERIVED and must never be
    edited by hand. This script is the only writer.
  - Generation is total, not incremental: the output is rebuilt from source
    every run, so a hand-edit to the GeoJSON is silently discarded on the next
    build and loudly reported by `--check` in the meantime.
  - Proposal-only: writes data files, never commits.

Usage:
    python3 tools/build_us_geojson.py            # write
    python3 tools/build_us_geojson.py --check    # exit 1 if output is stale
                                                 # (CI / pre-commit gate)
"""
import argparse
import glob
import json
import os
import sys

try:
    import yaml
except ImportError:
    sys.stderr.write("error: PyYAML required (pip install pyyaml)\n")
    sys.exit(2)

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASE_GLOB = os.path.join(REPO, "cases", "*.yaml")
OVERLAY_SRC = os.path.join(REPO, "overlays", "us.yaml")
CASE_OUT = os.path.join(REPO, "docs", "us", "data", "cases.geojson")
OVERLAY_OUT = os.path.join(REPO, "docs", "us", "data", "overlays.geojson")

# Properties the renderer reads, in render order. Anything not listed is
# editorial-internal and does not ship.
CASE_PROPS = [
    "case_id", "title", "utility_type", "control_layer",
    "affected_jurisdiction", "controlling_actor", "controlling_jurisdiction",
    "trigger", "public_consequence", "callout", "current_status",
    "affected_population_est", "status", "date_surfaced", "confidence",
    "one_line", "sources",
]

REQUIRED = [
    "case_id", "title", "utility_type", "control_layer", "controlling_actor",
    "trigger", "public_consequence", "affected_population_est", "status",
    "date_surfaced", "confidence", "one_line", "sources", "location",
]


def flatten_jurisdiction(v):
    """{locality, state} -> 'locality, state'. The renderer wants a string."""
    if v is None:
        return None
    if isinstance(v, str):
        return v
    parts = [v.get("locality"), v.get("state")]
    return ", ".join(p for p in parts if p)


def squash(v):
    """Normalise YAML folded-scalar whitespace to a single line."""
    if isinstance(v, str):
        return " ".join(v.split())
    return v


def load_cases():
    cases, errors = [], []
    for path in sorted(glob.glob(CASE_GLOB)):
        d = yaml.safe_load(open(path))
        rel = os.path.relpath(path, REPO)
        for f in REQUIRED:
            if d.get(f) in (None, "", []):
                errors.append(f"{rel}: missing required field `{f}`")
        loc = d.get("location") or {}
        if "lng" not in loc or "lat" not in loc:
            errors.append(f"{rel}: location needs `lng` and `lat`")
        for i, s in enumerate(d.get("sources") or []):
            for f in ("publisher", "url", "date"):
                if not s.get(f):
                    errors.append(f"{rel}: sources[{i}] missing `{f}`")
        cases.append((rel, d))
    return cases, errors


def build_cases(cases):
    feats = []
    for _, d in cases:
        props = {}
        for k in CASE_PROPS:
            if k not in d:
                continue
            v = d[k]
            if k in ("affected_jurisdiction", "controlling_jurisdiction"):
                v = flatten_jurisdiction(v)
            elif k == "sources":
                v = [{"publisher": s["publisher"], "url": s["url"],
                      "date": str(s["date"])} for s in v]
            else:
                v = squash(v)
            if v is not None:
                props[k] = v
        feats.append({
            "type": "Feature",
            "geometry": {"type": "Point",
                         "coordinates": [d["location"]["lng"],
                                         d["location"]["lat"]]},
            "properties": props,
        })
    feats.sort(key=lambda f: f["properties"]["case_id"])
    return {
        "type": "FeatureCollection",
        "_generated": "tools/build_us_geojson.py from cases/*.yaml — do not edit",
        "_evidence_window": max(
            s["date"] for f in feats for s in f["properties"]["sources"]),
        "features": feats,
    }


def build_overlays():
    if not os.path.exists(OVERLAY_SRC):
        return None, []
    src = yaml.safe_load(open(OVERLAY_SRC)) or {}
    feats, errors = [], []
    for case_id, polys in sorted((src.get("overlays") or {}).items()):
        for i, p in enumerate(polys):
            if p.get("role") not in ("affected", "control"):
                errors.append(
                    f"overlays/us.yaml: {case_id}[{i}] role must be "
                    f"affected|control, got {p.get('role')!r}")
            ring = [list(c) for c in p["polygon"]]
            if ring[0] != ring[-1]:
                ring.append(ring[0])          # close the ring
            feats.append({
                "type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": [ring]},
                "properties": {"case_id": case_id, "role": p["role"],
                               "label": p["label"],
                               "register": "interpreted"},
            })
    return {
        "type": "FeatureCollection",
        "_generated": "tools/build_us_geojson.py from overlays/us.yaml — do not edit",
        "_register": "interpreted — authored approximations of governance "
                     "footprints, not surveyed boundaries or physical routing",
        "features": feats,
    }, errors


def dump(obj):
    return json.dumps(obj, indent=2, ensure_ascii=False) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="verify outputs match source; exit 1 if stale")
    args = ap.parse_args()

    cases, errors = load_cases()
    overlays, ov_errors = build_overlays()
    errors += ov_errors
    if errors:
        for e in errors:
            sys.stderr.write("error: " + e + "\n")
        sys.stderr.write(f"\n{len(errors)} error(s); refusing to build.\n")
        return 2

    targets = [(CASE_OUT, dump(build_cases(cases)))]
    if overlays is not None:
        targets.append((OVERLAY_OUT, dump(overlays)))

    stale = []
    for path, text in targets:
        current = open(path).read() if os.path.exists(path) else None
        if current != text:
            stale.append(os.path.relpath(path, REPO))
            if not args.check:
                open(path, "w").write(text)

    if args.check:
        if stale:
            sys.stderr.write(
                "error: generated output is stale or hand-edited:\n  " +
                "\n  ".join(stale) +
                "\n\nRun: python3 tools/build_us_geojson.py\n")
            return 1
        print(f"ok: {len(cases)} cases, outputs match canonical source")
        return 0

    win = json.loads(targets[0][1])["_evidence_window"]
    print(f"wrote {len(cases)} cases -> {os.path.relpath(CASE_OUT, REPO)}")
    if overlays is not None:
        print(f"wrote {len(overlays['features'])} overlay polygons -> "
              f"{os.path.relpath(OVERLAY_OUT, REPO)}")
    print(f"evidence window (max source date): {win}")
    if stale:
        print(f"changed: {', '.join(stale)}")
    else:
        print("no change")
    return 0


if __name__ == "__main__":
    sys.exit(main())
