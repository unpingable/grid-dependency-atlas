#!/usr/bin/env python3
"""Build the Hormuz grammar specimen from the existing corpus.

    docs/hormuz/data/countries.geojson  ->  docs/hormuz/index.html

This is a SPIKE, not a shipping page. It exists to test whether the grammar in
ATLAS-DESIGN-GRAMMAR.md makes the *existing* evidence and its *limitations*
more legible. Constraints it holds itself to:

  - No new research. Every fact on the page comes from the GeoJSON.
  - No prose rewriting. Country claims and confidence notes are verbatim.
  - Derived values state their rule (grammar R5). There are exactly two on this
    page and both are computed here, in view: the evidence window, and the
    reserve-figure qualifier flag.
  - `stress_band` renders as `interpreted`, per the repository-history finding
    that no derivation rule was ever specified for it. The map is a secondary
    figure drawn in neutral ink so it cannot read as measurement.
  - No JavaScript. The page is static, printable, readable without scripts.

v2 (editorial reduction pass): summary strip for the 20-second read; prose cut
against "does removing this lose a claim, qualification, or boundary?"; the
qualification types separated by weight rather than concealment; the map back as
a large *secondary*, explicitly interpreted figure; more air between moves.
No architecture change.

Usage:  python3 tools/build_atlas_hormuz.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atlas_core import (  # noqa: E402
    CSS as CORE_CSS, e, w, cap, days_between, evidence_window, rings,
    load_substrate, svg_path, centroid, place_labels, head, evidence_banner,
    register_line, register_definitions, audit_divider, receipts_table,
    require_subject_fields)

# Hormuz-only editorial styling. Everything generic lives in atlas_core.
CSS = CORE_CSS + """
.ledger .mix{display:block;font-family:var(--mono);font-size:10.5px;color:var(--tx-faint);
  margin-top:5px}
.ledger .cope{display:block;font-size:12.5px;color:var(--tx-dim);line-height:1.5;
  margin-top:6px;max-width:88ch}
.ledger .cope b{color:var(--tx-mid);font-weight:600}
/* ---------- the turn ---------- */
.turn{border-top:1px solid var(--rule)}
.turn .e{padding:20px 0;border-bottom:1px solid var(--rule-soft);
  display:grid;grid-template-columns:150px 1fr;gap:22px}
.turn .cn{font-family:var(--serif);font-size:21px;font-weight:600;color:#fff;
  line-height:1.15}
.turn .tag{display:block;font-family:var(--mono);font-size:9.5px;letter-spacing:.09em;
  text-transform:uppercase;color:#b4655f;margin-top:6px}
.turn .st{font-size:15px;color:#c3ccd5;line-height:1.55}
.turn .st .lab{display:block;font-family:var(--mono);font-size:9.5px;
  letter-spacing:.09em;text-transform:uppercase;color:var(--tx-faint);margin-bottom:5px}
.turn .refuse{color:var(--refused)}
.payoff{font-family:var(--serif);font-size:25px;line-height:1.34;color:#fff;
  max-width:40ch;margin:34px 0 0}
.payoff span{color:var(--derived)}

"""

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "docs", "hormuz", "data", "countries.geojson")
OUT_DIR = os.path.join(REPO, "docs", "hormuz")
OUT = os.path.join(OUT_DIR, "index.html")
# Cartographic substrate. NOT evidence, NOT part of the claim corpus.
# Provenance: vendor/boundaries/PROVENANCE.md
SUBSTRATE = os.path.join(REPO, "vendor", "boundaries", "ne_50m_admin0_subset.geojson")
SUBSTRATE_NOTE = ("Natural Earth 1:50m Admin 0, v5.1.2, public domain "
                  "(vendor/boundaries/PROVENANCE.md)")

# Corpus country name -> ISO A3. Explicit so the join is auditable; the build
# fails if a corpus country has no mapping rather than silently dropping it.
ISO = {"Philippines": "PHL", "Sri Lanka": "LKA", "Bangladesh": "BGD",
       "Thailand": "THA", "South Korea": "KOR", "Vietnam": "VNM",
       "India": "IND", "Japan": "JPN", "Singapore": "SGP",
       "Pakistan": "PAK", "Taiwan": "TWN", "Cuba": "CUB"}

TODAY = "2026-08-14"   # passed in rather than computed, so the build is reproducible

# DISPLAY ORDER ONLY -- not a severity ranking. The corpus's five classes are
# not commensurable: "Already stressed" is a present state, "Acute if disruption
# persists" is a conditional, "Price shock first, physical shortage later" is a
# sequencing claim, "Resilient but expensive" is a cost judgment. Nothing in the
# corpus orders them, so this page must not either. An earlier draft of this
# specimen ranked them and called two of them "severest" -- that ordering was
# invented here, not found in the corpus, and has been removed.
BAND_DISPLAY_ORDER = ["already_stressed", "acute_if_persists", "price_shock_first",
                      "resilient_but_expensive", "special_case"]

# Categorical hues: distinct, restrained, NOT a gradient. Deliberately not a
# ramp, because a ramp would assert an ordering the corpus does not have.
BAND_INK = {
    "already_stressed":        "#e08b76",
    "acute_if_persists":       "#d7b169",
    "price_shock_first":       "#7fb3c9",
    "resilient_but_expensive": "#8fae8c",
    "special_case":            "none",
}

# --- derived-value rules, stated here and restated on the page ---------------
RANGE_RE = re.compile(r"(\d+)\s*[-–]\s*(\d+)\s*days", re.I)
# Counts a NARROWER QUANTITY than "days of reserve" -- not comparable on one axis.
BASIS_RE = re.compile(r"strategic oil|working LNG|foreign-owned", re.I)
# Counts the SAME quantity, imprecisely -- comparable, but not as a point.
PRECISION_RE = re.compile(r"estimates vary|data weak", re.I)


def load():
    d = json.load(open(SRC))
    out = []
    for f in d["features"]:
        p = dict(f["properties"])
        if isinstance(p.get("sources"), str):
            p["sources"] = json.loads(p["sources"])
        p["_geom"] = f["geometry"]
        out.append(p)
    return out


def quality(c):
    """DERIVED. Sorts each published reserve figure by what it actually counts,
    reading only the country's own confidence_note.

      kind 'other'  -- the note names a narrower basis than the label
                       (strategic oil, working LNG, foreign-owned storage).
                       Not the same quantity; must not share an axis.
      kind 'ranged' -- the note gives an explicit day-range, or says the
                       estimate varies. Same quantity, published as a span;
                       the corpus stores only a point.
      kind 'total'  -- no qualification recorded.

    Applied mechanically, no per-row judgment."""
    if c.get("reserve_days") is None:
        return {"kind": "none", "note": c.get("confidence_note") or ""}
    note = c.get("confidence_note") or ""
    basis = BASIS_RE.search(note)
    if basis:
        return {"kind": "other", "phrase": basis.group(0), "note": note}
    rng = RANGE_RE.search(note)
    prec = PRECISION_RE.search(note)
    if rng or prec:
        d = {"kind": "ranged", "note": note,
             "phrase": prec.group(0) if prec else "published as a range"}
        if rng:
            d["lo"], d["hi"] = int(rng.group(1)), int(rng.group(2))
        return d
    return {"kind": "total", "note": note}







def render():
    cs = load()
    all_dates = sorted({s["date"] for c in cs for s in c["sources"]})
    window_lo, window_hi = all_dates[0], all_dates[-1]
    stale = days_between(window_hi, TODAY)
    n_receipts = sum(len(c["sources"]) for c in cs)

    QQ = {c["country"]: quality(c) for c in cs}
    have = [c for c in cs if c.get("reserve_days") is not None]
    missing = [c for c in cs if c.get("reserve_days") is None]
    comparable = [c for c in have if QQ[c["country"]]["kind"] in ("total", "ranged")]
    other_basis = [c for c in have if QQ[c["country"]]["kind"] == "other"]
    n_ranged = sum(1 for c in comparable if QQ[c["country"]]["kind"] == "ranged")

    def lo_of(c): return QQ[c["country"]].get("lo", c["reserve_days"])
    def hi_of(c): return QQ[c["country"]].get("hi", c["reserve_days"])
    comparable.sort(key=lo_of)
    under = [c for c in comparable if hi_of(c) < 60]
    straddle = [c for c in comparable if lo_of(c) < 60 <= hi_of(c)]

    maxv = 280
    def pct(v): return 100.0 * v / maxv

    o = []
    A = o.append

    # ================= masthead: lead with the world =================
    A(f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Where a Hormuz shock leaves the least room for error</title>
<meta name="description" content="Twelve countries under a Strait of Hormuz disruption: published fuel margins, declared emergencies, and the countries whose condition looks worst but publish no figure at all.">
<link rel="preconnect" href="https://fonts.bunny.net">
<link rel="stylesheet" href="https://fonts.bunny.net/css?family=newsreader:400,500,600&display=swap">
<style>{CSS}</style></head><body>

<div class="evbanner">
<span class="big">Evidence current to {window_hi} — {stale} days ago</span>
Every present-tense claim below is present tense as of {window_hi}, not as of reading.
Built from <code>docs/hormuz/data/countries.geojson</code>.
</div>

<div class="wrap">

<div class="kicker">Hormuz Energy · Infrastructure Dependency Atlas</div>
<h1>Where a Hormuz shock leaves the least room for error</h1>

<div class="answer">
The Philippines declared a national energy emergency with <strong>forty-five days</strong>
of fuel in reserve. Thailand, at ninety-five, has ordered civil servants to take the
stairs. Vietnam publishes a margin of twenty to forty-five days and is buying Russian
crude. Those are the countries that publish a number at all — and across the twelve,
<strong>the ones whose condition reads worst are the ones with no number to read.</strong>
</div>

<div class="strip">
  <div class="s"><div class="n">12</div><div class="l">countries assessed</div></div>
  <div class="s"><div class="n">{len(have)}</div><div class="l">publish a reserve figure</div></div>
  <div class="s anom"><div class="n">{len(missing)}</div><div class="l">publish none at all</div></div>
  <div class="s anom"><div class="n">{len(other_basis)}</div><div class="l">of the {w(len(have))} count something else</div></div>
</div>

<div class="stamp">
  <span><b>EVIDENCE WINDOW OPENS</b> {window_lo}</span>
  <span><b>RECEIPTS</b> {n_receipts}</span>
  <span><b>COUNTRIES</b> 12</span>
</div>

<div class="regline">
  <span class="o">●</span> observed &nbsp;·&nbsp; <span class="d">◌</span> derived
  &nbsp;·&nbsp; <span class="i">▌</span> interpreted &nbsp;·&nbsp;
  <span class="r">⊘</span> refused &nbsp;— marks appear beside claims; defined under Method.
</div>
""")

    # ================= primary: published margins =================
    A("""<div class="sec"><div class="rung">Published margins · observed</div>
<figure>
<figcaption>%s countries publish a margin entirely under sixty days. %s straddles the line.</figcaption>
<div class="fignote">Days of national reserve, for the %s countries whose published figure
counts that quantity. Where the source gives a range, the range is drawn; the tick marks
the single value the corpus stores.</div>
<div class="bars">""" % (cap(len(under)), cap(len(straddle)), w(len(comparable))))

    for c in comparable:
        q = QQ[c["country"]]
        lo, hi, v = lo_of(c), hi_of(c), c["reserve_days"]
        if q["kind"] == "ranged" and hi > lo:
            bar = ('<div class="span" style="left:%.2f%%;width:%.2f%%"></div>'
                   '<div class="pt" style="left:%.2f%%"></div>'
                   % (pct(lo), pct(hi) - pct(lo), pct(v)))
            val, note = "%d–%d d" % (lo, hi), \
                '<div class="note">source range; corpus stores %d</div>' % v
        else:
            bar = '<div class="bar" style="width:%.2f%%"></div>' % pct(v)
            val, note = "%d d" % v, ""
        A("""<div class="row">
  <div class="nm">%s</div>
  <div class="tr"><div class="sixty" style="left:%.2f%%"></div>%s</div>
  <div class="val">%s</div>
  %s
</div>""" % (e(c["country"]), pct(60), bar, val, note))

    A("""</div>
<div class="axis"><div></div><div class="tr">
  <span class="tick" style="left:0%%">0</span>
  <span class="tick" style="left:%.2f%%">60</span>
  <span class="tick" style="left:%.2f%%">120</span>
  <span class="tick" style="left:%.2f%%">180</span>
  <span class="tick" style="left:%.2f%%">240</span>
</div><div></div></div>""" % (pct(60), pct(120), pct(180), pct(240)))

    A("""<div class="offaxis">
  <div class="t">Published — but counting something else</div>
  <div class="d">These have a number. It is not the number above, so it is not drawn
  against that axis.</div>
  <table class="offtbl"><tbody>""")
    for c in other_basis:
        A("""<tr><td class="k">%s</td><td class="n">%d d</td>
<td class="wq"><q>%s</q></td></tr>""" % (e(c["country"]), c["reserve_days"],
                                         e(QQ[c["country"]]["note"])))
    A("</tbody></table></div>")

    A(f"""<div class="figfoot">
  <span><b>WINDOW</b> {window_lo} → {window_hi}</span>
  <span><b>n</b> {len(have)} of 12 publish a figure — the other {len(missing)} are below</span>
  <span><b>UNIT</b> days</span>
</div>
</figure>

<div class="interp">
<p>Reserve depth measures how long a country can absorb a shortfall, not whether it can
distribute what it has. The Philippines declared an emergency at 45 days; Thailand, at 95,
has not. Those are not two points on one scale.</p>
<div class="by">▌Interpreted</div>
</div></div>""")

    # ================= the turn =================
    A(f"""<div class="sec"><div class="rung">The other five</div>
<h2>The missing bar is the bar</h2>
<div class="lede">{cap(len(missing))} of the twelve publish no reserve figure. This is what
the corpus records them doing instead — their own <code>current_status</code>, verbatim.</div>
<div class="turn">""")

    for c in missing:
        refuse = c["country"] == "Cuba"
        A("""<div class="e">
  <div><div class="cn">%s</div>
    <span class="tag">%s</span></div>
  <div class="st%s"><span class="lab">Current status · as of %s</span>%s</div>
</div>""" % (e(c["country"]),
             "⊘ not a hormuz case" if refuse else "no reserve figure",
             " refuse" if refuse else "",
             e(c.get("status_asof") or window_hi), e(c["current_status"])))

    A(f"""</div>
<div class="figfoot">
  <span><b>OBSERVED</b> status text and the absence of a reserve figure, per-country receipts</span>
  <span><b>WINDOW</b> {window_lo} → {window_hi}</span>
</div>

<div class="payoff">Military at the fuel depots, universities shut, queues reintroduced —
and <span>no figure to rank any of it by</span>.</div>

<div class="interp" style="margin-top:26px">
<p>Cuba disclaims membership in its own entry, and is kept because the corpus keeps it —
marked <span class="mk mk-r">refused</span> rather than quietly dropped. An atlas that
silently drops its awkward row is not showing you the corpus.</p>
<div class="by">▌Interpreted</div>
</div></div>""")
    # ============ secondary figure: the interpreted map ============
    SMALL = set()
    sub = load_substrate(SUBSTRATE)
    unmapped = [c["country"] for c in cs if ISO.get(c["country"]) not in sub]
    if unmapped:
        raise SystemExit("no boundary substrate for: %s" % ", ".join(unmapped))
    # The rendered geometry is the substrate. The corpus polygons
    # (countries.geojson `geometry`) are deliberately NOT drawn: they are
    # 9-31 vertex hand sketches, and rendering them implied a cartographic
    # fidelity the corpus does not have. They remain in the corpus untouched.
    for c in cs:
        c["_geom"] = sub[ISO[c["country"]]]
    asia = [c for c in cs if c["country"] != "Cuba"]
    cuba = next(c for c in cs if c["country"] == "Cuba")

    MW, MH = 800, 452
    L0, L1, B0, B1 = 59.0, 147.0, 0.0, 46.0
    KX = 0.927                                   # cos(~22N), keeps shapes sane
    sc = min((MW - 34) / ((L1 - L0) * KX), (MH - 40) / (B1 - B0))
    OX, OY = 17, 22

    def mx(lng): return OX + (lng - L0) * KX * sc
    def my(lat): return OY + (B1 - lat) * sc

    A(f"""<div class="sec"><div class="rung">Secondary evidence · interpreted</div>
<figure>
<figcaption>The classification, mapped. Nothing in this shape is measured.</figcaption>
<div class="fignote">Fill encodes the corpus's <span class="mk mk-i">stress_band</span> —
an authored assessment class with no derivation rule (see Method). The colours are
<b>categorical, not a scale</b>: the classes describe different kinds of thing, and nothing
in the corpus ranks them. Hatching marks the countries with no published reserve
figure.</div>
<svg viewBox="0 0 {MW} {MH}" width="100%" role="img"
 aria-label="Schematic map of eleven Asian countries shaded by an authored stress classification, with hatching on the five that publish no reserve figure, and Cuba shown separately as a refused non-case.">
<defs>
  <pattern id="hatch" width="6" height="6" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
    <line x1="0" y1="0" x2="0" y2="6" stroke="#0a0a0a" stroke-width="2.6" opacity="0.6"/>
  </pattern>
</defs>
<rect x="0" y="0" width="{MW}" height="{MH}" fill="#0c0e11"/>""")

    lbl_items, marks = [], []
    small = SMALL   # filled below; Method reports the actual set
    geo_of = {}
    for c in asia:
        g = c["_geom"]
        geo_of[c["country"]] = g
        ink = BAND_INK[c["stress_band"]]
        nul = c.get("reserve_days") is None
        d = svg_path(g, mx, my)
        A('  <path d="%s" fill="%s" fill-opacity="0.7" stroke="#818b96" stroke-width="0.7" '
          'stroke-opacity="0.95" stroke-linejoin="round"/>' % (d, ink))
        if nul:
            A('  <path d="%s" fill="url(#hatch)" stroke="#e8eef4" stroke-width="1" '
              'stroke-dasharray="3 2.5" stroke-opacity="0.8"/>' % d)
        cxg, cyg = centroid(g)
        px, py = mx(cxg), my(cyg)
        # Sub-pixel countries (Singapore, Taiwan) would otherwise vanish. A
        # minimum mark keeps them present; it exaggerates area, which is why
        # area is not an encoding on this map.
        pxs = [mx(q[0]) for r in rings(g) for q in r]
        pys = [my(q[1]) for r in rings(g) for q in r]
        if max(pxs) - min(pxs) < 9 or max(pys) - min(pys) < 9:
            A('  <circle cx="%.1f" cy="%.1f" r="5" fill="%s" fill-opacity="0.72" '
              'stroke="%s" stroke-width="%s" stroke-dasharray="%s"/>'
              % (px, py, ink, "#e8eef4" if nul else "#0a0a0a",
                 "1" if nul else "0.8", "3 2.5" if nul else "0"))
            small.add(c["country"])
        marks.append((px - 4, px + 4, py))
        wpx = 6.2 * len(c["country"]) + 4
        pref = py + (16 if c["country"] in small else 3)
        lbl_items.append((c["country"], px - wpx / 2, px + wpx / 2, pref))

    ys = place_labels(lbl_items, pad_y=11.5,
                      bounds=(OY + 8, OY + (B1 - B0) * sc - 4), obstacles=marks)
    for c in asia:
        cxg, cyg = centroid(geo_of[c["country"]])
        px, py = mx(cxg), my(cyg)
        ly = ys[c["country"]]
        on_fill = (c["stress_band"] in ("already_stressed", "acute_if_persists")
                   and c["country"] not in small)
        moved = abs(ly - (py + 3)) > 5
        if moved:
            # leader stops just short of the label, above or below as needed
            y2 = ly - 9 if ly > py else ly + 4
            if abs(y2 - py) > 3:
                A('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#59636e" '
                  'stroke-width="0.9"/>' % (px, py, px, y2))
        # dark ink on the light fills, light ink elsewhere; halo either way so
        # the label survives the hatch
        ink = "#0d1116" if (on_fill and not moved) else "#dfe6ed"
        halo = "#e9eff5" if (on_fill and not moved) else "#0a0c0f"
        A('  <text x="%.1f" y="%.1f" text-anchor="middle" font-size="10.5" '
          'font-family="-apple-system,sans-serif" fill="%s" stroke="%s" '
          'stroke-width="2.6" stroke-linejoin="round" paint-order="stroke" '
          'font-weight="500">%s</text>' % (px, ly, ink, halo, e(c["country"])))

    # Cuba inset -- the refusal, rendered rather than dropped
    IX, IY, IS = MW - 138, MH - 104, 4.8
    def cxf(lng): return IX + (lng + 86.0) * KX * IS
    def cyf(lat): return IY + (24.6 - lat) * IS
    A("""  <rect x="%d" y="%d" width="120" height="74" fill="none" stroke="#2b3138"
    stroke-dasharray="3 3"/>
  <path d="%s" fill="none" stroke="#aab3bd" stroke-width="1.6" stroke-dasharray="3 2.5"/>
  <text x="%d" y="%d" font-size="9.5" font-family="ui-monospace,monospace"
    fill="#79828c">%s CUBA — 220%s AWAY</text>
  <text x="%d" y="%d" font-size="9.5" font-family="ui-monospace,monospace"
    fill="#69727c">%sNot a Hormuz case.%s</text>"""
      % (IX - 8, IY - 8, svg_path(cuba["_geom"], cxf, cyf),
         IX - 8, IY - 14, "⊘", "°",
         IX - 8, IY + 80, "“", "”"))

    lx, ly0 = 34, 320
    A('  <text x="%d" y="%d" font-size="9.5" font-family="ui-monospace,monospace" '
      'fill="#8b949e" letter-spacing="1">ASSESSMENT CLASS — CATEGORICAL</text>' % (lx, ly0 - 8))
    for i, b in enumerate(BAND_DISPLAY_ORDER[:4]):
        yy = ly0 + i * 17
        lab = next(c["stress_label"] for c in cs if c["stress_band"] == b)
        A('  <rect x="%d" y="%d" width="11" height="11" fill="%s" fill-opacity="0.72"/>'
          '<text x="%d" y="%.1f" font-size="9" font-family="-apple-system,sans-serif" '
          'fill="#97a0aa">%s</text>' % (lx, yy, BAND_INK[b], lx + 16, yy + 9.5, e(lab.split(',')[0])))
    yy = ly0 + 4 * 17 + 6
    A('  <rect x="%d" y="%d" width="11" height="11" fill="#3a424b" stroke="#e8eef4" '
      'stroke-width="1" stroke-dasharray="2 2" stroke-opacity="0.8"/>'
      '<text x="%d" y="%.1f" font-size="9" font-family="-apple-system,sans-serif" '
      'fill="#97a0aa">no reserve figure</text>' % (lx, yy, lx + 16, yy + 9.5))

    A(f"""</svg>
<div class="figfoot">
  <span><b>n</b> 11 in frame · Cuba inset</span><br>
  <span class="long"><b>INTERPRETED</b> every fill. Shade encodes an authored band; neither
  it nor land area encodes a measured quantity.</span>
  <span class="long"><b>SUBSTRATE</b> national boundaries are reference geography, not
  evidence — they carry no claim (source in Method).</span>
  <span class="long"><b>OBSERVED</b> only the hatch — whether a reserve figure exists.</span>
</div>
</figure></div>""")

    # ============ why the classification can mislead ============
    A(f"""<div class="sec"><div class="rung">Qualification</div>
<h2>What each published figure counts</h2>
<div class="lede">The receipts for the split above. The corpus stores one integer per
country; each country's own confidence note says what that integer is.</div>
<div class="scroll"><table>
<thead><tr><th>Country</th><th>Stored</th><th>What the corpus says about that figure — verbatim</th><th>Treated as</th></tr></thead><tbody>""")

    KINDLBL = {"total": ('<span style="color:var(--tx-faint)">on the axis</span>'),
               "ranged": '<span class="mk mk-d">range</span>',
               "other": '<span class="mk mk-d">off the axis</span>'}
    for c in have:
        q = QQ[c["country"]]
        A("""<tr><td class="k">%s</td><td class="n">%d d</td>
<td><q>%s</q></td>
<td class="n">%s</td></tr>""" % (
            e(c["country"]), c["reserve_days"], e(c["confidence_note"]),
            KINDLBL[q["kind"]]))

    A(f"""</tbody></table></div>
<div class="figfoot">
  <span class="long"><b>DERIVED</b> the flag. A figure is flagged when its own confidence
  note contains an explicit day-range, or names a basis narrower than the label —
  “strategic oil”, “working LNG”, “foreign-owned”, “estimates vary”, “data weak”. Applied
  mechanically, no per-row judgment. {len(comparable)} on the axis ({n_ranged} as ranges),
  {len(other_basis)} off it.</span>
</div>

<div class="interp">
<p>South Korea's 210 days is strategic <em>oil</em>; its working LNG inventory is nine.
None of this is new research — every word was already in the corpus, in a field the
published map renders as a footnote.</p>
<div class="by">▌Interpreted · not evidence</div>
</div>""")

    # scatter: second exhibit in the same section
    pts = [c for c in cs if c.get("hormuz_oil_pct") is not None
           and c.get("gen_fossil_pct") is not None]
    SW, SH, PL, PB, PT, PR = 720, 384, 50, 66, 26, 22
    def sx(v): return PL + (SW - PL - PR) * v / 100.0
    def sy(v): return PT + (SH - PT - PB) * (1 - v / 100.0)

    A(f"""<figure class="support" style="margin-top:72px">
<figcaption>The inputs that do exist put the unmeasured countries in the worst corner.</figcaption>
<div class="fignote">Share of oil arriving through the strait against fossil share of
generation — the two dimensions published for nearly everyone. Dashed rings have no
reserve figure.</div>
<svg viewBox="0 0 {SW} {SH}" width="100%" role="img"
  aria-label="Scatter plot of chokepoint oil import share against fossil share of generation for eleven countries. Bangladesh and Pakistan sit at the extreme right; Singapore at the top.">
  <rect x="{PL}" y="{PT}" width="{SW-PL-PR}" height="{SH-PT-PB}" fill="#0c0e11" stroke="#1c2025"/>""")

    for g in (25, 50, 75):
        A('  <line x1="%.1f" y1="%d" x2="%.1f" y2="%d" stroke="#161a1e"/>'
          % (sx(g), PT, sx(g), SH - PB))
        A('  <line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="#161a1e"/>'
          % (PL, sy(g), SW - PR, sy(g)))
    A('  <rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="#ef5350" opacity="0.05"/>'
      % (sx(75), sy(100), sx(100) - sx(75), sy(70) - sy(100)))
    A('  <text x="%.1f" y="%.1f" fill="#ef5350" font-size="10.5" '
      'font-family="ui-monospace,monospace" opacity="0.8">&#8805;75%% imported &#183; '
      '&#8805;70%% fossil</text>' % (sx(75.8), sy(98.5)))

    obst = [(sx(c["hormuz_oil_pct"]) - 7, sx(c["hormuz_oil_pct"]) + 7,
             sy(c["gen_fossil_pct"]) + 4) for c in pts]
    # the quadrant caption occupies real estate too
    obst.append((sx(75.8), sx(75.8) + 168, sy(98.5)))
    for c in pts:
        x, y = sx(c["hormuz_oil_pct"]), sy(c["gen_fossil_pct"])
        nul = c.get("reserve_days") is None
        A('  <circle cx="%.1f" cy="%.1f" r="5" fill="%s" stroke="%s" stroke-width="%s" '
          'stroke-dasharray="%s" opacity="0.92"/>'
          % (x, y, "none" if nul else "#4fc3f7", "#ef5350" if nul else "#4fc3f7",
             "1.6" if nul else "1", "3 2" if nul else "0"))

    items = []
    for c in sorted(pts, key=lambda c: -c["gen_fossil_pct"]):
        x, y = sx(c["hormuz_oil_pct"]), sy(c["gen_fossil_pct"])
        anchor = "end" if c["hormuz_oil_pct"] > 82 else "start"
        dx = -10 if anchor == "end" else 10
        wpx = 6.6 * len(c["country"]) + 6
        lxp = x + dx
        x0, x1 = (lxp - wpx, lxp) if anchor == "end" else (lxp, lxp + wpx)
        items.append((c["country"], x0, x1, y + 4))
    lys = place_labels(items, pad_y=12.5, bounds=(PT + 8, SH - PB - 6), obstacles=obst)
    for c in pts:
        x, y = sx(c["hormuz_oil_pct"]), sy(c["gen_fossil_pct"])
        anchor = "end" if c["hormuz_oil_pct"] > 82 else "start"
        dx = -10 if anchor == "end" else 10
        ly = lys[c["country"]]
        if abs(ly - (y + 4)) > 6:
            A('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#39414a" '
              'stroke-width="1"/>' % (x + dx * 0.45, y + 2, x + dx * 0.8, ly - 3))
        A('  <text x="%.1f" y="%.1f" text-anchor="%s" fill="#a9b2bc" font-size="11.5" '
          'font-family="-apple-system,sans-serif">%s</text>'
          % (x + dx, ly, anchor, e(c["country"])))

    ax_y = SH - PB + 18
    A(f"""  <text x="{PL}" y="{ax_y}" fill="#69727c" font-size="10.5" font-family="ui-monospace,monospace">0%</text>
  <text x="{(PL+SW-PR)/2:.0f}" y="{ax_y}" fill="#69727c" font-size="10.5" text-anchor="middle" font-family="ui-monospace,monospace">Share of oil imports through the strait →</text>
  <text x="{SW-PR}" y="{ax_y}" fill="#69727c" font-size="10.5" text-anchor="end" font-family="ui-monospace,monospace">100%</text>
  <text transform="translate(15,{(PT+SH-PB)/2:.0f}) rotate(-90)" fill="#69727c" font-size="10.5" text-anchor="middle" font-family="ui-monospace,monospace">Fossil share of generation →</text>
  <g font-family="ui-monospace,monospace" font-size="10" fill="#69727c">
    <circle cx="{PL+5}" cy="{SH-16}" r="5" fill="#4fc3f7" opacity="0.92"/>
    <text x="{PL+16}" y="{SH-12}">reserve figure published</text>
    <circle cx="{PL+188}" cy="{SH-16}" r="5" fill="none" stroke="#ef5350" stroke-width="1.6" stroke-dasharray="3 2"/>
    <text x="{PL+199}" y="{SH-12}">no reserve figure</text>
  </g>
</svg>
<div class="figfoot">
  <span><b>n</b> 11 of 12 — Cuba has no recorded import share</span>
  <span><b>OBSERVED</b> both axes</span><br>
  <span><b>DENOM</b> oil imports by volume; generation by share of output</span>
  <span><b>DERIVED</b> the shaded quadrant, drawn for reading only</span>
</div>
</figure></div>""")

    # ============ country evidence ============
    A("""<div class="sec"><div class="rung">Country evidence</div>
<h2>The twelve</h2>
<div class="lede">Each claim as the corpus states it, against what is measured behind it.
Every band is an authored judgment.</div>
<div class="scroll"><table class="ledger">
<thead><tr><th>Country</th><th>Interpreted band</th><th>Conf.</th><th>Oil</th><th>LNG</th><th>Reserve</th><th>Fossil</th></tr></thead><tbody>""")

    order = {b: i for i, b in enumerate(BAND_DISPLAY_ORDER)}
    def cell(v, unit="%"):
        return ('<td class="n">%s%s</td>' % (v, unit)) if v is not None \
            else '<td class="n miss">none</td>'
    for c in sorted(cs, key=lambda c: (order.get(c["stress_band"], 9),
                                       c["reserve_days"] if c["reserve_days"] is not None else -1)):
        A("""<tr class="lr">
  <td class="k cty">%s</td>
  <td class="bandc">%s</td>
  <td class="n cf-%s">%s</td>
  %s%s%s%s
</tr>
<tr class="claimrow"><td colspan="7"><span class="cl">%s</span>
<span class="mix">%s</span>
<span class="cope"><b>If it persists:</b> %s <b>Capacity to ration:</b> %s</span>%s</td></tr>""" % (
            e(c["country"]), e(c["stress_label"]), e(c["confidence"]), e(c["confidence"]),
            cell(c.get("hormuz_oil_pct")), cell(c.get("hormuz_lng_pct")),
            cell(c.get("reserve_days"), " d"), cell(c.get("gen_fossil_pct")),
            e(c["one_line"]), e(c["gen_mix_summary"]),
            e(c["alternative_supply"]), e(c["rationing_capacity"]),
            ('<span class="qn">%s</span>' % e(c["confidence_note"]))
            if c.get("reserve_days") is None else ""))
    A("</tbody></table></div></div>")


    # ================= audit floor =================
    A("""<div class="auditline">Audit<span>Everything below is the page checking itself: limits, method, and the source record.</span></div>

<div class="sec audit"><div class="rung">Audit · what the marks mean</div>
<div class="regdefs">
  <div class="r-observed"><div class="rl">● Observed</div><div class="rd">Read off a cited source. Has a unit and a receipt.</div></div>
  <div class="r-derived"><div class="rl">◌ Derived</div><div class="rd">Computed here. Shows its rule; carries no receipt.</div></div>
  <div class="r-interpreted"><div class="rl">▌Interpreted</div><div class="rd">Authored judgment. Publishable — and not evidence.</div></div>
  <div class="r-refused"><div class="rl">⊘ Refused</div><div class="rd">Declined or unavailable. Shown, not omitted.</div></div>
</div>
<div class="refusal">
<b>What this page does not claim.</b> That the disruption will persist. That any country
will ration, or when. That the assessments here are forecasts, rankings of suffering, or
probabilities.
</div></div>""")
    # ============ boundary ============
    A(f"""<div class="sec audit bound"><div class="rung">Audit · boundary conditions</div>
<h2>What this page does not show</h2>
<div class="pull">The five countries with no reserve figure are not the least exposed.
They are the least measured.</div>
<ul>
<li><b>{cap(len(missing))} of twelve publish no reserve figure</b> —
{e(', '.join(c['country'] for c in missing))}. Their assessments rest on current-status
reporting and generation mix alone, and two carry <code>confidence: low</code>.</li>
<li><b>Even the comparable figures are not equally solid</b> — {w(n_ranged)} of the
{w(len(comparable))} on the axis are ranges the corpus flattened to a point. The range is drawn;
the point it stores is marked.</li>
<li><b>Bands are exposure, not forecast.</b> No probability, date, or ordering of harm
attaches to any of them, and none should be read off the shading of a map.</li>
<li><b>National aggregates say nothing about distribution.</b> A country with 95 days of
national reserve can still have a province out of diesel on day nine.</li>
</ul></div>""")

    small_list = sorted(SMALL)
    small_txt = (" and ".join(small_list) if len(small_list) < 3
                 else ", ".join(small_list[:-1]) + " and " + small_list[-1]) or "no country"
    small_pron = "its" if len(small_list) == 1 else "their"

    sub_note = SUBSTRATE_NOTE

    # ============ method ============
    A(f"""<div class="sec audit meth"><div class="rung">Audit · method</div>
<h2>How the bands were assigned</h2>
<div class="rule1">They were assigned by judgment. No derivation rule was ever specified
for <code>stress_band</code>, and none can honestly be reconstructed.</div>
<p>The field was introduced in commit <code>1ecc1de</code> (2026-03-29) and never edited.
That commit names the inputs — “12 countries scored on 7 dimensions” — then enumerates
which country landed in which band. It states no threshold, weight, or ordering rule; its
own framing is <i>“stress bands, not countdown clocks.”</i> The repository's
<code>schema.yaml</code> governs the U.S. case corpus only. No threshold table exists
anywhere in the repository or its siblings.</p>
<p><b>Nor are the classes a scale.</b> “Already stressed” is a present state, “acute if
disruption persists” a conditional, “price shock first, physical shortage later” a
sequencing claim, “resilient but expensive” a cost judgment. They describe different kinds
of thing, and nothing in the corpus ranks them — so nothing here does. The map's colours
are categorical for that reason, and an earlier draft of this page that ordered the classes
and called two of them “severest” was wrong: that ranking was invented here, not found in
the corpus.</p>
<p>A formula could be back-fitted to the twelve current values. That would be an invention
presented as a method, so it has not been done. <b><code>stress_band</code> therefore
renders as <span class="mk mk-i">interpreted</span> everywhere it appears</b> — including
on the map above, which is drawn in neutral ink for that reason.</p>
<p>The named inputs, so the judgment is at least inspectable: chokepoint oil share,
chokepoint LNG share, reserve days, generation mix, current status, alternative supply,
rationing capacity. Four of the twelve are missing at least one; Cuba is missing three.</p>
<p><b>The map's geography is not the corpus's.</b> <code>countries.geojson</code> carries a
hand-drawn outline per country — 9 to 31 vertices, roughly the right place, not the right
shape. Rendering those implied a cartographic fidelity the corpus does not have, so they
are no longer drawn. National boundaries here are vendored substrate — {sub_note} — joined
to the corpus by ISO country code at build time. They are reference geography: they carry
no claim, and the build fails if a corpus country has no boundary rather than dropping it.
The corpus polygons are left untouched in the data; they are simply not the render path.</p>
<p><b>Everything derived on this page.</b> Two computations, both stating their rule where
they appear: the <i>evidence window</i> ({window_lo} → {window_hi}) is min/max of all
receipt dates, and the <i>qualifier flag</i> is the rule given under the reserve table.
Everything else is presentational and encodes nothing: sort order, the 60-day line, the
shaded quadrant, label placement on both figures, and the minimum mark size that keeps
{small_txt} visible on the map — which exaggerates {small_pron} area, one reason area is
not an encoding there.
<b>Confidence</b> is the corpus's own field, reproduced unchanged; it rates a country's
<i>inputs</i>, never the band assignment.</p></div>""")

    # ============ receipts ============
    A(f"""<div class="sec audit rcpt"><div class="rung">Audit · receipts</div>
<h2>Source material</h2>
<div class="lede">All {n_receipts} citations, and what each supports.</div>
<div class="absence"><b>No citation in this corpus has a retrieval date or an archive
snapshot.</b> Those fields do not exist in the schema yet, so nothing here records when a
source was last seen or preserves it against removal. Stated once rather than repeated as
an empty column.</div>
<div class="scroll"><table>
<thead><tr><th>Supports</th><th>Publisher</th><th>Published</th></tr></thead><tbody>""")

    for c in sorted(cs, key=lambda c: c["country"]):
        for s in c["sources"]:
            A("""<tr><td class="k">%s</td>
<td><a href="%s" rel="noopener">%s</a></td>
<td class="n">%s</td></tr>"""
              % (e(c["country"]), e(s["url"]), e(s["publisher"]), e(s["date"])))

    A(f"""</tbody></table></div>
<div class="figfoot">
  <span><b>{n_receipts}</b> citations · <b>{len({s['url'] for c in cs for s in c['sources']})}</b> unique URLs</span>
</div></div>

<footer>
Built from <code>docs/hormuz/data/countries.geojson</code> by
<code>tools/build_atlas_hormuz.py</code>. Case prose is reproduced verbatim from the
corpus; every derived value states its rule on the page.<br>
<a href="../insurance/">Insurance</a> · <a href="../cloud/">Cloud &amp; CDN</a> ·
<a href="../">All atlases</a>
</footer>

</div></body></html>""")
    return "\n".join(o)


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    out = render()
    cov = require_subject_fields(out, load())
    print("  subject-field coverage: " +
          " ".join("%s %d/%d" % (k, a, b) for k, (a, b) in cov.items()))
    open(OUT, "w").write(out)
    print("wrote %s (%s bytes)" % (os.path.relpath(OUT, REPO), format(len(out), ",")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
