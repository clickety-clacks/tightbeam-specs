# Harness kill and park: distinct durable outcomes

**Status:** kill design ruled 2026-07-31. On Mike's 2026-09-01 ruling, this
contract defines two distinct operations: kill and park. See Naming below.

## Naming

This operation is a KILL and is named one. It was previously called "park", which
collided with two unrelated meanings and stalled the work that depends on it.

Three distinct things had claimed the word:

1. **Park (shipped, keeps the name).** A session parks itself on an open decision
   request and resumes when that request is ruled. `decision_requests.parkWakeId`
   is live in the substrate. Nothing here changes it.
2. **Kill (this contract).** End a running harness process group. Formerly called
   park; that was a misnomer.
3. **Park a session (this contract).** Set a session aside, preserved, so it can be
   relaunched later. A park request produces one durable success-or-failure outcome.

Mike's ruling, 2026-09-01: park does not mean kill in any ordinary sense of the
word, and a person reading "parked" will not expect the thing to be destroyed. The
destructive operation is called kill. Park keeps its plain meaning of setting
something aside to come back to.

The shipped request park and session park both mean "set aside and resume", at
different scopes. This contract does not choose their wire vocabulary. A public
operation must name its target scope so it cannot apply a request park to a session or
a session park to a decision request.

**Code reconciliation still owed.** Shipped internals under `harness_process.ex`
carry park-named identifiers predating this ruling. The process lifecycle state named
below is `kill_requested`. Reconciling existing code identifiers to the ruled names is
work item `wi_6937890c`'s to schedule; this document states the intended vocabulary,
not the current code.

## The promise

A user who sees "killed" believes that agent is DEAD. Anything it does afterwards, spending
budget, writing files, acting on a session they consider closed, is unexpected work. So a kill
always ends in the termination of the whole group, and the record says which path it took.

**The promise is best effort, ruled 2026-07-31.** It is absolute for every member we have
permission to signal, which is the entire tree in ordinary operation. It is not absolute
against the two accepted residues below, and we do not chase them. Do not restate this as a
guarantee anywhere in the code, the record, or the user-facing text; a survivor is a known
outcome, not a broken invariant.

Sequence: ask it to close, wait a 10 second grace, then kill the group. The grace BOUNDS
WAITING; a graceful close is decided by the exit we observe, never by the timer.

## A kill does not need confirming

"Kill" means SIGKILL, to the group. SIGKILL cannot be caught, blocked, or ignored. If the
call succeeds, every member of that group is dead.

So a kill asks no questions after killing, and none before. There is no absence probe, no
post-kill re-check, and no state meaning "killed but unproven." Code that asks whether the
target is gone can only ever return one answer, and every defect that lived in such code was
a defect in machinery that had nothing to decide.

Do not reintroduce verification under another name. The correct response to "how do we know
it died" is that the kernel guarantees it.

**This does not license killing without knowing what you are killing.** Two questions look
alike and are not:

- *Is the target dead after I signalled it?* Guaranteed. Never check.
- *Am I about to signal the RIGHT group?* Not guaranteed, and it must be checked before
  every signal.

Group ids recur after exit and across reboot, and gateway restarts are routine, so a stored
number alone can address a stranger's process. Authorize the target against the identity
recorded at launch — including a boot identity, so a reused id after a reboot fails the
check — and REFUSE to signal when it does not match. That authorization answers "is this
mine"; it must never grow into "is it alive."

**This reasoning is specific to SIGKILL.** The polite signal CAN be caught and ignored, and a
process sent SIGTERM may still be running afterwards — the sandbox work has a live case of a
shell spin loop surviving one. Never carry the confirmation rule from that signal to this one;
generalizing across the two is what produced the machinery this design removed.

## Delivery is a real question; compliance is not

Harnesses can run on another machine over ssh. The kill command may therefore fail to execute
at all — a dropped connection, an unreachable host. That is a question about whether we
succeeded in ASKING, and it is answerable from the command's exit status alone.

`kill_failed` records it, and the reconcile sweep retries. This is the only failure state, and
it never means "we do not know whether it died."

## Kill acceptance

1. Given an authorized request has a process-group record whose boot and launch identity
   match the live target, when group `SIGKILL` returns success, then the lifecycle records
   `killed` without issuing a post-signal process probe, readback, or verification command.
2. Given the recorded identity does not match the target group, when a kill request
   reaches authorization, then it refuses before any signal is sent and preserves the
   existing retry and custody boundaries.

## A park needs an outcome, not an inference

Park preserves a session for later relaunch. Unlike SIGKILL delivery, that result is
not self-proving: the operation can cross a durable fence and then fail to settle the
runtime, its custody, or the park state. The primitive therefore writes exactly one
durable **park outcome** for each accepted park request. The outcome is primitive
output, not a callback, an event-stream hint, or a later reconciliation enhancement.

The only closed outcome values are `parked` and `park_failed`:

- `parked` records that the session reached its durable parked state and is preserved
  for relaunch.
- `park_failed` records that this request did not establish that result. It names the
  durable recovery state and does not authorize relaunch from that failed request.

The completion-escalation rail may acknowledge a `park` disposition only after it
reads the committed `parked` outcome for its request. A `park_failed` outcome leaves
the completion disposition `open`. It changes neither the closed-wake cancellation
classification (`completion_transition`) nor the rail's shape stamp or closed
vocabulary. `completion-escalation-rail-v2.md` remains unchanged while its exact-SHA
review is open.

### Park request and outcome identity

A park request has a generated `requestId` and an idempotency key. The primitive
atomically records the accepted request and its one `park_outcomes` row before it
changes session runtime, worktree, wake, assignment, or completion state. The row
starts `open` and closes exactly once as `parked` or `park_failed`. The idempotency key
is unique for the requesting principal and operation target. Replaying that key
returns the same request and outcome; it does not start another park or write another
outcome. A retry after a `park_failed` result requires a new request id and idempotency
key, with the failed request recorded as its cause.

`park_outcomes.requestId` is both the primary key and a foreign key to the accepted
request. Its `status` values are `open`, `parked`, and `park_failed`; only the latter
two are closed. `closedAt`, `resultingLifecycleState`, failure code, recovery state,
and remedy are null while open and are written atomically when it closes. Each outcome
stores:

- `requestId`, target `sessionKey`, and the session lifecycle generation captured at
  acceptance;
- requesting typed principal, authority basis, cause kind and cause id;
- closed `status` (`parked` or `park_failed`) and `closedAt`;
- the resulting session lifecycle state and the exact recovery state when failed;
- the relaunch-continuity snapshot: session identity, owner and role binding,
  assignment/work-item links, workspace path, custody owner, and worktree preservation
  result; and
- an exact failure code and bounded remedy when `result='park_failed'`, otherwise
  null failure fields.

The row is immutable after close. Read and audit surfaces expose the request, its
outcome, all fields above, and the causal relationship to a later retry. They must not
derive a result from process absence, a timeout, a missing callback, or a later
session-row read.

### Park authority, transition, and custody

The primitive records the authenticated typed principal and authority basis before the
lifecycle transition. A caller without an admission below receives a durable refusal
and creates no accepted park request or park outcome. The primitive does not infer
authority from role names, ancestry, a report-to recipient, or the presentation origin.

- An active session principal may request its own graceful park.
- The authorized owner user may request graceful park or relaunch for the target
  session. A relaunch caller must be outside the parked runtime; no self-wake or timer
  inside that runtime may relaunch it.
- A completion disposition may invoke park only after the completion rail admits its
  session or user principal under R11. That admission is the request's authority basis;
  report-to delivery does not confer it.
- The typed process principal `tightbeam:harness-health` may request only the exact
  session park named by a durable recovery decision. That decision must bind the target
  session, runtime generation, action, mode, policy basis, and health evidence. It may
  not select a target, mode, or action from free text.
- Immediate park and any mode not explicitly bound by the preceding recovery decision
  require operator or admin authority. Omitted mode is graceful.

An accepted request owns one session lifecycle transition. It first closes session
intake and captures the session identity, worktree path and custody, attached runtime
identity, queued work, and pending wakes. A contending operation that loses before a
park request is accepted receives one named refusal and creates no park outcome. Once a
park request is accepted, a concurrent relaunch, recycle, or retire resolves through
the same lifecycle compare-and-set. A terminal retire that wins over the accepted park
closes that request's existing outcome `park_failed` with recovery state `retired`; it
never silently succeeds or recreates the session.

The primitive writes `parked` only after the session row reaches the durable parked
state with intake closed and the preserved continuity snapshot. It preserves the same
session key, owner, role binding, assignment holder, work-item links, transcript,
workspace path, worktree custody, queued turns, and pending wakes. Parked sessions do
not claim queued turns or receive pending wakes. A dirty worktree remains at its
captured path. Park neither deletes, resets, archives, transfers, nor recreates a
worktree. Relaunch consumes that recorded continuity snapshot and may start a successor
runtime, but it never creates a successor Tightbeam session.

If a step after acceptance fails, recovery either restores a safe active state or
retains a named fenced state. Before either result becomes externally final, the
primitive writes the single `park_failed` outcome with the exact recovery state and
remedy. A fenced or unknown-liveness failure keeps intake closed and forbids relaunch.
Recovery after a gateway restart finds the durable request and either resumes the same
transition or writes its one `park_failed` outcome; it never assumes success from a
missing process, an expired wait, or an absent in-memory operation.

## Park acceptance

1. Given authorized principal `P` accepts park request `Q` for active session `S`, when
   the session reaches its durable parked state, then exactly one immutable
   `park_outcomes` row for `Q` has `status='parked'`, identifies `S` and `P`, carries
   the required continuity snapshot, and enables a later same-session relaunch.
2. Given park request `Q` closes intake and then the runtime settlement fails, when the
   primitive closes `Q`, then exactly one immutable outcome has
   `status='park_failed'`, the exact recovery state and remedy, and no relaunch occurs
   from `Q`; a completion disposition that invoked `Q` remains `open`.
3. Given the completion rail receives an authorized park disposition for request `Q`,
   when `Q` has no committed `parked` outcome, then the rail records no acknowledgment
   or completion-transition wake cancellation. When it reads Q's committed `parked`
   outcome, then it may acknowledge that disposition through its existing R12 seam.
4. Given `P` replays park with `Q`'s idempotency key after either result closes, when the
   primitive receives the replay, then it returns Q's original request and outcome and
   writes no second lifecycle transition or outcome. Given a retry cites a failed `Q`,
   when it uses a new request id and idempotency key, then its own result is recorded in
   one distinct outcome row whose cause names `Q`.
5. Given a restart occurs after park request `Q` commits and before it closes, when
   recovery replays Q, then it resumes or terminally records `park_failed`; it does not
   create a second request, outcome, session key, or worktree custody record.
6. Given park and retire contend for `S`, when the lifecycle compare-and-set selects one
   operation, then a rejected park command records its named refusal, while an already
   accepted park request closes `park_failed/retired` if retire wins; no competing park
   reports `parked` from that race.
7. Given an owner or authorized auditor reads a closed park request, when the read
   returns, then it exposes the request identity, typed principal, authority basis,
   cause, result, timestamps, recovery state, custody snapshot, and any later retry;
   it never calls a process probe to supply missing outcome data.

## Dead means the tree, not the process

A harness spawns tool subprocesses. Killing only the recorded process orphans them — they
keep writing files and consuming budget after the row says "killed" and the user has been
told it is finished. That violates the promise.

**Launch the harness in its own session (`setsid`).** Everything it spawns is born into that
group by inheritance; nothing has to be tracked or enumerated. Terminate by GROUP, and the
whole tree dies in one operation that cannot miss a process spawned a moment ago.

This is not a macOS concern. `setsid` and group termination are POSIX and behave identically
on both platforms, and the defect is identical on both. Implementing it on one platform only
would CREATE a divergence — which this repository already treats as a violation: a rail
author must not be able to tell which OS ran their check.

Precedent for the choice of mechanism: the sandbox pid fix deliberately chose a POSIX
primitive over a Linux-only one to avoid two implementations. Linux has stronger tools
(cgroups, PDEATHSIG, pidfd); reaching for them means a platform split, and that trade should
only be made against evidence that groups are insufficient.

### Known residue, accepted

Two descendants can outlive a group kill. Both are documented and neither is engineered
around; do not build detection for either.

1. **A descendant that deliberately calls `setsid`** leaves the group and survives. Rare,
   deliberate, already documented in the containment wrapper.

2. **A descendant running under different credentials.** Linux `killpg` returns success if
   AT LEAST ONE member was signalled — `EPERM` is returned only when none could be
   ([kill(2)](https://man7.org/linux/man-pages/man2/kill.2.html)). So a child that changed
   its UIDs while keeping the inherited group — in practice, a harness invoking `sudo` —
   cannot be signalled by a non-root gateway, survives, and the call still reports success.

This is the one real exception to "a successful kill means the tree is dead," and it is the
reason that sentence is scoped to members we have permission to signal. It does not
resurrect post-kill confirmation: a probe would find the survivor and then be equally unable
to do anything about it.

## Identity must not recur

A pid recurs. A command line recurs. **`ps -o lstart` has one-second granularity, so pid +
start time recurs too** — a recycled pid within the same second matches, and reconciliation
would then kill an unrelated process.

The process group we mint at launch is a better handle than any number the kernel recycles,
though group ids do recur after exit and across reboot. Record the group, and where a finer
identity is needed, state honestly what its granularity is.

## What is durable

A launch is an event with a durable consequence — a running OS process — and it must be
written down at launch, not reconstructed when needed.

The row carries the LIFECYCLE, not a boolean: launching, running, kill_requested,
closed_gracefully, killed, kill_failed, exited. A boolean standing for the terminal outcomes
is wrong several ways, and that is why each previous fix picked a different untruth.

Consequences this buys:
- **The fence survives a restart.** A kill in progress is a row, not a map entry. An earlier
  design lost it when Credentials crashed and took the coordinator down with it under
  `:rest_for_one`, letting a successor start while a harness was still running.
- **Boot reconciliation.** Without rows, a gateway restart orphans every running harness —
  nobody knows they exist. Rows make them findable.
- **Killing without having watched.** Read the row, terminate the group, record. No live
  monitor held across the lifecycle.

## Rules that still bind

1. **Every external command must be bounded.** Unbounded `System.cmd` for a remote kill can
   hang the coordinator and prevent it finishing boot. SSH `ConnectTimeout` bounds connection
   establishment only, never an accepted remote command.
2. **Every return must be handled by its caller.** Two earlier attempts returned a new error
   into a caller that hard-matched success — once crashing Credentials and wiping the fence it
   protected, once raising in turn checkout. A new failure mode is not done until its callers
   handle it.
3. **A held fence must be clearable.** A key stranded with no operator path to retry or
   release is a dead end. `kill_failed` is retried by the sweep, not stranded forever.

## Out of scope

The onboarding ceremony spawns a harness on a different path for interactive login. Do not
conflate the two.
