# Soak & kill-matrix driver v1 — implementation spec

A chaos driver that runs a DEDICATED tightbeam gateway under sustained
message load while killing its processes on a schedule, then audits the
substrate's invariants from the database. Proves "recovers" rather than
"recovered when I tested recovery."

Repo: worktree `~/src/tightbeam_ex-soak` (branch `soak-driver`, cut from
main). NEW FILES ONLY: `scripts/soak.exs`, `docs/SOAK.md`, and
`test/soak_script_test.exs` if the helpers warrant unit tests. ZERO
changes to `lib/` or existing files — if the driver seems to need a lib
change, STOP and report. Gates: `mix compile --warnings-as-errors` clean,
`mix test` green, plus `mix run scripts/soak.exs --minutes 2 --self-check`
completing with a PASS verdict against a scratch gateway. Do not commit.

## Invariants under audit (the whole point — assert ALL from the DB/logs)

A1. Every turn reaches a terminal status; no row stuck `running`/`queued`
    older than the stall threshold (default 180s) at audit time.
A2. Message integrity: every delivered turn has its echo and (for
    delivered) an assistant row; counts consistent; no duplicate
    (wakeId) turns.
A3. Every failure is a visible row with a reason: failed turns carry
    error text; adapter deaths appear in lifecycle events.
A4. No message lost across kills: every wake the driver scheduled is
    accounted for (fired+turn, or pending, or wake_unresolved).
A5. The gateway always came back: after every kill event, /version
    answered within the recovery threshold (default 60s).

## Driver behavior

`mix run scripts/soak.exs -- --minutes N [--port P] [--base-dir D]
[--kill-every S] [--load-every S] [--sessions K] [--self-check]`

- Boots its OWN gateway (subprocess, `mix run --no-halt`, fresh base_dir
  default `~/.tightbeam-soak`, port default 11999, model haiku, claude
  only). SAFETY: refuses to run if base_dir exists and lacks the marker
  file `.soak-arena` it creates on first boot; NEVER touches any other
  base_dir or port. Reuses the org claude token by symlinking the auth
  dir read-only fashion (copy the oauth-token file is FORBIDDEN — symlink
  the existing `~/.tightbeam-beam/auth/claude` dir as the arena's auth/claude).
- Load: spawns K sessions (default 3) via /agent/dispatch, then every
  `--load-every` (default 20s) sends a short prompt (haiku-cheap, e.g.
  "reply with one word") round-robin: direct posts and wakes alternated,
  occasional queued bursts of 3.
- Kill matrix, one event every `--kill-every` (default 120s), cycling:
  (1) SIGKILL a random adapter process; (2) SIGTERM the gateway, wait
  exit, restart; (3) SIGKILL the gateway, restart; (4) cancel a running
  turn via the API mid-flight. Log each event with timestamp to stdout
  and to `<base_dir>/soak-events.log`.
- Audit: at the end (and every 10 minutes in long runs) run A1–A5 against
  the arena DB via sqlite queries from the script (Exqlite is already a
  dependency; open the DB read-only). Emit a scorecard: per-invariant
  PASS/FAIL with offending rows printed. Exit 0 only if all PASS.
- `--self-check`: 2-minute smoke of the driver itself (1 session, one
  kill of each type, audit) — this is the acceptance gate.

## docs/SOAK.md

One page: what it proves (A1–A5), how to run the 2-minute self-check,
the 1-hour default, and the 24h mode (`--minutes 1440`); where results
land; the rule that a FAIL blocks deploy of whatever changed; note that
the arena is disposable (`rm -rf` after).

## Out of scope

No multi-host kills (loopback ssh chaos is a v2), no codex load (claude
only until codex smoke leg completes), no changes to lib/, no CI wiring.
