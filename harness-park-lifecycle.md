# Parking a harness: durable identity and group termination

**Status:** design ruled 2026-07-31.

## The promise

A user who sees "parked" believes that agent is DEAD. Anything it does afterwards — spending
budget, writing files, acting on a session they consider closed — is unexpected work. So
parking always ends in a kill of the whole group, and the record says which path it took.

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

So park asks no questions after killing, and none before. There is no absence probe, no
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

The row carries the LIFECYCLE, not a boolean: launching, running, park_requested,
closed_gracefully, killed, kill_failed, exited. A boolean standing for the terminal outcomes
is wrong several ways, and that is why each previous fix picked a different untruth.

Consequences this buys:
- **The fence survives a restart.** A park in progress is a row, not a map entry. An earlier
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
   release is a dead end. `kill_failed` is retried by the sweep, not parked forever.

## Out of scope

The onboarding ceremony spawns a harness on a different path for interactive login. Do not
conflate the two.
