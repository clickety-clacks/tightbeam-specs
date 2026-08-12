# Gateway split — the monocode refactor — v1

Status: READY (gate-cleared 2026-07-26, r2 verdict READY — all four r1 findings closed; wave-manifest precision deliberately owned by the manifests. r1 NOT-READY(4) folded — two-phase I1, honestly-scoped I2, belongs-elsewhere split literal-vs-behavioral, per-wave normative manifests). Flynn order:
"push the monocode refactor." PURE MOTION refactor — zero behavior change; every wave
merges with the full suite + live smoke green and `git diff` reviewable as
moves-plus-qualified-calls. SEQUENCED AFTER feat-s4-forensics merges (it edits
adjudication/supervision/wakes in place; this spec then moves the enriched code once).

## Why (the defect)

gateway.ex is a 4k-line god module: verb registry, delivery, turn pipeline,
adjudication routing, credential wiring, boot, notifications — one file, 26-site
helpers spanning 3,900 lines, cross-module invariants living as tribal knowledge.
Every reviewer tonight cited it by five different line ranges; pattern-propagation
means agents will keep growing it.

## Prerequisites (BEFORE any motion — merged as their own commits)

P0. **Task #23 resolved** (dead escalation_context / silent owner doorbell): wire or
    delete BEFORE the split cements a dead surface into a new module.
P1. **Property tests for the five invariants** (from the seam map; each a named test
    file that any wave must keep green):
    - I1 hold/wake/claim (spans 6 modules), TWO-PHASE per the gate (a decision hold
      legitimately has NO recovery wake):
      DECISION phase (hold='*'): no turn claimable; exactly one live owner-decision
      path (the owner wake/turn or an open decision episode).
      RECOVERY phase (hold=recoveryWakeId): at most one queued/running turn whose
      wakeId equals the hold; released only by that turn's terminal transition.
      Observation points: after each committed transaction (not mid-txn transients);
      interleavings drawn from the REAL entry points (turn-failure txn, adjudicate
      verbs, wake fire, turn terminal, boot reconcile) in any serializable order.
      Liveness is scoped: in RECOVERY phase the wake exists (no temporal claim about
      DECISION phase, which awaits a human/heal by design). TEST FIRST.
    - I2 delivery atomicity+dedupe, honestly scoped (gate: exactly-once publication
      is FALSE today — the txn commits before complete_delivery publishes; a crash in
      the gap publishes zero and a replay republishes nothing): message∧turn commit
      atomically; wakeId UNIQUE collapses at-least-once enqueue; and FOR AN
      UNINTERRUPTED SUCCESSFUL COMPLETION exactly one message frame + one accepted
      turn-state frame publish. The crash-gap behavior is pinned AS-IS (a named
      at-most-once publication note), not asserted away; strengthening it is a
      behavioral prerequisite OUTSIDE this refactor if ever wanted.
    - I3 retire-cascade totality+ordering: every active transitive descendant exactly
      once, parent-last, all-or-nothing vs critical leases, intent-wake idempotence.
    - I4 respawn transfer atomicity: assignments+bindings+rearms move all-or-none
      (EffortRearmRace bounded retry); no observable half-transfer.
    - I5 reap never fails a committed retire; shared-adapter closure refcounted by
      live sessions.

## Target shape (module names = contracts; all under lib/tightbeam/gateway/)

Composition root stays `Tightbeam.Gateway` (~400 lines): `children/1`,
`children_after_preflight/1`, `preflight!/1`, `handlers/1` — handlers/1 remains THE
single assembly point (Rules.load! needs the complete closed verb set at boot; 22 test
files + Dispatch depend on the whole-table contract).

## Waves (each wave = one branch, one review, one merge; smallest-risk first)

W0 substrate (retires the cross-file helper spans):
  1. `Gateway.Notify` — broadcast/publish_message/publish_turn_state/
     assignment_change/item_change/markers/best_effort (26-site broadcast; gateway is
     the SOLE ConnRegistry publisher — that stays true, one module deeper).
  2. `Gateway.Callers` — resolve_caller/admin_origin?/admin handlers/role+binding
     authz. Pure functions over DB reads.
  3. `Gateway.SessionConfig` — defaults/validate_credential/validate_catalog_model/
     catalog_provider!/harness_for_ref/credential_status/spinup_opts/
     strict_apply_current_model. MUST land before spawn/tune/adjudicate move.
W1 clean leaves: `Gateway.Status` (org_options/session_status);
  `Gateway.Onboarding`; CLI-target probes → INTO `Tightbeam.Placement`
  (belongs-elsewhere); `Gateway.IdentityVerbs` (+ served_snapshot, its 4 callers
  qualify).
W2 verb surfaces: `Gateway.CredentialWiring` (children half + provider runtime;
  register-host keeps one callback in the registry); `Gateway.RoleVerbs`;
  `Gateway.WakeVerbs` (+facts_read); `Gateway.Spawn` (+carry_pinned_overrides);
  `Gateway.Tune`.
W3 the tangle, THIS order: `Gateway.Delivery` (public — four lib modules call it) →
  `Gateway.Lifecycle` (retire+reap+critical+host-rearm) → `Gateway.Adjudicate` (the
  468-line cluster, deps now all extracted) → `Gateway.Turn` LAST (runner's failure
  path is a second spelling of hold-arming — moving it last lets both converge on
  arm_hold_in_txn instead of freezing the duplication into two modules).

## Belongs-elsewhere — SPLIT per the gate into two classes

LITERAL-EQUIVALENT moves (in-scope, fix-while-moving, provably zero-behavior):
- Doorbell SQL reaching into assignments/work_items → WorkState/WorkItems (literal
  query relocation; Notify stays a pure wire seam).
- base_ref/1 → Adapter.base_model_ref/1 (it is literally
  elem(parse_model_ref(ref), 0)).

BEHAVIORAL consolidations (gate: NOT zero-behavior — DB selection/ordering/caller
mutations/filter semantics differ) — OUT OF SCOPE for this refactor, filed as their
own follow-up tickets with exact invocation/order/filter contracts and before/after
truth tables; the split MOVES this code verbatim wherever its cluster goes:
- Boot-schema single-ownership (Boot vs children_after_preflight's second loop —
  different DBs, different ordering, injected-DB tests).
- Ad-hoc SQL migrations out of the composition root (host='local' rewrite, cliToken
  backfill, migrate_handle_roles — moving them into Org.ensure_schema would make
  every caller mutate).
- Forest-walk unification (retirement walks ACTIVE rows; replay walks ALL rows
  selecting retired — similar, not equivalent, esp. around retired intermediates).

## Rules of motion

- A wave changes NO behavior: moves + qualified calls + @doc moves only. The diff for
  each wave must be reviewable as such; any behavioral fix discovered mid-wave is a
  FINDING routed out, never folded in (necessity gate).
- **Per-wave NORMATIVE MANIFEST (gate F4), written and reviewed BEFORE the wave's
  implementation**: source symbol → destination symbol + visibility; the EXACT caller
  files that change (incl. out-of-gateway callers — Delivery: assignments/wakes/
  effort_checkin/supervision; Status: wire/router) and the compatibility/delegation
  policy per caller; module attributes/aliases/defaults/callback-captures traveling
  with each symbol; the only permitted non-literal transformations with their
  equivalence argument. The wave's declared-files proof checks against ITS manifest.
- Full suite + the five property tests green per wave; LIVE smoke matrix per wave
  (motion around the adapter/delivery seams = the mock-divergence rule applies).
- Test files keep referencing public contracts; a wave may update test imports/module
  names but never assertions.
- Each wave merges before the next starts (no stacked motion).

## Required proofs

1. P1's five property tests exist and pass BEFORE W0 merges, and after every wave.
2. Per wave: suite 0 failures ×2 seeds, live smoke 9/9 both legs, and
   `git diff --stat` shows only the wave's declared files.
3. After W3: gateway.ex ≤ ~450 lines (composition root only); no module >900 lines;
   `broadcast` has exactly one home; the hold-arming protocol has exactly one
   spelling (arm_hold_in_txn).
4. Zero changes to any test assertion across all waves (module renames excepted).

## Component touches

lib/tightbeam/gateway/ (new tree), gateway.ex (shrinks), placement.ex/boot.ex/org.ex/
work_state.ex/adapter.ex (belongs-elsewhere receivers), test module renames. NO wire,
schema, or behavior surface.
