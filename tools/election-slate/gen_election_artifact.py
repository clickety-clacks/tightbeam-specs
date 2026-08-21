#!/usr/bin/env python3
"""Render the 0.2.0 election recommendation in the tightbeam spec house style."""
import html
import json
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from eli5 import ELI5
WITH_DIFF = "--with-diff" in sys.argv
PENDING = {"c4450c8d", "7f068d0c"}  # Mike 2026-08-21: selection pends on the force-roles ruling

SRC = "/home/mike/.tightbeam/work/9a2b5c417784/specs/tightbeam/0.2.0-spirit-and-work-sweep.md"
OUT = sys.argv[1]

text = open(SRC).read()

def bullets(section_text):
    out = []
    for m in re.finditer(r"^- `(wi_[0-9a-f-]+)` — (.+?)(?=\n- `|\n\n|\n#|\Z)", section_text, re.M | re.S):
        out.append((m.group(1), " ".join(m.group(2).split())))
    return out

def section(title):
    m = re.search(rf"### {re.escape(title)}\n(.*?)(?=\n### |\n## )", text, re.S)
    return bullets(m.group(1)) if m else []

A_SECTIONS = [
    ("a1", "Assignment and parent handoff"),
    ("a2", "Wake delivery and turn execution"),
    ("a3", "Recovery and continuity"),
    ("a4", "Supervision and liveness"),
    ("a5", "Truthful identity, evidence, and verdict state"),
]
a_groups = [(sid, t, section(t)) for sid, t in A_SECTIONS]
evidence = section("Evidence or duplicate rows, not independent candidates")
outside = section("Outside this 0.2 nervous-system recommendation")
list_b = bullets(re.search(r"## List B — Pressing bug election\n(.*?)\n## ", text, re.S).group(1))

a_ids = {i for _, _, rows in a_groups for i, _ in rows}
b_ids = {i for i, _ in list_b}
overlap = a_ids & b_ids
n_a, n_b, n_u = len(a_ids), len(b_ids), len(a_ids | b_ids)

core_m = re.search(r"### TIER CORE.*?(?=### TIER POST-CORE)", text, re.S)
core_ids = set(re.findall(r"`(wi_[0-9a-f-]+)`", core_m.group(0))) if core_m else set()
n_core = len(core_ids)
print(f"counts from doc: A={n_a} B={n_b} overlap={len(overlap)} union={n_u}", file=sys.stderr)

def item(wid, desc, badge=None, bug=False, eli5=False):
    short = wid[3:11]
    b = f' <span class="badge{" bug" if bug else ""}">{badge}</span>' if badge else ""
    c = ' <span class="badge core">core</span>' if wid in core_ids else ""
    cls = ' class="is-core"' if wid in core_ids else ""
    pend = (' <span class="badge pend">pends on roles ruling</span>'
            if short in PENDING else "")
    e = ""
    if eli5 and short in ELI5:
        e = f'<span class="eli5">{html.escape(ELI5[short])}</span>'
    return (f'<li id="{wid[:11]}"{cls}><code class="wid" title="{wid}">{short}</code>'
            f'<span>{html.escape(desc)}{c}{b}{pend}{e}</span></li>')

p = []
p.append("""<title>Tightbeam 0.2.0 Election</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
  :root {
    --bg: #F8FAF9; --surface: #EFF4F2; --ink: #1C2B2D; --muted: #5E7073;
    --accent: #0E7C86; --accent-ink: #0A5A62; --line: #DCE6E3;
    --code-bg: #EDF2F1; --tag-bg: #E1EDEC; --bug: #A03B2E; --bug-bg: #F4E7E3;
    --pend: #8a6d1f; --pend-bg: #f5edd7;
  }
  @media (prefers-color-scheme: dark) {
    :root:not([data-theme="light"]) {
      --bg: #101A1C; --surface: #162225; --ink: #D8E5E2; --muted: #8CA3A0;
      --accent: #45B8C4; --accent-ink: #63C9D3; --line: #243437;
      --code-bg: #142023; --tag-bg: #1B2E31; --bug: #DE8A76; --bug-bg: #2C201C;
      --pend: #dfc06a; --pend-bg: #2b2514;
    }
  }
  :root[data-theme="dark"] {
    --bg: #101A1C; --surface: #162225; --ink: #D8E5E2; --muted: #8CA3A0;
    --accent: #45B8C4; --accent-ink: #63C9D3; --line: #243437;
    --code-bg: #142023; --tag-bg: #1B2E31; --bug: #DE8A76; --bug-bg: #2C201C;
    --pend: #dfc06a; --pend-bg: #2b2514;
  }
  * { box-sizing: border-box; }
  body {
    background: var(--bg); color: var(--ink);
    font-family: "Source Serif 4", Georgia, serif;
    font-size: 1.05rem; line-height: 1.62; margin: 0; padding: 0 1.25rem 6rem;
  }
  .sheet { max-width: 72ch; margin: 0 auto; }
  header { padding: 3.5rem 0 1.75rem; border-bottom: 2px solid var(--ink); }
  .kicker {
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .72rem; letter-spacing: .14em; text-transform: uppercase;
    color: var(--accent); margin: 0 0 .8rem;
  }
  h1 {
    font-family: Archivo, "Helvetica Neue", sans-serif; font-weight: 700;
    font-size: clamp(1.9rem, 5vw, 2.6rem); line-height: 1.08;
    margin: 0 0 .9rem; text-wrap: balance;
  }
  .statusline {
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .78rem; color: var(--muted); line-height: 1.7; margin: 0;
  }
  .statusline b { color: var(--ink); font-weight: 600; }
  nav { display: flex; flex-wrap: wrap; gap: .4rem .5rem; padding: 1.1rem 0 0; }
  nav a {
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .72rem; letter-spacing: .02em; color: var(--accent-ink);
    text-decoration: none; background: var(--tag-bg);
    border: 1px solid var(--line); padding: .28rem .6rem; border-radius: 2px;
  }
  nav a:hover, nav a:focus-visible { border-color: var(--accent); outline: none; }
  .stats { display: flex; flex-wrap: wrap; gap: .75rem; margin: 1.6rem 0 0; }
  .stat {
    background: var(--surface); border: 1px solid var(--line);
    border-radius: 3px; padding: .6rem 1rem; min-width: 7.5rem;
  }
  .stat b {
    font-family: Archivo, "Helvetica Neue", sans-serif;
    display: block; font-size: 1.45rem; font-variant-numeric: tabular-nums;
  }
  .stat span {
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .68rem; letter-spacing: .08em; text-transform: uppercase;
    color: var(--muted);
  }
  h2 {
    font-family: Archivo, "Helvetica Neue", sans-serif; font-weight: 600;
    font-size: 1.28rem; text-wrap: balance; margin: 3rem 0 .4rem;
    padding-top: 1.4rem; border-top: 1px solid var(--line);
  }
  h2 .no {
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .8rem; color: var(--accent); margin-right: .55rem; font-weight: 500;
  }
  h3 {
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .74rem; letter-spacing: .1em; text-transform: uppercase;
    color: var(--muted); font-weight: 500; margin: 1.8rem 0 .3rem;
  }
  h3 b { color: var(--accent-ink); font-weight: 600; }
  p { margin: .85rem 0; }
  .prov { color: var(--muted); font-size: .95rem; }
  .prov b { color: var(--ink); }
  code {
    font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: .86em;
    background: var(--code-bg); border: 1px solid var(--line);
    border-radius: 2px; padding: .06em .3em;
  }
  ul.items { list-style: none; padding: 0; margin: .4rem 0 0; }
  ul.items li {
    display: flex; gap: .7rem; align-items: baseline;
    padding: .42rem 0; border-bottom: 1px solid var(--line);
  }
  ul.items li > span { flex: 1; font-size: .97rem; }
  .wid { white-space: nowrap; color: var(--accent-ink); }
  .badge {
    font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .66rem; font-weight: 600; letter-spacing: .04em;
    text-transform: uppercase; white-space: nowrap; vertical-align: .1em;
    color: var(--accent-ink); background: var(--tag-bg);
    border: 1px solid var(--line); border-radius: 2px; padding: .08rem .4rem;
  }
  .badge.bug { color: var(--bug); background: var(--bug-bg); }
  .badge.core { color: var(--bg); background: var(--accent); border-color: var(--accent); }
  .badge.pend { color: var(--pend); background: var(--pend-bg); border-color: var(--pend); }
  li.is-core { box-shadow: inset 3px 0 0 var(--accent); padding-left: .6rem; }
  .eli5 {
    display: block; color: var(--muted); font-size: .88rem; line-height: 1.5;
    margin-top: .2rem; max-width: 62ch;
  }
  .dim ul.items li { color: var(--muted); }
  .dim ul.items li .wid { color: var(--muted); }
  .callout {
    background: var(--surface); border-left: 3px solid var(--accent);
    padding: .8rem 1.1rem; margin: 1.2rem 0; font-size: .97rem;
  }
  .callout p { margin: .4rem 0; }
  ol { padding-left: 1.4rem; }
  ol li { margin: .3rem 0; }
  a { color: var(--accent-ink); }
  ::selection { background: var(--accent); color: var(--bg); }
  @media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth; } }
</style>

<div class="sheet">
<header>
  <p class="kicker">Tightbeam &middot; 0.2.0 &middot; election recommendation r1</p>
  <h1>Tightbeam 0.2.0 — the election slate</h1>
  <p class="statusline">
    swept <b>398 work items</b> on <b>2026-08-20</b> by
    <b>Product owner — Tightbeam 0.2.0</b> (s_80b6e0c8) &middot;
    boundary ruled <b>actionable only</b> (Mike) &middot;
    source of record: <b>0.2.0-spirit-and-work-sweep.md</b> in tightbeam-specs
  </p>
  <nav aria-label="Sections">
    <a href="#rule">election rule</a><a href="#lista">list A</a><a href="#listb">list B</a><a href="#evidence">evidence rows</a><a href="#outside">outside</a><a href="#transferred">transferred</a><a href="#exclusions">exclusions</a>
  </nav>""")

p.append(f"""
  <div class="stats">
    <div class="stat"><b>{n_u}</b><span>elected items</span></div>
    <div class="stat"><b>{n_core}</b><span>MVP core</span></div>
    <div class="stat"><b>{n_u - n_core}</b><span>post-core</span></div>
    <div class="stat"><b>{n_a}</b><span>list A &middot; nervous system</span></div>
    <div class="stat"><b>{n_b}</b><span>list B &middot; pressing bugs</span></div>
  </div>
</header>

<h2 id="rule"><span class="no">&sect;1</span>The election rule</h2>
<p>0.2.0 is the first version built on the worker/exec nervous-system model. Its topology is
assignment, turn execution, recovery, supervision, and truthful state. An existing work item
is recommended when its outcome directly changes at least one of:</p>
<ol>
<li>assignment identity, custody, state, or parent handoff;</li>
<li>wake delivery or turn execution;</li>
<li>recovery of a session, adapter, harness, client, or unfinished obligation;</li>
<li>supervision population, liveness, escalation, or bounded observation;</li>
<li>the durable truth those mechanisms expose about identity, execution, evidence, or completion.</li>
</ol>
<div class="callout">
<p>Election recommends 0.2.0 membership. It moves no custody, changes no assignment,
overrides no release target, and does not guarantee an item ships. Recommendation: elect
every item on either list &mdash; <b>{n_u} unique items</b>.</p>
<p><b>MVP tiering (Mike, 2026-08-21):</b> the <b>{n_core} items</b> marked
<span class="badge core">core</span> are the first cut &mdash; the truthful end-to-end work
loop, security and data-loss criticals, and the red suite on main. Mike's stance verbatim:
&ldquo;not looking for perfect operations, but a good core that we can apply other work items
to fix various bugs. just enough that the system could work.&rdquo; The other
{n_u - n_core} stay elected and land as ordinary work after the core exists.</p>
</div>

<h2 id="lista"><span class="no">&sect;2</span>List A — nervous-system items ({n_a})</h2>
<p class="prov">Grouped by the part of the topology each item primarily builds. An item
supporting several parts appears once, under its primary purpose.</p>""")

for i, (sid, title, rows) in enumerate(a_groups, 1):
    p.append(f'<h3 id="{sid}"><b>A.{i}</b> &middot; {html.escape(title)} ({len(rows)})</h3><ul class="items">')
    for wid, desc in rows:
        p.append(item(wid, desc, "also a pressing bug" if wid in overlap else None, bug=True, eli5=True))
    p.append("</ul>")

p.append(f"""
<h2 id="listb"><span class="no">&sect;3</span>List B — pressing bugs ({n_b})</h2>
<p class="prov">Elected for security, data-loss, silent-intent-loss, deploy-safety, or
first-boot impact, whether or not they concern the nervous system. Urgency and architectural
relevance are separate judgments; {len(overlap)} items carry both.</p>
<ul class="items">""")
for wid, desc in list_b:
    p.append(item(wid, desc, "also list A" if wid in overlap else None))
p.append("</ul>")

p.append(f"""
<div class="dim">
<h2 id="evidence"><span class="no">&sect;4</span>Evidence, duplicate, or conditional rows ({len(evidence)}) — not elected</h2>
<p class="prov">These stay attached to their canonical outcomes as evidence. A row here is
elected only if it also stands in list B.</p>
<ul class="items">""")
for wid, desc in evidence:
    p.append(item(wid, desc, "elected via list B" if wid in b_ids else None))
p.append(f"""</ul>

<h2 id="outside"><span class="no">&sect;5</span>Valid work outside this recommendation ({len(outside)})</h2>
<p class="prov">Real work whose primary outcome does not directly build the five topology parts.</p>
<ul class="items">""")
for wid, desc in outside:
    p.append(item(wid, desc))
p.append("""</ul>

<h2 id="transferred"><span class="no">&sect;6</span>Transferred out of 0.2 scope (1)</h2>
<ul class="items">
<li><code class="wid" title="wi_42156d31-6d80-47cc-9e6b-394913ea2923">42156d31</code>
<span>verdict artifact-pointer work, moved by Mike to versionless Tightbeam Relief custody
under asg_99dac51e; 0.2 performs no further design, review, implementation, or scheduling
for it.</span></li>
</ul>
</div>

<h2 id="exclusions"><span class="no">&sect;7</span>Standing exclusions</h2>
<p class="req">Items whose requested mutation targets 0.1.8 only are evidence; 0.1.8 is frozen.</p>
<p class="req">Clawline, Surf Ace, Lachesis, ATC, and host-operations items remain with their
existing product owners unless the Tightbeam half is separately identified above.</p>
<p class="req">Closed and failed items are evidence unless an active successor row still
requires a current 0.2 decision.</p>
<p class="req">List membership moves no custody, assignments, branches, or artifacts.</p>

<p class="prov">This page is a reading copy for comment. The source of record is
<code>0.2.0-spirit-and-work-sweep.md</code> in the <b>tightbeam-specs repo</b> (landed
2026-08-21, commit <code>dde35dd</code>); it wins on any divergence. ATC search card
<b>q45</b> shows the same set. Hover any short id for the full <code>wi_</code> id.</p>
</div>""")

if WITH_DIFF:
    import os
    SNAP = __file__.rsplit("/", 1)[0] + "/lista_rows_prev.txt"
    new_lines = []
    for _, _, rows in a_groups:
        for wid, desc in rows:
            short = wid[3:11]
            marker = "  [PENDS ON ROLES RULING]" if short in PENDING else ""
            new_lines.append(f"{short}  {desc}{marker}")
            if short in ELI5:
                new_lines.append(f"          eli5: {ELI5[short]}")
    new_text = "\n".join(new_lines) + "\n"
    if os.path.exists(SNAP):
        old_text = open(SNAP).read()
    else:
        old_text = "\n".join(l for l in new_lines if not l.startswith("          eli5:")) + "\n"
    open(SNAP, "w").write(new_text)
    old_c = json.dumps(old_text)
    new_c = json.dumps(new_text)
    p.append(f"""
<h2 id="changed"><span class="no">&Delta;</span>What changed (your comment: add an eli5 to list A)</h2>
<p class="prov">Every list A row gained a plain-language explainer. Unified diff of the row text, old vs new:</p>
<div id="whatchanged-diff" style="overflow-x:auto"></div>
<script type="module">
  import {{ FileDiff }} from "https://esm.sh/@pierre/diffs@1.2.10?bundle";
  const dark = matchMedia("(prefers-color-scheme: dark)").matches;
  new FileDiff({{ theme: {{ light: "github-light", dark: "github-dark" }},
    themeType: dark ? "dark" : "light", overflow: "wrap", diffStyle: "unified" }}).render({{
    containerWrapper: document.querySelector("#whatchanged-diff"),
    oldFile: {{ name: "list-A.txt", contents: {old_c} }},
    newFile: {{ name: "list-A.txt", contents: {new_c} }},
  }});
</script>""")

open(OUT, "w").write("\n".join(p))
print(f"wrote {OUT}: A={n_a} B={n_b} overlap={len(overlap)} union={n_u}")
