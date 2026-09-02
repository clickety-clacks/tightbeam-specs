# Class A failed-turn intent survival — dual-line candidate evidence

Date: 2026-09-02

Assignment: `asg_7f29cbc5-4cab-4431-aa30-b0a4fa0917c1`

Work item: `wi_6d418db1-26b4-4ad0-9886-86e757e93342`

## Authority and design trace

Mike elected exact 0.1.9 and main candidates for defects 1–3 without the
0.2 typed-run-disposition prerequisite. The bounded design input includes
checkpoint `att_20159eb6`, anatomy `att_e8684ab7-af91-43ee-9c85-07ac78241480`,
and the reviewed patrol classification and escalation specification at
`511539c8cefe0347cdcc74fcaf93642c6f5299d1` in this repository. The latter
was reviewed clean in `att_598c2933`, with report `art_e81605d3`.

The implementation does not change 0.1.8, install a release, modify Gibson,
work around a toolchain pin, or mutate live state. Both candidates are
targetless and await one independent review.

## Canonical candidate custody

Repository: `git@github.com:clickety-clacks/tightbeam.git`

| Line | Target baseline | Candidate branch | Exact candidate commit |
| --- | --- | --- | --- |
| main | `3e1dc56e1bd27854487228c05f4b2e1c9dd4fb22` | `candidate/class-a-failed-turn-main` | `8568d22476fe6435bba2d7afbfb190188f65a34f` |
| 0.1.9 | `c3299e3a75dab21ed2839822d8ad207514f92782` | `candidate/class-a-failed-turn-019` | `dc4a0d2bf8d00dac2117f1be454292c213c68f9e` |

After the gates completed, both target refs were fetched again and were
confirmed as ancestors of their candidate. `git ls-remote` then confirmed
that the canonical remote branches resolved to the exact commits above.

## Implemented behavior

- Eligible prompt wakes whose turns close as `rate-limit-dead` create a new,
  deterministic successor wake and turn with bounded exponential delay. The
  failed turn stays terminal. Unsafe or untyped failure classes do not replay.
- Canceling the original root wake follows the retry chain and cancels the
  newest pending successor.
- Patrol classifies terminal turns once. Ordinary successful delivery resets
  the session streak. Ordinary failed or canceled turns advance it. Bubble
  notice failures do not enter the same streak.
- The sixth consecutive ordinary failure creates one deterministic patrol
  escalation cause. A failed notice continues through parent sessions until
  Main. The distinct patrol cause prevents recursive streak formation.
- Main uses the operational effective-parent seam. The 0.1.9 port resolves
  its available transaction-local `spawnedBy` parent topology.
- The supervision prod ladder advances from heard prods rather than sent
  prods on both lines.

## Port and reconciliation record

The port was feasible with bounded line conflicts. Main already contained
the heard-prod repair and operational-parent seam. During the gate window,
main advanced to `3e1dc56e1bd27854487228c05f4b2e1c9dd4fb22`; that head was merged cleanly
into the candidate before the final gates. On 0.1.9, the heard-prod change was
ported and the implementation was reconciled manually with the older Bubble,
ledger, user-schema, and `spawnedBy` parent APIs. The exact delivery-sink
source census was extended on both lines for the new in-transaction patrol
route.

## Verification

All commands used Elixir 1.19.5 / Erlang OTP 28 where applicable. Each Mix
gate used its own temporary `TIGHTBEAM_BASE_DIR` and the repository's
authoritative gate script.

### main

Commands:

```text
mix format --check-formatted
scripts/verify_mix.sh
cd cli && cargo fmt --check && cargo test
```

Results:

- Authoritative Mix gate: 9 doctests, 2,166 tests, 0 failures, 11 skips.
- CLI gate: 279 tests across unit and integration binaries, 0 failures.
- Focused failed-turn intent suite: 4 tests, 0 failures.
- Related wake, Bubble, supervision, and failed-turn suites: 110 tests,
  0 failures.
- Exact delivery-sink census: 11 tests, 0 failures.

### 0.1.9

Commands:

```text
mix format --check-formatted
scripts/verify_mix.sh
cd cli && cargo fmt --check && cargo test
```

Results:

- Authoritative Mix gate: 9 doctests, 1,770 tests, 0 failures, 11 skips.
- CLI gate: 294 tests across unit and integration binaries, 0 failures.
- Focused failed-turn intent suite: 4 tests, 0 failures.
- Related wake, Bubble, supervision, and failed-turn suites: 105 tests,
  0 failures.
- Exact delivery-sink census: 12 tests, 0 failures.

The full gates emitted existing compiler and negative-fixture diagnostics.
Their exit status and final ExUnit/Cargo summaries were green. No
baseline-matching exception was used.

## Review boundary

Review the two exact commits as one dual-line change. The review should check
behavioral equivalence across the available parent APIs, deterministic retry
and escalation identity, cancellation continuity, exactly-once terminal
classification, Bubble recursion exclusion, and the closed scope above. No
target branch may advance from these candidates until the independent review
is clean and the applicable integration gate is green.
