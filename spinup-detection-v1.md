# Spinup detection & deployment v1 — implementation spec

Topology is the sole source of truth for capability (Flynn ruling,
2026-07-19): no capability registry, no cached "what works" — the machine
is asked, live, at every placement decision, and org-owned artifacts are
deployed idempotently as part of the same act. Records exist only as
HISTORY (where placed agents live; what was detected/failed, when) —
never consulted as capability authority. This is tenet T2 applied to
placement.

Repo: worktree `~/src/tightbeam_ex-spinup` (branch `spinup-detection`,
cut from main). Decision-complete; implementer decides internal naming
and test layout only. Gates: `mix compile --warnings-as-errors` clean,
`mix test` fully green. Do not commit. STOP and report on any conflict.

## Invariants (implementation is checked against these)

1. THE MACHINE IS THE TRUTH: no code path records a capability fact and
   consults it later. Every placement decision (spawn; tune set_host;
   tune set_harness) probes the target host at that moment.
2. DETECT + DEPLOY ARE ONE IDEMPOTENT ACT: org-owned artifacts —
   directories, ACP adapters, org CLI — are ENSURED (created/installed
   only if missing; cheap no-op when present). CREDENTIALS are only ever
   DETECTED, never copied, written, or deployed (grant doctrine: logins
   are the operator's act).
3. DENIALS NAME THE GAP AND THE REMEDY, as found on the machine at that
   moment: e.g. "host tars is not ready for claude: no credentials in
   /Users/mike/.tightbeam/auth/claude (run the setup ceremony there)".
4. TURN-TIME UNTOUCHED: no probing anywhere except the placement
   decisions listed above. Running adapters, lanes, wakes: zero change.
5. HISTORY, NOT AUTHORITY: every spinup writes one lifecycle event
   (findings, actions taken, outcome) for forensics. Nothing reads it
   back for decisions.
6. Local host with everything present behaves as today (the probe finds
   everything, deploys nothing, allows).

## New module: `lib/tightbeam/spinup.ex`

`ensure_ready(config, harness, host_name, opts \\ [])` →
`:ok | {:error, %{code: "host_unready", message: String.t()}}`

`config` = the Gateway config map (base_dir etc.); `opts[:sh]` =
injectable runner exactly like `Placement.deliver_home` (default
System.cmd) so tests capture command lines. Host config comes from
`Placement.hosts(config.base_dir)` (addressing only — ssh + base_dir).
Unknown host name → the existing unknown_host denial shape (reuse
Placement's wording).

Sequence (local when `ssh: nil`, else over `ssh` with Placement's
@ssh_opts; every remote command shell-quoted like deliver_home's link
script):

1. REACH: local → :ok; remote → `ssh <dest> true`. Failure →
   `host_unready`: "host <name> is unreachable: <output>".
2. DIRS (deploy): ensure `<base>/auth/<harness>`, `<base>/work`,
   `<base>/identity/skills` exist (`mkdir -p` — already idempotent).
3. ADAPTER (detect, deploy if missing): the adapter binary is
   `<base>/adapters/node_modules/.bin/<claude-agent-acp|codex-acp>`
   remote, or the existing local resolution for the local host (reuse
   Placement's binary-path logic — extract it into a shared helper
   rather than duplicating). Missing remotely → deploy:
   `npm install --prefix <base>/adapters @agentclientprotocol/claude-agent-acp @agentclientprotocol/codex-acp`
   (both, matching assimilate), then re-check; still missing (or npm
   fails, e.g. no node) → `host_unready` naming what failed. Missing
   LOCALLY → `host_unready` naming the path (the local install is the
   operator's repo checkout; npm-installing into it is not ours to do).
4. CREDENTIALS (detect ONLY): claude ready = `oauth-token` OR
   `.credentials.json` present in `<base>/auth/claude`; codex ready =
   `auth.json` present in `<base>/auth/codex`. Missing →
   `host_unready`: "no <harness> credentials in <path> (run the setup
   ceremony on <name>)". Never create, copy, or push.
5. Record: `EventLog.lifecycle(db, "spinup", "<harness>@<host>",
   detail)` where detail is a compact summary of findings + actions
   ("reached; adapters present; credentials present" / "deployed
   adapters; DENIED: no credentials..."). db passed via opts[:db]
   (default Tightbeam.DB). Written for BOTH allow and deny outcomes.

Batch remote commands sensibly (one ssh for reach+dirs+checks is fine;
the npm deploy is its own command) — but do not micro-optimize; clarity
first.

## Wiring (gateway.ex)

- `spawn_result`: after Placement.resolve succeeds and BEFORE
  Org.create / any idempotency write: `Spinup.ensure_ready(config,
  harness_atom, host)`. `{:error, denial}` → return the denial (spawn
  refused; nothing half-created).
- `tune set_host`: after resolve, before the workdir move:
  ensure_ready for the session's CURRENT harness on the NEW host.
- `tune set_harness`: ensure_ready for the NEW harness on the session's
  current host, before any state change.
- Adapter cold boot path: UNCHANGED (deliver_home already deploys homes;
  boot failure already degrades visibly). Do not add probing there.

## Out of scope (STOP conditions)

No changes to assimilate/CLI (its reduction is a follow-up), no
hosts.json field removals, no registry fields added anywhere, no probe
verb, no caching of any probe result, no changes to adapters/lanes/wire.

## Tests

1. Spinup unit (injectable sh, tmp base_dirs): local all-present → :ok,
   zero sh calls beyond none needed; local adapter missing → denial
   naming the path; creds missing → denial naming path + ceremony;
   remote: command sequence captured (reach, mkdir, checks) with
   shell-quoting asserted; remote adapter missing → npm deploy command
   issued then re-check; npm failure output → denial containing it;
   unreachable → denial with ssh output; lifecycle row written on allow
   AND deny (assert via EventLog.lifecycle_events).
2. Gateway: spawn to a not-ready host → denial surfaces, NO session row,
   NO role created, NO idempotency row; spawn to a ready host (stub sh)
   → proceeds as today. tune set_host/set_harness denial paths leave
   Org state unchanged.
3. Full suite green; files: `lib/tightbeam/spinup.ex` (new),
   `lib/tightbeam/gateway.ex`, `lib/tightbeam/placement.ex` (only the
   shared binary-path helper extraction), their test files.
