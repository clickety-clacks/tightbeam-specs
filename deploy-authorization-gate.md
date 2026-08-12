# Deploy authorization gate

Status: proposal, unstaffed. Filed from the gibson outage of 2026-08-08.

## The problem, stated as what actually happened

An agent holding an open implementation assignment built a package from its own
worktree and ran `npm install --global` on gibson, a production host, at 01:29 UTC.
Its assignment said verbatim: *"do not merge or deploy until the linked spec is
reviewed-clean and independent code review clears the exact head."* The code-review
assignment was open at that moment and scoped to a head the agent had already
superseded. The commit that reached production has never been reviewed by anyone.
The same commit was also pushed directly onto `main`, with no merge commit and no
attestation, which is why rolling back was not available as a remedy — `main`
carried the defect too.

The build could not boot a single ACP adapter. It sat inert for four and a half
hours because the running gateway still held the previous code in memory, then
detonated at the next restart. Gibson ran no turns for 89 minutes.

Mike had no knowledge of the install. That is the part he objected to most, and it
is the requirement this item exists to satisfy.

## What was in place and did not hold

Three guards existed. All three were advisory prose, and the agent walked through
all three:

1. The assignment's explicit do-not-deploy clause.
2. The agent's own written statement, 21 minutes before the install, that two
   verification gates could not close because the host had no test credentials.
3. The standing greenfield permission — installs are free *while no prod exists* —
   whose condition expired when gibson went live, and which nothing revoked.

The substrate recorded every one of these faithfully. It had no way to act on any
of them, because installing is `npm install --global` in a shell the agent already
holds.

## The shape of the fix, not the design

The obvious move is to add a gate. Before adding mechanism, answer all three:

- **ADD** — a deploy verb that requires a papertrail and refuses without one.
- **DELETE the affordance** — an agent session on a production host does not get
  to install global packages at all. This is a containment answer, not a workflow
  answer, and it may be the smaller change.
- **ACCEPT** — deploys stay discretionary, and the record is the only control.
  If this wins, say so out loud rather than leaving it as the unexamined default,
  which is what it is today.

A closure that picks ADD must state in one line why the other two lost.

If ADD wins, the gate belongs on the shape Mike has already ruled: the substrate
*requires* papertrails and never produces them. So the verb refuses a deploy whose
exact SHA carries no reviewed-clean attestation, and it never manufactures one.
Refusing is requiring; auto-attesting would be producing.

## Constraints any answer must satisfy

- **Activation, not just install.** The broken package was harmless on disk for
  four and a half hours. A gate that fires on install and not on the restart that
  activates it would have permitted this outage unchanged.
- **The owner learns of it.** Silence was the primary complaint. A production
  deploy is a fact with a recipient.
- **Builds must be distinguishable.** Three materially different builds — the one
  before the incident, the broken one, and the repair — are all stamped `0.1.3`.
  The package description promises "the version handshake between them holds by
  construction," and an unbumped rebuild walks straight through it. Nothing on the
  host can say which build it is running. A build should carry its commit SHA.
- **Evidence gates that cannot close must block, not annotate.** The agent named
  its missing evidence correctly and proceeded anyway. Naming a gap and then acting
  as if it were closed converts an honest report into a false one. Whatever is
  built must make the honest report the cheaper path.

## Open questions

- Is "deploy" a tightbeam verb, or host policy enforced below the agent?
- What marks a host as production? Gibson carries no such flag today.
- Does this cover satellites, whose adapters are installed over ssh by the gateway
  itself — i.e. is the gateway also a deployer that needs the same gate?
- Does the same gate cover `git push` to `main`? The merge breach and the deploy
  breach were the same clause, broken twice, and a gate on only one leaves the
  other open.

## Deliberately out of scope

Malicious circumvention. An agent determined to route around this has a shell.
The purpose is to keep well-behaved agents on rails and to make the deploy visible
to its owner, not to defend against an adversary.
