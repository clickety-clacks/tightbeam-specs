# Harness recovery Main wake v1

Status: implementation contract for `wi_3bb2ea6c-9cab-4e85-9981-676c4b32c3b6`.

## Spirit

A recovered harness is useful only when the minds that parked work on it learn
that the world changed. Tightbeam must surface that change without deciding
which product agents matter. It gives each affected owner one prompt at Main;
Main uses its installed or learned Kung Fu archetypes to inspect live agents and
resume the right stalled graphs.

## Law

1. The scope is `{ownerUserId, harness}`. It is not global and it is not a list
   of sessions. The owner is copied from the session whose unavailable turn was
   committed. The target is that owner's existing active personal Main.
2. A failed turn opens an episode only when its raw failure is classified as
   `adapter_unavailable`, `harness_unavailable`, `model_unavailable`, or
   `usageLimitExceeded`. The Codex regression evidence uses the captured
   ACP/provider-adapter field
   `data.codexErrorInfo = "usageLimitExceeded"`. Credential onboarding and OAuth
   recovery remain on the credential recovery rail.
3. Adapter startup is not proof of recovery. The first later delivered turn in
   the same scope is the recovery trigger. This is a lagging, use-confirmed
   signal, matching the `quota-recovered` boundary in `wake-on-fact-v1.md`.
4. The terminal transition, episode close, and one due-now blocker-class wake
   commit in one transaction. A repeated success while the episode is closed
   creates nothing. A later unavailable failure opens a new generation.
5. The wake targets Main only. Its prompt names the harness and episode evidence,
   tells Main to inspect relevant live agents through its Kung Fu Main
   archetypes, and requires resumption only for graphs blocked on that harness.
   Tightbeam does not enumerate, wake, or select product agents.
6. If no active owner Main exists, Tightbeam records
   `harness_recovery_wake_undeliverable`, leaves the episode open, and lets a
   later delivered turn retry the same deterministic target. It does not compose
   a turn for a session row that does not exist. The undeliverable evidence
   retains the successful recovery session as well as the recovery turn.
7. Every unavailable observation and recovery carries cause, turn, session,
   scope, and `process:tightbeam` principal in lifecycle evidence. The episode
   table, not lifecycle prose, is the decision state.

## Mechanism

`harness_recovery_episodes` holds one row per owner and harness. An open row
keeps the first and latest unavailable turns. A closed row keeps the successful
turn and recovery wake id. `generation` distinguishes successive outages.

The gateway turn runner passes raw failure terms and delivered-turn observations
to `Tightbeam.HarnessRecovery` through `SessionLane`'s terminal transaction.
`Wakes.schedule_in_txn/2` creates the Main prompt with `dueAt` equal to the
recovery observation clock and class `blocker`; the normal wake scheduler and
turn ledger provide delivery and replay. This mirrors the OAuth recovery
event-prompt boundary while replacing OAuth's captured-session broadcast with a
single product-judgment boundary at Main.

The Codex classifier regression loads
`test/fixtures/harness_recovery/codex-usage-limit-s1.json`. That fixture is a
safe projection of real specimen S1 in archived artifact `art_054cb5af`, whose
content SHA-256 is
`f8ec787572c32922d04a431a713f9634131eeef4e79828728c99930df5b66e88`.
The artifact records that the observed boundary is ACP/provider-adapter output;
it does not claim access to the raw upstream provider HTTP response.

## Acceptance

- Two unavailable turns in one owner+harness scope followed by one delivered
  turn create one closed generation and one pending Main wake.
- Further delivered turns create no additional wake.
- A new unavailable turn after closure opens generation two and permits exactly
  one later recovery wake.
- Success under another owner or another harness does not close the episode.
- An ordinary turn failure does not open an episode.
- The SHA-bound captured Codex S1 projection with
  `data.codexErrorInfo = "usageLimitExceeded"`, adapter-down, and
  model-apply-unavailable shapes classify; OAuth policy refusal and arbitrary
  model errors do not.
- A missing or retired Main receives no wake, produces named durable evidence,
  retains the recovery session and turn in that evidence, and leaves the episode
  open.
- The delivered-turn record action commits before terminal publication; a lost
  or duplicate terminal callback cannot split the episode and wake.
- The prompt explicitly forbids unrelated fan-out and leaves agent selection to
  Main.

## Compatibility and deletion

The table is additive and empty on upgrade. Existing turns and wakes keep their
meaning. No backfill is inferred from lifecycle text. The feature can be deleted
by removing the two turn hooks and schema registration; historical episode and
wake rows remain readable evidence and require no migration.
