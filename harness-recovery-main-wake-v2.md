# Harness recovery Main wake v2

Status: DRAFT for independent spec review. Not bound to the work item.

Governing work item: `wi_3bb2ea6c-9cab-4e85-9981-676c4b32c3b6`, row version
`1794025310655`. Commissioned by assignment
`asg_f853bd5b-cbf4-4c89-b2be-fceec27d1cfc`.

This revision answers changes-requested review `att_92d397fe` of
`harness-recovery-main-wake-v1.md` at commit
`73aec01d7331e08b148994d6525ff75c2b00e137` (SHA-256
`40654018a7ec353c393e2ea8230e3ecdc2aed3a6ecc0b3c99e49de1783960aea`), and
changes-requested review `att_5284b34e` (report `art_74107a30`) of this file at
commit `c396aced` (SHA-256
`b24d4fe1601fe8764f1f28f068bb8724b2b80a85efa2fbf4b2a4184801356b4d`). It changes
design only. It authorizes no source edit, test run, integration target, release,
installation or live action.

Normative keywords follow RFC 2119 as clarified by RFC 8174. Requirement
sentences use EARS.

Basis labels used below:

- **Ask** quotes the work item body.
- **Review** quotes `att_92d397fe`.
- **Review 2** quotes `att_5284b34e` and its report `art_74107a30`.
- **PO** quotes the WI932 PO intent and topology judgment `art_4bd40c7a` as WI932
  R9 quotes it.
- **WI932** cites the bound held-harness contract
  `held-harness-hourly-recovery.md`, work item
  `wi_93269dbf-9c94-43f9-a8f6-c6e82dfebf87`, SHA-256
  `85a1e07c6eb353d1ec86628926c4f3274195ada3d447efc2720698c5a535b7d0`.
- **OAuth** cites `spec-oauth-recovery-main-prompt-v2.md` in this repository.
- **Brief** quotes the commissioning assignment.

## Spirit

Sources relied on:

- The work item body, row version `1794025310655`: "after a durable owner+harness
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

The intent this contract serves: when a harness outage ends, the person who owns
the stalled work should not have to notice it. Their Main is told once, with
enough to act, and decides what to resume. Tightbeam reports a fact. It does not
choose which product agents matter.

## Goal

When WI932 releases a held harness, each owner whose sessions were held receives
exactly one due-now prompt at their Main. The prompt counts as sent only when it
reaches a delivered Main turn. Until then it stays durable and is retried on a
narrow set of existing signals.

"One wake" means one logical notice per episode, of which at most one attempt
reaches a delivered Main turn. Failed attempts stay as evidence. An attempt whose
outcome is unknown may have reached Main before it was interrupted, so Main can
see the prompt again on retry; Main judges live state, and this contract adds no
idempotency mechanism.

## Non-Goals

- A second outage or recovery detector. No classifier, episode detector, success
  observer or probe beyond WI932's.
- Recovery notices for holds resolved by any path other than the WI932 release
  action (see Q2).
- Choosing, enumerating, waking or resuming product agents.
- A general retry engine, a retry timer or exponential backoff. The retry behavior
  in R5 and R6 is fixed and serves only recovery notices.
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
  the hold's linked terminal-failure evidence, read at release time (WI932 R3).
- **Outage generation.** One hold id. A hold that opens after an earlier one on the
  same harness and host closed is a new generation, even for the same routes.
- **Release.** WI932 R7: the single transaction in which a successful check cycle
  resolves an eligible hold. Under the WI932 seed rail only `rate-limit-dead`
  holds are eligible, and release requires that every constituent route succeeded
  in one cycle (WI932 R2, R3).
- **Recovered outage.** A hold that ended by release. Nothing else is a recovered
  outage for this contract.
- **Affected owner.** A distinct non-null `sessions.ownerUserId` of a session in the
  hold's `harness_health_members` rows, read in the release transaction.
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
  WI932 R7 the fence is removed in the release transaction, so the owner Main can
  run the notice turn. Where WI932 R7's standing-reason guard keeps the fence, the
  attempt waits behind it like any queued turn.
## Invariants

Each requirement gives its basis, then an acceptance example.

### R1. Only a WI932 release starts episodes

When WI932 releases a hold, the system SHALL create the notices for that hold in
the release transaction. Each notice SHALL record the hold id and the failed-route
set that the release covered.
The system SHALL NOT create a notice for a hold resolved or ended any other way.
This includes normal delivered-turn resolution, `RateLimitReset` fence release,
repair resume, adapter close, expiry and "other" review.

- *Basis.* Brief: "cite bound WI932 spec ... as the sole recovery definition ...
  add no second detector". Ask: "do not build a second detector". Review F1: the
  v1 owner+harness scope "lets a success on credential/model B close an episode
  opened by credential/model A". WI932 R3 requires success on every constituent
  route in one cycle, so one route's success cannot end the outage. Correction
  from the commissioning session: "tie the recovered event to the same durable
  outage generation and failed-route set using WI932's bound route definition
  (harness, host, shared account, model), without adding a second detector".
- *Acceptance.*
  - (a) A `rate-limit-dead` hold on Codex has constituents luna, sol and astra. A
    cycle in which only astra succeeds releases nothing and creates no notice. The
    next cycle, in which all three succeed, releases the hold and creates its
    notices in the same transaction.
  - (b) A normal delivered turn resolves a `rate-limit-dead` hold under
    `resolve_normal_turn_in_txn`. No notice exists for that hold. This is the path
    real Claude hold `hhi_0d41a323-d344-4568-a552-cecb99413115` took at
    2026-11-07 01:02 UTC (resolution observation kind `normal-turn-success`).
  - (c) A Claude reset-time fence release under `RateLimitReset` creates no notice.
  - (d) Hold H on Codex has failed-route set {(codex, host, account A, luna)}. A
    turn on (codex, host, account B, luna) or on (codex, host, account A, sol)
    succeeds while H is open. Under WI932 R3 that success is outside H's set, so H
    is not released and no notice exists for H.
  - (e) The released notice for hold H records H's id and its routes. A later hold
    H2 on the same harness and host never satisfies, completes or reuses H's
    notice.

### R2. One notice per episode

When a release creates notices, the system SHALL create exactly one notice for
each affected owner of that hold, and none for any other owner.
The system SHALL enforce at most one notice per (hold id, owner) durably.
If the hold has no affected owner, the system SHALL create no notice.

- *Basis.* Ask: "exactly one due-now Main wake for that episode"; "a durable
  owner+harness outage". Brief: "match the same owner and harness outage".
- *Acceptance.*
  - (a) A hold's members are five sessions of owner U and two of owner V. Release
    creates one notice for (hold, U) and one for (hold, V).
  - (b) A replayed release of the same hold, or a second call of the release
    action in another transaction, finds the hold already resolved under WI932 R7,
    and the uniqueness rule refuses any second (hold, U) notice.

### R3. Release and notice commit together

The system SHALL commit the hold release, every notice it creates, and each
notice's first attempt or `awaiting_main` state in one transaction.
If any notice write fails, the release SHALL roll back and the hold SHALL stay open
for WI932's next cycle.

- *Basis.* Ask: "recovery produces exactly one due-now Main wake". Review F2: a
  notice must not be lost between the recovery and the wake. WI932 R7 puts release
  in one transaction.
- *Acceptance.* A fault injected after the notice insert and before commit leaves
  the hold open, its fence present, and no notice or attempt wake. The next
  successful cycle produces the release and one notice per affected owner.

### R4. The attempt is one due-now Main prompt with fixed content

When a notice starts an attempt, the system SHALL deliver one prompt to the owner
Main, due at the moment the attempt starts, with class `blocker` and origin
`process:tightbeam`.
The prompt SHALL contain this text, with the bracketed fields filled from the
hold:

> The `<harness>` harness on `<host>` recovered from a `<failureClass>` outage.
> Hold `<holdId>` opened at `<openedAt>` and was released at `<releasedAt>` after
> every affected model route (`<routes>`) answered in one check. `<memberCount>` of your
> sessions were held. Use your installed and learned Kung Fu to find live agents
> whose work stalled on this harness and host, and resume only those agent
> graphs. Do not wake or resume unrelated agents.

The system MAY append neutral correlation facts such as the notice id and attempt
number. It SHALL NOT shorten, move or replace any sentence above.

- *Basis.* Ask: "one due-now Main wake"; "Main uses installed Kung Fu to inspect
  and resume only work stalled on that harness; Tightbeam neither selects nor
  broadcasts to product agents." OAuth: the prompt text is a contract and a
  reference to standing guidance does not satisfy it.
- *Acceptance.* For a released Codex hold with seven members of owner U, U's owner
  Main receives one turn whose prompt contains every sentence above with the hold's
  values. No other session receives a prompt caused by the release.

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
action for it.
When a later hold on the same harness and host is released, the system SHALL treat
it as new episodes under R1 and R2.

- *Basis.* Ask: "Later success does nothing; a new outage is a new episode."
- *Acceptance.*
  - (a) After U's notice is `delivered`, fifty delivered turns on the recovered
    harness create no notice, attempt or wake.
  - (b) A new `rate-limit-dead` hold on the same harness and host opens next day
    and is released. U receives exactly one new notice keyed by the new hold id.

### R9. Tightbeam selects no product agent

The system SHALL deliver recovery notices only to owner Mains.
It SHALL NOT enumerate, prompt, wake or resume any other session because of a
release, beyond what WI932 R7 already does.

- *Basis.* Ask: "Tightbeam neither selects nor broadcasts to product agents."
- *Acceptance.* A release with members across 40 sessions of one owner creates
  exactly one prompt from this contract, at that owner's Main. WI932's own
  redelivery and lane starts are unchanged and counted separately.

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

## Architecture

This section names the existing seams. The exact shape is the implementer's
choice within the invariants.

Where the notification policy lives is open (Q1, BLOCKING). Only the notice
creation row depends on that answer; the other rows hold under either answer.

| Piece | Need | Serves |
|---|---|---|
| Notice creation | In the release transaction, after WI932 resolves the hold: read affected owners, insert notices, and start each first attempt or set `awaiting_main`. Its placement, and any policy or WI932 change it needs, waits on Q1. | R1, R3 |
| Notice table | One additive table keyed (holdId, ownerUserId) with state, attempt number, current wake id, current turn sequence, last outcome and timestamps. Empty on upgrade. | R2, R5, R6, R10 |
| Attempt start | Deliver the R4 prompt to the owner Main in the caller's transaction, as the "other" route does with `Gateway.deliver_prompt_in_txn` and a deterministic wake id. | R4, R6 |
| Turn settlement | Wherever a terminal transition already reaches `HarnessHealth.settle_other_route_in_txn`, also settle a notice attempt in the same transaction. That covers the `SessionLane` terminal transitions, the post-delivery `reconcile_delivered_turn`, and boot recovery in `Ledger.recover_running`. Find the attempt turn through the attempt wake's `deliveredTurnSeq`, which batching sets on each source wake. | R5, R6 |
| Wake cancellation | When an attempt's wake is canceled, whether by `Wakes.undeliverable_delivery_in_txn`, retirement or a requester, classify the reason as a non-delivered outcome or a deliberate cancellation in the same transaction. | R6, R7 |
| Retry signals | Owner Main activation, an owner Main delivered turn, and the gateway start pass in `LaneManager.init` that already runs `HarnessHealth.resume_other_routes` after `Ledger.recover_running`. Each starts at most one attempt per `awaiting_main` notice. | R6 |

Superseded mechanisms. The v1 `harness_recovery_episodes` table, its normal-turn
trigger, and the classifier `HarnessRecovery.unavailable?/1` in source commits
`ffb915e661864a37d3bf5efb77bc8c58fb5d6e8c`, `d1201ffe` and `9187c283d24f` are a
second detector under this contract. They are not to be ported.

Compatibility and deletion. The table is additive. Existing turns, wakes, holds
and "other" routes keep their meaning. Whether WI932's release action or rail
translation changes depends on Q1. No notice is backfilled for holds released
or resolved before the feature lands. Deleting the feature removes notice
creation, the settlement and signal hooks, and the schema registration. Historical
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
  only that a real outage opens the hold whose release R1 observes.
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

Each R1–R10 acceptance example SHALL be a behavioral test through the
repository's canonical wrapper on an isolated test host. The WI932 check outcomes
that drive release MAY be synthetic, as WI932 section 12 allows for release logic.
The tests SHALL use the real specimens in A1 to open holds. The restart cases in
R5 SHALL run the real boot path (`LaneManager.init` with `Ledger.recover_running`)
rather than skipping it.

### A3. Installed-release evidence

The work item's done condition is outside this spec's acceptance: "Done only when
an installed release has real recovered-outage evidence of one Main wake." That
evidence is one real released hold, its notice rows and lifecycle events, and one
delivered Main turn carrying the R4 prompt.

## Spec homing

The canonical contract lives only in the `tightbeam-specs` repository as
`harness-recovery-main-wake-v2.md`. It supersedes `harness-recovery-main-wake-v1.md`
at commits `73aec01d7331e08b148994d6525ff75c2b00e137` and
`0860144059f1`. Neither revision is on the main line, and neither may land.
Its coupled authority is WI932 `held-harness-hourly-recovery.md` at the SHA-256
named above, held outside this repository. A change to WI932's release action,
eligibility or Terms requires re-review of this contract. Recon documents, review
reports, artifact rows and transcripts are evidence, not canonical custody.

## Open Questions

- **Q1 (BLOCKING): where the notification policy lives.** The WI932 PO judgment
  `art_4bd40c7a`, as WI932 R9 quotes it, says: "Policy electing eligible holds,
  timing, suppression, recovery and notification belongs in configurable TOML
  rails." WI932's default rail says of its own effect: "No message goes to any
  agent or person." Review 2 B2 found that a compiled notice effect in the release
  action conflicts with that boundary unless a precise PO ruling accepts it. The
  delivery owner is routing this question to the product owner; this draft does
  not choose. The two shapes considered:
  - a compiled substrate effect in WI932's release action, which needs a PO ruling
    accepting the exception and an amendment to WI932's release effect and
    translation;
  - a separately elected TOML rail reacting to the hold's resolution, which needs
    the hold-resolved event to carry the resolution correlation and affected
    owners, an owner-Main recipient, a plain-English translation, and no compiled
    fallback, while the R5 and R6 retry behavior stays a fixed runtime mechanism.

  Blocked until the ruling: the notice creation seam, any rail or WI932 change, and
  how R1 and R3 apply when no policy is elected. Not blocked: R2 and R4 to R10,
  including the restart and settlement behavior, hold under either answer.
- **Q2 (NON-BLOCKING): holds resolved by a normal turn.** Today a single delivered
  turn on any model resolves a `rate-limit-dead` hold before WI932's cycle runs
  (R1 acceptance (b)). Those owners get no notice, though their preserved intents
  are redelivered. Default: no notice, because counting that path re-opens Review
  F1 and WI932 section 7 keeps it unchanged.
- **Q3 (NON-BLOCKING): an owner with no Main for a long time.** Default: the notice
  waits in `awaiting_main` with its evidence, and nothing is escalated. The
  harness-health "other" path files a `user-alerted` fact when no Main exists; this
  contract does not, because the ask does not request it.
- **Q4 (NON-BLOCKING): owners whose held sessions had no stalled work.** Default:
  every affected owner is notified, because the fence held all their sessions on
  that harness and host, and Main judges what stalled.

Q1 is the only BLOCKING question.
