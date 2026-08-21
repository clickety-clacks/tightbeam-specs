# Election slate reading-copy generator

Renders `0.2.0-spirit-and-work-sweep.md` (repo root, the source of record) as the
HTML reading copy Mike reviews: the lavish page on gibson, the claude.ai artifact,
and the eezo copy.

- `gen_election_artifact.py <out.html> [--with-diff]` — `--with-diff` appends a
  what-changed section (Mike's rule: comment-driven edits show a @pierre/diffs
  old-vs-new); the diff widget needs network (esm.sh), so it goes on the lavish
  copy only, never the claude.ai artifact (CSP).
- `eli5.py` — per-item plain-language explainers for list A, written 2026-08-21
  for Mike (audience: knows Tightbeam, has not seen the ticket). Intermediary
  prose, not PO prose; not part of the spec.
- `PENDING` set in the generator marks items whose election pends a Mike ruling.
  As of 2026-08-21: wi_c4450c8d and wi_7f068d0c pend the force-roles ruling
  (require role binding at seams that depend on roles; Mike's input is recorded
  on both cards by the 0.2.0 PO).
