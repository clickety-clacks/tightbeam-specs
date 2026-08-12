# Adjudication deletion — corpus amendment (2026-08-12)

Status: RECORD. This file is the single home of the spec-corpus consequences of
one ruling. It creates no new law; it banners existing law that the code already
executed. Authorized by Mike, 2026-08-12 ("amend away").

## The ruling

`tightbeam-decisions.md` §"2026-08-05 — Adjudication is DELETED. Model policy is
guidance, not substrate." (Flynn). The substrate owes exactly three things when
a model or engine cannot serve: **(1) TRUTH** (catalog contents, health,
exhaustion, routability, queryable), **(2) a NAMED FAILURE** (this turn did not
run, this is precisely why), **(3) a RECORD**. Nothing else. No hold, no
episode, no ladder, no ruling verb, no preference chain, no classification
taxonomy owned by the substrate.

Deleted from the tree accordingly: `Tightbeam.Adjudication` and its table,
`sessions.adjudicationHold` and every reader, the `adjudicate` verb, the
owner/recovery wakes, the adjudication escalation ladder, the boot reconciler,
and the heal machinery. Kept: the turn failing by name, the `[turn failed]`
marker, the lifecycle record.

The code executed this completely on 2026-08-05. The specs never heard about it
— until this amendment, the only written record of the consequence set was a
comment in `conformance_test.exs`. (One schema remnant: the empty
`adjudication_episodes` table still exists in deployed `state.db` files — no
drop migration shipped. It is dead weight, not live machinery.)

## What this deletion does NOT forbid

- **`decision_requests` and `effort-rule` survived the ruling** and remain the
  sanctioned shape for a question routed to a principal. The deleted thing was
  the substrate *seizing work* pending a ruling — holds wired into the turn-end
  schedule — not the existence of rulable rows.
- **Agent-elected block-and-ask is compatible** (GitHub issue #11, gdiab:
  agent create-path for `decision-requests`). Election vs. imposition is the
  boundary: the agent files the row and chooses whether to wait; it holds its
  obligation throughout and can progress, surrender, or work other things. If it
  sits idle, the effort-without-effect rail notices — the system working as
  designed.
- **The tripwire for any implementer:** the moment an open decision-request is
  *consumed by a substrate gate* — blocking a completion, holding a turn-end
  step, gating an assignment lifecycle — adjudication has been rebuilt under a
  new name. The row stays data the asker chooses to honor, never a condition
  the substrate enforces.

## Amended files (banner placed at the dead limb)

| File | Dead limb bannered |
|---|---|
| `s4-operability-v1.md` | Defect 2 entirely (holds releasing themselves); Defect 1 stays live |
| `supervision-impl-v1.md` | r21 schedule step 1 `:adjudication_hold`; stale "DRAFT r20" status label also corrected |
| `rails-mechanism-v1.md` | turn-end order position (4) ADJUDICATION-HOLD, incl. the code-sketch branch |
| `enforcement-smoke-set-spec.md` | `adjudicate`/`adjudication_episode` world keys, `adjudication-hold-order` fixture; census corrected 72 → 64 (per `conformance_test.exs`) |
| `topline-map-v1.md` | the `holds` output field sourced from `adjudication_episodes` |
| `observability-v1.md` | doorbell-audit rows for `adjudicationHold`, `adjudication_episodes`, adjudication respawn/chat (note also covers the previously-deleted `producer_jobs` row) |
| `job-forensics-v2.md` | §1 attribution columns + reopen/escalate kinds on adjudication episodes |
| `satellite-e2e-v1.md` | S4 resident-session recovery clause judged against a hold surface |
| `harness-support.md` | catalog re-keyed: the error-shape catalog SURVIVES (serves the ruling's named-failure duty); **GAP-1 is re-homed here** from `model-ringdown-pattern.md`; the classify-seam collection route is gone |
| `model-ringdown-pattern.md` | whole file as mechanism (top banner); principle survives in `production-machine-v1.md` |
| `effort-without-effect-checkin-v1.md` | whole file (top banner): superseded by `effort-checkin-v2.md`; its adjudication references are also dead |
| `wake-on-fact-v1.md` | citations of model-ringdown parked-state machinery (primitive itself unaffected) |
| `ROADMAP.md` | "A HELD SESSION IS INVISIBLE TO THE CLIENT" gap marked MOOT |
| `rails-and-guidance-roadmap.md` | phase KP1 (model adjudication) mechanism cancelled as written |
| `tightbeam.md` | hub rows updated same-change (effort-checkin v1→v2; this amendment recorded) |

Left deliberately unbannered: `tightbeam-decisions.md` (the ruling record
itself), `production-machine-v1.md` (the superseder; it describes the deletion),
the dated audit snapshots `sample-then-act-audit-2026-07-30.md` and
`topology-probe-2026-07-30.md` (honest records of the pre-deletion tree),
`conformance-handoff-ledger.md` / `conformance-spec-adjudications.md`
(historical handoff records; "adjudication" there also carries its other,
still-live sense — a ruling on a spec), `escalation-substrate-v1.md` (a single
precedent citation), and `derived-model-catalog-v1.md` (itself OBE —
superseded by `per-host-catalogs-v1.md` + `model-identity-v1.md`).

## Sweep contract

The dead vocabulary is: `adjudication_episodes`, `adjudicationHold`,
`adjudication[-_ ]hold`, `healToken`, `adjudication episode`, `ringdown`.
Verify with:

    grep -rlE 'adjudication_episodes|adjudicationHold|adjudication[-_ ]hold|healToken|adjudication episode|ringdown' *.md

Every hit must be this file, a bannered file, or a file in the
left-unbannered list above. When a future ruling deletes machinery, run the
same play: one amendment record, banners at every dead limb, hub updated in the
same change — the producer deletion (`p3-observables-producers-v1.md` §5) and
this amendment are the precedents.
