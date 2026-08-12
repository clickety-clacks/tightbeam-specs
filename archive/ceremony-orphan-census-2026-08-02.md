# Ceremony orphan census — does the signal-forwarding registry earn its existence?

Status: **RETRACTED 2026-08-02. THE pty ROW BELOW IS WRONG. NOTHING WAS DELETED.**

Flynn authorised the deletion on this document ("delete it. it goes away in 15 anyway"). The
authorisation was sound reasoning on a false fact that this document supplied, and it has
been withdrawn. **Do not act on the recommendation in this file.**

**What is wrong:** the pty row says a ceremony child self-reaps in ~3ms when the CLI dies. It
does not. `openpty` returns the master WITHOUT `FD_CLOEXEC`, and `pty.rs` neither sets it nor
closes the master in its `pre_exec` (which does `setsid` + `TIOCSCTTY` only). **The child
inherits the pty master across exec, and so does every descendant** — so the master never
fully closes when the CLI dies, no hangup is generated, and the tree survives.

**How the census got it wrong:** the harness is Python, which sets `FD_CLOEXEC` by default
(PEP 446), and it additionally closed the master in the child explicitly. It therefore
measured a child that does NOT hold the master. The real code's child does. This is the
SECOND harness-fidelity error in this one investigation — see the caveat at the bottom, which
was about the same class of mistake and did not prevent this one.

**Caught by:** deleting the registry and running the suite.
`ceremonies::tests::killing_the_ceremony_parent_leaves_no_surviving_child` went red —
"descendant continued running after its ceremony parent died". Independently reproduced. The
existing test knew what the census did not, because it exercises the real code path.

**The corrected picture, which is the opposite of what was reported:** NEITHER leg
self-cleans. The handoff row still stands and still orphans. And the unbounded ceremony —
`claude setup-token`, the one found alive after two days — is the pty leg, so the registry is
load-bearing precisely where this document claimed it was redundant.

**Next step, not yet authorised:** `pty.rs` should set `FD_CLOEXEC` on the master (or close
it in the existing `pre_exec`). That is a one-line fix and is independently correct — leaking
a controlling terminal's MASTER into the child is a capability leak every descendant
inherits. With it in place, the kernel may reap the pty tree as this census predicted. Re-run
the census **against the real binary rather than a model of it**, and only then revisit the
deletion.

## The question

`cli/src/child_process.rs` carries a 64-slot lock-free signal-forwarding registry with an
async-signal-safe handler and a hand-back path — roughly 200 lines. Its purpose is to make
sure that if the operator interrupts the CLI, the harness ceremony child is reaped rather
than orphaned.

Four consecutive review rounds found defects in it, each narrower than the last (round 3: two
findings; round 4: six). The fourth-round reviewer independently concluded the machinery
exists only because the TEST process supervises many ceremonies at once, while production
installs exactly one, and that it is "imposing product-path failure modes for test
convenience."

Nobody had measured whether the registry is needed at all. This is that measurement.

## Method

Three-level harness: a session-leading process standing in for the operator's shell → an
ordinary CLI inside that session → the ceremony child in one of the two real shapes.

The CLI is killed with **SIGKILL**, so no handler runs and the registry contributes nothing.
Census is by pid recorded at spawn, cross-checked against the command line — never by pgrep
pattern.

Two shapes:
- **pty** — child gets its own pty as controlling terminal (`setsid` + `TIOCSCTTY`). This is
  the `claude setup-token` leg.
- **handoff** — child does `setpgid` only and stays in the operator's session; the terminal
  is handed to its group. This is the `codex login --device-auth` leg.

## Result

| shape   | child    | eezo (darwin)        | shrdlu (linux)       |
|---------|----------|----------------------|----------------------|
| pty     | sleeping | died 0.003s          | died 0.017s          |
| pty     | reading  | died 0.002s          | died 0.018s          |
| handoff | sleeping | SURVIVED >8s ORPHANED| SURVIVED >8s ORPHANED|
| handoff | reading  | SURVIVED >8s ORPHANED| SURVIVED >8s ORPHANED|

Both platforms agree exactly. Independently reproduced on eezo by a second operator with the
same harness (0.004s / 0.005s / orphaned / orphaned).

## What it means

The asymmetry runs **backwards from the machinery**:

- The **pty leg does not need the registry.** Closing the master hangs up the child's session
  and the kernel reaps it in single-digit milliseconds, whether or not the child ever touches
  the terminal. Ctrl-C *does* reach the parent on this leg (measured separately), so the
  do-nothing behaviour is: parent takes the default action and dies, master closes, child
  dies.
- The **handoff leg orphans, and the registry cannot help with the case that matters.** After
  the terminal handoff the child's group is foreground, so Ctrl-C is delivered there and the
  parent's handler never runs (measured separately). What the registry buys on this leg is
  exactly one case: a catchable signal sent *directly* to the CLI process (`kill <pid>`),
  never Ctrl-C.

And the leg that orphans is the one that **self-limits**: `codex login --device-auth` expires
its own device code in 15 minutes and says so on screen. The leg with no bound at all is
`claude setup-token` — an abandoned one was found alive after two days, which is part of why
this branch exists — and that is the leg the kernel already handles for free.

So the registry's entire remaining job is to reap, on `kill`-to-the-CLI only, a ceremony that
would expire itself within 15 minutes.

## Recommendation (not a decision)

Delete the forwarding registry. Keep `terminate_process_group` and the lease/deadline
watchdog — a different mechanism, no signal handler, and the thing that actually bounds a
runaway ceremony. Expect the signal-firing tests to go with it.

Deleting is a smaller change than any of the four rounds spent hardening it.

If the `kill`-during-codex-login case is judged worth covering, cover it with something the
size of the problem.

## CAVEAT FOR ANYONE RE-RUNNING THIS — the two-level harness inverts half the answer

The first harness had only two levels and made the CLI its own **session leader**. Every
child died, handoff included, because killing a session leader hangs up its terminal. That
result was clean, unanimous, and wrong — and "clean" is what makes it dangerous, because a
tidy answer ends an investigation instead of provoking a second look. It was caught only
because it contradicted a Ctrl-C measurement already in hand.

**Three levels, or the answer inverts.** A convenience in a harness can silently answer a
different question than the one asked.

## Provenance

Harness: `orphan_census.py`, arguments *marker / shape (pty|handoff) / behaviour
(sleeping|reading) / linger seconds*. Written to a session scratchpad under `/private/tmp`,
which is ephemeral — reconstruct from the method above rather than expecting the file to
survive.

Branch state at time of measurement: `pty-onboarding` @ `ad25198`, gated green on both
platforms (eezo cargo 220+1+1+2, shrdlu cargo 221+1+1+2, mix 1202 tests + 6 doctests, zero
failures). Round-4 findings 1, 2, 4 and 5 deliberately left unaddressed pending this
decision; findings 3 and 6 (SA_SIGINFO, errno) were taken because they are correct under
every possible outcome.
