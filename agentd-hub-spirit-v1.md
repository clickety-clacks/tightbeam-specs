# agentd-hub — spirit charter v1

Ratification pending (PO). Source: Mike's design discussion, 2026-08-30/31,
distilled by his terminal session. Structure ruling at the end is Mike's.

## The product

One truthful, live view of every coding agent across the user's machines,
built only from what each machine's agentd publishes. The hub is the blessed
multi-machine consumer of the agentd contract and the proof that the contract
suffices for outside consumers.

## Invariants

H1. **Observation stays separate from action.** The hub reads. It never
injects input, answers permission prompts, or steers an agent. A future
command layer is a separate per-source adapter beside the stream, each
command explicitly confirmed and audited; it never becomes part of the
observation plane.

H2. **agentd stays off the network.** The hub must never require a listener,
port, or credential in agentd. Transport is the user's existing authorized
ssh running the documented CLI (`agentd watch --json`), one child per source.
If agentd cannot serve a need this way, that is a product question for the
owner, never a reason to open a port.

H3. **Truth over reassurance, one level up.** Every emission is a complete
snapshot; consumers never accumulate. Unknown renders as unknown. A source
that cannot be reached shows "not reached since T" and never silently
vanishes. Claim age is shown; staleness is never converted into a different
state.

H4. **Snapshot-first push.** The first event of a subscription is the
complete current merged state; every later event is also complete state.
No replay, no diffs, no cursors in 0.x. Reconnect means resubscribe.

H5. **Identity is per-machine.** Agents are keyed
(machine, instanceId, pid, startTimeTicks). A pid means nothing across
hosts. Names and locations come from the daemon's identity fields, never
from screens or transcripts.

H6. **Privacy floor inherited and extended.** No prompts, transcripts,
command lines, or environment values, ever. Snapshots carry working
directories and names, so the listener binds localhost; exposure beyond
that is the deployment's explicit choice (for example tailscale serve).
0.x invents no authentication and says so plainly rather than pretending.

H7. **Zero-config by membership, not broadcast.** Discovery is the user's
curated machine set: tailnet peers or a hosts list, probed once over
authorized ssh with the documented CLI. No mDNS, no per-machine discovery
daemons, no port scanning.

H8. **Stateless.** Kill the hub and restart it; it rebuilds everything by
resubscribing. No database, no durable roster.

H9. **MVP discipline.** Ship the smallest thing that shows the pane. One
review round unless a real defect forces another. A spec or process heavier
than the product is itself a defect.

## Non-goals (0.x)

Command injection of any kind; WebSocket; diff protocols; an authentication
system; a macOS agentd backend; replacing PTY-owning hosts (herdr's model);
any change to the agentd wire protocol.

## Structure ruling (Mike, 2026-08-31)

One Agentd Product Owner owns both spirits (agentd and agentd-hub). A
dedicated hub orchestrator, distinct from the agentd delivery orchestrator,
owns the hub's work-item lifetimes. A sibling PO is revisited only if hub
rulings come to conflict with agentd's spirit rather than extend it, most
plausibly when a command layer arrives.
