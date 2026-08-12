# Identity composition v2 — projection manifests, skill-rm transform, session overrides

Supersedes session-overrides-v1.md (whose DISPOSITION recorded the review
blockers) — every blocker and Flynn ruling from 2026-07-19 is resolved
here. THREE PARTS, implemented IN ORDER in one lane; run the full gate
(`mix compile --warnings-as-errors` clean, `mix test` green) after EVERY
part. Repo: worktree `~/src/tightbeam_ex-idv2` (branch `identity-v2`).
Do not commit. STOP and report on any conflict.

Governing rulings (bible §Agent identity, updated today):
- Manifests tell you what's in them; output never doubles as input.
- Skill removal is a transform, never a veto; affected sessions are told.
- An override is a personal want recorded on the session's row; library
  removal is not revocation (content pinned for the session); stopping
  the want is an explicit act with notification.
- Missing override dependencies: honor what exists, log the discrepancy;
  never brick a session, never block a boot.

## PART 1 — projection manifests become real (homes.ex + archetypes.ex)

The home's `.tightbeam-manifest` stops being an opaque hash and becomes a
readable JSON document; the regeneration gate hashes ITS bytes.

Manifest content (JSON, keys sorted, no timestamps — the bytes must be a
PURE function of the spec or every projection would regenerate):
```json
{
  "base_archetype": "coder",
  "parent_manifest": {"file": "identity/archetypes/coder.toml", "sha256": "<hex of the FILE bytes at load>"},
  "harness": "claude",
  "guidance_sha256": "<hex of composed guidance bytes>",
  "skills": [{"name": "swift", "provenance": "template", "linkage": "linked"}],
  "extra_files": {"settings.json": "<sha256 of content>"}
}
```
- `parent_manifest` for the builtin default (no file): `{"file": null,
  "sha256": null}`. Archetypes.load! must retain, per archetype, its
  source path + file-bytes sha256 (persist alongside in persistent_term;
  add to the archetype map as `source: %{file, sha256} | nil`).
- Homes.project: compose the manifest struct from the spec, encode with
  sorted keys, compare BYTES to the stored file; differ/absent → wipe
  (with harvest-back) + rebuild + write manifest. `manifest_hash/1` is
  subsumed — the manifest bytes ARE the identity fingerprint.
- Spec plumbing: `Homes.project`'s spec gains the fields the manifest
  needs (base_archetype, parent source, skill provenance/linkage —
  Placement supplies them; today all skills are provenance "template",
  linkage "linked").
- DEPLOY CONSEQUENCE (document in commit, not code): every home's stamp
  format changes → one-time global regeneration + context-reset markers.
- 1b — CREDENTIAL SWEEP (closes the abandoned-home harvest hole for both
  this and Part 3's path churn): generalize harvest — (a) keep the
  pre-wipe harvest of the target home; (b) add `Homes.sweep_auth/2`
  (base_dir, harness) that scans EVERY `homes/*/<harness>/` for
  regular-file credential entries and copies any whose mtime is newer
  than the store copy back to the store; called at `Gateway.children/1`
  once per harness at boot. A stranded rotated credential in an
  abandoned home path is recovered at the next boot, before any adapter
  needs it.

Tests: byte-purity (same spec twice → identical bytes, stamp untouched,
nested marker file survives); changed guidance/skills/extra → regenerate;
parent hash recorded and changes when the archetype FILE changes;
builtin-default null parent; sweep recovers a newer regular-file cred
from an abandoned home dir; sweep prefers newest mtime; old-format stamp
(opaque hash) → treated as differ → one regeneration.

## PART 2 — skill removal becomes a transform (archetypes.ex + gateway.ex)

- `Archetypes.rm_skill(base_dir, name)`: DELETE the elected-root refusal.
  New return: `{:ok, %{archetype_electors: [names], manifest_warnings:
  [...]}}` — electors = archetypes whose CURRENT election names the
  removed root (still fails on unknown_role→unknown skill as today for
  missing skills).
- Gateway `skill-rm` handler, after removal + existing replica push:
  1. For every ACTIVE session whose archetype elects the removed root
     (and, after Part 3, every session whose override elects it — see
     Part 3 for the pinning that happens FIRST for those), deliver a
     notification wake via the existing `deliver_prompt` path: origin
     `"process:tightbeam"`, prompt exactly:
     `The skill "<name>" has been removed from this org's library. Disregard it, including anything from it already in your context.`
  2. Response gains `notified: [sessionKeys]` and `manifest_warnings:
     ["archetype <a> still elects <name> in <file> — edit it before the
     next restart (boot validation is fail-closed)"]`.
- Boot-time election validation is UNCHANGED (fail-closed for archetype
  manifests): the warning above is how the operator is kept ahead of it.

Tests: rm with electors proceeds; wakes enqueued to each active electing
session with the exact prompt+origin; retired sessions not woken;
response carries electors + warnings; boot with a manifest electing the
removed skill still fails (unchanged law).

## PART 3 — session overrides

### Data & normalization
- `sessions` gains additive columns `overrides TEXT` and
  `identityName TEXT` (duplicate-column rescue pattern; identityName is
  a stored derivation — cache of a pure function, never edited by hand).
- Spawn param `overrides`: object with optional `skills_add`
  (list of library ROOT names) and `guidance_extra` (string). Validation
  order: BEFORE Spinup.ensure_ready and before any side effect
  (review finding: Spinup mutates remote state). Errors, all code
  `invalid_overrides`, message naming the offense: non-object; unknown
  keys; skills_add not a list of strings; unknown skill names (library
  roots only); guidance_extra not a string; guidance_extra whose
  #include resolution fails AT SPAWN (missing fragment/cycle — spawn
  fails, boot never involved).
- Normalize: dedupe+sort skills_add, drop entries already elected by the
  archetype; trim guidance_extra. Semantically empty result → store NULL
  and identityName = the bare archetype name. Store the NORMALIZED JSON.

### Effective identity & naming
- `Archetypes.effective(archetype, overrides_map_or_nil)` → archetype
  struct: skills = union sorted; guidance composition: the COMPOSED
  output = `Archetypes.guidance(base)` (base name in the header — never
  the hashed name, avoiding circularity) `<> "\n\n" <>` the resolved
  guidance_extra, resolved with a LENIENT resolver used only here: a
  missing include or missing skill at COMPOSE time (post-spawn drift)
  composes without the missing piece and records
  `EventLog.lifecycle(db, "override_discrepancy", identityName, detail)`
  — honor what exists, log the gap. (At SPAWN time strict validation
  already refused.)
- identityName for overridden sessions: `"<archetype>--<hex16>"` where
  hex16 = first 16 of sha256 over the projection-manifest bytes of the
  effective identity (Part 1 gives us canonical bytes; full digest is
  recorded IN that manifest as its own fingerprint so a hex16 collision
  is DETECTED at composition — full-digest mismatch with same name →
  raise, refuse to compose over a different identity; astronomically
  rare, loudly fatal, never silent). Separator is `--`; archetype name
  validation gains: names may not contain `--` (boot error; small law
  addition, include it).
- Dual-accessor contract (explicit; the r1 error was "thread
  everywhere"): IDENTITY reads (home path, adapter key, staging, stderr
  log, guidance/skills composition) use identityName. BASE reads (MCP
  config, fallback_models, placement `where`, model pin, org displays)
  use the row's archetype column. The complete identity-read seam list
  to convert: Gateway checkout (harness_session), Gateway cancel path's
  key construction, Gateway set_model immediate-reload key,
  Placement.adapter_opts, Placement.deliver_home. Everything else stays
  base. (Reviewer-verified list; if you find another key construction
  site, STOP and report.)
- Reconstruction at adapter (re)start: the coordinator's adapter_opts
  closure receives only the key. Placement resolves the effective
  identity: name without `--` → Archetypes.get as today; with `--` →
  `Org` lookup of any session (active preferred) with that identityName
  → effective(base, overrides). No session found → raise (adapter start
  fails visibly; nobody living there needs it).
- Homes spec for overridden identities: skills carry provenance
  "override" for added ones; linkage "linked" normally.

### Override skills survive library removal (pin-at-rm)
- Part 2's skill-rm, for sessions whose OVERRIDE elects the removed
  root: BEFORE deletion, materialize the skill directory to
  `<base_dir>/identity/pinned/<identityName>/<skill>/`; the affected
  identity's home projection now links that pinned path (linkage
  "pinned" in the manifest; lenient composition prefers pinned when the
  library root is gone). Remote: pinned dirs ride deliver_home's
  existing skills catch-up rsync (extend the loop to pinned sources).
  These sessions are notified with a DIFFERENT prompt:
  `The skill "<name>" was removed from the library, but your session elected it at spawn, so your copy is preserved. Use "tune" override removal if you no longer want it.`
- Explicit removal op: `tune` gains setting `remove_override`:
  params `skill: <name>` (drops one pinned/added skill) or
  `guidance: true` (drops guidance_extra). Recomputes normalization +
  identityName (identity change: home regenerates, context-reset marker
  — expected, document); deletes an orphaned pinned dir; notifies the
  session: `Your override "<x>" was removed by the operator; disregard it.`
  Owner-or-admin authorization, same style as other tune settings.

### Tests (Part 3)
Zero-override byte-identity: absent, {}, empty list, dup-only,
whitespace guidance → NULL stored, bare identityName, canonical home
path/key/stamp byte-identical to a no-overrides world. Validation matrix
(each error, and NO Spinup call/side effects on failure — assert via
the injectable sh capturing zero commands). Effective composition: base
header retained; union; lenient-resolver discrepancy row on post-spawn
drift. Naming: same normalized overrides (any input order/dupes) →
same identityName; different → different; `--` rejected in archetype
names; full-digest collision guard raises. Dual accessor: MCP servers
and model pin from BASE on an overridden session; home/adapter/stderr/
staging paths use identityName (exercise the literal `--` through the
remote command quoting). Reconstruction: kill the adapter, restart via
coordinator, SAME home bytes recomposed from the session row; all
sessions retired → adapter start fails visibly. Pin-at-rm: content
preserved+linked, manifest says pinned, notification prompts exact (both
variants); tune remove_override: row normalized, home regenerated,
pinned dir cleaned, notification sent, authorization enforced. Turn,
cancel, and set_model paths all use the overridden key (extend the
existing golden/coordinator stubs minimally). Credential sweep (Part 1b)
recovers a rotated cred from a home abandoned by identityName churn.

## Out of scope (STOP conditions)
No reaping. No non-additive overrides (removals/replacement of template
content). No mcp/defaults/where/rails overrides. No CLI flags (params
pass through /agent/dispatch as JSON already; /api/streams picker is NOT
extended — spawn-with-overrides is dispatch/CLI-JSON only in v2; note
that in the router if a stray overrides key arrives there: ignore is
FORBIDDEN — refuse with invalid_overrides naming the unsupported
transport). No statute-engine interaction. No changes to rails, roles,
wire payloads.

## FIX ROUND 1 (post adversarial review — six findings, all to fix)

Design corrections (maintainer errors in the original spec, now ruled):
- IDENTITY FINGERPRINT ≠ STAMP BYTES. identityName's hex16 derives from
  sha256 over HARNESS-INDEPENDENT effective content only: the composed
  effective guidance bytes <> 0-byte <> sorted effective skill names
  joined with 0-bytes. NOT the projection-manifest bytes. Rationale:
  harness is already its own component of the adapter key, and linkage
  (linked→pinned) is a materialization detail — neither changes WHO the
  identity is. The projection manifest (which legitimately includes
  harness, linkage, settings) remains the per-home REGENERATION gate
  only. Consequence: identityName is stable across tune set_harness and
  across pin-at-rm; the home still regenerates in both cases via the
  stamp.

Findings to fix (file:line refs from the review, branch identity-v2):
1. BLOCKING placement.ex:444 — reconstruction picks ORDER BY LIMIT 1 and
   bypasses collision detection. Fix: load ALL sessions with the
   identityName; compute each row's fingerprint; >1 distinct effective
   content → raise (collision guard applies on THIS path); else use the
   single effective. Add a test through the reconstruction path.
2. BLOCKING gateway.ex:315 — pin-at-rm notifies before the pinned
   content is reachable. Fix order: pin content → REPROJECT affected
   local homes (deliver the linkage change) and push the pinned dirs to
   remote replicas via the existing push machinery → delete the library
   root (local+remote) → notify. The wake must never claim preservation
   the projected path can't serve. Test: after skill-rm returns, the
   affected home's skill path resolves to pinned content WITHOUT any
   manual deliver_home call.
3. placement.ex:766 — resolved by the fingerprint redefinition above;
   add a test: pin-at-rm leaves identityName unchanged while the stamp
   changes (home regenerated, same path).
4. gateway.ex:1446 — resolved by the same redefinition; test: tune
   set_harness on an overridden session keeps identityName, home
   regenerates for the new harness under the same identity path.
5. homes.ex:161 — sweep must enumerate each home dir's REGULAR files
   (credential-shaped: every file present in the home dir that is not a
   symlink and not the manifest/instruction file... precisely: for each
   file in the HOME dir that is a regular file and whose name exists in
   the auth store OR matches the harness's known credential filenames
   (.credentials.json, oauth-token, auth.json), copy back when newer
   than the store copy OR when the store copy is absent; create the
   store dir if missing. Store-listing enumeration is the bug.
6. archetypes.ex:853 — rm_skill of a nonexistent skill must return the
   unknown-skill error again (no silent success, no notifications).

Gates unchanged; run the FULL suite after fixes. Do not commit.

## FIX ROUND 2 (re-review: 5/6 resolved; one partial + two regressions)
1. PARTIAL (finding 1): reconstruction collision check queries state='active' only — must check ALL rows carrying the identityName (retired included; a retired row's differing recipe still proves a collision).
2. REGRESSION: pin dirs are created BEFORE reprojection and their mere existence forces pinned linkage — if reprojection fails, deletion aborts but later deliveries use the snapshot despite the library being live. Order/guard so pinned linkage only takes effect once the transform commits (e.g. mark-complete file or pin under a staging name until success).
3. REGRESSION: set_harness persists the new engine BEFORE fallible eager delivery — a delivery failure leaves the row switched with no history clear/response. Deliver first (or make persistence contingent); on failure leave org state unchanged and surface the error.
Gates as always; do not commit.
