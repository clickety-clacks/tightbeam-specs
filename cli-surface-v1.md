# Tightbeam CLI surface — v1 (living contract)

Status: RATIFIED (Flynn ruling, adjudication #7, 2026-07-24). Supersedes the
retired Rust PORT spec (archive/cli-rust-v1-PORT-SPEC-RETIRED.md) — that spec's
"no new verbs" invariant was port-fidelity discipline for a completed migration,
not surface policy, and its ghost caused a spec-obedient deletion of working
commands. This document is the living answer to "which commands exist": the
surface is exactly what has a named consumer, and growing it means amending this
enumeration FIRST.

## The demand rule

A command family is in the surface iff a shipped consumer instructs its use. The
demand ledger is not opinion — it is greppable: the engineering kungfu's kernels
and skills, the substrate's own smoke drivers, and the operator ceremonies. Every
family below cites its demand. A verb nothing references is not shipped, however
cheap. (Same demand-first rule as rails F2(b) and the removed artifacts time
filter.)

## The v1 surface (families, with their demand)

Agent-facing (demanded by the shipped engineering-kungfu kernels/skills):
- **wake / cancel-wake** — comms-clock correspondence (kungfu: 24+ references).
- **attest / attests** — progress, completion, surrender, verdicts; reading an
  assignment's attest history (kungfu: 26 references; the flagship rail's
  vocabulary).
- **assign / assignments / dispatch / revoke-assignment** — commissioning,
  reading, and revoking work when the existing assignment handler authorizes
  the caller (kungfu: 14 references; feature-cycle skill;
  effort-without-effect-checkin-v1 §5).
- **effort-rule** — parent adjudication of an effort-without-effect request,
  limited to `continue|dismiss` (effort-without-effect-checkin-v1 §5).
- **decision-requests** — read the decision requests visible to the caller so
  an effort request can be selected for `effort-rule`
  (effort-without-effect-checkin-v1 §5).
- **work-item-create / work-item-get / work-item-trace** — the durable work
  thread and its pinned forensic query (kungfu: feature-cycle, work-tracking;
  job-trace-observability-v1).
- **transcript** — read a session's client-visible conversation from the
  substrate's own rows, by `--session <key>` (retrieval) or `--name
  <displayName>` (lookup returning candidates to choose from, never content),
  with tail-by-default and `--before`/`--after` cursors the previous response
  handed the caller (transcript-verb-v1).
- **spawn / retire / list** — session lifecycle and orientation (kungfu:
  operating manual, recon-lifecycle).
- **org-fault (show / impact-list / impact-link / impact-clear)** — read the one
  shared configured-harness fault and link or clear affected assignments
  through the versioned typed seam (configured-harness-org-fault-v1
  Architecture §§5, 7, 8). `show` is a direct REST read of
  `/api/org-faults/:faultId`. `impact-list <assignmentId>` is a direct REST read
  of `/api/assignments/:assignmentId/org-fault-impacts` under the parent
  assignment grant. The two remaining impact actions are dispatch writes.
- **skill (list / put / rm)** — org skill management (kungfu: operating manual).
- **artifacts (record / list)** — the artifact record and its two filters,
  work-item and session exactly (artifacts-and-reconciliation §1/§4; smoke
  coverage practice).
- **config (get / set)** — org settings incl. default-archetype
  (kungfu-template-v1 root-archetype apply; feature smoke drives it).

Operator-facing (demanded by operating ceremonies and the smoke):
- **kungfu-list** — enumerate the kungfu bundles this build ships, with each bundle's
  declared `purpose` and `root_archetype`. Demand: the seeded onboarding agent reads it to
  know what is available and what each bundle is FOR, so it can offer one when a user
  describes a capability it provides (neutral-seed-v1; kungfu-template-v1 manifest
  purpose). Ratified by Flynn 2026-08-01. It replaced an earlier draft that discovered
  bundles by triggering the unknown-bundle REFUSAL and reading the list out of the error
  message — an error path used as an API.
- **doctor** — install/health check (bundle operating manual).
- **assimilate** — host assimilation ceremony. RULED INTENDED (Flynn, 2026-07-25):
  assimilation installs adapter support for ALL registered harnesses on the target
  machine regardless of any single-harness selection — machines are kept fully
  provisioned because operators add/remove harnesses per machine after the fact.
  Bound: this holds while per-harness support stays small (today: two npm packages,
  megabytes); if a future harness's footprint is large, re-open the ruling.
- **run-smoke / run-tests** — producer verbs the rails' remedies dispatch
  (p3-observables-producers-v1; referenced by kungfu skills).

Substrate-internal (not agent surface, routed before the parser):
- **rail-exec / contain-exec** — the contained executors (rails-mechanism P4,
  containment-impl). Intercepted in main.rs ahead of `args::parse`; they never
  appear in HELP and are not part of the agent surface contract.

NOT in v1 (no consumer references them; they return when something does, by
amending this spec first): probe, condition, escalation/waiver commands,
critical, adjudicate, producer-management commands, cli-side init.

## Invariants carried forward from the port era (living qualities, not port rules)

1. **WIRE-FAITHFUL:** commands produce the gateway's canonical dispatch bodies
   (verb strings, camelCase param keys, typed target fields, identity fields
   as/asUser/asProcess). Byte-pinned by the CLI test suite.
2. **THIN STAYS THIN:** no retries, no caching, no state beyond the existing
   discovery chain; minimal dependencies.
3. **UX:** JSON result on stdout, human error on stderr, exit 0/1; HELP
   enumerates exactly this surface.
4. Gates: `cargo build --release`, `cargo test`, `cargo clippy -- -D warnings`
   clean, and the repo's `mix` suite green.

## Identity resolution

Identity resolution is session-first. With no explicit identity flag, the CLI
walks up from cwd for `.tightbeam-session`; when found, its token is the
principal and the dispatch body carries no `as`, `asUser`, or `asProcess`
override. An explicit `--as`, `--as-user`, or `--as-process` flag overrides
origin selection while the discovered session token remains the proved
principal. If no flag and no walk-up session file exist, the CLI fails locally
with a helpful identity/discovery error.

`session-tokens-v1` owns the discovery mechanics, including walk-up location,
malformed-file behavior, and precedence over environment and `gateway.json`.
The unconditional `identity required` behavior inherited from the retired Rust
port spec is a fossil and has no authority over this living contract (Flynn
ruling, 2026-07-25).

## Amendment duty

Adding a command = adding its family here WITH its named consumer, then
implementing. Removing one = removing its last consumer first. A spec whose
mission completes (as the port spec's did) is retired to archive/, not left
in force.
