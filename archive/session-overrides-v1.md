# Per-session identity overrides v1 — implementation spec

Spawn-time identity tweaks: "an X, but with these extra skills and this
extra guidance," producing a content-hash custom home so unmodified
sessions keep sharing the archetype's canonical home (bible §Agent
identity: "identity-affecting overrides produce an effective manifest
whose content hash keys a generated-on-demand home"). Repo: a fresh
worktree cut from main. Gates: warnings-clean compile, full suite green.
Do not commit. STOP and report on conflict.

## Invariants (the acceptance lens)

1. TEMPLATES STAY SHARED: a spawn with NO overrides behaves byte-
   identically to today — same home path, same adapter key, same manifest
   hash. Zero-override cost is zero.
2. EFFECTIVE IDENTITY IS DERIVED, STORED, AND STABLE: the session row
   records its overrides (data); the effective identity = archetype +
   overrides is recomputed deterministically from those facts whenever
   needed (guidance recompiles identically → same hash → same home).
   Archetype edits still flow through: the hash covers the COMPOSED
   result, so an archetype guidance change regenerates custom homes
   exactly like canonical ones.
3. OVERRIDES ARE ADDITIVE-ONLY in v1: skills may be ADDED (election
   union), guidance may be APPENDED. No removals, no replacing fragments,
   no defaults/where/mcp overrides — reject unknown override keys fail-
   closed at spawn with a named error (never silently ignore).
4. ISOLATION BY HASH: two sessions with identical overrides share one
   custom home and one adapter; different overrides never share. The
   custom home participates in every existing home behavior (hash-gated
   regeneration, auth symlinks, skills symlinks, rails settings, model
   pin) with NO special cases downstream — achieved by construction, not
   by copying code paths.
5. LAW STILL APPLIES: added skills must exist in the library (spawn
   denied naming unknown skills — same error style as archetype election
   validation); appended guidance passes through #include resolution with
   the same cycle/missing failure behavior, at SPAWN time (bad law fails
   the spawn, not the boot — the manifest was fine; the override wasn't).
6. NO REAPING IN V1 — DELIBERATE: custom homes accumulate; reaping is
   deferred until disk pressure is real (record this in the moduledoc as
   a decision, not a TODO).

## Wire/verb surface

`spawn` params gain optional `overrides`:

```json
{"overrides": {"skills_add": ["swift"], "guidance_extra": "## Assignment\nOwn the payments repo."}}
```

Both keys optional; empty/absent object = no overrides (invariant 1's
path). Unknown keys inside overrides → denial `invalid_overrides` naming
them. `skills_add` entries validated against the library (tree roots
only, like election). `guidance_extra` is a string, trimmed; empty after
trim = absent.

## Mechanics

- Org: sessions table gains additive column `overrides TEXT` (JSON;
  duplicate-column rescue pattern). Session type carries parsed map or
  nil.
- Archetypes: `effective(archetype, overrides)` → an archetype struct
  with skills = union (sorted, deduped) and guidance = archetype guidance
  <> "\n\n" <> resolved extra (through the same fragment resolver).
  Pure; no persistent_term writes.
- Identity key: today's adapter/home key is {harness, archetype, host}.
  Overridden sessions use identity name `"<archetype>#<hash12>"` where
  hash12 = first 12 hex of sha256 over the effective composed guidance
  + sorted skill list (the same inputs the manifest hash covers). This
  identity name flows everywhere the archetype name flows today
  (adapter key, home path homes/<identity>/<harness>, staging, stderr
  log name) — find the seams where archetype-name-as-identity is read
  (AdapterCoordinator keys, Placement.adapter_opts/deliver_home,
  Gateway.harness_session/checkout) and thread the session's identity
  name instead of session.archetype. The UNMODIFIED path must produce
  the bare archetype name (invariant 1).
- deliver_home resolves the effective archetype from the session's
  overrides (not just Archetypes.get) when composing guidance/skills/
  settings for that identity. MCP config: from the base archetype
  unchanged (no override in v1).
- spawn: validate overrides BEFORE Org.create (atomic with the existing
  all-or-nothing shape); store the JSON on the row.

## Tests

Zero-override byte-identity (home path, adapter key, manifest hash all
unchanged — pin against current values); union/dedup of skills;
guidance append with #include resolution incl. failure at spawn; unknown
override key denial; unknown skill denial; two same-override spawns
share identity name, different overrides differ; overridden home
contains the appended guidance and the added skill symlink while the
canonical archetype home is untouched; archetype guidance edit changes
BOTH canonical and custom hashes; stderr log and staging paths use the
identity name without collision (a `#` in paths must be exercised — if
`#` breaks any consumer (ssh quoting, file paths), use `--` as the
separator instead and note why).

## Out of scope (STOP conditions)

No removals/replacement overrides, no defaults/where/mcp/rails
overrides, no reaping, no tune-time override editing (spawn-only), no
CLI flag work beyond passing the params map through if trivial —
otherwise leave CLI to a follow-up lane.

## DISPOSITION (2026-07-19, post-review): NOT-READY — held for design

Adversarial review (codex xhigh) returned 18 findings; several are
architectural, and three need operator decisions before a v2 is worth
writing. DO NOT IMPLEMENT from this document.

Blockers requiring redesign (maintainer):
- Effective identity must be RECONSTRUCTIBLE from durable data at any
  moment (deliver_home and coordinator crash-restart hold only the key
  today) → likely a persisted identities record (hash → base+overrides),
  which also fixes hash-encoding, collision, and namespace findings.
- Credential continuity: a base-guidance edit changes a custom home's
  PATH, so the abandoned home is never harvest-backed — a rotated
  file credential stranded there would brick the login (the rotation
  war through a new door). Needs a harvest design that spans homes.
- Split base-archetype reads (MCP, fallback_models, placement, model
  pin) from identity reads (guidance, skills, home, adapter key) as an
  explicit dual-accessor contract; seam list corrected (cancel,
  set_model reload).

Operator decisions needed (Flynn):
1. Does a skill added by a live session's override count as an election
   that BLOCKS `skill rm` (like archetype elections do), or may the
   operator rip it out from under running sessions (visible failure)?
2. Are stored overrides revalidated at boot (a removed fragment/skill
   fails the boot — law posture) or lazily at next adapter start
   (visible degradation instead)?
3. Is a persisted identities registry acceptable given the topology
   ruling? (It records the org's OWN composition acts — like sessions
   and roles — not machine capability; maintainer believes it fits, but
   it is a new durable table and deserves the explicit call.)
