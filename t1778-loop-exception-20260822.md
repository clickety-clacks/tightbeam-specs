# T1778 governing exception — continuous loop until first green soak

Ruled by Mike 2026-08-22 (~11:05 PT), mediated through his external session.
Governing for T1778 ONLY, until the FIRST GREEN SOAK, then expires.

## The exception
- ONE standing operator runs install → preflight → soak as a continuous
  loop. No per-stage card churn; the seat persists across stages.
- The operator makes ONLY reversible, mechanical, TEST-FIXTURE fixes in
  place as it hits them (tool paths, assertions, launch mechanics, fixture
  state). Boundaries, absolute: no production behavior changes, no
  deployments, no scope expansion. Product-SOURCE fixes (e.g. the CLI
  migrationMaterial V3) are NOT covered — they exit to the normal
  independent-review path, then re-enter the loop.
- Every in-place fix is ledgered as it lands: file, diff hash, one-line
  reason. Independent review of the ACCUMULATED fixes happens ONCE, as a
  batch, immediately after the first green soak. Review is deferred, not
  waived.

## Explicitly NOT decided here
Which fleet/runbook definition governs (SA-20260811-001 rev 25's
Shrdlu/Racter/EEZO/Aleph fleet with TARS/Gibson excluded, versus the
current chain's configuration) remains UNRESOLVED. This approval does not
decide it. The loop proceeds on the current chain's configuration; the
admissibility of its evidence against the official soak may be limited by
the later fleet ruling. That ruling is owed separately by the Surf Ace
owner with Mike.
