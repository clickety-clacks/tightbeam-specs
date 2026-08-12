# Tightbeam Containment

How Tightbeam confines code it runs on behalf of an org: rail check scripts
today, adapter processes when adapter containment is turned on. Companion to
`tightbeam.md` (Law) and `tightbeam-decisions.md` (provenance).

## What containment is for

Containment keeps agents **on the rails**. It is not a defence against a malicious
agent, and it is not a security boundary. A circumvention that requires an agent to
be deliberately hostile is explicitly **out of scope**: we do not design for it, and
a finding premised on it is not work.

This is a standing product ruling, not a default to be re-litigated per change.
Weigh a proposed hardening by whether it keeps honest work inside its lines —
**parity, correctness, legibility** — and decline it when the only story that
reaches it is malice. Reviewers do not hold this frame and will raise
security-shaped findings by default; that alone does not make them work. A BLOCKING
finding is a claim to be weighed against this ruling, not an instruction.

It is stated here because this is where the next mechanism gets chosen, and because
it was violated once already: a symlink-swap race was raised as BLOCKING, actioned
without weighing it, and cost a round on a threat we do not defend against. The
same ruling sits in `containment.ex` and `contain.rs`, at the two places the
decisions actually get made.

Everything below — the guarantee, the mechanisms, the proof obligations — is
bounded by this. "A contained process may write only inside its write roots" is a
statement about code doing its job, not about an adversary who has stopped doing it.

## The parity obligation

A containment mechanism is per-OS. That is a property of every OS, not a
discovery about this one. **Any mechanism chosen for one supported platform
carries, at the moment of the choice, an obligation to name the mechanism for
every other supported platform and to prove each one on that platform.** The
obligation is discharged at design time, in this document, not deferred to a
test that someone might write later.

Tightbeam supports macOS and linux gateways. A module whose moduledoc says
"macOS Seatbelt profile rendering" is therefore either incomplete or the spec is
wrong about the supported set; there is no third reading. `Containment` was
macOS-only from its first line while linux was a shipped target, and every rail
check on a linux gateway returned CONTAINED_REFUSED as a result. Statutes and
gates were inert on linux.

This is not a subtle gap and must not be recorded as one. The corollary is a
standing rule: **a suite that passes on macOS and has never been executed on
linux is not a passing suite, it is an untested build.** Both platforms gate.

## The guarantee

One sentence, identical on every platform:

> A contained process may write only inside the write roots it was granted, and
> a containment that cannot be applied refuses instead of degrading.

Everything below serves that sentence. Two consequences are load-bearing:

1. **Never silently unconfined.** If containment cannot be applied on this
   host — mechanism absent, kernel too old, profile unparseable, a rule that
   will not attach — the run is CONTAINED_REFUSED. "Best effort" is forbidden:
   an unconfined run that reports success is strictly worse than the outage
   that preceded this spec.
2. **Never platform-legible.** A rail author reads a verdict, not an OS. The
   argv contract, the exit bands, and the classes the substrate parses are
   identical on both platforms. Where the platforms cannot behave identically,
   the difference resolves toward *more* restriction, never less, and is named
   here.

Reads and network are deliberately unrestricted in v1 (`(allow file-read*)`,
open egress). Containment is a write wall, not a jail.

## The seam

`Tightbeam.RailScript` renders a profile and hands it to the Rust wrapper:

    tightbeam rail-exec --profile <PROFILE> --timeout-ms <N> -- <script-path>

Fixed on both platforms:

| Band | Exit | Meaning |
|---|---|---|
| PASS | 0 | child exited 0; its stdout is forwarded verbatim |
| SCRIPT_ERROR | 10 | child ran and exited non-zero, or its input never landed |
| SCRIPT_TIMEOUT | 20 | the time box elapsed; the process group was killed |
| CONTAINED_REFUSED | 30 | containment was not applied; no verdict exists |

`rail_script.ex` maps these to `returned` / `error:<code>` / `timeout` /
`contained` / `unreported`. The argv shape, the band numbers, and the
`tightbeam rail-exec child exit: <N>` stderr line are platform-invariant.

### Neutral truth, per-OS encoding

The neutral truth is **the set of write roots**. Seatbelt SBPL is macOS's
*encoding* of that set, not the truth itself. Elixir stays the sole authority on
which roots are granted, because that set draws on product knowledge the wrapper
does not have (`Harness.containment_additions/0`). Only the encoding is per-OS.

The renderer therefore dispatches on `:os.type()`. The wrapper dispatches at
**compile time**, on `cfg(target_os)` — deliberately stronger than the runtime
`std::env::consts::OS` match `cli/src/probe.rs` uses for its collectors. probe.rs
is shaping data and must describe any host; containment is issuing syscalls and
must refuse to exist on a platform it cannot confine. So a platform with no named
mechanism **fails to compile** rather than reaching a runtime arm — the hardest
available form of "never silently unconfined", and the reason there is no
catch-all arm to audit.

### The two seams get different grants

`rail_profile/1` and `adapter_profile/1`, named separately, because a rail check
script is not a harness turn.

They were once one function. `Harness.containment_additions/0` — grants that exist
for a harness's *runtime* needs (`/private/tmp` for claude's Terminal workdir,
`/dev` for its PTY allocation) — arrived with the adapter-seam refactor two days
after rails were contained, and was appended to the renderer both seams happened
to share. Nothing made that coupling load-bearing. It was incidental, and its
effect was that **a grant added for a harness silently widened the rail write
wall.**

On linux that grant was `/dev`, and `/dev/shm` is world-writable tmpfs. Measured
on shrdlu against a real rail profile: the script wrote `/dev/shm`, the rail
returned PASS, and the file outlived the scratch `rm_rf`. A durable write channel
outside the scratch root — a platform difference resolving toward *less*
restriction, which is the one direction this spec forbids.

Rails now get their write roots plus exactly one fixed grant: **`/dev/null`**.
That grant is measured, not assumed — `>/dev/null` is in the shipped
`c5_script_guards` rail scripts, so removing all of `/dev` would have broken the
working platform in order to fix the broken one. A discard sink cannot carry
anything out of the scratch root, which is why it does not breach the guarantee
in substance. Everything else under `/dev`, `/dev/shm` above all, is gone. The
result is narrower than before on **both** platforms.

Naming the seams separately is the part that lasts: the widening was possible
because one list served two walls, so a caller now has to say which wall it wants.
Editing harness code can no longer move the rail wall.

- **macOS** → SBPL text, byte-identical to what shipped, passed through to
  `sandbox-exec -p`.
- **linux** → a minimal JSON envelope the wrapper parses:
  `{"tightbeam_containment":1,"write_roots":["/abs/path", ...]}`

Root *validation* (absolute, no quote/backslash/control bytes, no symlink
component, lstat-able ancestors) is platform-neutral truth about the filesystem
and runs unchanged on both. A grant must never silently miss its real path.

A profile the wrapper cannot parse, or whose version it does not know, is
CONTAINED_REFUSED. This is why the invalid-profile test is meaningful on both
platforms rather than accidentally green on one.

## Mechanism: macOS

Seatbelt via `/usr/bin/sandbox-exec -p <SBPL>`, unchanged. `(deny default)`,
`(allow file-read*)`, `(allow file-write* (subpath ...))` per granted root.

**Refusal is decided before the fork, never read off the child.** The wrapper
applies the profile to `/usr/bin/true` as a preflight; if that fails, the run is
CONTAINED_REFUSED and no script ever starts. An SBPL profile's validity does not
depend on the command it wraps, so this tests exactly the thing that can fail, and
it is the same preflight `placement.ex` already runs for adapters.

This replaced a sniff — exit 65 plus a `sandbox-exec:` stderr prefix with empty
stdout — and the sniff was a live defect, not merely inelegant. **Both halves are
child output, so a rail script could forge them:**

    echo "sandbox-exec: authored" >&2 ; exit 65

produced band 30 on macOS and band 10 on linux. That is rail-AUTHORED input
deciding the verdict, and the OS legible from it — the platform-illegibility
clause broken by the very seam meant to uphold it, and the same family as the
fabricated child-exit line (#43): a fact read off a channel the subject of the
judgement controls.

**The invariant now: once a child has run, nothing it writes or exits with can
mean "contained".** There is no post-spawn path to band 30 on either platform; the
function that used to provide one is deleted rather than left returning false.

## Mechanism: linux

**Landlock** (kernel LSM, `landlock_create_ruleset` / `landlock_add_rule` /
`landlock_restrict_self`), applied by the wrapper itself in the forked child
before `exec`, beside the existing `setpgid`.

Chosen over bubblewrap on four counts, in order of weight:

1. **Refusal is a fact we observe directly.** Landlock is applied inside our own
   process, so "containment was not applied" is a syscall return value, not an
   exit code to be inferred. CONTAINED_REFUSED becomes exact on linux — better
   than the macOS exit-65 sniff, and the property the spec cares most about.
2. **No helper binary, no privilege.** Landlock is unprivileged: no setuid, no
   user namespace, no `bwrap` on the host. bubblewrap adds a dependency and
   depends on unprivileged userns, which distributions restrict (Ubuntu's
   `kernel.apparmor_restrict_unprivileged_userns`) — a second, invisible way for
   containment to become unavailable.
3. **It maps onto the existing shape.** The renderer already produces a set of
   path rules. Landlock consumes a set of path rules. bubblewrap consumes a
   filesystem view, which would have to be constructed and reasoned about
   separately from the grant list.
4. **Process-group semantics are untouched.** bubblewrap becomes PID 1 of a new
   PID namespace, which is exactly the layer the timeout and killpg behavior is
   pinned on. Landlock adds no process layer: the wrapper execs the script
   directly, so the child *is* the process-group leader — the same shape macOS
   has, with one less process in it.

bubblewrap remains a legitimate mechanism and is what Codex itself uses; it is
rejected here for this seam, not in general.

### Rights handled

Handle the write-shaped access rights only, and grant them on the write roots.
Read, directory-read, and execute rights are deliberately **not** handled, which
leaves them unrestricted everywhere — the exact linux expression of
`(allow file-read*)` and `(allow process-exec)`. Network access is not handled,
expressing open egress.

Handled: `WRITE_FILE`, `REMOVE_DIR`, `REMOVE_FILE`, `MAKE_CHAR`, `MAKE_DIR`,
`MAKE_REG`, `MAKE_SOCK`, `MAKE_FIFO`, `MAKE_BLOCK`, `MAKE_SYM`, plus `REFER`
(ABI 2) and `TRUNCATE` (ABI 3).

`REFER` is handled and granted so renames and links *within* a granted root
work; unhandled, Landlock denies all cross-directory renames, which would make
scratch unusable in a way macOS is not.

### The ABI floor, and refusing an old kernel

Landlock's ABI level varies by kernel and must be queried
(`landlock_create_ruleset(NULL, 0, LANDLOCK_CREATE_RULESET_VERSION)`).

**The floor is ABI 3 (kernel 6.2).** Below it, `TRUNCATE` is not restrictable,
so a contained process can zero any file it can reach — a write outside its
write roots, which is precisely the guarantee. A host that cannot deliver the
guarantee **refuses**: no Landlock support, `ENOSYS`, or ABI < 3 is
CONTAINED_REFUSED with the reason on stderr. It is not a warning and not a
downgrade.

**The handled set is a constant, and that is the invariant.** Its highest right,
`TRUNCATE`, is exactly the floor, so *every accepted kernel enforces identically*.
There is no "use more when the kernel offers it, mask when it does not": masking a
write-shaped right by ABI would mean two accepted kernels with two different write
walls — the platform-legible difference this spec forbids, one level below the OS.

Adding a handled right **above** the floor is therefore not a local edit. It needs
a decision entry and a named policy for hosts that cannot enforce it — raise the
floor, or surface the gap — because the alternative is a host silently enforcing
less than its peers while reporting the same verdicts.

The refusal below the floor is a **pure function of the reported ABI**, split from
the syscall that reports it, precisely so a test can execute it: nothing in the
fleet is old enough to reach that branch, and a branch asserted by reading the
source is not proof by this spec's own standard.

One masking does exist, and it is a different thing: rights are masked to the set
valid for the grant target's **inode type**. Landlock validates a rule's rights
against the type of the object the rule attaches to and rejects an inapplicable
right with `EINVAL`, so the mask has three buckets:

- **directory** → the full handled set (the `MAKE_*`/`REMOVE_*`/`REFER` family is
  directory-only);
- **regular file** → `WRITE_FILE | TRUNCATE`;
- **anything else** (character/block device, fifo, socket) → `WRITE_FILE` only.

`/dev/null` is a character device and is the sole fixed rail grant, so the third
bucket is the production arm, not a corner. `TRUNCATE` is dropped there because it
is **meaningless** on a device — the VFS never truncates one, so a shell redirect's
`O_TRUNC` fires no truncate hook and the right cannot affect the wall. Narrowest
type-appropriate, not a compatibility workaround.

The set that actually EINVALs on a device is the **directory-only**
`MAKE_*`/`REMOVE_*`/`REFER` family, i.e. the full handled set. `WRITE_FILE |
TRUNCATE` is *accepted* on `/dev/null` by every kernel measured — ABI 4 on the
fleet and ABI 7 on the CI runner alike, which the `contain-probe` trace prints as
`WRITE_FILE|TRUNCATE -> ok`. An earlier reading of this blamed a "strict kernel
rejecting TRUNCATE"; that was false, and the real cause of the outage it was
invented to explain was a stale cached binary sending the full set (#60). Do not
reintroduce `TRUNCATE` for devices looking for a compatibility reason — there
isn't one; the reason is that it is inert there.

This mask keys off the target's type, a property of the path identical on every
accepted kernel — it is not the per-ABI masking forbidden above. **But the *valid
set per type* is itself kernel-dependent**, and that is exactly what three
same-version fleet hosts cannot show: shrdlu and eurisko (both Landlock ABI 4)
accept `WRITE_FILE | TRUNCATE` on `/dev/null`; the CI runner's newer kernel does
not. The all-platforms CI gate caught it; the fleet never could. The narrowest
type-appropriate set (`WRITE_FILE` for a device) is the one that holds across
kernels, and `>/dev/null` was verified still to work under it.

### A device, not a directory: ETXTBSY on exec

A separate hazard the `/dev/null` work surfaced. A rail script is written and then
executed, and `execve` returns `ETXTBSY` while any process holds the script open
for writing. The production wrapper is single-threaded when it forks, so it never
does — but a *multithreaded* parent (cargo's own test harness runs tests across
threads in one process) can have one thread's `fork` transiently inherit the write
fd another thread holds on a just-created script, and the exec then sees it busy.

`ETXTBSY` is always transient: it clears the instant the interfering fd closes or
execs. The contained spawn therefore **retries on `ETXTBSY` only** (bounded), which
is correct hardening for any substrate that writes a script from a threaded process
and not merely a test patch. A permanently-busy file exhausts the budget and still
refuses; no other errno retries.

### Making the kernel visible: `tightbeam contain-probe`

Because the mechanism's behavior is kernel-dependent and the fleet is one version,
guessing the runner's kernel is not good enough. `tightbeam contain-probe` prints
the OS release, the Landlock ABI, and a **right-by-right grant trace** for a
directory and a device node — the exact syscalls the enforcement path makes, so a
runner's `EINVAL` is diagnosed from its own output rather than inferred from a
version string. It is wired into the linux CI job as a diagnostic step and is safe
to run anywhere: it reports, it never enforces.

Probed directly: shrdlu and eurisko, both 6.8.0-134, both with `landlock` in
`/sys/kernel/security/lsm`. gibson is reported as 6.8.0-136 and so is above the
floor, but was not reachable to probe when this was written — confirm it before
the production cutover, since a host below the floor refuses every rail.

No real sub-floor kernel exists in the fleet to execute the refusal on, so the
sub-floor branch is proven the only honest way it can be: `rights_for_abi/1` is a
pure function of the reported ABI, and a test executes it for every ABI below the
floor and asserts it refuses (obligation 5). The unparseable-profile refusal is
executed end to end besides. Both refusal paths are proven.

### A refusal has to be readable afterwards

Failing closed is only half of it. The wrapper names *why* containment could not
be applied — kernel below the floor, no Landlock at all, a profile it cannot
read — on its stderr. That stderr is written **into the scratch directory**, and
the scratch directory is deleted on the way out.

So a host that refuses every rail used to record nothing but the class
`contained`: no kernel version, no ABI, no reason, on any row that survives. That
is the exact shape of the outage this spec exists because of — failing closed,
correctly, with nothing for anyone to read. Fail-closed without a legible cause is
how a total outage passes for normal operation.

**The refusal reason is therefore carried into the durable event-log detail**, on
the rail row, before the scratch directory goes away. The adapter path already did
this (`containment_refused!` logs `DENIED: <reason>`); the rail path now matches
it. A band-30 rail row says what it could not do.

The wrapper writes the invocation JSON to the script's stdin. Handing the child a
live pipe and writing afterwards made delivery race the child's exit, and a
script that never reads — a constant deny, an error-path fixture, four of the
shipped rail scripts — lost that race and was told it judged nothing.

macOS won the race by accident: `sandbox-exec`'s own startup delayed the script
long enough for a small write to land. Landlock removes that helper, so on linux
the script *is* the child and the write loses. Same script, same call, different
verdict per OS.

The pipe is therefore created by the wrapper and filled **before anything is
spawned**. Whatever fits cannot come undone, so a check receives its call whether
or not it ever reads. A payload past the pipe's capacity still has a tail to
write and can still be genuinely undelivered — the case that must stay
observable, and the one `unreported` exists for.

This was a latent macOS race, not a linux defect: it was decided by helper
startup latency and nothing made it hold.

### A grant resolves through the path that was validated

Elixir validates every write root component-by-component and refuses a symlink
anywhere in it. The wrapper then opens that path to attach the rule. Grants resolve
with **`openat2(RESOLVE_NO_SYMLINKS)`**, which refuses the whole resolution
atomically if any component is a symlink, so **the wrapper enforces at use-time
exactly what Elixir asserted at validation-time.** That is the reason it is there:
two halves of one rule that cannot drift apart, not a defence.

The facts, which are worth keeping: `O_NOFOLLOW` would not give that property. It
refuses only a **trailing** symlink, and combined with `O_PATH` it does not even do
that — it returns a descriptor to the symlink itself; intermediate components are
followed regardless. Measured on shrdlu: ordinary resolution follows a swapped
intermediate component, and with `RESOLVE_NO_SYMLINKS` the same root refuses with
`ELOOP` while a symlink-free root grants normally.

**This is not precedent, and the scope ruling is why.** It arrived as a BLOCKING
review finding about a swap race, and reaching that window needs an agent to
deliberately move a path component mid-run — which "What containment is for" puts
out of scope. The finding should have been weighed against the ruling and declined;
it was actioned instead, and cost a round.

The measurement is still worth recording, because it also shows the race was never
an escalation even on its own terms: a rail's write root is
`<base_dir>/rails/scratch/<uuid>`, and swapping a component needs write access to
`<base_dir>/rails` — outside every rail's write root, so no contained rail can
reach it, and the uncontained processes that can already have unrestricted write
access and gain nothing by racing.

So it stays on the in-scope ground only: `openat2` is kernel 5.6, far below the
ABI-3 (6.2) floor this seam already demands, so it needs no fallback and carries no
ongoing cost, and it keeps validation and enforcement in agreement. **A future
hardening whose only story is a hostile agent does not get built.**

### Where the platforms cannot match

Landlock rules attach to an open directory fd, so a write root **must exist**
when the ruleset is built. Seatbelt `subpath` rules are prefix matches and
accept paths that do not exist yet, and `validate_roots!/1` deliberately permits
a missing tail.

Resolution: a granted root that does not exist is **omitted** from the linux
ruleset. Omitting a grant is strictly more restrictive, so the guarantee is
never weakened — only a write that macOS would have allowed may be denied. Rail
scratch roots are created before the profile is rendered, so rails are
unaffected. Any future caller that grants a not-yet-existing root gets the
restrictive reading on linux, by design.

## Proof obligations

Per-OS, and satisfied on a real host of that OS — not inferred from the other.

1. **Enforcement, executed.** A test that applies the platform's real mechanism
   and asserts a write **outside** the write roots is *denied* and the file does
   not exist, while a write **inside** succeeds. Symlink cases included: a link
   inside a root pointing outside is denied; a link inside a root pointing into
   another granted root is allowed. A test that only checks the profile string
   renders is not proof of anything and does not discharge this obligation.
2. **The production grant shape actually applies.** Every kind of target a real
   profile contains, including a non-directory (`/dev/null`), must stage rather
   than refuse. An unapplied wall fails closed and is still a total outage.
3. **Deterministic rendering, per OS and per seam.** The exact bytes
   `rail_profile/1` produces on each platform, asserted on that platform.
4. **No grant belongs to a seam that did not ask for it.** A rail profile carries
   no harness addition and no writable `/dev` tree, asserted in the platform's own
   grant form — `/dev` is a substring of the `/dev/null` grant, so a substring test
   would pass while the wall stood wide open.
5. **Refusal, executed — including branches no host can reach.** An unparseable or
   unknown profile yields CONTAINED_REFUSED on both platforms. The sub-floor kernel
   refusal is a pure function executed by a test for every ABI below the floor,
   because no host in the fleet is old enough to run it and "the code obviously
   does that" is not proof.
6. **A child cannot forge a containment verdict.** A rail script that exits 65
   after writing `sandbox-exec`-shaped bytes to stderr yields the SAME band on both
   platforms, asserted on both. This is a *legibility* obligation, not an
   anti-adversary one: an honest script can emit those bytes by accident, and a
   verdict that changes with the OS is unreadable either way. Band 30 is the
   wrapper's to give, never the script's to take.
7. **Validation and enforcement agree on the path.** What Elixir validated is what
   the wrapper attaches the rule to: a symlink at any component refuses rather than
   resolving, asserted against a real intermediate symlink rather than reasoned
   about. The obligation is that the two halves cannot drift — not that a hostile
   agent is stopped from moving them.
8. **A refusal names its cause on a row that outlives the run.** Asserted, not
   assumed: the reason must survive the scratch teardown.
9. **Bands and wrapper semantics, on both.** The band table, process-group kill,
   escaped descendants, and the armed timer are wrapper concerns, not sandbox
   concerns, and had never once run on linux. They are now asserted there.
10. **Both platforms gate.** CI runs the identical suite on ubuntu and macOS. A
    difference in outcome between the two jobs is a parity defect by definition.

Skipping obligation 1 on a platform is the failure mode this spec exists to
prevent. A skip is permissible only for an *absent mechanism on that OS*, never
for "we run the suite elsewhere".

### Discharged

Proven on real hosts, not inferred from the other platform:

- **shrdlu** (linux, 6.8.0-134, Landlock ABI 4) and **eurisko** (linux,
  6.8.0-134): `cargo test` 81 + 2 green, including all six wrapper tests that
  failed before, the executed enforcement test, and the sub-floor refusal tests.
  Directly: a write inside the granted root lands, a write outside is `Permission
  denied` and the file never appears, and a macOS-dialect profile handed to the
  linux wrapper is band 30. Stress: 30 full-suite runs on a CPU-saturated box, 0
  flakes, after the `ETXTBSY` retry (before it, ~1 in 8).
- **eezo** (macOS): `cargo test` 79 + 2 green.
- **Proven on the runner's kernel.** The CI runner is `6.17.0-1020-azure`,
  Landlock ABI 7 — a newer kernel that rejects `TRUNCATE` on `/dev/null` where the
  ABI-4 fleet accepts it. The device-node masking (a device gets `WRITE_FILE` only)
  holds there: the linux CI job is green at 3dae945 (run 30265191569, three
  attempts), and the `contain-probe` diagnostic step prints that runner's ABI and
  per-right grant trace on every run, so the enforcement path and the kernel are
  shown to agree rather than assumed to.
- Non-vacuity: mutating the linux renderer to grant `/` instead of the real roots
  fails the enforcement test. A green enforcement test is therefore evidence.
- **The `/dev/shm` channel, measured before and after** on shrdlu against a real
  `rail_profile/1`: before, the escape wrote its file, the rail returned PASS, and
  the file outlived the scratch `rm_rf`. After, the write is `Permission denied`,
  the file never exists, and the rail denies (band 10) — while `>/dev/null` and
  writes inside scratch still work, which is what makes the narrowing safe rather
  than merely tighter.
- **Both platforms report the same suite and the same outcome**: 953 tests,
  6 doctests, 0 failures, 11 skipped, on eezo and on shrdlu. That equality is the
  gate; a difference between the jobs is a parity defect by definition.

The linux failure set went 44 → 0, over two lanes that had to be reconciled
before either number meant anything:

- **This seam accounted for 20 of the 44**: 12 `RailScriptTest`, 1
  `RailRemedyTest`, 7 `ConformanceTest` C5/C6/C7 rail-script vectors.
- **Platform test-parity (#56) accounted for the rest**: `ProducersTest` and the
  C4/Cap conformance vectors (`kill(1)` needs `--` before a process-group target
  or linux delivers nothing), and `IdentityTest` (a real `git` merge with no
  committer identity reports a phantom `{:conflict, []}`).
- The two sets overlapped in one direction that neither lane could see alone: a
  producer timeout was masking a `contained` deny underneath in six Cap fixtures.
  Fixing containment alone left them red for the producer reason; fixing the kill
  grammar alone unmasked them as containment failures. Only the merged tree is
  green, which is why reconciliation happens in the branch and not after.

## Scope

**In:** the rail-check seam — `Containment.rail_profile/1`, the `rail-exec`
wrapper, and the test double that stands in for the wrapper. All three carried the
same macOS-only assumption.

The double now models **only the exit bands**, never containment. It cannot
impose Landlock — no shell tool can — so a double that contained on macOS and not
on linux was the mock divergence itself: it would have vouched for a write wall
the real wrapper enforces differently. Containment assertions therefore run
against the real binary, and the double's agreement with it on the bands they
both claim is pinned by "real Rust rail-exec matches BEAM framing for pass, deny,
and escaped timeout". The residual risk is a future fixture-driven test that
assumes the double contains; the double says in its own text that it does not.

**Out, named rather than unmentioned:**

- **Adapter containment** (`placement.ex`: the `sandbox-exec` preflight probe and
  the `["/usr/bin/sandbox-exec", "-p", profile, binary]` adapter cmd). Same
  macOS-only assumption, unreachable today because every adapter key is
  `"shared"` (task #36). It is dead code, not a live defect — but it becomes a
  live one the moment adapter containment is enabled, and whoever enables it
  owns making both sites per-OS under this spec. `adapter_profile/1` being per-OS
  means the profile those sites pass is already correct on linux; the applier is
  not.
- **`containment_additions/0` is macOS-shaped** (`/private/tmp`, `/dev` for the
  claude harness) and now reaches only `adapter_profile/1`. Re-expressing it per-OS
  is adapter-containment work and belongs with #36 — and whoever does it should
  note that `/dev` on linux means `/dev/shm`, so the adapter wall will need the
  same narrowing the rail wall just got. The rail seam no longer depends on any of
  it.
- Read confinement, network confinement, and resource limits remain out of v1's
  posture on both platforms.
