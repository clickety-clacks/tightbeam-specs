# Router existence oracle — typed targets and who may learn what exists — v1

Status: DRAFT r1 (Fable-authored 2026-07-26). One ruling required (R1 below);
everything else follows from the audit.

## Defect

`typed_target` (wire/router.ex:515-564) runs for EVERY `/agent/dispatch` call
(router.ex:116) and resolves the volunteered reference BEFORE any handler or
handler-level authorization: `sessionKey` → `Org.get`, 404 `"unknown sessionKey:
<key>"` (router.ex:538-548); `userId` → `Devices.user`, 404 (router.ex:550-553);
`role` → `Roles.resolve`, 404 (router.ex:555-562). Because the seam runs for all
~50 agent verbs (router.ex:48) while only a handful consume a target, any
authenticated caller — any session's cliToken or the org token
(router.ex:366-378) — can attach a `sessionKey` field to a verb that ignores
targets entirely and read existence out of the status code. Verbs whose own
authorization is narrower than "authenticated org agent" would leak through the
same seam if they routed their key through it, because known-but-forbidden
(handler answer) and unknown (router 404) differ — the leak transcript-verb-v1
closed for itself.

## Audit

### Who can ask

`cli_auth` admits the org token and every session cliToken (router.ex:366-378).
The oracle audience is every live agent in the org.

### What each typed kind reveals, and the live authorization baseline

| kind | early answer | what it reveals | live authority found |
|---|---|---|---|
| `sessionKey` | 404 by name vs proceed (router.ex:538-548) | existence of a specific session | Point-addressing is org-visible BY DESIGN: `wake` delivers to ANY session with only a caller-known check, no target-ownership check (gateway.ex:2509-2510, wake_result); spawned keys are unguessable (`"agent:" <> uuid4`, gateway.ex:3673) so probing needs a key you were handed; personal keys are deterministic (`Org.personal_session_key/1`, org.ex:613) so this kind also answers USER existence. Enumeration, by contrast, is owner-scoped everywhere: `inspect` lists only the caller-owner's sessions (gateway.ex:2239-2241), clients list via `Org.list_for_user` (router.ex:136). |
| `userId` | 404 by name vs personal-key resolution (router.ex:550-553) | existence of a user | wake-to-user is the DM/escalation surface; user existence is org-visible through it and through deterministic personal keys. |
| `role` | 404 by name vs resolution (router.ex:555-562) | existence of a role | `role-list` has NO authorization at all (gateway.ex:668) — role existence is org-visible by construction; the 404 reveals nothing `role-list` doesn't. |

Not typed-target kinds, checked for completeness: `workItemId`/`assignmentId`
travel in params and their handlers own both answers (`work-item-get` is
readable by any session/user principal with no ownership check,
work_items.ex:565-575; `work-item-trace` is owner-or-admin with identical
not_found, work_items.ex:577-618); `deviceId` never routes through this seam
(device endpoints are separately device-authed, router.ex:380-391).

### Which verbs consume the typed target

Handlers reading `call.session_key` as a TARGET: `post` (gateway.ex:502),
`wake` (gateway.ex:2319+), `cancel` (gateway.ex:1478), `tune`
(gateway.ex:2658-2838), `retire` (gateway.ex:3143+), `critical`
(gateway.ex:3056), `assign`/`dispatch`/`assignments`
(assignments.ex:534,689,718,779). `artifact-record` uses the CALLER's session
only (router.ex:566-569). Every other agent verb ignores the target — for those,
the early resolution is a pure oracle serving no caller.

### Where the early 404 is load-bearing

For the consumers it is caller UX the tests pin as "teaching errors": assign/
dispatch require a target and reject `userId` and retired holders with named
bodies (router.ex:525-544); a typo'd key on a mutation must fail loudly by name.
test/router_test.exs pins exact bodies: `"unknown role: mike"` (:720),
`"unknown sessionKey"` (:754), the byte-exact unknown-role body (:794), and the
"typed-target teaching errors precede Dispatch and status classes are pinned"
test that follows. The CLI attaches `sessionKey` ONLY on target-taking commands
(cli/src/dispatch.rs:81,172,186,233,402). No conformance fixture stores these
bodies (repo-wide grep: only router_test.exs and the emitting sites).

### Known-but-forbidden today, inside consumers

`retire` answers `%{code: "not_found"}` for a cross-owner key (owner pattern
match, fallthrough gateway.ex:3151-3207) — distinguishable from the router's
named 404, which is consistent with org-visible existence and owner-scoped
mutation. `tune` (rename/set_harness) and `cancel` show NO target-ownership
check at all (gateway.ex:2658-2661, 1478-1493): any agent appears able to
rename any session or cancel its running turn. That is a MUTATION authorization
gap, out of this spec's scope, reported as its own finding.

## R1 — the one ruling this spec needs

**Point-addressed existence of sessions, users, and roles is org-visible to any
authenticated agent; enumeration stays owner-scoped.** The audit says this is
the built and intended baseline (wake's unscoped delivery, role-list, the
deterministic personal keys, inspect's own comment "Discovery beats
documentation … not a secret from its members", gateway.ex:2243-2245).

- **Confirm** → the rules below apply; the early 404 stays for consumers.
- **Reject (owner-scoped existence)** → the fix is not router surgery: wake,
  assign, dispatch, and role fallback all legitimately reveal cross-owner
  existence, so agent addressing itself would need redesign. That is a
  different, much larger spec; nothing below should be built first.

Everything below assumes CONFIRM.

## Normative rules

1. **Closed target-consumer table.** The router carries an explicit
   verb→accepted-target-kinds table containing exactly the consumers audited
   above (plus `retire`'s sessionKey-only and assign/dispatch's
   session-or-role restrictions, which it already special-cases,
   router.ex:525-533). `typed_target` resolves ONLY for verbs in the table.
2. **No free oracle.** A typed target field (`sessionKey`, `userId`, `role`) on
   a verb not in the table is refused `400 invalid_message "<verb> takes no
   target"` BEFORE any resolution — unknown and existing references get the
   byte-identical refusal.
3. **Teaching errors unchanged.** For table verbs, current early-404 bodies and
   status classes are preserved byte-for-byte (the pinned router_test bodies
   are the contract).
4. **Narrow verbs never route through the seam.** A verb whose own
   authorization is narrower than "authenticated org agent" (today:
   `transcript` per transcript-verb-v1; `work-item-trace` already conforms)
   MUST carry its selector in body params and answer unknown and
   known-but-forbidden byte-identically from its handler. Such verbs MUST NOT
   appear in the consumer table with the sensitive kind.
5. **No timing claims.** Resolution-before-vs-after timing differences are not
   specced and not proven; no test may claim to measure them.

Mechanism recommendation, per the audit: this is fix shape (a) generalized — a
router allowlist plus the params rule — NOT (b) deferral of existence
resolution until after handler authorization. (b) would break the load-bearing
teaching errors, force every consumer handler to re-own existence answers, and
under R1-confirm protects nothing.

## Necessity gate — exactly what changes on the wire

For every principal: a request pairing a non-table verb with any typed target
field changes from "resolved then ignored" (404 for unknown, silently accepted
otherwise) to `400 invalid_message` regardless of existence. No legitimate
caller sends that shape today (CLI audit above); no fixture captures it.
Nothing else changes: table verbs keep current answers, handlers keep current
answers. Conformance fixtures to re-capture: NONE. Tests extended, not
re-captured: test/router_test.exs (the pinned status-class test gains the
refusal rows).

## Required proofs

1. **Table closure, fail-before/pass-after.** A source test derives the set of
   handlers reading `call.session_key` as a target and asserts it equals the
   pinned table; a new consumer outside the table fails the test; a table verb
   losing its consumption fails it the other way.
2. **Oracle dead.** For a non-table verb: unknown key, existing cross-owner
   key, and existing own key each get the byte-identical 400 body. Fails
   before the change (unknown gets 404, existing proceeds).
3. **Teaching errors byte-stable.** For `wake`/`assign`/`dispatch`/`retire`:
   the unknown-sessionKey/-userId/-role bodies equal the currently pinned
   bodies exactly.
4. **Narrow-verb exclusion.** The table contains no entry for `transcript`
   (and any verb the elided-read set of transcript-verb-v1 grows to include);
   handler-level byte-identity for those verbs is proven in their own specs
   and referenced, not duplicated.
5. **CLI unaffected.** Every CLI command that emits a typed target maps to a
   table verb (asserted against cli/src/dispatch.rs's emission sites).

## Component touches

`wire/router.ex` (`typed_target` gains the verb table and refusal branch;
`@agent_verbs` untouched), test/router_test.exs additions, the source-closure
test file. NO handler changes, NO schema, NO CLI changes. Adjacent finding
filed separately: tune/cancel target-ownership gap (gateway.ex:2658-2661,
1478-1493).
