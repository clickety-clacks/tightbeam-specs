# Surf Ace: fleet-unique window labels are a core requirement

Ruled by Mike, 2026-09-03.

**This requirement was always explicit in the specification.** It is stated in
section 15.1 of the original Surf Ace spec, quoted verbatim below. It was never
implicit, never merely spoken, never a gap in the documentation. Any account of
this failure that says otherwise is wrong, including earlier revisions of this
document.

What actually happened: agents rewrote the architecture, wrote a new DESIGN.md
clause that contradicted section 15.1, and no review checked the new design
against the original requirement. The reviews passed because they compared the
code to the newer contradicting text. The requirement was superseded without
authorization by anyone entitled to supersede it.

## The requirement

Original Surf Ace specification, commit `236a999`, section 15.1, verbatim:

> Each window is assigned a short alphabetic identifier using an
> auto-incrementing sequence: `A`, `B`, `C` … `Z`, `AA`, `AB`, …

> The window label is the primary addressing handle. It MUST be visible at all
> times so that a user can tell CLU "move content to window B" without
> ambiguity.

## Why those two sentences force a single allocator

An auto-incrementing sequence is one counter. N clients each running their own
counter are N sequences. N sequences over one symbol set produce duplicate
labels. Duplicate labels make "move content to window B" ambiguous, which 15.1
forbids. Therefore exactly one authority must own the label space.

This is what the words mean. It is not an inference about intent.

## Current state: the requirement is not met

Verified in source on `main`:

- `packages/electron/src/surface-core.ts` builds `usedWindowLabels` from
  `this.listSurfaces()`, which is that client's own surfaces and nothing else,
  then takes the lowest free letter.
- `allocatePaneIdentity` in `lockless-client-authority.ts` does the same for
  pane numbers, starting at 1.

So eezo hands out `a` and pane 1, and shrdlu hands out `a` and pane 1. The live
fleet currently has multiple panes labelled 1. A user looking at two screens
cannot direct content at either one.

## How it was lost

The OpenClaw provider satisfied this invariant implicitly. Exactly one process
held the surface map and the label counter for every client it managed. See
`packages/extension/dist/openclaw-package/extension/src/surf-ace-runtime.ts`,
which builds `usedWindowLabels` from `this.surfaces` across all managed clients
and persists both `windowLabels` and `nextWindowLabelIndex`.

The CLI rewrite removed that process and did not replace the allocator.
Allocation became client-local. DESIGN.md was then amended to state that pane
labels are "not globally unique", directly contradicting section 15.1, which
was still in the repository and still said the opposite.

This is the core failure. The requirement was written down. It was available to
every agent that touched this. Instead of being checked against, it was
overwritten by a clause describing what the new code happened to do, and every
later review validated the code against that newer clause. No test asserted the
requirement, so every subsequent soak passed.

The clause is now deleted. DESIGN.md at `edc747d` carries the invariant
explicitly.

## Rejected alternatives

Do not propose these. Each was raised and ruled out.

1. **"The spec says client-local authority."** It said that because someone
   wrote down what the broken code does. Corrected at `edc747d`. The original
   specification is the source of the requirement.
2. **"Pane labels are unique within a surface, which is enough."** The
   user-facing token is `windowLabel + paneLabel`. If the letter is not
   fleet-unique, the pair is not either.
3. **"Host-qualify the token, `shrdlu b1`."** Rejected. The token is spoken
   aloud, including through a voice interface, where a hostname is far more
   error-prone than a single letter. It also violates "short alphabetic
   identifier".
4. **"Mint random identifiers, like `sf_` surface IDs."** Useless here. You
   cannot randomly mint `a` from 26 symbols and have it be the only `a`, and a
   UUID cannot be said out loud.
5. **"Take a provisional label and reconcile later."** Forbidden. A
   possibly-duplicate label is worse than no label: the user directs content at
   it and it lands on the wrong screen in another room.
6. **"Per-client uniqueness plus conversational context."** No. Someone looking
   at two screens that both show B cannot say which one they mean.
7. **"Bonjour discovery is enough."** Discovery gives presence, not consensus.
   Two clients that cannot see each other will both conclude `a` is free.

## What must be built

1. **One fleet-wide label allocator.** It owns the sequence and the
   surfaceId-to-label map, and persists across client restarts so a window keeps
   its label. A small resident sidecar is the known-sufficient shape and is
   effectively what OpenClaw was. Leader election among clients is permissible
   only with a proof of no split-brain, because split-brain here means two `a`s,
   which is the exact prohibited outcome.
2. **Clients display no label when they cannot obtain one**, and are not
   addressable until they can. Unaddressable is acceptable. Wrong is not.
3. **A test that fails when two clients can produce the same window label.**
   Mandatory. Its absence is why weeks of green soaks ran over a broken core
   requirement.
4. **Pane numbers stay per-window, lowest-free.** They need no change once the
   window letter is fleet-unique.

## Status

Not met. Surf Ace cannot ship until it is.
