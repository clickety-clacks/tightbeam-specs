# Containment v1 — OS-level session containment (design spec)

Status: RULED OUT 2026-07-28 (Flynn) — adapter-level containment. The
ruled design this doc carried (kernel-sandboxing the harness adapter
process: a Seatbelt profile wrapping adapter launch on macOS, and a
planned Linux cgroup (v2) + landlock wrap around adapter launch) is
dead and its implementation is being deleted; the Linux adapter lane
will not be built. Containment was only ever considered as a way to
apply rails, and no rail routes through adapter-level containment
(verified by exhaustive trace 2026-07-28: the rails path is
`Containment.rail_profile/1` → `bin/tightbeam rail-exec` →
`cli/src/contain.rs`, deliberately severed from adapter grants at
cef47b7, the /dev/shm escape fix). Kernel-confinement of the agent
process serves a threat model that is out of scope — rails keep agents
on rails, not attackers out.

Containment in tightbeam is a RAILS mechanism: every rail check script
runs kernel-contained — Seatbelt (`sandbox-exec`) on macOS, Landlock
LSM (raw syscalls, ABI floor 3) on Linux — via `cli/src/contain.rs`,
with the rail/adapter profile seam split, `Containment.rail_profile/1`,
`validate_roots!/1`, and both profile renderers live. The rails
containment contract is rails-mechanism-v1.md (§A2–A3).

If agent-process confinement is ever needed (e.g. untrusted org
members on a shared prod host), that is a NEW requirement to be
specced fresh on the rails Landlock plumbing — not a revival of this
design.

Spike history: containment-spike-report.md (2026-07-19 spike, PASS)
remains recorded ground truth for harness-under-outer-wall behavior.
Origin conversation: "what if we encapsulate sessions in a light
container that can contain and detect subprocess states, and even
gate/facade CLI calls" (Flynn), plus the macOS containerization
research (see tightbeam-decisions.md 2026-07-20 entries).

## What Seatbelt is (recorded so nobody re-asks)

macOS's built-in kernel sandbox (the substrate under App Sandbox,
Chrome, and both AI harnesses' own tool sandboxing). A profile is a
Scheme-LOOKING text (SBPL) but it compiles ONCE at spawn into a static
kernel rule table — pure match/no-match at operation time; no callbacks,
no logic runs per operation. Deprecated-in-manpage since ~10.11 yet
fully functional on macOS 15/26 and load-bearing across the industry;
no published replacement (apple/containerization#737 asks; unanswered).

Enforcement-layer rule that follows: decidable-at-spawn → kernel wall
(static); needs-a-live-look-at-the-action → harness hook (claude, and
codex's newly-confirmed hook surface) or the gateway chokepoint
(law-as-data over ledger facts). The constitution/statute split, one
layer down.

## Apple's new containerization: rejected for containment, useful as a HOST FACTORY

Apple `container` / Containerization.framework (macOS 26, Apple
Silicon) runs LINUX containers in per-container lightweight VMs (OCI
images, sub-second boot, kernel-per-container). It categorically cannot
contain native macOS processes — so it is NOT our containment layer.
Its legitimate role: minting Linux HOSTS on Mac hardware. A Linux VM
with sshd, assimilated like any machine, is just another host — full
Linux containment story, existing placement machinery, zero new
concepts. Optional; for Macs used as spare compute where mac-ness is
irrelevant.

## Rejected: shim/facade tunneling (the "driving off the farm" ruling)

Running workers in Linux containers on Macs while shimming mac-only
tools (xcodebuild, simctl, signing) back to the host was considered and
rejected: for iOS-heavy workloads the shimmed hole becomes the whole
(builds, simulators, UI automation, DerivedData, keychain all cross the
boundary; file topology is the hard part, not exec). The mechanism the
shim reinvents already exists as PLACEMENT: portable work → Linux
hosts (`where = ["shrdlu", ...]`); mac-native work → Mac hosts. The
workload chooses its farm as one word of manifest data. Facade CLIs
remain the right pattern ONLY for crown-jewel single operations
(signing, store upload, prod deploy) as future capability chokepoints —
never as a general platform proxy.

## Related cheap win (container-independent): per-session CLI tokens

Today every session shares the org-wide cliToken — CLI calls attribute
to "someone in the org." Mint per-session tokens at spawn (revoked at
retire): every /agent/dispatch call self-attributes deterministically;
statutes can gate per-caller; Zone-2 keys move behind the chokepoint
with no container involved. Small lane; specced in session-tokens-v1.md.
