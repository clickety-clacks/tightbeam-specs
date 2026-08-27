# Decision-expecter smoke integration

Status: landed and verified.

- Work item: `wi_db31a5d5-3c61-4da4-b4d4-a021900ea3dd`
- Integration assignment: `asg_8284d0a3-c53e-452e-9b32-a246a8152aed`
- Repository: `github.com/clickety-clacks/tightbeam`
- Main before landing: `cba8d6c5e43e974e93890a901b83abd55f723500`
- Reviewed source: `c5a56f005edbd1648b7e0b9140f40f07922db9be`
- Source branch: `smoke/decision-expecter-delegate`
- Integration branch: `integration/decision-expecter-smoke-c5a56f0`

## Authority and source identity

Mike elected `main` for this feature and required the smoke at landing. The
producer filed `tests-passed` in `att_5f892f6c`. The producer report is
`art_969abae8`. The different-session review filed `reviewed-clean` in
`att_948e4f96`. Its report is `art_bed13417`.

Remote `main` and the reviewed source still identify the exact commits above.
The source has one parent, which is the exact pre-landing `main`. A fast-forward
of the owned integration branch made its tip equal to the reviewed source.

The source changes only `scripts/feature_smoke.exs`. It adds 102 lines and
removes 39 lines. The source tree is
`cc954262942ff4911a4d8e3b01bb0a83318a9adc`. The binary diff SHA-256 is
`9d6ddf83074ed57b4fb8f69eb6bc0cc978fdec6c744a465c18180f68823059c7`.
These values match the independent review. `git diff --check` passed.

## Baseline and candidate gates

The integrator ran the same full matrix on the exact parent and candidate.
Both runs passed with the same counts:

- Shipped privacy: clean.
- Public rule facts: pass.
- Elixir format: clean.
- Mix: 9 doctests and 1,798 tests passed. The suite reported 0 failures and
  11 skips.
- Rust format: clean.
- Rust: 246 unit tests passed. The doctor, SIGCHLD, and two stdin tests also
  passed.
- Package smoke: manifest, CLI, and gateway reported `0.2.0`. The package
  assembled.

The baseline log SHA-256 is
`a7142e505c9ce73a0df98a88f29e3262061c54de7ee52c7af740e079d24100bd`.
The candidate log SHA-256 is
`2551f74bde47b15358ab33197bf9bf91ce8f2ea2c5ea322a2d9c4f9b36fed763`.

## Focused real-session smoke

The integrator ran only the decision-expecter case from the committed smoke.
The runner compiled the committed script in memory and narrowed its top-level
selection chain. It did not edit repository bytes.

The smoke used a new disposable org on port 21577. It created a real parent
session and a different real delegate session. The delegate exact-read and
ruled a real effort request through the running gateway. The persisted row
kept the exact assignment, different expecter, `continue` decision, and
delegate ruler. The audit row kept the delegate role as origin and the
delegate session as principal.

The smoke reported `1 checks PASS`. The log SHA-256 is
`62d5b6c84e0f216321ce83b17a1e55ff8b76204f07a86ec74d0369582cc3133c`.
The stopped database SHA-256 is
`2373083febd7784cfae2f3f2afd1c6436ed8137cb8b62f4661ca5dd92780ff10`.
The integrator stopped this gateway and verified that port 21577 was closed.

## Review evidence discrepancy

The independent review report says its gateway stopped and port 21567 closed.
At 22:08 PT, read-only inspection found `beam.smp` process 2226043 still
listening on port 21567. The process started at 21:47:55 PT from the exact
review checkout. The integrator recorded this discrepancy in
`att_36b4aab4` and notified the product owner. The integrator did not signal or
reuse the different-session process.

This discrepancy changes the teardown claim in the review report. It does not
change the exact source, independent code review, or repeated gate results.

## Landing evidence

At 22:13 PT, the final pre-write read showed `main` at exact
`cba8d6c5e43e974e93890a901b83abd55f723500`. It showed the source and owned
integration branch at exact
`c5a56f005edbd1648b7e0b9140f40f07922db9be`. The old `main` was an ancestor
of the candidate. `git diff --check` passed.

The non-force command `git push origin
c5a56f005edbd1648b7e0b9140f40f07922db9be:refs/heads/main` advanced `main`
by one direct fast-forward. The remote accepted the update from `cba8d6c5` to
`c5a56f0`.

The immediate remote readback returned `main`, the source branch, and the
owned integration branch at exact `c5a56f005edbd1648b7e0b9140f40f07922db9be`.
It returned `0.1.9` unchanged at
`6c0eacb337c1de086d8d7d76f1c1dc57cad9a3d5`. It returned locked `0.1.8`
unchanged at `2ff4ed2a93527f1a7eeb56f2b9a8c52f10368ab5`.

The remote proof log SHA-256 is
`a9e98a8f22d8050ef35735880da6518df95b643c5e6a33b1b2ae8ce9e78513f4`.
No release, deployment, maintenance-line change, configuration change,
credential change, identity change, or unrelated live-state change occurred.
