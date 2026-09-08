# Composed 0.1.9 canonical Mix verification

The single canonical Mix gate on Racter exited 2. It ran 9 doctests and 1,868 tests, with 2 failures and 11 skips. ExUnit reported 423.4 seconds. This is failed composition verification, not release acceptance.

## Source and execution

- Source: `racter:/home/clu/.tightbeam/work/ff60d70ebb06/integrated-019-dd36d2da`.
- Frozen tree before and after: `48ccadc9a6b9a7e75aa90f1273723ade932f3f46`.
- HEAD before and after: `57bc449c9478ed37170e3fe9981f6fc0fa6cc457`.
- MERGE_HEAD before and after: `926774a30fb79df5c66015b118689b8be45aa350`.
- Full-index binary patch against `b299457d5c95dd6e161ed9b1de70b4450b5166b7`: SHA256 `872f6d0a34143516c1514d26457e7a5171566bf1db28db475df6850fdedaff67` before and after.
- Unmodified `scripts/verify_mix.sh`: SHA256 `5ab75d72ed22d14dfee1eaec298c9b4f750f587d0777f421e7a6ca5ce1437397`.
- Started 2026-09-08 07:15:03 UTC; ended 07:22:23 UTC.
- BEAM PID `3801446`, node `tightbeam_mix_gate_ydHYQfWk`; process absent after terminal result.
- Command used the existing pinned OTP28.5/Elixir1.19.5 toolchain, retained Hex2.5.1, in-repository fixture CLI, command-local CI fixture Git identity, and allocated scratch TMPDIR `/tmp/dd36-mix-48ccadc9.7170V0uA`.
- No installs, dependency updates, Rust reruns, source edits, commits, or target movement.

`source.before` and `source.after` compare byte-for-byte equal. `status.before` and `status.after` compare equal. The final unstaged-diff exit is 0. Source custody can return to the existing composer for correction.

## Failures

1. `Tightbeam.LateRulingHandoffTest`, `dr_07bdef13_survives_revocation_late_ruling_successor_and_consumption`, defined at `test/late_ruling_handoff_test.exs:57`. Replayed receipt assertion at line216 raises `FunctionClauseError` in `Tightbeam.Assignments.attest/1`. Stack names `transaction_with_row_commits/3` at `assignments.ex:2486` and `attest_result/2` at line806. Log lines2707–2716.
2. `Tightbeam.LateRulingHandoffTest`, `receipt boundary is opaque and operational targets are singular`, defined at `test/late_ruling_handoff_test.exs:357`. Receipt replay assertion at line472 raises the same exception through the same transaction wrapper. Log lines2722–2731.

These are observed replay failures in the composed late-ruling/WakeRails path. No cause beyond those stack traces was established by this verification. Separate marker-owner findings reported by other reviewers are not these test failures and are not verified by this gate report.

## Durable evidence

All files are under `racter:/home/clu/.tightbeam/work/ff60d70ebb06/mix-verification-48ccadc9/logs/`:

- `mix.log`, SHA256 `20b6b7043040429fe07d217ad8fc238c41a36415e4fd16bd4d5fa0e2fdc3e18c`.
- `mix.exit`, value `2`.
- `mix.started`, `mix.ended`, `unstaged.after.exit`.
- `command.txt`, exact command and environment declarations, SHA256 `1392e0e91b46922a26547a214398568818347d335bbe6bd4de53c944d9a60403`.
- `source.before` and `source.after`, each SHA256 `347afadd32848353bd26db1db71bd91207154f3cf7b1468603312b4c4727e9f4`.
- `status.before` and `status.after`.

## Verification custody race

The external verifier launched after direct delegated authorization, checking the frozen source, empty reserved logs, and no competing process in the clone. The lead's subsequent HOLD message reporting a previously unknown future internal-verifier intention arrived after launch. The external verifier immediately reported its active handle and retained the single run. The lead then verified coordinator `att_b8de57f1` revoked the competing internal assignment and delivered no-launch direction. Repeated clone-scoped process checks observed only this canonical BEAM. No duplicate run was observed. This start-order race is preserved rather than represented as a pre-launch exclusion guarantee.

No rerun was launched. The existing composer owns source correction and subsequent review; this verifier's gate is terminal.

## Separate bounded semantic review

The lead's independent source helper inspected the same frozen tree read-only. This is a separate finding from the two executed test failures.

Both `operator-ruling-late-routed` at `lib/tightbeam/escalation.ex:1348` and `assignment-successor-created` at `lib/tightbeam/assignments.ex:1173` omit explicit `owner_user_id`. They use `process:tightbeam`, whose owner cannot be derived. `ConditionFacts` stores NULL ownership for these markers. Existing marker-count consumers can see them while tenant-scoped condition waits cannot recognize them.

Inspected boundaries on tree48ccadc9:

- `condition_facts.ex:107-130` stores explicit or derived ownership; its process-origin fallback at233 cannot derive a tenant.
- `rules.ex:2079-2113` requires owner equality for normal predicates. NULL is eligible only for the separate legacy-unscoped path.
- `wakes.ex:1170-1185` excludes ownerless transitions from tenant dependency recognition; legacy condition wakes at4386-4417 use their target session tenant.
- `schema.ex:1735-1794` backfills user/session origin or a direct `decision_requests.rulingFactId` relationship. It does not cover these two marker relationships. Ambiguous provenance remains NULL with a migration event.
- The primary `escalation-ruled` producer at `escalation.ex:1339` explicitly supplies `request.owner_user_id`, and its rule transaction performs row/condition recognition before delivery publication.

This failure is lost recognition, not demonstrated cross-tenant leakage. Preserve strict matching; never turn NULL into a tenant wildcard. Correct the two producers using authoritative owning relationships and cover safely attributable historical markers. Leave unknown or conflicting historical ownership visibly unattributed.

The inspected late-ruling tests122-129 check marker presence, and generic schema tests255-295 check unattributed process rows. Add focused proof that the right tenant recognizes fresh and safely migrated markers; another tenant cannot; ambiguous historical rows remain unrecognized; and ruling replay, successor carry and occurrence counts remain correct. Independent source review must assess the correction and the existing late-ruling/WakeRails transaction conditions.

## Lead handoff and custody

Lead hash-verified the external report as `788fbff5762b180c4015596ee1ea536d791621b6eef20319f93b24d58e1cebb6` and returned the terminal result plus semantic findings directly to sole composer s_76613413 through `w_81ab5f9c-dee4-4bab-a710-b8ffb7e2520c`. The verification freeze is released to that existing source owner. No source edits or second run were performed by the lead or verifier. Existing Rust299/0 remains attributed to the frozen pre-correction tree.

The lead also directly read internal verifier transcript124821: it confirmed no candidate Mix run was started, would ignore stale continuations, and retained r1_disposition_context as the sole external executor. That closes the observed competing-start intent after actual opener revocation, while preserving the earlier race in the report above.

The current composer must correct the real failures, retain exact source and evidence identity, and arrange applicable verification and independent review through the existing release coordinator. The served wrapper conflict remains a property of that holder's instructions; reuse capable external verification for a later frozen correction if required. Do not reopen product permission or modify the canonical runner to resolve it.
