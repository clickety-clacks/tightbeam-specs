# Source evidence — stale-running-turn settlement v1

This supporting artifact binds the candidate to the owned fresh product clone
used for the bounded read. It is evidence only. It changes no product source
and is not a second specification.

## Repository binding

- Remote: `git@github.com:clickety-clacks/tightbeam.git`
- Product checkout: `7a70a2f616363074514237b5bee48ba67c52e2ea`
- Current-main subject: `Correct branch target authority`
- Existing recovery object: `eea3e9a1eb73a63ae41eafa05fb42e410f362ee7`
- Existing recovery subject: `Recover after proven adapter death despite cleanup failure`
- Ancestry result: `git merge-base --is-ancestor eea3e9a1eb73a63ae41eafa05fb42e410f362ee7 7a70a2f616363074514237b5bee48ba67c52e2ea` returned success.
- Product checkout status: clean.

The product clone was fetched as an owned fresh clone. The candidate does not
claim that `eea3e9a` implements stale-turn settlement. It claims only that the
new operator verb is additive to the recovery and terminal seams already
present at the pinned current-main descendant.

## Reproducible commands

From the product checkout:

```text
git rev-parse HEAD
7a70a2f616363074514237b5bee48ba67c52e2ea

git rev-parse eea3e9a
eea3e9a1eb73a63ae41eafa05fb42e410f362ee7

git merge-base --is-ancestor eea3e9a HEAD
exit 0

git show --no-patch --format='eea3e9a=%H%nsubject=%s%nparent=%P' eea3e9a
eea3e9a=eea3e9a1eb73a63ae41eafa05fb42e410f362ee7
subject=Recover after proven adapter death despite cleanup failure
parent=63e3400eeddc3b118de5131efb4d251f4c10cab2

git show --no-patch --format='main=%H%nsubject=%s' HEAD
main=7a70a2f616363074514237b5bee48ba67c52e2ea
subject=Correct branch target authority

git status --short
<empty>
```

## Load-bearing source anchors

At the pinned checkout, the existing seams cited by the candidate resolve as
follows:

- `lib/tightbeam/session_lane.ex`: `nudge/1` at line 58; `cancel_current/2`
  at line 82; the lane-owned cancel handler at lines 136–154; the lane task
  claim and drain path in `claim_and_start/1`.
- `lib/tightbeam/ledger.ex`: `finish/5` at line 434; `finish_in_txn/5` at
  line 452; `recover_running/1` at line 522; `pending_sessions/1` at line
  560; `unpublished_terminals/1` at line 665; the existing terminal event
  builder at line 750.
- `lib/tightbeam/turn_lifecycle.ex`: terminal authority validation begins at
  line 390 and requires a durable cause and principal; the terminal event
  schema and `terminal_committed` kind are declared at lines 19–58.
- `lib/tightbeam/lane_manager.ex`: boot recovery is called at line 67;
  unpublished terminal reconciliation is at lines 96–100; pending-session
  lane reconciliation is at lines 102–104.
- `lib/tightbeam/gateway.ex`: the existing `cancel` handler is registered at
  line 1118 and `cancel_result/2` begins at line 2778.
- `lib/tightbeam/wire/router.ex`: the closed agent verb set is declared at
  line 57 and the existing `cancel_current_run` mapping is at line 843.
- `lib/tightbeam/idempotency.ex`: the existing durable `wire_idempotency`
  ledger is declared at lines 22–30 and read/write seams are at lines 36–104.
  Its operation vocabulary is currently closed; the candidate explicitly
  requires an additive `settle-turn` operation plus request-fingerprint and
  canonical-response fields.

These anchors establish the source lineage claimed in
`stale-running-turn-settlement-v1.md`; they do not authorize implementation in
this spec-only lane.
