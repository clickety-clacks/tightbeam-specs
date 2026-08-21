# Rails hydra spike — handoff

Written 2026-08-21 by tb02 after a working session with Mike. Audience: the
agent who picks this up. Read `rails-visualization-invariants.md` FIRST —
it is the ruled design (10 invariants); this doc covers only what the spike
settled beneath them, the engine lessons, and what is open.

## Artifacts
- `rails-hydra-spike.html` (this repo) — canonical copy of the accepted 2D
  spike. Deployed copies: serenity:~/rails-hydra.html (Mike's review copy),
  gibson:/tmp/claude-1000/rails-hydra/index.html (working copy; /tmp is
  volatile — this repo's copy is the durable one).
- eezo:~/rails-spike.html — spike 1, the 3D layered form. REJECTED
  (invariant 8). Reference only for what not to do.
- Work item: wi_99d6cb49 (iceboxed). Reopen it when this becomes real work.

## Settled by the spike (beneath the invariants)
- Interaction split: HOVER = isolate hydra + short on-line labels;
  CLICK = flyout callouts with full predicates; empty-space click resets.
- Flyout choreography (Mike-specified, accepted): each note originates at
  the midpoint of the line it describes, small (scale 0.6) and transparent;
  flies to its margin seat over 340ms ease-out (cubic-bezier .22,1,.36,1)
  fading to opaque; its hairline leader then DRAWS from box to line over
  220ms starting ~60% into the flight; notes launch one at a time, 90ms
  stagger, in landed reading order (sorted by y). Reduced-motion: instant.
  Re-selecting replays. Switching/reset cancels cleanly (generation token).
- Panel IA: eyebrow = promise class (small caps, colored); headline = the
  rule's plain-English sentence (every rule has one — keep this, it was
  Mike's explicit re-architecture); tag chip = machine name + layer;
  mechanics lists last.
- Promise colors: proof hsl(140,65%,58%), attention hsl(210,85%,62%),
  economy hsl(40,90%,58%), safety hsl(0,80%,62%). Legend explains the axis.
- Line language as built: trigger solid 2.4px; reads sparse dots
  ("1.5 9" dasharray, 1.1px) — deliberately far from any dash; disarmed
  long dash ("16 8"); create = arrowhead; veto = curve returns to the
  triggering row type ending in red ⊘ glyph.
- Short labels: "on:/reads:/creates:" + qualifier; veto label = the exact
  refusal string (rule_denied: <id>). Hidden at rest, shown on isolation,
  suppressed while that hydra's callouts are open.
- Layout constants that worked: 12 row types on the circle; callout radius
  ≈ node ring + 150; boxes 220px wide, 11px text; ≥8px vertical gaps,
  viewport clamp + exclusion zone for the legend overlay.

## Engine lessons (hard-won; do not relearn)
1. NEVER animate foreignObject content via the compositor (WAAPI/CSS
   transforms). WebKit composites those layers WITHOUT the outer viewBox
   scale: the flight renders unscaled, then snaps on landing. Fix that
   shipped: rAF loop writing SVG `transform` ATTRIBUTES (translate/scale in
   user units) + stroke-dashoffset attribute; settled DOM must equal the
   never-animated DOM.
2. pointer-events on an SVG group does NOT reliably propagate into
   foreignObject HTML in WebKit. Force it: CSS
   `#calloutLayer, #calloutLayer * { pointer-events: none !important }`.
3. Safari WAAPI (where used at all) needs px-unit strings in keyframes.
4. Verify at a SCALED window (e.g. 800×500 vs the viewBox), not 1:1 —
   both engine bugs above are invisible at scale 1.
5. Test rig on gibson: `node --check` on the extracted script; stub-DOM
   execution for ReferenceErrors and teardown-leak accounting; headless
   chromium from the playwright cache (~/.cache/ms-playwright) for
   screenshots. Playwright WEBKIT DOES NOT LAUNCH on gibson (missing
   system libs) — every Safari claim must be eyeballed by Mike on
   serenity/eezo. Budget for that loop.

## Data honesty (spike vs real)
- The 14 embedded hydras: 11 real rules hand-transcribed from the org's
  rules/rails TOMLs; 3 "planned" outcome rails are MOCKS and must NOT
  appear in a real build (invariant 1/6: only installed rules render;
  candidate rules enter only as auditions via the API).
- Firing counts are fake and labeled fake. Real source: the event log.
- The 5 git statutes are collapsed into one hydra (×5 noted in panel) —
  decide whether the real app keeps that compression.
- Data debris: ROWTYPES records carry meaningless `promise:` fields from a
  sloppy bulk edit; harmless, clean up on rewrite.

## Open questions
1. Generation pipeline: invariant 1 requires compiling from the executing
   declarations. Rules TOMLs give name/remedy; trigger/reads live partly in
   substrate code (rules.ex hook bindings). Where does the on/reads/emits/
   inhibited-by quadruple come from mechanically — extend the TOML schema,
   or a substrate export verb? (Likely pairs with the wi_ecd8cd9d fold,
   which specs new rails in exactly that quadruple form.)
2. Row-type taxonomy: the 12 circle nodes were chosen by judgment. Should
   they derive from the schema (which tables/kinds qualify as "row types")
   and what is the authority when schema and diagram disagree?
3. Staged/disarmed detection: the one real staged rule is a commented-out
   TOML block — comment-parsing is not detection. Does a staged state need
   to become first-class in the rules format?
4. Server shape: ATC sibling on gibson? Port, feed cadence, and whether it
   mounts into ATC's page or stands alone. Audition + draw API per
   invariants 6/9 (ATC author conventions verbatim).
5. Scar field sourcing (invariant 5): where does "born from: <incident>"
   live durably — rule TOML field, or a specs cross-reference?
6. Scale: layout is proven at 14 hydras. Collision behavior at 30+ rails
   (post-fold world) is untested; the margin may need pagination or
   promise-class filtering.
7. Label richness tier 2: ellipsis-at-~24-chars + tooltip was specced but
   not built (flyouts made it less urgent). Decide if still wanted.
8. UNVERIFIED ON REAL SAFARI as of handoff: the pointer-events fix for
   "hovering another rail doesn't step callouts aside" shipped without a
   confirming eyeball. First task: have Mike click a rail, hover another,
   confirm the notes step aside. If not, the event-swallowing theory is
   wrong — instrument on the real engine.
9. Cosmetic: a top-left callout can graze the subtitle text.
