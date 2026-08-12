# Service-mode installation — spec v1

Status: DRAFT, not yet reviewed. Blocks the Gibson production install.

## Why this exists

Tight Beam's documented customer installation ends at `mix run --no-halt` — a
foreground process bound to a terminal. It dies on logout and does not exist after
reboot. Every "successful" install to date has been a foreground process, which is
not how any customer will run this.

Ruling (Flynn, 2026-07-27): **Tight Beam must install as an independent persistent
system service on every supported host OS.** The account that runs the installer is
the *customer invoking the installer*; it is not where the service lives. A service
that dies when the installing account logs out has not been installed.

## The four phases, which the README and the test runbook must name separately

Conflating these is what produced a "successful" install that was a foreground
process. They have different actors, different privileges, and different proofs.

1. **Install** — places the service, its identity, and its durable state.
2. **Verification** — proves the service survives the events that define it.
3. **Functional testing** — the complete system sequence, run against the retained
   installation. This is what the install exists for; it is not a phase that
   follows teardown, because there is no teardown.
4. **Uninstall** — an operator action, available and documented, deliberately NOT a
   phase of the smoke and not an acceptance criterion (see below). Test hosts keep
   their installation; the smoke runs as the account that will really run the
   service (see `TEST-HOSTS.md`), because that account's permissions, paths and
   credential visibility are part of the artifact under test, and it never removes
   that account.

## Service identity and locations

The service runs as **the account that installed it** — no dedicated service
account is created. openclaw runs the same way (LaunchAgents under `mike`, no
LaunchDaemon, no service account), and inventing one here would test a configuration
nobody ships.

- **Run-as account**: set explicitly (`User=` / `UserName=`) so the init system does
  not default to root. It is a real operator account, not a synthetic identity.
- **`base_dir`**: selected by **`TIGHTBEAM_BASE_DIR`** — this is the one the gateway
  actually reads at boot (`config/runtime.exs`), falling back to
  `<user home>/.tightbeam`. `TIGHTBEAM_HOME` is honoured only by the mix tasks and is
  what the gateway EXPORTS to subprocesses, so a unit setting `TIGHTBEAM_HOME` alone
  leaves `mix tightbeam.init` and the service pointing at different orgs — a silently
  divergent install. An earlier draft of this spec made exactly that error, inherited
  from the README's prose rather than read from the code.
- **Credentials**: already independent of any human home — `credentials.ex:92`
  stores at `<base_dir>/auth/<harness>/oauth-token`, and `homes.ex:224` projects
  harness homes under `<base_dir>/homes/<machine>/<harness>`. This is the property
  that makes a system service viable at all: the harness CLIs read the projected
  home, not the installer's `~/.claude` or `~/.codex`.
- **Onboarding** targets the service's `base_dir`, so the service owns its own
  harness credentials. The installing account never holds them.

**Non-goal:** a system service reaching into a human's keychain or `~/.claude`.
That was the earlier user-scope design's premise and it is what made the service
die with its account. It is explicitly abandoned.

## Linux — systemd system unit

The supported mechanism. A **system** unit (`/etc/systemd/system/tightbeam.service`),
not a user unit, because a user unit requires lingering and dies with the account.

- `User=` / `Group=` set to the operator account (required — systemd defaults to root)
- `Environment=TIGHTBEAM_BASE_DIR=<base_dir>` — the variable the gateway reads at boot
- `Environment=PATH=...` spelled out: a system unit inherits almost no login
  environment, and `mix`, `node` and the harness CLIs must all resolve
- `%h` must NOT be used: in a system unit it expands to `/root`, not the operator's home
- `Restart=on-failure`, `RestartSec=5s`, `After=network-online.target`
- `systemctl enable --now tightbeam` — starts now AND at boot, no login required

## macOS — LaunchDaemon, and the open question

A **LaunchDaemon** (`/Library/LaunchDaemons/`), not a LaunchAgent. A LaunchAgent is
per-user and starts at login, which fails the survives-logout requirement.

**UNPROVEN and blocking macOS support:** whether the harness CLIs function under a
LaunchDaemon. The prior user-scope guidance asserted a root daemon cannot see harness
credentials. That premise is now believed wrong *for tightbeam specifically*, because
tightbeam projects harness homes into `base_dir` rather than using the human's home —
but it has not been tested. macOS service mode is not documented as supported until a
LaunchDaemon is proven to run a real turn.

## Uninstall — an operator action, NOT a gate

Uninstall is an ordinary thing an operator may want to do, documented for the
customer who wants it. **It is not a product proof and is not an acceptance
criterion.** Whether a service can be removed says nothing about whether it was
installed correctly, and making removal a required step of the install smoke costs
the run the very installation the rest of its testing has to be performed on.

The shape, for the operator who runs it:

- stop and disable the service
- remove the unit/plist
- if you want to confirm it: no unit, no plist, no process, no listener
- idempotent and legible when partially installed
- **preserve `base_dir`.** It holds the identity repo, sessions, work items and
  credentials; removing a service must not destroy the org. Destroying that state
  requires an explicit flag.

Test hosts do not uninstall at end of run — the installation is retained and the
functional sequence runs against it (`TEST-HOSTS.md` §5). Returning a host to a
Tight-Beam-free state is a separately authorized action, not a phase of the smoke.

## Acceptance criteria — a service is not installed until all pass

1. **Starts with no interactive login.** Enabled and running with no human session.
2. **Survives logout** of the installing account.
3. **Survives reboot**, coming back without intervention.
4. **Registered in the SYSTEM domain** — `/etc/systemd/system` or
   `/Library/LaunchDaemons`, not any user or gui domain. Criteria 1-3 can all be
   satisfied by a lingering user unit, which is not a system service; this is the
   criterion that distinguishes them.
5. **Runs a real turn** after onboarding against the service's own credentials.

Proof is observed state on a real host — a running foreground process is not
evidence for any of these, and a green unit file is not evidence for 2, 3, or 5.

## Open questions for Flynn

1. **Service-mode onboarding delivery** — both implemented flows are interactive
   (browser OAuth, device code) and run in the gateway's environment. Under a
   headless system unit there is no TTY and no browser. The staged
   `begin_onboard`/`finish_onboard` path is the obvious carrier; nothing specifies
   who runs it, as what account, or how the human step is reached.
2. **macOS LaunchDaemon viability** — the credential half is settled in code, but
   whether the harness CLIs run a real turn under a LaunchDaemon is unproven, and
   macOS is required for v1.

RESOLVED since the first draft: no dedicated service account (runs as the installing
account, matching openclaw); macOS AND Linux both required for v1; uninstall
preserves `base_dir` by default.
