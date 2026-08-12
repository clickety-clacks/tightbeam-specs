# Session tokens v1 — per-session CLI credentials (implementation spec, r4)

Status: DRAFT r4, revised per joint adversarial review (codex xhigh,
tokens-r3-attest-r4-review). Parent design: containment-v1.md §Related
cheap win (container-independent, queued ahead of containment). This
spec is the sole authority for the build lane, and it OWNS THE
PRINCIPAL SEAM that attest-v1 (r4) consumes — see §Principal seam and
§Seam table. Constitution line
(tightbeam.md): every mutation passes the chokepoint attributed; this
lane makes agent attribution VERIFIED against a credential instead of
trusted as spoken, without new verbs, new origin classes, or any
thinking in the substrate.

Revision note (r1 → r2): asUser is now VERIFIED (claimed user must be
the token session's owner) instead of banned — this preserves the
shipped `--as-user` workflows (assimilate, admin skill verbs) and
retracts r1-D5's "operator's own shell" ruling; omitted identity
resolves through a four-rung ladder that unlocks Mains (the seeded
Mains hold zero roles; bindability truth in D7); the guidance-edit
non-goal is dropped in favor of one clarifying line; the typed
`principal` field is added as the seam attest-v1 binds authorization
to — threaded through Dispatch, nil on legacy org-token `--as`,
audit-visible in verb event rows; rollout now orders the
satellite CLI push before the gateway restart and states the honest
window; unique-index creation is pinned after the ALTER loop; remote
command semantics are pinned exactly (exit codes, stderr, mode heal);
registry additions: host-move residue (mitigated), git-exclude heal
(adopted), staging try/after, retire linearization, role-rebind race,
sharing-key citation fixed to {harness, identity_name, host}.

Revision note (r2 → r3): principal union goes four-way (`{:process,
name}` added; nil reserved for org `as <role>`); the joint review's
seam table is adopted verbatim as normative (§Seam table); the remote
mode-heal and git-exclude commands are corrected and re-pinned; D7
states the Mains-bindability truth; rollout rules heterogeneous
satellites excluded; the CLI-integration harness is authorized and
defined in §Tests.

Revision note (r3 → r4): the host-move source cleanup (D8d) is
ensure-absent on BOTH sides — a legitimately absent token file
(pre-first-turn workdir) counts as success; only a real removal
error fails the move.

Today every session's shell reaches `/agent/dispatch` with the one
org-wide cliToken, and identity (`--as`, `--as-user`) is trusted as
stated — a CLI call attributes to "someone in the org." After this
lane: each session holds its own token, minted at spawn, delivered
into its private workdir, dead at retire; the gateway resolves token →
session row and VERIFIES the stated identity against it. Statutes
that predicate on origin become meaningfully per-caller for delivered
credentials; the guarantee is deterministic attribution of the
credential presented, not OS-enforced caller identity — the same-user
filesystem holes are recorded in D8 and belong to containment.

## Goals

1. Verified identity: on session-token calls, `--as` is checked
   against the token session's live role binding and `--as-user`
   against its owner — never trusted as spoken.
2. Every session can act: role-holders via `agent:<role>`, any
   session for its owner via verified `asUser`, Mains implicitly as
   their owner — no session class is stranded.
3. Lifecycle welded to the session row: mint at spawn, survive boots
   (it is a column), go dark at retire (active-only lookup).
4. Delivery that heals: the workdir file converges to correct content
   AND mode at every turn start, on both harnesses, across host
   moves, harness switches, home regenerations, and file wipes.
5. A typed, race-free caller principal on the dispatch call, for
   consumers whose authorization needs proof (attest-v1 first).
6. Zero behavior change outside this feature's surface (device auth,
   all /api routes, wire frames, verbs, homes), with one deliberate
   exception: a single clarifying line in the builtin Operations
   guidance (§Guidance).

## Non-goals (do not build)

Token rotation or re-mint verbs. Hashing tokens at rest (device
tokens are plaintext rows; mirror that). New origin classes
(`session:` does not exist; the closed set stays user | agent |
process, T3). Retrofitting EXISTING verbs onto the principal seam —
they keep resolving origin strings as today (D8f). Updating the TS
reference CLI (`~/src/tightbeam`) — the Rust CLI in `cli/` is the
shipped CLI and this spec amends its contract; note the divergence in
cli/ comments, nothing more. Filesystem isolation (same-user reads of
gateway.json and sibling workdir files — containment-v1's job,
recorded in D8). Statute authoring. Device-token changes. Workdir
cleanup at retire. No UI.

## Closed decisions (the shape)

- D1 Delivery is a WORKDIR FILE, not env and not the home. Adapter
  processes and homes are shared per {harness, identity_name, host}
  (identity_name = the archetype, or a session's effective override
  identity), so per-session env is structurally impossible — one
  adapter process serves every session of an identity, and
  `Adapter.new_session` carries no env; homes are disposable shared
  build outputs. The one per-session place that already exists is the
  session workdir (`work/<digest>`), which every harness tool
  inherits as cwd. Both harnesses are covered by construction — the
  file rides the workdir, not the harness. (Override identities can
  make an adapter effectively private; the workdir remains the
  uniform per-session place either way.)
- D2 The file is written at TURN START (inside the existing
  `session_workdir` ensure path), before the prompt reaches the
  harness — so by the time any tool can run, the file exists. This is
  also the healing loop: content is a pure function of (session row,
  current host config); every turn converges the file to expected
  content and 0600 mode.
- D3 The CLI discovers the session file by WALK-UP from cwd and it
  WINS over env. Rationale: the file is the session's own credential;
  env is ambient adapter state (possibly a stale org token on an
  un-restarted satellite). Precedence: `.tightbeam-session` walk-up →
  TIGHTBEAM_URL+TIGHTBEAM_TOKEN env → `<TIGHTBEAM_HOME>/gateway.json`.
- D4 Session-token calls VERIFY identity; org-token calls behave
  byte-identically to today (local-trust, v1 decision, unchanged). A
  session token can never do more than the org token grants the same
  identity — verification only narrows.
- D5 (r1 ruling RETRACTED and replaced) `asUser` on a session token
  is ALLOWED iff the claimed user equals the token session's OWNER —
  a strict tightening of today, where any asUser is accepted
  unverified. This preserves the three shipped workflows the r1 ban
  broke: the builtin attribution bullet ("--as <role> … or --as-user
  <human>"), agent-run `assimilate --as-user <operatorId>`, and the
  admin skill verbs run "--as-user the operator who asked" — all of
  which agents execute from their own workdir shells, where the
  session file wins discovery. The org token's remaining role: the
  discovery fallback for shells with no session file (a terminal
  outside any workdir), `process:` automation (cron/CI pass
  `--as-process`, named-not-authenticated, exactly as today), and
  emergencies. It remains in `gateway.json` (0600).
- D6 Remote adapter env loses `TIGHTBEAM_TOKEN` (org). TIGHTBEAM_URL
  stays. The session file carries its own url, so agent shells need
  no env token; a remote shell outside its workdir gets a clean
  client-side discovery error instead of a silently org-attributed
  call. Local adapter env is unchanged (it never carried the token;
  gateway.json fallback remains). The gateway.json read in
  `Placement.adapter_opts` becomes unused and is deleted with it.
- D7 Identity resolution on session-token calls, complete ladder:
  - `as` present: `Roles.resolve(db, role)` must return
    `{:ok, S.session_key, false}` (bound-active to the token session,
    no fallback) → origin `agent:<role>`. Anything else → 403
    `role_not_held`, message naming the role and S's held roles (or
    "none").
  - `asUser` present: claimed id must equal `S.owner_user_id` →
    origin `user:<owner>` (downstream identical to today's asUser
    path, including admin authority when the owner is admin).
    Otherwise → 403 `identity_not_yours`, message naming the owner.
  - `asProcess` present → 403 `identity_not_yours` (a session is not
    a process).
  - No identity, in order: (1) exactly one bound role → origin
    `agent:<that role>`; (2) zero roles AND the session is a Main
    (the same row predicate the retire handler's permanence check
    uses — the seeded `is_built_in` Mains) → origin `user:<owner>`
    implicitly, because a Main IS its owner's stream; (3) zero roles,
    not a Main → 403 `no_role` ("this session holds no role; its
    owner must bind one, or pass --as-user <owner>"); (4) several
    roles → 400 `ambiguous_identity`, message listing the held roles
    and instructing `--as <role>`.
  - Mains are NOT role-restricted: `Roles.bind` accepts any active
    session, including a built-in Main (roles.ex:104), and no binding
    restriction is authorized here. A role-bound Main derives
    `agent:<role>` per rung (1) — or 400 `ambiguous_identity` with
    several — like any other session; the implicit-owner rung (2)
    applies only at zero roles.
- D8 Risk registry (recorded, with rulings):
  - a) Workdir committed to git: MITIGATED by the `.git/info/exclude`
    heal (§Delivery) — convergent, invisible to the agent, kills the
    weeks-lived-token push risk. Residual (agent force-adds or copies
    the file) accepted.
  - b) An operator who cd's into a session's workdir attributes as
    that session — accepted; operators do not work in `work/<digest>`.
  - c) Local same-user filesystem: an agent on the gateway host can
    read `gateway.json` (org token) and sibling sessions' token files
    (0600 does not isolate one unix user from itself), and deleting
    its own file fails open to the org-token fallback. This lane
    authenticates possession of a bearer, not the OS caller;
    containment owns the walls. The spec's claims are scoped
    accordingly (see Status paragraph).
  - d) Host move source residue: MITIGATED — `move_workdir` deletes
    the SOURCE `.tightbeam-session` after a successful copy, with
    ENSURE-ABSENT semantics on BOTH sides: absent counts as success.
    A pre-first-turn workdir legitimately has no token file yet
    (delivery happens at turn start, D2), so local `File.rm`
    returning `{:error, :enoent}` is success; any OTHER error fails
    the move. Remote stays `ssh … rm -f` (already ensure-absent). A
    real removal failure fails the move (Org.set_host is never
    written, the session stays where its file is valid).
  - e) Retire linearization: revocation takes effect at the
    active-only lookup — the state flip and the lookup going dark are
    the same write. Calls that passed auth before the flip complete.
    Queued ledger turns may still run after retirement (existing lane
    semantics, deliberately unchanged) and will re-deliver the file;
    the credential in it is already dark, so the residue is inert 401
    material. Retire touches no workdirs (unchanged; see Non-goals).
  - f) Role-rebind race: for ORIGIN-STRING flows, router verification
    and downstream `resolve_caller`/statute-fact resolution are two
    reads of the live role binding; a rebind between them
    re-attributes to the new holder. The identical race exists today
    on every org-token `--as` call (the router resolves, handlers
    re-resolve); this lane neither introduces nor widens it, and
    retrofitting existing verbs is ruled OUT of v1. The `principal`
    field does NOT inherit the race — it is computed once from the
    token, no binding involved (§Principal seam).

## Token format & schema

Token: `"tbs_" <> Base.url_encode64(:crypto.strong_rand_bytes(24),
padding: false)` — the org token's generation verbatim with prefix
`tbs_` (org stays `tbc_`; the prefixes are disjoint by construction,
so the auth branch can never confuse the classes).

Schema, in this exact order inside `Org.ensure_schema` (the order is
load-bearing — `@ddl` executes BEFORE the additive-ALTER loop, so an
index in `@ddl` referencing `cliToken` would error on every
pre-existing DB and brick the boot at `:ok = ensure_schema` in
`Gateway.children`):

1. `cliToken TEXT` column in the fresh-DB `@ddl` CREATE TABLE — the
   column only, no index there.
2. The additive-ALTER loop gains
   `ALTER TABLE sessions ADD COLUMN cliToken TEXT` (duplicate-column
   tolerated, existing convention).
3. AFTER the ALTER loop: `CREATE UNIQUE INDEX IF NOT EXISTS
   sessions_cli_token ON sessions(cliToken)` — never in `@ddl`.
4. Backfill (in `Gateway.children`, beside the existing host
   rewrite): select active sessions with `cliToken IS NULL`, mint
   each a fresh token (per-row UPDATE, distinct tokens). Retired rows
   stay NULL. Silent, like the host rewrite.

- Mint UNCONDITIONALLY inside `Org.create_in_txn` (no input
  override). After boot, every active session has a token — delivery
  code may assume non-NULL and fail loudly if reality disagrees (no
  defensive branch).
- `Org.by_cli_token(db, token) :: session | nil` — active-only lookup
  (`WHERE cliToken = ?1 AND state = 'active'`), mirroring
  `Devices.by_token`. Retire needs no token code: `Org.retire` flips
  state and the lookup goes dark in the same write (D8e).
- `Org.get`/row mapping must surface `cli_token` to callers — and it
  must NOT leak outward: `Payloads.stream_session`, `inspect`'s
  `Map.take` whitelist, and session-status stay token-free (test it).

## Gateway resolution (POST /agent/dispatch)

`cli_auth` becomes a two-class branch on the bearer:

1. Bearer == deps.cli_token (org) → the EXISTING path, untouched:
   `agent_origin/2` trusts as/asUser/asProcess exactly as today,
   including its "as (role) or asUser required" 400.
2. Else `Org.by_cli_token(db, bearer)` → session S: derive origin per
   the D7 ladder (add `Roles.for_session(db, session_key) :: [name]`
   if absent, for the held-roles lookup and error messages).
3. Else → 401 `auth_failed` — unknown and revoked/retired tokens are
   deliberately indistinguishable from any bad bearer (no oracle).

Everything downstream (typed_target, verbs, resolve_caller, admin
gating via the origin's owning user, event rows, statutes) is
UNCHANGED — the origin string arrives in the same closed vocabulary
it always had, now verified at the door (race caveat recorded in
D8f). No dependency on the statute engine either way.

## Principal seam (the contract attest-v1 r4 consumes)

The token-resolved principal is carried THROUGH Dispatch, never
collapsed back into the origin string: today the router passes only
origin + target + params, so org-token `--as` and session-token
`--as` are indistinguishable downstream — which is exactly what
breaks holder authorization for attest. This spec owns the
resolution, so it owns the seam.

The dispatch call map (the `call` argument of `Dispatch.dispatch/3`)
gains ONE additive field, `principal` — the caller identity as
PROVEN by the bearer, threaded from the router through Dispatch to
handlers alongside `origin` (which stays the closed
user | agent | process vocabulary, derived per the D7 ladder).
Exactly one of:

- `{:session, session_key}` — the bearer is a session token. ALWAYS,
  regardless of identity flags: the token is the proof, and
  `as`/`asUser`/the Main derivation select the ORIGIN vocabulary,
  never the principal. Race-free: computed once from the token row,
  no role binding involved. (Pinned deliberately: putting the
  Main/verified-asUser cases under `{:user, ...}` would make Mains
  and roleless holders unable to satisfy attest's
  holder-session-only rule — the exact finding this seam exists to
  fix. Owner-ness rides the origin; the principal states what the
  credential proved.)
- `{:user, id}` — the bearer is the org token AND `asUser` is given.
  LOCAL-TRUST, self-declared, UNVERIFIED (the operator-shell path —
  consumers accept it by their own ruling, as attest-v1 does for
  revoke). Only session-token `asUser == owner` is verified; org-token
  `asUser` never is.
- `{:process, name}` — the bearer is the org token AND `asProcess` is
  given: named-not-authenticated, exactly today's trust grade, but the
  claimed class is carried so consumers can refuse processes
  explicitly instead of conflating them with legacy nil.
- `nil` — RESERVED for the org token with `as <role>`: legacy-grade,
  no proven principal. A verb MAY declare it requires a principal
  (attest will; the requirement and its error shape are the declaring
  spec's business) — such verbs refuse principal-less calls with a
  teaching error naming session tokens.

Audit-visible: the verb/denied event row records the principal
alongside origin — additive column `principal TEXT` on the `events`
table (same additive-ALTER convention as §Schema; never in `@ddl`
index positions — it is a bare column, no index), serialized
`"session:<key>"` | `"user:<id>"` | `"process:<name>"` | NULL,
written by Dispatch's existing `EventLog.append_event` call sites.
The serialization carries the KEY, never the token.

Scope, pinned: the principal is constructed ONLY at
`/agent/dispatch`; call maps built elsewhere (device-authed routes,
Wire.Socket) carry no `:principal` key in v1 — absent ≡ nil, and no
principal-requiring consumer is reachable from those surfaces. It is
internal (never a wire field) and ignored by every existing handler
(zero behavior change; `Dispatch.dispatch/3`'s signature is
unchanged — the field rides the call map). First consumer: attest-v1
r4 holder/opener authorization. Note the consequence the ladder
already supports: a roleless non-Main session reaches
principal-gated verbs by passing `--as-user <owner>` (D7 verifies
it, the principal stays `{:session, S}`), so attest's
roleless-holder-attests-freely clause is satisfiable.

## Seam table (normative)

Adopted verbatim from the joint review; attest-v1 r4 cross-references
THIS table as the single seam story. Every row is binding.

| Request | Dispatch principal | Event origin |
|---|---|---|
| Session token, held `as` or one derived role | `{:session, S}` | `agent:<role>` |
| Session token, verified `asUser == owner` | `{:session, S}` | `user:<owner>` |
| Session token, zero-role Main, no flags | `{:session, S}` | `user:<owner>` |
| Org token + `asUser` | `{:user, U}` | `user:<U>` |
| Org token + `asProcess` | `{:process, P}` | `process:<P>` |
| Org token + `as <role>` | nil | `agent:<role>` |

A roleless non-Main session token with no identity flags returns 403
`no_role` during origin derivation. It never reaches Dispatch and
creates no event row. Passing verified `--as-user <owner>` makes the
same holder eligible to attest with origin `user:<owner>` and
principal `{:session, S}`.

No call proceeds with an undefined origin. If neither an agent nor
user origin applies, the only proceeding closed-vocabulary case is
`process:<name>`; otherwise the router refuses the request before
Dispatch.

## Delivery (Placement owns the mechanics)

File: `<workdir>/.tightbeam-session`, mode 0600, content
`JSON.encode!(%{url: url, token: session.cli_token, sessionKey:
session.session_key})` — no trailing newline; camelCase keys per wire
convention. `url` = `"http://127.0.0.1:#{config.port}"` when the
session's host has `ssh: nil`, else
`Application.fetch_env!(:tightbeam, :advertised_url)` (only the
remote branch reads it, as today).

Hook point: `Gateway.session_workdir/2` currently calls
`Placement.ensure_dir(host, path)` (its only caller). Widen it to
`Placement.ensure_workdir(host_config, path, file_content, opts)`
(raise-on-failure posture — an undeliverable workdir fails the turn
visibly; `:sh` injectable as everywhere in Placement, plus `:sh_out`
below):

- Local: `File.mkdir_p!`; rewrite the file (write +
  `File.chmod!(0o600)`) when it is missing, its content differs, OR
  its mode (masked 0o777) is not 0o600. Then the git-exclude heal: if
  `<path>/.git/info` is a directory and `<path>/.git/info/exclude`
  lacks an exact `.tightbeam-session` line, append one (creating the
  file if absent; when appending to an existing file that does not
  end in a newline, write the separating newline first — the line
  must land exact, never concatenated onto a previous line).
  Idempotent; never runs when no `.git` exists.
- Remote: ONE combined ssh (same count as today's mkdir), exactly:

      ssh <@ssh_opts> dest sh -c '<shell_quote of:
        mkdir -p <path> &&
        { find <file> -maxdepth 0 -perm 600 -print 2>/dev/null \
            | grep -q . && cat <file> 2>/dev/null; true; } &&
        if [ -d <path>/.git/info ]; then
          grep -qxF .tightbeam-session <path>/.git/info/exclude \
            2>/dev/null ||
            printf "\n%s\n" .tightbeam-session \
              >> <path>/.git/info/exclude;
        fi>'

  Semantics, pinned: a failed `mkdir` makes the whole command exit
  nonzero → RAISE (matching today's `ensure_dir` posture — never
  masked into a downstream rsync error). Any nonzero ssh exit
  (including transport 255) ALWAYS raises — it is never read as
  mismatch. The `cat` is gated on the permission predicate actually
  MATCHING: `find … -perm 600 -print | grep -q .` succeeds only when
  the file exists AND its mode is exactly 0600 (bare `find … &&`
  exits 0 whenever the path exists, matched or not — that shape is
  wrong and forbidden). So a missing or wrong-mode file emits empty
  stdout → mismatch → re-delivery (`rsync -a` re-asserts 0600,
  healing a correct-content 0644 file's mode as well as content
  drift). The `-perm 600` probe is exact-octal, portable GNU/BSD.
  The git-exclude fragment writes nothing to stdout, so it can never
  poison the comparison; its `printf "\n%s\n"` leading newline means
  the line can never concatenate onto an unterminated final line of
  an exclude file lacking a trailing newline — the possible extra
  blank line is inert (git ignores blank exclude lines) and the
  `grep -qxF` guard makes the append at-most-once thereafter, so the
  heal converges.

  The compare call runs through `:sh_out` — a sibling injectable
  runner with the same `([argv]) -> {stdout, exit}` contract whose
  default is `System.cmd/3` WITHOUT `stderr_to_stdout` (stderr goes
  to the BEAM's stdio, never into the compared output). Required
  because the existing default runner merges stderr
  (`stderr_to_stdout: true`), and ssh banners/warnings — emitted by
  the LOCAL ssh client, unreachable by any remote redirect — would
  poison the equality check and force a spurious rsync every turn.
  `:sh_out` is used ONLY for this compare; every other Placement
  command keeps `:sh`.

  On mismatch: stage the file at
  `<base_dir>/staging/session-files/<workdir-digest>/.tightbeam-session`
  (0600), `rsync -a` it into `dest:<path>/`, with the stage removed
  in a `try/after File.rm_rf!` (the repo's move_workdir precedent) so
  a failed rsync never leaves a 0600 token file under staging/. The
  token must NEVER appear in any argv (ssh command lines land in
  process lists and logs); it travels only via the staged file.

Convergence covers every lifecycle event with zero extra code:
- Boot/restart: token is a column; first turn re-asserts the file.
- Host move (`tune set_host`): `move_workdir` deletes the source file
  on successful copy (D8d); the copied file at the destination may
  carry the wrong url — the first post-move turn rewrites it for the
  new host before any tool runs.
- Harness switch (`tune set_harness`): workdir and token unchanged;
  nothing happens.
- Home regeneration: homes never carry the token; nothing happens.
- Operator wipes the workdir, the file, or its mode: healed at next
  turn start.
- Retire: see D8e — later queued turns may re-deliver an inert file;
  the lookup is already dark.

`Placement.adapter_opts` remote branch: delete the
`TIGHTBEAM_TOKEN=...` entry and the now-unused gateway.json read;
keep TIGHTBEAM_URL, TIGHTBEAM_HOME, the harness token env, and PATH
exactly as they are. Local branch: untouched.

## Guidance (one line, deliberate)

The builtin Operations attribution bullet in `archetypes.ex` ("Every
action is attributed: --as <role> … or --as-user <human>") gains ONE
clarifying clause: on a session token, `--as-user` is verified — a
session may act only as its OWN owner (org-token calls stay
local-trust, unchanged). No other fragment changes; the assimilate and
skill-management fragments' `--as-user` instructions remain correct
under D5/D7 as written. This edit changes the manifest hash and
regenerates each home once; it lands in the same deploy as the
feature (which restarts adapters anyway), so the regeneration rides
the deploy boundary — pre-deploy, effectively free, with the usual
visible context-reset markers.

## CLI (Rust, cli/ — amends cli-rust-v1's discovery contract)

- Discovery: from cwd walk up to filesystem root; first
  `.tightbeam-session` wins — parse JSON, use `url` + `token`, ignore
  unknown keys. Else env (URL+TOKEN both required, as today), else
  `gateway.json` (as today). Malformed session file → hard error
  naming the path (never silently fall through a corrupt credential).
- Identity: the identity-required check moves AFTER discovery (today
  `args.rs` validates identity before discovery runs — this reorder
  is the one structural CLI change). When discovery used a session
  file, identity flags are OPTIONAL — omitted, the body carries none
  of as/asUser/asProcess and the gateway derives per D7. When
  discovery used env or gateway.json, the existing "identity
  required" error is unchanged. The CLI never pre-validates identity
  against the file's sessionKey — thin stays thin; the gateway
  teaches via its refusal.
- Everything else byte-identical (cli-rust-v1 invariant 1 holds for
  all org-token traffic; session-token bodies differ only by the
  possible absence of identity fields, which this spec legalizes).

## Failure modes (closed list)

- Unknown token → 401 `auth_failed`. Retired session's token → 401
  `auth_failed` (indistinguishable, deliberate).
- `--as` a role not bound to the token's session (incl. fallback
  resolution and roles bound to sibling sessions) → 403
  `role_not_held`.
- `--as-user` of anyone but the session's owner → 403
  `identity_not_yours`, naming the owner. `--as-process` on a session
  token → 403 `identity_not_yours`.
- Omitted identity: one role → derived; zero + Main → owner; zero +
  not Main → 403 `no_role`; several → 400 `ambiguous_identity`.
- Missing session file (agent cd'd away, wiped workdir): CLI falls to
  env/gateway.json — on a satellite that means a clean discovery
  error; on the gateway machine it means org-token fallback (D8c).
- Undeliverable file or unmakeable workdir (host unreachable, mkdir
  failure, nonzero ssh exit) → the turn fails visibly (raise), never
  a silent mismatch.

## Invariants (acceptance lens)

1. On session-token calls nothing self-declared is trusted: `as` is
   verified against the live binding, `asUser` against the owner,
   `asProcess` refused, omission derived by the D7 ladder. Every
   session class can act (roles, owners, Mains).
2. The org-token dispatch path is byte-identical to today; device
   auth and every /api route are untouched (their existing tests pass
   unmodified). The `principal` field is additive and ignored by
   every existing handler.
3. Every active session has a token after boot; it survives restarts
   and goes dark at retire in the same state write. Tokens are
   unique. Boot succeeds on fresh AND pre-existing databases (index
   ordering, §Schema).
4. After any turn's start, the session's workdir file equals the pure
   function of (row, current host config) at mode 0600 — moves,
   switches, regens, wipes, and mode drift all converge by the next
   turn, before any tool runs. A `.git`-bearing workdir excludes the
   file from version control via `.git/info/exclude`.
5. The token never appears in argv, ssh command lines, wire frames,
   inspect/stream/status payloads, or event rows (the event row's
   `principal` column carries the session KEY, never the token);
   on-disk copies are 0600; staging never outlives the delivery
   attempt (try/after); a host move leaves no source-side copy.
6. No new verbs, no new origin classes, no statute dependency.
   Exactly one guidance line changes (one home regeneration, riding
   the deploy). The substrate resolves by row lookup and equality —
   it never thinks.

## Tests (condensed contract — cover every clause)

Schema/mint: fresh DB has column + unique index; a pre-existing DB
(old schema, no cliToken) BOOTS — ensure_schema then backfill succeed
(this is the index-ordering test); spawn mints `tbs_` tokens,
distinct; backfill mints for active NULL-token rows only, distinct
per row; retired rows left NULL; `by_cli_token` resolves active, nil
for retired/unknown.
Resolution: org token → existing router tests pass UNMODIFIED (the
guarantee test); session token + held role → origin `agent:<role>`
(assert via event row); + unheld/sibling/fallback-resolving role →
403 role_not_held naming held roles; + asUser == owner → origin
`user:<owner>`, executes — including an admin verb when the owner is
admin (the agent-run assimilate REGISTER path); + asUser != owner →
403 identity_not_yours naming the owner; + asProcess → 403; omitted
identity: one role → derived; zero roles on a Main → `user:<owner>`
(wake-reply from a Main end-to-end); a Main bound to one role →
`agent:<that role>`, not `user:<owner>` (rung 2 applies only at zero
roles); zero roles, not Main → 403 no_role AND no event row is
written; two roles → 400 ambiguous_identity listing both; unknown
token → 401; retired session's token → 401.
Principal: session-token calls carry `{:session, S}` under `--as`,
under `--as-user <owner>`, with identity omitted, and on a Main's
implicit-owner call; org + asUser → `{:user, id}`; org + as-role →
nil; org + asProcess → `{:process, name}`; the verb/denied event row
records the serialized principal (`process:<name>` for org asProcess,
NULL for org as-role) while never containing `tbs_`; a pre-existing
events table gains the column via
the additive ALTER and boots; an existing verb behaves identically
with the field present (spot-check via any handler test).
Delivery (local): first turn writes 0600 file with 127.0.0.1 url,
token, sessionKey; unchanged content+mode not rewritten;
deleted/tampered file healed; correct-content 0644 file rewritten to
0600; file exists before the adapter prompt is sent (order within
harness_session); workdir with `.git` gets exactly one
`.tightbeam-session` exclude line, idempotent across turns —
including an exclude file lacking a trailing newline (the line lands
exact, never concatenated); workdir without `.git` is untouched.
Delivery (remote, injected :sh/:sh_out): converged → exactly one ssh
(the combined command, via :sh_out) and no rsync; mismatch → staged
0600 file, rsync argv targets `dest:<workdir>/`, stage removed; rsync
FAILURE → stage still removed (try/after); nonzero ssh exit → raise,
never treated as mismatch; token absent from EVERY captured argv; the
combined command matches the pinned skeleton (mkdir chain raises,
find-perm-pipe-grep probe gates cat, leading-newline git-exclude
fragment present); `tune set_host` → next turn's expected content
carries the new host's url.
move_workdir: each topology leg deletes the source
`.tightbeam-session` on success; a pre-first-turn source workdir
with NO token file moves successfully on both local and remote legs
(ENOENT ≡ success); a non-ENOENT rm failure fails the move before
Org.set_host.
Env: remote adapter_opts argv contains TIGHTBEAM_URL and no
TIGHTBEAM_TOKEN and no gateway.json read; local adapter_opts
unchanged from today's assertion.
Leak-proofing: inspect result, /api/streams payloads, and
session-status contain no `cliToken`/`tbs_` under a session that has
one.
Guidance: the builtin Operations fragment contains the verified-
asUser clause (accept the manifest-hash/golden churn once).
CLI (cargo): walk-up finds the file from a nested cwd; precedence
file > env > gateway.json; malformed file errors naming the path;
with a file and no identity flags the body omits as/asUser/asProcess;
without a file the identity-required error is unchanged (and still
fires before any network call); Bearer comes from the file.
CLI-integration harness (AUTHORIZED AND DEFINED HERE — no such
harness exists at 0015883; the repo has only inline Rust unit tests
and Plug.Test router tests. attest-v1 r4 references THIS harness
rather than defining its own): `test/cli_integration_test.exs`,
tagged `@moduletag :cli_integration` and excluded by default
(`ExUnit.configure(exclude: [:cli_integration])` in test_helper.exs).
It serves the real `Wire.Router` — same deps construction the router
tests use — under Bandit on an ephemeral port (`port: 0`; read the
bound port from the listener), locates the built binary at
`cli/target/release/tightbeam` (hard error if missing when the tag is
selected — never a silent skip), and drives that binary via
`System.cmd` with cwd set inside a prepared session workdir,
asserting wire behavior. Gate: `mix test --only cli_integration`
runs after `cargo build --release` (§Build ordering).
E2E (via that harness): spawn a role-bound session, write its file,
drive `tightbeam list` and `wake`
through the real router with the session token; drive one call
`--as-user <owner>`; retire it and assert the same call 401s.

## Rollout (ordered — the order is the spec)

1. FIRST, per registered remote host with a matching target triple
   (mismatched hosts are excluded — ruling below): push the
   session-file-aware CLI binary via the existing assimilate CLI-push
   step (`Spinup` does not deploy the CLI; assimilate's CLI step is
   the only delivery path). The old gateway is still running, so the
   new CLI on the satellite discovers via the still-present env
   URL+TOKEN and keeps working with old attribution.
2. THEN restart the gateway on the new build: schema migration +
   backfill run, remote adapters respawn without the env token, and
   each session's first post-restart turn delivers its file before
   the prompt runs.

Heterogeneous satellites (this spec's RULING): assimilate's CLI step
copies the currently running executable only when the satellite's
probed target triple matches the local one; otherwise it warns and
SKIPS the CLI (ceremonies.rs:377). Cross-compilation is out of scope.
A mismatched-triple host keeps its existing CLI and is EXCLUDED from
the session-token rollout until an operator builds a matching binary
on a matching machine and re-runs assimilate (the existing warning
already teaches this). Stated honestly: after step 2 such a host's
old CLI has lost its env token and has no session-file support, so
CLI calls there fail with the clean discovery error until the
matching binary lands — sessions on the host are otherwise unaffected
(turns, wire, and file delivery all work), and the delivered file
becomes live the moment a new CLI arrives, with no further gateway
action. Boot warning: in `Gateway.children`, beside the existing
backfill, probe each configured remote host with `uname -sm` (the
Spinup ssh posture: BatchMode, ConnectTimeout 5), map it through the
same probe→triple table the CLI uses, and compare to the gateway
host's own platform; on mismatch append
`EventLog.lifecycle(db, "cli_target_mismatch", host_name, detail)` —
the lifecycle kind set is open, so no schema change. Best-effort: an
unreachable host or failed probe emits no row and never fails or
blocks boot beyond the probe timeout; the authoritative check remains
assimilate's own probe-and-skip.

Honest window, stated: between step 1 and each session's first
post-restart turn, calls attribute the old way (self-declared, org
token). Bound: the operator's push-to-restart gap plus one turn per
session. After that, the only holdouts are processes a pre-restart
turn left detached outside the adapter tree — they keep the old env
(org token, still valid) until they exit; custody of those is
containment's problem, recorded here, not this lane's. Reversing the
step order bricks satellite CLIs (no env token, no session-file
support, no gateway.json on a satellite) — do not.

No data migration beyond the additive column + backfill; nothing to
roll back except the deploy itself.

## Build ordering & handoff

Cut the worktree from main AFTER the cli-rust branch is merged — it
merged at `0015883`, so the precondition is currently satisfied;
still verify `cli/` exists in your cut and STOP if it does not (do
not patch the TS CLI instead). No statute-engine dependency.
attest-v1 cuts AFTER this lane merges (its spec says so; nothing here
depends on attest). Gates: `mix compile --warnings-as-errors` clean;
full `mix test` green; `cargo build --release`, `cargo test`,
`cargo clippy -- -D warnings` clean in `cli/`; then
`mix test --only cli_integration` green against the built binary
(§Tests harness). Commit on the branch; do not merge. STOP and report on any conflict with existing code or
this spec.
