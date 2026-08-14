#!/usr/bin/env python3
"""Build the cloud/CDN grammar specimen from the existing corpus.

    docs/cloud/data/cases.geojson  ->  docs/cloud/index.html

Third specimen. Same loop, third defect class.

  Hormuz    — missing measurement tracks apparent fragility.
  Insurance — one column, six semantics; the field name lies about comparability.
  Cloud     — TENSE COLLAPSE. Four of the ten cases are events that ended; six
              are conditions that persist. The corpus stores no date field, so
              the published map renders a 49-minute outage from June 2021 as a
              dot identical to a standing control-plane dependency. And
              `severity: demonstrated | structural` is not a severity axis at
              all — it is an evidential-mode axis wearing a magnitude's name.

Deliberately has NO MAP. The original review found cloud's geography close to
decorative ("AWS us-east-1 as a dot in Virginia carries almost no information
that the sentence beside it does not"), and this corpus's argument is temporal,
not spatial. atlas_core supplies mechanism, not composition; a specimen that
needs no map should not have one.

Constraints: no new research; no rewritten case prose; derived values state
their rule.

Usage:  python3 tools/build_atlas_cloud.py
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from atlas_core import (  # noqa: E402
    CSS as CORE_CSS, e, w, cap, days_between, evidence_window, head,
    evidence_banner, register_line, register_definitions, audit_divider,
    receipts_table, require_subject_fields, REPO)

SRC = os.path.join(REPO, "docs", "cloud", "data", "cases.geojson")
OUT_DIR = os.path.join(REPO, "docs", "cloud")
OUT = os.path.join(OUT_DIR, "index.html")
TODAY = "2026-08-14"

# Durations asserted in prose. Order matters: match the longest unit first.
DUR_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*(minutes?|mins?|hours?|hrs?|days?)\b", re.I)
_MON = ("January|February|March|April|May|June|July|August|September|"
        "October|November|December")
MONTH_RE = re.compile(r"\b(" + _MON + r")\s+(20[12]\d)\b")
MONTH_N = {m: i + 1 for i, m in enumerate(_MON.split("|"))}
UNIT_H = {"minute": 1 / 60.0, "min": 1 / 60.0, "hour": 1.0, "hr": 1.0, "day": 24.0}

CSS = CORE_CSS + """
/* ---------- cloud-only: one timeline, two tenses ---------- */
.tl2{border-top:1px solid var(--rule);padding-top:4px;position:relative;
  --c1:212px; --c3:104px; --g:16px}
/* a month the corpus records in two tenses at once */
.tl2 .twice{position:absolute;top:34px;bottom:34px;width:1px;
  background:repeating-linear-gradient(180deg,#e9c46a 0 4px,transparent 4px 9px);
  opacity:.5;pointer-events:none;
  left:calc(var(--c1) + var(--g) + (100% - var(--c1) - var(--c3) - 2*var(--g))
        * var(--x) / 100)}
.tl2 .twice span{position:absolute;top:-26px;transform:translateX(-50%);
  font-family:var(--mono);font-size:9px;letter-spacing:.06em;color:#c9a45e;
  white-space:nowrap}
.tl2row{display:grid;grid-template-columns:212px 1fr 104px;gap:16px;
  align-items:center;padding:13px 0;border-bottom:1px solid var(--rule-soft)}
.tl2row .nm{font-size:14px;color:var(--tx);line-height:1.3}
.tl2row .nm small{display:block;font-family:var(--mono);font-size:9.5px;
  color:var(--tx-faint);margin-top:3px}
.tl2row .tr{position:relative;height:20px}
.tl2row .ev{position:absolute;top:2px;height:16px;width:2px;background:var(--hot)}
.tl2row .evlab{position:absolute;top:0;transform:translateX(-50%);
  font-family:var(--mono);font-size:9px;color:#c98d84;white-space:nowrap;
  margin-top:-2px}
/* a condition: fades in on the left (no recorded start), capped at today */
.tl2row .rail{position:absolute;top:8px;height:5px;left:0;right:0;
  background:linear-gradient(90deg,rgba(79,195,247,0) 0%,rgba(79,195,247,.30) 22%,
    rgba(79,195,247,.55) 100%);
  border-right:3px solid var(--observed)}
.tl2row .mo{position:absolute;top:5.5px;width:10px;height:10px;
  transform:translateX(-50%) rotate(45deg);background:#0c0e11;
  border:1.6px solid #e9c46a}
.tl2row .molab{position:absolute;bottom:-3px;transform:translateX(-50%);
  font-family:var(--mono);font-size:9px;color:#b1904e;white-space:nowrap}
.tl2row .dur{font-family:var(--mono);font-size:11.5px;color:var(--tx-mid);
  text-align:right}
.tl2row.cond .dur{color:var(--observed)}
.tl2 .grp{font-family:var(--mono);font-size:10px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--tx-mid);padding:20px 0 8px}
.tl2 .grp em{font-style:normal;text-transform:none;letter-spacing:0;
  color:var(--tx-faint);margin-left:10px}
.tl2axis{display:grid;grid-template-columns:212px 1fr 104px;gap:16px;
  font-family:var(--mono);font-size:10px;color:var(--tx-faint);padding-top:9px}
.tl2axis .tr{position:relative;height:12px}
.tl2axis .tk{position:absolute;transform:translateX(-50%)}
.tl2axis .tk.now{color:var(--observed);transform:translateX(-100%)}
@media (max-width:760px){.tl2row,.tl2axis{grid-template-columns:132px 1fr 74px;gap:9px}
  .tl2row .nm{font-size:12.5px} .tl2row .molab,.tl2row .evlab{font-size:8px}
  .tl2{--c1:132px; --c3:74px; --g:9px}}

/* ---------- old two-list timeline (retired) ---------- */
.tl{border-top:1px solid var(--rule);padding-top:6px}
.tlrow{display:grid;grid-template-columns:210px 1fr 96px;gap:16px;
  align-items:baseline;padding:11px 0;border-bottom:1px solid var(--rule-soft)}
.tlrow .nm{font-size:14px;color:var(--tx)}
.tlrow .nm small{display:block;font-family:var(--mono);font-size:10px;
  color:var(--tx-faint);margin-top:3px}
.tlrow .tr{position:relative;height:15px;top:2px}
.tlrow .ev{position:absolute;top:0;height:16px;width:2px;background:var(--hot);
  opacity:.95}
.tlrow .ongoing{position:absolute;top:3px;height:10px;right:0;
  background:linear-gradient(90deg,rgba(79,195,247,.12),rgba(79,195,247,.5));
  border-right:2px solid var(--observed)}
.tlrow .dur{font-family:var(--mono);font-size:12px;color:var(--tx-mid);
  text-align:right}
.tlrow.cond .dur{color:var(--observed)}
.tlaxis{display:grid;grid-template-columns:210px 1fr 96px;gap:16px;
  font-family:var(--mono);font-size:10px;color:var(--tx-faint);padding-top:7px}
.tlaxis .tr{position:relative;height:12px}
.tlaxis .tk{position:absolute;transform:translateX(-50%)}
.split{font-family:var(--mono);font-size:10.5px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--tx-mid);padding:20px 0 7px}
.split span{display:block;text-transform:none;letter-spacing:0;font-size:13px;
  color:var(--tx-dim);margin-top:5px;max-width:60ch;line-height:1.5}

/* severity-axis exhibit */
.sev{display:grid;grid-template-columns:1fr 1fr;gap:0 30px;border-top:1px solid var(--rule);
  padding-top:16px}
.sev .col h3{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;
  text-transform:uppercase;color:var(--tx-mid);margin-bottom:4px;font-weight:700}
.sev .col .q{font-size:13px;color:var(--tx-dim);line-height:1.5;margin-bottom:12px}
.sev .col li{margin:0 0 6px 18px;font-size:13.5px;color:var(--tx-mid)}
@media (max-width:760px){.sev{grid-template-columns:1fr;gap:22px}
  .tlrow,.tlaxis{grid-template-columns:150px 1fr 72px;gap:10px}}
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


def duration_hours(c):
    """DERIVED. Longest duration asserted anywhere in the case's prose, in
    hours. Rule: regex for '<n> minutes|hours|days'; take the maximum. Returns
    None when the prose states no duration."""
    best = None
    for k in ("one_line", "consequence", "dependency", "affected_scope"):
        for m in DUR_RE.finditer(c.get(k) or ""):
            unit = m.group(2).lower().rstrip("s").rstrip(".")
            h = float(m.group(1)) * UNIT_H.get(unit, UNIT_H.get(unit[:3], 1.0))
            if best is None or h > best:
                best = h
    return best


def event_date(c):
    """DERIVED, and only because the corpus forces it: there is no date field
    anywhere in this atlas. For a case the corpus marks `demonstrated`, the
    earliest source date is used as the date the thing happened — which is a
    proxy, not a record. For `structural` cases the earliest source date is
    merely when somebody wrote about it, and is NOT used as a date."""
    return min(s["date"] for s in c["sources"])


def embedded_moments(c):
    """DERIVED. Dated moments named inside a case's own prose, as (label, frac).
    Rule: match '<Month> <Year>'. These are the instants a standing condition
    cites as evidence for itself — the point at which a record carries two
    tenses at once."""
    txt = " ".join(str(c.get(k) or "") for k in
                   ("one_line", "dependency", "consequence", "who_controls",
                    "affected_scope"))
    out = []
    for mon, yr in sorted(set(MONTH_RE.findall(txt))):
        out.append(("%s %s" % (mon, yr), int(yr) + (MONTH_N[mon] - 1) / 12.0))
    return out


def fmt_dur(h):
    if h is None:
        return "—"
    if h < 1:
        return "%d min" % round(h * 60)
    if h < 48:
        return "%g hr" % (round(h * 10) / 10)
    return "%g d" % (round(h / 24 * 10) / 10)


def render():
    cs = load()
    window_lo, window_hi = evidence_window(cs)
    stale = days_between(window_hi, TODAY)
    n_receipts = sum(len(c["sources"]) for c in cs)

    events = sorted([c for c in cs if c["severity"] == "demonstrated"],
                    key=event_date)
    conditions = [c for c in cs if c["severity"] != "demonstrated"]
    dated = [(c, event_date(c), duration_hours(c)) for c in events]
    with_dur = [d for _, _, d in dated if d is not None]

    lo_y, hi_y = 2021, 2026
    def xp(datestr):
        y, m, _ = map(int, datestr.split("-"))
        frac = y + (m - 1) / 12.0
        return 100.0 * (frac - lo_y) / (hi_y - lo_y)

    o = []
    A = o.append
    A(head("Four of these ten are already over",
           "Ten cloud dependency cases: four are outages that ended, six are "
           "conditions that persist, and the corpus records no date for any of them.",
           CSS))
    A(evidence_banner(window_hi, stale, "docs/cloud/data/cases.geojson"))
    A('<div class="wrap">')

    A(f"""
<div class="kicker">Cloud &amp; CDN Dependency · Infrastructure Dependency Atlas</div>
<h1>Four of these ten are already over</h1>

<div class="answer">
Fastly's CDN failed for <strong>49 minutes</strong> in June 2021. CrowdStrike cancelled
<strong>5,078 flights</strong> in July 2024. Those are over. Meanwhile one county in
Virginia still holds the control plane for every AWS customer on earth, 49% of domains
still resolve through ten providers, and the CLOUD Act still reaches inside Microsoft's EU
Data Boundary. <strong>Four of these ten are finished events; six are conditions that have
not stopped</strong> — and the record marks neither.
</div>

<div class="strip">
  <div class="s"><div class="n">10</div><div class="l">cases</div></div>
  <div class="s anom"><div class="n">{len(events)}</div><div class="l">are outages that ended</div></div>
  <div class="s"><div class="n">{len(conditions)}</div><div class="l">are conditions that persist</div></div>
  <div class="s anom"><div class="n">0</div><div class="l">date fields in the schema</div></div>
</div>

<div class="stamp">
  <span><b>EVIDENCE WINDOW</b> {window_lo} → {window_hi}</span>
  <span><b>CITATIONS</b> {n_receipts}</span>
  <span><b>CASES</b> 10</span>
</div>
""")
    A(register_line())

    # ---------------- primary: one timeline, two tenses ----------------
    NOW_F = 2026 + (8 - 1) / 12.0
    lo_f, hi_f = 2021.0, NOW_F
    def fx(frac):
        return 100.0 * (frac - lo_f) / (hi_f - lo_f)
    def fx_date(datestr):
        y, m, _ = map(int, datestr.split("-"))
        return fx(y + (m - 1) / 12.0)

    rows = []
    for c, d, hrs in dated:
        rows.append(("event", c, fx_date(d), fmt_dur(hrs), d, []))
    for c in conditions:
        rows.append(("cond", c, None, "no recorded end", None,
                     embedded_moments(c)))
    n_embedded = sum(len(r[5]) for r in rows)
    # DERIVED: a month carrying both a finished event and a moment cited inside a
    # standing condition — the same instant recorded in two tenses.
    ev_months = {d[:7]: c for _, c, _, _, d, _ in rows if d}
    twice = []
    for _, c, _, _, _, moments in rows:
        for lab, frac in moments:
            yy = int(frac); mm = int(round((frac - yy) * 12)) + 1
            key = "%04d-%02d" % (yy, mm)
            if key in ev_months:
                twice.append((lab, frac, ev_months[key], c))

    A(f"""<div class="sec"><div class="rung">Primary evidence · derived from sources</div>
<figure>
<figcaption>Four things that happened. Six things that are still true.</figcaption>
<div class="fignote">Every case in the atlas on one axis. The outages are marks at a moment;
each lasted between 49 minutes and 15 hours, too brief to draw at this scale, so the
duration is written instead. The conditions have no recorded beginning — the rail fades in
rather than starting — and no recorded end, so it runs to today.
<b>◆ marks a dated moment a standing condition cites inside its own text</b> — and the
dashed column marks a month this corpus records in both tenses at once.</div>
<div class="tl2">""")

    for lab, frac, ev_case, cond_case in twice:
        A('<div class="twice" style="--x:%.3f"><span>%s — recorded twice</span></div>'
          % (fx(frac), e(lab)))

    A('<div class="grp">Ended · %s of 10</div>' % w(len(events)))
    for kind, c, x, lab, d, moments in [r for r in rows if r[0] == "event"]:
        A("""<div class="tl2row">
  <div class="nm">%s<small>%s</small></div>
  <div class="tr"><div class="ev" style="left:%.2f%%"></div>
    <div class="evlab" style="left:%.2f%%">%s</div></div>
  <div class="dur">%s</div>
</div>""" % (e(c["title"].split("—")[0].strip()[:44]), e(c["category_label"]),
             x, x, e(d[:7]), e(lab)))

    A('<div class="grp">Still true · %s of 10 <em>no recorded start, no recorded end</em></div>'
      % w(len(conditions)))
    for kind, c, x, lab, d, moments in [r for r in rows if r[0] == "cond"]:
        marks = "".join(
            '<div class="mo" style="left:%.2f%%" title="%s"></div>'
            '<div class="molab" style="left:%.2f%%">%s</div>' % (fx(f), e(t), fx(f), e(t))
            for t, f in moments if lo_f <= f <= hi_f)
        A("""<div class="tl2row cond">
  <div class="nm">%s<small>%s</small></div>
  <div class="tr"><div class="rail"></div>%s</div>
  <div class="dur">ongoing</div>
</div>""" % (e(c["title"].split("—")[0].strip()[:44]), e(c["category_label"]), marks))

    A(f"""<div class="tl2axis"><div></div><div class="tr">
  <span class="tk" style="left:{fx(2021.0):.1f}%">2021</span>
  <span class="tk" style="left:{fx(2022.0):.1f}%">2022</span>
  <span class="tk" style="left:{fx(2023.0):.1f}%">2023</span>
  <span class="tk" style="left:{fx(2024.0):.1f}%">2024</span>
  <span class="tk" style="left:{fx(2025.0):.1f}%">2025</span>
  <span class="tk" style="left:{fx(2026.0):.1f}%">2026</span>
  <span class="tk now" style="left:100%">today</span>
</div><div></div></div>
</div>
<div class="figfoot">
  <span><b>n</b> 10 cases · {len(events)} dated · {len(with_dur)} state a duration · {n_embedded} moments cited inside conditions</span><br>
  <span class="long"><b>DERIVED</b> every position on this figure. Outage dates are the
  earliest citation attached to the case, used as a proxy because the schema has no date
  field; durations are the longest interval stated in the case's own prose; ◆ moments are
  “&lt;Month&gt; &lt;Year&gt;” matched in a condition's text. The rails assert nothing except
  that no start and no end were recorded.</span>
  <span class="long"><b>AND THE PROXY IS ALREADY WRONG ONCE.</b> The October 2025 AWS
  outage sits at 2025-10-15, the date of its earliest citation. Widely reported accounts put
  the outage several days later. A citation can predate the thing it describes, which is why
  an inferred date is not a record.</span>
</div>
</figure>

<div class="interp">
<p>Look at the column above <b>December 2021</b>. The AWS cascade is there as a finished
event, seven hours long, closed. It is also there as a ◆ on the control-plane rail, cited
as evidence that the dependency exists — a rail with no end. The same three weeks are in
this corpus twice, once as something that happened and once as proof of something that has
not stopped. Nothing in the schema distinguishes the two readings, and the published map
draws both as the same dot.</p>
<div class="by">▌Interpreted</div>
</div></div>""")

    # ---------------- severity is not severity ----------------
    dem = [c for c in cs if c["severity"] == "demonstrated"]
    A(f"""<div class="sec"><div class="rung">Qualification</div>
<h2>“Severity” is not measuring severity</h2>
<div class="lede">The field is called <code>severity</code> and takes two values. Neither
is a magnitude. They answer a different question — <i>has this already happened?</i> — and
sorting by them ranks nothing.</div>
<div class="sev">
  <div class="col"><h3>severity: demonstrated — {len(dem)} cases</h3>
    <div class="q">“Demonstrated failure”. An event with a date, a duration and a
    casualty list.</div><ul>""")
    for c in dem:
        A("<li>%s <span style='color:var(--tx-faint)'>· %s</span></li>"
          % (e(c["title"].split("—")[0].strip()[:44]), fmt_dur(duration_hours(c))))
    A(f"""</ul></div>
  <div class="col"><h3>severity: structural — {len(conditions)} cases</h3>
    <div class="q">“Structural dependency”. A standing arrangement with no event, no
    duration, and no end.</div><ul>""")
    for c in conditions:
        A("<li>%s</li>" % e(c["title"].split("—")[0].strip()[:44]))
    A("""</ul></div>
</div>
<div class="figfoot">
  <span class="long"><b>OBSERVED</b> the field values, verbatim. <b>NOT DERIVED</b> any
  ordering — a 49-minute CDN failure and a control-plane concentration with no recorded end are
  not two points on one scale, and this page does not place them on one.</span>
</div>

<div class="interp">
<p>A demonstrated failure is <em>better</em> evidenced than a structural one — it has a
date, a duration, and named casualties. A structural dependency is arguably the more
serious finding and the harder one to prove. Reading the field as severity gets the
relationship backwards: it is an axis of proof, not of harm.</p>
<div class="by">▌Interpreted</div>
</div></div>""")

    # ---------------- the world ----------------
    A("""<div class="sec"><div class="rung">What the ten records describe</div>
<h2>Somebody else's region policy, somebody else's billing model</h2>
<div class="lede">The corpus's own account of each dependency: what runs through it, what
happens when it moves, and who decides. Verbatim.</div>
<div class="turn">""")

    for c in cs:
        A("""<div class="e">
  <div><div class="cn">%s</div>
    <span class="tag" style="color:var(--tx-faint)">%s</span>
    <span class="tag" style="color:%s">%s</span></div>
  <div class="st"><span class="lab">The dependency</span>%s
    <span class="lab" style="margin-top:12px">What happened / what it costs</span>%s
    <span class="lab" style="margin-top:12px">Who decides</span>%s
    <span class="lab" style="margin-top:12px">Who is downstream</span>%s</div>
</div>""" % (e(c["title"].split("—")[0].strip()), e(c["category_label"]),
             "#b4655f" if c["severity"] == "demonstrated" else "var(--observed)",
             e(c["severity_label"]),
             e(c["dependency"]), e(c["consequence"]), e(c["who_controls"]),
             e(c["affected_scope"])))

    A("""</div>
<div class="figfoot">
  <span><b>OBSERVED</b> reproduced verbatim from the corpus, per-case citations</span>
</div></div>""")

    # ---------------- ledger ----------------
    A("""<div class="sec"><div class="rung">Case evidence</div>
<h2>The ten</h2>
<div class="scroll"><table class="ledger">
<thead><tr><th>Case</th><th>Category</th><th>Mode</th><th>Provider</th><th>Location</th></tr></thead><tbody>""")
    for c in cs:
        A("""<tr class="lr">
  <td class="k cty">%s</td><td class="bandc">%s</td>
  <td class="n%s">%s</td><td class="n">%s</td><td class="n">%s</td>
</tr>
<tr class="claimrow"><td colspan="5"><span class="cl">%s</span></td></tr>""" % (
            e(c["title"].split("—")[0].strip()[:40]), e(c["category_label"]),
            "" if c["severity"] == "demonstrated" else "",
            e(c["severity_label"].split()[0]), e(c["provider"]),
            e(c["location"]), e(c["one_line"])))
    A("</tbody></table></div></div>")

    # ---------------- audit ----------------
    A(audit_divider("Everything below is the page checking itself."))
    A('<div class="sec audit"><div class="rung">Audit · what the marks mean</div>')
    A(register_definitions())
    A("""<div class="refusal">
<b>What this page does not claim.</b> That any of these outages will recur, or that a
structural dependency will fail. That one case is worse than another. That the four dated
events are representative of anything — they are the ones somebody wrote about.
</div></div>""")

    A(f"""<div class="sec audit bound"><div class="rung">Audit · boundary conditions</div>
<h2>What this page does not show</h2>
<div class="pull">An atlas of ongoing dependency, whose only precise records are of
things that stopped.</div>
<ul>
<li><b>Every date on this page is inferred.</b> The schema has no date field, so event
dates are the earliest citation attached to the case. A citation can predate or postdate
the thing it describes; these are proxies and should not be read as a record.</li>
<li><b>Durations come from prose, not fields.</b> {len(with_dur)} of the {len(events)}
events state one somewhere in their own text. Nothing enforces that they are measured the
same way.</li>
<li><b>Selection is invisible.</b> Four outages appear out of the many that occurred in
this period. The corpus records no criterion for inclusion, so the set cannot be read as a
sample of anything.</li>
<li><b>The conditions are not unmeasured — they are undated.</b> Their prose carries plenty
of figures (49% of domains, 115 data centers, 8.5 million machines). What none of them has
is a date, a duration, or a field to put either in. The schema has no slot for when a
standing arrangement began.</li>
<li><b>The event/condition split is the corpus's, and it leaks.</b> The DNS concentration
case is marked <code>structural</code>, yet its own prose contains a dated, timed event —
Facebook's October 2021 BGP misconfiguration, “3.5 billion users offline for 6 hours”. The
duration rule on the figure above is applied only to cases the corpus marks
<code>demonstrated</code>, so that event gets no tick. Tense collapse happens inside single
records too, not only across them.</li>
<li><b>Nothing records how sure anyone was.</b> This atlas has no confidence field at
all, so every case is presented at the same footing regardless of how well attested it
is.</li>
</ul></div>""")

    A(f"""<div class="sec audit meth"><div class="rung">Audit · method</div>
<h2>What is computed here</h2>
<div class="rule1">Three derivations, all forced by the same absence: this corpus has no
time in it.</div>
<p><b>Event date</b> — earliest source date, for the four cases the corpus marks
<code>demonstrated</code> only. <b>Duration</b> — the longest interval matched by regex in
a case's own prose. <b>The still-running band</b> — drawn for every
<code>structural</code> case, and it asserts nothing except that the corpus records no
end. The <i>evidence window</i> ({window_lo} → {window_hi}) is min/max of all citation
dates.</p>
<p><b><code>severity</code> is reproduced, never ordered.</b> Its two values distinguish an
evidential mode, not a magnitude, so nothing on this page sorts or colours by it as though
it were a scale.</p>
<p><b>There is no map</b> because this atlas's cases are global services and concentration
facts. Placing “us-east-1” as a dot in Virginia would add a geography that carries almost
none of the argument.</p></div>""")

    rows = [(c["title"].split("—")[0].strip()[:38], s["publisher"], s["url"], s["date"])
            for c in cs for s in c["sources"]]
    A(f"""<div class="sec audit rcpt"><div class="rung">Audit · sources</div>
<h2>Source material</h2>
<div class="lede">All {n_receipts} citations — exactly two per case.</div>""")
    A(receipts_table(rows, absence_note=(
        "<b>These dates are doing double duty.</b> For the four outages they are close to "
        "the date of the event. For the six standing dependencies they record only when "
        "someone published about it. The schema cannot tell the two apart, and neither "
        "can the evidence window computed from them.")))
    A("</div>")

    A("""<footer>
Built from <code>docs/cloud/data/cases.geojson</code> by
<code>tools/build_atlas_cloud.py</code>. Case prose is reproduced verbatim from the
corpus; every derived value states its rule on the page.<br>
<a href="../hormuz/">Hormuz</a> · <a href="../insurance/">Insurance</a> ·
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
