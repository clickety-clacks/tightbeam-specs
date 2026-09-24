# Addendum 1 to bounded guidance review asg_23375f4e

Base report: art_0a19acff, sha256 df505d88837868becf606e4b77779b8f600a2f0cd1b4c48e109cd7ff6884a9ff
Work item: wi_c13b63c8-b21f-47ce-bfac-61d51de854a4; producer asg_06a5780a
Date: 2026-09-24. Reviewer: s_16e60e31 (claude-opus-5-5). No tests run anywhere.

## Inputs read

- Writer addendum art_d7e3d6d4, sha256 f4ec9447...c771 (verified). Contents:
  `bounded-review-disposition-20260924.md`, `bounded-review-inputs.sha256`, and an
  earlier copy of the review brief.
- Updated owner brief art_001c8ce7, sha256 2cb99d0f...bf30 (verified). It adds a
  "Later bounded input" section; the review subject is otherwise unchanged.
- Every entry in `bounded-review-inputs.sha256` (live-candidate files and patch
  a437ffcb, legacy candidate 9d61c12b, source patch ced17ebe, bundle, hunk map,
  acceptance matrix 22c35749) recomputes OK against the files in
  `/home/mike/.tightbeam/work/ea541c9d8c00`.
- I read the new test directly, read-only via git on Racter, in
  `/home/clu/.tightbeam/work/1b54aa406cba/tightbeam-engineering-ownership`:
  commit b2d330f3, tree ec62922e confirmed, `test/gateway_test.exs` lines
  2219-2282, "fresh PDO and orchestrator spawns resolve their defaults without
  changing coder choice".

## Model-evidence credit (Q3)

The writer's description matches the bytes. The test:

- calls the real gateway `spawn` handler without model or effort parameters and
  asserts the stored models: pdo and orchestrator gpt-6-sol/low, coder
  gpt-6-luna/max, harness codex, provider openai;
- writes its own three manifests with `File.write!` and literal model values
  (`where = ["testhost"]`, no elections), and a synthetic host catalog;
- always passes `archetype:` explicitly.

Credit: this is real progress on the spawn seam. Manifest `[defaults]` flow
through the actual spawn handler into the stored session model when no override
is given. That is stronger than the earlier `Archetypes.load`-only assertion.

Not credited: it does not show that a fresh session gets its defaults from the
shipped .9 engineering candidate's `pdo.toml`/`orchestrator.toml`/`coder.toml`,
because it never learns or loads the packaged bundle. It does not cover an
omitted archetype resolving through default-archetype = pdo. It does not show
host-catalog qualification on a real host, or a provider receipt. The writer's
reported 105/0 and 11/0 counts were not independently inspected here.

## Effect on the base findings

- The source (19eb9895/tree 21581), live candidate (a437ffcb) and legacy
  candidate (9d61c12b) are byte-identical to what the base report reviewed.
  F1 and F2 stand as blocking. F3-F9 are unchanged.
- The verdict stays changes-requested, bounded, not overall clean.
- The carry-forward list is unchanged. Q3 carry-forward now also includes the
  spawn-seam credit above.
- The delta review item "fresh PDO default creation and provider receipt" stays
  open. It narrows to: defaults resolved from the actual learned .9 package
  manifests, the omitted-archetype path, and a real host or provider receipt.
  The test/runner fix belongs to Lane 2.
- The review timing correction (Mike's direct authorization of this bounded
  review before full dynamic receipts) matches how this review ran. It changes
  no finding.
