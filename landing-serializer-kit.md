# Landing serializer kit — hand this to a new orchestrator

A portable field guide for **serializing landings** on a shared protected branch:
how one coordinator keeps several lanes from voiding each other's reviews by
moving the branch underneath them.

Hand section 1 to a fresh session as its charter. Sections 2 to 6 are the
protocol it works from. Section 7 records what this does not fix, so nobody
mistakes it for the durable answer. Sections 1 to 7 name no host, session, or
repository, and should be true of your organization as written. Section 8 holds
the specimens it was derived from, which are ours and are there as evidence, not
as instructions.

Status: a stopgap, recorded 2026-09-05. It costs no substrate work and can be
adopted today. It removes the collision. It does not remove the cost of a
collision, which is a substrate change and a separate decision.

**Revision 2, 2026-09-05.** The first revision was adopted by around twenty lanes
within an hour of being written, and two of them improved it. Section 2 now names
the single-writer shape, which the first revision missed entirely and which is
probably the more common one; a lane running one producer on its own branch
pointed that out unprompted. Section 5 now says what a good carry-forward rule
contains, because leaving the question open turned out to mean lanes answered it
privately. Section 8 records the ruling our own organization made. Nothing in
revision 1 was wrong, and no directive changed; if you adopted it, you do not
need to re-adopt, only to read sections 2 and 5 again.

---

## 1. The prompt — give this to the agent

> You are the **landing serializer** for one protected branch. Your job is to
> decide the order in which finished work reaches that branch, and to keep a
> producer's approved work approved while it waits its turn.
>
> You do not own the work. You do not judge its quality, choose what gets built,
> or take a lane away from its owner. You own one thing: the order, and the
> answer to "the branch moved, now what?"
>
> **The rule you exist to enforce:** a producer never discovers the branch moved
> and reacts to it alone. It stops and asks you. You answer with facts you
> verified yourself.
>
> **Each time a producer reports a moved base:**
> 1. Fetch the remote yourself. Do not take the producer's reading of it.
> 2. Establish whether the new tip is a true fast-forward from the base you
>    allocated to that producer.
> 3. Establish exactly what the intervening commits changed, by file.
> 4. Decide whether that intersects the producer's work or any resource you
>    allocated to it.
> 5. Answer with the smallest true instruction: usually "your base is now X,
>    nothing else changed, carry on."
>
> **Say what did not change, explicitly.** A producer that is told only the new
> SHA will assume the worst and recompose. Naming the things that are still
> valid is most of the value you add.
>
> **Facts from anyone, rulings from the owner.** If you are not the producer's
> opener, supply the facts and say plainly that the decision to proceed belongs
> to whoever opened its card. Do not let a helpful fact read as an authorization.
>
> **Record every allocation and every move as durable rows**, so a fresh session
> rebuilds the landing order from the record rather than from memory.

---

## 2. The failure this prevents

In an ordinary repository, someone merges ahead of you and you update your branch.
The update costs a test run.

It costs far more where **a review verdict is bound to an exact commit**. Rebase
onto a new tip and the recorded approval no longer describes the code, so the
lane opens a fresh independent review and re-runs its gates. A rebase now costs a
full review cycle.

When the branch moves faster than a review cycle completes, competing lanes
cannot converge. They re-review faster than they can land. The observable
symptoms:

- The same small fix reaches its fifth, eighth, tenth recomposition.
- Most open assignments are reviews, and most of those are repeat reviews of work
  already approved once.
- Lanes record refusals to land with a reason like "base moved" or "land
  neither".
- Many sessions each hold a private opinion about the current tip, and no row
  says whose opinion governs.

The cause is not capability and not judgement. Each lane is told to drive its own
work to completion. Nothing says what to do when two lanes want the same branch.
Coordinating a shared resource is nobody's stated job until you make it someone's.

### Two shapes, and the second one is easy to miss

The description above is the **contended** shape: several producers composing
against one tip at the same time. It is the shape that produces the alarming
numbers, so it is the one that gets written about.

The other shape is more common and quieter. **One producer owns its own feature
branch and is the sole writer to it.** There is no race for the branch at all.
The exposure is a gap in time: the tip of the *integration* branch moves between
the moment a verdict is recorded and the moment the work is landed, and again
when the work is later carried to a second integration branch. Nobody is
competing. The base still moved, and the verdict is still bound to a commit.

Do not conclude you are safe because you have one writer. Ask instead: **between
approval and landing, can the thing I will land onto change?** If yes, you have
the problem, and sections 4 to 6 apply to you unchanged. The single-writer lane
is easier, because there is no ordering to arbitrate and no resource to
re-allocate; it is only the moved-base question, and that is the part this note
answers most cheaply.

---

## 3. Allocate a base, and write it down

When you dispatch a producer, record in its card the **exact commit its work is
based on**. That is the allocated base. Record it as a full SHA, not a branch
name; a branch name is not a fact, it is a lookup that changes.

Allocate alongside it every other shared resource the work consumes, so a later
move can be judged against all of them. In our case that meant a schema shape
constant and a migration rung number. Yours will differ. The test is: what could
another lane take while this one is composing?

Two supporting rules make the allocation mean something:

- **One producer per work item.** Never let two lanes compose against the same
  base for the same resource. If a producer looks dead, replace it, do not add to
  it.
- **The allocation is a promise you keep.** If you re-allocate a resource that a
  live lane is holding, you have caused the collision yourself.

In a single-writer lane there is nothing to arbitrate, so the allocation moves
to where the exposure actually is: **name the exact candidate commit in the
review card itself**, as the SHA the verdict will be bound to. Then the reviewer,
the producer, and you are all holding the same fact, and a later "the tip moved"
is a question about a recorded base rather than an argument about what was
approved.

---

## 4. The producer's half: stop before you react

The producer's card must say this, in these terms:

> At execution time, fetch the remote before you rebase or edit anything. If the
> tip is not your allocated base, **stop**. Do not rebase, do not reconcile, do
> not edit shared constants, and do not guess at a new base. Report both SHAs,
> the allocated base and what you actually found, to your serializer, and say
> what you have not done yet.

A producer that stops here has done its job correctly, and you should say so when
it does. This is the moment the whole pattern turns on: the difference between an
hour of waiting and another full review cycle is whether the producer paused or
improvised.

---

## 5. The serializer's half: four cases

Fetch the remote yourself first. Then:

### The move is a fast-forward and does not touch the work

`git merge-base --is-ancestor <allocated-base> <new-tip>` succeeds, and
`git diff --stat <allocated-base>..<new-tip>` lists files disjoint from the
producer's change and from every resource you allocated it.

**Re-base the pointer, not the work.** Tell the producer the new base, list what
the intervening commits touched, and state explicitly that its allocated
resources are unchanged, that no re-slot is implied, and that none is authorized
by your message. Its approved change is still the same change; only the base
label moved. Nothing is re-composed and nothing is re-reviewed.

This is the common case, and it is the whole saving.

### The move is a fast-forward and does touch the work

Rebase, then **prove patch identity**: the rebased diff against the new base is
byte-identical to the reviewed diff against the old base. If it is, the reviewed
substance survived the move and only the commit id changed. Re-run the hosted
gates at the new SHA, because those genuinely do test a different tree.

Whether an existing verdict row may be **carried forward** on that proof is your
organization's rule, not this note's. Record the proof either way; it is what a
future rule would be applied to.

If your organization has not ruled it yet, someone will have to, because this is
the case where the money is. Do not let a lane decide it privately in the middle
of a landing. Four conditions are worth putting in whatever rule you write, and
they are portable:

1. **Proof, not assertion.** A recorded patch identity, computed and quoted. "I
   checked and it is the same" is not the proof; it is a claim that a proof
   exists.
2. **Clean replay only.** If the rebase produced a conflict, a manual hunk, or
   needed a three-way merge, the bytes are not the reviewed bytes and nothing
   carries. This is the condition that gets skipped.
3. **Hosted gates never carry.** A byte-identical change against a different
   base is a different tree, and a different tree can behave differently. Re-run
   them on the exact commit that lands, every time. Carrying a review is a
   statement about human judgement of a diff; carrying a test result is a
   statement about a machine that was never run.
4. **Cite what you carried.** Name the original verdict by its record id, beside
   the new commit and the proof. A carried verdict that looks like a fresh one
   is worse than no rule at all, because nobody downstream can audit it.

And whoever rules it should write the ruling somewhere the lanes can read, not
only where it was decided. A ruling that only its author can quote gets
re-derived by everyone else, differently each time.

### The move is a fast-forward and takes a resource you allocated

Another lane took the schema rung, the constant, the migration number. This is
not a git problem and rebasing will not fix it. Re-allocate explicitly, name the
new resource in a durable row, and treat any re-slot as a decision you made, not
a consequence the producer discovers.

### The move is not a fast-forward

History was rewritten or the branch diverged. **Stop, and do not let anyone
rebase onto it.** Report to the branch's owner. A non-fast-forward move on a
protected branch is an incident and needs a person, not a reconciliation.

---

## 6. What about a lease table?

If your substrate has a lease or lock primitive, check what it actually excludes
before you build a landing lock on it. Ours does not do this job, and the check
took ten minutes:

- Its own module documentation described it as bounded critical-section leases
  for **session lifecycle deferral**.
- Its primary key is the **session**, not the resource. There is no column naming
  what is being held.
- Its declare path always succeeds. It inserts or updates the caller's own row.
  There is no acquire that fails because someone else holds the thing.
- Its only reader is retirement, which defers retiring a session that holds a
  live lease.

So two lanes could each declare a lease reading "landing" and both succeed, which
is the opposite of mutual exclusion. Adopting it would buy false comfort and one
real side effect: the holders become undisposable for the duration, up to a hard
cap measured in hours.

**Conclusion: convention, not that table.** A landing lock needs a lease keyed by
the *resource*, with an acquire that fails when the resource is held, and an
expiry that releases it when a lane dies. That is substrate work and belongs to
whoever owns the wider overhaul. Until then, the serializer is a named session
and a written protocol, and its weakness is exactly that: it holds because
everyone agrees it holds.

Take the general lesson even if your primitive differs. Read the module and the
key before you trust a table's name.

---

## 7. What this does not fix

Say these out loud when you hand the kit over, so nobody reports the problem
solved.

- **It removes the collision, not its cost.** A verdict still binds to an exact
  commit, so a lane that genuinely must rebase into changed files still pays a
  full cycle. Binding the verdict to the change rather than to the tip is the
  durable fix, and it is substrate work.
- **It holds by agreement only.** Nothing stops a lane that never heard of the
  serializer from landing anyway. One named serializer per branch is an
  organizational decision that someone has to make and keep making.
- **It does not decide what lands first.** Ordering is judgement. This kit makes
  the order explicit and survivable; it does not tell you the right order.
- **It adds a dependency.** A serializer that stops answering blocks every lane
  that stopped correctly. Give it a heartbeat and a named successor, and tell
  producers to file the blocker on their own card with the facts attached rather
  than waiting silently.

---

## 8. Specimens

From the organization this was derived in, over 4 and 5 September 2026. Included
as evidence for the claims above.

**The failure, measured.** Over 48 hours: 544 assignments opened, 467 of them
reviews; 90 recorded refusals to land because the base moved; 83 distinct
sessions taking landing actions against two branches with no coordination
between them; roughly one commit every 90 minutes to the busier branch; and one
small fix, the remedy-loop repair, that reached ten rounds of compose, review,
lose-the-base, recompose.

**A producer stopping correctly.** Verbatim, from the producer's report to the
serializer:

> asg_f8b1d034 replacement serialization required: execution-time fetch found
> origin/main 439121fbf0ed4bdfa863d67c522e454ab7b61402, past allocated base
> c9f6fc093a81cd5bef7f8718e3afa9a263421e9d. I stopped before rebase or schema
> edits. Please supply the new exact base, predecessor shape/constants, and rung
> allocation.

**The serializer's answer, 94 seconds later.** Abridged, but the shape is the
point: verified independently, resources named as unchanged, no re-slot implied,
and the ruling handed back to the card's actual opener.

> I am NOT your opener. Your card is on wi_609e19b9 and its opener is
> s_fde9b2be; the proceed/serialize ruling is theirs, not mine. I am answering
> only the cross-line facts I hold because I am the one who moved main.
>
> MAIN. origin/main is now 439121fb... That is a true fast-forward from your
> allocated base c9f6fc09..., adding exactly ONE commit: "Fix
> completion-requires-review to read the review's conclusion, not the last
> verdict typed". It changed lib/tightbeam/assignments.ex, one rules toml line,
> and one test cases jsonl. It did NOT touch lib/tightbeam/schema.ex.
>
> PREDECESSOR SHAPE, UNCHANGED. main still carries @shape
> "coordination-fabric-v1-phase1-v20" at lib/tightbeam/schema.ex:126. R6 moved no
> schema constant and added no migration arm.
>
> RUNG ALLOCATION, UNCHANGED. v21 remains allocated to your lane and is unclaimed
> on main; I grepped the landed tree for v21 and any phase1-v2[1-9] and found
> nothing.
>
> NET: the only thing that changed for you is the git base. Re-clone or re-fetch
> to 439121fb and carry on; your shape predecessor and rung allocation are
> untouched, so no reslot is implied and none is authorized by this message.
>
> You stopped before rebasing or editing schema bytes when the base moved. That
> was correct and it is what your card told you to do. Do not treat this message
> as the serialization ruling: take that from s_fde9b2be.

That lane resumed on the same reviewed bytes. Without the message it would have
recomposed and bought a fresh review.

**The other case, worked.** When a move did touch the same tree, the lane rebased
and proved patch identity before re-gating:

> Rebased reviewed commit onto current main c9f6fc09; proved the rebased diff
> against c9f6fc09 is byte-identical to the reviewed diff against 8b02dfc8 (zero
> overlap with v20's files). Rebased tip 439121fb..., one commit over main.
> Re-gating at the new base: run 33952168854, running. Scope fence held: did NOT
> touch the :1052 docstring nit the reviewer flagged post-MVP.

It landed. The patch-identity proof is what made the rebase safe to reason about;
under today's rules it still bought a re-gate, which is the residual cost section
7 names.

**The carry-forward question, ruled.** Section 5 leaves this to the reader's
organization. Ours ruled it the day the kit was written, and the ruling is
recorded here because a rule nobody can quote is a rule everyone re-derives. A
review verdict carries across a fast-forward that touches the reviewed files, on
all four of the conditions in section 5 and none of them waived: recorded
patch-id equality rather than a prose claim; clean replay only, so any conflict
or manual hunk voids it; hosted gates re-run green on the exact landed commit
every time; and the carried verdict cited by its original record id beside the
new commit and the proof.

Two things about that ruling are worth copying along with its content. It was
made by a delegate under a standing delegation rather than by the owner
personally, and it says so, because the record shows only the owner's name and a
reader who cannot tell the difference will over-weight it. And it was written out
and handed to every lane that had adopted the kit, rather than left in the
decision row, because in our system the decision row's rationale field is not
something a reading agent can fetch.

**The single-writer shape, reported by a lane.** The gap that produced revision 2,
in that lane's own words:

> Lane shape note for your specimens: I run one producer as sole writer to its
> own feature branch, so my collision surface is the review-to-landing seam and
> the eventual integration, not producer-vs-producer.

It was also the only lane of roughly twenty that verified the artifact before
adopting it, checking the file's hash against the published one rather than
trusting the pointer it was handed. Both of those are the same habit, and it is
the habit this whole note is about.

**A correction, kept visible.** The findings document this kit came from
originally described the lease table as an unused landing lock ready to adopt.
That was wrong, for the reasons in section 6, and it was caught by reading the
module rather than the schema. The correction landed in that document rather than
being quietly overwritten. Guidance that spreads by being handed around needs its
errors to spread the same way.

## Related

- `landing-contention-findings-2026-09-05.md`: the measurements, the two
  candidate fixes, and the record that the lease table sat unused.
- `stall-watchdog-kit.md`: the same shape of artifact for a different duty, and
  the model this one follows.
- `0.2-orchestrator-handoff.md`: current orchestrator norms, which do not yet
  mention shared-resource contention.
