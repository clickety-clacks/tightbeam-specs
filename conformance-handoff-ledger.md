# Conformance HANDOFF ledger — honest gaps surviving lane merges

Entries move here from lane HANDOFF.md files at merge time. Cross-lane entries that
dissolve at integration get struck with a note; spec-blocked entries await Flynn
adjudication (checklist item 7c).


## Lane: fix-spinup (merged 6bc71e6)

# Spinup conformance handoffs

## Clause 3 — org CLI detect/ensure/deploy

Blocker: the ruling `spinup-detection-v1.md` requires Spinup to ensure the org CLI, but `session-tokens-v1.md` §Rollout says “Spinup does not deploy the CLI; assimilate's CLI step is the only delivery path,” and `probe-v1.md` §Rollout repeats that Spinup never refreshes the shipped CLI. The Spinup spec also limits host data to SSH/base-directory addressing and does not define the CLI source artifact, destination path, target-triple compatibility rule, local-host behavior, or deployment command. Implementing any choice in `lib/tightbeam/spinup.ex` would invent behavior across a binding spec conflict.

Required change: reconcile the three specs and define one owner for CLI delivery. If Spinup remains the owner, amend the governing spec with the source artifact, remote and local destination paths, target-triple policy, presence/post-deploy checks, exact deployment action, and lifecycle detail, then authorize the corresponding full present/missing/failure/post-check matrix in `test/spinup_test.exs`. If assimilate remains the only owner, remove the org-CLI requirement from spinup clause 3.

## Clause 13 — proof for failure-specific denial remedies

Blocker: production remedy selection is implemented in the lane-owned `lib/tightbeam/spinup.ex`, including a real `:enotdir` correction (“remove or rename the non-directory component”) and a corrective adapter post-check action (“reinstall”). The required proof file `test/spinup_test.exs` is outside this lane's explicit ownership boundary. Its current local-directory test still asserts only the verifier-rejected generic permissions substring, and its post-deploy test still asserts only the verifier-rejected diagnostic substring, so neither can honestly prove the corrected implementation under the anti-stub contract.

Required cross-lane change: authorize the test-owning lane to replace those weak assertions with exact failure-specific messages and observable remedy proof. For the local `:enotdir` case, create the conflicting file, assert the remove/rename remedy exactly, apply that remedy, rerun readiness, and assert the work path becomes a directory. For the adapter post-deploy case, assert the reinstall-and-executable-path correction exactly. Retain exact assertions for remote permission denial, npm-not-found, connection-refused, local-adapter-missing, and credential-missing so the complete denial-branch matrix fails if any remedy selector or corrective message is removed.


## Lane: fix-core-containment (merged ae17512)

# core-containment cross-lane handoffs

- **C3, C6, C17, C67, C78, C79, C82, C106, C109, C113, C128, C132, and C138 — shipped `contain-exec` reachability.** `cli/src/contain.rs` now contains the custody engine and its real tests, but this lane does not own `cli/src/main.rs`; the shipped binary still sends `contain-exec` through the ordinary parser. The CLI-routing lane must add a raw `argv[1] == "contain-exec"` branch before `args::parse`, call `contain::contain_exec(&args[2..])`, and exit with that returned status. It must keep HELP, `args.rs`, and `dispatch.rs` unchanged and add release-binary acceptance proving `tightbeam contain-exec --check` succeeds on Darwin. C3 additionally needs an actual adapter/descendant launch through Placement and this shipped route.

- **C131 — shipped-wrapper Darwin kernel acceptance.** The existing non-owned `test/containment_test.exs` test invokes `/usr/bin/sandbox-exec` directly. After the raw route above lands, the containment-test lane must invoke the built/installed `tightbeam contain-exec --profile ... -- /bin/sh -c ...` and assert all five observable outcomes: allowed inside write, denied outside write, stdout passthrough, denied symlink escape, and allowed home-symlink-to-auth write.

- **C77, C112, and C126 — uncontained load mode reassertion.** This lane does not own `lib/tightbeam/acp/adapter.ex` or `test/acp_adapter_test.exs`. That lane must make successful uncontained `session/load` issue the same best-effort preset `session/set_mode` request as uncontained `session/new`, retain success-required behavior when contained, and test both success and ignored failure on real fake-connection request state.

- **Containment conformance fixture following C45/C119.** `test/conformance_test.exs` is not owned here. Its Darwin temporary base must be canonicalized before building the rail scratch root; stock `/var` is a symlink to `/private/var`, and `Containment.profile/1` now correctly refuses that unresolved component.

- **C139 — production-cwd credentialed spike.** This is manual evidence outside the owned files. Re-run the credentialed harness-under-wall spike without setting adapter OS cwd to the session workdir and record the result in `/Users/mike/src/shared-workspace/shared/specs/tightbeam/containment-spike-report.md`.

- **G10 — remove prohibited static version probing.** `Placement.harness_binary_probe/3` cannot be removed in isolation because non-owned `lib/tightbeam/gateway.ex` and `lib/mix/tasks/tightbeam.doctor.ex` still call it. Their owning lane must remove/replace both callers with the live wiring-check contract; then `harness_binary_probe/3` and its test can be deleted without breaking compilation.

- **G11 and G68 — `CODEX_CONFIG` as the sole trust lever and byte-identical lawless boot.** Placement no longer exports `CODEX_PATH`, but non-owned `lib/tightbeam/gateway.ex` still unconditionally creates `bin/codex` with the rejected `--dangerously-bypass-hook-trust` flag. The Gateway lane must remove that shim/artifact generation and add a fresh-default Gateway test proving a lawless Codex boot creates no gate-era artifact or adapter-env delta.

- **G40 — one regeneration plus visible context reset.** The required end-to-end proof belongs to non-owned Gateway/Homes lifecycle tests. Add a first-statute-deploy test that begins with a real projected Codex home/session, changes statute bytes, observes exactly one regeneration, and asserts the resulting substrate context-reset marker.

- **G48 — single source for the Codex fallback and probe model.** Non-owned `lib/tightbeam/gateway.ex` currently resolves modelless Codex through `config.default_model`, while Placement has the required `gpt-5.6-sol[medium]` literal. The Gateway lane must expose/use one Codex fallback source at spawn resolution; Placement must then consume that same source, with a relationship test that fails if either value drifts.

- **G70 and G77 — independent Claude pre-change byte golden.** The implementation preserves the Claude projection, but this lane is forbidden to edit non-owned `test/placement_test.exs`. Replace the self-derived `JSON.encode!(Map.merge(Rails.hook_settings(), ...))` oracle with a fixed literal or fixture captured from canonical pre-codex-gates behavior, and assert the real generated `settings.json` bytes equal it and contain no probe entry.


## Lanes: fix-core-supervision + fix-wake-on-fact (merged 9dc2c68)

# Core-supervision conformance handoff

This file records every clause that the independent verifier classified
`STILL-OPEN`. None is claimed closed. The four verifier-approved
`CLOSED-REAL` clauses remain implemented and unchanged:

- Supervision 31.
- Escalation 13.
- Escalation 54.
- Escalation 120.

## Authoritative spec conflicts

### Supervision 5, 12, 15, 22, 33, 42, 50, 60, 74, 75, 86, 89, 107, 119, 122, 123, 125, 129; Escalation 21 and 122

**Exact blocker:** `supervision-impl-v1.md` r20 says it is the sole authority for
the build lane and requires pending-wake suppression before the canonical claim,
watermark movement only on a canonical claim, an exact public result-tag set, no
statute-expressed supervision policy, no check-tier completion gate, no
assignment mutation, no `rail_sweep` lifecycle kind, and substrate acts limited
to wakes/stamps. The ratified `escalation-substrate-v1.md` r7 and its named
parent `rails-mechanism-v1.md` require the already-shipped turn-end order and
effects: adjudication hold, `Rules.decide/2`, remedy close/fire, escalation
open/park, and rail lifecycle emission before the generic target-keyed pending
wake check. Existing conformance and unit tests assert the latter behavior.
Choosing either side in `lib/tightbeam/supervision.ex` would silently violate the
other governing spec.

**Required change:** Flynn/spec authority must amend the specs to select one
ordering and ownership model. If supervision r20 wins, the rails/escalation
specs and their conformance fixtures must remove the turn-end rail fold, and the
supervision implementation must remove `Adjudication`, `Rules`, `RailRemedy`,
turn-end `Escalation`, `rail_sweep`, noncanonical watermark writes, and the
extra public outcomes. If the rails/escalation model wins, supervision r20 and
the listed supervision clauses/acceptance contract must be amended with a new
termination proof and exact public contract. The owning test lane must then add
the full real-state matrix for the selected behavior.

### Supervision 29

**Exact blocker:** supervision r20 makes `notify_retired` doorbell-only, while
ratified escalation r7 §8 explicitly requires the same handler to call
`Escalation.withdraw_for_retired/2`. Removing that call closes Supervision 29
but violates escalation's retirement fast path; keeping it does the reverse.

**Required change:** an authoritative spec amendment must either move
retirement withdrawal to another durable/fast-path owner or explicitly permit
it in supervision's retirement handler. The selected path then needs a
real-state retirement test in the owning test lane. Supervision 31's existing
total catch must remain around the whole selected handler.

### Accountability 82

**Exact blocker:** the accountability constitution requires a strand to notify
the first living ancestor/root through wake-to-user, while supervision r20 step
7 says waking anyone about a retired holder is an operator judgment and limits
the optional doorbell to a stamp/lifecycle row.

**Required change:** the two specs must receive an authority ruling. If
notification is required, the owner-delivery lane must expose the existing
wake-to-user capability to the selected owner and define whether the recipient
is `ladder_target/3` or the org owner/root, then a real retired-holder matrix
must assert the actual delivered prompt. If supervision r20 wins,
Accountability 82 must be amended or removed.

## Owned behavior blocked by the test-file boundary

The lane owns only `lib/tightbeam/supervision.ex` and
`lib/tightbeam/escalation.ex`; the task expressly forbids editing the test files.
The anti-stub contract also forbids claiming implementation-only closure.

### Supervision 10 and 59

**Exact blocker:** the implementation still writes
`lastEvaluatedTerminal` for a retired holder, and
`test/supervision_test.exs` currently asserts that forbidden write. Correcting
the implementation alone makes the required test gate fail, while this lane
cannot change that test.

**Required change:** the test-owning lane must replace the contrary oracle with
a real retired-holder terminal and recovery-sweep matrix asserting no wake,
claim, counter, or watermark movement. Then remove the retired-branch
`write_watermark/3` call in `lib/tightbeam/supervision.ex`.

### Supervision 57

**Exact blocker:** the implementation already uses
`Assignments.list(%{state: "open"})`, deduplicates holder keys, unions pending
outbox sessions, and evaluates the union. The verifier found no regression test
that fails if this is reverted to raw assignment SQL. A normal end-state test
cannot distinguish two query mechanisms that intentionally return the same
rows, and this lane may not add a test seam or edit tests.

**Required change:** the spec/test owner must either authorize an observable
dependency seam that a test can exercise (for example, an injected candidate
enumerator used only through the public `Assignments.list` contract), or accept
source-level dependency inspection as the oracle for this implementation-mechanic
clause. Then add the corresponding non-stub test outside this lane.

### Supervision 135

**Exact blocker:** the N=0 fixture does not assert every session ledger and every
watermark outbox is quiescent.

**Required change:** extend `test/supervision_test.exs` to drive the real
cross-assignment reaction to rest and assert zero pending ledger/wake rows for
every session and `pendingBranch IS NULL` for every watermark.

### Supervision 136

**Exact blocker:** the past-sink fixture stops with a pending escalation.

**Required change:** extend the fixture through delivery and terminal handling
until real quiescence, then assert every ledger, wake, and outbox end-state.

### Supervision 137

**Exact blocker:** the suppressed/reclaimed fixture stops after scheduling one
wake.

**Required change:** deliver the reclaimed chain to rest and assert complete
ledger/wake/outbox quiescence.

### Supervision 138

**Exact blocker:** only pure `ladder_target/3` resolution is covered.

**Required change:** add a real H→S→H delivery/terminal cascade that reaches Main
and quiesces with no pending ledger, wake, or outbox state.

### Supervision 139

**Exact blocker:** no restart-gap test drops a published terminal cast while
Supervision is down and proves both recovery legs.

**Required change:** add a real supervised restart fixture that simultaneously
proves closed-assignment pending-outbox drain and open-holder predicate replay.

### Supervision 140

**Exact blocker:** no successful-dispatch/lost-clear crash fixture exists.

**Required change:** add a controlled post-dispatch/pre-clear failure seam and
assert duplicate redispatch occurs while `prodCount` advances exactly once.

### Supervision 141

**Exact blocker:** no test counts automatic recovery sweeps across boot and
forced restart.

**Required change:** add an authorized sweep-observation seam and assert exactly
one recovery sweep for each server start, including restart.

### Supervision 143

**Exact blocker:** no pending-outbox replay test changes `prod_limit`.

**Required change:** claim under old N, retain the real pending outbox, restart
under a new N, drain it, and assert the delivered prompt contains the frozen old
N and k/rung.

### Supervision 146

**Exact blocker:** the existing derived-stranded test proves only the open
retired-holder leg.

**Required change:** extend `test/work_state_test.exs` to close the assignment
and assert the same query no longer returns `stranded`.

### Supervision 149

**Exact blocker:** no non-Main contiguous holder reply-chain test proves the
N+1 wake bound.

**Required change:** run a real holder through N prods and the one off-holder
escalation with no fresh external input, assert at most N+1 contiguous wakes,
and do not assert N+1 as a per-assignment total.

### Supervision 151

**Exact blocker:** no two-assignment/repeat/dropped-`notify_retired` matrix
exists, and the required no-watermark oracle also conflicts with the existing
retired-holder test and the escalation retirement-withdrawal spec.

**Required change:** after the Supervision 29 authority ruling, add a
two-assignment retired-holder fixture asserting doorbell stamp dedupe, zero
wakes/claims/watermarks, repeat silence, and unchanged derived-stranded truth
when the cast is dropped.

### Supervision 152

**Exact blocker:** no pending-outbox fixture contrasts the two retirement
branches.

**Required change:** add real pending entries proving an escalation re-resolves
past a retired rung and dispatches to a live target while a prod to a retired
holder clears with no dispatch or counter movement.

### Supervision 153

**Exact blocker:** current tests cover a synthetic transient error and an exit,
not a raising handler plus both exit and throw total-catch branches.

**Required change:** add three real handler fixtures: raise must leave the
outbox pending and emit `supervision_dispatch_failed`; exit and throw must emit
`supervision_evaluate_failed` while the server survives.

### Supervision 156

**Exact blocker:** the code contains `strandedAt`, the four pending fields, and a
four-field clear, but schema acceptance does not exercise all of them.

**Required change:** extend schema tests to assert the `strandedAt` column and
run a real pending entry through clear, asserting all four pending fields become
NULL.

### Supervision 157

**Exact blocker:** later-evaluation transient retry is covered, but
`request_sweep` retry is not.

**Required change:** create a real pending transient outbox, restore the
handler, call `request_sweep`, and assert dispatch, one counter advance, and a
cleared outbox.

### Supervision 158

**Exact blocker:** the denial acceptance matrix is incomplete.

**Required change:** add real-state cases for delivered-after-denials resetting
the streak, a fully denied assignment retrying branch 1 forever, and duplicate
evaluation of the same terminal producing no extra denial/count/write.

### Supervision 159

**Exact blocker:** the pause/reset/oldest-selection matrix is incomplete.

**Required change:** add real-state cases for resume after the continuation wake
fires, a progress-only turn drawing prod 1, completion and surrender returning
idle, and selection of the oldest of two open assignments.

### Supervision 160

**Exact blocker:** the ladder acceptance matrix omits named branches.

**Required change:** add all required real-state cases: escalation after N
delivered prods, `stalledAt` set once, two-deep active lineage, nil-spawner Main
fallback, retired-rung skip, cycle handling, and exhausted-chain Main fallback.

### Supervision 162

**Exact blocker:** branch-level dedupe exists, but the required interleavings do
not.

**Required change:** add the exact lost-T1/newer-T2 `:coalesced` fixture and the
revoked-A1→oldest-A2 shift fixture, asserting zero action on the stale terminal.

### Supervision 164

**Exact blocker:** only the canceled-pause sweep case is covered.

**Required change:** add the full real sweep matrix: lost cast, nil-terminal
pending drain, already-claimed duplicate, canceled pause, pre-assignment
terminal, and never-terminal skip.

### Supervision 165

**Exact blocker:** row/query APIs lack a mixed fixture.

**Required change:** test `prod_state/2`, `watermark/2`,
`Ledger.pending_count/2`, `Ledger.last_terminal_seq/2`,
`Wakes.pending_count/2`, `Assignments.oldest_open/2`, and
`Assignments.attest_count/2` over mixed pending, terminal, claimed, and
unclaimed real rows.

### Supervision 168

**Exact blocker:** no single integration test covers the specified complete
timeline.

**Required change:** add the exact prod1→prod2→pause→prod3→escalation1→
escalation2→progress-reset→completion run and assert every wake, counter,
watermark, stamp, and lifecycle/event row at each transition.

## Escalation cross-lane implementation handoffs

### Escalation 6, 61, 105

**Exact blocker:** `rules.ex`/`dispatch.ex` do not carry the owner-delivery
capability into `Escalation.escalate/4`, and `Gateway.escalation_context/3` is
unused and resolves a personal session directly instead of using the existing
owner-user delivery seam.

**Required change:** the Rules/Dispatch/Gateway lane must supply a post-commit
owner-user delivery callback routed by `ownerUserId`, use the existing
wake-to-user path, and add an end-to-end halt/open/one-owner-delivery/pending
test.

### Escalation 8, 18, 44, 45, 47, 49, 78, 106, 111, 112

**Exact blocker:** no shipped live-agent caller/guidance implements the mandatory
session-raiser park protocol.

**Required change:** the live-agent/guidance lane must schedule the exact
self-created `escalation-ruled/<id>` wake before turn end, schedule-then-check
and cancel/act if already resolved, recheck/re-subscribe on every finite
fallback while open, and cancel/recheck on withdrawal. Add end-to-end real
agent tests for ruled-before/after schedule, two fallback iterations, and
withdrawal.

### Escalation 20, 48, 111, and the schedule-then-check portion of 122

**Exact blocker:** `park_escalation/3` must cancel a just-scheduled wake inside
its open transaction, but `lib/tightbeam/wakes.ex` exposes no transaction-scoped
cancellation operation; that file is outside this lane.

**Required change:** the Wakes lane must add the existing pending→canceled CAS
and lifecycle write for `DB.Txn`. Then `park_escalation/3` can schedule, re-read
`decision_requests.status`, cancel and act immediately for
`ruled|consumed|withdrawn`, with ruled-before/after race tests.

### Escalation 42 and 63

**Exact blocker:** r7 requires a separate thin `decision_request_event` doorbell
grain but does not define its DDL, sequence/cursor, writer API, retention, or
owner-surface consumer. A lifecycle row is explicitly insufficient.

**Required change:** the observability/spec owner must define the exact doorbell
schema and query/emission seam. Then the owning engine/wire/test lanes must emit
one doorbell on open and every resolve edge and prove owner queue observation
without using lifecycle rows as a substitute.

### Escalation 53

**Exact blocker:** direct engine option validation is implemented, but
`lib/tightbeam/rules.ex` cannot author or carry `options`; that file is outside
the lane.

**Required change:** the Rules lane must accept and validate
`[{label, effect}]` with `effect ∈ allow|deny`, carry it into escalation ctx,
and add real rule-load/decision tests for every option branch.

### Escalation 65

**Exact blocker:** `Escalation.list/4` and `get/4` are read-only, but the shared
Dispatch success path appends a `"verb"` event for the read verbs.

**Required change:** the Dispatch/Gateway lane must route
`decision-requests`/`decision-request` through a read-only dispatch outcome that
preserves authorization while appending no success event; tests must assert
event counts do not change.

### Escalation 66, 123, 124

**Exact blocker:** Gateway passes `owner_user_id` for same-owner agent/session
raisers, making owner scope indistinguishable from raiser scope inside
`Escalation.visibility/2`. Fixing only `escalation.ex` would either retain the
leak or wrongly remove admin-agent access.

**Required change:** Gateway must pass owner scope only when the existing
owner/admin axis authorizes it; otherwise call without owner scope so exact
canonical `raiserId` filtering applies. Add same-owner agent/session list/get
isolation tests plus authorized owner/admin coverage.

### Escalation 96

**Exact blocker:** r7 says deadline config is threaded through Escalation's child
spec, but `Escalation` is an effect-only module with no specified process state,
and `application.ex`/Gateway child wiring are outside this lane.

**Required change:** the spec owner must define whether Escalation becomes a
configured child or the child-spec sentence is removed in favor of the already
specified Application-env read. If a child is required, the Application/Gateway
lane must start it and thread `escalation_decision_deadline_ms`, with boot/default/
override tests.

### Escalation 102

**Exact blocker:** CLI files and CLI tests are outside this lane.

**Required change:** the CLI lane must add positive argument/help tests for
`revoke-waiver`, `withdraw`, `decision-requests`, and `decision-request`.



## Lane: fix-catalog (merged c2e085d)

# Catalog lane handoffs

- Clauses #1 and #2 — `lib/tightbeam/model_catalog.ex` now rejects a Claude row whose required `max_input_tokens` is missing, `null`, or non-integer and a Codex row whose required `supported_reasoning_levels` is missing, `null`, or non-list, so those payloads cannot become fresh partial truth. Full clause closure still requires `lib/tightbeam/gateway.ex` to stop collapsing `session_status` inventory entries and instead publish every derived entry with its effort-qualified `ref`, `display_name`, `efforts`, `max_input_tokens`, and `capabilities`. The gateway-owned projection and its tests must be changed in the gateway lane.
- Clause #57 — the violating caller is `Tightbeam.Gateway.harness_for_ref/1` in `lib/tightbeam/gateway.ex`, not `lib/tightbeam/adjudication.ex`. The gateway lane must retain `ModelCatalog.member?/3` health and emit `model_unavailable` only for `present?: false, health: :fresh`; stale and unavailable catalog health must propagate as catalog-health failures. Add real stale and unavailable adjudication swap/respawn tests in `test/gateway_test.exs`.
- Clause #63 — the owned `ModelCatalog` portion remains closed-real: no effort rank or tier sorting is present. Overall closure requires the gateway lane to remove base-ref grouping from `session_status` and bare-ref effort fallback selection from tune, then update the corresponding real gateway tests.
- Clause #71 — the test-owning gateway lane must exercise actual gateway startup and the actual `"inspect"`/`list` handler for all four specified degradation cases: missing Claude token, failed Claude fetch, malformed Claude JSON, and missing Codex cache. Each case must assert no process crash and empty-or-last-known catalog output.
- Clause #72 — the test-owning gateway lane must hang a real Claude refresh task, concurrently invoke the actual `"inspect"`/`list` handler, and assert it promptly returns cached or empty models. `Gateway.org_options/0` is not sufficient proof.
- Clause #79 — required pre-merge review proof cannot be produced by either owned implementation file. The integration owner must dispatch the spec-required distinct reviewer, record reviewer identity/model and ordering before merge, and attach that evidence to the integration/ticket record.


## Lane: fix-artifacts (merged b9fb927)

# Artifacts redo handoffs

- **Clause 4 — exact archived file `home`:** `Tightbeam.Artifacts` now maps and
  verifies an artifact's real path inside a reachable local workspace, but
  `lib/tightbeam/gateway.ex` still passes `nil` for remote workspaces. The Gateway
  / remote-workspace owner must execute archival where the workspace is reachable
  and return the resulting archive path; its integration test must assert the exact
  archived file bytes and `home`.

- **Clause 7 — no-policy/ticket-ID floor:** the spec says both that every closing
  workspace is archived and tied to a work item without recording discipline, and
  that a workspace with no `in-workspace` artifact rows is removed. A spec ruling
  must choose which behavior owns an unrecorded workspace and, if it is archived,
  define the authoritative work-item edge that cleanup must use.

- **Clause 8 — conversation/intent provenance graph (AMENDED by Flynn's carrier
  ruling, 2026-07-29, per artifact-carrier-proposal-v1):** the substrate attaches
  the BEST SUBSTRATE-OBSERVED message edge plus its evidence class
  (`recordedTurnEvidence`: `tool-call-observed` | `session-concurrent` | `none`,
  meanings exactly as the proposal defines). The former wording demanded the
  exact firing `messages.id` unconditionally; that exactness was UNSATISFIABLE —
  no per-turn gateway→agent channel exists, and an agent-filled wire field is
  forgeable — so the original wording is not and cannot be claimed closed. The
  CLI `--work-item` requirement stands unchanged. Caller-supplied provenance
  fields remain stripped (forensics-v2 boundary).

- **Clause 11 — firing-turn evidence (AMENDED by the same ruling):**
  `recordedMessageId` becomes nullable, paired with `recordedTurnEvidence`.
  `tool-call-observed` is an observation-quality claim — the runtime's hook saw
  the tool call inside a known turn — NEVER an unforgeability or exact-causality
  claim. Artifact recording FAILS OPEN: it must not trap a correct agent in an
  unsatisfiable completion loop. No consumer may silently treat
  `session-concurrent` or `none` as exact turn proof. The former
  exact-firing-turn wording was unsatisfiable and is recorded as such, not
  closed.

- **Clause 12 — exact work-item edge:** the owned table now requires an exact
  `work_items.id` FK and upgrades populated compatible legacy tables, but the shipped
  CLI still makes `--work-item` optional. The CLI parser/dispatcher must make it
  required. The spec owner must also rule how pre-migration rows with a null
  `workItemId` are repaired without inventing intent or deleting permanent rows.

- **Clause 14 — legacy rows with absent load-bearing edges:** the owned persistent
  migration and rollback paths are now covered against both compatible data and a
  row actually produced by the old writer. That old writer always stored a null
  `recordedMessageId` and could store a null `workItemId`, so those rows cannot enter
  the ratified non-null FK shape without fabricated provenance. The spec owner must
  define a truthful legacy-row repair policy.

- **Clause 20 — released transition:** `Artifacts.release/2` performs the real
  transition, but no shipped verb reaches it. Gateway, router, and CLI owners must
  add `artifact-release` and an end-to-end test that observes the retained row in
  `released` state with no `home`.

- **Clause 21 — archived home is actual custody:** reachable local workspaces now
  use canonical paths so a symlink cannot leave artifact bytes outside custody.
  Remote workspaces and hard copy failures still lack an archive executor. Gateway
  / remote-workspace ownership must supply archival where the bytes live and test
  the returned exact home.

- **Clause 22 — released means no asserted home:** the owned operation and migrated
  schema enforce this, but the release operation has no Gateway/router/CLI surface.
  Those owners must expose it. The spec owner must also decide how a legacy
  `released` row with a non-null `home` is migrated without silently rewriting
  historical custody assertions.

- **Clause 31 — archiving always succeeds:** the literal clause cannot be guaranteed
  for a missing remote workspace or an exhausted/unwritable filesystem while also
  requiring archived bytes to survive and teardown never to block. The spec must
  define valid archival preconditions and a durable failure/retry owner, or the
  remote-workspace/Gateway lane must provide a guaranteed archive service. Until
  then, this module deliberately raises on missing bytes or terminal rename-plus-copy
  failure rather than falsely labeling an uncustodied row `archived`.

- **Clause 33 — archived rows and bytes remain findable:** the local owned path is
  real, but the clause also depends on authoritative firing-turn/work-item callers
  (clauses 8/11/12) and remote archive execution (clauses 4/21/31). Those exact
  cross-lane changes must land before this aggregate clause can close.

- **Clause 35 — archived means actual Tightbeam custody:** local canonical custody is
  enforced in this module. `lib/tightbeam/gateway.ex` must stop passing `nil` for
  remote workspaces and must return a real archive result before any row is marked
  archived.

- **Clause 36 — out of custody preserves provenance and clears location:** the owned
  release update retains the row and clears `home`; Gateway/router/CLI owners must
  expose that operation and prove the observable end state through the shipped
  interface.

- **Clauses 38 and 39 — warm custody-handoff notice:** the required notice belongs
  in relocating-agent archetype guidance, not in the artifact substrate. The
  `lib/tightbeam/archetypes.ex` owner must add the ratified plain-language notice
  before any relocating agent moves archived bytes into user/org-managed space,
  with an archetype test that asserts the notice is present.

- **Clause 40 — durable topology reaches the exact conversation:** this depends on
  the authoritative firing-turn binding and required CLI work-item input described
  for clauses 8, 11, and 12. The router/transcript and CLI owners must implement and
  integration-test those edges; `Artifacts` cannot infer them truthfully.

- **Clause 45 — time-window filters:** the spec requires a time window but does not
  define the bound names, inclusivity, or which artifact timestamp the window uses.
  The spec owner must ratify those semantics before `Artifacts.list/2`, Gateway,
  router, and CLI owners implement and test the full public filter.

- **Clause 51 — org-visible branch registration:** the branch-producing
  reconciliation/integration path is outside `Artifacts`; its owner must call the
  artifact-record seam for the resulting org-visible branch with authoritative
  work-item, session, and transcript provenance, then prove the branch row is
  queryable from the work item.

- **Clause 57 — authoritative work-item spec resolver:** generic artifact filtering
  cannot decide which artifact satisfies `work_items.specRefName`.
  `lib/tightbeam/work_items.ex`, Gateway, and CLI owners must replace or bind that
  string to an exact spec artifact identity and resolve its current `home`.

- **Clause 58 — artifact workspace archival is universal and nonblocking:** the
  reachable local path is real, but remote sessions still have no reachable
  workspace in the Gateway reap call and terminal filesystem failure has no durable
  retry owner. The Gateway/remote archive lane plus the clause-31 spec ruling must
  provide those missing states and end-to-end coverage.


## Lane: fix-core-rules (merged 5395ab0)

# Core-rules conformance handoffs

## Check-tier clause 127 — verdict filing emits exactly one verb event

- Blocker: the required behavior already exists in the owned implementation at
  `Tightbeam.Dispatch.dispatch_to_handler/7`: a successful `attest` handler
  return appends exactly one `events(kind="verb")` row. The rejected proof used
  a completion attest, however, and this lane does not own any test path.
- Required cross-lane change: in `test/check_tier_test.exs`, create a real open
  assignment and authorized user or session principal, file
  `kind="verdict"` through `Dispatch.dispatch/3`, assert the verdict row's
  observable fields, and assert the event table contains exactly one row whose
  `kind` is `"verb"` and `verb` is `"attest"`. The test must use the real
  Gateway handler and must not call `Assignments.__handle__/3` directly.
- Existing cross-lane proof: the core-assignments lane commit `1f74cd6`
  contains this real verdict-via-Dispatch assertion in
  `test/assignments_test.exs`; integrate that proof in the lane that owns the
  test rather than duplicating verdict-specific production logic here.
- Self-proof target: removing the successful-handler
  `EventLog.append_event(db, "verb", ...)` call in
  `Tightbeam.Dispatch.dispatch_to_handler/7` makes that test fail.

## Rails I8.2 / F2.2 / P5.1 / C6.8 — F2 fixed target/parameter reachability

- Blocker: `rails-mechanism-v1.md` F2(b) says literal remedy targets and params
  map to `target.*`/parameter facts, but it does not define that mapping.
  Runtime `target.*` facts are projections of `Org.get(call.session_key)`, not
  of literal target names: assign/wake role targets require runtime role
  resolution and a DB row, while spawn dispatches with `session_key=nil`.
  The closed fact registry also has no generic remedy-parameter facts; the only
  parameter-derived facts are `attest.kind` and
  `assign.declared_files_overlap_open`, neither of which has a general
  literal-to-fact mapping. Inventing one would change the substrate fact model.
- Required spec change: add an explicit per-action table mapping every literal
  `[rule.remedy]` target/param field to an existing fixed fact value, including
  the behavior for role targets, literal session keys, spawn's nil target, list
  params, and interpolated values; or narrow F2(b) to the currently
  implementable fixed attributes (`verb` and
  `caller.origin_class="remedy"`). Then add the complete table-driven load
  matrix in the lane that owns `test/rail_remedy_test.exs`.

## Rails I7.1 / E1.1 — turn-end non-pass denial rows

- Blocker: the missing actor is `Tightbeam.Supervision.rail_step`, outside this
  lane's owned paths.
- Required cross-lane change: in `lib/tightbeam/supervision.ex`, append one
  best-effort `events(kind="denied")` row for each turn-end remedy, escalate,
  and deny branch using the synthesized call and E1 payload. Add real
  `test/supervision_test.exs` assertions for exactly one row per branch with
  `edge="turn-end"`, statute, reason, ref, and manifest SHA.

## Rails I8.3 / F2.5 — blocked turn-end remedy re-enters the ladder

- Blocker: only `Tightbeam.Supervision.rail_step` can inspect a blocked remedy
  outcome and fall through to the existing prod/escalation ladder; that module
  is outside this lane's owned paths.
- Required cross-lane change: retain the existing acted/watermarked branch for
  non-blocked outcomes, but on `outcome=="blocked"` record
  `rail_sweep/re-obligate` and fall through to the ordinary ladder. Add a real
  conditional-blocker integration in `test/supervision_test.exs` that observes
  the blocked remedy lifecycle row and the ladder action on the same terminal.

## P3 clause 91 — producer worker unlocks a produced-verdict gate

- Blocker: the required acceptance proof belongs to the producer runner and
  `test/producers_test.exs`, outside this lane's owned paths.
- Required cross-lane change: load a real
  `assignment.produced_verdict_kinds not_in ["tests-passed"]` gate, prove
  completion denies, invoke public `run-tests`, allow the actual async runner
  to file its frozen producer verdict, then re-dispatch completion and prove it
  succeeds. Do not insert the verdict through a helper.

## Check-tier clause 124 — zero-rule lifecycle precedence remainder

- Blocker: the remaining acceptance matrix belongs to
  `test/check_tier_test.exs`, outside this lane's owned paths.
- Required cross-lane change: send lifecycle attests through
  `Dispatch.dispatch/3` under zero rules and assert non-holder plus garbage kind
  returns `not_holder`, holder plus garbage kind returns `invalid_kind`, and a
  lifecycle kind carrying stray `verdictKind` returns
  `invalid_verdict_kind` last.

## Check-tier clause 126 — verdict activity resets supervision prod state

- Blocker: this is a `Tightbeam.Supervision` integration and its implementation
  and test are outside this lane's owned paths.
- Required cross-lane change: mirror the real progress-row prod-reset fixture,
  file a real verdict on the open assignment, prove `attest_count` advances,
  and prove the next supervision evaluation resets the attempt/prod counters
  from that neutral row count.

## Check-tier clauses 129A / 129B — complete attests kind/order matrix

- Blocker: the required query fixture belongs to
  `test/check_tier_test.exs`, outside this lane's owned paths.
- Required cross-lane change: create progress, completion, surrender, and
  verdict rows with both distinct and tied timestamps, call the real `attests`
  read verb, and assert all kinds are returned in `ts ASC, id ASC` order.


## Lane: fix-core-assignments (merged 855bc9a)

# Core assignments redo handoffs

- **Work-item 48 — ordinary Dispatch audit only:** remove the remaining `metadata`/`composition` event taxonomy, derived work-item event projection, and public owner-partitioned work-item API from `lib/tightbeam/work_state.ex` and `lib/tightbeam/wire/router.ex`; update their tests to expect only the four v1 Dispatch verbs and ordinary `kind="verb"` audit. The owned `Assignments` and `WorkItems` callback emitters are already absent.
- **Check-tier 124 — complete zero-rules acceptance matrix:** add an explicit zero-rules test through `Dispatch.dispatch/3` in `test/check_tier_test.exs`. It must prove completion with zero verdicts succeeds, exercise the full v1 lifecycle authorization/state/error precedence matrix through Rules/Dispatch, and compare the complete lifecycle response against the v1 shape to show the check-tier delta is exactly always-present null `verdictKind` and `byUser` (accounting separately for later-spec P3 fields). No owned implementation change can supply this missing test proof.
- **P3 45 — full wrong-link Rules matrix:** extend `test/rules_test.exs` with review assignments linked to both the correct producer assignment and a different producer assignment, crossed with holder/third-session/user authors, producer/non-producer commissioners, and same/cross harness/provider stamps. Assert the exact `independent_`, `cross_harness_`, and `cross_provider_` fact results. The owned SQL helper excludes wrong links, but query-helper proof is not the required Rules fact matrix.


## Lane: feat-bug-provenance (merged 9e5ef0f)

# Handoff

## `refix-requires-diagnosis` statute — blocked on missing substrate observables

The `agentic-engineering-guidance-spec.md` §6 statute cannot be authored as live,
loadable law in this content-only lane. Its predicate requires both a bug-kind
work-item attribute and a typed link identifying completed prior fix assignments.
Neither exists in the current work-item/assignment model or in the closed
`Tightbeam.Rules` fact registry. The shipped `identity/rails` loader accepts only
tool-call matcher statutes and explicitly rejects predicates; encoding the rule there
as a comment, inert matcher, or ignored table would be a stub.

The blocking cross-lane change is a ratified substrate spec and implementation adding
those two typed model observables, exposing the corresponding rule facts, and defining
the once-per-work-item redirect/remedy episode. After that lands,
`priv/kungfu/agentic-engineering/rails/engineering.toml` can carry a real
`refix-requires-diagnosis` rule whose absent `diagnosed` verdict assigns recon with
`bug-provenance` and whose integration test proves the remedy creates the diagnosis
assignment and permits the re-fix on re-dispatch.


## Lane: feat-refix-statute (merged f2891a8) — follow-ups

# conformance-smoke handoffs

Only the independent verifier's ten legitimate external/spec blockers remain. Every
lane-closeable residual was removed from this handoff and is covered by the executable
corpus runner.

| Clause(s) | Exact blocker | Required cross-lane/spec change |
|---|---|---|
| #4 | Copying the corpus and invoking the same ExUnit loader is not a second self-tuning consumer. | The self-tuning/generated-rail owner must load `identity/conformance/` through its real validator and run the unchanged corpus. |
| #7, #147, #155 | The governing spec makes forbidden-substitution intent advisory and names containment only as partial coverage. | Define an enforceable observable if this advisory intent is to become a mechanical acceptance check. |
| #21 | §1.2 says every fixture in a green class is green, while A1 requires green C2/C3 classes containing three `pending-unhomed` fixtures. | Reconcile the governing spec's class-green rule with A1/taxonomy. |
| #39 | The locked `world.adjudicate = {session, hold}` shape conflicts with the actual owner API, which requires an episode/action request. | Reconcile the world shape with the authorized owner verb; direct SQL remains forbidden. |
| #43, #116 | The exact public `rail_step/4`/`window_start` seam named by the spec is not exposed; the available public consumer is `Supervision.evaluate/5`. | Expose the pinned rail-step/window input contract. The public consumer's nil/no-write and duplicate end states are covered here. |
| #60 | Canonical fresh-identity bootstrap is owned by identity/archetype code and canonical material outside this lane. | The identity owner must supply the fresh-bootstrap artifact proof. |
| #133 | A sandbox profile-application refusal cannot be deterministically caused by fixture script content. | Expose Q3's deterministic profile-apply-failure hook; `contained-refused` remains case-level `pending-runtime`. |
| C6 `escalation-return-dispatch` self-park | The dispatch actor opens/re-returns the decision request, but neither `Dispatch.dispatch/3` nor `Escalation.escalate/4` schedules the live raiser's verb-edge self-park required by enforcement-smoke-set-spec C6. This lane owns only the corpus/runner. | The escalation/dispatch owner must add the verb-edge self-park, after which this fixture must assert its wake row and target. |
| C7 `schedule-then-check` recovered race | `Supervision.park_escalation/3` schedules/stores `parkWakeId` but has no post-schedule decision-status read, cancellation, or no-replay cursor. Public seams prove pre-ruled/no-park and later-ruling/ordinary-wake, but cannot produce the required “ruling lands between schedule and recovered check” branch because the check does not exist. | The supervision/escalation owner must add the wake-first recovered-status check and cancellation/no-replay behavior from mechanism r11; then replace the partial executable proof with the exact race assertion. |
| C7 `scheduled-wake-suppression` r21 self-wake branch | `Supervision.turn_end_schedule/0` exposes the Flynn-ratified r21 order, but `rail_step/5` still returns `:fallthrough` when `Wakes.self_pending_count/2 > 0`, bypassing `:rail_enforcement` before the named `:pending_wake_gate`. The pending fixture executes and records this mismatch. | Remove the internal self-wake bypass from `rail_step/5`; all pending wakes must be handled only by the later `:pending_wake_gate` slot. Then flip the fixture assertion from the recorded mismatch to `{:acted, :rail_remedy}`. |
| Required full-suite proof after merging `main` | `mix test test/conformance_test.exs` reaches the Cap producer actor, but merged commit `5ca6728` makes `Producers.execute/4` fail with `host-fail: producer process group unavailable`. The canonical independent test `mix test test/producers_test.exs:65 --trace` fails waiting for the same producer job to reach `done`, so this is not a conformance-fixture surrogate or assertion defect. | The producer owner must repair the host process-group launch/verification contract on eezo. Keep the conformance Cap actor's real producer execution; do not weaken it to accept a host failure. |
| `refix-requires-diagnosis` full-suite gate | `mix test` executes 619 tests and 6 doctests but has 9 failures, all in the existing producer/process-group path. On eezo, stopped producer processes report state `TNs` (nice level 5), while `Producers.verify_process_group/2` accepts only `T` or `Ts` and returns `host-fail: producer process group unavailable`. The isolated `mix test test/producers_test.exs` reproduces the same blocker with 7 failures out of 10; the 52 statute/rules/remedy/work-item tests pass. | The producer owner must make process-group verification recognize the valid stopped state with the host's niceness flag, then rerun the full suite. This statute lane must not alter unrelated producer lifecycle code or weaken its tests. |


## Lane: fix-cli (merged) — SUPERSEDED by cli-surface-v1 (adjudication #7)

Both items below were filed against the RETIRED cli-rust-v1 PORT spec and are moot under cli-surface-v1: the "only two dependencies" limit was port-fidelity discipline (gone), and rail-exec interception before args::parse is now INTENDED (substrate-internal verb, not an agent-surface command needing the TS canonical error). No action required.

# CLI lane handoffs

## Clause 11 — direct dependency limit

`cli/Cargo.toml` is outside the CLI lane's owned paths and still declares
`libc = "0.2"`. The dependency is used directly by `cli/src/contain.rs` for
process-group and signal operations, which is also outside this lane. A
Cargo/containment owner must either replace those calls using only the two
dependencies permitted by `cli-rust-v1.md` and remove `libc`, or obtain and
record a governing-spec amendment that permits `libc`.

## Clauses 1, 57, and 66 — executable-level `rail-exec` command

`cli/src/main.rs` is outside this lane's owned paths and intercepts `rail-exec`
before `args::parse`, so the parser cannot make that command produce the
TypeScript reference's canonical unknown-command error. The executable owner
must remove the `rail-exec` interception from `main.rs` (and adjudicate the
resulting `contain` module reachability), then add a real-binary test that runs
`tightbeam rail-exec` and asserts the exact canonical unknown-command stderr
and exit status 1.

## Mandatory clippy gate — unreachable legacy `init` and `probe` modules

`cli/src/main.rs`, `cli/src/ceremonies.rs`, and `cli/src/probe.rs` are outside
this lane's owned paths. The v1 command surface intentionally does not expose
the later `init` and `probe` commands, but `main.rs` still compiles both legacy
modules. Removing the rejected discarded-function-pointer suppression from
`dispatch::run` exposes dead-code errors throughout those modules under
`cargo clippy -- -D warnings`. The executable/module owner must stop compiling
the non-v1 modules (while preserving the v1 `setup` and `assimilate` ceremony
paths), or obtain a governing-spec amendment that makes their behavior
reachable; lint suppression or unused function-pointer references are not an
acceptable close.

## Tagged CLI integration suite versus clauses 1, 10, 14, 19, 36, 57, and 66

`test/cli_integration_test.exs` is outside this lane and requires
`.tightbeam-session` identity discovery plus assignment, producer, and work-item
verbs. Those expectations directly conflict with the governing v1 spec's
TypeScript-normative discovery, exactly-one explicit identity, canonical command
set, and no-new-verbs requirements. The spec/test owner must adjudicate the
source of truth and then either update the tagged integration suite to the v1
CLI surface or amend `cli-rust-v1.md` before those tests can be made compatible.

# conformance-smoke handoffs

Only the independent verifier's ten legitimate external/spec blockers remain. Every
lane-closeable residual was removed from this handoff and is covered by the executable
corpus runner.

| Clause(s) | Exact blocker | Required cross-lane/spec change |
|---|---|---|
| #4 | Copying the corpus and invoking the same ExUnit loader is not a second self-tuning consumer. | The self-tuning/generated-rail owner must load `identity/conformance/` through its real validator and run the unchanged corpus. |
| #7, #147, #155 | The governing spec makes forbidden-substitution intent advisory and names containment only as partial coverage. | Define an enforceable observable if this advisory intent is to become a mechanical acceptance check. |
| #21 | §1.2 says every fixture in a green class is green, while A1 requires green C2/C3 classes containing three `pending-unhomed` fixtures. | Reconcile the governing spec's class-green rule with A1/taxonomy. |
| #39 | The locked `world.adjudicate = {session, hold}` shape conflicts with the actual owner API, which requires an episode/action request. | Reconcile the world shape with the authorized owner verb; direct SQL remains forbidden. |
| #43, #116 | The exact public `rail_step/4`/`window_start` seam named by the spec is not exposed; the available public consumer is `Supervision.evaluate/5`. | Expose the pinned rail-step/window input contract. The public consumer's nil/no-write and duplicate end states are covered here. |
| #60 | Canonical fresh-identity bootstrap is owned by identity/archetype code and canonical material outside this lane. | The identity owner must supply the fresh-bootstrap artifact proof. |
| #133 | A sandbox profile-application refusal cannot be deterministically caused by fixture script content. | Expose Q3's deterministic profile-apply-failure hook; `contained-refused` remains case-level `pending-runtime`. |
| C6 `escalation-return-dispatch` self-park | The dispatch actor opens/re-returns the decision request, but neither `Dispatch.dispatch/3` nor `Escalation.escalate/4` schedules the live raiser's verb-edge self-park required by enforcement-smoke-set-spec C6. This lane owns only the corpus/runner. | The escalation/dispatch owner must add the verb-edge self-park, after which this fixture must assert its wake row and target. |
| C7 `schedule-then-check` recovered race | `Supervision.park_escalation/3` schedules/stores `parkWakeId` but has no post-schedule decision-status read, cancellation, or no-replay cursor. Public seams prove pre-ruled/no-park and later-ruling/ordinary-wake, but cannot produce the required “ruling lands between schedule and recovered check” branch because the check does not exist. | The supervision/escalation owner must add the wake-first recovered-status check and cancellation/no-replay behavior from mechanism r11; then replace the partial executable proof with the exact race assertion. |
| C7 `scheduled-wake-suppression` r21 self-wake branch | `Supervision.turn_end_schedule/0` exposes the Flynn-ratified r21 order, but `rail_step/5` still returns `:fallthrough` when `Wakes.self_pending_count/2 > 0`, bypassing `:rail_enforcement` before the named `:pending_wake_gate`. The pending fixture executes and records this mismatch. | Remove the internal self-wake bypass from `rail_step/5`; all pending wakes must be handled only by the later `:pending_wake_gate` slot. Then flip the fixture assertion from the recorded mismatch to `{:acted, :rail_remedy}`. |
| Required full-suite proof after merging `main` | `mix test test/conformance_test.exs` reaches the Cap producer actor, but merged commit `5ca6728` makes `Producers.execute/4` fail with `host-fail: producer process group unavailable`. The canonical independent test `mix test test/producers_test.exs:65 --trace` fails waiting for the same producer job to reach `done`, so this is not a conformance-fixture surrogate or assertion defect. | The producer owner must repair the host process-group launch/verification contract on eezo. Keep the conformance Cap actor's real producer execution; do not weaken it to accept a host failure. |

## CLI v1 clippy gate — unowned retired ceremony and containment code

The ratified CLI surface removes CLI-side `init` and `setup`, so the real
implementations still compiled from unowned `cli/src/ceremonies.rs` are now
unreachable. `cargo clippy --manifest-path cli/Cargo.toml -- -D warnings`
reports dead code for `setup`, `init`, their helpers, and the `InitArgs` /
`SetupArgs` types that `ceremonies.rs` still imports. The same gate reports an
independent `clippy::collapsible-if` finding in unowned
`cli/src/contain.rs:444`. The executable/ceremony owner must stop compiling and
delete the retired init/setup code and its argument types, and the containment
owner must apply the clippy-prescribed equivalent conditional rewrite. This CLI
lane cannot truthfully close the requested clippy gate without modifying files
the assignment explicitly forbids.
