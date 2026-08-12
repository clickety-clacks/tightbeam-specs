# Statute engine v1 — verb rules as data (implementation spec, r6)

r6 after four adversarial review rounds (codex xhigh, 2026-07-19).
Supersedes r1–r5 entirely.

ORIGIN GRAMMAR (referenced throughout): an origin is WELL-FORMED iff it
is exactly `user:<rest>`, `agent:<rest>`, or `process:<rest>` with
non-empty `<rest>`. Anything else — no colon, unknown prefix, empty
rest — is MALFORMED. Malformed origins → ALL caller.* facts nil
(including caller.verb_count_24h; no exact-string counting for them),
and nil-never-fires (invariant 6) applies.

Operator-authored rules over the org's VERBS, evaluated at the dispatch
chokepoint. The statute half of the constitution/statute line (bible
§rails): rules where sane operators could differ become data; the
constitution stays code, untouched and untouchable from here. Repo: a
fresh worktree cut from main. Gates: warnings-clean compile, full suite
green. Do not commit. STOP and report on conflict.

## Invariants (the acceptance lens)

1. DENY-ONLY, ORDER-SAFE: rules evaluate inside `Dispatch.dispatch/3` —
   the single chokepoint all transports converge on — BEFORE guards and
   the verb handler. Because rules can only deny, this ordering cannot
   grant: a call that passes the rules still runs every existing
   hardcoded check inside the handler, unchanged. A rule may PRE-EMPT a
   constitutional denial (the caller sees the rule's message instead),
   never reverse one — the final outcome class (denied, no mutation) is
   identical. A monotonicity test proves this with a rule that MATCHES a
   constitutionally-denied call (e.g. process-origin spawn): denied with
   rules present, denied with rules absent, zero DOMAIN mutation either
   way (audit rows excluded, per invariant 7).
2. TOTAL AND DUMB: conditions are comparisons over a CLOSED fact
   vocabulary. Implicit AND within a rule; OR exists only as multiple
   rules; NO boolean tree syntax (negative comparators ne/not_in are
   fine and are not "NOT"). No arithmetic, regex, nesting, or
   user-defined anything.
3. FAIL CLOSED AT LOAD: every malformed input stops the boot with an
   error naming the FILE, plus the rule NAME (or table ordinal when the
   name is missing/invalid) for rule-level failures; file-level failures
   (unparseable/empty TOML, no [[rule]] tables, unknown root keys) are
   attributed to the file alone. The full list is in §Validation.
4. FAIL CLOSED AT RUNTIME, TOTALLY: fact computation is wrapped to
   catch ALL of raise/:exit/:throw (public DB reads can EXIT when a
   GenServer is unavailable — rescue alone is not total). Any escape →
   the call is DENIED with code `"rule_error"`, message naming the rule
   and fact. Recording that denial is best-effort: if the audit sink
   itself is unavailable, the call is STILL denied (denial never depends
   on the row landing). Worst case over-restricts; never fails open.
4b. EVERY FACT IS A BEST-EFFORT SNAPSHOT: all facts are point-in-time
   reads computed once per call (WHEN computed is pinned — the
   demand-driven order in §Evaluation; this clause is about the reads'
   NON-ATOMICITY, not their order), with no synchronization against
   concurrent mutation (rebinding, promotion, retirement mid-flight may
   yield mixed facts). Deny-only makes this safe in the direction that
   matters: a race may under-enforce a STATUTE (a stale fact misses a
   rule that fresh facts would fire) or spuriously deny (a stale fact
   fires a rule), but can never bypass the CONSTITUTION — any call the
   rules tier lets through still runs every hardcoded handler check on
   live state. Statute enforcement is snapshot-grade by design;
   constitutional enforcement stays exact. This is a documented
   property of the tier, stated in the moduledoc.
5. REFUSE BY NAME: rule denials return code `"rule_denied"`, message
   `<rule-name>: <text>`. Transport status mapping follows each
   transport's EXISTING denial conventions (agent dispatch → 400,
   control responses → 200-with-error) — no new transport behavior.
6. NIL NEVER FIRES: the evaluator checks fact PRESENCE first; a nil
   fact makes the condition FALSE for EVERY operator, explicitly
   including ne and not_in. An empty LIST is a present fact, not a
   missing one — `caller.roles not_in ["admin"]` FIRES for a caller
   holding no roles; the spec's fact table and the moduledoc must both
   carry this worked example as a warning to rule authors.
7. DENIALS ARE ROWS (BEST-EFFORT): rule denials and rule_errors are appended
   through the EXISTING event mechanism — EventLog kind `"denied"` (the
   schema CHECK permits only verb|denied; do NOT invent kinds), with
   the code/rule name in the recorded payload, exactly one row per
   denied call across all three transports WHEN the audit sink is
   available; if recording fails, the call is still denied and the
   missing row is an accepted, documented property (invariant 4's
   carve-out wins — denial never depends on the row landing).
8. ZERO RULES = TODAY: no rules dir, empty dir, or a load of zero rules
   (which must CLEAR any previously persisted set) → identical results,
   identical mutations, identical event rows, handlers invoked exactly
   as today. (Observable equivalence — no prescriptions about internals.)
9. TESTS-CALL-DISPATCH-DIRECTLY SAFETY: `Rules.evaluate` reads its set
   via persistent_term WITH a default of [] — Dispatch used without a
   prior `Rules.load!` (as existing tests do) behaves as zero-rules.

## Rule files

`<base_dir>/identity/rules/*.toml`, loaded in filename order by NEW
module `Tightbeam.Rules`; `load!/2` called from `Gateway.children/1`
(any point after schemas; no ordering relationship with Rails is
promised). Signature: `load!(base_dir, valid_verbs)` where valid_verbs
is the KEY SET OF THE GATEWAY HANDLER MAP — the public dispatch
authority — passed by Gateway at build time (do not reach for the
router's private @agent_verbs).

```toml
[[rule]]
name = "agent-spawn-quota"   # ^[a-z0-9][a-z0-9-]*$ ; unique across all files
verb = "spawn"               # must be in valid_verbs
deny_when = [                # non-empty list of condition tables; ALL must hold
  { fact = "caller.origin_class", op = "eq", value = "agent" },
  { fact = "caller.verb_count_24h", op = "gte", value = 3 },
]
text = "agents may spawn at most 3 sessions per day"  # non-empty after trim; multiline legal
```

## Fact vocabulary (closed; declared types; computed per call)

Facts are computed BY THE RULES MODULE from the raw dispatch call
(origin string, session_key, verb), using public APIs (Org, Roles,
Devices). This intentionally duplicates lookups the handler will repeat
— rules are the rare path and correctness beats sharing; do NOT attempt
to thread resolved context through Dispatch (r1's error: no such
context exists there). Compute lazily and DEMAND-DRIVEN (the exact
order is pinned in §Evaluation): a fact is computed only at the moment
a condition actually evaluates it; computed values are cached per call.
Facts named only by non-matching verbs, by rules after the deciding
rule, or by conditions after a false condition in their own rule are
never computed — so a failing fact can produce `rule_error` only when
evaluation genuinely reached it.

| fact | type | definition & nil cases |
|---|---|---|
| caller.origin_class | string | "user" \| "agent" \| "process" from the origin prefix; malformed origin → all caller.* facts nil |
| caller.user | string | user:<id> → id; agent:<role> → the bound session's owner (nil if role unknown/unbound); process → nil |
| caller.is_admin | bool | admin flag of caller.user's user ROW; nil when caller.user is nil OR no user row exists |
| caller.roles | list(string) | roles whose CURRENT BINDING equals the caller's session, by direct binding lookup (never Roles.resolve — fallback must not contribute). For WELL-FORMED origins: a present list — [] for user/process origins and for an agent:<role> whose role is unknown/unbound/bound-to-retired (remember `not_in` FIRES on a present []). MALFORMED origin (see §Origin grammar) → nil, like every caller.* fact; nil-never-fires applies. |
| target.owner | string | Org.get(call.session_key).owner — nil when the call carries no session_key OR no row exists (idempotent-retire ghost keys, unknown targets: all target.* nil) |
| target.archetype | string | same source; nil as above |
| target.host | string | same; nil as above |
| target.kind | string | "main" \| "dm" \| "custom" (the full schema set); nil as above |
| target.state | string | "active" \| "retired"; nil as above |
| org.live_sessions_owned_by_caller | int | count of state=active sessions owned by caller.user; nil when caller.user nil |
| caller.verb_count_24h | int | WELL-FORMED origins only (malformed → nil like all caller.*): count of EventLog kind="verb" rows with this exact origin string AND this verb, `ts > now − 86_400_000` (strict). kind="verb" means ATTEMPTS THAT REACHED A HANDLER: handler failures and successful idempotency replays each count (they append verb rows today); rule/guard denials do not (kind="denied"). "Attempts count" is the contract — do not build success-discrimination machinery. Via a NEW public `EventLog.verb_count(db, origin, verb, since_ms)` (this spec authorizes that one addition). |

(No `verb` fact — every rule already names its verb; redundant.)

## Operators & typing (validated at load against declared fact types)

- eq, ne: string/bool/int facts; value must match the fact's type.
- gt, gte, lt, lte: int facts only; value must be a TOML integer
  (floats rejected at load, including 3.0).
- in, not_in — two shapes by fact type:
  - scalar fact: value is a flat list of that scalar type (non-empty,
    no nesting, no mixed types — validated).
  - list fact (caller.roles only): `in` = intersection non-empty;
    `not_in` = intersection empty. eq/ne/ordered ops on list facts →
    load error. The VALUE side is validated exactly like the scalar
    case: a non-empty flat list of strings — `roles in []` and
    `roles in [1]` are both LOAD ERRORS (non-empty and string-typed
    apply to every in/not_in value, scalar or list fact).

## Evaluation

Signature: `Rules.evaluate(db, call)` — the SAME db Dispatch.dispatch/3
received (tests pass test-local dbs; every fact lookup and the denial
row must thread it; nothing may reach for the global name). Inside
`Dispatch.dispatch/3`, before guard/handler invocation: select rules for
this verb (zero → proceed); evaluate rules in filename-then-table
order; within a rule, conditions in table order, short-circuiting on
the first FALSE condition (that rule is skipped; its remaining facts
are not computed); first rule whose conditions ALL hold denies —
evaluation stops, later rules' facts are never computed. Facts are
computed only when a condition demands them, cached per call across
rules. Consequently `rule_error` (invariant 4) occurs iff a DEMANDED
fact escapes — a fact that would fail but is never demanded (later
rule, or after a false condition) causes nothing. Denial surfaces
exactly like existing guard denials (same return shape the transports
already map) and appends the kind="denied" event row.

## Validation (boot errors: file-level failures name the FILE; rule-level failures name file + rule/ordinal)

Malformed/empty TOML file; file without [[rule]] tables; unknown keys
at root, rule, or condition level; missing/blank name, verb, text;
whitespace-only text; name failing the lexicon; duplicate names (same
or different files); verb not in valid_verbs; deny_when missing, empty,
or containing non-tables; condition missing fact/op/value; unknown
fact; unknown op; op/type mismatch per the matrix; float where int
required; nested or mixed-type lists; list value for scalar-only ops;
eq on a list fact.

## Tests (condensed contract — cover every clause)

Every §Validation row. Evaluator: each operator's positive/negative/
boundary; nil with EVERY operator (ne and not_in pinned); empty-list
present-fact behavior (the roles warning example); AND with one false
term; first-match ordering across files and tables; non-matching verbs
compute zero facts (probe via a fact that would raise). Integration:
the §1 monotonicity test (matching rule over a constitutional denial);
denial + exactly one "denied" row + handler-not-invoked + zero DOMAIN
mutation (the denied-event audit row itself excluded, per invariant 7)
proven on ALL THREE transports (WS post, REST, /agent/dispatch);
laziness: a would-raise fact after a false condition in its own rule,
and one named only by a later rule than the deciding one, each cause
nothing; quota
end-to-end from seeded verb events incl. 24h boundary edge and
denied-rows-don't-count; caller matrix (user/agent/process/malformed;
admin true/false/nil; multi-role; unbound role); target matrix (active/
retired/missing/ghost-key/dm/main); zero-rules observable equivalence;
empty load clears a previously loaded set; Dispatch-without-load!
behaves as zero-rules.

## Out of scope (STOP conditions)

No allow/grant rules, no boolean condition trees, no rule verbs (files
only; restart to apply), no per-archetype scoping, no atomic quota
reservation, no Rails unification, no changes to constitutional guards
or transport status mappings, no CLI changes.
