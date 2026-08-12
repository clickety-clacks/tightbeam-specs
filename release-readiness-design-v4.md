# Release readiness, frozen main candidates, and optional release lines — revision 4

Status: spec-approved candidate for fresh independent exact-artifact review.  
Canonical path: `specs/tightbeam/release-readiness-design-v4.md`  
Work item: `wi_3c9d3a64-15a8-457e-b2b1-429a1264f04f`  
Producer assignment: `asg_ea220e82-5a11-4706-9fd0-ffbb979dc134`

This revision replaces the decision authority of `art_3d656920`, SHA-256
`6af5e684ee145314d6a906429378c1709e126a3de815d59e65d89c95ac8b1df0`, and its
imported baseline `art_df141e91`, SHA-256
`3252a3928f3ff64865c8f8c53ea3a94d68a9cd24ba134aaf7ac49cee94828001`.
Those artifacts and earlier revisions remain immutable history.

This revision closes the controlling review `att_4506ae4f-9b29-4eda-8207-936e1341e344`
and its full report `art_df1f7f1d`, SHA-256
`a7ec2c75e96bdf6b093c2e734a8aa57dfcf49606eaea5df1b530190a36fd9594`.
It also implements the product-owner ruling
`att_2a65ba32-88ad-460b-afde-ae47a409bd93` in the design. That ruling supersedes
`att_8db7d29a-588e-4745-8dde-082a0cc10089` where the older ruling made a release
branch the default candidate path. The older ruling remains superseded provenance and
has no normative force in this revision.

This file is one self-contained authority. A builder does not need a prior revision to
interpret it. No implementation, merge, release, deployment, tag, or branch mutation is
authorized by this file. Implementation remains blocked until a different Codex session
files `reviewed-clean` against this file's exact SHA-256 and the product owner then opens
an implementation assignment.

## Goal

Give each product owner a durable release train, an exact accountable owner, and a readable
release-readiness brief. The default path integrates independently reviewed-clean features
into `main`, freezes one exact `main` commit SHA as the release candidate, and binds CI,
packages, installed test-host deployment, evidence, promotion, and the immutable version
tag to that SHA.

Support a named protected release branch only when the creation request explicitly declares
a concurrent stabilization, maintenance, or patch line and the exact target accepts that
declaration as owner. In that optional mode, the exact release-branch head SHA becomes the
candidate source.

The substrate records and enforces declarations. The product owner alone chooses release
scope, gates, evidence, risks, decisions, readiness, and go/no-go.

The operating pattern established here is **frozen-SHA release**. It applies to a registered
release train from candidate freeze through proof, promotion, post-proof tagging, and
rollback. Its optional **release-line** variant applies only after an explicit product-owner
mode choice. It does not apply to ordinary feature branches or unrelated CI workflows.

## Non-Goals

- This revision does not implement the design.
- This revision does not select features, infer readiness, waive a gate, rule a decision,
  or choose go/no-go.
- This revision does not replace work items, assignments, attests, artifacts, decision
  requests, roles, wakes, or the event stream.
- This revision does not make causal descendants implicit release members.
- This revision does not make a Git tag a release candidate, a CI input, or a deployment
  input.
- This revision does not require a release branch for an ordinary release from `main`.
- This revision does not allow direct pushes, history rewrites, force pushes, or branch
  deletion as release repair mechanisms.
- This revision does not define production-host containment. The existing deploy-gate and
  containment work retain that responsibility.
- This revision does not move `main` backward. A source rollback uses a reviewed revert in
  a new train. An installed test-host rollback reuses a previously proved artifact digest.
- This revision does not migrate historical work into release trains automatically.

## Terms

**Release train** (`rel_<uuid>`): the durable coordination record for one product-authored
release effort in one repository.

**Sponsor**: the user who creates the train. The sponsor can open an emergency owner offer
or cancel with a reason. Sponsor status does not grant readiness, integration, promotion,
or tag authority.

**Owner offer** (`roo_<uuid>`): a pending offer to one exact live session incarnation.

**Owner epoch** (`roe_<uuid>`): the interval during which one exact accepted session is
accountable and authorized for owner actions.

**Canonical brief** (`rb_<uuid>`): one immutable `release-brief/v1` document that contains
literal members, watches, gates, risks, decisions, readiness, go/no-go, candidate mode,
candidate identity, and evidence bindings.

**Currency**: the structural state `current | stale | needs_attention`. Currency reports
whether the current brief covers declared material facts and passes integrity checks. It
does not report readiness.

**Candidate mode**: the closed value `main_snapshot | release_line`. `main_snapshot` is the
default when creation carries no optional-line declaration. `release_line` requires an
explicit creation declaration with purpose `concurrent_stabilization | maintenance | patch`
and rationale, followed by the exact target's acceptance as owner before any branch effect.

**Frozen main candidate**: the exact commit SHA that `main` named when the product owner
created the candidate generation. Later movement of `main` does not change this immutable
candidate.

**Optional release branch**: the one registered protected branch for a `release_line` train.
Its name is `release/<train-id>`, where `<train-id>` is the full lower-case release UUID
without the `rel_` prefix. The stored repository identity and branch name form its immutable
identity.

**Line head**: the exact 40-hex Git commit SHA currently named by an optional release branch.

**Integration entry** (`ri_<uuid>`): an append-only record of one reviewed feature entering
`main`, or one accepted update from an expected optional-line head to a new head. It
identifies the introduced commit set, source kind, review evidence, actor, cause, provider
effect, and ref readback.

**Independent reviewed-clean evidence**: a `reviewed-clean` verdict filed on a review
assignment whose `reviewsAssignmentId` names the feature-producing assignment, whose
reviewer session differs from the producing holder session, and whose structured
`commitRefs` contains the exact repository and commit SHA. A note, branch name, pull request
number, ancestor SHA, descendant SHA, or replaced head does not qualify.

**Reviewed feature commit**: an exact Git commit SHA with independent reviewed-clean
evidence for that repository and SHA.

**Candidate generation** (`rcg_<uuid>`): an immutable binding of a train, mode, repository,
candidate SHA, base SHA, integration provenance, creation cause, and generation ordinal. In
`main_snapshot` mode, candidate freeze creates one immutable generation and later `main`
movement does not supersede it. In `release_line` mode, a line-head change creates a new
generation and supersedes the prior one.

**Candidate run**: CI admitted for one candidate generation. `main_snapshot` admission uses
an explicit dispatch naming `main` and the frozen SHA. `release_line` admission uses an
optional-line push or an explicit dispatch naming that branch and its exact current head.

**Candidate bundle** (`rcb_<uuid>`): one immutable set of source SHA, pipeline revision,
CI run, package artifact ids and digests, installed test-host deployment evidence, and
proof records. Each gate used for promotion names one candidate bundle.

**Promotion** (`rpo_<uuid>`): the authorized durable decision that one proved candidate
generation and bundle are the release. In `main_snapshot` mode it performs no Git ref
change. In `release_line` mode it requires a closed reconciliation decision but does not
rewrite `main` or the release line.

**Version tag**: an immutable post-proof, post-promotion marker whose target equals the
promoted candidate SHA. A tag is not a candidate generation, candidate trigger, build
input, test input, or deployment input.

**Release-line reconciliation**: the product-owner decision that states how the exact
optional-line candidate relates to `main`. `already_contained` requires the candidate SHA
to be reachable from the cited main SHA. `forward_ported` maps each optional-line
integration not reachable from main to one or more exact reviewed main integration entries.
`not_applicable` is allowed only for purpose `maintenance | patch` and carries a rationale.

**Decision request direct reference**: a canonical brief member or watch that names the
exact decision request id.

**Effort-request parent**: the work item reached only through the existing structural path
`decision_requests.assignmentId -> assignments.workItemId` for an effort request.

**Authorized reader**: an authenticated user or session principal whose org id equals the
train's org id.

## Assumptions

1. Git commit SHAs identify immutable Git objects. A repository can verify ancestry and the
   commit set introduced between two SHAs.
2. The Git provider supports protected `main` and optional release branches, plus a
   conditional ref update that names an expected old SHA and a new SHA.
   The provider also supports a tag ruleset that refuses update and deletion for registered
   release-tag names.
3. `main` is the default integration line. A train can freeze an exact commit that `main`
   currently names without preventing later reviewed commits from entering `main`.
4. The existing `decision_requests` row has a nullable `assignmentId` and no `workItemId`.
   Effort requests require an assignment. Statute requests can exist without one.
5. Existing artifacts can carry a content SHA-256 and work-item provenance. Release-specific
   evidence adds a typed binding to a candidate generation and bundle; it does not alter the
   artifact row.
6. CI can receive the Git event type, repository identity, ref name, and after-SHA. Explicit
   dispatch can receive a repository, branch name, and exact SHA.
7. Installed test hosts can report the installed package digest and embedded source SHA.
8. The release tables described in revision 3 have not shipped. Migration can add the
   consolidated revision-4 schema without translating live release rows.
9. The immutable Clawline fixture retained from revision 3 is `art_ab55409f`, observed
   SHA-256 `08311b7779f8445369e6bf3a5d0c7bfe6203ca833a74b5ebe36b757f9fdf3670`. It contains
   transcript continuity, Gate D, and reopened work item
   `wi_9086ebd5-bd62-4c04-9b97-ac83ce34f53e`. It is acceptance data, not Tightbeam policy.

If an implementation falsifies an assumption, the affected scope returns to spec review.
It does not substitute a heuristic.

## Invariants

### Product authority

**I-01 — Judgment boundary.** Tightbeam stores, validates, routes, times, and projects
literal product declarations. Tightbeam does not derive scope, materiality, gate status,
risk acceptance, readiness, go/no-go, or rollback choice.

**I-02 — Exact owner.** One active or shipped train has one current owner epoch. Only the
exact session credential stored in that epoch can commit or acknowledge the current brief,
author current decisions/readiness/go-no-go, freeze the candidate, mutate an optional
release line, promote, create a release tag, grant relief, open an ordinary transfer, or
owner-cancel. A pending-acceptance train has no epoch.

**I-03 — Main is notice-only.** The owner user's Main can read and receive escalation. That
fact grants zero owner mutations.

### Brief, membership, and decisions

**I-04 — Atomic brief.** One transaction writes the canonical bytes, digest, normalized
members and watches, their counts and hashes, source bases, author provenance, commit event,
and current pointer. A read returns the prior complete brief or the new complete brief.

**I-05 — Initial provenance.** The pre-acceptance initial brief stores
`ownerEpochId = null`, the exact `ownerOfferId`, its author principal, and its commit event.
Owner acceptance opens the first epoch and acknowledges that immutable brief in one
transaction. Acceptance does not rewrite the brief.

**I-06 — Literal membership.** Membership is the normalized set declared in the current
brief. Causal ancestry, titles, notes, role names, and shared user ownership add no member.

**I-07 — Decision requests.** Each decision request has an exact direct subject. An effort
request can also project to a parent work item through its stored assignment and that
assignment's stored work item. A statute request with no assignment has no implicit work
item parent. No implementation invents or stores a replacement work-item field on the
decision request.

**I-08 — Read audience.** An authorized reader can read current and historical canonical
brief bytes, metadata, event history, branch state, and evidence bindings. An unauthenticated
or cross-org caller receives the ordinary non-disclosing authorization refusal.

### Candidate source and optional release lines

**I-09 — Default main snapshot.** A train whose creation request carries no valid
`release_line` declaration commits in `main_snapshot` mode. Candidate freeze requires the
owner to name the exact commit that `main` names in the same checked operation. The
committed generation remains bound to that SHA when `main` later advances.

**I-10 — Optional mode is explicit.** A train enters `release_line` mode only when its
creation request carries an explicit declaration of purpose and rationale. The creation
transaction fixes the mode, which is immutable thereafter. The exact target must accept
and acknowledge that declaration before a release-line provider effect. No default,
migration, or heuristic creates a release branch.

**I-11 — One optional-line identity.** A `release_line` train binds exactly one repository
and branch name. The pair is immutable. A uniqueness constraint prevents two nonterminal
trains from registering the same repository and branch name.

**I-12 — Protected refs and reviewed inputs.** `main` and an optional release branch accept
feature changes only through a reviewed integration seam. Each introduced feature commit
has independent reviewed-clean evidence for its exact SHA. A generated integration commit
either introduces no content beyond its reviewed parents or has its own independent
reviewed-clean evidence for the exact integration SHA. The provider and Tightbeam refuse
direct unreviewed pushes, force pushes, non-fast-forward updates, deletion, and
administrator bypass.

**I-13 — One candidate SHA.** Candidate CI, package construction, installed test-host
deployment, proof, promotion, and tag target accept the current generation SHA as their
source SHA. In `main_snapshot` mode this is the frozen main SHA. In `release_line` mode it
equals the current optional-line head.

**I-14 — Closed CI admission.** Candidate CI starts only from:

1. an explicit dispatch that names `main` and the exact frozen main generation SHA;
2. a push event for the registered optional release branch whose after-SHA becomes the
   admitted generation SHA; or
3. an explicit dispatch that names the optional release branch and the same exact current
   head SHA.

A `main` push event creates zero candidate runs. After freeze, only the explicit dispatcher
can admit the exact main generation. A tag event creates zero candidate runs, packages,
deployments, proofs, and release state changes.

**I-15 — Generation invalidation.** A `main_snapshot` generation is immutable and remains
current for its train after later main commits. An optional-line head change appends a new
generation and makes earlier line generations `superseded`. Runs and evidence for a
superseded line generation remain historical and cannot satisfy a gate or promotion for the
current generation.

**I-16 — One proof bundle.** Promotion selects one candidate bundle. Each gate whose
evidence concerns candidate bytes references that bundle. A non-candidate decision gate can
cite other evidence. The selected bundle's source SHA equals the current generation SHA.
Package and installed-host evidence in that bundle names exact artifact digests. Evidence
from a different SHA or bundle does not combine with it.

### Promotion, tag, recovery, and rollback

**I-17 — Promotion preconditions.** Promotion requires the exact owner, a structurally
`current` and owner-acknowledged brief, literal `go`, satisfied product-authored gates, a
candidate bundle bound to the current generation SHA, and source readback appropriate to
the mode. `main_snapshot` readback must prove the frozen SHA remains a Git object and was
the recorded main head at freeze. `release_line` readback must equal the current generation
SHA and the brief must contain a closed reconciliation decision with evidence.

**I-18 — Promotion records proved bytes.** Promotion records the current generation SHA and
candidate bundle as the released identity. It changes no Git ref and creates no merge
commit, rebuild, package, source archive, or replacement proof.

**I-19 — Tag after promotion.** A release tag can be created only after promotion is
durably complete. The tag target equals the promoted SHA. Provider protection and the tag
seam refuse later update or deletion. A tag provider event has no route to candidate CI.

**I-20 — Idempotent operations and effects.** Integration, candidate freeze, candidate
dispatch, package recording, installed-test recording, promotion, tag creation, and
rollback deployment each use a stable operation id. An operation that invokes an external
system also uses one stable effect id per phase and target. Retry reads the durable
operation and external state; it does not mint a second semantic result.

**I-21 — Crash recovery.** A durable phase record precedes each external Git, CI, package,
or deployment effect. Recovery uses the same effect id and authoritative readback. Timeout
or lost response records uncertainty; it does not declare success or failure without
readback evidence.

**I-22 — Concurrent trains.** Separate `main_snapshot` trains can freeze different reviewed
main SHAs without branches. An explicitly concurrent stabilization, maintenance, or patch
train uses its own protected release line. One train's later main integration does not
silently change another train's frozen candidate.

**I-23 — Release-line reconciliation.** Before `release_line` promotion, the owner records
exactly one reconciliation state: `already_contained | forward_ported | not_applicable`.
`already_contained` cites a main SHA from which the candidate is reachable.
`forward_ported` maps each optional-line integration absent from main to exact reviewed main
integration entries. `not_applicable` requires purpose `maintenance | patch` and a
product-authored rationale. Tightbeam validates references and completeness and records the
decision; it does not select the state.

**I-24 — Rollback without rewrite.** A pre-promotion rollback cancels the train and retains
its candidate and optional branch evidence as history. A post-promotion installed test-host
rollback uses an earlier proved artifact digest selected by the exact release owner. A
source rollback uses a reviewed revert commit integrated into `main` and then a new release
train. No rollback moves `main` or a release branch backward.

## Architecture

### 1. Consolidated durable model

The implementation adds one release projection. It does not create a second task tracker.
Work items, assignments, attests, artifacts, and decision requests remain their current
authorities.

| Record | Mutable purpose | Immutable material |
| --- | --- | --- |
| `release_trains` | current state, currency, owner/brief/generation pointers | repository id, candidate mode, optional branch identity, sponsor, creation audit |
| `release_owner_offers` | open/accepted/expired/withdrawn state | target session, delivery user, deadline, reason, actor/cause |
| `release_owner_epochs` | current epoch end fields | exact owner session, acceptance, start/end audit |
| `release_brief_revisions` and normalized children | no mutation after commit | canonical bytes/digest, members, watches, bases, decisions, provenance |
| `release_source_occurrences` and subject heads | append and head advance | typed cause, direct/parent projections, literal filters |
| `release_action_needs` and deliveries | action state/retry coverage | generation, source range, due time, attempts, acknowledgments |
| `release_integrations` | phase and authoritative outcome | target ref, expected/new head, introduced set, evidence, operation/effect ids |
| `release_candidate_generations` | superseded marker for optional lines | release, ordinal, mode, candidate SHA, base SHA, freeze/readback cause |
| `release_candidate_bundles` and evidence bindings | no mutation after seal | source SHA, pipeline revision, run, artifact digests, host proofs |
| `release_promotions` | phase and authoritative outcome | mode, candidate SHA, bundle, reconciliation, owner, operation id |
| `release_tag_markers` | phase and authoritative outcome | tag name, promoted SHA, operation/effect ids |
| `release_events` | append-only | actor, cause, typed payload/hash, sequence, time |

One partial unique index enforces one active owner epoch per train. One partial unique index
enforces one nonterminal `release_line` train per repository/branch pair. One partial unique
index enforces one open action per release, owner epoch, brief generation, and action kind.
One unique index reserves each repository/tag-name pair for one promotion.

Mechanism choice: ADD wins because Git refs alone cannot preserve product ownership,
review provenance, proof binding, or recovery after a lost external response. DELETE loses
because Mike requires a durable release responsibility and an exact frozen candidate SHA.
ACCEPT loses because an unreviewed or tag-built candidate is an explicitly rejected release
state. Optional release-line state is added only for the explicit concurrency, maintenance,
and patch cases; ordinary releases add no branch.

### 2. Owner and brief lifecycle

`release-create` runs one transaction that:

1. validates the sponsor, repository, exact target session, candidate mode, optional-line
   purpose/rationale when selected, initial brief, and offer deadline;
2. verifies that an optional branch name is unused by another nonterminal train;
3. creates the pending train with `main_snapshot` as the default mode and stores an optional
   immutable release-line identity only when explicitly selected;
4. commits the initial brief with `ownerEpochId = null` and `ownerOfferId = offerId`;
5. creates the owner offer, acceptance action, and delivery coverage;
6. appends the create and brief-commit events.

`release-accept` compares the caller credential with the exact offer target. One transaction
accepts the offer, opens the first epoch, acknowledges the initial brief for that epoch,
satisfies the action, activates the train, and installs the owner pointer.

Transfer keeps the prior epoch current until the exact target accepts. Sponsor/admin
emergency transfer requires a reason. Relief is exact-session and proposal/evidence-only.

The train state machine is closed:

```text
pending_acceptance --exact target acceptance--> active
active --authorized promotion---------------> shipped
pending_acceptance|active --authorized cancel--> canceled
```

Only `active` accepts candidate freeze, optional-line creation/integration, brief mutation,
bundle sealing, or promotion. `shipped` accepts post-promotion tag creation, exact-target
owner transfer, reads, and installed test-host rollback. `canceled` accepts reads. Promotion
and cancellation make an optional line retained read-only. The last owner epoch remains the
current exact owner after `shipped` so that tag creation and installed test-host rollback
remain attributable. If that session retires, sponsor/admin can open the same exact-target
emergency transfer without gaining owner authority.

### 3. Brief shape and source projection

`release-brief/v1` has required keys: `schema`, `target`, `candidate`, `members`, `gates`,
`risks`, `decisions`, `readiness`, and `goNoGo`. Arrays can be empty. Required objects cannot
be omitted.

The candidate object is:

```json
{
  "repository": "github:owner/repo",
  "mode": "main_snapshot",
  "sourceRef": "refs/heads/main",
  "releaseLinePurpose": null,
  "baseSha": "89abcdef0123456789abcdef0123456789abcdef",
  "candidateGenerationId": "rcg_...",
  "candidateSha": "0123456789abcdef0123456789abcdef01234567",
  "candidateBundleId": "rcb_..."
}
```

A brief can use `null` for generation, SHA, and bundle before the first candidate exists.
The owner must commit a covering brief after a candidate generation or bundle changes.
`baseSha` is the product-authored exclusive baseline for reviewed-integration coverage. It
must resolve in the same repository and be an ancestor of `candidateSha`.

The required `decisions` array uses closed status
`open | ruled | withdrawn | superseded`. Each item stores exact product-authored question,
ruling, rationale, optional direct decision-request id, and evidence refs. The substrate
validates ids and status and stores actor/cause; it does not summarize or rule the decision.

One source mutation creates one cause with a canonical ordered projection set. Assignment,
attest, and artifact writes project directly and through their stored `workItemId` when
present. Decision-request writes follow this closed rule:

- direct projection: exact decision request for each request kind;
- effort parent projection: stored `assignmentId`, then the assignment's stored
  `workItemId`, when both exist;
- statute parent projection: absent unless a future separately reviewed schema gives the
  statute request a structural parent.

The source transaction advances projected subject heads atomically. Matching uses subject
kind/id, occurrence kind, and closed literal fields. It does not scan prose. Direct and
parent matches for one source sequence reduce to one action update.

Closed attest occurrence kinds distinguish progress, completion, surrender, and verdict.
Verdict occurrences store exact `verdictKind`. A reviewed-clean watch therefore ignores a
progress attest and a changes-requested verdict.

Each product-declared material watch supplies a positive `refreshWithinMs`. The number
bounds owner response time; it does not decide materiality or readiness. The first matching
source occurrence atomically makes currency `stale` and opens one `refresh-brief` action for
the release, owner epoch, and brief generation. Later matching source sequences coalesce
into that action, preserve their ids/count, and move the due time only to the earliest
declared deadline. For a source occurrence at `T`, that watch's due time is
`T + refreshWithinMs`. One source sequence increments the count once when direct and parent
watches both match.

Each open offer and stale generation has one action with a pending delivery or durable
retry time. Delivery targets the exact owner session. Failure records cause and sends one
notice to the derived owner user's Main. Acknowledgment proves receipt and does not satisfy
the action. Exact target acceptance satisfies an owner action; a covering owner-committed
brief satisfies a refresh action. Boot recovery restores missing delivery coverage and
reuses the open action id. If an action remains open at `dueAt`, the substrate records one
deadline escalation and sends one high-attention marker to Main. Main delivery grants no
owner authority.

Delivery retry ordinals use waits of 5, 10, 20, 40, then 60 seconds; later retries remain
60 seconds apart. The delivery row persists ordinal and `retryAt` before scheduling the
wake. Satisfaction or cancellation suppresses a pending retry by action id.

### 4. Reviewed integration, candidate freeze, and optional release line

The repository protects `main`. A reviewed integration operation records the expected main
head, exact reviewed feature commits, their independent reviewed-clean attests, the
resulting main head, actor/cause, and provider readback. The commit set between expected and
new head cannot contain an unreviewed feature. A merge commit with content not represented
by its reviewed parents requires its own exact reviewed-clean attest. A merge commit counts
as content-free only when its tree equals the provider-computed conflict-free merge of its
recorded parents.

In default mode, `release-candidate-freeze <releaseId> --ref main --sha <C>` is the candidate
mutation seam. One checked operation:

1. locks the train and verifies mode `main_snapshot`;
2. re-reads `main` and requires `main == C` at that point;
3. verifies the product-authored base-to-C integration set against exact reviewed-clean
   evidence;
4. writes one immutable candidate generation for C and appends the freeze event.

Later movement of `main` creates no generation on that train and does not stale C. A new
default candidate requires a new release train; it does not rewrite the frozen generation.
A second freeze with the same operation key returns the first result. A second freeze with
a different candidate or key returns `candidate_already_frozen`.

In optional mode, `release-line-create` creates the protected branch at an exact
owner-selected base SHA. The base must be either the current `main` head read in the create
operation or the target of an immutable tag recorded by a prior succeeded promotion. The
durable operation records that base source before the provider effect. Readback must show
the registered branch at that SHA before generation 1 commits.

`release-line-integrate` is the only optional-line mutation seam. It accepts source kind
`reviewed-feature | reviewed-backport | current-main-sync`, expected old line head, exact
source and result SHAs, reviewed-clean evidence for each introduced feature/backport and
any content-bearing integration commit, parents, exact owner, and idempotency key. The
transaction locks and re-reads the line, validates graph/evidence, and writes a prepared
operation. The executor uses a conditional fast-forward ref update. Readback resolves:

- line equals new SHA: record one integration and one new generation;
- line equals expected old SHA after a retryable result: retry the same effect;
- line equals another SHA: record `branch_head_conflict`, set `needs_attention`, and change
  no generation pointer;
- provider reports non-fast-forward, deletion, force, direct unreviewed push, or bypass:
  record `branch_rewrite_forbidden` and change no generation pointer.

A lost response uses the same effect id and line readback. It creates no second integration
or generation.

Each external operation follows one protocol. The admission transaction stores operation
id, phase `prepared`, exact target, inputs, expected readback, and a stable effect id derived
from `(operationId, phase, target)`. The executor invokes the external system with that
effect id when supported and then stores its response. Recovery reuses the row and effect
id. Authoritative readback decides succeeded, retryable, conflict, or terminal refusal.
A timeout records `outcome_unknown`; timeout does not decide the external outcome. Recovery
performs authoritative readback after waits of 5, 10, 20, 40, then 60 seconds, with later
readbacks 60 seconds apart. It re-invokes the same effect only after readback proves
`not_started` or the external system reports a retryable pre-effect failure. `in_progress`
or unavailable readback schedules the next readback and does not invoke a second effect.

### 5. Candidate CI, package, installed-host proof, and stale heads

The candidate workflow accepts these trigger envelopes:

```json
{"kind":"explicit_dispatch","repository":"github:owner/repo","branch":"main","sha":"<frozen-sha>","generationId":"rcg_..."}
```

```json
{"kind":"branch_push","repository":"github:owner/repo","ref":"refs/heads/release/<train-id>","afterSha":"<sha>"}
```

```json
{"kind":"explicit_dispatch","repository":"github:owner/repo","branch":"release/<train-id>","sha":"<sha>"}
```

Default admission resolves the train by generation id and requires branch `main`, envelope
SHA equal to the frozen generation SHA, and Git-object readback for that SHA. It does not
require current `main` to remain at the frozen SHA. A generic main-push envelope creates no
candidate run.

Optional-line admission resolves the train by exact repository/branch identity and re-reads
the line. The envelope SHA, line readback, and current generation SHA must match in one
admission decision. A mismatch returns `stale_candidate_head` and creates no candidate run.

The candidate workflow has no tag trigger. If the CI provider delivers a tag event to its
endpoint, the handler records `candidate_tag_event_ignored` with event id and returns a
non-run result. It creates no run, artifact, deployment, proof, wake, or release mutation.

Each build records the checked-out source SHA before package construction. Each package
records its content digest and embedded source SHA. Each installed test host reports the
package digest and embedded source SHA. A bundle seals only when these values equal the
current generation SHA and one product-authored gate set names the same bundle.

A retry for the same source can produce the same digest or a different digest. The same
digest deduplicates. A different digest forms a different candidate bundle; installed-host
and proof records from the earlier bundle do not transfer.

When an optional-line head changes, the new generation supersedes the prior generation in
the same transaction that advances the release pointer. Running jobs can finish and append
historical results. Their results cannot satisfy the current brief or promotion. Main
movement after a default freeze has no such invalidation effect.

### 6. Promotion protocol

`release-promote` is one database transaction after read-only Git verification:

1. Lock the train. Re-read owner epoch, current brief, generation, candidate bundle, gates,
   package digests, and installed test-host proof.
2. In `main_snapshot` mode, verify the frozen SHA remains readable and its freeze event
   records that exact SHA as main head. Current main can name a later reviewed commit.
3. In `release_line` mode, verify line readback equals the generation SHA and validate the
   closed reconciliation decision and cited evidence.
4. Validate I-17, write one succeeded promotion, append the exact mode/SHA/bundle/digests,
   and set the train state to `shipped`.

Promotion invokes no Git update, build, package, deployment, or tag effect. A database crash
before commit leaves no promotion. A retry with the same operation id returns the one
committed result.

### 7. Post-promotion tag marker

`release-tag-create` accepts an exact tag name only for a durably succeeded promotion. It
derives the target from `promotion.candidateSha`; a caller cannot supply another target.
The provider effect and readback use stable ids.

- Missing tag: create it at the promoted SHA.
- Existing tag reserved by this promotion at the promoted SHA: return the prior semantic
  success.
- Existing tag at the promoted SHA without this promotion's reservation: record
  `tag_name_claimed` and change no tag.
- Existing tag at another SHA: record `tag_conflict` and change no tag.
- Promotion incomplete: return `promotion_not_complete` and call no provider.

The tag operation does not invoke candidate CI. A tag failure leaves the train shipped and
records marker state `pending | failed | complete`. Retrying tag creation does not rebuild,
retest, redeploy, or change `main`.

### 8. Rollback

Before promotion, the exact owner or sponsor/admin with reason can cancel the train. A
frozen candidate remains retained history. An optional branch becomes read-only retained
history. Generations, runs, bundles, and events remain queryable.

After promotion:

- the exact release owner can redeploy a previously proved package to an installed test
  host by exact artifact id and digest; the rollback operation records prior/replacement
  digests, hosts, actor, cause, effect id, and readback;
- production-host rollback remains governed by the separate deploy-authorization gate;
- a source rollback integrates a reviewed revert commit into `main`, then begins a new
  default release train and follows this specification through promotion;
- `main`, the prior release branch, and a version tag receive no backward ref update.

### 9. Authorization

| Action | Authorized principal |
| --- | --- |
| Read current/history/branch/evidence | authenticated same-org user or session |
| Create train | sponsor user, sponsor-owned session, or admin |
| Accept offer | exact target session |
| Commit/ack brief; decide; freeze candidate; optional-line integrate; promote; create tag | exact current owner session |
| Integrate a reviewed feature into `main` | existing authorized merge principal after exact reviewed-clean gate |
| Propose brief/evidence | exact owner or exact live relief session |
| Grant/revoke relief; ordinary transfer | exact current owner session |
| Emergency transfer | sponsor/admin with reason |
| Cancel before promotion | exact owner or sponsor/admin with reason |
| Admit optional-line push CI | authenticated CI process after exact branch/SHA checks |
| Admit explicit CI | exact owner request executed by authenticated CI process |
| Record package/test proof | authenticated CI/deployment process bound to operation id |
| Execute Git/provider effects and recovery | `process:tightbeam` using prepared operation |
| Roll back installed test-host package | exact current release owner with proved digest |

The gateway derives org, caller, exact session, owner epoch, actor, cause, hashes, sequences,
times, and effect ids. It strips caller-supplied audit fields. Sponsor/admin emergency power
does not bypass branch, evidence, bundle, or promotion invariants.

### 10. Read, observability, and compatibility

`release-get` and `GET /api/releases/:id` return one atomic snapshot with canonical brief
bytes, digest, owner epoch, currency, open actions, candidate mode, frozen main SHA or
optional-line identity/head, current generation, integration provenance, candidate runs,
bundle/artifact digests, installed-host proof, reconciliation decision,
promotion phase, tag marker state, rollback records, and requested event page.

`release-brief-get`, generation-by-id, bundle-by-id, integration-by-id, and promotion-by-id
return immutable historical records. Clients recompute canonical content and manifest
hashes. Integrity mismatch returns `needs_attention`; it does not return `current`.

The event stream exposes typed events for offer/epoch, brief, source match, action, reviewed
main integration, main candidate freeze, optional-line preparation/outcome/refusal,
generation supersession, CI admission/refusal,
bundle seal/refusal, promotion phases/readback, tag marker phases/conflict, and rollback.
Each refusal carries principal, cause, repository, ref, expected SHA, observed SHA, and
operation id when those values exist.

Migration is additive. Existing work rows, decision requests, roles, artifacts, wakes,
messages, and event rows remain byte-identical. Existing repositories get no train. A train
gets no release branch unless its owner explicitly selects `release_line`. Generic legacy
tag workflows can continue for
unrelated purposes, but a tag event cannot enter the candidate release workflow or write a
candidate run/evidence record. The wire protocol keeps `protocolVersion: 1` and advertises
the additive feature `release-state-v1`.

## Acceptance

Each clause below is a required pass/fail check. Tests inspect durable rows, provider calls,
ref readback, output, and forbidden side effects.

### Product authority, owner, brief, and readers

**A-01 — Product judgment.** Given closed gates without an owner readiness declaration,
when Tightbeam projects the train, then readiness and go/no-go remain the exact authored
values and no inferred declaration or ship event exists.

**A-02 — Exact owner.** Given two sessions owned by Mike and an epoch naming session A,
when session B tries commit, decide, freeze, optional-line integration, promote, tag,
ordinary transfer, ship, or owner-cancel, then each request returns `not_release_owner` and
writes zero mutation rows. This check does not replace the separately authorized
sponsor/admin emergency-transfer and reasoned-cancellation cases.

**A-03 — Initial epoch ordering.** Given a newly created pending train, when storage is read
before acceptance, then the initial brief has `ownerEpochId = null`, the exact offer id,
author, and commit event, and no owner epoch exists. When the exact target accepts, then one
epoch opens and one acknowledgment binds that epoch to the unchanged brief digest.

**A-04 — Atomic brief.** Given a fault after each brief child write, when commit runs, then
the transaction rolls back and the prior current pointer remains. Given no fault, the
canonical bytes, digest, children, bases, counts, hashes, event, acknowledgment, and pointer
appear together.

**A-05 — Decision request direct and effort parent.** Given an effort request with an
assignment whose `workItemId` is `wi_1`, when it opens and is ruled, then each occurrence
projects to the exact request and `wi_1` through the stored assignment path.

**A-06 — Statute request direct only.** Given a statute request with `assignmentId = null`,
when it opens and is ruled, then each occurrence projects to the exact request, creates no
parent work-item projection, and matches an exact direct-request watch.

**A-07 — Reader allow.** Given an authenticated same-org session that is not owner, sponsor,
or relief, when it reads current and historical release records, then it receives canonical
bytes and evidence metadata and can verify their hashes.

**A-08 — Reader deny.** Given an unauthenticated caller and an authenticated cross-org
caller, when each reads the same release id, then each receives byte-equivalent
`release_not_found` responses and no content or existence metadata.

### Default main path and optional release line

**A-09 — Main snapshot is default.** Given a train create request with no mode field, when
creation commits, then mode is `main_snapshot`, no release branch identity or provider call
exists, and the initial brief records main as the candidate source ref.

**A-10 — Reviewed main integration.** Given feature SHA F with independent reviewed-clean
evidence for F and expected main H, when an authorized merge principal integrates F, then
new main N is a fast-forward descendant of H and the integration record names F, its exact
structured commit-ref verdict, review-to-producer assignment link, distinct reviewer
session, H, N, actor, and provider readback. Evidence for another SHA, an unlinked review,
or the producer session's own verdict returns `feature_review_mismatch` and calls no ref
update. A content-bearing merge commit without its own exact clean evidence returns
`unreviewed_integration_commit`.

**A-11 — Exact main freeze.** Given current main C and a train in `main_snapshot`, when the
owner freezes C, then one generation records mode, repository, source ref main, base,
candidate C, integration evidence, owner, and freeze readback. Given requested D while main
is C, then it returns `candidate_not_current_main` and creates no generation. Given a base
that is missing, from another repository, or not an ancestor of C, then it returns
`invalid_candidate_base`. Given an existing frozen generation, a different-key freeze
returns `candidate_already_frozen`; a same-key retry returns the first result.

**A-12 — Unreviewed main-range refusal.** Given the product-authored base..C range contains
reviewed F and unreviewed U, when candidate freeze validates the range, then it returns
`unreviewed_main_commit`, creates no generation, and starts no CI.

**A-13 — Frozen main stability.** Given a frozen main candidate C and later reviewed main
head D, when the train is read and candidate CI is dispatched, then C remains its current
generation and source; D neither supersedes C nor transfers evidence into C.

**A-14 — Optional mode and identity.** Given a creation request explicitly selects
`release_line` with purpose `maintenance` and rationale, when train creation commits, then
it stores one immutable `release/<train-id>` identity. Missing purpose/rationale is refused.
A second nonterminal train using the same repository/name or a later mode change is refused. A base
that is neither the current main head nor a prior immutable promoted tag target returns
`invalid_release_line_base` and calls no branch provider. Before the exact target accepts
and acknowledges the declaration, `release-line-create` returns `train_not_active` and
calls no branch provider.

**A-15 — Optional-line protection and review.** Given a reviewed feature or backport F and
expected line head H, when the owner integrates F, then new head N is a conditional
fast-forward descendant and the entry records exact review evidence. Given an unreviewed
introduced commit, content-bearing unreviewed merge commit, direct push, non-fast-forward,
force push, deletion, or admin bypass, then the attempt is refused, the line is unchanged,
and one typed refusal event records actor and cause.

**A-16 — Optional-line recovery and conflict.** Given the provider applies H->N and loses
the response, when recovery runs twice, then readback N produces one integration and one new
generation. Given provider head X instead, then `branch_head_conflict` sets
`needs_attention` and changes no generation pointer.

### Candidate admission, packages, evidence, and stale heads

**A-17 — Default explicit admission.** Given frozen main generation C, when the owner
dispatches candidate CI with branch main, generation id, and C, then one run binds C even if
main later names D. A different SHA, branch, or generation returns
`candidate_generation_mismatch` and starts zero runs.

**A-18 — Main push is not admission.** Given reviewed main push H->C with no prior frozen
generation dispatch, when candidate CI receives the event, then it starts zero candidate
runs and writes zero candidate evidence.

**A-18B — Optional-line admission.** Given a push or owner dispatch for the registered
optional line at current head C, when provider/generation readback is C, then one candidate
run starts. A different SHA or branch returns `stale_candidate_head` or
`wrong_release_branch` and starts zero runs.

**A-19 — Tag cannot trigger candidate work.** Given annotated and lightweight tag create,
update, delete, and push events, when each is delivered to candidate CI, then zero candidate
runs, builds, packages, deployments, proofs, wakes, and release mutations exist; one
`candidate_tag_event_ignored` observation can record the provider event id.

**A-20 — Candidate source binding.** Given a candidate run for C, when checkout reports D,
then package construction is refused. Given checkout C, package digest P, and installed host
reports embedded SHA C and digest P, then those records can enter one bundle.

**A-21 — Mixed proof refusal.** Given CI proof for C/bundle 1 and installed-host proof for
C/bundle 2, when candidate-byte gates try to combine them, then bundle sealing or brief
commit returns `mixed_candidate_bundle` and those gates remain unsatisfied. A non-candidate
decision gate can cite another artifact without changing the selected candidate bundle.

**A-22 — Rebuild digest split.** Given two builds from C with digests P1 and P2, when both
complete, then they form distinct bundles. Installed-host proof for P1 cannot satisfy a
gate naming P2.

**A-23 — Optional-line stale generation.** Given a running job for optional-line generation
G1 and a successful line update that creates G2, when the G1 job finishes, then its evidence
remains queryable under G1 and cannot satisfy the current brief or G2 promotion.

**A-24 — Optional-line admission race.** Given a line event for C and a line move to D
before admission, when admission atomically checks the event, provider, and generation,
then it starts zero C jobs and returns `stale_candidate_head`.

### Promotion and irreversible-boundary refusals

**A-25 — Default promotion happy path.** Given exact owner, current acknowledged brief,
literal go, satisfied gates, frozen main candidate C, and one sealed bundle for C, when
promotion runs after main has optionally advanced to D, then one promotion event records
mode, C, bundle, and digests, the train becomes `shipped`, main remains D, and no Git,
build, package, deployment, or tag provider is called.

**A-26 — Table-driven promotion refusal.** Given each case below in turn, when promotion is
requested, then the named error is returned, provider receives zero Git/build/package/
deployment/tag calls, and zero promotion or terminal-state events are written:

| Failed precondition | Error |
| --- | --- |
| caller differs from owner session | `not_release_owner` |
| currency is `stale` | `release_brief_stale` |
| currency is `needs_attention` | `release_needs_attention` |
| owner acknowledgment is absent | `brief_not_acknowledged` |
| go/no-go is `undecided` | `explicit_go_required` |
| go/no-go is `no-go` | `explicit_go_required` |
| one product gate is unsatisfied | `release_gate_unsatisfied` |
| brief, member, watch, or bundle integrity fails | `release_integrity_error` |
| evidence names another SHA or bundle | `candidate_proof_mismatch` |
| frozen main SHA is missing or lacks valid freeze provenance | `frozen_main_candidate_invalid` |
| optional-line readback differs from generation SHA | `stale_candidate_head` |
| optional-line reconciliation is open or missing | `release_line_reconciliation_required` |
| reconciliation evidence names another main/line SHA | `reconciliation_evidence_mismatch` |

**A-27 — No rebuild at promotion.** Given a valid promotion, when it completes, then build,
package, archive, and deployment invocation counts do not change and recorded artifact
digests equal the pre-promotion bundle.

**A-28 — Promotion transaction crash.** Given a crash before promotion transaction commit,
when recovery and the same operation retry run, then zero partial promotion rows exist and
one complete result can commit. Given a crash after commit and lost response, retry returns
that result and writes no second event.

**A-29 — Optional-line reconciliation.** Given a maintenance candidate C not intended for
main, when the owner records `not_applicable` with rationale and promotes, then promotion
records that literal decision and tag target C. Given `already_contained` or
`forward_ported`, then cited exact main/review evidence must resolve or promotion refuses.
Given two optional-line integrations absent from main and a forward-port mapping for only
one, then promotion returns `reconciliation_incomplete`.

**A-30 — Concurrent trains.** Given default trains A and B freeze reviewed main SHAs C1 and
C2, when both prove and promote, then each retains its own SHA/bundle and neither needs a
release branch. Given a concurrent stabilization train S, then only S has a protected
release line and its head movement cannot change A or B.

### Post-promotion tags, retry, and rollback

**A-31 — Tag timing.** Given an active train with no completed promotion, when the owner
requests a tag, then it returns `promotion_not_complete` and calls no tag provider.

**A-32 — Tag target.** Given a completed promotion at C, when tag `v1.2.3` is created, then
provider readback shows `v1.2.3 -> C`. A caller-supplied target is rejected by request
validation.

**A-33 — Tag idempotency and conflict.** Given the tag already points to C, when the same
tag operation retries, then it returns the prior semantic success. Given another
promotion claims the same repository/tag at C, then it records `tag_name_claimed`. Given the
tag points to D, then it records `tag_conflict`, changes no ref, and invokes no candidate
workflow. Given an update or deletion request for a completed release tag, then provider
protection and the tag seam refuse it and the tag remains at C.

**A-34 — Tag failure isolation.** Given completed promotion and a terminal tag-provider
failure, when tag creation runs, then the train remains shipped, marker state becomes
`failed`, main and artifact digests remain unchanged, and no rebuild or candidate run
starts.

**A-35 — Stable idempotency keys.** Given duplicate integration, candidate freeze, CI
dispatch, package, installed-proof, promotion, tag, and rollback requests with the same key,
when responses are delivered, lost, and retried, then each key resolves to one semantic
operation and its durable attempts. Each external phase/target reuses one effect id.

**A-35B — Unknown external outcome.** Given an external timeout and unavailable readback,
when recovery reaches successive retry times, then it records the 5, 10, 20, 40, and
60-second readback waits, preserves `outcome_unknown`, and invokes no second effect. Given
readback `not_started`, then it invokes the same effect id once; given `in_progress`, it
schedules another readback.

**A-36 — Pre-promotion cancel.** Given an active unpromoted train, when the exact owner or
sponsor/admin with reason cancels it, then the train becomes canceled and history remains
readable. A default frozen candidate gains no branch. An optional line switches to retained
read-only.

**A-37 — Installed-package rollback.** Given current installed digest P2 and earlier
promoted digest P1, when the exact release owner selects P1 for an installed test host,
then deployment uses the stored P1 artifact, host readback reports P1, and no build, main
update, branch update, or tag update occurs.

**A-38 — Source rollback.** Given a shipped bad commit C, when a revert is required, then a
direct backward update of main or an optional release line is refused. The reviewed revert
integrates into main, and a new default train can freeze, prove, and promote its exact SHA.

### Compatibility, observability, and reality

**A-39 — Additive migration.** Given a pre-release database, when migration and a second
bootstrap run, then release tables are empty and idempotent and existing work, decision,
artifact, wake, message, role, and event rows are byte-identical.

**A-40 — Legacy tag workflow isolation.** Given an unrelated legacy tag workflow, when a tag
event runs, then its unrelated output can continue, but the release candidate endpoint
records no run, bundle, proof, deployment, or promotion.

**A-41 — Authorization matrix.** Given one real principal for each authorization-table row
and one crossed principal per row, when the built CLI and real gateway execute the actions,
then allowed calls write the specified rows and crossed calls return the specified refusal
with zero forbidden rows.

**A-42 — Real default-main journey.** Given a real protected repository, real CI, package
storage, and installed test host, when a reviewed feature integrates into main, the owner
freezes exact main SHA C, CI runs by exact main+C dispatch, the package is installed and
proved, the owner promotes, and then creates the tag, then frozen SHA, checkout SHA,
embedded package SHA, evidence SHA, promoted SHA, and tag target equal C. No release branch
exists and tag creation starts zero candidate jobs.

**A-43 — Crash-boundary journey.** Given injected process death after each durable phase and
external effect boundary for reviewed main integration, candidate freeze, optional-line
creation/integration, CI dispatch, package record, installed proof, promotion, tag, and
rollback, when boot recovery runs, then authoritative readback produces one semantic
outcome, retained attempts, and no inferred success.

**A-44 — Read and event observability.** Given one success and one refusal for each release
operation, when an authorized reader requests the atomic snapshot and event page, then it
can identify owner, cause, operation, expected/observed refs, generation, bundle, digest,
phase, outcome, retry state, and stale reason without reading prose notes.

**A-45 — Real optional-line journey.** Given an explicitly selected concurrent stabilization
line, when reviewed features/backports enter its protected branch, its exact head C is
proved, the owner records reconciliation, promotes, and creates the tag, then line head,
checkout SHA, embedded package SHA, proof SHA, promoted SHA, and tag target equal C. A line
head change before admission invalidates the older generation.

**A-46 — Owner transfer and retirement.** Given an active owner and an open transfer offer,
when the exact target accepts, then one transaction closes the prior epoch, opens one new
epoch, acknowledges the current brief, and exposes no zero-or-two-owner snapshot. Given a
retired owner, Main receives escalation but cannot act; sponsor/admin can offer transfer to
one exact live session. The same transfer rule applies after `shipped` for tag and installed
test-host rollback authority.

**A-47 — Relief boundary.** Given an exact live relief session, when it proposes a brief and
evidence, then the proposal persists. When it tries commit, acknowledge, decide, freeze,
line-integrate, promote, tag, transfer, ship, or cancel, then each request is refused with
zero owner mutation.

**A-48 — Typed source and action dedupe.** Given one child assignment reviewed-clean verdict
that matches direct and parent watches, when the source transaction commits, then both
subject heads advance, one source sequence opens or coalesces one refresh action, and its
count increments once. Progress, completion, surrender, and changes-requested attests do
not match that reviewed-clean watch.

**A-49 — Action coverage and recovery.** Given an open owner offer and a stale brief, when
delivery fails and the gateway restarts, then each action retains a pending delivery or
retry time, recovery reuses its action id, one Main fallback notice records failure cause,
and Main gains zero owner authority. Given the action remains open at its computed due time,
then exactly one deadline escalation and high-attention Main marker exist. Acknowledgment
leaves refresh open; a covering owner brief satisfies it. Repeated delivery failure records
5, 10, 20, 40, and 60-second waits, then 60-second waits until satisfaction or cancellation.

**A-50 — Canonical content and decisions.** Given current and historical briefs with open,
ruled, withdrawn, and superseded decision entries, when an authorized reader fetches them,
then it receives the complete canonical bytes and recomputes the stored digest. Given
missing content, missing required keys, altered bytes, member/watch hash mismatch, or commit
marker mismatch, then the snapshot returns an integrity error and currency
`needs_attention`, not `current`.

**A-51 — Preserved Clawline fixture.** Given immutable fixture `art_ab55409f` at the assumed
digest, when release membership and gates are serialized, then transcript continuity, Gate
D, reopened `wi_9086ebd5-bd62-4c04-9b97-ac83ce34f53e`, and literal decisions round-trip as
product evidence without becoming Tightbeam defaults.

**A-52 — Terminal optional-line protection.** Given a shipped or canceled `release_line`
train, when owner, sponsor, admin, merge principal, or provider event attempts line
integration, direct push, force update, or deletion, then the operation is refused, the
line head remains unchanged, and retained history remains readable.

## Open Questions

None. The product owner will separately author each train's scope, gates, evidence, risks,
decisions, deadlines, readiness, go/no-go, tag name, and rollback choice. Those values are
runtime product decisions, not holes in this design.
