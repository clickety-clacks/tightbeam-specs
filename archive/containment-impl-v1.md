# Containment impl v1 — macOS Seatbelt composite (implementation spec, r3)

Status: RULED OUT 2026-07-28 (Flynn). Adapter-level containment — this
spec's whole subject: the Seatbelt wall at adapter spawn plus the
`contain-exec` custody wrapper — is ruled out and its implementation
is being deleted. Containment was only ever considered as a way to
apply rails, and no rail routes through adapter-level containment
(verified by exhaustive trace 2026-07-28: the rails path is
`Containment.rail_profile/1` → `bin/tightbeam rail-exec` →
`cli/src/contain.rs`, deliberately severed from adapter grants at
cef47b7, the /dev/shm escape fix). Kernel-confinement of the agent
process serves a threat model ruled out of scope — rails keep agents
on rails, not attackers out. The planned Linux adapter lane
(cgroups/landlock around adapter launch) will not be built.

What lives on is RAILS containment: every rail check script runs
kernel-contained — Seatbelt (`sandbox-exec`) on macOS, Landlock LSM
(raw syscalls, ABI floor 3) on Linux — via `cli/src/contain.rs`,
using `Containment.rail_profile/1`, `validate_roots!/1`, and both
profile renderers. Citations elsewhere (rails-mechanism-v1.md) to this
spec's profile template and Rust `contain` module refer to that
machinery, which now serves rails only. The rails containment contract
is rails-mechanism-v1.md (§A2–A3); design context: containment-v1.md.

If agent-process confinement is ever needed (e.g. untrusted org
members on a shared prod host), that is a NEW requirement to be
specced fresh on the rails Landlock plumbing — not a revival of this
spec.
