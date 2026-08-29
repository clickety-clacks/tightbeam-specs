# Independent review — feature-smoke Claude session-sidecar contract

Review assignment: `asg_d4ee6811-87b7-4b89-9be2-aad820f95ed1`

Producer assignment: `asg_ee922fe3-3005-406b-af46-82cb4ffa2d10`

Reviewed at: 2026-08-28 20:50 PT

Verdict: **changes-requested**

## Exact target and custody

- Reviewed commit: `0d422d33632eb13e63a5129f7f34890628cb06a6`
- Tree: `08828a75da61f6e131337c2a486867ddf857139c`
- Parent: `b20194fe464f5792788bb5b7033245e4d0696889`
- Remote branch readback: `refs/heads/spec/feature-smoke-sidecar-contract-asg-ee922fe3`
  equals the reviewed commit.
- Contract blob: `ee37ab685c8d931d436a205418a10bc77ed54e96`
- Contract SHA-256: `c925150bfaf2ba80866941969d7a010ee2b3dba742b0803f2670079fa4c86e35`
- Recon blob: `31eb2d34979a3fd7046f375d4667668033b99f0b`
- Recon SHA-256: `faa9c47ac5d57dd1f7e1deec8285fbaaf171cacac49c0425f55a315a48d8909a`
- Canonical raw object-diff SHA-256: `dbfa755c8c21a40e95d54c4ca68a19fc7442c132795ac11033ad9da772c1483f`
- Custody is exactly the contract and recon paths, 691 insertions and no deletion.
- `art_2dd34430`, `art_ef6bf43e`, `att_91a18226`, and ruled requests
  `dr_e649588d=reopen-and-use-git-binding` and
  `dr_d419d501=authorize-linked-review` agree with this target.

I read both exact files twice. I also consumed the current complete work-item trace:
47 assignments and 1,789 timeline events. Its sorted compact JSON SHA-256 at review time
was `888be44d785f2019a1ccaf05f063a73f6dc9c7cb845edb37db9ffad59242fc32`.

## Findings

### F1 — blocking — the two-harness phase topology is undecidable

The architecture requires one seam to validate both harnesses at pre-spawn, pre-wake,
and post-turn. C-01 then requires the Claude five-path delta and the empty Codex delta
at both later phases. AC-29 separately requires both full harness legs to complete.
The terms define pre-spawn and pre-wake around a generic harness spawn request, but do
not say whether those phases occur once around Claude, once around each leg, or around
two concurrently held sessions.

Two incompatible implementations satisfy the text:

1. Apply C-01 only around the Claude leg. C-07 then proves Codex is empty before Codex
   starts, but never checks Codex after its own spawn.
2. Apply C-01 around each sequential leg. During the Codex leg, C-02 still requires the
   Claude five-path set even though the existing per-leg cleanup can retire Claude and
   remove its sidecar.

The current source makes this load-bearing: `scripts/feature_smoke.exs` at source commit
`be61cfc9` loops over harness legs and each `check_local_deployment` invocation retires
its session in its own `after` block. The contract must name the session lifetime and
the exact observation sequence for each harness before one-file implementation is
decidable.

Citations: contract lines 69-82, 154-175, 274-281, and 412-413; source commit
`be61cfc9`, `scripts/feature_smoke.exs` lines 76-103 and 119-223.

Deletion test: deleting the claim that both harnesses share every sidecar phase, then
stating separate per-leg observations, can close the ambiguity without adding a second
validator. Deleting Codex separation entirely cannot close it because C-07 is a ruled
boundary.

### F2 — blocking — the durable evidence contract cannot be implemented or reviewed

The Evidence record term and AC-26 require metadata, hashes, booleans, cause, and
principal. C-10 does not define the record's serialization, destination, cardinality,
or write/read seam. It defines cause only for refusals, leaving the required cause of a
passing record unspecified. It also requires cross-phase identity equality among the
predicate results for each sidecar observation, although that value cannot exist at
pre-wake and cannot exist after a pre-wake refusal.

An implementation that prints one line per entry and one that holds an aggregate map
until cleanup both satisfy “records,” but they produce different durable evidence.
A reviewer cannot decide AC-26, and the one-shot fixture can remove the only sidecar
before the ambiguity is discovered.

Citations: contract lines 93-95, 323-341, and 408-410.

Deletion test: deleting evidence is not available because the controlling Class-12
boundary and I-12 require content-free evidence before cleanup. The smallest closure is
one explicit record schema and destination, with phase-specific availability and a
defined cause for passing records.

### F3 — blocking — the implementation base is not a Git ref

The header and AS-01 name `origin/0.1.x`; C-11 and AC-28 require the implementer to
start from its then-current value. Remote readback on 2026-08-28 PT showed only
`refs/heads/0.1.8` at `2ff4ed2a` and `refs/heads/0.1.9` at `7eec98b7`; no
`refs/heads/0.1.x` exists. The served integration rule locks 0.1.8 and directs active
0.1 maintenance work to 0.1.9. A producer attest later interprets “0.1.x” as 0.1.9,
but that correction is absent from the durable normative file.

The implementation cannot perform the required start operation from the named ref.

Citations: contract lines 19-20, 99-101, 343-354, and 411-412; independent
`git ls-remote` readback; served `integration-targets` rule.

Deletion test: delete the nonexistent alias and name the authorized concrete branch.
No new mechanism is needed.

### F4 — important — same-path failures have no deterministic tie-break

C-09 orders categories and then relative paths. It does not order predicates when one
path fails more than one predicate in the same category. For example, a sidecar can
fail filename/internal-PID equality under C-03 and expected-CWD equality under C-04.
Both map to `FX_SIDECAR_SEMANTIC` on the same path, while the required refusal line
still exposes a `clause` value. AC-25 requires only code, phase, and path stability, so
either C-03-first or C-04-first implementations pass it while emitting different
causes.

Citations: contract lines 283-321 and 408-409.

Deletion test: deleting the exposed clause/cause would conflict with C-10 and wisdom 5.
The smallest closure is a predicate tie-break order or a rule that evaluates and emits
all failed predicates without a first-predicate choice.

## Clause table

`Satisfied` means the candidate text is scoped, supported, and decidable. It does not
claim that an implementation exists.

| Clause | Classification | Evidence |
| --- | --- | --- |
| Goal | satisfied | Strict fixture-only PID-independent admission traces to Class 12 and the consumed fixture. |
| Non-Goals 1-8 | satisfied | Source/live/review/retry exclusions are explicit and preserved by C-11/C-12. |
| Terms: Fresh fixture, Projected home, Owned baseline, Runtime delta, Relative runtime path | satisfied | Each denotes an observable fixture/path set; byte escaping and no-symlink traversal are decidable. |
| Terms: Evidence token | satisfied | Literal byte class plus uppercase `%HH` makes one-line tokens unambiguous. |
| Terms: Spawn interval and five phases | unsatisfied | Phase names are locally clear, but their two-harness application is not; F1. |
| Terms: numeric stem, permission mode, sidecar, identity | satisfied | Predicates and tuple are exact. |
| Term: Evidence record | unsatisfied | Required cause/timing/format/destination are incomplete; F2. |
| AS-01 | unsatisfied | `origin/0.1.x` does not exist; F3. |
| AS-02 | satisfied | Authority split between Homes ownership and fixture admission is explicit. |
| AS-03-AS-06 | satisfied | Recon and surrender rows support the preserved metadata and two sampled schemas without claiming deleted bytes. |
| AS-07-AS-09 | satisfied | CWD derivation, epoch assumption/refusal, and one-shot release are explicit and falsifiable. |
| I-01-I-11 | satisfied | Scope, whole-set evaluation, no launcher PID, Codex refusal, no mutation/reuse, evidence exclusions, custody, and frozen state are exact. |
| I-12 | unproven | Evidence must precede cleanup, but the evidence write seam is undefined; F2. |
| C-01 | unsatisfied | The per-harness/full-run phase topology is undecidable; F1. |
| C-02-C-07 | satisfied, subject to C-01 | Path/type/mode/schema/freshness/continuity and Codex predicates are individually exact. |
| C-08 | unproven | “First failing ordered check” depends on the missing same-path tie-break in C-09; F4. |
| C-09 | unsatisfied | Category and path order omit a same-path predicate order; F4. |
| C-10 | unsatisfied | Record shape, destination, pass cause, and phase availability are missing; F2. |
| C-11 | unsatisfied | One-file custody is exact, but its required base ref does not exist; F3. |
| C-12 | satisfied | Review, release, deterministic gates, one fixture, smoke, and exact-commit review are ordered and separately authorized. |
| AC-01-AC-03 | unproven | Individual assertions are decidable, but their run/leg placement depends on F1. |
| AC-04-AC-24 | satisfied, subject to C-01 | Each positive or refusal case has exact inputs and outcomes; no launcher PID is reintroduced. |
| AC-25 | unsatisfied | It omits the exposed clause/cause from repeatability and leaves same-path ties open; F4. |
| AC-26 | unsatisfied | Evidence presence is not decidable without a record contract; F2. |
| AC-27 | satisfied | Consumption, no mutation, retained base, and cleanup boundary are exact. |
| AC-28 | unsatisfied | It requires a nonexistent `origin/0.1.x` base; F3. |
| AC-29 | unproven | Both legs are required, but the shared/per-leg validation sequence is missing; F1. |
| AC-30 | satisfied | New runtime shape refuses once and returns for ruling. |
| AC-31 | satisfied | Current trace preserves the named parent, product assignment, and facts boundary. |
| Open Questions | unsatisfied | “None” conflicts with the four unresolved implementation choices above. |
| Spec homing | satisfied | Ruled Git binding, exact remote commit/tree/blobs, two artifact rows, and hash-bearing review assignment identify the canonical set. |
| Agent operating pattern | satisfied | Non-Goals explicitly say none; the capability remains fixture-only and needs no manual amendment. |

## YAGNI and subtraction

The five-path strict validator is within the Class-12 authority. The candidate does not
reintroduce launcher topology, expand Codex admission, or authorize live work. I found
no separate embellishment beyond the four findings above.

The mechanism itself should exist: deletion loses the required exact-home and real
two-harness smoke evidence, and accepting permanent failure leaves the parent gate
closed. F1 and F3 have subtraction-first closures. F2 and F4 need only the minimum
missing contract text; they do not justify another file, validator, or lifecycle.
