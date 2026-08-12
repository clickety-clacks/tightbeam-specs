# Containment wall v1 — macOS Seatbelt gating (implementation spec, r5)

Status: RULED OUT 2026-07-28 (Flynn). The adapter wall — this spec's
whole subject: seatbelt-wrapping the harness adapter launch, with its
posture schema, adapter write grants (work root / home / auth store),
`adapter_opts` wiring, and the sandbox-disable contract — is ruled out
and its implementation is being deleted. Containment was only ever
considered as a way to apply rails, and no rail routes through
adapter-level containment (verified by exhaustive trace 2026-07-28:
the rails path is `Containment.rail_profile/1` →
`bin/tightbeam rail-exec` → `cli/src/contain.rs`, deliberately severed
from adapter grants at cef47b7, the /dev/shm escape fix).
Kernel-confinement of the agent process serves a threat model ruled
out of scope — rails keep agents on rails, not attackers out. The
planned Linux adapter lane (cgroups/landlock around adapter launch)
will not be built.

What survives from this spec's machinery, serving RAILS containment
only: the rail/adapter profile seam split; `Containment.rail_profile/1`
with its path alphabet and lexical canonicality rules; the effectful
`validate_roots!/1` walk; both profile renderers — Seatbelt
(`sandbox-exec`) on macOS, Landlock LSM (raw syscalls, ABI floor 3) on
Linux; and the profile-rides-argv rule (never written to disk). Every
rail check script runs kernel-contained through that path
(`cli/src/contain.rs`). The rails containment contract is
rails-mechanism-v1.md (§A2–A3); design context: containment-v1.md;
empirical ground truth for harness-under-outer-wall behavior:
containment-spike-report.md (2026-07-19 spike, PASS).

If agent-process confinement is ever needed (e.g. untrusted org
members on a shared prod host), that is a NEW requirement to be
specced fresh on the rails Landlock plumbing — not a revival of this
spec.
