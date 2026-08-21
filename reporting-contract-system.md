# The reporting-contract system — one release, four parts

Status: grouping record, 2026-08-21. These ship together as a system; none
is complete alone. Target: a single 0.2.x release landing (order within it
per the wi_ecd8cd9d fold's build cards).

| part | work item | state |
|---|---|---|
| cannot-proceed replaces surrender; typed awaiting; boundary-anchored checkpoints | wi_ecd8cd9d (staffed: asg_bed98474) | spec fold in progress |
| effect kind `outcome` (enum + DDL migration) with one opener guidance line and `unspecified` → `code` | rides wi_ecd8cd9d, same MVP fold | clause filed; `fixture` deferred |
| identity CLI verb: shared guidance docs + manual override (`identity edit --doc`) | wi_2629d68d | iceboxed until fold sizes it |
| user-alerted → decision-request threshold statute | wi_a8de6fe5 (notes: user-alerted-decision-request-escalation.md) | iceboxed pending Mike discussion |

Why a system: all four reshape the same contract — how a blocked or waiting
agent's state becomes a row someone must act on. Shipping them piecemeal
recreates the seams they close (a cannot-proceed without `outcome` cannot size
its accountable done-test; `outcome` without the guidance verb cannot teach openers
org-locally; the threshold statute without cannot-proceed double-covers
persistence). Mike's instruction 2026-08-21: schedule into a release as a
system; the items reference each other through this record.

MVP trim, Mike 2026-08-21: `fixture` and RE-ARM do not ship in this system
landing. Both are deferred second-occurrence purchases. Guidance and kit 4.9
continue to govern retry; successor dispatch remains the default instead of
RE-ARM. Omitting any of the four table rows still requires Mike's explicit
ruling.
