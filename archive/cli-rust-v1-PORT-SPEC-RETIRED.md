# Tightbeam CLI in Rust — port spec (v1)

Faithful port of the reference CLI from TypeScript/Node to a single
static Rust binary, living IN THE ELIXIR REPO. The behavioral source of
truth is the existing implementation at
`/Users/mike/src/tightbeam/src/cli/main.ts` — read it first and port its
observable behavior exactly; where this spec and that file disagree on
behavior, STOP and report. Motivation: agents invoke this CLI constantly
and pay Node's startup tax every time; and the operator hates Node.

Repo: worktree `~/src/tightbeam_ex-clirs` (branch `cli-rust`, cut from
main). New cargo project at `cli/` (package + binary name `tightbeam`,
edition 2024). Toolchain present on this machine (cargo 1.93). Gates:
`cargo build --release`, `cargo test`, `cargo clippy -- -D warnings` all
clean in `cli/`, AND the repo's `mix compile --warnings-as-errors` +
`mix test` still fully green. Do not commit. STOP on any conflict.

## Invariants

1. WIRE-IDENTICAL: every command produces byte-equivalent dispatch
   bodies to the TS CLI (same verb strings, same param keys incl.
   camelCase like sessionKey/idempotencyKey, same typed target fields,
   same identity fields as/asUser/asProcess). The gateway must not be
   able to tell which CLI called it.
2. UX-FAITHFUL: same commands, flags, positional shapes, error messages
   for usage errors (match the TS strings), same help content (port the
   HELP text verbatim, adjusting only the header line if needed), JSON
   result on stdout, human error on stderr, exit 0/1 semantics.
3. THIN STAYS THIN: no retries, no caching, no state, no config files
   beyond the existing discovery chain. Dependencies: `serde_json` and
   ONE minimal blocking http client (`ureq`, default features) — nothing
   else (NO clap/tokio/anyhow/reqwest; args are hand-parsed like the TS
   original; errors are plain strings).
4. CEREMONIES INTERACTIVE-HONEST: `setup` and `assimilate` drive child
   processes inheriting the tty; both detect non-tty stdin/stdout and
   degrade exactly as the TS versions do (print the manual commands /
   skip ONBOARD with the warning).

## Behavior to port (checklist — the .ts file is normative for each)

- Discovery: TIGHTBEAM_URL + TIGHTBEAM_TOKEN env, else
  `$TIGHTBEAM_HOME/gateway.json`, else `~/.tightbeam/gateway.json`
  (fields: cliToken; URL from... read the TS `discover` logic and match
  it, including the error text when nothing is found).
- Dispatch: POST {url}/agent/dispatch, Authorization Bearer, JSON body;
  print response body JSON to stdout (pretty like the TS? match it);
  non-2xx or {"error":...} → stderr + exit 1 (match TS behavior).
- Identity flags: exactly one of --as / --as-user / --as-process;
  wording of the exclusivity error matches TS.
- Typed targets: exactly one of --session/--role/--user where a target
  is required (wake), --session only for retire; params emitted as
  sessionKey/role/userId; the exactly-one CLI error text matches TS.
- Commands: wake (--prompt required, --after durations <n>ms|s|m|h,
  --at epochMs), spawn (--display required; --name registers a role;
  --archetype/--harness/--model/--host/--key; overrides NOT exposed —
  parity with TS), list, retire (--key), cancel-wake <wakeId>,
  role create|bind|rm|list, skill list|put(--file)|rm,
  approve-device/deny-device/revoke-device/promote-user(--demote),
  setup (--base-dir/--harness/--force; drives `claude setup-token` /
  `codex login` with CLAUDE_CONFIG_DIR/CODEX_HOME env; prints the
  oauth-token save hint for claude), assimilate (<ssh-dest> --name
  --base-dir --harness --push-credentials --no-onboard --dry-run; the
  full step sequence PROBE/DIRS/CREDENTIALS/ONBOARD/ADAPTERS/CLI/
  REGISTER with the same step-log format and summary; ssh/scp/rsync via
  std::process with BatchMode/ConnectTimeout options identical to TS).
- assimilate's CLI-ship step changes ONE way, deliberately: it ships
  THIS binary (`std::env::current_exe`) to `<base>/bin/tightbeam` (no
  node shim on the satellite). Before shipping, compare the satellite's
  `uname -sm` against this binary's compile target; on mismatch, WARN
  with a named remedy ("build for <triple> and re-run") and skip the
  CLI step — never ship a wrong-arch binary silently.
- help: port the HELP string; unknown-command error lists the same
  command set.

## Structure (suggested, not binding beyond testability)

`cli/src/main.rs` thin; modules: `args` (parse → typed Command enum),
`dispatch` (discovery + request build + http), `ceremonies` (setup,
assimilate). REQUIRED for tests: request-building must be a pure
function (Command → (path, headers-sans-token-value, body_json)) so unit
tests assert wire bodies without network.

## Tests (cargo test; no network, no tty)

Arg parsing: every command's happy shape; identity exclusivity (0 and 2
given); typed-target exactly-one incl. retire's session-only; duration
parsing (30s/5m/2h/250ms, garbage rejected with TS-matching message);
unknown command text. Request building: byte-exact JSON bodies (assert
against literals copied from the TS behavior) for wake (all three target
types, --after math NOT baked in — afterMs computed; assert key
presence), spawn with role name, role bind, skill put (file content
embedding), promote-user --demote. Discovery precedence with temp dirs +
env. Ceremony arg validation (unsupported harness). Non-tty detection
paths return the manual-command outputs (capture as strings).

## Elixir-side integration (the ONLY lib change)

`Gateway.install_cli_bin/1`: if `cli/target/release/tightbeam` exists
relative to the repo (resolve like the current dist path is resolved),
COPY that binary into `<base_dir>/bin/tightbeam` (mode 0755) instead of
writing the node shim; else keep today's shim exactly (fallback while
unbuilt). Update its test to cover both paths. NOTHING else in lib/
changes.

## Out of scope (STOP conditions)

No TS repo edits (it remains until the operator retires it). No new
verbs or behavior improvements — parity only (file any temptation as a
report note). No cross-compilation setup, no CI, no release packaging.
No async runtime. No changes to gateway behavior beyond install_cli_bin.

## CONFLICT RULINGS (round 1 — spec vs TS source; these are final)

1. Identity flags: TS silently prioritizes --as > --as-user >
   --as-process when several are given. The Rust port REFUSES multiples
   with the exclusivity error (help already says "Pass exactly ONE").
   DELIBERATE DIVERGENCE: silent priority is an untyped-seam behavior;
   refusal matches org doctrine. Note it in the module doc.
2. 2xx responses whose body is {"error": ...}: TS prints nothing and
   exits 0 — a bug (swallowed failure). The Rust port prints the body to
   stderr and exits 1. DELIBERATE DIVERGENCE: failures are visible.
3. Assimilate mechanics: the TS is right and the spec was wrong — ssh
   with BatchMode=yes only (no ConnectTimeout), ssh/scp for transfers,
   rsync merely PROBED for. Port the TS as-is; strike the spec's
   ConnectTimeout/rsync wording.
Everything else: TS remains behaviorally normative per the main spec.
