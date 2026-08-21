# Grammaton (rails visualization) — initial invariants

Status: recorded 2026-08-21 from the working session with Mike; not scheduled.
Named Grammaton (Mike, 2026-08-21); "hydra" names one rail's drawn shape only.
Spikes: eezo:~/rails-spike.html (3D, rejected), serenity:~/grammaton.html
(2D circle+hydra, accepted as the base). Work item: see wi reference below.

## What it is
A viewer (later: an app with a server) that renders the org's rails — the
deterministic laws — as relationships over row types, generated from the same
declarations the substrate executes.

## Invariants (ruled during the session)

1. TRUTH FROM DECLARATIONS. The diagram renders only what is installed:
   armed rules solid, installed-but-disarmed (staged) rules long-dashed.
   Spec documents never render. Generated, never hand-drawn — it cannot
   drift from reality because it compiles from the executing declarations.
2. A RAIL IS A TYPED TRIGGER. Declaration form: on <row event> / reads
   <rows,fields> / emits <rows> | vetoes <the triggering row> /
   inhibited-by <who may override>. The spec for every new rail states this
   quadruple; the viewer draws from it.
3. FORM: row types on a circle; ONE rail = ONE hydra — origins converge to
   a single hub, heads fan out. Veto = the curve returns to the triggering
   row type ending in ⊘. One hover/click unit per rail.
4. LINE LANGUAGE: solid = trigger; sparse dots = read (visually far from
   any dash); long dash = disarmed; arrowhead = creates.
5. MEANING AXES: color = the promise class (proof / attention / economy /
   safety — the failure the rail exists to prevent). Information
   architecture: plain-English sentence is the headline; machine name and
   mechanics are fine print. Optional recorded layer: the scar — the
   incident that birthed the rail; a rail with no scar and no firings
   deserves suspicion.
6. AUDITION (future, server mode): an agent may submit a candidate rule
   declaration to RENDER on the diagram without installing it — a third
   visual state, distinct from armed and staged, ephemeral, attributed to
   its author, and unmistakably non-authoritative. Audition is how "what
   would this law look like here" gets answered without touching the
   ruleset. Auditions never persist into the installed tree by the viewer;
   promotion goes through the normal identity/rules path.
7. LIVE OVERLAY (future): firing counts and last-refusal specimens from the
   event log; sampled or fake data must be labeled as such on the surface.
8. REJECTED: the 3D layered form (spike 1) — failed first-glance
   legibility; altitude-as-layer did not self-explain. Do not revisit
   without new evidence.

9. REST INTERFACE FOR DRAWING (future, server mode): external agents can
   draw on the diagram over a small HTTP API — submit a rail declaration
   (the on/reads/emits/inhibited-by quadruple) and it renders as an
   audition; list, update, and remove their own auditions. The ATC
   conventions apply verbatim: every call carries an `author`, which
   renders on the drawn rail and scopes cleanup (an agent removes only its
   own work; unqualified clear-all is refused); reads before writes; the
   API is the authority on itself via a /help endpoint shipped with the
   server. Drawing is presentation only — nothing submitted through this
   interface touches the installed ruleset, ever.

10. LINE LABELS — label what a reader would grep for; hidden at rest,
    shown only on an isolated hydra, always duplicated in the panel:
    - trigger: the event qualifier ("on: filed", "on: horizon passed"),
      not the row name — the endpoint already shows that;
    - read: the predicate ("effectKind ∈ {code,policy,release,
      live_mutation}", "verdict = reviewed-clean") — a read without its
      condition is meaningless, and the predicate is where the rule's
      logic lives;
    - create: what is minted and for whom ("prod (rung 2)",
      "DR → principal");
    - veto: the exact refusal string the victim sees
      ("rule_denied: completion-requires-review") — so an agent can grep
      the diagram by the error it just received and land on the line
      that fired it.
