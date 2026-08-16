# Ceremony lifecycle — v1

Decided 2026-07-28 (Flynn). Makes "the gateway owns all lifecycle"
(SATELLITE.md) true for interactive ceremonies, where it is currently false.

## Problem

Adapters get the full supervision treatment — restart, backoff, circuit.
Processes involved in *ceremonies* get no owner at all. Three independent
sightings of the one hole:

- A `claude setup-token` ceremony ran for TWO DAYS on eurisko, orphaned to
  init, against a binary deleted from under it (#77). No timeout, no reaper.
- 40 stopped `tightbeam-producer` test shells accumulated on eezo (oldest
  2d11h): they `kill -STOP $$` themselves and nothing CONTs or reaps them when
  the parent BEAM dies (#87).
- Onboarding cancel is CLIENT-driven: the CLI dispatches `cancel` on failure.
  A CLI that dies between `begin` and `cancel` leaves the provider pending
  forever — no server-side lease timeout (#64's residue; the interactive-
  failure path itself was proven clean, three consecutive re-arms).

Pattern: anything spawned outside the supervision tree gets no timeout, no
lease, no reaper.

## Design

1. **Onboarding leases expire server-side.** `begin_onboard` records a
   deadline with the pending entry. Expiry is checked lazily at the read
   seams (next `begin`/`status`/`finish`) — no timer, no sweep, matching
   `Credentials`' stated posture ("expiry is compared only at read seams").
   An expired lease behaves exactly as a cancel: staging cleaned (local or
   over ssh, the existing clauses), pending cleared, the event logged with
   the reason `lease_expired`. TTL default generous — 30 minutes — because a
   human is in the loop; configurable like other timeouts in
   `production_config`.
2. **Ceremony children are bounded.** The CLI wraps each provider ceremony
   (`claude setup-token` under script(1); `codex login --device-auth`) in a
   watchdog: on expiry of the same TTL, the process GROUP is terminated and
   the failure reported as a timeout naming what was killed. Codex already
   self-limits at 15 minutes; claude's does not, and the eurisko orphan is
   what that looks like. Kill discipline per the standing pid rule: the
   wrapper signals only the group it created.
3. **The producer test fixture reaps itself.** `on_exit` reaps anything the
   fixture spawned, and the parked (`kill -STOP`) shell carries a
   self-limiting watchdog (CONT + TERM after a bound) so a fixture orphaned
   by a dying BEAM self-terminates instead of parking forever.
4. **One-time cleanup**, host-side, identity-verified per the standing pid
   rule (the `kill -STOP $$` cmdline shape is unambiguous; verify each pid's
   cmdline immediately before signalling):
   - eezo: the ~40 stopped `tightbeam-producer` shells.
   - eurisko: the Jul 26 `script`/`claude setup-token` pair (pids were
     1109018/1109020; RE-VERIFY, they may have died or been recycled).

## The definition of interactive onboarding (Mike, 2026-08-16; decisions ledger latest + 8287cd0)

Interactive onboarding is DEFINED as incomplete until the operator holds the
sign-in URL and code. The loop runs through the user: no code in the user's
hands means the user cannot finish, therefore the onboarding IS incomplete —
not a delivery step bolted on, the definition of the task itself.

Every "onboard <provider>" instruction means the FULL LOOP:
ceremony -> URL+code to operator (within one minute of minting: URL opened
on the operator's current browser host — ask Mike which; serenity as of
2026-08-16 — code waked to user mike and filed as an attest) -> operator
signs in -> credential installed and verified. Anything less is the task not
done, and a card for any ceremony MUST name the full loop as its acceptance.

(Origin: the 0.1.8 S2c saga — four ceremonies burned because the runbook
said only "onboard codex", activity language that named no loop; this
definition makes it a runbook fact future carding minds copy, not re-derive.
Release-plan instance: release-018-test-plan-v2.md S2 v2.15. When
wi_0535922b lands — onboard emitting url+code as structured output — the
same sentence propagates into the product repo's onboarding runbook: the
mechanism and the definition ship together.)

## Non-goals

- No change to the interactive-failure path — cancel works there, proven.
- No server-side process management of ceremony children (the gateway cannot
  reach a process on the operator's terminal; bounding them is the CLI's
  job — point 2).
- No producer-runtime changes beyond the fixture (production producer kill
  verification is #45's territory, already fixed).

## Acceptance

1. Kill the CLI between `begin` and `cancel` (test: begin, then never
   finish); after TTL, the next `begin` succeeds and the event log carries
   `lease_expired`. Before the fix this wedges until gateway restart —
   fail-before is demonstrable.
2. A ceremony child that outlives the TTL is terminated by the wrapper and
   the error names it. (Test with a stub provider command that sleeps.)
3. A suite run aborted mid-producer-test leaves zero `tightbeam-producer`
   processes (assert in the fixture's own teardown; the watchdog covers the
   SIGKILLed-BEAM case, verifiable manually).
4. Cleanup: zero stopped `tightbeam-producer` shells on eezo; the eurisko
   orphan pair gone; both verified by process-table absence, with each kill
   preceded by a cmdline identity check.
