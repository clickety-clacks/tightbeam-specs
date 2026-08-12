# Probe v1 — lineage marker + machine-facts diagnostics (implementation spec, r4)

Status: DRAFT r4 after third adversarial review (codex xhigh; 2
blocking + 2 important + 1 minor findings resolved below). Parent
design: supervision-v1.md (§Forensics — PROBE, triggered not
resident). This spec is the sole authority for the build lane;
supervision-v1.md is background.

Revision note (r3 → r4): B1 root truth extended — SQLite's WAL
sidecars `state.db-wal`/`state.db-shm` (db.ex:101 pins
`journal_mode=WAL`) join the closed root set beside the 11 canonical
entries and the stderr logs; B2 dual adapter-name matches (reachable:
spinup's and assimilate's npm install line carries BOTH names) emit
one row per (pid, harness) pair, `adapter_candidates` sorted by
(pid, harness); I3 `base_dir.status` itself pinned (metadata ok but
read_dir fails → `"unreadable"`, count null, note); I4 stderr caveat
extended to outside-root escape via `/`-`..` components, not just
nesting; M5 old-CLI error text corrected to `unknown command: probe`
(args.rs:582). All r1→r3 resolutions retained.

The forensic census tool: `tightbeam probe`, run ON a machine
(typically over ssh by a supervisor or the gateway), reports processes
that CLAIM the org's lineage marker, adapter-looking processes, and
basic host facts — as one JSON document. Triggered, never resident: no
daemon, no launchd, no schedule; it ships inside the CLI binary. It is
ACCIDENT-GRADE evidence for a judgment already in the loop: markers
are process-owned, spoofable, and launderable (deliberately, or
innocently via `env -i`, `sudo`, ssh hops, containers, hermetic build
tools), so absence reads "possibly laundered," NEVER "definitely
gone" — and presence reads "claimed," never "proven." Both postures
ride structurally in the schema (per-row `evidence`, constant
`epistemics`), because the substrate never concludes.

BUILD ORDERING: cut worktree `~/src/tightbeam_ex-probe` (branch
`probe`) from main AFTER the cli-rust branch merges; the subcommand
lands in the existing cargo project at `cli/`. If `cli/` is absent
from main, STOP and report — do not vendor around it. Statute engine,
attest, and session-tokens are NOT prerequisites (probe dispatches
nothing).

## Goals

1. Emit the marker: every adapter process spawned by placement carries
   `TIGHTBEAM_LINEAGE` in its environment, in a canonical shell-safe
   encoding, so everything the harness spawns inherits it (inheritance
   survives orphaning and double-fork).
2. Census: `tightbeam probe` enumerates own-user-visible processes and
   returns marker-claiming candidates (pid, ppid, pgid, start-time
   estimate, cwd, executable, claimed lineage, evidence grade),
   adapter candidates, per-identity grouping, and host facts —
   versioned JSON, read-only, no side effects, no network.
3. Honest evidence: every detection row carries an `evidence` grade;
   scanned counts and constant epistemic framing appear in EVERY
   document, including the empty census.

## Non-goals (later specs; do not build)

Ephemeral watcher. Session-grain attribution (the marker is
identity-grain — sessions share adapters; the attribution ladder is
supervisor judgment, supervision-v1 §Forensics). Kernel-grade custody
(cgroups). Authenticated provenance (a marker is a CLAIM by
construction; signing/verifying it is a different design). Any gateway
verb, ledger row, or dispatch call. Windows or any platform beyond
macOS/Linux. No UI.

## The marker (the ONLY lib/ change) — B5

Identity names and host names are NOT constrained: archetype
validation forbids only empty and `--` (archetypes.ex:962), host
registration validates nothing (placement.ex:133) — whitespace, `:`,
`@`, `/`, and shell metacharacters are all legal today, and this spec
changes NO validation. Therefore the marker value is a canonical
encoding, shell- and whitespace-safe for ANY inputs:

    payload = "<identity_name>@<host>"          (UTF-8)
    value   = "tb1-" <> base64url_no_pad(payload)

Alphabet `[A-Za-z0-9_-]` plus the version prefix: no whitespace, no
shell metacharacters, by construction. The version prefix makes future
encodings distinguishable; probe decodes `tb1-` and reports any other
form as an undecoded claim. Harness is deliberately NOT in the payload
(identity grain per supervision-v1; harness is recoverable from the
adapter-candidate executable). Elixir emission:
`"tb1-" <> Base.url_encode64("#{identity_name}@#{host}", padding: false)`.

In `Placement.adapter_opts/2` (`{harness, identity_name, host}`):

- local branch: append `{"TIGHTBEAM_LINEAGE", value}` to the Port env
  list.
- remote branch: append `TIGHTBEAM_LINEAGE=<value>` to `remote_env`
  UNQUOTED. The value's alphabet is `[A-Za-z0-9_-]` plus the `tb1-`
  prefix, so the whole assignment contains no whitespace and no shell
  metacharacters — it is sh-safe BY CONSTRUCTION through both reparse
  layers: the Conn's local `sh -c` argv join (acp/conn.ex:80), whose
  escaping the LOCAL shell consumes, and ssh's space-join that the
  remote shell reparses. Do NOT `shell_quote` this assignment —
  quoting would leave literal quote characters in the ssh process's
  argv element and defeat the darwin whitespace-boundary extraction
  rule below. This exemption is specific to this assignment; a future
  encoding that widens the alphabet must bump the `tb1-` prefix and
  revisit it. ALSO set the ssh wrapper's local Port env to
  `[{"TIGHTBEAM_LINEAGE", value}]` (currently `[]`) so a gateway-side
  probe sees remote transports.

Nothing else in lib/ changes.

## Command

`tightbeam probe [--json] [--base-dir DIR]`

Standalone: no gateway discovery, no TIGHTBEAM_URL/TOKEN, no HTTP —
the discovery chain is not consulted and its absence is not an error.
Base dir resolution: `--base-dir`, else `$TIGHTBEAM_HOME`, else
`~/.tightbeam`; a missing base dir is a reported fact, never a
failure. Unknown flags / positional args → the CLI's standard usage
error. Add one `probe` line to HELP (existing style); approved delta
from cli-rust-v1's verbatim-port rule.

Exit codes: 0 whenever the census ran — empty machine, missing base
dir, degraded facts are all successful answers. 1 only for usage
errors and fatal collection failure (the enumeration pass itself
failed or timed out; unsupported platform). Human error on stderr,
exit 1, per CLI convention.

## Evidence grades (the per-row epistemic unit)

Every candidate row carries `evidence`, one of:

- `"environ_exact"` — Linux: exact key `TIGHTBEAM_LINEAGE` found in
  `/proc/<pid>/environ`.
- `"argv_or_env_indistinguishable"` — Darwin: the token was observed
  in the flattened `ps -E` line, where Apple's ps concatenates argv
  and environment with no boundary — an argv-only string matches
  identically (live-verified in review). The ssh wrapper's unquoted
  marker assignment in argv is an EXPECTED true positive at this
  grade.
- `"env_unreadable"` — Linux: the `environ` read failed with any
  non-ENOENT error (EACCES — environ is ptrace-gated — EPERM, or any
  other I/O class): no claim observable either way.
- `"none_observed"` — the observable surface was read and no marker
  was found. NOT proof of absence; the row states what was looked at,
  never what exists.

`marked_candidates` rows carry only the first two grades (a claim was
observed). `adapter_candidates` rows may carry any of the four.
`lineage` is a CLAIM everywhere: any process can set the variable or
embed the token; nothing authenticates it (epistemics carries this as
a constant).

## Collection mechanics (per platform; all reads behind injectable seams)

Platform selected at runtime from `std::env::consts::OS`: `"macos"` →
ps strategy; `"linux"` → procfs strategy; anything else → fatal
"unsupported platform". NO new crates: `std::fs` (procfs),
`std::process` (`ps`/`lsof`/`uname`), and the already-present
`serde_json`.

External-command deadlines: the enumeration pass (darwin pass 1)
gets 1500ms — breach → kill, fatal exit 1 (no census is possible).
Every other spawned command (`ps` pass 2, `ps` etime, `lsof`,
`uname`) gets 1000ms — breach → kill the child, null the facts it
would have supplied, append a note naming the command. Implemented as
spawn + `try_wait` poll + kill (std only). `<2s` total is a TARGET;
the deadlines are the enforcement seam.

Linux (procfs; pinned pipeline):

Snapshot: readdir `/proc`, collect numeric entries once;
`pids_scanned` = that count, fixed at snapshot time. Per pid, in this
ORDER:

1. `stat` — parse after the LAST `)` (comm may contain spaces and
   parens): ppid (field 4), pgid (field 5), starttime (field 22,
   retained for the stability check). Any error → row dropped.
2. `environ` — NUL-split, EXACT key match. Ok → claim or none;
   ENOENT → dropped; any other error → env-unreadable.
3. `cmdline` — NUL-split; adapter pattern match (below). ENOENT →
   dropped; any other error → treated as no match.
4. Candidates only (marker claim ∨ adapter match): `exe` readlink →
   `executable` (any error → null); `cwd` readlink (any error →
   null).
5. re-read `stat` — ENOENT or starttime ≠ step 1's → row DROPPED
   (exit or pid reuse mid-read).

Retention per error class (closed table — B3; every failure is one of
these, and every dropped pid stays counted in `pids_scanned`):
- `stat` any error (ENOENT included) → dropped (identity/stability
  unestablishable).
- `environ` ENOENT → dropped (process gone).
- `environ` any other error (EACCES, EPERM, any I/O class) + adapter
  cmdline match → RETAINED as adapter candidate, evidence
  `"env_unreadable"`.
- `environ` any other error + no adapter match → not a candidate;
  counted in `pids_env_unreadable`.
- `cmdline` ENOENT → dropped.
- `cmdline` any other error → adapter match unobservable, treated as
  no match (the row survives only via a marker claim).
- `exe`/`cwd` error of ANY class (ENOENT included) → that field
  null, row RETAINED — liveness is the re-stat guard's job, not
  exe/cwd's.
- re-stat ENOENT or starttime mismatch → dropped.
Note procfs may hide processes entirely (hidepid mounts): the
snapshot is what the mount showed — platform_limits says so.

macOS (ps; there is no procfs):

- Pass 1 (enumeration): one `ps -axEww -o pid=,command=`. `-E`
  flattens each process's argv AND exec-time environment into one
  string — visible only for same-euid processes, and Apple platform
  binaries can hide it even own-user (live review finding: Homebrew
  node's env visible, own-user `/bin/sleep`'s invisible; Apple ps
  collapses KERN_PROCARGS2 failure to a bare command name with no
  error signal). Consequences, ruled: darwin detection is
  CANDIDATE-GRADE, evidence `"argv_or_env_indistinguishable"` on
  every marked row, and `pids_env_unreadable` is NULL on darwin — it
  is not computable, and pretending otherwise is the overclaim the
  parent forbids. Extraction rule, pinned (B5): a row is a candidate
  iff its line contains at least one `TIGHTBEAM_LINEAGE=` preceded by
  whitespace or column start; each occurrence's token is the
  following run of non-whitespace (canonical values are
  whitespace-free; a spoofed value truncates at whitespace — it is a
  claim either way). One line may carry SEVERAL bounded occurrences
  (the wrapper's argv assignment plus its env image): the row's token
  is the FIRST occurrence that decodes; if none decodes, the first
  occurrence (prefer-decodable-first). `pids_scanned` = pass-1 row
  count.
- Pass 2, candidates only: `ps -o pid=,ppid=,pgid=,comm= -p <list>`;
  comm is the last column (join the remainder — paths may contain
  spaces) and maps VERBATIM to `executable` — darwin's only source
  for that field (B2). Pid absent from pass-2 OUTPUT while the
  command succeeded → row dropped (it exited). The pass-2 COMMAND
  failing or breaching its deadline → ppid, pgid, executable null on
  every candidate row, rows RETAINED, note appended — per-pid absence
  is evidence about the process; whole-command failure is evidence
  about the probe (I7).
- cwd, candidates only: one `lsof -n -a -p <list> -d cwd -Fn`,
  parsed from `p<pid>`/`n<path>` pairs; deadline breach, missing
  lsof, or failure → cwd null for all candidates + note.

Both platforms:

- Token decoding: strip `tb1-`, base64url-no-pad decode, UTF-8 →
  `lineage` (the decoded `identity@host` claim). Malformed base64,
  invalid UTF-8, or an unknown prefix → `lineage` null, raw token
  kept.
- Bytes → JSON (B4): OS-derived bytes (procfs blobs, ps output,
  paths, raw tokens) need not be UTF-8; JSON strings must be. Every
  OS-derived string crossing into the document — `executable`, `cwd`,
  `hostname`, `lineage_raw` — is converted LOSSILY (invalid sequences
  → U+FFFD). No rejection, no null-for-undecodable: visibility beats
  purity in a forensic tool. The raw token specifically: truncate the
  observed BYTES at 256 bytes (bounded output; it is the claim
  itself, under our own variable name — reporting it is in-contract);
  `lineage_raw` = lossy conversion of those bytes; `lineage_raw_b64`
  = standard base64 of those same bytes, non-null IFF the conversion
  replaced anything — byte-exact recovery for exactly the rows where
  the string form lies. Rows with no observed token carry all three
  lineage fields null (B2).
- Start times, candidates only: one `ps -o pid=,etime=` invocation;
  grammar `[[dd-]hh:]mm:ss` with dd 1..5 digits, hh 0..23, mm/ss
  0..59; any component out of bounds, parse failure, or checked
  arithmetic overflow → `elapsed_s` and `started_at_s` null (+ note
  only if `ps` itself failed — the same whole-command vs per-pid
  split as pass 2). `probed_at_ms` is sampled ONCE, before
  enumeration; `started_at_s = floor(probed_at_ms/1000) - elapsed_s`.
  This is a WHOLE-SECOND ESTIMATE: etime has 1s granularity and the
  candidate may have been measured up to `collection_ms` after
  `probed_at_ms` — consumers comparing against ledger windows must
  pad by at least `1s + collection_ms`. The spec states this;
  `collection_ms` in the output makes it computable. `collection_ms`
  itself (I7): the MONOTONIC-clock delta from the `probed_at_ms`
  sampling instant to the start of serialization — wall clock stamps
  the run, the monotonic delta bounds it.
- hostname: `uname -n`, trimmed; failure → `"(unknown)"` + note.
- Adapter candidates: a process whose cmdline (Linux) or pass-1 line
  (darwin) contains `claude-agent-acp` (harness `claude`) or
  `codex-acp` (harness `codex`) — the adapter binary names from
  `Placement.adapter_binary_path/2`. This is SUBSTRING evidence:
  editors, greps, and ssh transports mentioning the name match too —
  hence *candidates*, with the same evidence grading; detection is
  independent of the marker (a laundered adapter still surfaces,
  evidence `"none_observed"` or `"env_unreadable"` — the
  disagreement between the two lists IS the diagnostic). A line
  matching BOTH names — reachable, not hypothetical: spinup's and
  assimilate's adapter install is one npm command carrying both
  (spinup.ex:122-124, ceremonies.rs:368-371) — emits TWO rows, one
  per matched harness: a row per (pid, harness) pair, identical
  process fields, each graded exactly as a single match would be.
  Deterministic and honest — no precedence rule to defend.
- Candidate passes run once over the UNION of both candidate lists
  (B2): pass 2, exe/cwd, and etime cover marker-and-adapter
  candidates alike; a pid on both lists reports identical values in
  both rows.
- The probe's own pid (`std::process::id`) is excluded from both
  candidate lists (a probe launched from a marked shell inherits the
  marker; ancestors are reported, itself is noise).
- Env facts are exec-time images on BOTH platforms (procfs environ
  and KERN_PROCARGS2 alike): post-exec setenv changes are invisible.
  Fine for our purpose — the marker is set at exec — noted here, not
  per-run.

## Privacy contract (enforceable, not aspirational)

The collector NECESSARILY receives full environment and argv buffers
from the OS — `ps -E` output contains every visible env entry of
every process (including live `TIGHTBEAM_TOKEN` and
`CLAUDE_CODE_OAUTH_TOKEN` values placed by placement), and
`/proc/<pid>/environ` is read as a whole blob. The contract is
therefore about what LEAVES the process, and it is absolute:

- Raw buffers (env blobs, ps lines, cmdline, lsof output) are
  process-internal only. They MUST never be written to stdout or
  stderr, logged, persisted, embedded in `notes`, error messages, or
  panic diagnostics — in ANY code path, including failures.
- Only the enumerated schema fields cross the process boundary:
  decoded/raw lineage token (bounded, our own variable; its
  byte-exact `lineage_raw_b64` when lossy), pids, executable paths,
  cwd, times, and the fixed epistemics strings.
- Full argv is never reported — executable path only (command lines
  carry secrets).
- Implementation rules: parse/decode errors produce CONSTANT
  messages that echo no input bytes; no `Debug`-format of raw
  buffers on error paths; no `unwrap`/`expect` on buffer-derived
  values whose panic payload would embed content.
- "Reads no file contents" is scoped honestly: probe reads procfs
  process metadata by design (Linux) and performs existence-only
  checks under the base dir; it never opens base-dir or user file
  CONTENTS.

## Output schema (the contract; --json emits exactly this)

Serialized from structs via `serde_json::to_string_pretty` + trailing
newline, snake_case keys in this order (probe's OWN schema, not
gateway wire). Deterministic: `marked_candidates` sorted by pid
ascending, `adapter_candidates` by (pid, harness) ascending;
`identity_candidates` keys sorted (BTreeMap). Every field
always present; unknown facts are null or empty, never missing keys.

    {
      "schema": "tightbeam.probe.v1",
      "probed_at_ms": 1752900000000,
      "collection_ms": 240,
      "host": { "hostname": "eezo", "platform": "macos" | "linux",
                "probe_version": "<CARGO_PKG_VERSION>" },
      "base_dir": {
        "path": "/Users/org/.tightbeam",
        "status": "present" | "absent" | "unreadable",
        "entries": { "adapters": "...", "assets": "...", "auth": "...",
                     "bin": "...", "gateway.json": "...",
                     "homes": "...", "hosts.json": "...",
                     "identity": "...", "staging": "...",
                     "state.db": "...", "work": "..." },
        "adapter_stderr_log_count": 2
      },
      "marked_candidates": [
        { "pid": 4242, "ppid": 1, "pgid": 4242,
          "lineage": "resident@eezo",
          "lineage_raw": "tb1-cmVzaWRlbnRAZWV6bw",
          "lineage_raw_b64": null,
          "evidence": "environ_exact",
          "executable": "/usr/local/bin/node",
          "elapsed_s": 8021, "started_at_s": 1752891979,
          "cwd": "/Users/org/.tightbeam/work/9f8a3c2d1b40" },
        { "pid": 4290, "ppid": 4242, "pgid": 4242,
          "lineage": "resident@eezo",
          "lineage_raw": "tb1-cmVzaWRlbnRAZWV6bw",
          "lineage_raw_b64": null,
          "evidence": "environ_exact",
          "executable": "/usr/bin/git",
          "elapsed_s": 63, "started_at_s": 1752899937,
          "cwd": "/Users/org/.tightbeam/work/9f8a3c2d1b40" }
      ],
      "identity_candidates": { "resident@eezo": [4242, 4290] },
      "adapter_candidates": [
        { "pid": 4242, "harness": "claude", "ppid": 1, "pgid": 4242,
          "lineage": "resident@eezo",
          "lineage_raw": "tb1-cmVzaWRlbnRAZWV6bw",
          "lineage_raw_b64": null,
          "evidence": "environ_exact",
          "executable": "/usr/local/bin/node",
          "elapsed_s": 8021, "started_at_s": 1752891979,
          "cwd": "/Users/org/.tightbeam/work/9f8a3c2d1b40" },
        { "pid": 5100, "harness": "codex", "ppid": 1, "pgid": 5100,
          "lineage": null, "lineage_raw": null,
          "lineage_raw_b64": null,
          "evidence": "none_observed",
          "executable": "/usr/local/bin/node",
          "elapsed_s": 122, "started_at_s": 1752899878,
          "cwd": "/Users/org/code" }
      ],
      "epistemics": {
        "census_grade": "accident",
        "absence_means": "possibly_laundered",
        "lineage_is_claim": true,
        "pids_scanned": 312,
        "pids_env_unreadable": 41,
        "platform_limits": [ "..." ],
        "notes": []
      }
    }

Field rulings:
- Root contents, the CLOSED set the code actually creates (B1): the
  11 canonical entries below, PLUS SQLite's WAL sidecars
  `state.db-wal`/`state.db-shm` (db.ex:101 pins
  `PRAGMA journal_mode=WAL`, so they appear beside `state.db` on any
  running or uncleanly-stopped gateway), PLUS the variable
  `adapter-*.stderr.log` files. `entries` reports the 11 canonical
  names; the sidecars are NOT separate keys — they are `state.db`'s
  runtime artifacts, and their presence tracks DB activity, not
  layout — and the stderr logs are counted, not listed. A consumer
  diffing a live root against `entries` must expect both.
- The 11 canonical entries — gateway: `state.db` (application.ex:54),
  `assets/` (assets.ex:98), `gateway.json` (gateway.ex:134),
  `hosts.json` (placement.ex:148), `bin/` (gateway.ex:610),
  `staging/` (placement.ex:265), `work/` (gateway.ex:867),
  `identity/` (gateway.ex:1123), `homes/` + `auth/` (homes.ex:74-75),
  `adapters/` (placement.ex:495); satellite: `adapters/`
  (spinup.ex:120), `auth/`, `work/`, `identity/` (spinup.ex:180-182),
  `bin/` (assimilate CLI step, ceremonies.rs), `homes/`
  (placement.ex:628). Union: the 11 entries above — there is no
  `state/` and no `logs/`. Each TRI-STATE via `symlink_metadata`:
  Ok → `"present"`, NotFound → `"absent"`, other error →
  `"unreadable"`. Session workdirs are
  `work/<first-12-hex-of-sha256(session_key)>` (placement.ex:302,
  gateway.ex:862) — there is no `workdirs/` (I6).
- `base_dir.status` itself, pinned (I3): `symlink_metadata` on the
  base dir — NotFound → `"absent"`; any other error →
  `"unreadable"`; Ok → attempt `read_dir` (the stderr glob needs it):
  Ok → `"present"`, error → `"unreadable"` + note. Per-child entry
  checks run only when status is `"present"`. status `"absent"` →
  all entries `"absent"`, count null; `"unreadable"` → all entries
  `"unreadable"`, count null.
- Adapter stderr logs live at the base ROOT
  (`adapter-<harness>:<identity>@<host>.stderr.log`, placement.ex:357)
  — counted by `adapter_stderr_log_count` (glob
  `adapter-*.stderr.log`; null when base status ≠ present). CAVEAT
  (I4): the filename embeds RAW names, and `/` and `..` are legal in
  them — a slash-bearing identity/host nests its log below root,
  places it OUTSIDE the base root entirely (`..` components resolve
  upward), or fails creation; all three escape the glob. The count
  means "root-level adapter logs", and may UNDERCOUNT; stated here
  once, not per-run.
- Row shape (B2): `marked_candidates` and `adapter_candidates` rows
  carry the SAME process fields — pid, ppid, pgid, lineage,
  lineage_raw, lineage_raw_b64, evidence, executable, elapsed_s,
  started_at_s, cwd — with `harness` added on adapter rows. An
  adapter row is keyed by (pid, harness): a dual-match pid yields two
  rows differing only in `harness` (B2). A pid on both lists appears
  in both, with identical values.
- Lineage is TRI-NULL-consistent (B2): token observed and decoded →
  `lineage` and `lineage_raw` set; token observed, undecodable
  (unknown prefix or malformed) → `lineage` null, `lineage_raw` kept
  (`lineage_raw_b64` per B4) — the row remains a candidate; NO token
  observed (evidence `"none_observed"` or `"env_unreadable"`) → all
  three null. `identity_candidates` keys are decoded lineage where
  available, else `lineage_raw`; token-less rows appear under no key.
- `pids_env_unreadable` is an integer on linux (count of environ
  reads failing with non-ENOENT errors), NULL on darwin — not
  computable there.
- `platform_limits` is a constant array per platform, pinned here for
  golden tests — linux: ["environ is ptrace-gated; other-user and
  protected processes are unreadable", "procfs may hide processes
  entirely", "markers are spoofable env content"]; darwin: ["env
  visible only for same-euid processes; platform binaries may hide it
  even own-user", "ps flattens argv and env; marker position is
  indistinguishable", "markers are spoofable argv or env content"].
- `census_grade`, `absence_means`, `lineage_is_claim` are constants —
  the structural carrier of "possibly laundered, never definitely
  gone; claimed, never proven". `notes` is run-specific degradation
  text (constant strings + command names only, per the privacy
  contract); empty array when clean.
- Schema changes bump the `schema` string; fields are never
  repurposed.

## Human output (default, non-contractual)

Without `--json`: a terse summary — header (hostname, platform,
base_dir path + status), one block per identity listing its candidate
pids (pid, ppid, up-time, cwd, executable, evidence), an
`adapter candidates:` line, and ALWAYS a closing epistemics line,
e.g. `scanned 312 pids (41 env-unreadable) — claims, not proof;
absence may be laundered` (with `no marked candidates` prepended when
empty; on darwin the unreadable clause is omitted). Only `--json` is
a stable contract; the human form may change freely.

## What probe never does (acceptance lens, negative space)

No base-dir or user-file contents read (existence/count checks only;
procfs process metadata on Linux is in-contract per §Privacy). No env
dump — only `TIGHTBEAM_LINEAGE`-derived fields are reported. No full
argv reported. No network I/O. No writes: no logs, no state, no temp
files. No privilege escalation, no ptrace/DTrace, no per-pid retry
loops. No conclusions: no "stalled"/"gone"/"orphaned"/"verified"
labels anywhere in output.

## Rollout (I8)

Probe ships inside the CLI binary. Assimilate ships `current_exe`
ONLY when the remote target triple matches the assimilating host's
binary (ceremonies.rs:379-381 skips the CLI step on mismatch) — so,
per the same ruling session-tokens-v1 §Rollout pins for its CLI push,
mismatched-triple satellites are EXCLUDED from probe availability
until a matching binary is provided through that lane's stated path;
this spec invents no second mechanism. EXISTING satellites likewise
wait on the SAME satellite CLI-refresh path session-tokens-v1
§Rollout uses (spinup refreshes directories/adapters/credentials,
never the shipped CLI — spinup.ex). Until a satellite's CLI is
refreshed and triple-matched, the old CLI's `unknown command: probe`
error there (args.rs:582) is a rollout fact, not evidence.

## Invariants

1. Read-only and self-contained: zero writes, zero network; running
   two probes concurrently is trivially safe.
2. Nothing is proof: every detection row carries `evidence`; lineage
   is a claim; the constant epistemics fields appear in EVERY
   document, including the empty census.
3. Raw OS buffers never leave the process (§Privacy) — on any path,
   including errors and panics; everything that does leave is lossy
   UTF-8 (B4), byte-recoverable only via `lineage_raw_b64`.
4. Empty is success: exit 0 with a full schema-valid document on a
   machine with nothing tightbeam on it.
5. Marker emission is placement's only lib/ change: canonical `tb1-`
   encoding, no validation changes, remote assignment UNQUOTED
   (sh-safe by construction, B5); zero behavior change to any verb,
   adapter lifecycle, or existing env entries.
6. Platform mechanics live behind injectable seams; report assembly
   is a pure function of collected raw facts; every external command
   has a hard deadline.

## Structure & tests (cargo test; no network, no live process scans)

New module `cli/src/probe.rs` (+ `args` gains the Probe command).
REQUIRED for tests: raw collection (an injectable trait supplying
procfs reads / command outputs / deadline outcomes) is separate from
pure parsing and assembly (`RawFacts -> Report`).

Marker codec: encode/decode roundtrip for names containing spaces,
`:`/`@`/`$(`/quotes, and non-ASCII UTF-8; malformed base64 → lineage
null + raw kept; unknown prefix (`tb2-…`) → same; raw truncation at
256 BYTES pre-conversion; non-UTF-8 raw token → `lineage_raw` carries
U+FFFD and `lineage_raw_b64` the exact bytes; clean token → b64 null.
Parsers: environ NUL-split exact-key (hit, miss,
`X_TIGHTBEAM_LINEAGE` rejected); stat after-last-`)` with comm
containing `) (`; darwin pass-1 extraction (mid-line, end, absent,
whitespace-precedence rule, argv-embedded spoof STILL matches — and
is asserted to carry `argv_or_env_indistinguishable`; double
occurrence with one decodable → the decodable one wins regardless of
position; double occurrence with none decodable → first wins; a
quote-prefixed `'TIGHTBEAM_LINEAGE=…` occurrence does NOT match the
boundary rule); pass-2 comm-with-spaces join mapping to `executable`;
etime (`00:03`, `59:59`, `2:00:00`, `3-12:00:01`, `99:99` rejected,
garbage → null, overflow → null); lsof `-Fn` pairs; non-UTF-8 bytes
in exe/cwd/comm → U+FFFD strings, never errors. Linux pipeline: one
test per retention class (stat error, environ ENOENT dropped, environ
EACCES and EPERM each with and without adapter match, cmdline ENOENT
dropped vs cmdline EACCES no-match, exe/cwd errors of any class →
field null row retained, re-stat starttime mismatch → dropped while
`pids_scanned` holds the snapshot count). Assembly: grouping (two
identities, undecodable key falls back to raw, token-less rows
ungrouped); row-shape parity for a pid on both lists; unmarked
adapter row carries tri-null lineage + `none_observed`; self-pid
exclusion; harness mapping; a dual-name line (both adapter names, the
npm-install shape) → TWO rows for one pid, (pid, harness)-sorted,
identical process fields; darwin `pids_env_unreadable` null vs
linux integer; started_at math and `probed_at_ms` single-sampling.
Deadlines: mocked timeout on lsof → cwd null + note; on pass 2 →
ppid/pgid/executable null on all rows + note, rows retained; per-pid
absence from a SUCCESSFUL pass 2 → row dropped; on pass 1 → fatal.
Privacy: feed raw buffers containing sentinel `SECRETXYZ` through
every parser error path and a full assembly; assert the sentinel
appears in NO output, error string, or note. Schema stability: golden
byte-compare of a fully-populated report and of the EMPTY census
(fixed platform_limits strings included). Base-dir: temp-dir
tri-state (present/absent/unreadable), metadata-ok/read_dir-fail →
status `"unreadable"` + count null + note, closed 11-entry set
including `state.db` and `assets`, a root carrying
`state.db-wal`/`state.db-shm` still yields the 11-key entries map,
stderr-log glob count (root-level only).
Args: happy, `--json`, `--base-dir`, positional rejected, help text
includes probe.

Elixir side: extend the existing `Placement.adapter_opts/2` tests —
local opts env contains `{"TIGHTBEAM_LINEAGE", "tb1-" <> encoded}`;
remote command line contains the UNQUOTED assignment as its own argv
element (and no quoted variant); the ssh wrapper's Port env carries
the marker tuple; one roundtrip test decoding the emitted value back
to `identity@host` for a name containing a space.

## Handoff

Gates: `cargo build --release`, `cargo test`, `cargo clippy -- -D
warnings` clean in `cli/`; `mix compile --warnings-as-errors` clean;
full `mix test` green. Commit on the branch; do not merge. STOP and
report on any conflict with existing code or this spec.
