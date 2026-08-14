#!/usr/bin/env python3
"""Build the insurance grammar specimen from the existing corpus.

    docs/insurance/data/states.geojson  ->  docs/insurance/index.html

Second specimen. Same loop as Hormuz (corpus audit -> overbuilt specimen ->
cold read -> editorial reduction), deliberately NOT the same page shape: the
composition follows this corpus's argument, not the previous one's.

Hormuz's finding was that missing measurement tracks apparent fragility.
Insurance's is different and worse: the measurements exist, and the field name
is lying about their comparability. Two states are each recorded as "highest in
the nation" with different numbers, and the corpus never says over what period
either was measured.

Constraints held: no new research; no rewritten case prose; derived values state
their rule; `stress_band` renders interpreted (no derivation rule was ever
specified for it — see the Hormuz Method section and commit 1a72110); the
rate figures are NOT put on a shared axis, per grammar R4a.

Usage:  python3 tools/build_atlas_insurance.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atlas_core import (  # noqa: E402
    CSS as CORE_CSS, e, w, cap, days_between, evidence_window,
    load_substrate, svg_path, centroid, place_labels, head, evidence_banner,
    register_line, register_definitions, audit_divider, receipts_table,
    require_subject_fields, REPO)

SRC = os.path.join(REPO, "docs", "insurance", "data", "states.geojson")
OUT_DIR = os.path.join(REPO, "docs", "insurance")
OUT = os.path.join(OUT_DIR, "index.html")
SUBSTRATE = os.path.join(REPO, "vendor", "boundaries",
                         "ne_50m_admin1_us_subset.geojson")
SUBSTRATE_NOTE = ("Natural Earth 1:50m Admin 1, v5.1.2, public domain "
                  "(vendor/boundaries/PROVENANCE.md)")
TODAY = "2026-08-14"

# Corpus state name -> postal, for the substrate join. Explicit and auditable;
# the build fails rather than silently dropping a state.
POSTAL = {"Florida": "FL", "California": "CA", "Texas": "TX",
          "Louisiana": "LA", "Colorado": "CO", "North Carolina": "NC"}

# DISPLAY ORDER ONLY. Not a ranking: "systemic retreat" is a market state,
# "accelerating withdrawal" a rate-of-change claim, "growing residual exposure"
# a trend, "post-disaster underinsurance crisis" a different mechanism entirely.
# Nothing in the corpus orders them.
BAND_DISPLAY_ORDER = ["systemic_retreat", "accelerating_withdrawal",
                      "growing_residual", "underinsurance_crisis"]
BAND_INK = {}   # filled from the data; categorical hues, never a ramp
PALETTE = ["#e08b76", "#d7b169", "#7fb3c9", "#8fae8c", "#b49ad0"]

PROSE_FIELDS = ["one_line", "insurer_exits", "regulatory_response",
                "mortgage_impact"]
NUM_RE = re.compile(r"\$?\d[\d,]*\.?\d*\s?(?:%|B\b|M\b|K\b|billion|million)?")
SENT_SPLIT_RE = re.compile(r"(?<!\d)\.(?!\d)\s*")   # don't split on 76.6
RATE_WORD_RE = re.compile(r"\b(?:rate|premium)s?\b", re.I)

CSS = CORE_CSS + """
/* ---------- insurance-only: the contradiction block ---------- */
.claimoff{border-top:1px solid var(--rule)}
.claimoff .row2{display:grid;grid-template-columns:132px 96px 1fr;gap:20px;
  padding:19px 0;border-bottom:1px solid var(--rule-soft);align-items:baseline}
.claimoff .st{font-family:var(--serif);font-size:20px;font-weight:600;color:#fff}
.claimoff .pc{font-family:var(--serif);font-size:31px;font-weight:600;
  color:var(--observed);line-height:1;letter-spacing:-.02em}
.claimoff .pc.dim{color:var(--tx-dim)}
.claimoff .says{font-size:13.5px;color:var(--tx-mid);line-height:1.5}
.claimoff .says q{font-style:italic;color:#c3ccd5;quotes:none}
.claimoff .missing{color:#b4655f;font-family:var(--mono);font-size:11.5px}
.claimoff .row2.clash{background:linear-gradient(90deg,rgba(224,139,118,.07),transparent 70%)}
.claimoff .flag{display:block;font-family:var(--mono);font-size:9.5px;
  letter-spacing:.09em;text-transform:uppercase;color:#e08b76;margin-top:6px}

/* prose-vs-record ledger */
.pv .b{padding:16px 0;border-bottom:1px solid var(--rule-soft)}
.pv .h{display:flex;gap:12px;align-items:baseline;flex-wrap:wrap;margin-bottom:7px}
.pv .s{font-family:var(--serif);font-size:19px;font-weight:600;color:#fff}
.pv .cnt{font-family:var(--mono);font-size:10.5px;color:var(--tx-faint)}
.pv .toks{display:flex;flex-wrap:wrap;gap:6px}
.pv .t{font-family:var(--mono);font-size:11.5px;padding:2px 7px;
  border:1px solid #2b3138;color:var(--tx-dim)}
.pv .t.backed{border-color:#2b4a5a;color:var(--observed)}
"""


def load():
    d = json.load(open(SRC))
    out = []
    for f in d["features"]:
        p = dict(f["properties"])
        if isinstance(p.get("sources"), str):
            p["sources"] = json.loads(p["sources"])
        out.append(p)
    return out


def rate_context(c):
    """DERIVED. Does this state's own record say what its rate_change_pct
    measures? Rule: collect every sentence in the state's prose containing
    'rate' or 'premium'; report them verbatim, and flag whether the stored
    value appears in one. Purely mechanical, no per-row judgment."""
    sents = []
    for f in PROSE_FIELDS:
        for part in SENT_SPLIT_RE.split(c.get(f) or ""):
            part = part.strip()
            if part and RATE_WORD_RE.search(part):
                sents.append(part.rstrip(".") + ".")
    stored = c.get("rate_change_pct")
    exact = [s for s in sents if stored is not None and re.search(
        r"\b%d(?:\.\d)?\s*%%" % stored, s)]
    near = [s for s in sents if stored is not None and re.search(
        r"\b%d\.\d\s*%%" % (stored - 1), s)]     # 77 stored vs "76.6%" in prose
    return {"sentences": sents, "exact": exact, "near": near,
            "anchored": bool(exact or near)}


def prose_numbers(c):
    """DERIVED. Numeric tokens asserted in prose, and whether each is present in
    the structured record. Rule: regex over the four prose fields; a token counts
    as backed when it equals a stored numeric field, comma-insensitively."""
    stored = set()
    for k in ("fair_plan_policies", "fair_plan_peak", "rate_change_pct"):
        v = c.get(k)
        if v is not None:
            stored.add(str(v))
            stored.add("{:,}".format(v))
    seen, out = set(), []
    for f in PROSE_FIELDS:
        for m in NUM_RE.finditer(c.get(f) or ""):
            tok = m.group(0).strip().rstrip(".")
            if len(tok.strip("$%")) < 2 or re.fullmatch(r"(19|20)\d\d", tok):
                continue                      # skip bare years
            if tok in seen:
                continue
            seen.add(tok)
            bare = tok.strip("$%").replace(",", "")
            out.append((tok, any(bare == s.replace(",", "") for s in stored)))
    return out


def render():
    cs = load()
    for i, b in enumerate(sorted({c["stress_band"] for c in cs},
                                 key=lambda b: BAND_DISPLAY_ORDER.index(b)
                                 if b in BAND_DISPLAY_ORDER else 9)):
        BAND_INK[b] = PALETTE[i % len(PALETTE)]

    window_lo, window_hi = evidence_window(cs)
    stale = days_between(window_hi, TODAY)
    n_receipts = sum(len(c["sources"]) for c in cs)

    RC = {c["state"]: rate_context(c) for c in cs}
    PN = {c["state"]: prose_numbers(c) for c in cs}
    anchored = [c for c in cs if RC[c["state"]]["anchored"]]
    highest = [c for c in cs
               if any(re.search(r"highest", s, re.I)
                      for s in RC[c["state"]]["sentences"])]
    tot_tok = sum(len(PN[c["state"]]) for c in cs)
    backed_tok = sum(1 for c in cs for _, b in PN[c["state"]] if b)
    no_fair = [c for c in cs if c.get("fair_plan_policies") is None]
    n_bare = sum(1 for c in cs for s_ in c["sources"]
                 if s_["url"].rstrip("/").count("/") < 3)
    has_fair = [c for c in cs if c.get("fair_plan_policies") is not None]

    o = []
    A = o.append

    A(head("Which state is worst? The atlas says two of them",
           "Six states under insurer retreat: the corpus records two of them as "
           "the highest rate increase in the nation, and cannot say which is right.",
           CSS))
    A(evidence_banner(window_hi, stale,
                      "docs/insurance/data/states.geojson"))
    A('<div class="wrap">')

    # ---------------- masthead ----------------
    A(f"""
<div class="kicker">Insurance Dependency · Infrastructure Dependency Atlas</div>
<h1>Which state is worst? The atlas says two of them</h1>

<div class="answer">
Louisiana's record says its <strong>58%</strong> rate rise is “the highest rate increase in
the nation.” Colorado's says its <strong>76.6%</strong> is. Both are in this atlas; both are
painted on the same map, on the same scale. Colorado's figure at least carries a period —
six years — but only inside a sentence of prose. Louisiana's carries none at all, and
<strong>neither period is stored in any field a map can read.</strong>
</div>

<div class="strip">
  <div class="s"><div class="n">6</div><div class="l">states assessed</div></div>
  <div class="s anom"><div class="n">{len(highest)}</div><div class="l">claim “highest in the nation”</div></div>
  <div class="s anom"><div class="n">{len(no_fair)}</div><div class="l">record no policy count at all</div></div>
  <div class="s anom"><div class="n">{n_bare}</div><div class="l">of {n_receipts} citations point at a home page</div></div>
</div>

<div class="stamp">
  <span><b>EVIDENCE WINDOW OPENS</b> {window_lo}</span>
  <span><b>CITATIONS</b> {n_receipts}</span>
  <span><b>STATES</b> 6</span>
</div>
""")
    A(register_line())

    # ---------------- primary: the contradiction ----------------
    A(f"""<div class="sec"><div class="rung">Primary evidence · observed</div>
<figure>
<figcaption>One field, six states, six different meanings.</figcaption>
<div class="fignote">Each state's stored <code>rate_change_pct</code>, beside every
sentence in that state's own record that mentions rates. <b>These are deliberately not
drawn on a shared axis.</b> Putting them on one would assert a comparison the corpus
cannot support — which is what the published map does.</div>
<div class="claimoff">""")

    for c in sorted(cs, key=lambda c: -(c.get("rate_change_pct") or 0)):
        rc = RC[c["state"]]
        clash = c in highest
        says = ""
        if rc["sentences"]:
            says = " ".join('<q>%s</q>' % e(s) for s in rc["sentences"][:2])
        else:
            says = ('<span class="missing">nothing in this state\'s record says '
                    'what this number measures</span>')
        flag = ""
        if clash:
            flag = '<span class="flag">claims “highest in the nation”</span>'
        elif not rc["anchored"]:
            flag = ('<span class="flag" style="color:var(--tx-faint)">'
                    'stored value appears nowhere in the prose</span>')
        A("""<div class="row2%s">
  <div class="st">%s</div>
  <div class="pc%s">%s%%</div>
  <div class="says">%s%s</div>
</div>""" % (" clash" if clash else "", e(c["state"]),
             "" if clash else " dim",
             c["rate_change_pct"], says, flag))

    A(f"""</div>
<div class="figfoot">
  <span><b>n</b> 6 states · {len(anchored)} anchored to a sentence</span>
  <span><b>WINDOW</b> {window_lo} → {window_hi}</span><br>
  <span class="long"><b>DERIVED</b> the anchoring flag: a figure counts as anchored when its
  stored value appears in one of its own state's rate sentences. Colorado's stored <b>77</b>
  is the prose's <b>76.6%</b> rounded, and its six-year window is the only period the corpus
  states anywhere. No shared axis and no severity sort — the values are not one quantity.</span>
</div>
</figure>

<div class="interp">
<p>Texas's stored figure is <b>3</b>. The only rate sentence in its record says residential
rates were “deemed inadequate by 38%” — a regulator's judgment about a shortfall, not an
increase paid by anyone. Whatever the 3 is, the corpus does not say, and the published map
paints it in the same scale as Colorado's 77.</p>
<div class="by">▌Interpreted</div>
</div></div>""")

    # ---------------- what the records actually describe ----------------
    A("""<div class="sec"><div class="rung">What the six records describe</div>
<h2>The backstop is becoming the market</h2>
<div class="lede">Underneath the schema argument there is a story the corpus tells
plainly: what insurers did, what the state did back, and what it costs the people who
live there. Verbatim, in the corpus's own words.</div>
<div class="turn">""")

    for c in cs:
        A("""<div class="e">
  <div><div class="cn">%s</div><span class="tag" style="color:var(--tx-faint)">%s</span></div>
  <div class="st"><span class="lab">Insurer behaviour</span>%s
    <span class="lab" style="margin-top:12px">State response</span>%s
    <span class="lab" style="margin-top:12px">What it costs households</span>%s</div>
</div>""" % (e(c["state"]), e(c["stress_label"]),
             e(c["insurer_exits"]), e(c["regulatory_response"]),
             e(c["mortgage_impact"])))

    A("""</div>
<div class="figfoot">
  <span><b>OBSERVED</b> reproduced verbatim from the corpus, per-state receipts</span>
</div>

<div class="interp">
<p>Two of these accounts carry figures the record cannot check. California's headline —
<q>FAIR Plan up 139% in 4 years</q> — is a claim about a trend, and the corpus stores one
snapshot with no baseline. Florida's <q>1.41M policies to 395K</q> is the largest movement
on the page, and both of its citations are home pages. Neither is likely to be wrong.
Neither can be verified from here.</p>
<div class="by">▌Interpreted</div>
</div></div>""")

    # ---------------- map ----------------
    sub = load_substrate(SUBSTRATE, key="postal")
    missing_geo = [c["state"] for c in cs if POSTAL.get(c["state"]) not in sub]
    if missing_geo:
        raise SystemExit("no boundary substrate for: %s" % ", ".join(missing_geo))

    MW, MH = 800, 400
    L0, L1, B0, B1 = -125.5, -74.5, 24.0, 42.5
    KX = 0.79                                  # cos(~38N)
    sc = min((MW - 40) / ((L1 - L0) * KX), (MH - 48) / (B1 - B0))
    OX, OY = 18, 22

    def mx(lng): return OX + (lng - L0) * KX * sc
    def my(lat): return OY + (B1 - lat) * sc

    A(f"""<div class="sec"><div class="rung">Secondary evidence · interpreted</div>
<figure>
<figcaption>The classification, mapped. The shading is an authored class, not a measurement.</figcaption>
<div class="fignote">Fill encodes the corpus's <span class="mk mk-i">stress_band</span> —
an assessment class with no derivation rule. The colours are <b>categorical, not a
scale</b>. Hatching marks the states with no FAIR-plan policy counts recorded at all.</div>
<svg viewBox="0 0 {MW} {MH}" width="100%" role="img"
 aria-label="Map of six US states shaded by an authored insurer-stress class, with hatching on the three that record no FAIR-plan policy counts.">
<defs>
  <pattern id="hatch" width="6" height="6" patternTransform="rotate(45)" patternUnits="userSpaceOnUse">
    <line x1="0" y1="0" x2="0" y2="6" stroke="#0a0a0a" stroke-width="2.6" opacity="0.6"/>
  </pattern>
</defs>
<rect x="0" y="0" width="{MW}" height="{MH}" fill="#0c0e11"/>""")

    items, obst = [], []
    for c in cs:
        g = sub[POSTAL[c["state"]]]
        d = svg_path(g, mx, my)
        A('  <path d="%s" fill="%s" fill-opacity="0.7" stroke="#818b96" '
          'stroke-width="0.7" stroke-opacity="0.95" stroke-linejoin="round"/>'
          % (d, BAND_INK[c["stress_band"]]))
        if c.get("fair_plan_policies") is None:
            A('  <path d="%s" fill="url(#hatch)" stroke="#e8eef4" stroke-width="1" '
              'stroke-dasharray="3 2.5" stroke-opacity="0.8"/>' % d)
        cx, cy = centroid(g)
        px, py = mx(cx), my(cy)
        obst.append((px - 4, px + 4, py))
        wpx = 6.2 * len(c["state"]) + 4
        items.append((c["state"], px - wpx / 2, px + wpx / 2, py + 3))

    ys = place_labels(items, pad_y=11.5,
                      bounds=(OY + 8, OY + (B1 - B0) * sc - 4), obstacles=obst)
    for c in cs:
        g = sub[POSTAL[c["state"]]]
        cx, cy = centroid(g)
        px, py = mx(cx), my(cy)
        ly = ys[c["state"]]
        if abs(ly - (py + 3)) > 5:
            A('  <line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#59636e" '
              'stroke-width="0.9"/>' % (px, py, px, ly - 9))
        A('  <text x="%.1f" y="%.1f" text-anchor="middle" font-size="11" '
          'font-family="-apple-system,sans-serif" fill="#0d1116" stroke="#e9eff5" '
          'stroke-width="2.6" stroke-linejoin="round" paint-order="stroke" '
          'font-weight="500">%s</text>' % (px, ly, e(c["state"])))

    lx, ly0 = 30, MH - 112
    A('  <text x="%d" y="%d" font-size="9.5" font-family="ui-monospace,monospace" '
      'fill="#8b949e" letter-spacing="1">ASSESSMENT CLASS — CATEGORICAL</text>'
      % (lx, ly0 - 8))
    for i, b in enumerate(sorted(BAND_INK, key=lambda b: BAND_DISPLAY_ORDER.index(b)
                                 if b in BAND_DISPLAY_ORDER else 9)):
        yy = ly0 + i * 17
        lab = next(c["stress_label"] for c in cs if c["stress_band"] == b)
        A('  <rect x="%d" y="%d" width="11" height="11" fill="%s" fill-opacity="0.7"/>'
          '<text x="%d" y="%.1f" font-size="9" font-family="-apple-system,sans-serif" '
          'fill="#97a0aa">%s</text>' % (lx, yy, BAND_INK[b], lx + 16, yy + 9.5,
                                        e(lab.split(",")[0])))
    yy = ly0 + len(BAND_INK) * 17 + 6
    A('  <rect x="%d" y="%d" width="11" height="11" fill="#3a424b" stroke="#e8eef4" '
      'stroke-width="1" stroke-dasharray="2 2" stroke-opacity="0.8"/>'
      '<text x="%d" y="%.1f" font-size="9" font-family="-apple-system,sans-serif" '
      'fill="#97a0aa">no FAIR-plan counts recorded</text>' % (lx, yy, lx + 16, yy + 9.5))

    A(f"""</svg>
<div class="figfoot">
  <span><b>n</b> 6 states</span>
  <span><b>SUBSTRATE</b> boundaries are reference geography, not evidence (source in Method)</span><br>
  <span class="long"><b>INTERPRETED</b> every fill. Neither shade nor land area encodes a
  measured quantity.</span>
  <span class="long"><b>OBSERVED</b> only the hatch — whether FAIR-plan counts exist.</span>
</div>
</figure></div>""")

    # ---------------- FAIR plan ----------------
    A(f"""<div class="sec"><div class="rung">Policy counts</div>
<h2>Two numbers, no dates</h2>
<div class="lede">FAIR plans are the insurer of last resort — the residual market that
absorbs what private carriers drop. Their policy counts are the nearest thing here to a
measurement. They are not a series: no date is attached to either number, so the interval
between them is unknown, and half the states record neither.</div>
<div class="scroll"><table>
<thead><tr><th>State</th><th>Plan</th><th>Policies</th><th>Recorded peak</th><th>Reading</th></tr></thead><tbody>""")

    for c in cs:
        p, pk = c.get("fair_plan_policies"), c.get("fair_plan_peak")
        if p is None:
            read = '<span class="missing" style="color:#b4655f">no count recorded</span>'
            pv = pkv = '<span style="color:#b4655f">none</span>'
        else:
            pv, pkv = "{:,}".format(p), "{:,}".format(pk)
            if p == pk:
                read = ('<span style="color:var(--derived)">peak equals current — the '
                        'record holds one point, so no trend can be read from it</span>')
            else:
                read = "%.0f%% below the recorded peak" % (100.0 * (pk - p) / pk)
        A("""<tr><td class="k">%s</td><td>%s</td><td class="n">%s</td>
<td class="n">%s</td><td>%s</td></tr>""" % (e(c["state"]), e(c["fair_plan_name"]),
                                            pv, pkv, read))

    A(f"""</tbody></table></div>
<div class="figfoot">
  <span><b>OBSERVED</b> both counts, where recorded</span>
  <span><b>DERIVED</b> the “% below peak” reading</span><br>
  <span class="long"><b>DENOM</b> policies in force. No date is attached to either count
  anywhere in the corpus, so “peak” is undated and the interval between the two numbers is
  unknown.</span>
</div></div>""")

    # ---------------- ledger ----------------
    A("""<div class="sec"><div class="rung">State evidence</div>
<h2>The six</h2>
<div class="lede">Each claim as the corpus states it. Every class is an authored
judgment.</div>
<div class="scroll"><table class="ledger">
<thead><tr><th>State</th><th>Assessment class</th><th>Conf.</th><th>Rate</th><th>FAIR policies</th></tr></thead><tbody>""")

    for c in sorted(cs, key=lambda c: BAND_DISPLAY_ORDER.index(c["stress_band"])
                    if c["stress_band"] in BAND_DISPLAY_ORDER else 9):
        p = c.get("fair_plan_policies")
        A("""<tr class="lr">
  <td class="k cty">%s</td><td class="bandc">%s</td>
  <td class="n cf-%s">%s</td><td class="n">%s%%</td>
  <td class="n%s">%s</td>
</tr>
<tr class="claimrow"><td colspan="5"><span class="cl">%s</span>
<span class="qn">%s</span></td></tr>""" % (
            e(c["state"]), e(c["stress_label"]), e(c["confidence"]),
            e(c["confidence"]), c["rate_change_pct"],
            "" if p is not None else " miss",
            "{:,}".format(p) if p is not None else "none",
            e(c["one_line"]), e(c["confidence_note"])))
    A("</tbody></table></div></div>")

    # ---------------- audit floor ----------------
    A(audit_divider("Everything below is the page checking itself: limits, method, "
                    "and the source record."))
    A('<div class="sec audit"><div class="rung">Audit · what the marks mean</div>')
    A(register_definitions())
    A("""<div class="refusal">
<b>What this page does not claim.</b> That one state is worse off than another, or that the
assessment classes rank anything. It reports what the corpus can and cannot substantiate.
</div></div>""")

    A(f"""<div class="sec audit bound"><div class="rung">Audit · boundary conditions</div>
<h2>What this page does not show</h2>
<div class="pull">The atlas is six individually researched essays wearing one schema.
The schema is the part that does not fit.</div>
<ul>
<li><b>Unverifiable is not wrong.</b> Of the {tot_tok} figures asserted in prose, {backed_tok}
appear in a structured field. The rest may be perfectly accurate; the record simply cannot
confirm them, and neither can this page.</li>
<li><b><code>rate_change_pct</code> has no period and no base.</b> One state's prose gives
a window (Colorado, six years). The other five give none, so the field cannot be compared
across rows — and this page does not compare it.</li>
<li><b>Half the states record no FAIR-plan count</b> — {e(', '.join(c['state'] for c in no_fair))} —
and two of those carry <code>confidence: high</code> anyway.</li>
<li><b>Colorado disclaims the atlas's own subject.</b> Its record opens “Not primarily an
exit story — Colorado is the underinsurance story,” inside an atlas about insurer exit. It
is kept because the corpus keeps it, marked <span class="mk mk-r">refused</span> rather
than dropped.</li>
<li><b>{cap(len([1 for c in cs for s in c['sources'] if s['url'].rstrip('/').count('/') < 3]))} of
{n_receipts} citations point at a home page, not a document</b> — including both of
Florida's, the state with the largest figures on the page.</li>
</ul></div>""")

    A(f"""<div class="sec audit meth"><div class="rung">Audit · method</div>
<h2>What is computed here, and what is not</h2>
<div class="rule1">Nothing on this page ranks the six states, because the corpus provides
no basis on which they could be ranked.</div>
<p><b><code>stress_band</code> is interpreted.</b> No derivation rule was ever specified
for it — the repository history records the class assignments and no threshold, weight, or
ordering. The classes are also not commensurable — “systemic insurer retreat” is a market state,
“accelerating withdrawal” a rate-of-change claim, “post-disaster underinsurance crisis” a
different mechanism entirely. So the map's colours are categorical.</p>
<p><b>Two derivations, both stated where they appear.</b> The <i>rate-anchoring flag</i>
(rule under the first figure) and the <i>prose-token backing flag</i> (rule under the
second). The <i>evidence window</i> ({window_lo} → {window_hi}) is min/max of all receipt
dates. Everything else is presentational.</p>
<p><b>Geography is substrate.</b> The corpus's own state outlines are coarse hand sketches;
drawing them implied a precision it does not have. Boundaries here are vendored —
{SUBSTRATE_NOTE} — and carry no claim. The corpus polygons are untouched in the data.</p>
<p><b>Confidence</b> is the corpus's own field, unchanged. It rates a state's inputs, never
the class assignment — which is why Colorado can be <code>confidence: high</code> with no
FAIR-plan count recorded.</p></div>""")

    rows = [(c["state"], s["publisher"], s["url"], s["date"])
            for c in sorted(cs, key=lambda c: c["state"]) for s in c["sources"]]
    A(f"""<div class="sec audit rcpt"><div class="rung">Audit · sources</div>
<h2>Source material</h2>
<div class="lede">All {n_receipts} citations — exactly two per state, for every state, which
is itself a sign of a quota rather than a search.</div>""")
    A(receipts_table(rows, absence_note=(
        "<b>Seven of these twelve point at a home page rather than a document.</b> "
        "A citation to <code>propublica.org/</code> or <code>ncdoi.gov/</code> cannot be "
        "checked and will never break, which makes it invisible to link-checking. No "
        "citation in this corpus has a retrieval date or an archive snapshot either.")))
    A("</div>")

    A(f"""<footer>
Built from <code>docs/insurance/data/states.geojson</code> by
<code>tools/build_atlas_insurance.py</code>. Case prose is reproduced verbatim from the
corpus; every derived value states its rule on the page.<br>
<a href="../hormuz/">Hormuz</a> · <a href="../cloud/">Cloud &amp; CDN</a> ·
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
