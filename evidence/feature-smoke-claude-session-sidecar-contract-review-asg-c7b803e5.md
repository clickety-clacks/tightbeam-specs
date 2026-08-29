# Successor review — feature-smoke Claude session-sidecar contract

Review assignment: `asg_c7b803e5-e1f4-4c4e-98cf-5475e1d40236`

Producer assignment: `asg_ee922fe3-3005-406b-af46-82cb4ffa2d10`

Reviewed at: 2026-08-28 21:31 PT

Verdict: **changes-requested**

## Exact target and custody

- Reviewed commit: `6881ff5af10ea32635ccc7c04499a1eb0429361a`
- Tree: `bbc6563f86aafd7e49a9743254bf655bf8ec2915`
- Parent: `0d422d33632eb13e63a5129f7f34890628cb06a6`
- Remote branch: `refs/heads/spec/feature-smoke-sidecar-contract-asg-ee922fe3`
  equals the reviewed commit.
- Contract blob: `805fbd6a1670f0048e0c02520f5d02cb53f3eb9c`
- Contract SHA-256:
  `ce94f072a03dd1a5a032b131aac36623e5bda22e74082538b61108590076dd20`
- Recon blob: `808b364c621f7b039a472c1a37211e1ad9675521`
- Recon SHA-256:
  `00876c1b73deb1dbbba907ed578ad4ed101a2e28dc687a6cc43c655b09a8bae4`
- The reviewed commit changes exactly the contract and recon paths. `git diff --check`
  passes. The owned review clone was clean before this report.
- Independent remote readback confirms product branch `refs/heads/0.1.9` exists at
  `7eec98b7848340ae00e2b564a4eb97c0f429a445`; no `refs/heads/0.1.x` exists.

I read the amended contract and recon whole, the full producer attest history, the
first review verdict and report, the cited upstream receipts, the work-item trace, and
Mike's bounded rework ruling. I did not edit either reviewed file or run source,
fixtures, or smoke.

## Findings

### F5 — blocking — an evidence-write failure makes C-10 contradict its own record guarantee

C-10 requires every phase to append exactly one synced evidence record. It then says an
append or sync failure emits `FX_EVIDENCE` and must not attempt a second append. The next
paragraph says every refusal after evidence-file creation contains all completed-phase
records plus one complete `refused` record for the failing phase. Those requirements
cannot all hold when the failing operation is the append itself. An append can fail
before a complete JSON object and LF exist; a sync failure cannot prove the appended
record is durable. Retrying is expressly forbidden.

Two incompatible implementations follow: one treats `FX_EVIDENCE` as an exception to
the record-cardinality guarantee, while another tries to preserve the guarantee despite
the no-second-append rule. I-12 also promises evidence before cleanup, although C-10 and
AC-34 require cleanup after a post-spawn evidence-sink failure.

Citations: contract C-10 lines 371-382, I-12 lines 156-157, and AC-34 line 560.

Deletion test: yes. Exclude evidence append/sync failures from the complete-record
cardinality sentence and say that the console refusal is the only guaranteed evidence
when the evidence sink itself fails. No retry, fallback sink, or new mechanism is
needed.

### F6 — important — path-set refusal output is not deterministic when a required path is absent

C-02 requires refusal for a missing listed path. C-09 orders observed relative runtime
paths by raw bytes and requires the refusal line to expose a path token or dash. The
Terms define a relative runtime path as a path to an actual recursive entry. Therefore,
a missing required path has no relative runtime path to sort. The contract does not say
whether a missing path emits its expected name or `-`, nor how a missing expected path
orders against an unexpected observed path in the same `FX_PATH_SET` failure.

Both a symmetric-difference implementation that includes absent expected names and an
observed-only implementation that chooses an extra path or dash satisfy the current
words but emit different refusal lines. AC-25 does not close this case because its Given
describes paths that fail predicates, not an absent required path.

Citations: Terms lines 63-66, C-02 lines 204-220, C-09 lines 327 and 340-350, and AC-25
line 551.

Deletion test: yes. Define every set-level `FX_PATH_SET` refusal to emit `path=-` and
remove path sorting for that category. If the path token must remain, the spec instead
needs an explicit missing-versus-extra candidate order.

## First-review finding closure

| First finding | Result | Evidence |
| --- | --- | --- |
| F1 per-leg topology | satisfied | Harness-leg and phase terms at lines 70-87; per-leg seam and ordered Claude cleanup before Codex at C-01 lines 166-200; AC-03, AC-24, and AC-29 preserve no cross-home read. |
| F2 exact retained evidence | unsatisfied | Destination, mode, seven-record pass order, schema, applicability, and pass cause are now exact at lines 98-106 and 357-484, but F5 leaves the required evidence-sink refusal state contradictory. |
| F3 `origin/0.1.9` | satisfied | Header line 19, AS-01 lines 110-113, C-11 lines 486-490, and AC-28 line 554 use the concrete branch; independent remote readback confirms it exists. |
| F4 category/path/predicate tie-break | satisfied for the cited same-path case | C-09 lines 321-355 and C-10 lines 414-448 fix predicate order and clause mapping; AC-25 now exposes clause. F6 is a separate absent-path set-error hole. |

## Clause table

`Satisfied` means the candidate text is supported, scoped, and decidable. It does not
claim an implementation exists. `Unsatisfied` means the text contradicts or omits a
required decision. `Unproven` means the clause might work but the contract lacks the
evidence needed to classify it.

| Clause | Classification | Evidence |
| --- | --- | --- |
| Goal | satisfied | Fixture-only PID-independent admission remains exact and traces to the consumed-fixture ruling. |
| Non-Goals | satisfied | Source, live, retry, Codex-admission, and operating-pattern exclusions remain explicit. |
| Terms: fixture, homes, baseline, delta, paths, token | satisfied | Each denotes an observable set or reversible ASCII token. |
| Terms: harness leg and phases | satisfied | One sequential Claude leg, cleanup, then one Codex leg is explicit; no cross-home read. |
| Terms: numeric stem, mode, sidecar, identity | satisfied | Each predicate and identity member is exact. |
| Terms: evidence file and record | satisfied subject to C-10 | Path, exclusive creation, mode, retention, JSONL framing, and content exclusion are exact. |
| AS-01 | satisfied | `origin/0.1.9` is concrete and exists remotely; the old commit is historical evidence. |
| AS-02-AS-09 | satisfied | Ownership, preserved observations, falsifiable epoch assumption, CWD seam, and one-shot release remain explicit. |
| I-01-I-11 | satisfied | Scope, whole-set evaluation, no launcher PID, Codex refusal, no mutation/reuse, custody, and frozen state are exact. |
| I-12 | unsatisfied | It promises evidence before cleanup for every refusal, but F5 shows the evidence sink can fail before a durable record while cleanup still runs. |
| Architecture pattern and seam | satisfied | One fixture-only per-leg seam is bounded to `check_local_deployment`; no concurrent session or parallel allow-list pattern appears. |
| C-01 | satisfied | Run-start and each leg's pre-spawn, pre-wake, post-turn, refusal, and cleanup order are decidable. |
| C-02 | satisfied subject to C-09 | The five-path set, types, modes, cardinality, nesting, and symlink refusal are exact; F6 affects only the refusal-path output. |
| C-03-C-06 | satisfied | Filename self-binding, exact schema, freshness bracket, and phase continuity are exact and launcher-independent. |
| C-07 | satisfied | Codex delta must be empty and the Codex leg cannot inspect Claude's home. |
| C-08 | satisfied | Admission mismatch does not mutate observed entries; existing lifecycle cleanup remains separate. |
| C-09 | unsatisfied | Same-path predicate order is closed, but F6 leaves the required path field undecidable for missing-path set failures. |
| C-10 | unsatisfied | Record format and pass behavior are exact, but F5 makes the append/sync error path internally contradictory. |
| C-11 | satisfied | One-file custody and current `origin/0.1.9` base are exact. |
| C-12 | satisfied | Review, explicit release, deterministic cases, one fixture, smoke, and implementation review remain ordered. |
| AC-01-AC-24 | satisfied | Each positive or refusal case has a decidable input and outcome under the per-leg topology. |
| AC-25 | unproven | It proves category/path/predicate stability for present paths but does not cover F6's absent-path choice. |
| AC-26 | satisfied | The passing evidence file has exact mode, framing, cardinality, order, schema, and content boundary. |
| AC-27 | satisfied | Consumption, retained fixture base, no fixture mutation, and lifecycle cleanup remain exact. |
| AC-28-AC-33 | satisfied | Base/custody, full matrix, one-shot blockers, frozen state, evidence refusal detail, and preexisting evidence path are decidable. |
| AC-34 | unsatisfied | It requires the evidence-sink refusal but does not reconcile it with C-10's complete failing-phase record guarantee; F5. |
| Open Questions | unsatisfied | `None` conflicts with F5 and F6, which an implementer must decide. |
| Spec homing | satisfied | Exact Git commit/tree/blobs, artifact hashes, producer binding, and linked successor assignment identify the canonical set. |
| Agent operating pattern | satisfied | Non-Goals explicitly state none; this remains fixture-only capability. |

## Completeness, YAGNI, and subtraction

The amendment stays within Mike's F1-F4 authority. The evidence-file creation and sink
failure clauses are necessary consequences of making F2 durable, not independent
capability. The change does not widen the five-path set, admit Codex state, infer a
launcher relationship, authorize a second fixture, expand implementation custody, or
resume product work. I found no separate embellishment.

The narrow fixture validator should exist. Deleting it loses the required exact-home
and two-real-harness proof; accepting permanent failure leaves the required smoke gate
closed. Both reported defects have subtraction-first closures. Neither needs another
file, fallback evidence system, retry, or lifecycle.
