# Roles registry v1 — implementation spec

Roles: durable names for offices, with mutable session bindings, total
fallback resolution, and typed reference grammar. This document is
decision-complete: every core semantic is fixed here; implementers decide
only internal naming and test organization. Two INDEPENDENT lanes:

- **Lane E (Elixir substrate)**: repo `~/src/tightbeam_ex`.
- **Lane C (reference CLI, TypeScript)**: repo `~/src/tightbeam`, files
  `src/cli/main.ts` + `src/cli/main.test.ts` ONLY. Lane C depends only on
  the verb contract in §6 — not on Lane E's code.

Gates (end conditions) are per-lane in §10. Follow each repo's existing
comment discipline and voice. Do not commit in either lane. If anything
here conflicts with the tree: STOP and report; never improvise.

## 1. Invariants (normative — implementation is checked against these)

1. NO VOID: a valid role reference always resolves to exactly one live
   session — the bound session if it is active, else the role OWNER's
   Main. Worst case is "the operator sees it," never "nobody does."
2. DERIVATION, NEVER JUDGMENT: resolution computes role → binding → key
   from recorded facts. The substrate never chooses a binding.
3. TYPED REFERENCES, NO UNIONS: a target field admits exactly three
   syntactic forms, each its own type — (a) session keys, recognized by
   prefix `agent:`; (b) `user:<id>`, always a user reference resolving to
   that user's Main by derivation; (c) any other word, always a role
   name. No field is ever Role|User; no uniqueness constraint across
   namespaces; a role named `mike` and a user `mike` coexist and the
   engine never confuses them.
4. LATE-BIND THE FUTURE, PIN THE PAST: standing references (scheduled
   wakes, config, guidance) hold role NAMES and resolve at each use.
   History (turn rows) records BOTH the role reference and the concrete
   resolution it produced at that moment, plus whether fallback fired.
5. NAMES OUTLIVE INCARNATIONS: rebinding, retiring, or death of a bound
   session never invalidates a role name — only explicit `role-rm` does,
   after which the name errors by name (never silently reroutes).
6. MUTATION ONLY BY VERB: role-create / role-bind / role-rm through the
   dispatch chokepoint, attributed, fail-closed validation.
7. ACTING-AS REQUIRES HOLDING THE OFFICE: `--as <role>` is valid only
   while that role is bound to an active session; the origin is
   `agent:<role>`.
8. ONE MECHANISM: handle RESOLUTION is removed everywhere (the sessions
   table's handle column survives as a vestigial spawn-time record only).
   Existing handles migrate into roles once at boot. `spawn --name X` now
   means "create role X bound to the new session."

## 2. Lane E — data layer (`lib/tightbeam/roles.ex`, NEW file)

Table (own `ensure_schema`, called from `Gateway.children/1` with the
other schemas):

```sql
CREATE TABLE IF NOT EXISTS roles (
  name            TEXT PRIMARY KEY,
  boundSessionKey TEXT,
  ownerUserId     TEXT NOT NULL,
  createdAt       INTEGER NOT NULL,
  updatedAt       INTEGER NOT NULL
);
```

Public API (all `db \\ Tightbeam.DB` first arg, matching Org's style):

- `create!(db, name, owner_user_id, bound_session_key_or_nil)` →
  role map `%{name, bound_session_key, owner_user_id}` |
  `{:error, %{code, message}}` with codes: `"role_exists"`,
  `"invalid_role_name"`, `"unknown_session"` (binding given but no such
  active session).
- `bind(db, name, session_key)` → `:ok` | `{:error, %{code, message}}`
  (`"unknown_role"`, `"unknown_session"` — binding target must EXIST and
  be state `active`).
- `rm(db, name)` → `:ok` | `{:error, %{code: "unknown_role", ...}}`.
- `get(db, name)` → role map | nil.
- `list(db)` → [role maps] sorted by name.
- `resolve(db, name)` → `{:ok, session_key, fallback? :: boolean}` |
  `{:error, %{code: "unknown_role", message}}`. Resolution rule
  (invariant 1): binding present AND that session exists with state
  `"active"` → `{:ok, bound, false}`; otherwise (nil binding, missing or
  non-active session) → `{:ok, Org.personal_session_key(owner), true}`.

Name lexicon: `^[a-z0-9][a-z0-9-]*(:[a-z0-9][a-z0-9-]*)*$` AND must not
begin with `agent:` or `user:` (reserved by the typed grammar — refuse
with `invalid_role_name` naming the reservation).

## 3. Lane E — typed target resolution (single chokepoint)

Replace the target-resolution logic in `Wire.Router.target_session/2`
(and any twin in gateway — there must be exactly ONE implementation; if
two exist, unify to one shared function first):

1. `""` → `{:ok, nil}` (unchanged).
2. Target begins with `"agent:"` → session-key type: `Org.get` hit →
   that key; miss → 404 `unknown target` (NEVER falls through).
3. Target begins with `"user:"` → user type: user exists (Devices) →
   `Org.personal_session_key(id)`; else 404.
4. Anything else → role type: `Roles.resolve/2`; `unknown_role` → 404
   with the role name in the message.

The bare-user-id branch shipped in ops-hardening v1 is REMOVED (bare
words are role-typed now; `user:<id>` remains the user spelling). Remove
`Org.get_by_handle` from resolution (see §7 for its other call sites).
Resolution must RETURN the reference metadata to callers that record
history: `{:ok, session_key, %{role: name | nil, fallback: boolean}}` —
shape the single function so both router and gateway receive it.

## 4. Lane E — late binding for wakes; history records both

- `wakes` table gains additive column `targetRole TEXT` (use the
  established duplicate-column rescue pattern from `org.ex`).
- Scheduling: when the wake verb's target was role-typed, store the ROLE
  name in `targetRole` and ALSO the resolution-at-schedule-time in the
  existing sessionKey column (so `inspect` shows something meaningful
  now). When key- or user-typed, `targetRole` is NULL and behavior is
  unchanged.
- FIRING: if `targetRole` is set, re-resolve the role AT FIRE TIME and
  deliver to that result (invariant 4) — the stored sessionKey is a
  display hint, not the delivery address. If the role was deleted between
  schedule and fire: do NOT deliver; record a lifecycle event
  `EventLog.lifecycle(db, "wake_unresolved", wake_id, "role <name> no longer exists")`
  and mark the wake fired (visible failure, no crash, no retry).
- `turns` table gains additive columns `roleRef TEXT` and
  `roleFallback INTEGER NOT NULL DEFAULT 0`. `Gateway.deliver_prompt`
  accepts `role_ref:`/`role_fallback:` opts and writes them into the turn
  row in the same transaction. The wake fire path and the immediate-wake
  path both pass them whenever the target was role-typed.

## 5. Lane E — acting-as and spawn sugar

- `agent_origin` / caller resolution: `as: <word>` is now role-typed —
  valid iff the role exists AND `resolve` returns `fallback: false`
  (i.e., the office is actually held); the origin string is
  `agent:<roleName>` and the caller session is the bound session. An
  unbound/fallback role → the existing unknown-caller/denied error,
  message naming the unbound role. `Org.get_by_handle` is no longer
  consulted here.
- `spawn` with `--name X` (params `handle`/`name` — keep the existing
  param key): after the session row is created, `Roles.create!` with the
  new session as binding, owner = the spawned session's owner.
  `role_exists` → the spawn FAILS with that error (transactionally: do
  not leave the session created — same all-or-nothing the handle
  uniqueness check has today). The sessions.handle column is still
  written (vestigial record).
- Migration at `Gateway.children/1` (after schemas): for every session
  with a non-null handle and no role of that name yet, create the role
  bound to that session (owner = session owner). Idempotent; runs before
  Bandit accepts connections.

## 6. Verb contract (both lanes; Lane C codes against THIS table)

All via POST /agent/dispatch, existing auth/attribution. New verbs added
to the router's `@agent_verbs`:

| verb | params | result | errors |
|---|---|---|---|
| role-create | name (req), bind (opt sessionKey), idempotency-free | `{role: {name, boundSessionKey, ownerUserId}}` | role_exists, invalid_role_name, unknown_session |
| role-bind | name (req), sessionKey (req) | `{role: {...updated}}` | unknown_role, unknown_session, denied (non-owner non-admin) |
| role-rm | name (req) | `{removed: name}` | unknown_role, denied |
| role-list | — | `{roles: [{name, boundSessionKey, ownerUserId, fallbackTarget}]}` where fallbackTarget = owner's Main key | — |

Authorization: `role-create` owner = caller's owning user (process
origins DENIED for all three mutations — processes may only TARGET
roles). `role-bind`/`role-rm`: role owner or admin. Binding target must
be owned by the role owner unless caller is admin.

## 7. Lane E — removals and touch-ups

- Every `Org.get_by_handle` call site outside spawn's uniqueness check is
  replaced by role resolution or deleted; spawn's handle-uniqueness check
  is REPLACED by the role_exists check in §5. If `get_by_handle` ends up
  unused, delete it and its tests.
- Builtin guidance (`@builtin_operations` and `@builtin_comms` in
  archetypes.ex): update the addressing language — targets are session
  keys (`agent:...`), `user:<id>` (a human's Main), or a role name; roles
  are rebindable offices with fallback to their owner's Main; `--as
  <role>` requires the role be bound to you. Keep edits to those
  sentences; pinned guidance tests updated to match (this is an identity
  change; homes regenerate — expected, note in commit message not code).
- `inspect` result: sessions gain nothing; add top-level `roles:` =
  role-list's payload, so agents discover offices in one call.

## 8. Lane C — reference CLI

In `src/cli/main.ts` + tests ONLY:

- New commands (dispatch passthrough, mirroring existing style):
  `role create <name> [--bind <sessionKey>]`, `role bind <name>
  <sessionKey>`, `role rm <name>`, `role list` → verbs per §6.
- HELP: update the TARGET section to the typed grammar (keys start with
  `agent:`; `user:<id>` reaches that human's Main; any other word is a
  ROLE — a rebindable office that falls back to its owner's Main). Update
  `--as` text (act as a role you currently hold). Update `spawn --name`
  text (registers a role bound to the new session). Add `role` to the
  unknown-command list string.
- Tests: one per new command asserting the dispatched verb+params (same
  pattern as existing wake/spawn tests); help renders the word "role".

## 9. Out of scope (STOP conditions — build none of this)

No election/auto-staffing logic. No role permissions beyond §6. No rooms.
No changes to rails, skills, homes, placement, adapters, or the wire
socket protocol. No handle-column schema removal. No client (Swift) work.
If a needed change falls outside the file sets below, STOP and report.

## 10. End conditions

Lane E: `mix compile --warnings-as-errors` clean; `mix test` fully green
including NEW tests covering — every §2 API branch and error code; the
§3 typed-grammar matrix (key hit/miss, user hit/miss, role
bound/fallback/unknown, bare word is NEVER user-resolved); late-binding
(schedule wake to role → rebind → fire → delivered to NEW binding; turn
row carries roleRef + resolved key + roleFallback); role deleted before
fire → wake_unresolved lifecycle row, no delivery; §5 act-as (bound ok,
unbound denied) and spawn sugar (role created; role_exists fails spawn
atomically); §5 migration (pre-existing handles become roles, idempotent
re-run); §6 authorization matrix incl. process-origin denials; §7
guidance pins updated. Files: `lib/tightbeam/roles.ex` (new),
`lib/tightbeam/gateway.ex`, `lib/tightbeam/wire/router.ex`,
`lib/tightbeam/wakes.ex`, `lib/tightbeam/ledger.ex`,
`lib/tightbeam/org.ex` (only if a shared helper lives there),
`lib/tightbeam/archetypes.ex`, plus test files for each. Do not commit.

Lane C: `npx tsc --noEmit` clean; `npx vitest run src/cli/main.test.ts`
fully green. Files: `src/cli/main.ts`, `src/cli/main.test.ts`. Do not
commit.

## Addendum A (supersedes §3's target grammar): strictly typed target fields

RULING (Flynn): reference seams are STRICTLY TYPED — a parameter is a
userId, a role, or a sessionKey, never a union, and the type is carried
STRUCTURALLY (by field name), never inferred from string shape. The §3
"typed grammar" (prefix classification of one `target` string) is a
tagged-union-by-convention and is REMOVED. The model to follow is the
existing attribution seam (`as` / `asUser` / `asProcess`).

### Lane E changes

- `/agent/dispatch` body: the `target` field is GONE. Verbs that address
  a session take EXACTLY ONE of three fields:
  - `sessionKey` — a session key, resolved by exact `Org.get`; miss → 404
    `unknown sessionKey: <v>`.
  - `role` — a role name, resolved by `Roles.resolve` (binding else
    owner-Main fallback, metadata recorded as already built); unknown →
    404 `unknown role: <v>`.
  - `userId` — a user id, resolved by derivation to their Main; unknown
    user → 404 `unknown userId: <v>`.
  Zero of the three when the verb needs one → 400 naming all three
  fields. Two or more → 400 `exactly one of sessionKey, role, userId`.
  A request still sending `target` → 400 `"target" is retired: use
  sessionKey | role | userId` (fail closed, teaches the seam).
- Applies to `wake` (all three) and `retire` (`sessionKey` ONLY — retire
  addresses an incarnation, never an office or a person; `role`/`userId`
  on retire → 400 `retire takes sessionKey only`). `cancel-wake`
  (wakeId), `tune`/`cancel`/`inspect`/session-status (already
  sessionKey-shaped) are unchanged. Remove the string-classification
  function entirely; no code path may branch on a target string's shape.
- Role NAME lexicon: the `agent:`/`user:` prefix reservations in §2 are
  now unnecessary (nothing classifies strings) — but KEEP them: names
  that look like other types' spellings are still human-hostile. Note the
  reason changed in the validator comment.
- Guidance (`@builtin_operations`/`@builtin_comms`): rewrite addressing
  language to the typed flags (see Lane C) and reply spelling:
  `[from user:mike]` → `wake --user mike`; `[from agent:notetaker]` →
  `wake --role notetaker`; `[from process:x]` → cannot be woken. Pinned
  guidance tests updated.
- Update every existing test that used `target` to the typed fields; add
  the exactly-one-of validation matrix (zero/two/retired-`target`) and
  the retire-is-sessionKey-only cases.

### Lane C changes (src/cli/main.ts + test only)

- `wake` loses its positional target: `tightbeam wake --session <key> |
  --role <name> | --user <id> --prompt ...` (exactly one; CLI validates
  before dispatch and errors with the three options named). `retire
  --session <key>` likewise (positional removed). Params sent as
  `sessionKey`/`role`/`userId` per the wire contract above.
- HELP: TARGET section replaced by the three flags with one-line
  meanings (session = this exact incarnation; role = the office, falls
  back to its owner's Main if unstaffed; user = that human's Main).
  Update wake/retire examples and the reply-spelling text under --as.
- Tests updated/added: one per flag per verb; exactly-one-of CLI error.

### End conditions

Same gates as §10 per lane. SMOKE §10 steps 24 and 28 will be updated by
the maintainer (not the lanes).
