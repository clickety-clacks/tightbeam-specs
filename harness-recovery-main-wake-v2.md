# Harness recovery Main wake v2

Status: DRAFT for independent spec review. Not bound to the work item.

Governing work item: `wi_3bb2ea6c-9cab-4e85-9981-676c4b32c3b6`, row version
`1794076140532`. Commissioned by assignment
`asg_f853bd5b-cbf4-4c89-b2be-fceec27d1cfc` and finalized under successor
assignment `asg_348f579e-54cf-4751-a421-726dd2157399`.

This revision answers changes-requested review `att_92d397fe` of
`harness-recovery-main-wake-v1.md` at commit
`73aec01d7331e08b148994d6525ff75c2b00e137` (SHA-256
`40654018a7ec353c393e2ea8230e3ecdc2aed3a6ecc0b3c99e49de1783960aea`), and
changes-requested review `att_5284b34e` (report `art_74107a30`) of this file at
commit `c396aced` (SHA-256
`b24d4fe1601fe8764f1f28f068bb8724b2b80a85efa2fbf4b2a4184801356b4d`). It
applies product ruling `att_5172407a` on that review, WI932 ruling
`att_a0e28188`, and changes-requested review `att_dcadcd9c` (report
`art_537517fa`) of this file at commit `63c8bedd` (SHA-256
`e291ff9842ce9e37d3cf134319af069bde8d513aa0d2db46d1f7828c03b5301c`). It then
closes Q5 against the reviewed and rebound WI932 r3, starting from the interim
revision at commit `e2c515053185f9259048a07c22fec8824e4f0cac` (SHA-256
`7f343e10d8f2fffdf212fd011bfee12f4f466fa3f73d8f85d76bc263f54586ef`), whose
separable clauses were reviewed clean for that phase in `att_21918a0e` (report
`art_2d2ccd10`). It changes design only. It authorizes no source edit, test run, integration target, release,
installation or live action.

This amendment, under assignment `asg_259ad210-3b79-4eea-aa58-2cab7f80374f`,
amends the revision bound at commit `d7b1985026aebd54c23ddc399fab5bd7a47e5de8`
(SHA-256 `3637b0121721137f2f70042b8dc58962e97492002e0365b68700ee4a891caae4`,
artifact `art_6220a6c7`). The resolution correlation alone cannot tell a WI932
release from any other resolution without parsing an opaque value (gap report
`art_3212fbdd`). This amendment therefore applies product ruling `att_05b91e15`
(`art_e6b67dda`) and the reviewed and bound WI932 r5, whose section 6 adds the
typed event value `cycleRelease`, and uses that value as the only release
discriminator.

This amendment, under assignment `asg_d3e63fc4-0a26-40e6-9be0-8f343b59d170`,
amends the revision bound at commit `9ec5d81d52ec502fdcd094cbee726721cf828026`
(SHA-256 `364425aa60d31f6b02371c645f79c09596c3d075e44b2317ae88da23a643c9ad`,
artifact `art_775088f2`). It applies Scope ruling `art_0f65a7ef`: a hold that
ends because an ordinary turn on the held harness succeeds is also a recovered
outage, and gets the same single Main notice per episode. It keys on the
hold-resolved event that WI932's existing normal-turn resolution already emits,
reads only typed values the bound WI932 r5 event already carries, and adds
nothing to WI932. It also records Section 12 ruling `art_272e927e` in A2.

Normative keywords follow RFC 2119 as clarified by RFC 8174. Requirement
sentences use EARS.

Basis labels used below:

- **Ask** quotes the work item body.
- **Review** quotes `att_92d397fe`.
- **Review 2** quotes `att_5284b34e` and its report `art_74107a30`.
- **PO** quotes the WI932 PO intent and topology judgment `art_4bd40c7a` as WI932
  R9 quotes it.
- **Ruling** quotes product ruling `att_5172407a` on Review 2.
- **Review 3** quotes `att_dcadcd9c` and its report `art_537517fa`.
- **WI932 ruling** quotes WI932 product ruling `att_a0e28188`, which elected the
  event-field route recorded in assessment `art_7bb12133`.
- **R62** cites the row-reaction contract R62 v13, `art_f574333c`, SHA-256
  `d0fdf4c303db2f973a9050d0ba696f7c387e02986e1a900821b18df699b1d19d`, read from
  its registered archive copy.
- **WI932** cites the bound held-harness contract r5
  `held-harness-hourly-recovery-r5.md`, work item
  `wi_93269dbf-9c94-43f9-a8f6-c6e82dfebf87`, SHA-256
  `6d4dee3fc31b5582d52e41e7094302a792fb1554096eb6819a0a4e2bee66d629`
  (artifact `art_521abed7`, reviewed clean in `att_890746f6`). **WI932 section 6
  note** quotes its note "Resolution correlation and cycle release on the
  resolution event (r3, r5)".
- **Cycle release ruling** quotes product ruling `att_05b91e15` (`art_e6b67dda`),
  which approved the typed boolean `cycleRelease` and this contract's rebinding
  of Terms "Release event", R1, the R11 trigger, the plain-English Conditions row,
  the "Release event interface" architecture row and Q5.
- **Scope ruling** quotes PO scope ruling `art_0f65a7ef`, which withdrew decision
  `dr_9a52966d` and "Supersedes: att_5172407a's Q2 acceptance and spirit-approved
  att_67b4a3de's scope limit only."
- **Section 12 ruling** quotes PO ruling `art_272e927e` on when WI932's section 12
  real-response evidence runs.
- **WI932 source** cites the WI932 lane source at commit
  `170a573d214f58136f9751a966d8d9c11b4ca4f5`, read for which paths emit a
  hold-resolved event (A7).
- **OAuth** cites `spec-oauth-recovery-main-prompt-v2.md` in this repository.
- **Brief** quotes the commissioning assignment.

## Spirit

Sources relied on:

- The work item body, row version `1794076140532`: "after a durable owner+harness
  outage, recovery produces exactly one due-now Main wake for that episode. Later
  success does nothing; a new outage is a new episode. If Main cannot be reached,
  preserve evidence and a retryable notice. Main uses installed Kung Fu to inspect
  and resume only work stalled on that harness; Tightbeam neither selects nor
  broadcasts to product agents. Share the recovery notion with held-harness work
  wi_93269dbf; do not build a second detector or general retry engine."
- The PO direction carried by the brief: WI932 is "the sole recovery definition
  (seed eligibility is rate-limit-dead only; every constituent route must succeed
  in one cycle; add no second detector)".
- The PO policy boundary that WI932 R9 carries: "Policy electing eligible holds,
  timing, suppression, recovery and notification belongs in configurable TOML
  rails."
- Product ruling `att_5172407a`: "With the default composition, every recovered
  outage gives each affected owner exactly one delivered Main notice. No one has to
  configure anything."
- Scope ruling `art_0f65a7ef`: "an outage that ends because an ordinary turn on the
  held harness succeeds is a recovery and must produce the same single Main wake as
  an outage ended by the WI932 hourly release." Its basis: 94 of 94 recent
  rate-limit outages ended that way, so a release-only notice "would almost never
  wake Main."

The intent this contract serves: when a harness outage ends, however it ends, the person who owns
the stalled work should not have to notice it. Their Main is told once, with
enough to act, and decides what to resume. Tightbeam reports a fact. It does not
choose which product agents matter.

## Goal

When a held harness recovers, each owner whose sessions were held receives
exactly one due-now prompt at their Main. A hold recovers when WI932 releases it,
or when an ordinary turn on its harness and host succeeds and WI932's existing
normal-turn path resolves it. The prompt counts as sent only when it
reaches a delivered Main turn. Until then it stays durable and is retried on a
narrow set of existing signals. The notice is a separate reaction in the base seed
composition's TOML rails, on by default and triggered by WI932's hold-resolved
event. WI932's release and its normal-turn resolution themselves send nothing.
Delivery, settlement, retry and one notice per episode are runtime guarantees, not
rail duties.

"One wake" means one logical notice per episode, of which at most one attempt
reaches a delivered Main turn. Failed attempts stay as evidence. An attempt whose
outcome is unknown may have reached Main before it was interrupted, so Main can
see the prompt again on retry; Main judges live state, and this contract adds no
idempotency mechanism.

## Non-Goals

- A second outage or recovery detector. No classifier, episode detector, success
  observer or probe beyond WI932's.
- Recovery notices for "other"-class holds. WI932's normal-turn path never resolves
  them; they end by their own authorized resolve command or by expiry, and keep
  their own review and notice routes (see Q6).
- Recovery notices for holds that end without a hold-resolved event, such as
  "other" expiry.
- Combining holds. Each hold that recovers is its own outage, even when one turn
  resolves several holds on the same harness and host.
- Choosing, enumerating, waking or resuming product agents.
- A general retry engine, a retry timer or exponential backoff. The tracked notice
  in the Architecture section serves only the recovery notice reaction; its retry
  behavior is fixed by R5 and R6 and is not configurable.
- New rail settings, rail-language features, per-owner settings, or notification
  options beyond the reaction's trigger, target and fixed R4 texts.
- Any change to WI932's release effect, its normal-turn resolution, its reactions,
  its plain-English translation or its resolution event. This contract reads the
  hold's state and class from the snapshot and the `cycleRelease` value that WI932
  r5 section 6 already puts on the event, and adds no field, marker or record to
  it.
- Security hardening, forgery, replay, timing or denial-of-service defenses.
- Changes to harness-health classification, incident opening, fence ownership,
  intent redelivery or the "other" review routes.
- Notifying anyone when a hold opens, while it stays open, or when a check cycle
  fails.
- Escalating to the person outside Tightbeam when no Main exists (see Q3).
- Changing the WI932 check schedule, eligibility or release rule.

## Terms

- **Hold.** A `harness_health_incidents` row as defined in WI932 section 3, for one
  (harness, host).
- **Route.** WI932's bound definition: (harness, host, shared account, model).
- **Failed-route set.** WI932's constituent routes of a hold: the distinct routes in
  the hold's linked terminal-failure evidence, read at recovery time (WI932 R3).
- **Outage generation.** One hold id. A hold that opens after an earlier one on the
  same harness and host closed is a new generation, even for the same routes.
- **Release.** WI932 R7: the single transaction in which a successful check cycle
  resolves an eligible hold. Under the WI932 seed rail only `rate-limit-dead`
  holds are eligible, and release requires that every constituent route succeeded
  in one cycle (WI932 R2, R3).
- **Ordinary-turn resolution.** WI932's existing normal delivered-turn resolution,
  unchanged under WI932 section 7: when a turn reaches `delivered` on a session on
  the hold's harness and host, the turn's terminal transaction resolves every open
  hold of a class other than `other` on that harness and host
  (`resolve_normal_turn_in_txn`), whatever model or route the turn used. A turn
  that follows a `RateLimitReset` fence release or a repair resume and is
  delivered is an ordinary-turn resolution.
- **Recovery.** A release or an ordinary-turn resolution of a hold. The recovery
  time is the hold's `resolvedAt`.
- **Recovered outage.** A hold that ended by recovery. Nothing else is a recovered
  outage for this contract.
- **Affected owner.** A distinct non-null `sessions.ownerUserId` of a session in the
  hold's `harness_health_members` rows as they stand at the hold's recovery.
- **Episode.** One (outage generation, affected owner) pair, that is (hold id,
  owner). Its outage is exactly that hold and its failed-route set, never every
  outage that shares the owner and harness. A recovered outage has one episode per
  affected owner.
- **Owner Main.** The session with `kind = 'main'`, `state = 'active'` and the
  owner's `ownerUserId`. This is the same selection harness health already uses
  for its owner-Main fallback. Today it resolves to the owner's personal session
  `agent:main:clawline:<owner>:main`.
- **Recovery notice (notice).** The durable record of one episode's obligation to
  reach the owner Main. Its states are:

  | State | Meaning |
  |---|---|
  | `awaiting_main` | No delivery attempt is outstanding. The notice is waiting for a retry signal (R6). |
  | `attempting` | One delivery attempt is outstanding, linked to its wake and, once known, its turn. |
  | `delivered` | A turn carrying the notice reached terminal status `delivered` on an owner Main. Terminal. |
  | `canceled` | The attempt's wake had a deliberate cancellation (R7). Terminal. |

- **Attempt.** One prompt delivery to the owner Main for one notice, with wake id
  `harness-recovery:<holdId>:<owner>:<n>`, where `n` counts attempts from 1.
- **Attempt turn.** The turn that carries an attempt's wake. When the wake is
  delivered inside a notice batch, the carrier wake owns the turn, and the attempt's
  own wake row records it as `deliveredTurnSeq`. The attempt turn is found through
  that field, not by matching `turns.wakeId` to the attempt's wake id.
- **Queued attempt.** An attempt whose wake is pending or whose attempt turn is
  queued and has not started running.
- **Interrupted attempt.** An attempt whose attempt turn was running when the
  gateway stopped. Existing boot recovery (`Ledger.recover_running`) ends that turn
  `failed_unknown` and never retries it.
- **Non-delivered outcome.** Any of: no owner Main exists when an attempt would
  start; the attempt's wake is canceled with reason `target_unresolvable`,
  `consumer_unavailable` or `target_retired`; the attempt turn ends `failed`,
  `failed_unknown` or `canceled`.
- **Deliberate cancellation.** Cancellation of an attempt's wake with any other
  reason, such as `requester_withdrew` or `superseded`.
- **Retry signal.** One of the three existing events named in R6.
- **Hold-resolved event.** The row-reaction event that WI932 section 6 ("Hold row
  events") admits when a hold resolves.
- **Resolution correlation.** The correlation a hold-resolved event carries under
  the WI932 section 6 note: "the correlation of the incident's resolution
  observation" that the resolving path already recorded. A WI932 release records
  one naming its check cycle (WI932 R7). A normal delivered turn carries "that
  turn's existing normal-success correlation". When no resolution observation was
  recorded, the event carries none.
- **Cycle release value.** The typed boolean `cycleRelease` that the WI932 r5
  section 6 note puts on hold row events. It is `true` only when it is set in
  WI932 R7's resolving transaction, after a cycle in which every constituent route
  succeeded (WI932 R3). It is `false` on every other resolution path and on every
  opened event. It changes no event's resolution correlation.
- **Release event.** A hold-resolved event whose `cycleRelease` is `true`, that is
  an event matching `{"op":"eq","args":[{"ref":"event.cycleRelease"},true]}`.
  Nothing else is a release event for this contract.
- **Ordinary-turn recovery event.** A hold-resolved event whose `cycleRelease` is
  `false` and whose hold snapshot class is not `other`, that is an event matching
  `{"op":"and","args":[{"op":"eq","args":[{"ref":"event.after.state"},"resolved"]},{"op":"eq","args":[{"ref":"event.cycleRelease"},false]},{"op":"ne","args":[{"ref":"event.after.failureClass"},"other"]}]}`.
  Under A7 this is exactly the event an ordinary-turn resolution emits.
- **Recovery event.** A release event or an ordinary-turn recovery event. No other
  event is a recovery event for this contract, and none is told apart by its
  resolution correlation.
- **Recovery notice reaction.** The separate reaction in the base seed
  composition's TOML rails that carries this contract's notification policy: its
  trigger, its target and the R4 texts (R11). It is not one of WI932's reactions.
  Its translation is in "Default recovery notice reaction, in plain English".

## Assumptions

Each can be falsified against source or records.

- **A1.** WI932's release action exists and runs in one transaction that can carry
  additional writes. It is not in the current release line: a search of
  release `0.1.14` source finds no check cycle or release action. This contract
  cannot be exercised before WI932 lands.
- **A2.** `harness_health_members` lists every session held by the hold's fence.
  At open it snapshots every active session on that harness and host, and it adds
  sessions from attached observations (`snapshot_affected_work` and the member
  insert in `harness_health.ex`).
- **A3.** Each owner has at most one session with `kind = 'main'` and
  `state = 'active'`. A read-only count of the live store on 2026-11-07 found
  exactly one such session.
- **A4.** Turn terminal status is one of `delivered`, `failed`, `failed_unknown`
  and `canceled`. Retirement reaches an attempt through wake cancellation with
  reason `target_retired`, not as a turn status. Every terminal transition already
  reaches `HarnessHealth.settle_other_route_in_txn` in its own transaction: the
  `SessionLane` terminal transitions, and boot recovery in `Ledger.recover_running`,
  which runs from `LaneManager.init` before `HarnessHealth.resume_other_routes`.
- **A5.** The owner Main may itself run on the recovered harness. A read-only query
  of the live store on 2026-11-07 listed the owner Main as a member of 153 holds. Under
  WI932 R7 the fence is removed in the release transaction, and an ordinary-turn
  resolution of a `rate-limit-dead` hold completes the shared park in the turn's
  terminal transaction, so the owner Main can run the notice turn. Where WI932 R7's
  standing-reason guard keeps the fence, the attempt waits behind it like any
  queued turn.
- **A6.** R62 v13 supports both R3 shapes. R62 Terms: "Source transition and
  action admission MUST be atomic when they share a transaction. Otherwise a
  durable event cursor and pending evaluation record MUST permit retry without
  losing or duplicating an effect." It keys each effect as "`(org, family_id,
  source_event_id, effect_slot)`, independent of rule text and recipient", and a
  source event carries "committed before/after facts" with "typed relationships"
  supplied by the engine. Today's row-commit rule notices are scheduled inside the
  committing transaction (`wakes.ex`, the rule-notice scheduling path), but that
  path records some notice errors as lifecycle evidence instead of failing, so it
  does not by itself meet R3. An implementation meets R3 only through R62's atomic
  or durable-admission contract.
- **A7.** Exactly three paths emit a hold-resolved event, and each is told apart by
  typed event values alone. In WI932 source, the only callers that emit a
  hold-resolved event are `resolve_open` and `resolve_other_open`:
  - WI932 R7 release (`resolve_recovery_cycle_in_txn` into `resolve_open`):
    `cycleRelease` `true`.
  - Ordinary-turn resolution (`resolve_normal_turn_in_txn` into `resolve_in_txn`
    into `resolve_open`): `cycleRelease` `false`, and the class is never `other`,
    because that path skips `other` holds. The test-facing `HarnessHealth.resolve/2`
    runs the same `resolve_in_txn` and has no gateway route.
  - The `other` resolve command (`harness-health-resolve-other` into
    `resolve_other_open`): `cycleRelease` `false` and class `other`.

  Expiry sets state `expired` and emits no hold-resolved event. A `RateLimitReset`
  fence release, a repair command and an adapter close resolve no hold
  themselves. A hold they free ends only when a later delivered turn resolves it.
  This assumption is falsified if any other path emits a hold-resolved event, if
  the normal-turn path resolves an `other` hold, or if the `other` command resolves
  a hold of another class.

## Invariants

Each requirement gives its basis, then an acceptance example.

### R1. Only a WI932 recovery starts episodes

When WI932 releases a hold, or an ordinary-turn resolution resolves it, the system
SHALL create the notices for that hold through the recovery notice reaction (R3,
R11). Each notice SHALL record the hold id, the failed-route set read at recovery,
and whether the recovery was a release.
The system SHALL recognize a recovery only by a recovery event: a release by the
hold-resolved event's `cycleRelease` being `true`, and an ordinary-turn resolution
by an ordinary-turn recovery event.
The system SHALL NOT read, parse or match the resolution correlation to recognize
either.
The system SHALL NOT create a notice for a hold that opens, or that ends any other
way. This includes the `other` resolve command, expiry, and any hold that ends
with no hold-resolved event.

- *Basis.* Brief: "cite bound WI932 spec ... as the sole recovery definition ...
  add no second detector". Ask: "do not build a second detector". Scope ruling:
  "an outage that ends because an ordinary turn on the held harness succeeds is a
  recovery and must produce the same single Main wake as an outage ended by the
  WI932 hourly release"; "WI932 already resolves harness_health_incident rows on
  normal-turn-success and emits the resolved hold transition. The trigger should
  key on that existing resolved transition, whatever its path." Commissioning
  assignment `asg_d3e63fc4`: tell ordinary successful-turn resolution from other
  non-R7 resolutions only by a raw fact, "without parsing opaque correlation or
  amending WI932". WI932 section 6: hold row events carry "that hold's current
  facts (state, class, constituent routes, fence presence)". WI932 section 6 note:
  "It SHALL be `true` only when R7 releases the hold after a cycle in which every
  constituent route succeeded (R3), and `false` on every other resolution path";
  "No resolution path gains, loses or changes its correlation." Review F1: the v1
  owner+harness scope "lets a success on credential/model B close an episode opened
  by credential/model A". Correction from the commissioning session: "tie the
  recovered event to the same durable outage generation and failed-route set using
  WI932's bound route definition (harness, host, shared account, model), without
  adding a second detector". WI932 ruling: "nothing new is invented for them."
- *Acceptance.*
  - (a) A `rate-limit-dead` hold on Codex has constituents luna, sol and astra,
    and no turn is delivered on that harness and host while it is open. A cycle in
    which only astra succeeds releases nothing and creates no notice. The next
    cycle, in which all three succeed, releases the hold, and its notices are
    created under R3 with the release text (R4(a)).
  - (b) A normal delivered turn resolves a `rate-limit-dead` hold under
    `resolve_normal_turn_in_txn`. Its hold-resolved event carries that turn's
    normal-success correlation, `cycleRelease` `false` and class
    `rate-limit-dead`, so it is an ordinary-turn recovery event, and each affected
    owner gets one notice with the work-resumed text (R4(b)). This is the path real
    Claude hold `hhi_0d41a323-d344-4568-a552-cecb99413115` took at 2026-11-07
    01:02 UTC (resolution observation kind `normal-turn-success`).
  - (c) A Claude reset-time fence release under `RateLimitReset` creates no notice
    by itself. The first turn delivered on that harness and host afterwards
    resolves the hold, and its notices are created as in (b).
  - (d) Hold H on Codex has failed-route set {(codex, host, account A, luna)}. A
    turn on (codex, host, account B, luna) or on (codex, host, account A, sol)
    is delivered while H is open. Under WI932 R3 that success is outside H's set,
    so it is no release, and H's notice never uses the release text. The delivered
    turn does resolve H under the ordinary-turn path, so H's notice is created with
    the work-resumed text, which does not claim that luna answers, and it records
    H's id and the set {luna}.
  - (e) The notice for recovered hold H records H's id and its routes. A later hold
    H2 on the same harness and host never satisfies, completes or reuses H's
    notice.
  - (f) An `other` hold is resolved by `harness-health-resolve-other`. Its
    hold-resolved event carries `cycleRelease` `false` and class `other`. No
    notice exists for it. An `other` hold that expires emits no hold-resolved
    event and gets no notice.
  - (g) An `auth-dead` hold and a `rate-limit-dead` hold are open on the same
    harness and host, both with owner U's sessions as members. One delivered turn
    resolves both. U gets one notice for each hold.

### R2. One notice per episode

When a recovery creates notices, the system SHALL create exactly one notice for
each affected owner of that hold, and none for any other owner.
The system SHALL enforce at most one notice per (hold id, owner) durably.
This is a runtime guarantee and SHALL hold whatever the reaction's TOML states.
If the hold has no affected owner, the system SHALL create no notice.

- *Basis.* Ask: "exactly one due-now Main wake for that episode"; "a durable
  owner+harness outage". Brief: "match the same owner and harness outage".
  Ruling: "One notice per episode (R2/R3) remains a runtime guarantee, not a rail
  duty."
- *Acceptance.*
  - (a) A hold's members are five sessions of owner U and two of owner V. Its
    recovery, by release or by an ordinary-turn resolution, creates one notice for
    (hold, U) and one for (hold, V).
  - (b) A replayed release of the same hold, or a second call of the release
    action in another transaction, finds the hold already resolved under WI932 R7,
    and the uniqueness rule refuses any second (hold, U) notice.
  - (c) The reaction is delivered its source event twice, for example after a
    restart. U still has exactly one (hold, U) notice and one first attempt.
  - (d) An ordinary-turn resolution resolves hold H while a WI932 check cycle for
    H is due. The cycle withdraws under WI932 R1, H emits no second hold-resolved
    event, and U has exactly one (H, U) notice.

### R3. A recovery neither loses nor doubles its notices

When a recovery commits under a composition that elects the recovery notice
reaction, the system SHALL create each affected owner's notice exactly once, even
if the gateway stops at any point between the recovery and the notices' creation.
If the recovery does not commit, the system SHALL create no notice.
The system SHALL write each notice and its first attempt or `awaiting_main` state
in one transaction.
The implementer MAY create a release's notices in the release transaction, or
afterwards from its durably admitted recovery event. Where the notices are written
in the release transaction and a notice write fails, the release SHALL roll back
and the hold SHALL stay open for WI932's next cycle.
For an ordinary-turn resolution, a failure to create a notice SHALL NOT fail, roll
back or change the delivered turn or the hold's resolution, and the notices SHALL
still be created exactly once.

- *Basis.* Ask: "recovery produces exactly one due-now Main wake". Review F2: a
  notice must not be lost between the recovery and the wake. Ruling: "The author
  decides how the reaction and the notice row commit relative to release, within
  that invariant." WI932 section 7 keeps "normal delivered-turn resolution"
  unchanged, and R6 forbids changing existing turn semantics, so a notice failure
  cannot undo a delivered turn.
- *Acceptance.*
  - (a) A fault injected before the release commits leaves the hold open, its fence
    present, and no notice or attempt wake. The next successful cycle produces the
    release and one notice per affected owner.
  - (b) The gateway stops at the latest point the implementation allows between the
    release commit and notice creation. After start, each affected owner has
    exactly one notice and one first attempt or `awaiting_main` state. A second
    restart, with no attempt turn running in between, creates no further notice or
    attempt. This case tests replay of the source event; an attempt interrupted
    while running is governed by R5(b) and R6.
  - (c) A fault is injected into notice creation for an ordinary-turn resolution.
    The turn stays `delivered`, its assistant messages stay recorded, the hold
    stays resolved. When the fault is removed, each affected owner ends with
    exactly one notice.
    The same holds when the gateway stops between the turn's commit and notice
    creation.

### R4. The attempt is one due-now Main prompt with fixed content

When a notice starts an attempt, the system SHALL deliver one prompt to the owner
Main, due at the moment the attempt starts, with class `blocker` and origin
`process:tightbeam`.
The prompt SHALL contain one of these texts, with the bracketed fields filled from
the hold. Every attempt of a notice SHALL use the same text.

(a) Release text, when the notice's recovery was a release:

> The `<harness>` harness on `<host>` recovered from a `<failureClass>` outage.
> Hold `<holdId>` opened at `<openedAt>` and was released at `<releasedAt>` after
> every affected model route (`<routes>`) answered in one check. `<memberCount>` of your
> sessions were held. Use your installed and learned Kung Fu to find live agents
> whose work stalled on this harness and host, and resume only those agent
> graphs. Do not wake or resume unrelated agents.

(b) Work-resumed text, when the notice's recovery was an ordinary-turn resolution:

> Work resumed on the `<harness>` harness on `<host>` after a `<failureClass>`
> outage. Hold `<holdId>` opened at `<openedAt>` and was resolved at
> `<resolvedAt>` when a turn on this harness succeeded. This does not mean every
> model route on this harness is back. `<memberCount>` of your sessions were held.
> Use your installed and learned Kung Fu to find live agents whose work stalled on
> this harness and host, and resume only those agent graphs. Do not wake or resume
> unrelated agents.

The system MAY append neutral correlation facts such as the notice id and attempt
number. It SHALL NOT shorten, move or replace any sentence of the chosen text.
The texts are the reaction's fixed texts. The class, due time and origin are runtime
behavior, not reaction options.

- *Basis.* Ask: "one due-now Main wake"; "Main uses installed Kung Fu to inspect
  and resume only work stalled on that harness; Tightbeam neither selects nor
  broadcasts to product agents." OAuth: the prompt text is a contract and a
  reference to standing guidance does not satisfy it. Ruling: "no notification
  options beyond trigger, target and fixed R4 text". Scope ruling: "The
  ordinary-path wake text must say work resumed on the harness, not that every
  route is back."
- *Acceptance.*
  - (a) For a released Codex hold with seven members of owner U, U's owner Main
    receives one turn whose prompt contains every sentence of the release text
    with the hold's values. No other session receives a prompt caused by the
    release.
  - (b) For a Codex hold with seven members of owner U, resolved by a delivered
    turn on model sol, U's owner Main receives one turn whose prompt contains
    every sentence of the work-resumed text with the hold's values, and no sentence
    saying that every route answered. No other session receives a prompt caused by
    the recovery.
  - (c) That notice's first attempt fails and attempt 2 starts under R6. Attempt
    2's prompt carries the work-resumed text again.

### R5. A notice is complete only when delivered

The system SHALL set a notice to `delivered` only when a turn carrying its current
attempt reaches terminal status `delivered` on an owner Main.
Inserting the wake, admitting the prompt or starting the turn SHALL NOT complete
the notice.

- *Basis.* Review F2: v1 "closes the episode with wake insertion, but normal
  delivery can suppress a Main that retires before delivery". Ask: "If Main cannot
  be reached, preserve evidence and a retryable notice." Brief: "retain a durable
  retry if Main is unreachable rather than completing at wake insertion". Review 2
  B1: "Distinguish a queued attempt that survives restart from an interrupted
  running attempt", preserving existing turn semantics. Review 2: "Settlement must
  use that supported correlation; direct `turns.wakeId == sourceWakeId` alone is
  insufficient."
- *Acceptance.*
  - (a) A queued attempt survives restart. An attempt's wake is pending, or its
    attempt turn is queued and not running. The gateway stops and starts. The
    notice is still `attempting` and links that wake and turn, and no second
    attempt starts. When that turn ends `delivered`, the notice becomes
    `delivered`.
  - (b) An interrupted attempt is settled at boot. Attempt 1's turn is running on
    U's Main when the gateway stops. On start, `Ledger.recover_running` ends that
    turn `failed_unknown`. In the same transaction the notice becomes
    `awaiting_main` with outcome `failed_unknown`, and its lifecycle evidence
    names attempt 1, its wake and the turn. The startup retry pass that follows
    (R6 signal 3) starts attempt 2 once. The old turn stays `failed_unknown` and is
    not retried. When attempt 2's turn ends `delivered`, the notice becomes
    `delivered`.
  - (c) Attempt 1's wake is delivered inside a notice batch whose carrier wake owns
    the turn. When that turn ends `delivered`, the notice becomes `delivered`,
    found through the attempt wake's `deliveredTurnSeq`.

### R6. A non-delivered outcome keeps the notice and retries on existing signals

When an attempt has a non-delivered outcome, the system SHALL record that outcome
on the notice, set the notice to `awaiting_main`, and keep it, in the transaction
that records the outcome. This includes boot recovery's `failed_unknown`
terminalization of an interrupted attempt.
While a notice is `awaiting_main`, the system SHALL start one new attempt on the
first of these signals:

1. a session for the notice's owner enters `kind = 'main'` and
   `state = 'active'`;
2. a turn on the owner Main ends `delivered`, and that turn did not carry this
   notice;
3. the gateway starts, if an owner Main exists. This pass SHALL run after boot
   recovery has settled interrupted attempts, so a notice settled at boot gets its
   one startup attempt.

A notice SHALL have at most one outstanding attempt.
The system SHALL NOT retry on a timer and SHALL NOT add a retry policy beyond these
three signals.
The system SHALL NOT change existing turn semantics to serve a retry: a terminal
attempt turn is never re-run, and each retry is a new attempt with a new wake.

- *Basis.* Ask: "preserve evidence and a retryable notice ... do not build ... a
  general retry engine." Review F2. OAuth: when Main retires before delivery, the
  ordinary target gate suppresses the turn; without a durable retry the notice is
  gone.
- *Acceptance.*
  - (a) Release happens while owner U has no active Main. U's notice is
    `awaiting_main` with outcome `no_owner_main`, and no wake exists. When a Main
    for U becomes active, one attempt starts and its prompt reaches that Main.
  - (b) U's Main retires after the attempt's wake is inserted and before delivery.
    The scheduler cancels the wake as `target_unresolvable`. The notice becomes
    `awaiting_main` with that outcome. No second wake exists until a retry signal
    occurs. The same holds when retirement cancels the wake as `target_retired`.
  - (c) The attempt's turn on U's Main ends `failed`. The notice becomes
    `awaiting_main`. U's Main later completes an unrelated delivered turn, and
    attempt 2 starts once.
  - (d) The gateway restarts while U's notice is `awaiting_main` and U's Main is
    active. Attempt n+1 starts once, not once per missed signal.

### R7. A deliberate cancellation ends the notice

When an attempt's wake has a deliberate cancellation, the system SHALL set the
notice to `canceled`, record the canceller and reason, and start no further
attempt.
Cancellation SHALL NOT be treated as a recall. If the attempt's text was already
sealed into a notice batch and that batch is delivered, the system SHALL record a
lifecycle event naming the delivered turn and SHALL leave the notice `canceled`.

- *Basis.* Ask: "exactly one due-now Main wake for that episode". A person or Main
  that withdraws the prompt has disposed of it; retrying would override that
  choice. Review 2: current batch cancellation "records cancellation after seal
  without removing the included text ... R7 should not be presented as guaranteed
  recall".
- *Acceptance.*
  - (a) U cancels the pending attempt wake with `cancel-wake`. The notice becomes
    `canceled`. A later delivered turn at U's Main starts no attempt.
  - (b) U cancels an attempt wake after it was sealed into a batch. The batch is
    delivered with the prompt text. The notice stays `canceled`, a lifecycle event
    names the delivered turn, and no further attempt starts.

### R8. After an episode ends, later events do nothing; a new hold is a new episode

While a notice is `delivered` or `canceled`, the system SHALL take no further
delivery or retry action for it. R7's lifecycle event for late delivery of sealed
text is evidence, not an action.
When a later hold on the same harness and host recovers, the system SHALL treat
it as new episodes under R1 and R2.

- *Basis.* Ask: "Later success does nothing; a new outage is a new episode."
- *Acceptance.*
  - (a) After U's notice is `delivered`, fifty delivered turns on the recovered
    harness create no notice, attempt or wake.
  - (b) An ordinary-turn resolution creates U's notice for hold H. The next fifty
    delivered turns on that harness and host find no open hold, resolve nothing
    and create no notice.
  - (c) A new `rate-limit-dead` hold on the same harness and host opens next day
    and recovers. U receives exactly one new notice keyed by the new hold id.

### R9. Tightbeam selects no product agent

The system SHALL deliver recovery notices only to owner Mains.
It SHALL NOT enumerate, prompt, wake or resume any other session because of a
recovery, beyond what WI932 R7 and its ordinary-turn resolution already do.

- *Basis.* Ask: "Tightbeam neither selects nor broadcasts to product agents."
- *Acceptance.* A recovery, by release or by an ordinary-turn resolution, with
  members across 40 sessions of one owner creates exactly one prompt from this
  contract, at that owner's Main. WI932's own redelivery and lane starts are
  unchanged and counted separately.

### R10. Evidence is durable and the notice row is the decision state

The system SHALL record a lifecycle event with principal `process:tightbeam` for
each of: notice created, attempt started, non-delivered outcome, delivered and
canceled. Each event SHALL carry the hold id, owner, attempt number, wake id and
turn sequence where known.
The system SHALL decide notice behavior from the notice row only, never from
lifecycle text.

- *Basis.* Ask: "preserve evidence". v1 Law 7, rated satisfied by Review.
- *Acceptance.* For case R6(b), the lifecycle log shows created, attempt 1 started,
  non-delivered `target_unresolvable`, then later attempt 2 started and delivered,
  all naming the same hold and owner. Deleting those lifecycle rows in a test copy
  does not change the notice's next action.

### R11. The notice policy is a default reaction in the base seed

The base seed composition SHALL contain the recovery notice reaction, elected by
default, so that the default composition gives R1 to R10 behavior with no setup.
The reaction SHALL state only:

- its trigger: a recovery event, that is a hold-resolved event matching
  `{"op":"or","args":[{"op":"eq","args":[{"ref":"event.cycleRelease"},true]},{"op":"and","args":[{"op":"eq","args":[{"ref":"event.after.state"},"resolved"]},{"op":"eq","args":[{"ref":"event.cycleRelease"},false]},{"op":"ne","args":[{"ref":"event.after.failureClass"},"other"]}]}]}`
  (WI932 section 6 and its note, R7, A7), using the existing `or`, `and`, `eq` and
  `ne` operations over the event's typed values;
- its target: the owner Main of each affected owner;
- the two R4 texts, with R4(a) chosen when the event's `cycleRelease` is `true`
  and R4(b) otherwise.

The reaction SHALL add no rail setting, rail-language feature, per-owner setting or
notification option beyond those three, apart from the identity and translation
every R62 reaction carries.
Notice uniqueness, delivery tracking, settlement, retry, class and timing SHALL be
runtime behavior and SHALL NOT be configurable from TOML.
The runtime SHALL contain no compiled copy of the reaction. With the reaction
removed from a composition, a release or an ordinary-turn resolution SHALL proceed
under WI932 and SHALL create no notice.
WI932's release effect and its ordinary-turn resolution SHALL send nothing, and
WI932's reactions and translation SHALL stay unchanged, including "No message goes
to any agent or person."
The reaction SHALL have a linked plain-English translation stating trigger;
conditions; effect and recipient; timing, repetition and stop; owning bundle; and
intentional change.

- *Basis.* Ruling: "The Main recovery notice belongs in the existing TOML rail as a
  reaction in the base seed composition, on by default and triggered by WI932's
  release of a held harness, over generic runtime mechanics: durable notice and
  attempt state, settlement and the R6 retry signals." Ruling: "WI932's own release
  effect keeps its meaning and sends nothing; the notice is a separate reaction to
  it." Ruling: "Rail placement adds no new configurability: no per-owner settings,
  no new rail-language features and no notification options beyond trigger, target
  and fixed R4 text." PO: "Policy electing eligible holds, timing, suppression,
  recovery and notification belongs in configurable TOML rails." WI932 section 8:
  base seed reactions follow R62's no-compiled-fallback rule and carry an English
  translation. Ask: "do not build a second detector or general retry engine", so
  retry is fixed, not a policy knob. Scope ruling: "The trigger should key on that
  existing resolved transition, whatever its path"; "The ordinary-path wake text
  must say work resumed on the harness, not that every route is back."
- *Acceptance.*
  - (a) A new org with the default composition and no configuration has a WI932
    release of a hold whose members belong to owners U and V. U's Main and V's Main
    each get exactly one delivered notice.
  - (b) With the reaction removed from the composition, a WI932 release resolves
    the hold, removes the fence and redelivers intents exactly as WI932 R7 says,
    and a normal delivered turn resolves another hold as WI932 section 7 keeps it.
    No notice, attempt or wake from this contract exists for either.
  - (c) A hold resolved by a normal delivered turn emits a hold-resolved event whose
    resolution correlation is that turn's normal-success correlation, whose
    `cycleRelease` is `false` and whose class is `rate-limit-dead`. The reaction
    fires, and each affected owner gets one notice with the R4(b) text.
  - (d) WI932's section 5 translation reads the same before and after this feature
    lands, and neither WI932's release reaction nor its ordinary-turn resolution
    writes a wake or prompt.
  - (e) The reaction's TOML holds its trigger, its target and the two R4 texts, and
    no other field beyond the identity and translation every R62 reaction carries.
  - (f) An `other` hold is resolved by `harness-health-resolve-other`. Its
    hold-resolved event carries `cycleRelease` `false` and class `other`. The
    reaction does not fire and no notice exists. The reaction's trigger contains no
    reference to the resolution correlation.
  - (g) A hold opens. Its opened event carries `cycleRelease` `false` and state
    `open`. The reaction does not fire and no notice exists.
  - Cases (a), (c), (f) and (g) SHALL exercise the same trigger, each on its own
    hold, and differ only in the event's typed `cycleRelease`, state and class.
    Each event's resolution correlation is what its path records under WI932
    section 6, unchanged by this contract.

## Default recovery notice reaction, in plain English

| Field | Value |
|---|---|
| Trigger | A harness-health hold resolves. |
| Conditions | The hold-resolved event says it is a cycle release (`cycleRelease` is true), which happens only when a check cycle in which every constituent route succeeded releases the hold; or the hold is resolved, is not a cycle release and is of any class other than "other", which happens only when an ordinary turn on that harness and host succeeds. An "other" hold resolved by its own command gets nothing, a hold that expires gets nothing, and an opened hold never qualifies. |
| Effect / recipient | For each owner whose sessions were held, one prompt to that owner's Main. A cycle release uses the fixed recovery text; an ordinary-turn resolution uses the fixed work-resumed text, which says work resumed and does not claim every route is back. No other agent or person receives anything. |
| Timing / repetition / stop | Due at once on recovery. If it does not reach a delivered Main turn, it waits and is tried again when that owner's Main becomes active, when that Main completes another turn, or when the gateway starts. Stops when delivered or deliberately canceled. No timer. These are runtime behavior, not reaction settings. |
| Owning bundle | Substrate base seed, on by default. |
| Intentional change | New behavior. Previously no prompt went to any Main when a held harness recovered. |

## Architecture

This section names the existing seams. The exact shape is the implementer's
choice within the invariants.

Policy is the reaction's trigger, target and text; the runtime pieces below carry
the delivery guarantees and no other policy.

| Piece | Need | Serves |
|---|---|---|
| Recovery notice reaction | One reaction and its plain-English translation in the base seed composition, elected by default and keyed as R62 v13 requires (org, family, source event, slot). | R11 |
| Recovery event interface | The reaction's trigger reads the typed values that WI932 r5 section 6 puts on hold row events: `cycleRelease`, and the hold snapshot's state and class (`after.state`, `after.failureClass`), with the existing `eq`, `ne`, `and` and `or` operations. It fires on a release event or an ordinary-turn recovery event. The trigger does not read, parse or match the resolution correlation. This contract adds no field, marker, record or rail-language operation. | R1, R4, R11 |
| Owner-Main target | For each affected owner, read from the hold's member rows, resolve that owner's Main by the existing owner-Main selection. No Main is a non-delivered outcome, not an error. | R2, R6, R9 |
| Tracked notice | One additive table keyed (holdId, ownerUserId) with state, attempt number, current wake id, current turn sequence, last outcome and timestamps. The key enforces R2. Empty on upgrade. Its only consumer is the recovery notice reaction. | R2, R3, R5, R6, R10 |
| Attempt start | Deliver the R4 prompt to the owner Main in the caller's transaction, as the "other" route does with `Gateway.deliver_prompt_in_txn` and a deterministic wake id. | R4, R6 |
| Turn settlement | Wherever a terminal transition already reaches `HarnessHealth.settle_other_route_in_txn`, also settle a notice attempt in the same transaction. That covers the `SessionLane` terminal transitions, the post-delivery `reconcile_delivered_turn`, and boot recovery in `Ledger.recover_running`. Find the attempt turn through the attempt wake's `deliveredTurnSeq`, which batching sets on each source wake. | R5, R6 |
| Wake cancellation | When an attempt's wake is canceled, whether by `Wakes.undeliverable_delivery_in_txn`, retirement or a requester, classify the reason as a non-delivered outcome or a deliberate cancellation in the same transaction. | R6, R7 |
| Retry signals | Owner Main activation, an owner Main delivered turn, and the gateway start pass in `LaneManager.init` that already runs `HarnessHealth.resume_other_routes` after `Ledger.recover_running`. Each starts at most one attempt per `awaiting_main` notice. | R6 |

Superseded mechanisms. The v1 `harness_recovery_episodes` table, its normal-turn
trigger, and the classifier `HarnessRecovery.unavailable?/1` in source commits
`ffb915e661864a37d3bf5efb77bc8c58fb5d6e8c`, `d1201ffe` and `9187c283d24f` are a
second detector under this contract. They are not to be ported.

Compatibility and deletion. The table is additive. Existing turns, wakes, holds
and "other" routes keep their meaning. WI932's release action, normal-turn
resolution, reactions and translation keep their meaning, and neither its release
nor its normal-turn resolution sends anything; the notice is a separate reaction to
their hold-resolved events. No notice is backfilled for holds released
or resolved before the feature lands. Deleting the feature removes the recovery
notice reaction, the settlement and signal hooks, and the schema registration. Historical
notice and wake rows remain readable.

## Acceptance

### A1. Outage specimens are real captures

Tests that open the hold SHALL drive the existing classifier with captured real
failure projections. Each fixture SHALL carry its provenance: source record id,
observed time, harness, failure class, and the captured `reason` projection
without host or session identifiers. Hand-written shapes SHALL NOT stand in for
them.

- *Basis.* Review F4: labels and informal shapes "lack exact captured-real
  fixtures/provenance". This contract adds no classifier, so the specimens test
  only that a real outage opens the hold whose recovery R1 observes.
- *Specimens.*

  | Id | Harness | Source record | Observed | Captured `reason` projection |
  |---|---|---|---|---|
  | C1 | codex | `hho_bd254f96-37f5-4105-b9e2-32cf95b4436d` | 2026-11-05 05:05:40 UTC | `{"code":-32603,"data":{"codexErrorInfo":"usageLimitExceeded","message":"You’ve hit your usage limit. Visit https://chatgpt.com/settings/usage to purchase more credits or try again at Nov 8th, 2026 4:03 PM."},"message":"Internal error"}` |
  | C2 | claude | `hho_4d9d4b68-0388-4705-8142-9356ac553dd4` | 2026-11-06 16:52:57 UTC | `{"code":-32603,"data":{"errorKind":"rate_limit"},"message":"Internal error: You've hit your weekly limit · resets Nov 10, 6am (UTC)"}` |
  | S1 | codex | fixture `test/fixtures/harness_recovery/codex-usage-limit-s1.json` at source `9187c283d24f`, SHA-256 `5831185462e8e07807270be55e152c2e0e9feed56b967e7b8928e6c46452fe82` | turns 9136–9184 | `{"code":-32603,"message":"Internal error","data":{"codexErrorInfo":"usageLimitExceeded"}}` |

  C1 and C2 are observation rows classified `rate-limit-dead` by release
  `0.1.14`. They were read from the live store read-only on 2026-11-07. Their
  `cause` field records `stage=prompt reason=<projection>`. S1's source artifact
  `art_054cb5af` (content SHA-256
  `f8ec787572c32922d04a431a713f9634131eeef4e79828728c99930df5b66e88`) has no
  stored content, so S1 can be checked only against its fixture hash. C1 and C2 are
  the primary specimens.

### A2. Behavioral cases

Each R1–R11 acceptance example SHALL be a behavioral test through the
repository's canonical wrapper on an isolated test host. The WI932 check outcomes
that drive release MAY be synthetic, as WI932 section 12 allows for release logic.
Ordinary-turn cases SHALL drive a turn to `delivered` through the existing turn
path in the test harness, so WI932's own normal-turn resolution resolves the hold.
The tests SHALL use the real specimens in A1 to open holds. The restart cases in
R5 SHALL run the real boot path (`LaneManager.init` with `Ledger.recover_running`)
rather than skipping it.

This contract makes no provider call and adds no real-response evidence of its
own. Section 12 ruling: WI932's real provider responses are tested "after merge"
on the exact integrated build, and "WI932 stays unaccepted until the integrated
build has one genuine succeeded and one genuine failed or inconclusive response
for each of Claude and Codex on a permitted test host." That evidence stays
required before WI932 acceptance, release or installation, and so before A3. The
integration target is still an open decision (`dr_273844d9`). This contract does
not choose it.

### A3. Installed-release evidence

The work item's done condition is outside this spec's acceptance: "Done only when
an installed release has real recovered-outage evidence of one Main wake." That
evidence is one real recovered hold, by release or by ordinary-turn resolution,
its notice rows and lifecycle events, and one delivered Main turn carrying the R4
text for that path.

## Spec homing

The canonical contract lives only in the `tightbeam-specs` repository as
`harness-recovery-main-wake-v2.md`. It supersedes `harness-recovery-main-wake-v1.md`
at commits `73aec01d7331e08b148994d6525ff75c2b00e137` and
`0860144059f1`. Neither revision is on the main line, and neither may land.
Its coupled authority is WI932 `held-harness-hourly-recovery-r5.md` at the SHA-256
named above, held outside this repository. A change to WI932's release action,
normal delivered-turn resolution, eligibility, Terms, hold-resolved event, hold
snapshot state or class, resolution correlation or `cycleRelease` requires
re-review of this contract. Recon documents, review
reports, artifact rows and transcripts are evidence, not canonical custody.

## Open Questions

- **Q1 (RESOLVED by Ruling `att_5172407a`): where the notification policy lives.**
  It is a separate reaction in the base seed composition's TOML rails, on by
  default and triggered by WI932's release (R11). WI932's release sends nothing.
  One notice per episode is a runtime guarantee (R2, R3).
- **Q2 (RESOLVED by Scope ruling `art_0f65a7ef`): holds resolved by a normal
  turn.** An outage that ends because an ordinary turn on the held harness
  succeeds is a recovery and gets the same single Main notice (R1, R4(b), R11).
  This supersedes `att_5172407a`'s acceptance of the earlier no-notice default and
  the scope limit in `att_67b4a3de`. Review F1 stays answered: the ordinary-turn
  text says only that work resumed, and each notice records its own hold and
  failed-route set (R1 acceptance (d)).
- **Q3 (NON-BLOCKING): an owner with no Main for a long time.** Default: the notice
  waits in `awaiting_main` with its evidence, and nothing is escalated. The
  harness-health "other" path files a `user-alerted` fact when no Main exists; this
  contract does not, because the ask does not request it.
- **Q4 (NON-BLOCKING): owners whose held sessions had no stalled work.** Default:
  every affected owner is notified, because the fence held all their sessions on
  that harness and host, and Main judges what stalled.

- **Q5 (RESOLVED by WI932 r5 and Cycle release ruling `att_05b91e15`): how the
  reaction tells a WI932 release from other resolutions.** WI932 r3's resolution
  correlation alone could not discriminate: a rail can only compare it, and its
  release form is opaque and unfixed (gap report `art_3212fbdd`). WI932 r5
  section 6, bound at the SHA-256 named above, adds the typed boolean
  `cycleRelease`, `true` only in R7's resolving transaction after every
  constituent route succeeded and `false` on every other path, including opened
  events. Correlations are unchanged. R1, R3, R11 and the plain-English table use
  `cycleRelease` as the only discriminator (Release event in Terms), through the
  existing `eq` operation. Ordinary-turn recovery is told apart from the `other`
  resolve command by the typed hold state, class and `cycleRelease` that WI932 r5
  section 6 already carries (A7), not by the correlation. This contract does not
  amend WI932.
- **Q6 (NON-BLOCKING): which classes the ordinary-turn path covers.** Default:
  every class WI932's normal-turn path resolves, that is every class except
  `other`, because the Scope ruling keys on "that existing resolved transition,
  whatever its path". `other` holds are excluded because they end by their own
  resolve command or expiry and keep their own review routes. A read-only query of
  the live store on 2026-11-07 found, among holds opened in the prior 30 days,
  128 non-`other` holds resolved by a normal turn (46 `rate-limit-dead`, 51
  `adapter_unavailable`, 16 `interrupted-outcome-unknown`, 13 `auth-dead`, 2
  `task_crash`), so the default wakes Main for every class, not only rate limits.
  Narrowing to `rate-limit-dead` would be one added clause in the trigger. The PO
  confirms or narrows this at the spirit judgment.

No question is BLOCKING.
