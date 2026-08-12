# Release readiness, frozen main candidates, and optional release lines — revision 6

Status: spec-approved candidate for fresh independent exact-artifact review.  
Canonical path: `specs/tightbeam/release-readiness-design-v6.md`  
Work item: `wi_3c9d3a64-15a8-457e-b2b1-429a1264f04f`  
Producer assignment: `asg_b4011dae-23aa-41ec-9e66-b08fc09e65c7`

This revision replaces the decision authority of sealed revision 5, `art_fe8314ec`, SHA-256
`511d53d57a346898d36d2ea62540af8bcae2a90a5b879c53144cdb0e3cd039ba`.
Revision 5 remains immutable at `specs/tightbeam/release-readiness-design-v5.md`.

Revision 5 had replaced revision 4, `art_25b966e7`, SHA-256
`fcb6e16af03f2d1c6c590107744a2bdfd62c1856cf07d14f32d3b38194a2ead1`.
Revision 4 remains immutable at `specs/tightbeam/release-readiness-design-v4.md`.
Its byte-identical Gibson review projection `art_0791914f`, SHA-256
`fcb6e16af03f2d1c6c590107744a2bdfd62c1856cf07d14f32d3b38194a2ead1`, also remains
non-canonical provenance.

Revision 4 had replaced `art_3d656920`, SHA-256
`6af5e684ee145314d6a906429378c1709e126a3de815d59e65d89c95ac8b1df0`, and its
imported baseline `art_df141e91`, SHA-256
`3252a3928f3ff64865c8f8c53ea3a94d68a9cd24ba134aaf7ac49cee94828001`.
Those artifacts and earlier revisions remain immutable history.

This revision closes the five findings in revision-5 review
`att_62fb5f13-c20a-4671-af1f-893bf3294880` under owner rulings
`att_1233d254-9c8f-4618-b781-d9cf013eb369` for F1-F3 and
`att_e83f8168-99b8-461a-bef8-bd285b5dceab` for F4-F5.

It preserves revision 5's closure of the eight findings in revision-4 review
`att_7aeb95d6-f5d0-496e-8aa3-13c2863ce266` under owner rulings
`att_21d69cad-cc45-40da-b605-9853847a121d` for F1-F4 and
`att_253d0baa-a17f-4dea-bbd6-2cb3b6145835` for F5-F8. It retains the closure of controlling
historical review `att_4506ae4f-9b29-4eda-8207-936e1341e344` and its full report
`art_df1f7f1d`, SHA-256
`a7ec2c75e96bdf6b093c2e734a8aa57dfcf49606eaea5df1b530190a36fd9594`.
It also implements the product-owner ruling
`att_2a65ba32-88ad-460b-afde-ae47a409bd93` in the design. That ruling supersedes
`att_8db7d29a-588e-4745-8dde-082a0cc10089` where the older ruling made a release
branch the default candidate path. The older ruling remains superseded provenance and
has no normative force in this revision.

Two unpublished draft digests are explicitly rejected: SHA-256
`0bbc4505e7e2b39ba23fcf0d39126ac908aab5b2bea025ca6f52d70d14ee034c` and SHA-256
`81a8ff12a78e72e97f8c85624c7b36301820d59d660e4e7262a2f749a2bea02c`. Neither digest
identified an artifact or authority. No release, review, or implementation can cite either
digest as revision 4, revision 5, or revision 6.

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

**Sponsor**: the user who creates the train. The sponsor can open an emergency-owner
responsibility offer
or cancel with a reason. Sponsor status does not grant readiness, integration, promotion,
or tag authority.

**Responsibility offer** (`rro_<uuid>`): the one durable offer form used for an initial
owner, owner transfer, emergency owner transfer, or relief. Its purpose is
`initial_owner | owner_transfer | emergency_owner_transfer | relief`, and its state is
`pending | accepted | rejected | expired | withdrawn | superseded`. It binds one exact
target session key and session incarnation, deadline, reason, predecessor offer, dedupe and
reissue key, `originOwnerEpochId`, expected train generation, expected line generation or
null, delivery acknowledgments, and terminal actor/cause/time. Only an `initial_owner` offer
has a null origin epoch. Reissue appends a new offer and changes the pending predecessor to
`superseded`; it never rewrites history.

**Owner epoch** (`roe_<uuid>`): the interval during which one exact accepted session is
accountable and authorized for owner actions.

**Train generation**: the monotonically increasing compare-and-set ordinal used to fence
ownership, relief-offer, and relief-proposal mutations on one train. Train creation starts generation
0. Each successful offer acceptance advances it once. When ownership acceptance closes an
epoch, that close and increment are one CAS, not two increments. It is not a candidate or line
generation.

**Capable live target**: the offered session row is live, its current incarnation equals the
offer's stored incarnation, and the existing authorization matrix permits that session to
accept the offer purpose. The phrase adds no inferred skill or readiness judgment.

**Relief grant** (`rrg_<uuid>`): the accepted result of a `relief` responsibility offer. The
offer fixes the grant's future expiry and proposal-only scope before acceptance. The grant
binds the accepting target's exact session key and incarnation to the offering owner epoch.
Its only authority is the nonempty subset of `brief | evidence | owner_transfer_proposal`
stored in its closed `proposalKinds` scope. It ends on explicit revocation, its declared
future expiry, or the end of its owner epoch.

**Relief proposal** (`rrp_<uuid>`): a durable request that the current product owner offer
an ownership transfer. It stores the train, origin owner epoch, expected train and optional
line generation, exact proposer principal, cause, correlation, proposed successor, scope,
reason, idempotency key, timestamps, occurrence history, and state
`pending | accepted | rejected | withdrawn | superseded | expired`. Filing a proposal does
not change ownership or create an offer. Owner acceptance creates an owner-authored transfer
offer; the proposed successor must separately accept that offer through the ownership CAS.

**Canonical brief** (`rb_<uuid>`): one immutable `release-brief/v1` document that contains
literal members, watches, gates, risks, decisions, readiness, go/no-go, candidate mode,
candidate identity, and evidence bindings.

**Brief fact** (`rbf_<uuid>`): one durable, versioned member, watch, gate, risk, decision,
readiness, go/no-go, or evidence identity for a train. Each fact version stores its closed typed state,
predecessor version, actor, cause, and sequence. A canonical brief is the deterministic
projection of exact fact versions; opaque document bytes are not a second authority.

**Watch** (`rbw_<uuid>`): a brief fact whose version stores an exact owner reference, durable
gate/risk/evidence selector, trigger class, acknowledged fact cursor, next due time, dedupe
key, watch generation, rebound predecessor or null, state `active | superseded | retired`,
and reissue policy
`coalesce_until_covered | supersede_after_acknowledged`. Only a durable gate, risk, or
evidence fact transition can be a meaningful change for a watch. The owner reference names
either the pending initial responsibility offer or an owner epoch, never both. Initial-owner
or transfer acceptance appends owner-epoch-bound successor watch versions, supersedes the
offer- or closing-epoch-bound versions, and preserves both the immutable versions and their
old-to-new resolution map.

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

**Line generation**: the monotonically increasing optional-line ref ordinal. Generation 0
binds the protected branch's creation base and has no candidate generation. Each successful
reviewed integration increments it and binds the same ordinal to one releasable candidate
generation.

**Integration entry** (`ri_<uuid>`): an append-only record of one reviewed feature entering
`main`, or one accepted update from an expected optional-line head to a new head. It
identifies the introduced commit set, source kind, review evidence, actor, cause, provider
effect, and ref readback.

**Repository release anchor** (`rra_<uuid>`): an immutable repository, `main` ref, exact
SHA, provider protection-ruleset identity/digest, readback, actor, cause, and time. It marks
the exclusive baseline after which each candidate commit must have reviewed-integration
provenance. It does not assert that commits at or before the anchor were independently
reviewed.

**Independent reviewed-clean evidence**: a `reviewed-clean` verdict filed on a review
assignment whose `reviewsAssignmentId` names the feature-producing assignment, whose
`holderKey` differs from the producing assignment holder, whose verdict `bySession` equals
that review assignment's exact `holderKey` at filing, and whose structured
`commitRefs` contains the exact repository and commit SHA. A verdict from a non-holder
principal, note, branch name, pull request number, ancestor SHA, descendant SHA, or replaced
head does not qualify.

**Reviewed feature commit**: an exact Git commit SHA with independent reviewed-clean
evidence for that repository and SHA.

**Candidate generation** (`rcg_<uuid>`): an immutable binding of a train, mode, repository,
candidate SHA, base SHA, protected provenance anchor, protection readback, integration
provenance, eligibility `releasable | no_change`, creation cause, and generation ordinal. A
`no_change` generation has `baseSha == candidateSha`; it records the checked empty range but
cannot start candidate work or be promoted or tagged. A releasable generation has a strict
ancestor base. In `main_snapshot` mode, candidate freeze creates one immutable generation
and later `main` movement does not supersede it. In `release_line` mode, a successful
reviewed line integration creates a releasable generation and supersedes the prior one.

**Candidate pointer**: the current tuple `(candidateGenerationId, eligibility,
candidateSha, candidateBundleId)` and the SHA-256 digest of its canonical encoding. A change
to any tuple member is a structural brief-staleness event. Identical tuple bytes have the
same digest and are not a change.

**Candidate run**: CI admitted for one candidate generation. `main_snapshot` admission uses
an explicit dispatch naming `main` and the frozen SHA. `release_line` admission uses an
optional-line push or an explicit dispatch naming that branch and its exact current head.

**Branch-push delivery**: the raw provider input consisting only of provider delivery/event
identity, repository, ref, before-SHA, and after-SHA. Gateway ingestion durably enriches a
recognized optional release-line delivery with an allocated operation id, the locked current
line generation, train id, derived branch-push key, and canonical payload hash before
candidate admission evaluates it.

**Candidate bundle** (`rcb_<uuid>`): one immutable set of source SHA, pipeline revision,
CI run, package artifact ids and digests, installed test-host deployment evidence, and
proof records. The candidate pointer names a bundle when the owner selects it. Each gate used
for promotion names one candidate bundle.

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

**Decision request direct reference**: a canonical brief member or evidence fact whose
durable source occurrence names the exact decision request id.

**Effort-request parent**: the work item reached only through the existing structural path
`decision_requests.assignmentId -> assignments.workItemId` for an effort request.

**Authorized reader**: an authenticated user or session principal whose org id equals the
train's org id.

**Line generation lock**: the durable row keyed by exact train, target ref, and line
generation, with state `open | effect_pending | promotion_closed | terminal`. An
optional-line integration changes the exact generation lock from `open` to
`effect_pending` before its ref effect. Promotion changes that same lock from `open` to
`promotion_closed` only after it proves that no ref effect is prepared or in flight.

## Assumptions

1. Git commit SHAs identify immutable Git objects. A repository can verify ancestry and the
   commit set introduced between two SHAs.
2. The Git provider supports protected `main` and optional release branches, plus a
   conditional ref update that names an expected old SHA and a new SHA. It returns the
   active protection-ruleset identity and canonical digest so Tightbeam can verify that
   direct push, force push, deletion, and administrator bypass are disabled.
   The provider also supports a tag ruleset that refuses update and deletion for registered
   release-tag names.
3. `main` is the default integration line. A train can freeze an exact commit that `main`
   currently names without preventing later reviewed commits from entering `main`.
4. The existing `decision_requests` row has a nullable `assignmentId` and no `workItemId`.
   Effort requests require an assignment. Statute requests can exist without one.
5. Existing artifacts can carry a content SHA-256 and work-item provenance. Release-specific
   evidence adds a typed binding to a candidate generation and bundle; it does not alter the
   artifact row.
6. CI can receive the Git event type, provider event id, repository identity, ref name,
   before-SHA, and after-SHA. Explicit dispatch can receive a repository, branch name, exact
   SHA, and caller idempotency key.
7. Installed test hosts can report the installed package digest and embedded source SHA.
8. The release tables described in revisions 3 through 5 have not shipped. Migration can add
   the consolidated revision-6 schema without translating live release rows.
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
release line, promote, create a release tag, offer or revoke relief, open an ordinary transfer, or
owner-cancel. A pending-acceptance train has no epoch.

**I-03 — Main is notice-only.** The owner user's Main can read and receive escalation. That
fact grants zero owner mutations.

### Brief, membership, and decisions

**I-04 — Atomic brief.** One transaction appends exact versions of the durable member,
watch, gate, risk, decision, readiness, go/no-go, and evidence facts; deterministically
projects their canonical bytes, digest, counts, hashes, source bases, and order; and writes
author provenance, commit event, and current pointer. Each collection conforms to the
closed `release-brief/v1` schema in Architecture 3. The transaction refuses any supplied
bytes that do not equal the row-derived projection. A read returns the prior complete brief
or the new complete brief.

**I-05 — Initial provenance.** The pre-acceptance initial brief stores
`ownerEpochId = null`, the exact initial-owner responsibility offer id, its author principal,
and its commit event.
Owner acceptance opens the first epoch, appends epoch-bound successor versions for every
active initial watch, marks the offer-bound versions superseded, appends a mechanically
rebound brief revision, stores the complete old-to-new watch-version map, and acknowledges
that rebound brief in one transaction. The initial brief and watch versions remain immutable.

Only a `pending` offer can be accepted. A rejected, expired, withdrawn, superseded,
accepted, wrong-target, dead-target, or stale-incarnation offer cannot open an epoch or
grant relief. Reissue appends a new exact-target offer and preserves every prior transition.

**I-06 — Literal membership.** Membership is the normalized set declared in the current
brief. Causal ancestry, titles, notes, role names, and shared user ownership add no member.

**I-07 — Decision requests.** Each decision request has an exact direct subject. An effort
request can also project to a parent work item through its stored assignment and that
assignment's stored work item. A statute request with no assignment has no implicit work
item parent. No implementation invents or stores a replacement work-item field on the
decision request.

The source projection has closed lifecycle occurrences `decision-request-opened`,
`decision-request-delivered`, `decision-request-reminder`,
`decision-request-acknowledged`, `decision-request-withdrawn`,
`decision-request-superseded`, `decision-request-expired`,
`decision-request-resolved`, and `decision-request-delivery-failed`. Every occurrence stores
its causal predecessor occurrence id and dedupe identity. Direct and eligible effort-parent
projections preserve every occurrence; no projection erases, collapses, or rewrites history.

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

**I-12 — Protected refs and reviewed inputs.** Train creation requires authoritative
provider readback of the active `main` protection rules and records their identity and
digest. Candidate freeze stores and rechecks the protected provenance anchor, remote ref,
protection ruleset, and ancestry. The product-authored `baseSha` must equal a proved prior
promoted SHA or the exact protected-main anchor in the same repository. A releasable freeze
requires it to be a strict ancestor of the candidate SHA. Equality creates only a durable
`no_change` generation. `main` and an optional release branch accept feature changes only
through a reviewed integration seam. Each
introduced feature commit has independent reviewed-clean evidence from the exact
review-assignment holder for its exact SHA. A generated integration commit either
introduces no content beyond its reviewed parents or has its own holder-authored independent
reviewed-clean evidence for the exact integration SHA. The provider and Tightbeam refuse
direct unreviewed pushes, force pushes, non-fast-forward updates, deletion, and
administrator bypass.

**I-13 — One candidate SHA.** Only a `releasable` generation can enter candidate CI,
package construction, installed test-host deployment, proof, promotion, or tagging. Those
operations accept the current generation SHA as their source SHA. In `main_snapshot` mode
this is the frozen main SHA. In `release_line` mode it equals the current optional-line head.

**I-14 — Closed CI admission.** Candidate CI starts only from:

1. an explicit dispatch that names `main` and the exact frozen main generation SHA;
2. a push event for the registered optional release branch whose to-SHA becomes the
   admitted generation SHA; or
3. an explicit dispatch that names the optional release branch and the same exact current
   head SHA.

A `main` push event creates zero candidate runs. After freeze, only the explicit dispatcher
can admit the exact main generation. A tag event creates zero candidate runs, packages,
deployments, proofs, and release state changes.

An optional-line CI caller supplies only provider delivery/event identity, repository,
target ref, before-SHA, and after-SHA. Gateway ingestion deduplicates the provider identity,
durably allocates or recovers `operationId`, resolves the exact registered release line and
current `lineGeneration` under its generation lock, derives the idempotency key from
`(trainId, lineGeneration, targetRef, fromSha, toSha)`, and commits the enriched operation
before candidate admission evaluates it. An unknown ref records
`ignored_non_release_line_event` and creates no admission. A line generation that changes
between enrichment and admission returns `stale_candidate_head` and creates no run.

The durable admission records states
`prepared | effect_pending | receipt_recorded | terminal`. Redelivery with another provider
delivery id but the same provider event identity and immutable payload converges on that
operation and its first terminal run or non-run result. Reuse of a provider delivery or event
identity with a different immutable payload is an identity mismatch.

**I-15 — Generation invalidation.** A `main_snapshot` generation is immutable and remains
current for its train after later main commits. A successful reviewed optional-line
integration appends a new generation and makes earlier line generations `superseded`. Runs and evidence for a
superseded line generation remain historical and cannot satisfy a gate or promotion for the
current generation.

Every committed candidate-pointer tuple change atomically marks a covering current brief
`stale` and opens or reissues the one durable `refresh-readiness` action for the train,
current generation, and latest pointer digest. Identical tuple bytes deduplicate. A newer
tuple supersedes the earlier open target while preserving occurrence history.
Acknowledgment does not close the action. Only a newly committed owner brief that binds the
exact latest candidate tuple and digest closes it.

**I-16 — One proof bundle.** Promotion selects one candidate bundle. Each gate whose
evidence concerns candidate bytes references that bundle. A non-candidate decision gate can
cite other evidence. The selected bundle's source SHA equals the current generation SHA.
Package and installed-host evidence in that bundle names exact artifact digests. Evidence
from a different SHA or bundle does not combine with it.

### Promotion, tag, recovery, and rollback

**I-17 — Promotion preconditions.** Promotion requires the exact owner, a structurally
`current` and owner-acknowledged brief, `goNoGo.decision == go`, satisfied product-authored gates, a
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

Optional-line push admission uses the Gateway-enriched operation id and derived stable
idempotency key from train, line generation, target ref, from-SHA, and to-SHA. It stores the
canonical raw-delivery hash, every provider delivery/event identity observed for that
operation, the enriched operation, and the prepare/effect/receipt/terminal history. Explicit
dispatch requires a caller idempotency key.

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
its candidate and optional branch evidence as history. Optional-line cancellation requires
the current generation lock to be `open` and atomically changes it to `terminal`; it refuses
while a ref effect or promotion owns the lock. A post-promotion installed test-host rollback uses an earlier
proved artifact digest selected by the exact release owner. A source rollback uses a
reviewed revert commit integrated into `main` and then a new release train. No rollback
moves `main` or a release branch backward.

**I-25 — Optional-line generation lock.** An optional-line integration uses compare-and-set
on the exact `(trainId, targetRef, lineGeneration)` lock from `open` to `effect_pending` and
holds it until authoritative readback records success, conflict, or terminal refusal. A
successful effect commits the integration and next generation atomically, terminates the old
lock, and creates the next generation's `open` lock. Promotion first proves zero prepared or
in-flight effects, then compare-and-sets that same generation lock from `open` to
`promotion_closed`, reads the ref, and commits the promotion. After the close, a receipt for
an older generation is historical only: it cannot invoke a provider, move a ref, advance the
current generation, or alter promoted state.

**I-26 — Responsibility offer lifecycle.** One train has at most one `pending` offer of each
purpose. Initial ownership, owner transfer, emergency owner transfer, and relief all use the
same lifecycle. Acceptance requires the exact capable live target session and stored
incarnation, state `pending`, time before the deadline, the stored expected train generation,
the stored expected line generation when present, and the stored origin owner epoch to equal
the current epoch. Only an initial-owner offer has no origin epoch. The first concurrent
acceptance compare-and-set wins. An ownership acceptance installs the successor epoch; a
relief acceptance installs the proposal-only grant. Either advances the train generation and
atomically supersedes every other pending ownership or relief offer from that origin epoch.
Target rejection changes it to
`rejected`; deadline processing changes it to `expired`; authorized withdrawal changes it
to `withdrawn`; reissue changes it to `superseded` and appends a successor linked by the
same reissue key. Each terminal transition stores actor, cause, time, acknowledgments, and
predecessor. The current owner remains responsible until an exact target atomically accepts
an ownership offer. Closing an owner epoch supersedes every remaining pending ownership or
relief offer and relief proposal from that epoch; only the new current owner can author a
later transfer. Accepted relief creates one proposal-only grant for the current owner epoch.
A dead or stale target cannot accept and causes exactly one deduped reissue-required
action and escalation; it does not select a successor.

**I-27 — Relief proposal lifecycle.** Filing a relief proposal changes no ownership, owner
epoch, responsibility offer, or owner-authored brief fact. Proposal acceptance requires the
exact current product owner, proposal state `pending`, matching origin owner epoch, and
matching expected train and optional line generation. It atomically changes the proposal to
`accepted` and creates one owner-authored `owner_transfer` offer bound to that same current
epoch and generations. Successor acceptance remains a separate I-26 CAS. The proposer can
withdraw a pending proposal; the current owner can reject it; deadline processing can expire
it; owner-epoch close supersedes it. Every terminal transition and replay preserves immutable
occurrence history.

## Architecture

### 1. Consolidated durable model

The implementation adds one release projection. It does not create a second task tracker.
Work items, assignments, attests, artifacts, and decision requests remain their current
authorities.

| Record | Mutable purpose | Immutable material |
| --- | --- | --- |
| `release_trains` | current state, currency, train generation, owner/brief/candidate pointers | repository id, candidate mode, optional branch identity, sponsor, creation audit |
| `release_responsibility_offers` and transition history | pending/terminal state and delivery coverage | purpose, origin owner epoch, expected train/line generations, exact target session key/incarnation, deadline, reason, predecessor, dedupe/reissue key, conditional relief expiry/scope, acknowledgments, actor/cause/time |
| `release_owner_epochs` | current epoch end fields | exact owner session, acceptance, start/end audit |
| `release_relief_grants` | revoked/expired/end-of-epoch state | accepted responsibility offer, owner epoch, exact relief session key/incarnation, expiry, proposal-only scope, actor/cause |
| `release_relief_proposals` and occurrence history | pending/terminal state | proposal id, train, origin owner epoch, expected train/line generations, proposer principal/cause/correlation, proposed successor/scope/reason, idempotency key, timestamps, predecessor occurrence |
| `release_repository_anchors` | no mutation | repository/ref/SHA, protection ruleset id/digest/readback, actor/cause |
| `release_brief_facts`, fact heads, and append-only fact versions | head advance only | stable identity and kind for every member, gate, risk, decision, readiness, go/no-go, and evidence fact; typed state, predecessor, actor/cause, sequence |
| `release_watch_facts`, heads, and append-only versions | head advance only | exact owner offer-or-epoch reference, watch generation, rebound predecessor, durable selector, trigger class, acknowledged cursor, next due time, dedupe key, state, reissue policy, predecessor, actor/cause, sequence |
| `release_brief_revisions` and exact fact bindings | no mutation after commit | row-derived canonical bytes/digest, ordered fact-version ids, counts/hashes, provenance, watch-version resolution map when rebound |
| `release_source_occurrences` and subject heads | append and head advance | typed cause, direct/parent projections, literal filters |
| `release_action_needs` and deliveries | action state/retry coverage | action kind, train/owner/candidate generations, owner-rebind history, latest candidate-pointer digest, source range, due time, attempts, acknowledgments, superseded target history |
| `release_integrations` | phase and authoritative outcome | target ref, expected/new head, introduced set, evidence, operation/effect ids |
| `release_line_generation_locks` | CAS state | train, target ref, exact line generation, state/owner operation, transition history |
| `release_candidate_generations` | superseded marker for optional lines | release, ordinal, mode, eligibility, candidate SHA, base SHA, anchor/ref/ruleset/ancestry, integration provenance, freeze/readback cause |
| `release_candidate_admissions` and provider-delivery identities | prepare/effect/receipt/terminal phase and first outcome | raw provider delivery/event identity and payload hash; enriched trigger kind, derived or caller key, repository/ref/from/to SHA, train/line generation, operation id |
| `release_candidate_bundles` and evidence bindings | no mutation after seal | source SHA, pipeline revision, run, artifact digests, host proofs |
| `release_promotions` | phase and authoritative outcome | mode, candidate SHA, bundle, reconciliation, owner, operation id |
| `release_tag_markers` | phase and authoritative outcome | tag name, promoted SHA, operation/effect ids |
| `release_events` | append-only | actor, cause, typed payload/hash, sequence, time |

One partial unique index enforces one active owner epoch per train. One partial unique index
enforces one nonterminal `release_line` train per repository/branch pair. One partial unique
index enforces one open action per release, owner epoch, brief generation, and action kind.
One partial unique index enforces one pending responsibility offer per train and purpose.
One lifetime unique index binds each
`(trainId, originOwnerEpochId, proposerPrincipal, idempotencyKey)` to one relief proposal,
including after terminal state. One partial unique index enforces one open
`refresh-readiness` action per train; that row names the current candidate generation and
latest pointer digest, and its target advances only in the candidate-pointer transaction.
One unique index enforces one branch-push admission per derived
`(trainId, lineGeneration, targetRef, fromSha, toSha)` key. Separate lifetime unique indexes
bind `(provider, repository, eventId)` and `(provider, deliveryId)` to one immutable raw
payload. A unique operation reservation on the provider-scoped event identity lets concurrent
enrichment recover one operation id.
One unique index reserves each repository/tag-name pair for one promotion.

Mechanism choice: ADD wins because Git refs alone cannot preserve product ownership,
review provenance, proof binding, or recovery after a lost external response. DELETE loses
because Mike requires a durable release responsibility and an exact frozen candidate SHA.
ACCEPT loses because an unreviewed or tag-built candidate is an explicitly rejected release
state. Optional release-line state is added only for the explicit concurrency, maintenance,
and patch cases; ordinary releases add no branch.

The repository anchor, offer/relief lifecycle, admission key, and line generation lock are one closed
set of rails for facts the substrate must recover without inference. DELETE loses the
required first-release provenance, owner reissue, automatic push admission, or optional
release mode respectively. ACCEPT loses because each missing fact permits an unreviewed
candidate, ownerless hold, duplicate run, or post-proof ref race.

Watch-version rebinding, origin-epoch/generation CAS, Gateway enrichment, durable relief
proposals, and candidate-pointer refresh actions are added because each owner ruling requires
recoverable identity and ordering across crashes. DELETE loses because the required watch,
delegation, provider-event, proposal, and stale-brief surfaces remain product obligations.
ACCEPT loses because a stale owner, duplicate run, unrecorded proposal, or unrefreshed brief
would become a silent release-authority error.

Revision-4 review findings trace in both directions as follows:

| Finding | Normative closure | Acceptance |
| --- | --- | --- |
| F1 review author not holder-bound | Independent evidence term; I-12; Architecture 4 | A-10 |
| F2 brief fields undefined | I-04; Architecture 3 closed schema | A-04, A-50, A-55 |
| F3 empty-range/arbitrary-base escape | Anchor term; I-12; Architecture 2 and 4 | A-11, A-12, A-54 |
| F4 optional ref-effect promotion race | Line generation lock term; I-25; Architecture 4 and 6 | A-28B, A-43 |
| F5 offer and relief lifecycle missing | Offer/relief terms; I-05, I-26; Architecture 2 | A-03B, A-46B, A-47 |
| F6 branch-push replay unkeyed | I-14, I-20; Architecture 5 | A-18C, A-35 |
| F7 decision terminal occurrences absent | I-07; Architecture 3 | A-05, A-06, A-48 |
| F8 provisional digests unnamed | Header rejection | A-53 |

Revision-5 review findings trace in both directions as follows:

| Finding | Normative closure | Acceptance |
| --- | --- | --- |
| F1 watch ownership cannot survive transfer | Watch term; I-05, I-26; Architecture 2 and 3 | A-03, A-46, A-55 |
| F2 stale or competing offers can accept | Offer and train-generation terms; I-26; Architecture 2 | A-03B, A-46, A-46B |
| F3 branch-push envelope has no production enrichment seam | Branch-push delivery term; I-14, I-20; Architecture 5 | A-18C, A-24, A-35 |
| F4 relief proposal has no durable lifecycle | Relief proposal term; I-27; Architecture 2, 9, and 10 | A-47 |
| F5 candidate pointer can change without durable refresh coverage | Candidate pointer term; I-15; Architecture 3 and 5 | A-49 |

### 2. Owner and brief lifecycle

`release-repository-anchor-create` is the one anchor mutation seam. An authorized merge
principal or admin names repository, ref `main`, and exact SHA. Tightbeam reads `main`,
requires it to equal that SHA, reads the active protection ruleset, verifies the four
I-12 protections, and appends the immutable anchor without changing a Git ref. A repository
with no protected-main anchor or proved prior promoted SHA cannot create a release train.

`release-create` runs one transaction that:

1. validates the sponsor, repository, exact target session, candidate mode, optional-line
   purpose/rationale when selected, initial brief, and offer deadline;
2. reads `main` and the active protection ruleset, requires direct push, force push,
   deletion, and administrator bypass to be disabled, and stores the ruleset id/digest;
3. verifies that the brief's base names the exact protected-main anchor or a proved prior
   promoted SHA and that an optional branch name is unused by another nonterminal
   train;
4. creates the pending train at train generation 0 with `main_snapshot` as the default mode
   and stores an optional immutable release-line identity only when explicitly selected;
5. commits the initial brief with `ownerEpochId = null` and
   `responsibilityOfferId = offerId`;
6. creates the `pending` `initial_owner` responsibility offer with null origin owner epoch,
   expected train generation 0, null expected line generation, its acceptance action, and
   delivery coverage;
7. appends the create, protection-readback, and brief-commit events.

`release-offer-create` is the single mutation seam for all four purposes. It records exact
target session key/incarnation, deadline, reason, predecessor offer id or null, stable
dedupe/reissue key, origin owner epoch, expected train generation, expected current line
generation for a `release_line` train or null for `main_snapshot`, delivery acknowledgment
state, actor, cause, and creation time. A relief
offer also stores its future grant expiry and the closed proposal-only scope. The
sponsor/admin creates or reissues an initial or emergency-owner offer with a reason. The
exact current owner creates or reissues an ordinary owner-transfer or relief offer. A
noninitial offer always binds the current owner epoch and generations at authoring. A
transfer offer does not end the current epoch, and a relief offer creates no grant.

`release-offer-accept` compares the caller credential and incarnation with the exact target
and re-reads target liveness and the authorization matrix. One transaction requires state
`pending`, time before the deadline, the expected train generation, the expected current line
generation when present, and the current origin epoch for a noninitial offer. It
compare-and-sets the train generation; changes the accepted offer to `accepted`; supersedes
every other pending ownership or relief offer from that origin epoch; stores terminal
actor/cause/time and acceptance acknowledgment; satisfies its action; and advances the train
generation. Concurrent acceptances therefore have one winner. A stale origin, train
generation, or line generation returns `responsibility_offer_stale` and changes no row.

For `initial_owner`, the transaction opens the first epoch, activates the train, and installs
the owner pointer. For `owner_transfer` or `emergency_owner_transfer`, it closes the prior
epoch, supersedes every remaining pending relief proposal from that epoch, and opens the
target epoch. For `relief`, it creates one proposal-only grant with the offer's stored
expiry/scope, bound to the still-current owner epoch.

Every ownership acceptance also appends successor versions for every current active watch on
the pending, active, or shipped train whose owner reference names the accepted initial offer
or closing epoch. It preserves the
watch id and all selector, trigger, cursor, due-time, dedupe, and reissue fields; increments
the watch generation; sets the new epoch owner; sets `reboundFromWatchVersionId` to the old
version; and marks the old version `superseded`. The same transaction appends a mechanically
rebound canonical brief with unchanged product facts, stores the complete old-to-new map on
the acceptance and both brief-history entries, makes the rebound brief current, and records
the new owner's acknowledgment. It also terminates pending delivery to the prior watch owner
and atomically rebinds the same open watched-fact action from the closing epoch to the new
epoch with immutable owner-binding history, then appends delivery coverage to the new exact owner. No read can
observe a current epoch with an old-epoch watch or a gap with no current watch. No existing
brief or watch version is rewritten.

The exact target can change a pending offer to `rejected`. The authorized offerer can change
it to `withdrawn`. `release-offer-expire` changes it to `expired` once at the stored deadline.
Reissue changes the pending predecessor to `superseded` and appends its successor in one
transaction. Every transition appends an immutable history fact with predecessor, actor,
cause, time, and acknowledgment state. No terminal offer can transition again.
The reissued successor captures the origin epoch and expected current generations at reissue
time; it does not copy stale CAS values from its predecessor.
Closing an owner epoch supersedes every still-pending offer whose origin names that epoch.
Only the new current owner can author a later ordinary transfer or relief offer.

A target retirement, stale incarnation, or loss of capability does not change a pending
offer to a false acceptance. The first such observation appends one terminal
acceptance-refusal fact while the offer remains pending, opens exactly one action keyed by
the offer's reissue key, and sends one high-attention Main escalation. Repeated observations
coalesce into that action. An authorized human or owner
must select the successor; the substrate does not. The current owner remains responsible
until an ownership successor accepts atomically.

`release-relief-revoke` requires the exact owner while the grant's epoch is current. Expiry,
revocation, or epoch end closes the accepted grant. A closed grant can read history as an
authorized reader but creates no proposal or owner mutation.

`release-relief-proposal-file` is the only proposal-create seam. It requires an exact live
session/incarnation with a current unexpired relief grant whose closed scope permits
ownership-transfer proposals. The caller supplies a proposed exact successor session and
incarnation, scope `{ "purpose": "owner_transfer", "offerDeadline": <future timestamp> }`,
reason, proposal expiry, and idempotency key. The Gateway derives and stores `proposalId`,
`trainId`, current `originOwnerEpochId`, expected train generation, expected current line
generation or null, proposer principal, cause, correlation, state `pending`, `createdAt`,
`expiresAt`, null terminal time, and the first occurrence. Replaying the same proposer and
idempotency key with identical bytes returns the same proposal; different bytes return
`relief_proposal_identity_mismatch`. Filing changes no ownership, offer, or brief row.
The seam performs that lifetime identity lookup before create authorization. The exact
original proposer can replay identical bytes and receive the existing readable proposal after
its grant or proposal becomes terminal; only creation of a new identity requires a live grant.

`release-relief-proposal-accept` requires the exact current product owner and compare-and-sets
state `pending`, origin epoch, expected train generation, expected line generation, and time
before expiry. It revalidates the proposed successor as an exact capable live target under
the ordinary owner-transfer authorization row. In one transaction it appends the accepted
occurrence and creates one
owner-authored pending `owner_transfer` offer to the proposed exact successor, bound to the
same current epoch and generations. If another pending owner-transfer offer exists, it
returns `owner_transfer_offer_pending` and leaves the proposal pending. The proposed
successor separately accepts through `release-offer-accept`; proposal acceptance never opens
an epoch. The current owner can reject a pending proposal, its exact proposer can withdraw
it, and `process:tightbeam` can expire it at `expiresAt`. Owner-epoch close changes every
remaining pending proposal from that epoch to `superseded`. Each transition appends actor,
cause, correlation, time, predecessor occurrence, and terminal state before publication;
retry and crash recovery reuse the proposal id and occurrence identity.

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

`release-brief/v1` has required keys: `schema`, `target`, `candidate`, `members`, `watches`,
`gates`, `risks`, `decisions`, `readiness`, `goNoGo`, and `evidence`. Arrays can be empty.
Required objects cannot be omitted. Unknown keys at the document or item level are refused.
The `schema` value is exactly `release-brief/v1`.

The target object is `{ "repository": "github:owner/repo", "releaseName": "1.2.3" }`.
`releaseName` is a product label, not a tag trigger.

The candidate object is:

```json
{
  "repository": "github:owner/repo",
  "mode": "main_snapshot",
  "sourceRef": "refs/heads/main",
  "releaseLinePurpose": null,
  "refreshWithinMs": 86400000,
  "baseSha": "89abcdef0123456789abcdef0123456789abcdef",
  "candidateGenerationId": "rcg_...",
  "eligibility": "releasable",
  "candidateSha": "0123456789abcdef0123456789abcdef01234567",
  "candidateBundleId": "rcb_...",
  "candidatePointerDigest": "<sha256>"
}
```

A brief can use `null` for generation, eligibility, SHA, and bundle before the first
candidate exists. Generation id, eligibility, and candidate SHA are null or non-null
together. `candidatePointerDigest` is always the SHA-256 of the canonical ordered tuple
`(candidateGenerationId, eligibility, candidateSha, candidateBundleId)`, including its null
values. `refreshWithinMs` is a positive product-authored bound for delivery and escalation of
candidate-pointer refresh actions; it is not part of the tuple and does not decide readiness.
A non-null bundle requires a non-null releasable generation and resolves to that generation.
Candidate repository equals target
repository. `main_snapshot` requires source ref `refs/heads/main` and null line purpose.
`release_line` requires the registered branch ref and its declared non-null purpose.
The owner must commit a covering brief after a candidate generation or bundle changes.
`baseSha` is the product-authored exclusive baseline for reviewed-integration coverage. It
must name the exact protected-main anchor or a proved prior promoted SHA in the same
repository. A `releasable` generation requires it to be a strict ancestor of `candidateSha`.
Equality requires eligibility `no_change` and a null bundle.

The remaining collections and declarations use these closed item schemas:

- `members[]`: `{ "factId": <id>, "factVersionId": <id>, "kind": <kind>, "id": <id> }`, where kind is
  `work_item | assignment | artifact | decision_request` and the id resolves to that kind.
- `watches[]`: `{ "factId": <id>, "factVersionId": <id>,
  "owner": { "ownerEpochId": <id|null>, "responsibilityOfferId": <id|null> },
  "watchGeneration": <nonnegative integer>,
  "reboundFromWatchVersionId": <id|null>,
  "selector": { "factKind": "gate"|"risk"|"evidence", "factId": <id> },
  "triggerClass": "gate_state_changed"|"risk_state_changed"|"evidence_added"|
  "evidence_replaced", "sourceOccurrenceKind": <kind|null>,
  "sourceVerdictKind": <string|null>, "acknowledgedCursor": <integer>,
  "nextDueAt": <timestamp|null>, "dedupeKey": <string>,
  "state": "active"|"superseded"|"retired",
  "reissuePolicy": "coalesce_until_covered"|"supersede_after_acknowledged",
  "refreshWithinMs": <positive integer> }`. A source occurrence filter is allowed only for
  an evidence trigger. Exactly one owner field is non-null. A pending initial brief uses its
  initial responsibility offer; an active or shipped current brief uses its owner epoch.
  An initial watch has generation 0 and null rebound predecessor. Each ownership acceptance
  increments the generation and names the exact prior version. Decision
  occurrence values are the nine `decision-request-*` values
  in I-07; attest filters distinguish progress, completion, surrender, and exact verdict
  kind.
- `gates[]`: `{ "factId": <id>, "factVersionId": <id>, "id": <string>,
  "kind": "candidate_bytes"|"decision",
  "status": "open"|"satisfied", "candidateBundleId": <id|null>,
  "evidenceRefs": [<evidence id>...] }`. A candidate-bytes gate requires the selected bundle
  id when satisfied. An open candidate-bytes gate can use null until a bundle is selected. A
  decision gate requires null candidate bundle.
- `risks[]`: `{ "factId": <id>, "factVersionId": <id>, "id": <string>, "statement": <string>,
  "status": "open"|"accepted"|"mitigated", "rationale": <string|null>,
  "evidenceRefs": [<evidence id>...] }`. Accepted and mitigated risks require rationale.
- `decisions[]`: `{ "factId": <id>, "factVersionId": <id>, "id": <string>, "question": <string>,
  "status": "open"|"ruled"|"withdrawn"|"superseded", "ruling": <string|null>,
  "rationale": <string|null>, "decisionRequestId": <id|null>,
  "evidenceRefs": [<evidence id>...] }`. A ruled decision requires ruling and rationale;
  withdrawn or superseded requires rationale and null ruling; open requires null ruling.
- `readiness`: `{ "factId": <id>, "factVersionId": <id>,
  "state": "undecided"|"ready"|"not_ready",
  "rationale": <string|null>, "evidenceRefs": [<evidence id>...] }`. `ready` and
  `not_ready` require rationale.
- `goNoGo`: `{ "factId": <id>, "factVersionId": <id>,
  "decision": "undecided"|"go"|"no-go", "rationale": <string|null>,
  "evidenceRefs": [<evidence id>...] }`. `go` and `no-go` require rationale.
- `evidence[]`: `{ "factId": <id>, "factVersionId": <id>, "id": <string>,
  "kind": "artifact"|"attest"|"candidate_bundle"|
  "provider_readback"|"decision_request", "refId": <id>,
  "candidateGenerationId": <id|null>, "candidateBundleId": <id|null>,
  "sourceSha": <40-hex|null>, "artifactDigest": <sha256|null> }`.

Fact ids are stable within a train; fact-version ids are immutable and resolve to that fact.
Every version stores its predecessor version or null, common record state
`active | superseded | retired`,
the displayed kind-specific state, actor, cause, and source sequence. The current brief binds
only active exact versions. A retired version preserves removal history and cannot appear as
a current member, watch, gate, risk, decision, readiness, go/no-go, or evidence binding.
For a watch, a superseded version preserves ownership-rebinding history and likewise cannot
appear in a current brief.
Reference
ids resolve to an item or durable row of the declared kind. Candidate-byte evidence requires
generation id, bundle id, source SHA, and artifact digest. Evidence not bound to candidate
bytes uses null for each candidate-only field it cannot substantiate.

A watch selector resolves to one durable fact identity. A gate or risk selector requires an
active version in the same brief. An evidence identity can have no version yet; in that case
its immutable identity stores the owner-declared source subject and closed filter, and the
first matching durable occurrence appends version 1. This reservation is a selector, not
evidence and not a readiness fact.

The canonical encoder reads the exact bound fact-version rows, emits document keys in the
required-key order above and item keys in the displayed schema order, and sorts set-like
arrays by `(factId, factVersionId)`. Evidence fact versions that share one source occurrence
sort their direct projection before their effort-parent projection, then by subject kind/id.
It emits UTF-8 JSON with no insignificant whitespace and hashes those exact bytes plus each
ordered normalized collection manifest. Stored bytes, A-48 action order, and A-50 content
must all recompute from these rows and sequences.

The substrate validates this structure and stores actor/cause. It does not summarize, rule,
waive, accept risk, declare readiness, or choose go/no-go.

`release-brief-fact-append` is the only writer of fact heads and versions. An owner brief
commit uses it for product-authored member, watch, gate, risk, decision, readiness, go/no-go,
and evidence versions. The watch action path uses it only for the rule-determined cursor,
due-time, state, and predecessor transition. Ownership acceptance uses it only for the
rule-determined owner epoch, watch generation, rebound predecessor, and
superseded-to-active transition described in Architecture 2. A source transaction can use it only to append
the exact typed evidence projection of its durable occurrence; neither path can author gate,
risk, readiness, or go/no-go judgment. The brief commit binds the resulting exact versions
and derives bytes from them in the same transaction.

One source mutation creates one cause and occurrence with `occurrenceId`, causal predecessor
occurrence id or null, dedupe identity, and a canonical ordered projection set. Assignment,
attest, and artifact writes project directly and through their stored `workItemId` when
present. Decision-request writes follow this closed rule:

- direct projection: exact decision request for each request kind;
- effort parent projection: stored `assignmentId`, then the assignment's stored
  `workItemId`, when both exist;
- statute parent projection: absent unless a future separately reviewed schema gives the
  statute request a structural parent.

Decision requests append exact occurrences for opened, delivered, reminder, acknowledged,
withdrawn, superseded, expired, resolved, and delivery-failed. A transition projects
directly to the request and, for an effort request only, through its stored assignment to
that assignment's stored work item. No occurrence is collapsed into another or erased by a
terminal projection. Each occurrence stores its source operation id. Its dedupe identity is
the tuple `(decisionRequestId, occurrenceKind, causalPredecessorOccurrenceId,
sourceOperationId)`: replay of that tuple returns the existing occurrence, while a later
reminder with a new source operation id appends a new causally linked occurrence.

The source transaction advances projected subject heads atomically. When an active
owner-authored evidence selector names that exact source kind and subject, the same
transaction appends durable evidence fact versions for its ordered direct and parent
projections. An unselected source occurrence appends no brief fact. Gate and risk mutation
seams invoke `release-brief-fact-append` for their typed versions. Matching uses a watch's durable fact selector,
trigger class, and closed source filter; it does not scan prose. A raw source occurrence,
note, delivery, or prose change that creates no gate, risk, or evidence fact version is not
a watch-meaningful change and cannot stale a brief. Candidate-pointer change is the separate
structural staleness trigger below. Direct and parent evidence versions for one
source sequence reduce to one ordered action update.

Closed attest occurrence kinds distinguish progress, completion, surrender, and verdict.
Verdict occurrences store exact `verdictKind`. A reviewed-clean evidence selector therefore
ignores a progress attest and a changes-requested verdict.

Each product-declared watch supplies a positive `refreshWithinMs`, exact owner reference,
acknowledged fact cursor, next due time, dedupe key, state, watch generation, rebound
predecessor, and reissue policy. The number
bounds owner response time; it does not decide materiality or readiness. The first matching
fact version after the acknowledged cursor atomically makes currency `stale` and opens one
`refresh-brief` action keyed by watch dedupe key. Later matching fact sequences under
`coalesce_until_covered` coalesce into that action, preserve ordered fact ids/count, and move
the due time only to the earliest declared deadline. Under
`supersede_after_acknowledged`, acknowledgment advances the cursor; the next matching fact
version terminates the prior action as superseded and opens one linked successor. For a
fact at `T`, due time is `T + refreshWithinMs`. One source sequence increments the action
count once when direct and parent evidence both match.

The candidate-pointer mutation seam computes the canonical tuple and digest before commit.
If its bytes equal the current tuple, it returns the existing pointer and creates no
staleness or action occurrence. Otherwise, the same transaction advances the pointer, marks
the covering current brief stale, and opens one `refresh-readiness` action targeted by
`(trainId, currentCandidateGenerationId, latestPointerDigest)` with due time equal to the
pointer occurrence time plus the current brief's `candidate.refreshWithinMs`. If an earlier
`refresh-readiness` action remains open, the transaction terminates that target as
`superseded` and appends one linked successor for the latest tuple; it preserves ordered
pointer-change occurrences and leaves exactly one open action. Freeze, a successful optional
line-generation advance, candidate-bundle selection, and candidate-bundle replacement use
this seam. Sealing or replaying a selected bundle leaves the tuple unchanged and creates no
pointer occurrence. This structural trigger
records no judgment about materiality or readiness.

An owner brief commit recomputes the candidate pointer from current rows. A supplied tuple or
digest that differs returns `candidate_pointer_mismatch`, writes no brief revision, and does
not close `refresh-readiness`. An exact tuple and digest can commit a new covering brief and
atomically close the matching latest action.

Each pending offer, watched-fact stale brief generation, and uncovered latest candidate pointer has one
action with a pending delivery or
durable retry time. Offer delivery targets the exact offered session/incarnation; refresh
delivery targets the exact owner session. Failure records cause and sends one
notice to the derived owner user's Main. Acknowledgment proves receipt and does not satisfy
the action. Exact target acceptance satisfies an owner action; a covering owner-committed
brief satisfies a watched-fact refresh action. Only a new owner-committed brief whose
candidate tuple and digest equal the latest pointer satisfies a `refresh-readiness` action.
Boot recovery restores missing delivery coverage and
reuses the open action id. If an action remains open at `dueAt`, the substrate records one
deadline escalation and sends one high-attention marker to Main. Main delivery grants no
owner authority.

Delivery retry ordinals use waits of 5, 10, 20, 40, then 60 seconds; later retries remain
60 seconds apart. The delivery row persists ordinal and `retryAt` before scheduling the
wake. Satisfaction or cancellation suppresses a pending retry by action id.

### 4. Reviewed integration, candidate freeze, and optional release line

The repository protects `main`. A reviewed integration operation records the expected main
head, exact reviewed feature commits, their independent reviewed-clean attests, the
resulting main head, remote ref, protection-ruleset identity/digest, exact ancestry result,
actor/cause, and provider readback. Each optional-line integration stores the same remote
ref, ruleset, ancestry, and exact reviewed-clean material for its target generation. The
commit set between expected and new head cannot contain an unreviewed feature. A merge commit with content not represented
by its reviewed parents requires its own exact reviewed-clean attest. A merge commit counts
as content-free only when its tree equals the provider-computed conflict-free merge of its
recorded parents. For each cited verdict, the validator requires
`verdict.bySession == reviewAssignment.holderKey`, requires that holder to differ from
the producing assignment holder, and verifies the exact structured repository/SHA ref.

In default mode, `release-candidate-freeze <releaseId> --ref main --sha <C>` is the candidate
mutation seam. One checked operation:

1. locks the train and verifies mode `main_snapshot`;
2. re-reads `main` and requires `main == C` at that point;
3. re-reads the active protection ruleset and requires its identity/digest and four enforced
   protections to match the train-creation readback;
4. reads and stores the exact remote ref, protected-main anchor or proved prior promoted SHA,
   ruleset identity/digest, and `baseSha` ancestry to C;
5. if `baseSha` is a strict ancestor of C, verifies each commit in the exclusive
   `baseSha..C` set against exact holder-authored reviewed-clean integration evidence and
   sets eligibility `releasable`;
6. if `baseSha == C`, proves equality and sets eligibility `no_change`; any other ancestry
   returns `invalid_candidate_base`;
7. writes one immutable candidate generation for C and appends the freeze event.

Later movement of `main` creates no generation on that train and does not stale C. A new
default candidate requires a new release train; it does not rewrite the frozen generation.
A second freeze with the same operation key returns the first result. A second freeze with
a different candidate or key returns `candidate_already_frozen`.

In optional mode, `release-line-create` creates the protected branch at the exact brief
`baseSha`. That SHA must be the exact protected-main anchor or a SHA recorded by a prior
succeeded promotion. The operation rechecks main and branch protection,
records the anchor/promotion source and ruleset digest before the provider effect, and requires
readback of the registered protected branch at that SHA. Branch creation creates no
candidate generation; it creates the `open` train/ref/line-generation-0 lock. The first
reviewed descendant integration creates line generation 1 and candidate generation 1.

`release-line-integrate` is the only optional-line mutation seam. It accepts source kind
`reviewed-feature | reviewed-backport | current-main-sync`, expected old line head, exact
source and result SHAs, reviewed-clean evidence for each introduced feature/backport and
any content-bearing integration commit, parents, exact owner, and idempotency key. The
transaction locks and re-reads the line, validates graph/evidence, and writes a prepared
operation. In the same transaction it compare-and-sets the exact train/ref/current-generation
lock from `open` to `effect_pending` owned by that operation. The executor uses a conditional
fast-forward ref update. Readback resolves:

- line equals new SHA: atomically record one integration and one releasable new generation,
  terminate the old lock, and create the new generation's `open` lock;
- line equals expected old SHA after a retryable result: retry the same effect;
- line equals another SHA: record `branch_head_conflict`, set `needs_attention`, and change
  no generation pointer;
- provider reports non-fast-forward, deletion, force, direct unreviewed push, or bypass:
  record `branch_rewrite_forbidden` and change no generation pointer.

A terminal refusal or conflict compare-and-sets `effect_pending` back to `open` for the same
generation when the train remains active. Cancellation changes an `open` current-generation
lock to `terminal`; promotion changes it to `promotion_closed`. A lost response keeps
`effect_pending`, uses the same effect id and line readback, and creates no second integration
or generation. Promotion cannot close that generation while the state persists. Once a
newer generation or promotion terminates the old lock, any late receipt is appended as
historical audit only and performs zero provider or current-state mutation.

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

The explicit candidate workflow accepts the two explicit-dispatch envelopes below. The
Gateway accepts the raw provider delivery between them and produces the enriched internal
branch-push operation described afterward:

```json
{"kind":"explicit_dispatch","idempotencyKey":"<key>","repository":"github:owner/repo","branch":"main","sha":"<frozen-sha>","generationId":"rcg_..."}
```

```json
{"provider":"github","deliveryId":"<provider-delivery-id>","eventId":"<provider-event-id>","repository":"github:owner/repo","ref":"refs/heads/release/<train-id>","beforeSha":"<old-sha>","afterSha":"<new-sha>"}
```

```json
{"kind":"explicit_dispatch","idempotencyKey":"<key>","repository":"github:owner/repo","branch":"release/<train-id>","sha":"<sha>","generationId":"rcg_..."}
```

Default admission resolves the train by generation id and requires branch `main`, envelope
SHA equal to the frozen generation SHA, and Git-object readback for that SHA. It does not
require current `main` to remain at the frozen SHA. A generic main-push envelope creates no
candidate run.

`release-branch-push-ingest` is the sole production seam for the raw branch-push delivery.
It strips caller-supplied operation, train, line-generation, and idempotency fields. It first
inserts or reads the durable `(provider, repository, eventId)` identity and canonical
raw-payload hash. One event
identity can collect multiple delivery ids, but each event or delivery identity binds one
immutable payload. Concurrent ingestion of the same identity reserves and recovers one
operation id.

The ingestion transaction then locks the repository/ref selector. If no nonterminal
`release_line` train registers that exact ref, it records terminal
`ignored_non_release_line_event` and invokes no release or CI operation. Otherwise it locks
the current line-generation row, resolves train id and line generation, maps before/after to
from/to SHA, derives `(trainId, lineGeneration, targetRef, fromSha, toSha)`, and commits the
complete enriched admission row before production evaluation. A second event identity with
the same derived tuple converges on that row and records its delivery identity.

Admission re-locks the exact enriched train/ref/generation and re-reads the line. Enriched
to-SHA, line readback, and current generation SHA must match in one decision. If generation
or head changed after enrichment, it records terminal `stale_candidate_head` and creates no
candidate run. Otherwise the row advances through `prepared`, `effect_pending`,
`receipt_recorded`, and `terminal`; the CI invocation receipt is durable before terminal
publication. Replay before, during, or after those phases returns the same operation and
first run or non-run result and invokes CI zero additional times. Reusing one provider event
or delivery identity with another repository, ref, before-SHA, or after-SHA returns
`provider_event_identity_mismatch`. Explicit dispatch inserts or reads one row keyed by owner
session and caller idempotency key.

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

`release-promote` uses a database-only operation and read-only Git verification. In
`main_snapshot` mode, one transaction locks the train; re-reads owner epoch, current brief,
generation, candidate bundle, gates, package digests, and installed test-host proof;
verifies the frozen SHA remains readable and its freeze event recorded that SHA as main
head; validates I-17; writes one succeeded promotion; and sets the train to `shipped`.
Current main can name a later reviewed commit.

In `release_line` mode, promotion uses this fenced sequence:

1. An admission transaction locks the train and exact current
   `(trainId, targetRef, lineGeneration)` row, verifies zero prepared, `effect_pending`,
   in-progress, or outcome-unknown ref operations for that generation, validates non-ref
   I-17 preconditions, compare-and-sets `open` to `promotion_closed` owned by the promotion
   operation, closes new integration admission, and commits that phase.
2. Tightbeam reads the optional branch and requires its head to equal the current generation
   SHA. It validates the closed reconciliation decision and cited evidence.
3. A completion transaction requires the same lock owner and unchanged generation, writes
   one succeeded promotion with exact mode/SHA/bundle/digests, changes the train to
   `shipped`, and changes the lock to `terminal`.
4. A stale readback or failed precondition records the typed refusal and returns the lock
   to `open` only by compare-and-set on the same unchanged generation; crash recovery retains
   `promotion_closed` and repeats readback with the same operation id before choosing
   completion or refusal.

Integration admission and integration recovery invoke zero line effects while the lock is
`promotion_closed` or `terminal`. A receipt for an effect prepared against an older
generation is historical only and cannot reopen a lock, invoke the provider, advance a ref
or generation, or alter the promotion. Promotion invokes no Git update, build, package,
deployment, or tag effect. A retry with the same operation id returns the first terminal
result.

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
frozen candidate remains retained history. For an optional line, the cancellation
transaction requires the current generation lock to be `open`, changes it to `terminal`, and
makes the branch read-only retained history. A pending ref effect or promotion close returns
`release_line_mutation_pending`; the caller retries after authoritative recovery.
Generations, runs, bundles, and events remain queryable.

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
| Register repository release anchor | authorized merge principal or admin after exact protection readback |
| Accept or reject pending unexpired offer | exact capable live target session and stored incarnation |
| Expire offer | `process:tightbeam` at stored deadline |
| Withdraw/reissue initial or emergency-owner offer | sponsor/admin with reason |
| Withdraw/reissue owner-transfer or relief offer | exact current owner session |
| Commit/ack brief; decide; freeze candidate; optional-line integrate; promote; create tag | exact current owner session |
| Integrate a reviewed feature into `main` | existing authorized merge principal after exact reviewed-clean gate |
| Propose brief/evidence | exact owner or exact live session/incarnation with current unexpired relief grant |
| File relief proposal | exact live session/incarnation with a current unexpired relief grant whose scope permits ownership-transfer proposals |
| Withdraw relief proposal | exact proposer principal while proposal is pending |
| Accept/reject relief proposal | exact current owner session after origin-epoch/generation CAS |
| Expire relief proposal | `process:tightbeam` at stored deadline |
| Offer relief; revoke accepted relief; ordinary transfer | exact current owner session |
| Emergency transfer | sponsor/admin with reason |
| Cancel before promotion | exact owner or sponsor/admin with reason |
| Ingest optional-line provider push | authenticated provider Gateway principal; caller supplies only provider delivery/event identity, repository, ref, before-SHA, and after-SHA |
| Admit enriched optional-line push CI | authenticated CI process after exact train/ref/generation/SHA checks |
| Admit explicit CI | exact owner request executed by authenticated CI process |
| Record package/test proof | authenticated CI/deployment process bound to operation id |
| Execute Git/provider effects and recovery | `process:tightbeam` using prepared operation |
| Roll back installed test-host package | exact current release owner with proved digest |

The gateway derives org, caller, exact session, owner epoch, actor, cause, hashes, sequences,
times, branch-push operation ids, train/line generation, idempotency keys, and effect ids. It
validates raw provider delivery/event identities against their immutable payload rows and the
enriched operation against its admission row. It strips caller-supplied audit and enrichment
fields.
Sponsor/admin emergency power does not bypass branch, evidence, bundle, or promotion
invariants.

### 10. Read, observability, and compatibility

`release-get` and `GET /api/releases/:id` return one atomic snapshot with canonical brief
bytes, digest, exact fact-version bindings and history, owner epoch, responsibility offers,
relief grants, relief proposals and occurrence histories, currency, watches/cursors and
rebind maps, open actions and candidate-pointer target history, repository
anchor and protection digest, candidate mode, frozen main SHA or
optional-line identity/head, current generation, integration provenance, candidate runs,
bundle/artifact digests, installed-host proof, reconciliation decision,
line generation lock, promotion phase, tag marker state, rollback records, and requested
event page.

`release-brief-get`, generation-by-id, bundle-by-id, integration-by-id, and promotion-by-id
return immutable historical records. Clients recompute canonical content and manifest
hashes. Integrity mismatch returns `needs_attention`; it does not return `current`.

The event stream exposes typed events for offer lifecycle, owner epoch, relief grant and
proposal lifecycle,
repository anchor/protection, brief, decision-request lifecycle, source match, action,
reviewed main integration, main candidate freeze, optional-line generation-lock/preparation/outcome/
refusal, generation supersession, candidate-pointer refresh, raw provider delivery,
Gateway enrichment, CI admission/replay/refusal,
bundle seal/refusal, promotion phases/readback, tag marker phases/conflict, and rollback.
Each refusal carries principal, cause, repository, ref, expected SHA, observed SHA, and
operation id when those values exist.

Migration is additive. Existing work rows, decision requests, roles, artifacts, wakes,
messages, and event rows remain byte-identical. Existing repositories get no train. A train
gets no release branch unless its creation declaration selects `release_line` and the exact
target accepts that declaration as owner. Generic legacy tag workflows can continue for
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
before acceptance, then the initial brief has `ownerEpochId = null`, the exact responsibility
offer id,
author, and commit event; every initial watch owner reference names that offer; and no owner
epoch exists. When the exact target accepts, then one epoch opens; each active offer-bound
watch gets one active epoch-bound successor with the same watch id, generation incremented,
and `reboundFromWatchVersionId` naming its superseded predecessor; one complete old-to-new
map appears on the acceptance and brief history; and one acknowledgment binds the epoch to
the mechanically rebound brief. The initial brief and watch versions remain byte-identical,
pending delivery to the offer target is terminated, the same open action gains delivery
coverage to the new exact owner with an immutable owner-rebind occurrence, and no read
exposes a zero-watch or offer-bound current
snapshot after the epoch opens.

**A-03B — Unified offer closure and reissue.** Given each purpose `initial_owner`,
`owner_transfer`, `emergency_owner_transfer`, and `relief` in turn, when its exact target
accepts, rejects, its deadline arrives, its offerer withdraws, or its offerer reissues, then
the pending row changes once to `accepted`, `rejected`, `expired`, `withdrawn`, or
`superseded`, with exact target session/incarnation, deadline, reason, predecessor,
dedupe/reissue key, acknowledgments, and terminal actor/cause/time retained. A later
transition returns the matching typed refusal. Reissue appends one linked successor and
preserves the predecessor's history.

Given an initial offer, it stores null origin epoch, expected train generation 0, and null
line generation. Given any noninitial offer, it stores the exact current origin epoch and
train generation plus the exact current line generation for optional mode. Acceptance after
any stored value becomes stale returns `responsibility_offer_stale` and creates no epoch or
grant. Given pending offers from one epoch, race acceptances in separate fixtures for
`owner_transfer` against `emergency_owner_transfer`, `owner_transfer` against `relief`, and
`emergency_owner_transfer` against `relief`. Exactly one train-generation CAS wins. An
ownership winner installs one successor epoch; a relief winner installs one grant. In each
fixture every other pending ownership or relief offer from the origin becomes `superseded`,
with occurrence history retained. Closing an
epoch supersedes all remaining pending origin offers, and only the new current owner can
author a later ordinary transfer.

**A-04 — Atomic brief.** Given a fault after each brief child write, when commit runs, then
the transaction rolls back and the prior current pointer remains. Given no fault, the
durable identities and exact versions for members, watches, gates, risks, decisions,
readiness, go/no-go, and evidence, plus row-derived canonical bytes, digest, bases, counts,
hashes, event, acknowledgment, and pointer appear together. Each version retains
predecessor, typed state, actor, cause, and sequence; a watch also retains owner, selector,
trigger, watch generation, rebound predecessor, acknowledged cursor, next due time, dedupe
key, state, and reissue policy. Given
supplied bytes differ from the deterministic row projection, or given
each missing required key, unknown key, invalid enum, duplicate item id, unresolved ref,
invalid watch filter, or incomplete candidate-byte evidence in turn, commit returns
`invalid_release_brief` and writes zero revision rows.

**A-05 — Decision request direct and effort parent.** Given an effort request with an
assignment whose `workItemId` is `wi_1`, when opened, delivered, reminded, acknowledged,
withdrawn, superseded, expired, resolved, and delivery-failed occur in separate fixtures,
then each exact lifecycle occurrence projects to the request and `wi_1` through the stored
assignment path and retains its causal predecessor occurrence id and dedupe identity.
Replay of the same source operation creates no duplicate; a later reminder with a new source
operation id appends one linked reminder.

**A-06 — Statute request direct only.** Given a statute request with `assignmentId = null`,
when the same nine lifecycle occurrences run in separate fixtures, then each occurrence
projects to the request, creates no parent work-item projection, retains predecessor and
dedupe identity, and cannot erase or collapse another occurrence. Replay of an occurrence's
source operation creates no duplicate.

**A-07 — Reader allow.** Given an authenticated same-org session that is not owner, sponsor,
or relief, when it reads current and historical release records, then it receives canonical
bytes and evidence metadata and can verify their hashes.

**A-08 — Reader deny.** Given an unauthenticated caller and an authenticated cross-org
caller, when each reads the same release id, then each receives byte-equivalent
`release_not_found` responses and no content or existence metadata.

### Default main path and optional release line

**A-09 — Main snapshot is default.** Given a train create request with no mode field, when
creation commits, then mode is `main_snapshot`, no release branch identity or provider
mutation exists, and the initial brief records main as the candidate source ref. The only
Git-provider interaction is the required read-only main/protection readback.

**A-10 — Reviewed main integration.** Given feature SHA F with independent reviewed-clean
evidence for F and expected main H, when an authorized merge principal integrates F, then
new main N is a fast-forward descendant of H and the integration record names F, its exact
structured commit-ref verdict, review-to-producer assignment link, distinct reviewer
holder key and verdict author, H, N, actor, and provider readback. Evidence for another
SHA, an unlinked review, a review assignment whose `holderKey` equals the producing
assignment's `holderKey`, the producer's own
verdict, or a verdict authored by any principal other than the review assignment's exact
`holderKey` returns `feature_review_mismatch` and calls no ref update. A content-bearing merge
commit without its own exact clean evidence returns `unreviewed_integration_commit`. The
record also stores remote ref, protection-ruleset identity/digest, and H-to-N ancestry; any
missing or mismatched value refuses the integration before the provider effect.

**A-11 — Exact main freeze.** Given current main C, a strict-ancestor protected anchor or
proved prior promoted SHA B, and a train in `main_snapshot`, when the
owner freezes C, then one generation records mode, repository, source ref main, base,
candidate C, eligibility `releasable`, anchor/promotion provenance, remote-ref readback,
protection-ruleset readback, ancestry, integration evidence, owner, and freeze readback.
Given requested D while main is C, then it returns
`candidate_not_current_main` and creates no generation. Given a base that is missing, from
another repository, not the exact protected-main anchor or proved prior promoted SHA, or is
neither equal to nor a strict ancestor of C, then it returns `invalid_candidate_base`. Given a changed or
insufficient protection ruleset, it returns `release_ref_unprotected`. Given an existing
frozen generation, a different-key freeze returns `candidate_already_frozen`; a same-key
retry returns the first result.

**A-12 — Unreviewed main-range refusal.** Given the product-authored base..C range contains
reviewed F and unreviewed U, when candidate freeze validates the range, then it returns
`unreviewed_main_commit`, creates no generation, and starts no CI.

Given `baseSha == C`, candidate freeze stores one generation with eligibility `no_change`
and the exact anchor/ref/ruleset/ancestry readback. Candidate dispatch, package, proof,
promotion, and tag requests return `candidate_no_change` and create zero such rows or
external effects; the empty range is not reviewed-release evidence.

**A-13 — Frozen main stability.** Given a frozen main candidate C and later reviewed main
head D, when the train is read and candidate CI is dispatched, then C remains its current
generation and source; D neither supersedes C nor transfers evidence into C.

**A-14 — Optional mode and identity.** Given a creation request explicitly selects
`release_line` with purpose `maintenance` and rationale, when train creation commits, then
it stores one immutable `release/<train-id>` identity. Missing purpose/rationale is refused.
A second nonterminal train using the same repository/name or a later mode change is refused. A base
that is neither the exact protected-main anchor nor a proved prior promoted SHA returns
`invalid_release_line_base` and calls no branch provider. Before the exact target accepts
and acknowledges the declaration, `release-line-create` returns `train_not_active` and
calls no branch provider. A successful branch create records no candidate generation; the
branch creates one open line-generation-0 lock, and the first reviewed descendant
integration records line and candidate generation 1.

**A-15 — Optional-line protection and review.** Given a reviewed feature or backport F and
expected line head H, when the owner integrates F, then new head N is a conditional
fast-forward descendant and the entry records exact review evidence. Given an unreviewed
introduced commit, content-bearing unreviewed merge commit, direct push, non-fast-forward,
force push, deletion, or admin bypass, then the attempt is refused, the line is unchanged,
and one typed refusal event records actor and cause.

**A-16 — Optional-line recovery and conflict.** Given the provider applies H->N and loses
the response, when recovery runs twice, then readback N produces one integration and one new
generation, terminates the old generation lock, creates one open new-generation lock, and
invokes no second effect.
Given provider head X instead, then `branch_head_conflict` sets `needs_attention`, releases
the same generation lock to `open`, and changes no generation pointer.

### Candidate admission, packages, evidence, and stale heads

**A-17 — Default explicit admission.** Given frozen main generation C, when the owner
dispatches candidate CI with branch main, generation id, and C, then one run binds C even if
main later names D. A different SHA, branch, or generation returns
`candidate_generation_mismatch` and starts zero runs. A `no_change` generation returns
`candidate_no_change` and starts zero runs.

**A-18 — Main push is not admission.** Given reviewed main push H->C with no prior frozen
generation dispatch, when candidate CI receives the event, then it starts zero candidate
runs and writes zero candidate evidence.

**A-18B — Optional-line admission.** Given a push or owner dispatch for the registered
optional line at current head C, when provider/generation readback is C, then one candidate
run starts. A different SHA or branch returns `stale_candidate_head` or
`wrong_release_branch` and starts zero runs.

**A-18C — Gateway push enrichment and replay.** Given raw provider delivery D1/event E1 with
only provider identity, repository, registered optional-line ref, H before-SHA, and C
after-SHA, when Gateway
ingestion runs, then it durably binds the raw payload, allocates one operation O, locks and
resolves the current train/line generation, derives
`(trainId, lineGeneration, ref, H, C)`, and commits that enriched operation before candidate
evaluation. No caller-supplied operation, train, generation, or key is accepted.

Given concurrent duplicate D1/E1 ingestion before prepare, during `effect_pending`, after
`receipt_recorded`, and after terminal publication, every delivery recovers O and one
candidate run exists. Given another delivery id D2 for E1 with identical raw bytes, or event
E2 that derives the same tuple, it converges on O and its first run or non-run result. Given
the first operation recorded a non-run refusal, every replay returns it and starts zero runs.
Reusing a provider delivery or event identity with another repository, ref, before-SHA, or
after-SHA returns `provider_event_identity_mismatch`. Given an unknown ref, ingestion records
one `ignored_non_release_line_event`, allocates no production admission, and invokes no CI.

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
after Gateway enrichment but before admission, when admission atomically checks the enriched
generation, provider ref, and current generation, then it starts zero C jobs, records the
terminal non-run result, and returns `stale_candidate_head`. Concurrent enrichment and a
generation advance either bind the old generation and receive that refusal or bind the new
generation; they never produce an admission with a fabricated generation.

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
| generation eligibility is `no_change` | `candidate_no_change` |
| frozen main SHA is missing or lacks valid freeze provenance | `frozen_main_candidate_invalid` |
| main protection readback is missing or insufficient | `release_ref_unprotected` |
| an optional-line effect is prepared, in progress, or outcome-unknown | `release_line_mutation_pending` |
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

**A-28B — Optional-line generation-lock races.** Given generation G at line head C, test the
same prepared C->D effect in four fixtures. If the effect and receipt commit before
promotion, then G+1/D becomes current and promotion can close only the G+1 lock. If the G
lock is `effect_pending` when promotion starts, promotion returns
`release_line_mutation_pending` and writes no promotion. If promotion compare-and-sets the G
lock to `promotion_closed` first, integration admission and recovery invoke zero ref effects.
If a C->D receipt arrives after promotion closes or commits G/C, it is historical only and
cannot move the ref, advance the generation, or alter promoted state. Given a crash after
effect prepare, provider effect, promotion close, ref readback, and database commit in turn,
recovery uses the same operation and generation lock and converges to the corresponding one
semantic outcome without reopening an older generation.

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
operation and its durable attempts. Given branch-push redelivery with the same or another
provider delivery/event identity and the same derived
`(trainId, lineGeneration, targetRef, fromSha, toSha)` key, Gateway enrichment resolves to the
first admission operation/result and preserves raw-delivery, enrichment,
prepare/effect/receipt history. Each external phase/target reuses one effect id.

**A-35B — Unknown external outcome.** Given an external timeout and unavailable readback,
when recovery reaches successive retry times, then it records the 5, 10, 20, 40, and
60-second readback waits, preserves `outcome_unknown`, and invokes no second effect. Given
readback `not_started`, then it invokes the same effect id once; given `in_progress`, it
schedules another readback.

**A-36 — Pre-promotion cancel.** Given an active unpromoted train, when the exact owner or
sponsor/admin with reason cancels it, then the train becomes canceled and history remains
readable. A default frozen candidate gains no branch. An optional line switches to retained
read-only and its current generation lock changes atomically from `open` to `terminal`.
Given `effect_pending` or `promotion_closed`, cancellation returns
`release_line_mutation_pending` and changes no train state.

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
storage, and installed test host, when an authorized principal records anchor A and its
protection digest, a reviewed feature integrates into main, the owner freezes exact main SHA
C strictly after A, CI runs by exact main+C dispatch, the package is installed and proved,
the owner promotes, and then creates the tag, then anchor/protection readback remains valid
and frozen SHA, checkout SHA, embedded package SHA, evidence SHA, promoted SHA, and tag
target equal C. No release branch exists and tag creation starts zero candidate jobs.

**A-43 — Crash-boundary journey.** Given injected process death after each durable phase and
external effect boundary for reviewed main integration, candidate freeze, optional-line
creation/integration, CI dispatch, package record, installed proof, promotion, tag, and
rollback, when boot recovery runs, then authoritative readback produces one semantic
outcome, retained attempts, and no inferred success. A crash with a generation lock in
`effect_pending` or `promotion_closed` never permits the competing ref or promotion effect
before recovery records a terminal readback. A late receipt for an older generation changes
no current ref, generation, promotion, or terminal state.

**A-44 — Read and event observability.** Given one success and one refusal for each release
operation, when an authorized reader requests the atomic snapshot and event page, then it
can identify responsibility-offer transition/relief state, target session/incarnation,
owner, origin epoch and train generation, relief-proposal state/occurrences, cause, fact/watch
versions, generations, rebound maps and cursors, candidate-pointer digest/action history,
anchor/protection digest, raw provider delivery, enriched operation, event id, derived key,
expected/observed refs, generation-lock owner/state, generation eligibility, bundle, digest,
phase, outcome, retry state, and stale reason without reading prose notes.

**A-45 — Real optional-line journey.** Given an explicitly selected concurrent stabilization
line, when reviewed features/backports enter its protected branch, its exact head C is
proved, the owner records reconciliation, promotes, and creates the tag, then line head,
checkout SHA, embedded package SHA, proof SHA, promoted SHA, and tag target equal C. A line
head change before admission invalidates the older generation.

**A-46 — Owner transfer and retirement.** Given an active owner and a pending transfer offer,
the current owner remains responsible until the exact capable live target session and stored
incarnation accepts. Acceptance then closes the prior epoch, opens one new epoch,
advances train generation, supersedes every other pending ownership/relief offer and relief
proposal from the closing epoch, and exposes no zero-or-two-owner snapshot. Every current
watch owned by the closing epoch gets one successor version owned by the new epoch, with
generation incremented and predecessor named; the old versions become superseded. The same
transaction makes the mechanically rebound brief current, acknowledges it for the new owner,
and stores a complete old-to-new map without rewriting prior bytes or exposing a watch-owner
gap. An open watch action retains its identity, terminates delivery to the closing owner, and
rebinds its owner epoch with immutable history before gaining delivery coverage to the
successor. Given a retired
owner, Main receives escalation but cannot act; sponsor/admin can offer transfer to one exact
live session. The same accepted-offer rule applies after `shipped` for tag and installed
test-host rollback authority.

**A-46B — Dead or stale offer target.** Given pending offers of all four purposes in turn,
when the target retires, its incarnation changes, or it ceases to satisfy the action's
existing authorization row, then acceptance returns `offer_target_unavailable`, creates no
epoch or grant, and opens exactly one deduped reissue-required action plus one escalation.
Repeated observations or restarts create no duplicate. When the authorized offerer selects
a new exact capable live target, then one linked successor carries the same reissue key and
the predecessor changes to `superseded`; the substrate never selects the successor.
Given a live target but stale origin epoch, train generation, or optional-line generation,
acceptance instead returns `responsibility_offer_stale`, creates no epoch or grant, and does
not revive or rebind the stale offer.

**A-47 — Relief boundary.** Given a pending relief offer with future grant expiry E and the
closed proposal-only scope, before target acceptance no grant
or proposal authority exists. When the exact capable live target session/incarnation accepts,
one current-epoch grant with E and that scope appears. When that session files a permitted
ownership-transfer relief proposal, one durable row stores proposal id, train, origin owner
epoch, expected train/line generations, proposer principal/cause/correlation, exact proposed
successor, closed scope and offer deadline, reason, idempotency key, state `pending`, and
timestamps; filing changes no owner epoch, offer, or brief fact. Identical replay returns the
same proposal and different bytes with the same key return
`relief_proposal_identity_mismatch`, before or after any terminal proposal state.

When the exact current owner accepts that pending proposal before expiry with matching epoch
and generations, the proposal becomes `accepted` and one owner-authored pending
`owner_transfer` offer bound to those same values appears atomically. The proposed successor
still must win the separate offer-acceptance CAS. A non-owner accept is refused. A competing
pending transfer offer returns `owner_transfer_offer_pending` and leaves the proposal
pending. An unavailable proposed successor returns `offer_target_unavailable` and leaves the
proposal pending. In separate fixtures, owner rejection, exact-proposer withdrawal, deadline expiry,
and owner-epoch close produce `rejected`, `withdrawn`, `expired`, and `superseded`, preserve
occurrence predecessors, and create no transfer offer. Concurrent accept/withdraw has one
state-CAS winner. A crash before or after each proposal write, terminal occurrence, and offer
creation boundary recovers one proposal state and at most one transfer offer.

When the relief session tries commit, acknowledge, decide, freeze, line-integrate, promote,
tag, direct transfer,
ship, or cancel, then each request is refused with zero owner mutation. Given the grant is
revoked, expired, bound to an ended epoch, or names another session, then proposal returns
`relief_not_active` and writes zero proposal rows.

**A-48 — Fact-derived change and action order.** Given one child-assignment reviewed-clean
verdict, when its source transaction commits, then exact ordered direct and effort-parent
evidence fact versions append, their subject heads advance, and a watch selecting that
evidence/trigger opens or coalesces one refresh action whose ordered source range and count
recompute from the fact rows. Progress, completion, surrender, changes-requested, prose, and
delivery events that create no selected gate/risk/evidence fact version do not stale the
brief. Given each of the nine decision-request occurrences, its evidence fact retains the
exact occurrence kind, predecessor, dedupe identity, and direct-before-parent order. Given
`supersede_after_acknowledged`, acknowledgment advances the cursor and the next selected fact
terminates the prior action as superseded and opens one linked successor.

**A-49 — Action coverage and recovery.** Given a pending responsibility offer and a stale brief, when
delivery fails and the gateway restarts, then the offer action still targets the exact
offered session/incarnation, the refresh action still targets the exact owner, and each
retains a pending delivery or retry time. Recovery reuses each action id, one Main fallback notice records failure cause,
and Main gains zero owner authority. Given the action remains open at its computed due time,
then exactly one deadline escalation and high-attention Main marker exist. Acknowledgment
leaves a watched-fact refresh open; a covering owner brief satisfies that watched-fact
action. Repeated delivery failure records
5, 10, 20, 40, and 60-second waits, then 60-second waits until satisfaction or cancellation.

Given each candidate-pointer transition in turn—no candidate to `releasable`, no candidate to
`no_change`, optional-line G1 to G2, null bundle to selected B1, and B1 to selected
replacement B2—the pointer, stale currency, and exactly one open `refresh-readiness` action for
the train/current candidate generation/latest pointer digest, with due time equal to the
pointer occurrence plus the product-authored candidate `refreshWithinMs`, commit atomically. A fault at
each child write leaves all three at their prior values. Replaying identical tuple bytes
creates no action or occurrence; this includes sealing or replaying selected B2. A newer tuple terminates the prior open target as
`superseded`, appends one linked action with ordered pointer history, and leaves exactly one
open action. Delivery acknowledgment does not close it. A brief for an earlier candidate or
bundle returns `candidate_pointer_mismatch`, writes no brief, and does not close it. Only a
new owner brief whose candidate fields and digest equal the exact latest pointer closes it.

**A-50 — Canonical content and decisions.** Given current and historical brief fact versions
and all nine decision-request occurrence histories, when an authorized reader fetches them,
then it receives the complete canonical bytes and deterministically recomputes their order,
stored digest, and member, watch, gate, risk, decision, readiness, go/no-go, and evidence
manifest hashes from exact durable rows. Terminal facts and later brief revisions do not
erase predecessor versions or occurrences. Given missing
content, missing required keys, unknown keys, altered bytes, any collection-hash mismatch,
unresolved evidence, or commit marker mismatch, then the snapshot returns an integrity error
and currency `needs_attention`, not `current`.

**A-51 — Preserved Clawline fixture.** Given immutable fixture `art_ab55409f` at the assumed
digest, when release membership and gates are serialized, then transcript continuity, Gate
D, reopened `wi_9086ebd5-bd62-4c04-9b97-ac83ce34f53e`, and literal decisions round-trip as
product evidence without becoming Tightbeam defaults.

**A-52 — Terminal optional-line protection.** Given a shipped or canceled `release_line`
train, when owner, sponsor, admin, merge principal, or provider event attempts line
integration, direct push, force update, or deletion, then the operation is refused, the
line head remains unchanged, and retained history remains readable.

**A-53 — Rejected provisional digests.** Given the two unpublished provisional SHA-256
values named in the header, when an artifact, review, implementation handoff, or release
operation cites either as revision 4, revision 5, or revision 6 authority, then resolution returns
`unknown_spec_artifact` and selects neither digest.

**A-54 — Repository anchor and protection.** Given main head A with the four required
provider protections, when an authorized principal records an anchor, then one immutable
anchor stores A and the exact ruleset id/digest without changing main. Given any protection
is absent, main readback differs from A, or the ruleset changes before train creation/freeze,
then the operation returns `release_ref_unprotected` and creates no train or generation.

**A-55 — Full brief schema round-trip.** Given one valid item for each member, watch,
gate, risk, decision status, readiness state, go/no-go value, and evidence kind, when the
owner commits and reads the brief, then canonical bytes and normalized rows round-trip every
fact id/version and field exactly, including the row-derived candidate-pointer digest. Given
both watch reissue policies and an active watch's owner offer-or-epoch reference, watch
generation, rebound predecessor, selector, trigger, cursor, due time, and dedupe field,
row-derived order is stable. The candidate's positive `refreshWithinMs` round-trips but is
excluded from the pointer digest. Given a
later superseded or retired watch version, it remains in history and a current brief that
cites it is refused. Given each
invalid enum, missing conditional field, duplicate id/version, unresolved reference, unknown
key, or caller-supplied bytes inconsistent with the rows in turn, commit returns
`invalid_release_brief` with zero partial rows.

## Open Questions

None. The product owner will separately author each train's scope, gates, evidence, risks,
decisions, deadlines, readiness, go/no-go, tag name, and rollback choice. Those values are
runtime product decisions, not holes in this design.
