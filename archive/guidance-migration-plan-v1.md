# Guidance migration plan v1 — mapping distributed agent guidance into tightbeam

Status: DRAFT r1 (Claude/Opus authored; for Sol xhigh adversarial review BEFORE execution).

## Purpose

Today, "dark factory" and adjacent agent behavior is produced by guidance
scattered across many uncoordinated sources on multiple hosts. We must map ALL
of it into tightbeam's structure — guidance fragments, rails TOML, skill
elections, and roles (orchestrator / reviewer / coder-implementor) — while
correctly classifying each piece as SUBSTRATE (constitution) or KUNGFU (tunable
law/skills/guidance). Beyond a 1:1 port, we want to REFACTOR (in the
factorization sense) into a congruent, better-organized set that conforms to
tightbeam's structure. The first kungfu bundle produced is
`kungfu/agentic-engineering/` (dark-factory, graph-based), each kungfu carrying a
manifest/README describing its purpose and contents.

## Governing principle (everything below serves this)

The enemy is SILENT LOSS, and it enters the moment anything is moved, merged, or
deleted before everything has been listed. Therefore the sequence is rigid:
inventory → atomize → classify → factor → map → reconcile, and NOTHING is moved,
merged, or deleted until a reconciliation gate proves every atom has an explicit
disposition. Two invariants throughout:

- I1 — Classify NORMS, not files. rules.md / claude.md / soul are bundles of
  dozens of distinct norms; file-level classification drops nuance.
- I2 — Bidirectional traceability. Every atom points to its source span + content
  hash; every target points to its atom(s). The final gate proves 100% coverage
  both ways.

## Known sources (Phase 0 must DISCOVER, not trust this list)

- TARS openclaw: `agents`, `soul`, `rules.md`, `skills`, plus other standard
  openclaw guidance files (enumerate the dirs — do not rely on memory).
- CONTRIBUTED `agents.md` + skills files.
- eezo `.claude/CLAUDE.md`, `.codex/codex.md`, and BOTH skill trees (which
  "should be the same" — a dedup candidate, not an assumption).
- This repo's CLAUDE.md; the tightbeam decisions ledger (it encodes rulings =
  guidance); ROADMAP / spec guidance.
- Anything else the enumeration turns up. TARS openclaw is PRODUCTION: read-only,
  never mutate. Every TARGET lands in tightbeam kungfu on eezo.

## Phases

- Phase 0 — CENSUS. Discover + hash every guidance source across hosts.
  Read-only. Output: a manifest (source, host, path, hash, size, mtime).
  Parallelizable (one reader per source/host). This is THE checklist; nothing is
  authoritative until it is on it.
- Phase 1 — ATOMIZE. Decompose each source into atomic guidance units (one
  norm/rule/skill/fact each): stable ID, provenance (file:lines + hash), verbatim
  text, one-line summary. No classification. A dropped norm surfaces later as a
  missing atom.
- Phase 2 — CLASSIFY (author → cross-model review). Per atom, two axes: (A)
  substrate-vs-kungfu via the litmus "could a sane operator reasonably want this
  different?"; (B) for kungfu atoms, the FORM: rails-toml (deny/halt/escalate) |
  skill | guidance-fragment | role-binding. Plus authority (openclaw-core /
  contributed / Flynn-directive) and confidence. Opus authors classifications;
  Sol xhigh adversarially reviews (mis-classified? substrate-creep? lost
  nuance?); disagreements → Flynn rulings queue.
- Phase 3 — FACTOR (author → cross-model review). Across classified atoms:
  dedupe (e.g. claude/codex skills → one shared atom, noting real divergences),
  factor common structure (role norms → base + role deltas), and SURFACE
  contradictions (the "schizophrenia" — conflicting sources) and gaps
  (relied-on behavior written nowhere). Contradictions + gaps → Flynn rulings.
  Output: a factored target model.
- Phase 4 — TARGET LAYOUT (Opus designs → Sol reviews). Map factored atoms to
  tightbeam structures: substrate code (expected few), rails TOML (which kungfu),
  skills (elected by which roles), guidance fragments, role definitions
  (orchestrator / reviewer / coder). Design the `kungfu/agentic-engineering/`
  tree and the per-kungfu MANIFEST schema (purpose, contents, elections, rails
  carried, provenance, dependencies).
- Phase 5 — RECONCILE + EXECUTE. Gate: EVERY Phase-0/1 atom has a disposition —
  mapped | deferred-with-reason | dropped-with-Flynn-ruling. No silent
  unaccounted atom. Then build the bundle(s) + manifests + substrate changes via
  the normal spec→review→build→review→merge pipeline, each traceable to atoms.

## Structural recommendations

- R1 — A durable migration REGISTRY (census → atoms → classifications →
  dispositions) as one inspectable artifact. The anti-drop guarantee cannot live
  in an agent's context (compaction loses it). The registry is the spine and
  spans many sessions.
- R2 — Batch Flynn rulings. Phases 2–3 accumulate a rulings queue (classification
  disagreements, contradictions, boundary calls); batch them rather than
  interrupting per-atom. This migration is escalation-policy's first customer.
- R3 — Read from openclaw/TARS; write only to tightbeam. Sources are never
  mutated; TARS openclaw stays production-clean.

## Review-pass model (corrected)

"Bounce" = the standard cross-model review topology (author → adversarial review
→ revise), NOT an interactive dialogue. Each phase: Opus authors the artifact,
Sol xhigh reviews it, revise, escalate disagreements to Flynn. Same topology used
for specs and code this session.

## Open questions for Sol's review of THIS plan

- Does the phasing miss a silent-drop vector?
- Is atom granularity (Phase 1) the right unit, or does it need a coarser/finer
  cut?
- Is there a better ordering (e.g. should dedup happen during atomization to
  reduce classification load, or does that risk premature merging)?
- Is the substrate-vs-kungfu litmus sufficient, or are there atoms it can't
  cleanly adjudicate (needing a third bucket, e.g. "role-scoped constitution")?
- Registry format: single structured file vs. tightbeam work-items vs. other?
