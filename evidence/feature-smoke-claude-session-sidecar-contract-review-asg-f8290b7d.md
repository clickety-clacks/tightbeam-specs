# Final review — feature-smoke Claude session-sidecar contract

Review assignment: `asg_f8290b7d-130f-46bc-a63a-dc0fc524abcd`

Producer assignment: `asg_ee922fe3-3005-406b-af46-82cb4ffa2d10`

Reviewed at: 2026-08-28 23:52 PT

Verdict: **changes-requested**

## Exact target and custody

- Reviewed commit: `aad893964b0bbf08c99dfec54f64801611e85eca`
- Tree: `3906f4a992da947e8ce83ad5df69f1187479a8f6`
- Parent: `a3b1e249250b14daafe40e217f59e0e047144411`
- Parent tree: `f0ec46c94d3259e6e1d276cb2003b82e92833880`
- Parent parents: reviewed amendment
  `6881ff5af10ea32635ccc7c04499a1eb0429361a` and synchronized specs `main`
  `9ddcb07a779ee9f73285f5bfa54898651e781f13`
- Remote branch `refs/heads/spec/feature-smoke-sidecar-contract-asg-ee922fe3`
  resolves to the reviewed commit after a fresh fetch and `ls-remote` readback.
- The commit changes exactly these two paths:
  `specs/tightbeam/feature-smoke-claude-session-sidecar-contract.md` and
  `evidence/feature-smoke-claude-session-sidecar-contract-recon.md`.
- Contract blob: `14a3011981539de0c04d4908a111426a6281f21b`
- Contract SHA-256:
  `a0764919f9007c577cc4a3a0c045897de7ec9f2e1179692e51b114a5d040867d`
- Recon blob: `d92df381d0890442b551aefcb433ac921da8a937`
- Recon SHA-256:
  `ee254707c2291efc0d87430857cea1049236d436d71034bd3340419bd71712c7`
- Binary diff SHA-256:
  `1838b0e84dee44d0477c763099142d14f0b598ebd19133e57a8c32dd1d15fbaf`
- `git diff --check` passes.
- Current product-remote readback confirms `refs/heads/0.1.9` exists at
  `bdf0ad2c9ae4078f897a00e8c57767968676477c`; no `refs/heads/0.1.x` exists.

I consumed the full current work-item readback and trace: 49 assignments, 1,809
timeline events, 840 attests, and 19 decision requests. The sorted compact trace
SHA-256 is `ac0bfad936224ba41a5691cb128b07246e05a893eeb5dae8119525313173a55e`.
The sorted compact work-item readback SHA-256 is
`0ef04e67b0343c55764cdc064a45d96d6712597caa057706ccabbc52eddad837`.
I also read both prior exact-commit verdicts and their complete reports, both bounded
rework rulings, the producer's full attest history, and both reviewed files whole.

## Prior-finding closure

| Finding | Result | Evidence |
| --- | --- | --- |
| F1 — per-leg topology | satisfied | The harness-leg and phase terms require one sequential Claude leg, its cleanup, then one Codex leg; C-01 applies baseline and runtime checks per leg and forbids cross-home reads; AC-03, AC-24, and AC-29 preserve that topology. Contract lines 70-87, 168-202, 541-542, 562, 567. |
| F2 — exact retained evidence | satisfied subject to F7 | C-10 fixes exclusive creation, mode, phase cardinality, sync, field order, check order, pass cause, refusal truncation, and retention. F5 removes the impossible sink-failure record promise. The separate acquisition-error hole is F7 below. Contract lines 98-106, 363-496. |
| F3 — implementation base | satisfied | AS-01 and C-11 name concrete `origin/0.1.9`; current remote readback confirms it exists, while the historical commit remains evidence only. Contract lines 19-21, 110-113, 498-509, 566. |
| F4 — same-path predicate tie | satisfied | C-09 chooses category, observed raw path, then C-10 check order and maps the selected predicate to a clause; AC-25 requires stable code, phase, path, and clause. Contract lines 321-361, 421-460, 563. |
| F5 — evidence-sink contradiction | satisfied | C-10 makes the console `FX_EVIDENCE` refusal the only guaranteed evidence when append or sync fails, excludes that failure from record cardinality, and forbids retry, fallback, or a second append. I-12 and AC-34 carry the same boundary. Contract lines 156-159, 377-394, 572. |
| F6 — absent-path output | satisfied | Every `FX_PATH_SET` refusal is set-level `path=-`; it creates no missing-path candidate and performs no path sort. C-02 examples and AC-06, AC-16, AC-19, and AC-35 agree. Contract lines 204-222, 321-356, 544, 554, 557, 573. |

## Finding

### F7 — important — runtime-snapshot acquisition failures have no representable outcome

The contract makes filesystem acquisition part of the normative validator. The runtime
delta is a complete recursive set; the spawn interval ends only after all delta metadata
and regular-file bytes are read; decisions use `lstat` metadata and captured bytes; and
pre-wake/post-turn evidence requires a SHA-256 value for every regular entry. C-08 and
C-09 then require the validator to refuse on the first ordered check and emit a stable
code, path, clause, cause, and principal.

No clause defines what happens if directory enumeration, `lstat`, open, or read fails,
or if an entry disappears or changes type between those operations. The listed C-09
categories contain no acquisition-error value. A wrong-mode but regular file can also
be unreadable while C-10 still requires its hash in the refused record. One
implementation can crash without a refusal record; another can map the error to
`FX_JSON`, `FX_TYPE`, or `FX_EVIDENCE`; each choice changes the observable refusal and
none is selected by the contract. This leaves the one-shot smoke's core failure surface
undecidable.

Citations: Terms lines 61-66 and 74-76; I-03 and I-05 lines 142-146; C-02 lines
204-218; C-08-C-09 lines 311-352; C-10 lines 413-424 and 462-480; AC-20-AC-22 lines
558-560.

Deletion does not fully close F7. Deleting the unconditional hash requirement for a
regular entry whose bytes were not captured removes one impossible record field, but
deleting snapshot validation loses C-02-C-06. The narrow closure is to accept
acquisition failure as one named deterministic refusal value, define its ordering and
evidence fields, and permit `sha256=null` when bytes were not captured. It needs no
retry, fallback reader, second snapshot, or new file.

## Clause table

`Satisfied` means the candidate text is supported, scoped, and decidable. `Unsatisfied`
means it contradicts or omits a required decision. `Unproven` means the text might work
but the evidence or behavior contract is incomplete.

| Clause | Classification | Evidence |
| --- | --- | --- |
| Goal | satisfied | The contract is fixture-only, Claude-specific, and independent of launcher `osPid`. |
| Non-Goals | satisfied | Source, live, Codex admission, retry, second-fixture, and agent-pattern exclusions are explicit. |
| Terms: fixture, home, baseline, delta, relative path, token | unproven | The set and token grammar are exact, but snapshot acquisition failure is undefined; F7. |
| Terms: harness leg and phases | satisfied | Claude-first sequential legs, per-leg cleanup, and no cross-home read are explicit. |
| Terms: stem, mode, sidecar, identity | satisfied | Each predicate and identity member is exact. |
| Terms: evidence file and record | satisfied subject to F7 | Path, creation, mode, retention, JSONL framing, and content exclusions are exact; missing bytes make one entry field undecidable. |
| AS-01-AS-09 | satisfied | Branch, ownership, preserved observations, falsifiable epoch assumption, CWD seam, and one-shot release are explicit. |
| I-01-I-02 | satisfied | Claude-only fresh-fixture scope and pre-spawn baseline proof are exact. |
| I-03 | unproven | Complete-set evaluation has no result when enumeration or metadata acquisition fails; F7. |
| I-04 | satisfied | Launcher `osPid` is excluded from admission. |
| I-05 | unsatisfied | It requires captured metadata and bytes but defines no acquisition-error value; F7. |
| I-06-I-11 | satisfied | Codex refusal, no runtime mutation, consumption, evidence-content boundary, custody, and frozen state are exact. |
| I-12 | satisfied | Ordinary validator refusals are synced before cleanup; evidence-sink failure has an explicit console-only exception. |
| Architecture pattern and seam | satisfied | One fixture-only per-leg seam stays inside `check_local_deployment`; no concurrent shared-home mechanism appears. |
| C-01 | satisfied | Run-start and each leg's pre-spawn, pre-wake, post-turn, refusal, and cleanup sequence are decidable. |
| C-02 | unproven | The exact five-path set and predicates are clear, but an acquisition failure cannot reach a named result; F7. |
| C-03-C-07 | satisfied subject to F7 | Filename self-binding, schema, freshness, continuity, and Codex separation are exact once bytes and metadata are captured. |
| C-08 | unsatisfied | It promises an ordered refusal but does not cover a failed snapshot operation; F7. |
| C-09 | unsatisfied | F1-F6 ordering is deterministic, but the category list omits acquisition failure; F7. |
| C-10 | unproven | F5 is closed, but mandatory regular-file SHA-256 cannot be populated after a failed open/read; F7. |
| C-11 | satisfied | One-file custody and current `origin/0.1.9` base are exact. |
| C-12 | satisfied | Review, explicit release, deterministic cases, one fixture, smoke, and implementation review remain ordered. |
| AC-01-AC-19 | satisfied subject to F7 | Each positive or refusal case is decidable when snapshot acquisition succeeds. |
| AC-20-AC-22 | unproven | Symlink/type/mode/size cases require metadata and, for a wrong-mode regular file, evidence fields that can require an unavailable read; F7. |
| AC-23-AC-35 | satisfied subject to F7 | JSON, Codex, ordering, evidence, lifecycle, custody, full-matrix, sink-failure, and absent-path outcomes are otherwise exact. |
| Open Questions | unsatisfied | `None` conflicts with F7, which an implementer must decide. |
| Spec homing | satisfied | Exact pushed commit, tree, blobs, hashes, artifact rows, producer, and linked review identify the canonical set. |
| Agent operating pattern | satisfied | Non-Goals explicitly says none; this is a fixture-only admission contract. |

## Completeness, YAGNI, law, and subtraction

The F5-F6 amendment is bounded to Mike's ruling `dr_fb80acd4`; it adds no retry,
fallback sink, path admission, launcher topology, implementation file, live authority,
or second fixture. F1-F6 are closed. I found no amendment-specific embellishment.

The narrow validator should exist. Deleting it loses the required exact-home and
two-real-harness evidence; accepting permanent smoke failure leaves the required gate
closed. The design keeps inference out of the substrate, reports cause and principal,
and makes unknown runtime shapes fail loudly. F7 asks only that the same design make an
unknown filesystem acquisition failure representable; it does not justify another
mechanism or retry loop.
