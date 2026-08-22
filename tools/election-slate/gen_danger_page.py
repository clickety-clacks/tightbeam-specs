#!/usr/bin/env python3
"""Render the repurposed sweep doc: headline danger list, record appendix pointer."""
import html
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from eli5 import ELI5

SRC = "/home/mike/src/tightbeam-specs/0.2.0-spirit-and-work-sweep.md"
OUT = sys.argv[1]

text = open(SRC).read()
m = re.search(r"## Egregious and dangerous problems[^\n]*\n(.*?)(?=\n## )", text, re.S)
body = m.group(1)
items = [(w, " ".join(d.split())) for w, d in
         re.findall(r"^- `(wi_[0-9a-f-]+)` — (.+?)(?=\n- `|\n\n|\Z)", body, re.M | re.S)]
n = len(items)
audited = re.search(r"checked all (\d+) actionable", body).group(1)

OLD_67 = set()
rec = text[text.index("## Record appendix"):]
for w in re.findall(r"`(wi_[0-9a-f]{8})", rec):
    OLD_67.add(w)
new_ids = [w for w, _ in items if w[3:11] not in {x[3:11] for x in OLD_67}]

def row(wid, desc):
    short = wid[3:11]
    newb = ' <span class="badge new">surfaced by this audit</span>' if wid in new_ids else ""
    e = (f'<span class="eli5">{html.escape(ELI5[short])}</span>'
         if short in ELI5 else "")
    return (f'<li id="{wid[:11]}"><code class="wid" title="{wid}">{short}</code>'
            f'<span>{html.escape(desc)}{newb}{e}</span></li>')

page = f"""<title>Tightbeam 0.2.0 Election</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;0,8..60,600;1,8..60,400&family=IBM+Plex+Mono:wght@400;500;600&display=swap">
<style>
  :root {{
    --bg: #F8FAF9; --surface: #EFF4F2; --ink: #1C2B2D; --muted: #5E7073;
    --accent: #0E7C86; --accent-ink: #0A5A62; --line: #DCE6E3;
    --code-bg: #EDF2F1; --tag-bg: #E1EDEC; --bug: #A03B2E; --bug-bg: #F4E7E3;
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme="light"]) {{
      --bg: #101A1C; --surface: #162225; --ink: #D8E5E2; --muted: #8CA3A0;
      --accent: #45B8C4; --accent-ink: #63C9D3; --line: #243437;
      --code-bg: #142023; --tag-bg: #1B2E31; --bug: #DE8A76; --bug-bg: #2C201C;
    }}
  }}
  :root[data-theme="dark"] {{
    --bg: #101A1C; --surface: #162225; --ink: #D8E5E2; --muted: #8CA3A0;
    --accent: #45B8C4; --accent-ink: #63C9D3; --line: #243437;
    --code-bg: #142023; --tag-bg: #1B2E31; --bug: #DE8A76; --bug-bg: #2C201C;
  }}
  * {{ box-sizing: border-box; }}
  body {{ background: var(--bg); color: var(--ink);
    font-family: "Source Serif 4", Georgia, serif; font-size: 1.05rem;
    line-height: 1.62; margin: 0; padding: 0 1.25rem 6rem; }}
  .sheet {{ max-width: 72ch; margin: 0 auto; }}
  header {{ padding: 3.5rem 0 1.75rem; border-bottom: 2px solid var(--ink); }}
  .kicker {{ font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .72rem; letter-spacing: .14em; text-transform: uppercase;
    color: var(--bug); margin: 0 0 .8rem; }}
  h1 {{ font-family: Archivo, "Helvetica Neue", sans-serif; font-weight: 700;
    font-size: clamp(1.9rem, 5vw, 2.6rem); line-height: 1.08;
    margin: 0 0 .9rem; text-wrap: balance; }}
  .statusline {{ font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .78rem; color: var(--muted); line-height: 1.7; margin: 0; }}
  .statusline b {{ color: var(--ink); font-weight: 600; }}
  .stats {{ display: flex; flex-wrap: wrap; gap: .75rem; margin: 1.6rem 0 0; }}
  .stat {{ background: var(--surface); border: 1px solid var(--line);
    border-radius: 3px; padding: .6rem 1rem; min-width: 7.5rem; }}
  .stat b {{ font-family: Archivo, "Helvetica Neue", sans-serif; display: block;
    font-size: 1.45rem; font-variant-numeric: tabular-nums; }}
  .stat span {{ font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .68rem; letter-spacing: .08em; text-transform: uppercase;
    color: var(--muted); }}
  h2 {{ font-family: Archivo, "Helvetica Neue", sans-serif; font-weight: 600;
    font-size: 1.28rem; text-wrap: balance; margin: 3rem 0 .4rem;
    padding-top: 1.4rem; border-top: 1px solid var(--line); }}
  h2 .no {{ font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .8rem; color: var(--bug); margin-right: .55rem; font-weight: 500; }}
  p {{ margin: .85rem 0; }}
  .prov {{ color: var(--muted); font-size: .95rem; }}
  .prov b {{ color: var(--ink); }}
  code {{ font-family: "IBM Plex Mono", ui-monospace, monospace; font-size: .86em;
    background: var(--code-bg); border: 1px solid var(--line);
    border-radius: 2px; padding: .06em .3em; }}
  ul.items {{ list-style: none; padding: 0; margin: .4rem 0 0; }}
  ul.items li {{ display: flex; gap: .7rem; align-items: baseline;
    padding: .5rem 0 .5rem .6rem; border-bottom: 1px solid var(--line);
    box-shadow: inset 3px 0 0 var(--bug); }}
  ul.items li > span {{ flex: 1; font-size: .97rem; }}
  .wid {{ white-space: nowrap; color: var(--accent-ink); }}
  .badge {{ font-family: "IBM Plex Mono", ui-monospace, monospace;
    font-size: .66rem; font-weight: 600; letter-spacing: .04em;
    text-transform: uppercase; white-space: nowrap; vertical-align: .1em;
    color: var(--accent-ink); background: var(--tag-bg);
    border: 1px solid var(--line); border-radius: 2px; padding: .08rem .4rem; }}
  .badge.new {{ color: var(--bug); background: var(--bug-bg); border-color: var(--bug); }}
  .eli5 {{ display: block; color: var(--muted); font-size: .88rem; line-height: 1.5;
    margin-top: .2rem; max-width: 62ch; }}
  .callout {{ background: var(--surface); border-left: 3px solid var(--accent);
    padding: .8rem 1.1rem; margin: 1.2rem 0; font-size: .97rem; }}
  .callout p {{ margin: .4rem 0; }}
  a {{ color: var(--accent-ink); }}
  ::selection {{ background: var(--accent); color: var(--bg); }}
</style>

<div class="sheet">
<header>
  <p class="kicker">Tightbeam &middot; 0.2.0 &middot; dangerous problems &middot; r4</p>
  <h1>Tightbeam 0.2.0 — dangerous problems to land</h1>
  <p class="statusline">
    repurposed by <b>Mike, 2026-08-21</b> &middot; audited <b>{audited} actionable items</b>
    (183 open, 35 iceboxed), no nervous-system filter &middot; by
    <b>Product owner — Tightbeam 0.2.0</b> &middot; source of record:
    <b>0.2.0-spirit-and-work-sweep.md</b> in tightbeam-specs (commit 6c42b62)
  </p>
  <div class="stats">
    <div class="stat"><b>{n}</b><span>dangerous problems</span></div>
    <div class="stat"><b>{audited}</b><span>items audited</span></div>
    <div class="stat"><b>{len(new_ids)}</b><span>new to this audit</span></div>
  </div>
</header>

<h2><span class="no">&sect;1</span>The danger bar</h2>
<p>An item qualifies only when the present defect creates a direct <b>security</b>,
<b>privacy</b>, <b>data-loss</b>, <b>identity-forgery</b>, <b>silent-intent-loss</b>, or
<b>destructive-deployment</b> danger. Ordinary reliability, usability, and
smooth-operation defects do not qualify, and relationship to the nervous-system model is
irrelevant. Landing this list changes no custody, assignment, or existing release target.</p>

<h2><span class="no">&sect;2</span>The list ({n})</h2>
<ul class="items">
{chr(10).join(row(w, d) for w, d in items)}
</ul>

<h2><span class="no">&sect;3</span>Record appendix</h2>
<div class="callout">
<p>The former nervous-system election (67 elected, 28-core/39-post-core tiers, family map)
is preserved in the sweep doc's record appendix; it no longer controls the headline. One
finding from it remains load-bearing: <b>TIER REQUIRED is empty</b> &mdash; no existing item
constructs the worker/exec model, so 0.2.0's first construction work is new, and this danger
list is what lands alongside it.</p>
</div>

<p class="prov">Reading copy for comment. The source of record is
<code>0.2.0-spirit-and-work-sweep.md</code> in the tightbeam-specs repo; it wins on any
divergence. Hover any short id for the full <code>wi_</code> id.</p>
</div>
"""
open(OUT, "w").write(page)
print(f"wrote {OUT}: {n} dangers, {len(new_ids)} new, audited {audited}")
