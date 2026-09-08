# Tightbeam 0.1.9 full-process recovery acceptance

Date: 8 September 2026

Scope: one deterministic, isolated process-boundary acceptance test for the exact 0.1.9 release candidate. This is not a live Gibson fault injection and does not claim a root cause for the observed database timeouts.

## Existing coverage

- `test/ledger_test.exs:91` proves startup recovery changes a claimed running turn to `failed_unknown` once, never requeues it, and permits later queued work to proceed.
- Candidate `test/row_driven_waits_test.exs:571` proves latched dependency recognition survives a Wakes-process restart and deterministic `wakeId` prevents duplicate turn creation.
- `test/escalation_delivery_test.exs`, proofs 4 through 6, proves durable pending wakes drain after DB/Wakes restart, raising or exiting delivery remains pending, and a committed turn with a still-pending wake is deduplicated to one message and turn.
- `scripts/soak.exs` supports SIGTERM/SIGKILL and restart of its own isolated gateway and records unexpected exit.
- `test/readiness_test.exs:113` distinguishes gateway serving/readiness from provider advisories.

These tests prove the component behaviors. None synchronizes a full gateway death with a claimed turn and both sides of the wake delivery commit boundary, then checks recovery and provider classification through ordinary startup.

## Smallest missing executable path

Add one focused integration test using the existing soak gateway launcher and a newly created marked temporary arena. Run only the exact frozen release candidate. Never target the live Gibson base directory, service, port, database, adapters, or credentials.

Before the crash, create and verify these durable states in one isolated database:

1. State A: one claimed `running` turn for a test session, followed by a second queued turn for that session.
2. State B: one due `pending` wake with no committed message or turn.
3. State C: one synthetic wake whose message and turn are committed under its unique `wakeId` while the wake row remains `pending`. Reuse the durable synthetic state from escalation-delivery proof 6 if current APIs cannot pause deterministically between delivery commit and fired marking.
4. Record baseline provider/harness-health rows and readiness output.
5. Record stable identifiers and byte-level values for every pre-crash committed artifact, attest, message, turn, wake, and other effect used by the fixture.

After all preconditions are observed, SIGKILL only the arena gateway. Wait for its process exit. Restart the same frozen candidate against the same arena base directory. Observe recovery through normal application startup, ledger recovery, and scheduler delivery. Do not call `recover_running`, `fire_due`, or direct database repair helpers from the assertion path.

## Required observations

- State A's original turn becomes exactly one `failed_unknown` terminal and is never run again.
- State A's queued successor becomes claimable and is delivered exactly once.
- State B creates exactly one message and one turn carrying its `wakeId`; its wake becomes `fired` only after the supported notification enqueue/publication boundary succeeds. The consumer turn reaching `delivered` is a separate later outcome, and neither state proves that the agent fulfilled the underlying work.
- State C remains exactly one message and one turn and reconciles to `fired` without replay.
- Every pre-crash committed artifact, attest, and effect identifier remains byte-identical and single-count.
- A test external-effect callback, if used, records no duplicate invocation.
- Failed or incomplete wake delivery remains visibly pending; a queued or attempted delivery is never counted as fulfillment.
- Queued work drains through supported recovery without manual database edits.
- The gateway returns to serving and readiness reporting independently of any pre-existing real credential advisory.
- No new provider outage, harness-health failure, shared-outage classification, or credential diagnosis is attributed solely to the gateway crash.

Capture the exact candidate commit and tree, old and new gateway PIDs, exit status, restart/recovery latency, and pre/post rows for all wake IDs, turn sequences/statuses, and effect IDs.

## Boundaries

- Do not add a production fault-injection hook solely for this test.
- Do not run against the live Gibson service or mutate its power state.
- Do not read, copy, or reuse live credentials.
- Do not rerun the completed Surf Ace soak for this test.
- Do not create a new test platform when the isolated soak launcher and existing fixtures suffice.
- Do not claim the test diagnoses or fixes the unresolved cause of the observed database-call timeouts.
- Run this focused test first. Once green and independently reviewed, include it in the final canonical release gate for the exact integrated candidate.

## Lead selection and implementation custody

The external lead read the complete Parallax proposal and selected this bounded acceptance path within the existing release requirement. Source report SHA256 `733f95c78cfed3a44d335f2e6d65e4892ae7c5e3e4ba9b7c114661aae7b2a17b` includes the clarification separating notification publication, consumer-turn delivery and fulfillment. Earlier copied hashes are superseded by this verified content hash.

The existing release coordinator routed the scope in `w_3975b09c`. Reported owner disposition `att_2792af2b` allocates it to the same integrated source/test executor after replay correction. Retain that custody and the actual corrected-source order. The lead selected no new source lane, service action, production fault hook or independent platform. The fixture and its final-candidate results remain to be implemented and verified. Source coverage statements above are attributed to Parallax's bounded inspection, not a new lead test execution.
