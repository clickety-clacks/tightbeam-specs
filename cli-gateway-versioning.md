# CLI ↔ gateway versioning

**Status:** ruled by Flynn, 2026-07-31.

## The numbering system is semantic versioning

`MAJOR.MINOR.PATCH`. MAJOR is incremented **when and only when a change breaks
compatibility between a CLI and a gateway**. MINOR and PATCH never break it.

This is the industry-standard convention rather than a house rule, which matters because
the number is now load-bearing: the gateway refuses connections on it.

## The compatibility rule

A CLI states its version when it connects. The gateway accepts it **if and only if the
MAJOR components match**. Minor and patch drift freely.

That is what makes a missed satellite harmless instead of an outage: a machine one patch
behind keeps working, a machine across a breaking change is refused loudly with the version
it offered and the version required.

## Keeping the fleet current

**`update-clients` is admin-only (Flynn ruling, 2026-08-01).** It replaces the CLI binary
on every registered machine, and that reach is an operator power, not an agent verb. An
implementation guard to this effect was once added unrequested and removed for lacking
authority; this ruling is that authority, and the guard returns with it.


1. Upgrade the gateway.
2. Run the client-update command. It asks each satellite's CLI what version it is — a direct
   question with a clean answer — and ships a new binary where needed.
3. The connect-time check is the backstop for whatever the sweep missed.

Note the distinction from what was deleted: the gateway does **not** infer a remote CLI's
identity from exit codes and stdout at boot. That inference was unbounded in its failure
modes and produced a new defect every review round. Asking a CLI its version and reading the
answer is a different mechanism with a different epistemic basis.

## Cutting a release REQUIRES a compatibility decision

Every release must answer, explicitly and in the release record: **does this change the
contract between a CLI and a gateway?** If yes, MAJOR increments and every satellite must be
updated. If no, it does not.

This is not a formality. The version is the only thing standing between a stale satellite
and a silent protocol mismatch, and it is only as good as the judgement applied when the
number is chosen.

## Where we are now: pre-1.0, and the check is EXACT MATCH

The CLI is at `0.x`, and semantic versioning treats `0.x` as unstable — anything may break
at any time. That is presently accurate rather than a formality: **right now essentially
every release is a breaking change.** `0.x` is the honest number.

So while pre-1.0 the compatibility check is **exact version match**. A CLI connects only if
its version equals the gateway's. That is the same rule the MAJOR comparison expresses, just
evaluated where every release breaks: gateway and CLI move as one atomic unit, and
`update-clients` exists precisely so that is not painful.

**The MAJOR rule above takes effect at `1.0.0`**, when releases stop breaking the contract
by default. Declaring 1.0.0 is the moment the exactness relaxes — that is what the number
means, and it should be declared when it becomes true, not before.

Practical consequence today: every gateway upgrade requires every satellite to be updated.
That is not a defect of the scheme; it is an accurate reflection of a contract that is still
changing on every release.

## Offline satellites reconcile themselves on first contact

`update-clients` remains the normal admin release sweep. A gateway release may nevertheless
complete while a registered satellite is offline or temporarily unreachable; it must record
that satellite as pending rather than pretend it was updated.

That temporary condition must not orphan the satellite. On the first subsequent contact from
a satellite whose CLI version is incompatible with the gateway, the version-mismatch path is
an update handshake, not a terminal refusal:

1. The gateway identifies the required, target-specific CLI artifact and its integrity data.
2. The satellite obtains and verifies that artifact, replaces its local CLI atomically, and
   restarts the original request through the new CLI.
3. If the update cannot be completed, the satellite records and returns a named, actionable
   upgrade failure. It retries reconciliation on a later contact; it must not silently remain
   stranded on the old version.

The bootstrap handshake must remain compatible with a stale CLI precisely so it can obtain
the current CLI. Ordinary gateway verbs remain unavailable until reconciliation succeeds.

Release success therefore means the fleet was swept and every reachable satellite was
updated; unreachable satellites may remain pending, but are self-healing on their next
contact. A release record must make that pending state visible.
