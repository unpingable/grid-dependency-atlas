#!/usr/bin/env python3
"""atlas_core — shared mechanism for atlas specimen renderers.

**Scope discipline: this module holds MECHANISM, not composition.**

In scope: typography and colour tokens, the register marks, figure/table/ledger
primitives, the audit-floor treatment, vendored-geography loading and
projection, label de-collision, evidence-window derivation, small text helpers.

Explicitly OUT of scope: what sections a page has, in what order. Two specimens
is enough to eliminate duplicate machinery; it is nowhere near enough to prove a
universal composition. Hormuz opens with a margin chart and turns on missing
measurement; insurance opens on a contradiction between two states. Those are
different arguments and must stay free to be different pages. If a third
specimen wants the same shape as a previous one, that is the moment to consider
promoting shape — not before.

Consumers: tools/build_atlas_hormuz.py, tools/build_atlas_insurance.py
"""
import html
import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# --------------------------------------------------------------- text helpers
def e(s):
    """Escape for HTML attribute/text context."""
    return html.escape(str(s if s is not None else ""), quote=True)


_WORDS = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
          6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
          11: "eleven", 12: "twelve"}


def w(n):
    """Spell small integers. Prose reads as prose; figures stay numeric."""
    return _WORDS.get(n, str(n))


def cap(n):
    """Sentence-initial form of w()."""
    return w(n).capitalize()


def days_between(a, b):
    from datetime import date
    ya, ma, da = map(int, a.split("-"))
    yb, mb, db = map(int, b.split("-"))
    return (date(yb, mb, db) - date(ya, ma, da)).days


def evidence_window(records, key="sources"):
    """DERIVED, and the only freshness claim any specimen may make:
    min/max of every receipt date in the corpus. Fully determined by committed
    data, so it cannot drift and cannot overstate."""
    dates = sorted({s["date"] for r in records for s in (r.get(key) or [])})
    return dates[0], dates[-1]


# ----------------------------------------------------------------- geography
def rings(geom):
    if geom["type"] == "Polygon":
        return geom["coordinates"]
    return [r for poly in geom["coordinates"] for r in poly]


def load_substrate(path, key="iso_a3"):
    """Vendored boundaries, keyed for joining. SUBSTRATE ONLY: carries no
    corpus property and supports no claim. See vendor/boundaries/PROVENANCE.md."""
    d = json.load(open(path))
    return {f["properties"][key]: f["geometry"] for f in d["features"]}


def svg_path(geom, fx, fy):
    out = []
    for r in rings(geom):
        out.append("M" + " L".join("%.1f,%.1f" % (fx(p[0]), fy(p[1])) for p in r) + " Z")
    return " ".join(out)


def centroid(geom):
    """Anchor on the largest part. A mean over all rings drags the label into
    the sea for archipelagos and for states with offshore islands."""
    best, best_area = None, -1.0
    for r in rings(geom):
        xs = [p[0] for p in r]
        ys = [p[1] for p in r]
        a = (max(xs) - min(xs)) * (max(ys) - min(ys))
        if a > best_area:
            best, best_area = r, a
    return (sum(p[0] for p in best) / len(best),
            sum(p[1] for p in best) / len(best))


def extent(geom):
    """(minx, miny, maxx, maxy) across all parts."""
    pts = [p for r in rings(geom) for p in r]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def place_labels(items, pad_y=12.5,
                 steps=(0, 13, -13, 26, -26, 39, -39, 52, -52),
                 bounds=None, obstacles=()):
    """Greedy vertical de-collision. items: (key, x0, x1, y_pref) -> {key: y}.
    Presentational only: never moves a mark, only its label."""
    placed = list(obstacles)
    out = {}
    for key, x0, x1, base in items:
        ly = base
        for step in steps:
            ly = base + step
            if bounds and not (bounds[0] <= ly <= bounds[1]):
                continue
            if not any(not (x1 < px0 or x0 > px1) and abs(ly - py) < pad_y
                       for px0, px1, py in placed):
                break
        placed.append((x0, x1, ly))
        out[key] = ly
    return out


# --------------------------------------------------- corpus coverage guard
def field_coverage(page_html, records, skip=("sources",)):
    """How many records have each of their text fields actually rendered?

    Exists because the same defect appeared in two specimens running: the
    renderer described the corpus's *shape* immaculately while leaving the
    corpus's *subject* unrendered. Hormuz shipped with `current_status` at 0/12;
    insurance shipped with `insurer_exits`, `regulatory_response` and
    `mortgage_impact` all at 0/6. Both were caught by a human reading the page,
    which is too late and too expensive.
    """
    fields = {}
    for r in records:
        for k, v in r.items():
            if k in skip or k.startswith("_") or not isinstance(v, str):
                continue
            if len(v) < 25 or " " not in v.strip():
                continue           # enums, slugs and labels are not subject matter
            fields.setdefault(k, [0, 0])
            fields[k][1] += 1
            if html.escape(v, quote=True) in page_html or v in page_html:
                fields[k][0] += 1
    return {k: tuple(v) for k, v in sorted(fields.items())}


def require_subject_fields(page_html, records, skip=("sources",)):
    """Fail the build if any substantial prose field is rendered for NO record.

    A field may legitimately be partially rendered — a specimen can quote three
    of twelve. Zero is different: zero means the corpus said something and the
    page never repeated it. That is the recurring failure, so it is an error
    rather than a warning."""
    cov = field_coverage(page_html, records, skip=skip)
    dead = [k for k, (got, tot) in cov.items() if got == 0]
    if dead:
        lines = ["corpus fields present in the data but rendered nowhere on the page:"]
        lines += ["    %-24s 0/%d" % (k, cov[k][1]) for k in dead]
        lines.append("")
        lines.append("  Render them, or if a field is genuinely not for this page,")
        lines.append("  pass it in skip=(...) with a reason in the call site.")
        raise SystemExit("error: " + "\n".join(lines))
    return cov


# ------------------------------------------------------------------ fragments
def head(title, description, css):
    """Document head. Mechanism: every specimen needs one; none of it is
    editorial."""
    return f"""<!DOCTYPE html>
<html lang="en"><head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="preconnect" href="https://fonts.bunny.net">
<link rel="stylesheet" href="https://fonts.bunny.net/css?family=newsreader:400,500,600&display=swap">
<style>{css}</style></head><body>
"""


def evidence_banner(window_hi, stale, source_path):
    """Staleness warning, carried in production.

    Must survive being screenshotted out of context, which is why it is heavy
    and states the date rather than hinting at it. This is the honest freshness
    claim: max(citation date), fully determined by committed data. It is not a
    'last reviewed' stamp, because nothing keeps one of those true."""
    return f"""<div class="evbanner">
<span class="big">Evidence current to {window_hi} — {stale} days ago</span>
Every present-tense claim below is present tense as of {window_hi}, not as of reading.
Built from <code>{e(source_path)}</code>.
</div>
"""


def register_line():
    """The register marks, compact. R2a: infrastructure, not protagonist — the
    definitions belong at the audit floor, not above the first finding."""
    return """<div class="regline">
  <span class="o">●</span> observed &nbsp;·&nbsp; <span class="d">◌</span> derived
  &nbsp;·&nbsp; <span class="i">▌</span> interpreted &nbsp;·&nbsp;
  <span class="r">⊘</span> refused &nbsp;— marks appear beside claims; defined under Method.
</div>
"""


def register_definitions():
    return """<div class="regdefs">
  <div class="r-observed"><div class="rl">● Observed</div><div class="rd">Read off a cited source. Has a unit and a receipt.</div></div>
  <div class="r-derived"><div class="rl">◌ Derived</div><div class="rd">Computed here. Shows its rule; carries no receipt.</div></div>
  <div class="r-interpreted"><div class="rl">▌ Interpreted</div><div class="rd">Authored judgment. Publishable — and not evidence.</div></div>
  <div class="r-refused"><div class="rl">⊘ Refused</div><div class="rd">Declined or unavailable. Shown, not omitted.</div></div>
</div>
"""


def audit_divider(note):
    return (f'<div class="auditline">Audit<span>{e(note)}</span></div>\n')


def receipts_table(rows, absence_note=None):
    """rows: (supports, publisher, url, date). One column per field that exists;
    absence is stated once in prose rather than rendered as a column of dashes."""
    o = []
    if absence_note:
        o.append('<div class="absence">%s</div>' % absence_note)
    o.append('<div class="scroll"><table>'
             '<thead><tr><th>Supports</th><th>Publisher</th><th>Published</th>'
             '</tr></thead><tbody>')
    for sup, pub, url, date in rows:
        o.append('<tr><td class="k">%s</td><td><a href="%s" rel="noopener">%s</a></td>'
                 '<td class="n">%s</td></tr>' % (e(sup), e(url), e(pub), e(date)))
    o.append("</tbody></table></div>")
    return "\n".join(o)


CSS = """
:root{
  --ink:#0a0a0a; --panel:#101215; --rule:#22262b; --rule-soft:#171a1e;
  --tx:#e2e7ed; --tx-mid:#98a1ab; --tx-dim:#69727c; --tx-faint:#525b64;
  --observed:#4fc3f7; --derived:#e0a03a; --interpreted:#b9c2cc; --refused:#79828c;
  --hot:#ef5350;
  --serif:'Newsreader',Georgia,'Times New Roman',serif;
  --sans:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;
}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
body{background:var(--ink);color:var(--tx);font-family:var(--sans);
  font-size:15px;line-height:1.62;-webkit-font-smoothing:antialiased}
.wrap{max-width:880px;margin:0 auto;padding:0 24px 110px}

.evbanner,.evbanner{background:#2a1c05;border-bottom:2px solid #6b4d12;color:#f0cf8d;
  font-family:var(--mono);font-size:12px;letter-spacing:.02em;
  padding:13px 24px;line-height:1.55}
.evbanner b{color:#ffdf9c}
.evbanner .big{display:block;font-size:14px;font-weight:700;letter-spacing:.06em;
  text-transform:uppercase;color:#ffd98a;margin-bottom:3px}

/* ---------- question + answer ---------- */
.kicker{font-size:11px;font-weight:700;text-transform:uppercase;
  letter-spacing:.19em;color:var(--tx-dim);padding-top:62px}
h1{font-family:var(--serif);font-size:47px;font-weight:600;line-height:1.04;
  letter-spacing:-.02em;color:#fff;margin:20px 0 22px;max-width:19ch}
.answer{font-family:var(--serif);font-size:21px;line-height:1.48;
  color:#ccd4dd;max-width:56ch;margin-bottom:38px}
.answer strong{color:#fff;font-weight:600}

/* ---------- summary strip: the 20-second read ---------- */
.strip{display:grid;grid-template-columns:repeat(5,1fr);
  border-top:1px solid var(--rule);border-bottom:1px solid var(--rule);
  margin-bottom:16px}
.strip .s{padding:16px 16px 15px 0}
.strip .s+.s{padding-left:18px;border-left:1px solid var(--rule-soft)}
.strip .n{font-family:var(--serif);font-size:33px;font-weight:600;color:#fff;
  line-height:1;letter-spacing:-.02em}
.strip .l{font-size:12px;color:var(--tx-dim);line-height:1.38;margin-top:8px}
.strip .anom .n{color:var(--derived)}
.strip .anom .l{color:#a8853f}
.strip .n .den{font-size:19px;color:var(--tx-dim)}

.stamp{display:flex;flex-wrap:wrap;gap:0 22px;font-family:var(--mono);
  font-size:11px;color:var(--tx-faint);margin-bottom:46px}
.stamp b{color:var(--tx-dim);font-weight:400}
.stamp .stale{color:var(--hot)}

/* ---------- refusal + register key ---------- */
.refusal{border-left:2px solid var(--refused);padding:1px 0 1px 17px;
  margin:0 0 30px;font-family:var(--serif);font-size:17.5px;line-height:1.48;
  color:#a9b2bc;max-width:60ch}
.refusal b{color:#e2e7ed;font-weight:600}

.regkey{display:grid;grid-template-columns:repeat(4,1fr);gap:0 26px;
  border-top:1px solid var(--rule);padding-top:13px;margin-bottom:24px}
.regkey .rl{font-family:var(--mono);font-size:10px;font-weight:700;
  letter-spacing:.11em;text-transform:uppercase;margin-bottom:4px}
.regkey .rd{font-size:12px;color:var(--tx-faint);line-height:1.42}
.r-observed .rl{color:var(--observed)} .r-derived .rl{color:var(--derived)}
.r-interpreted .rl{color:var(--interpreted)} .r-refused .rl{color:var(--refused)}

.mk{font-family:var(--mono);font-size:9.5px;font-weight:700;letter-spacing:.09em;
  text-transform:uppercase;vertical-align:.18em;padding:1px 4px;margin-left:5px;
  border:1px solid currentColor;white-space:nowrap}
.mk-o{color:var(--observed)} .mk-d{color:var(--derived)}
.mk-i{color:var(--interpreted)} .mk-r{color:var(--refused)}

/* ---------- section rhythm: air between evidentiary moves ---------- */
.sec{margin-top:104px}
.rung{font-family:var(--mono);font-size:10px;letter-spacing:.16em;
  text-transform:uppercase;color:var(--tx-faint);margin-bottom:12px}
h2{font-family:var(--serif);font-size:27px;font-weight:600;color:#fff;
  line-height:1.18;margin:0 0 10px;letter-spacing:-.012em;max-width:24ch}
.lede{font-family:var(--serif);font-size:17.5px;color:#a4aeb8;line-height:1.5;
  max-width:60ch;margin-bottom:26px}
p{max-width:64ch;margin-bottom:14px}

/* ---------- figures: finding is loud, apparatus is quiet ---------- */
figure{margin:0}
figcaption{font-family:var(--serif);font-size:23px;font-weight:600;color:#fff;
  line-height:1.22;margin-bottom:8px;max-width:27ch}
.fignote{font-size:13.5px;color:var(--tx-dim);max-width:58ch;margin-bottom:26px}
.figfoot{border-top:1px solid var(--rule-soft);margin-top:20px;padding-top:11px;
  font-family:var(--mono);font-size:10.5px;color:var(--tx-faint);line-height:1.8}
.figfoot b{color:var(--tx-dim);font-weight:400}
.figfoot span{display:inline-block;margin-right:20px;max-width:100%;
  vertical-align:top}
.figfoot span.long{white-space:normal;display:block;margin-right:0}

/* ---------- bar rows ---------- */
.bars{border-top:1px solid var(--rule)}
.row{display:grid;grid-template-columns:110px 1fr 58px;gap:14px;
  align-items:baseline;padding:10px 0;border-bottom:1px solid var(--rule-soft)}
.row .nm{font-size:14.5px;color:var(--tx)}
.row .tr{position:relative;height:16px;top:3px}
.row .bar{position:absolute;left:0;top:3px;height:11px;background:var(--observed);
  opacity:.85}
/* a published range: drawn as the span it is, with the stored point marked */
.row .span{position:absolute;top:3px;height:11px;background:var(--observed);opacity:.34;
  border-left:1px solid rgba(79,195,247,.85);border-right:1px solid rgba(79,195,247,.85)}
.row .pt{position:absolute;top:0px;height:17px;width:2px;background:var(--observed)}
/* figures that count something else: no axis, no bar, no implied comparison */
.offaxis{margin-top:22px;padding:16px 0 4px;border-top:1px solid var(--rule)}
.offaxis .t{font-family:var(--mono);font-size:10.5px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--tx-mid);margin-bottom:5px}
.offaxis .d{font-size:13px;color:var(--tx-dim);max-width:58ch;line-height:1.5;
  margin-bottom:10px}
.offtbl{font-size:13px}
.offtbl td{border-bottom:1px solid var(--rule-soft);padding:8px 14px 8px 0}
.offtbl .wq{color:var(--tx-faint);font-size:12px}
.offtbl .wq q{font-style:italic;quotes:none}
.row .val{font-family:var(--mono);font-size:13px;color:var(--tx);text-align:right}
.row .note{grid-column:2/4;font-size:11.5px;color:#93763b;margin-top:3px;
  line-height:1.4}
.row.null .tr{background:repeating-linear-gradient(45deg,transparent,transparent 4px,
  #1e2227 5px,#1e2227 6px);height:11px;top:6px;border:1px dashed #2b3037}
.row.null .val{color:var(--refused);font-size:10.5px}
.row.null .note{color:var(--tx-faint)}
.sixty{position:absolute;top:-4px;bottom:-4px;width:1px;background:var(--hot);
  opacity:.5}
.axis{display:grid;grid-template-columns:110px 1fr 58px;gap:14px;
  font-family:var(--mono);font-size:10px;color:var(--tx-faint);padding-top:6px}
.axis .tr{position:relative;height:12px}
.axis .tick{position:absolute;transform:translateX(-50%);white-space:nowrap}
.bandsplit{padding:18px 0 9px;border-bottom:1px solid var(--rule);margin-top:5px}
.bandsplit .t{font-family:var(--mono);font-size:10.5px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--tx-mid);margin-bottom:5px}
.bandsplit .d{font-size:13px;color:var(--tx-dim);max-width:58ch;line-height:1.5}

/* ---------- interpretation: authored, subordinate to the finding ---------- */
.interp{border-left:2px solid #3b434c;padding:2px 0 2px 18px;margin:30px 0 0;
  max-width:58ch}
.interp p{font-family:var(--serif);font-size:17.5px;line-height:1.5;
  color:#b6bfc9;margin-bottom:0}
.interp .by{font-family:var(--mono);font-size:10px;letter-spacing:.11em;
  text-transform:uppercase;color:var(--tx-faint);margin-top:11px}

/* ---------- tables ---------- */
table{border-collapse:collapse;width:100%;font-size:13.5px}
th{text-align:left;font-family:var(--mono);font-size:10px;font-weight:700;
  letter-spacing:.1em;text-transform:uppercase;color:var(--tx-faint);
  border-bottom:1px solid var(--rule);padding:0 12px 8px 0;vertical-align:bottom}
td{border-bottom:1px solid var(--rule-soft);padding:10px 12px 10px 0;
  vertical-align:top;line-height:1.5;color:var(--tx-mid)}
td.k{color:var(--tx);white-space:nowrap}
td.n{font-family:var(--mono);color:var(--tx);white-space:nowrap}
td q{color:#aab3bd;font-style:italic;quotes:none}
.scroll{overflow-x:auto}

/* ---------- supporting figure: quieter than a major beat ---------- */
figure.support{max-width:660px}
figure.support figcaption{font-family:var(--sans);font-size:16px;font-weight:600;
  color:#c3ccd5;max-width:46ch;line-height:1.35}
figure.support .fignote{font-size:12.5px;max-width:52ch;margin-bottom:18px}

/* ---------- country ledger ---------- */
table.ledger{font-size:13px}
table.ledger th{padding-bottom:9px}
table.ledger tr.lr>td{border-bottom:none;padding:12px 12px 2px 0}
table.ledger tr.claimrow>td{padding:0 0 13px 0;border-bottom:1px solid var(--rule-soft)}
.ledger .cty{font-family:var(--serif);font-size:17px;font-weight:600;color:#fff;
  padding-right:16px}
.ledger .bandc{font-family:var(--mono);font-size:10.5px;color:var(--interpreted);
  letter-spacing:.02em;white-space:nowrap}
.ledger .bandc::before{content:"▌";color:#3b434c;margin-right:5px}
.ledger td.n{font-size:11.5px;text-align:right;color:var(--tx-mid);padding-right:14px}
.ledger td.miss{color:#b4655f}
.ledger .cf-low{color:#c97a72} .ledger .cf-medium{color:#b6924e}
.ledger .cf-high{color:var(--tx-faint)}
.ledger .cl{font-size:14px;color:var(--tx-mid);line-height:1.5}
.ledger .qn{display:block;font-family:var(--mono);font-size:10.5px;color:var(--tx-faint);
  margin-top:5px;line-height:1.45}

/* ---------- audit register: deliberate, not another chapter ---------- */
.sec.audit{border-top:2px solid #39414a;padding-top:30px;margin-top:96px}
.sec.audit .rung{color:#8d97a1}
.sec.audit h2{font-size:25px}
.sec.audit+.sec.audit{margin-top:68px}

/* ---------- country index (retired; ledger replaces it) ---------- */
.idx{border-top:1px solid var(--rule)}
.idx .c{padding:16px 0;border-bottom:1px solid var(--rule-soft)}
.idx .h{display:flex;flex-wrap:wrap;gap:10px;align-items:baseline;margin-bottom:5px}
.idx .cn{font-family:var(--serif);font-size:19.5px;font-weight:600;color:#fff}
.idx .band{font-family:var(--mono);font-size:10px;letter-spacing:.06em;
  color:var(--interpreted);border:1px solid #2b3138;padding:1px 6px}
.idx .conf{font-family:var(--mono);font-size:10px;color:var(--tx-faint)}
.idx .cl{font-size:14.5px;color:var(--tx-mid);max-width:64ch;line-height:1.5;
  margin-bottom:5px}
.idx .meta{font-family:var(--mono);font-size:10.5px;color:var(--tx-faint)}
.idx .meta .miss{color:#b4655f}

/* ---------- boundary / method ---------- */
.bound li,.meth li{margin:0 0 12px 20px;max-width:62ch;color:var(--tx-mid)}
.pull{font-family:var(--serif);font-size:22px;line-height:1.36;color:#fff;
  max-width:44ch;margin:0 0 26px}
.rule1{border-left:2px solid var(--interpreted);padding:3px 0 3px 18px;
  margin:0 0 24px;font-family:var(--serif);font-size:19px;line-height:1.45;
  color:#e2e7ed;max-width:58ch}

.absence{border-left:2px solid #b4655f;padding:2px 0 2px 17px;margin:0 0 26px;
  font-size:14px;line-height:1.55;color:var(--tx-mid);max-width:62ch}
.absence b{color:#e2e7ed}
.rcpt a{color:var(--observed);text-decoration:none}
.rcpt a:hover{text-decoration:underline}
.rcpt td{font-size:12.5px}

footer{margin-top:96px;border-top:1px solid var(--rule);padding-top:22px;
  font-size:12.5px;color:var(--tx-faint);line-height:1.7}
footer a{color:var(--observed);text-decoration:none}

@media (max-width:760px){
  h1{font-size:33px}
  .answer{font-size:18.5px}
  .strip{grid-template-columns:1fr 1fr}
  .strip .s+.s{padding-left:0;border-left:none}
  .strip .s{border-top:1px solid var(--rule-soft);padding:13px 14px 13px 0}
  .strip .s:nth-child(-n+2){border-top:none}
  .regkey{grid-template-columns:1fr 1fr;gap:14px 20px}
  .sec{margin-top:72px}
  .row,.axis{grid-template-columns:86px 1fr 50px;gap:10px}
  .row .nm{font-size:13px}
  .figfoot span{display:block;margin-right:0}
  table.ledger{font-size:12px}
  .ledger .cty{font-size:15px;padding-right:10px}
  .ledger .bandc{font-size:9.5px}
  .ledger td.n{padding-right:8px;font-size:10.5px}
  .ledger .cl{font-size:13px}
  figure.support .fignote{max-width:none}
}
@media print{body{background:#fff;color:#000}.evbanner{background:#eee;color:#000}}
"""

CSS += """
/* ---------- compact register line: infrastructure, not protagonist ---------- */
.regline{font-family:var(--mono);font-size:10.5px;color:var(--tx-faint);
  letter-spacing:.04em;margin-bottom:44px}
.regline b{font-weight:400}
.regline .o{color:var(--observed)} .regline .d{color:var(--derived)}
.regline .i{color:var(--interpreted)} .regline .r{color:var(--refused)}

/* ---------- audit divider ---------- */
.auditline{margin-top:110px;border-top:2px solid #39414a;padding-top:14px;
  font-family:var(--mono);font-size:10.5px;letter-spacing:.16em;
  text-transform:uppercase;color:#8d97a1}
.auditline span{color:var(--tx-faint);letter-spacing:.02em;text-transform:none;
  margin-left:14px}
.sec.audit{border-top:none;padding-top:0;margin-top:64px}
.sec.audit .rung{color:#8d97a1}

/* register definitions, demoted to the audit floor */
.regdefs{display:grid;grid-template-columns:repeat(2,1fr);gap:12px 26px;
  margin:0 0 26px}
.regdefs .rl{font-family:var(--mono);font-size:10px;font-weight:700;
  letter-spacing:.11em;text-transform:uppercase;margin-bottom:3px}
.regdefs .rd{font-size:12.5px;color:var(--tx-dim);line-height:1.45}

@media (max-width:760px){
  .turn .e{grid-template-columns:1fr;gap:8px}
  .regdefs{grid-template-columns:1fr}
  .payoff{font-size:21px}
}
"""
