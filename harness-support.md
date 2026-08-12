# Harness support matrix

Parity-law status: **ACTIVE**. The READY r3 migration gate closed on
2026-07-25 with CAP-001..CAP-017, named negative-tested divergences, the
reconciled shipped skill, and registry-driven feature smoke.

Canonical record of which tightbeam features work on which harness, and by
what mechanism. Discipline (Flynn directive, 2026-07-18): per-harness
support is FACTS TO KNOW, never facts to rediscover — every feature that
diverges by harness gets a row here when it ships, and the shipped
`tightbeam-harnesses` skill mirrors this table so agents consult instead
of guessing. A feature not listed diverges nowhere.

Legend: PARITY = complete through Tightbeam · DIVERGENCE = named vendor or
runtime difference with a negative test · GAP = vendor capability exists but
Tightbeam does not project it, with a negative test. The capability census is
CLOSED as of the READY r3 parity amendment (2026-07-25): every capability has a
stable ID, every {capability × registered production harness} cell has a status
and proof reference, and unverified capability claims are forbidden.

FRAMING RULE (2026-07-20, after a reality audit found codex
systematically undersold — see below): describe EACH harness's own
mechanism; never write "codex has no X" for a capability codex provides
by a different mechanism. Neither harness is "the reference." A vendor
✖ means the VENDOR lacks it; a tightbeam-side gap is ◐ᵗ. As of this
audit codex has ZERO true vendor-✖ rows.

| ID | Capability | claude status + proof | codex status + proof | Mechanism / notes |
|---|---|---|---|---|
| CAP-001 | Sessions, turns, cancel, load | PARITY — `test/acp_adapter_test.exs` new/load/close/cancel contract; `docs/SMOKE.md` steps 3,5,8 | PARITY — same proof | ACP `session/new·load·prompt·cancel·close`; load sends `mcpServers: []`. |
| CAP-002 | Model selection + effort | DIVERGENCE `DIV-MODEL-CLAUDE-ENVIRONMENT` — negative `test/acp_adapter_test.exs` “model-selection divergence…” | PARITY — positive control in the same test | Claude's offered set is cwd/settings-dependent and can refuse `Invalid value for config option model`; a refused reassert preserves loaded continuity. Codex applies model + reasoning effort. |
| CAP-003 | Slash-command passthrough | PARITY — `docs/SMOKE.md` §6 steps 11–13 | PARITY — same proof | Prompt text passes through unchanged. Claude `/clear /compact /model`; codex-acp `/status /mcp /skills /review /review-branch /review-commit /compact /logout /new /clear` plus configured skills. |
| CAP-004 | Projected identity | PARITY — `test/acp_adapter_test.exs` guidance metadata test; `test/placement_test.exs` identity assertions | PARITY — same proof | Same composed guidance; Claude system-prompt `_meta`, Codex developer-instruction `_meta`. |
| CAP-005 | Skills — native discovery | PARITY — `test/identity_test.exs` reserved materialization; `docs/SMOKE.md` skills step | PARITY — same proof | Native progressive disclosure under `.claude/skills` / `.codex/skills`; Tightbeam owns only `tightbeam__*`. |
| CAP-006 | Vendor-native skills/commands | PARITY — vendor surface preserved by `test/identity_test.exs` unreserved-entry preservation | PARITY — same proof | Projection is additive and never removes vendor-native entries. |
| CAP-007 | Rails — gate statutes | PARITY — `test/rails_test.exs`; `docs/SMOKE.md` steps 17–23 | PARITY — `test/acp_adapter_test.exs` gate wiring-check; `test/rails_test.exs` | Same deny law; Claude `settings.json`, Codex `hooks.json` plus the fail-closed boot probe. |
| CAP-008 | Rails — future block/check tiers | DIVERGENCE `DIV-RAILS-FUTURE-RESERVED` — `test/rails_test.exs` rejects non-gate modes | DIVERGENCE `DIV-RAILS-FUTURE-RESERVED` — same negative proof | Reserved, not claimed. Codex 0.144.x PreToolUse is deny-only; substrate checks remain harness-neutral. |
| CAP-009 | Credentials — file lifecycle | PARITY — `test/credentials_test.exs`; `test/homes_test.exs` harvest preservation | PARITY — same proof | Provider stores project the harness credential entry; stopped-runtime harvest protects rotations. |
| CAP-010 | Credentials — token environment | PARITY — `test/placement_test.exs` Claude token-env injection | PARITY — `test/credentials_test.exs` Codex device/access-token lifecycle | Both have noninteractive token mechanisms; subscription-longevity policy is not claimed as a capability. |
| CAP-011 | Onboarding login flow | PARITY — `test/credentials_test.exs` setup-token lifecycle; CLI ceremony tests | PARITY — `test/credentials_test.exs` device-auth lifecycle; CLI ceremony tests | `tightbeam onboard <provider>` gates, stops, installs, marks, starts, and resumes on the target host. |
| CAP-012 | Typing-indicator progress | PARITY — `test/acp_adapter_test.exs` streamed progress/chunk tests; `docs/SMOKE.md` step 4 | PARITY — same proof | Rich ACP updates are mapped to the shared progress channel. |
| CAP-013 | Context-usage telemetry | PARITY — `docs/SMOKE.md` per-harness progress/usage observation | PARITY — same proof | Both adapters emit per-turn usage; this row claims emission, not compaction projection. |
| CAP-014 | Compaction visibility | DIVERGENCE `DIV-COMPACTION-CLAUDE-ABSENT` — negative `test/acp_adapter_test.exs` “structured compaction…” | GAP `DIV-COMPACTION-CODEX-UNPROJECTED` — same negative test | Claude adapter drops structured `compact_boundary`; Codex adapter emits `contextCompaction`, but Tightbeam currently does not project it end-to-end. Codex's former unknown status is resolved as a named Tightbeam gap. |
| CAP-015 | Hash-gated home regeneration | PARITY — `test/homes_test.exs`; shared conformance `reconcile_home` oracle | PARITY — same proof | Ownership-scoped regeneration preserves non-owned bytes. |
| CAP-016 | Harness switch on a session | PARITY — `test/gateway_test.exs` set_harness barrier tests | PARITY — same proof | `tune set_harness` uses history barrier + tombstone; context never crosses engines. |
| CAP-017 | Auth-event classification | DIVERGENCE `DIV-AUTH-CLAUDE-UNKNOWN` — negative `test/acp_adapter_test.exs` auth divergence test | PARITY — terminal/transient positive controls in the same test and shared conformance vectors | Claude has no classified auth envelope and always returns `:unknown`; Codex classifies logged-out terminal and logged-in/transient account updates. |
Maintenance rules (parity formality):
1. Any change that introduces `if harness == …` in the substrate, the CLI,
   or the ceremonies MUST add or amend a row here and in the
   `tightbeam-harnesses` skill in the same change.
2. Every status cell MUST carry a proof reference. The former
   `(unverified)` allowance is revoked: missing proof blocks the row and the
   harness bundle instead of shipping as a claim.
3. A known difference is legal only as a stable `DIV-*` row with a negative
   test. Silence and question-mark capability cells are forbidden.
4. The empirical error-shape catalog below is not a capability census: its
   opportunistic `?` cells mean “envelope not yet observed” and make no
   support claim.

## Harness error-shape catalog (harness error classification, GAP-1)

> **AMENDED 2026-08-12:** the model-adjudication engine this catalog fed was
> deleted 2026-08-05 (`model-ringdown-pattern.md` is dead as mechanism). The
> catalog itself SURVIVES with new standing: it serves the ruling's NAMED
> FAILURE duty — a turn that cannot run fails with a precise, classified
> reason — and **GAP-1 (harness error classification) is re-homed HERE** from
> `model-ringdown-pattern.md`. The classify-seam collection route described
> below is gone with the engine; wild-failure capture needs a new carrier. See `adjudication-deletion-amendment.md`.

The empirical error envelopes each harness emits, keyed to the classified
condition the model-adjudication engine (`model-ringdown-pattern.md`) routes on.
This catalog is INHERENTLY OPPORTUNISTIC (Flynn/team-lead ruling 2026-07-22):
quota-exhaustion and post-exhaustion recovery shapes cannot be induced on
demand, and deliberately breaking a live harness's auth to sample its auth-fail
shape is FORBIDDEN (the org runs on it). So the catalog builds two ways: (a) the
adjudication classify seam records every UNCLASSIFIED runtime error's raw
envelope (`unclassified_harness_error` lifecycle marker), turning every wild
production failure into a contribution automatically; (b) the two SAFE probes
(model-refusal per harness). Rows are provenance-marked; `?` = not yet captured,
never guessed. The classification-mapping lane consumes this table.

| condition | claude envelope | codex envelope | surfacing / provenance |
|---|---|---|---|
| `auth_failed` | ? (opportunistic only — NO auth-breaking probe) | `turn_error` whose output = `"Your access token could not be refreshed because your refresh token was revoked. Please log out and sign in again."` | codex: surfaces at the adapter as `detail=turn_error` (seen at the boot gate wiring-check as `gate wiring-check FAIL detail=turn_error output=…`). LIVE INCIDENT 2026-07-21, `adapter-codex:reviewer@eezo.stderr.log`. First empirical entry. |
| `model_unavailable` | `"Invalid value for config option model: <ref>"` (config-option refusal; see the Model-selection row — environment-dependent offered set) | ? (SAFE model-refusal probe pending) | claude: known symptom from the Model-selection row; codex: to be captured by applying a catalog-invalid model to a scratch session (safe probe). |
| `boot_failed` | ? | ? | residual — a boot fault that is neither auth nor model refusal; because boot is lazy it can surface after a successful spawn. Opportunistic. |
| `quota_exhausted` | ? | ? | NOT inducible on demand — opportunistic capture via the `unclassified_harness_error` seam. |
| recovery (`quota-recovered`) | ? | ? | NOT inducible — opportunistic; the gauge/hysteresis for filing `quota-recovered` is the fast-follow producer's concern. |

Discipline: this catalog is FACTS TO KNOW (the framing rule above). An `other`
classification in the live engine that recurs is a signal to add its row here,
mapped, and promote it out of `other` — that promotion is the classification
lane's per-shape work, backed by the recorded envelope, never by a guess.
