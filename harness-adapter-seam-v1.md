# Harness adapter seam — v1

Status: READY (gate-cleared 2026-07-25, Sol-high round 10: zero blocking; trajectory
8→7→6→3→2→4→1→1→1→0 across ten rounds). r10 supersedes r9 after its NOT-READY(1)
gate (sole finding: the emission-closures merge `5ae730c` landed mid-gate and added the
credential-transition capture/publish path — `harness_for_provider` enumeration — as an
uncovered seam site; folded below). r9 fixed the help fallback (`tightbeam doctor`).
Prior: NOT-READY(4) at r7
(rounds: 8→7→6→3→2→4 — r7's regression came from the markers merge landing mid-review).
r8: harvest/inject prose contradiction removed; exemption widened to ceremony-execution
literals (home writes still banned); Rust help acceptance is negative as well as
positive across all three embedded-name sites; NEW `classify_subagent_event` callback
owns the markers merge's harness-private envelope decode, with its DDL CHECK added to
the persisted-enum inventory.
Ground truth: main `5ae730c` (post markers + emission-closures merges) — the
served-identity merge moved skills
materialization to the session cwd (`identity.ex`), landed guidance delivery through ACP
`_meta` (`adapter.ex session_meta/2` + `codex_acp_patch.ex`), and gave `account/updated`
a live consumer. r2's inventory (69 sites / 16 files) predates that merge; the impl
re-derives the inventory from THIS main as its first deliverable (§Coverage).

## The defect

Call sites ask *which harness is this* and then assemble harness-specific behavior inline:

```elixir
home_env = if harness == :codex, do: "CODEX_HOME", else: "CLAUDE_CONFIG_DIR"
adapter  = if harness == :codex, do: "codex-acp", else: "claude-agent-acp"
```

Two consequences. First, `else` means "everything that is not codex is claude": a third
harness is silently misrouted, not rejected. Second — the deeper defect — **the call site
encodes harness shape**: that a home is an env var, that rails are a file. A harness that
configures differently cannot be expressed no matter how the branch is written.

Current main measures: 5 `if`-style branches, ~20 `case harness` dispatches, 11 hardcoded
harness lists across lib/ and cli/src/. The counts move; the shape is the defect.

## The seam

Call sites state intent. The harness implementation performs it and owns its own constants.

`Tightbeam.Harness` is a **behaviour**, implemented by `Tightbeam.Harness.Codex` and
`Tightbeam.Harness.Claude`. Every harness-specific literal — env var names, filenames,
binary and package names, credential paths, ACP `_meta` shapes, containment additions —
is **private to the implementing module**. No struct of fields; a field table is this
defect one level up. **Harness modules are stateless, not pure**: callbacks perform
filesystem, process, network, and credential EFFECTS — stateless means no retained
process/global state, no harness-specific supervised service, and every dependency or
mutable context arriving as an argument (r3 gate F12). A harness needing its own
long-lived supervised service is out of scope for v1 and requires a spec amendment, not
a workaround (r2 gate, classification D).

### Callbacks — named for intent, grounded in a current call site

Each callback exists because a production site needs it TODAY; none is speculative. The
r2 gate's coverage failures are folded in: launch is ONE operation owning serialization,
session configuration and credential readiness are first-class, and every callback names
its consuming site class.

Callbacks that touch a placement machine take a **`target`** first argument — the
local/SSH runner context (host, ssh spec, staging/rsync executor) — so satellite behavior
lives INSIDE the harness module, not assembled in Placement (r3 F5: remote skill
projection and remote home reconciliation do staging, remote deletion, git-exclude
reconciliation, SSH and rsync today; leaving that assembly at the call site retains
harness paths there and breaks the single-writer invariant). The runner primitives
(run/copy/stage) are substrate-owned and harness-agnostic; WHAT to run and WHICH paths
to touch are the harness's.

- `prepare_launch(target, home_path, opts)` — the COMPLETE launch recipe for this
  harness's adapter on a target: environment (home env var, credential injection,
  `CODEX_CONFIG` seeding), adapter invocation (binary resolution, shim policy, remote
  package name), and **local-vs-remote serialization** — for a satellite the harness
  module renders the second-shell command string with its own quoting and on-satellite
  token expansion (r2 F1: `launch_env`/`adapter_command` split an indivisible operation;
  placement's remote path proves the env cannot be an ordinary map handed back to the
  caller). Returns an executable launch plan, not parts for the caller to assemble.
- `ensure_adapter(target)` — adapter readiness (r3 F7), PRESERVING today's per-arm
  behavior (r4 F5): LOCAL = locate the ACP adapter, apply the harness's vendored patch,
  REFUSE readiness when the adapter is absent (no local install — today's behavior);
  REMOTE = when the requested adapter is absent, trigger the substrate's combined
  install (below), then re-check the REQUESTED executable and patch.
  **Remote install is a REGISTRY-WIDE substrate operation, not per-module** (r5 A2 —
  current behavior installs BOTH packages in one npm invocation and
  `spinup_test.exs` asserts that package-set): harness-agnostic `Spinup` code asks
  EVERY registry harness for its install contribution via `install_package()` (a
  private-literal-rendering callback — each module renders only its own package
  string) and combines them into ONE install operation, exactly today's observable
  package-set semantics. No package descriptor leaks: the combiner never inspects the
  strings, it concatenates them. `prepare_launch` may assume `ensure_adapter` has
  succeeded; spinup calls them in that order.
- `session_config(session, guidance)` — everything harness-shaped that enters ACP
  session creation/resume: the `_meta` guidance carrier (codex `developerInstructions`;
  claude `systemPrompt` preset-append — today's `session_meta/2`), permission mode, and
  effort encoding. Grounded: `adapter.ex` session paths.
- `reconcile_home(target, home_path, desired)` — the SINGLE writer for every
  Tight-Beam-owned artifact in this harness's home. `desired` carries rails and
  auth-link intent together, because artifacts can compose into ONE file write (r2 F3:
  two independent callbacks racing one file is spec-level corruption). The owned set is
  enumerated in §Home ownership — re-derived from post-r5 main, r3 F4. Harness-owned
  durable state survives byte-identical, locally and on satellites.
- `materialize_skills(target, cwd, snapshot)` — place elected skills where this harness
  discovers them **at the session cwd** under the reserved `tightbeam__*` namespace
  (post-r5 `identity.ex materialize!/3`), including the satellite arm (staging, remote
  delete of stale reserved entries, git-exclude reconciliation — today in Placement).
- `credential_ready?(target, home_path)` / `harvest_credential(target, home_path)` —
  readiness probing (spinup's checks) and rotation harvest. `harvest_credential`
  RETURNS the harvested bytes (or none) to the caller — the provider store decides
  where they land; the harness module only knows which home entry may hold rotated
  durable content (r6 A1: no resolved-credential argument exists on harvest — that
  language applied to `prepare_launch` injection only). The harvest-before-wipe
  ordering that has bricked a credential once already is preserved. Distinct from
  onboarding; distinct from launch.
  **The store/home literal split (r6 A1):** the credential STORE
  (`auth/<harness>/...` layout, backing filenames, staging paths — `credentials.ex`)
  is PROVIDER mechanics and a NAMED EXEMPTION zone in invariant 1; the HOME-ENTRY
  names (which filename a harness's home links, e.g. its auth entry) are harness
  mechanics — provider code passes the store path as auth-link intent and
  `reconcile_home/3` picks the home filename. Provider code never writes a home path
  directly.
- `probe_cli(target)` — harness CLI discovery/version pinning (placement's
  CODEX_PATH doctrine). Distinct from locating the ACP adapter.
- `containment_additions()` — harness-derived containment grants (containment.ex).
- (Onboarding is NOT a harness callback — r4 F7. Credential ceremonies are
  PROVIDER-owned and stay where they live today: `credentials.ex`, keyed by provider,
  public contract `tightbeam onboard openai|anthropic` UNCHANGED. The harness meets
  credentials only at `prepare_launch` (which takes the resolved credential from the
  caller for injection) and `harvest_credential` (which RETURNS harvested bytes — r7
  F1). A multi-provider harness needs no harness ceremony precisely because the
  ceremony belongs to the provider.)
- `classify_auth_event(event)` — `:terminal | :transient | :unknown`, unknown
  non-terminal. Grounded post-r5: `adapter.ex` consumes `account/updated.authMode`
  (r2 F1 called this unspecced; it no longer is).
- `classify_subagent_event(update)` — decode this harness's PRIVATE `_meta`/envelope
  shape for subagent activity into `{:subagent_start | :subagent_stop, refs} | :skip`
  (r7 F4: the markers merge landed `SubagentMarkers.classify/2`, which dispatches on
  harness identity and decodes harness-private shapes — a seam site that existed
  before this spec's implementation and moves behind the behaviour like every other).
  Semantics per `subagent-markers-v1.md` (pinned envelopes, termination carriers);
  parity acceptance covers both harnesses' classification fixtures.
- `fetch_catalog(state)` — provider transport + parsing + capability hydration for this
  harness's model inventory (codex: home cache file; claude: `/v1/models`). Cohesive,
  not a god-function (r2 gate, classification A). Deliberately has NO target argument:
  the catalog is org-level and refreshes only on the gateway machine (r4 F4 — the
  target rule covers callbacks that touch a PLACEMENT machine; this one never does).

### Queryable attributes

`id`, `wire_name`, and `credential_provider`. The last resolves r5 A1's contradiction by
separating two concepts that were being conflated:

- **Billing/model provenance** is the CATALOG ENTRY's `provider` field (r2 F4 stands):
  `fetch_catalog` stamps it; spawn, tune, schema generation, and model-to-harness
  inference take provider from the selected entry. Today's `model_catalog.ex`
  `provider/1` harness map collapses into the entry stamp.
- **Credential consumption** is `credential_provider` — WHICH provider's credential this
  harness consumes, **1:1 in v1** (claude→anthropic, codex→openai). This is what
  onboarding completion uses to find affected harnesses (relink each harness where
  `credential_provider == provider`, THROUGH `reconcile_home/3` — today's direct
  `relink_home_entry!` home write in `credentials.ex` moves behind the single writer),
  what provider-runtime stop/start iterates on, what the credential-transition
  CAPTURE path enumerates (the emission closures' capture of affected sessions —
  today's `harness_for_provider()` map — becomes registry enumeration of every harness
  whose `credential_provider == provider`), and why
  `credential_ready?(target, home_path)` needs no extra argument (the module knows its
  own provider). Spawn's credential-check-before-catalog-resolution ordering is
  UNCHANGED — readiness is per-harness, not per-entry.

**A multi-provider harness is OUT of v1** (r5 A1): it would need per-entry credential
resolution and is a spec amendment when a real one arrives, not a v1 abstraction. The
catalog/billing side is already entry-shaped, so that future costs one attribute
migration, not a redesign.

### Registry

`Harness.all/0` is the single home of the harness list, replacing every hardcoded
`[:claude, :codex]`. `Harness.parse!/1` converts a wire string, **raising** on unknown —
no default-to-claude path. **Registry order is the default order**: `Harness.default/0`
returns the configured default harness (from product config — `application.ex` /
runtime env), falling back to the first registry entry; the doctor task and any
default-model policy read product configuration, not harness mechanics (r2 F6).
Startup iterates `Harness.all/0`; the current claude-before-codex sweep order is
preserved by registry order until a test proves it immaterial (§Care sites).

## The parity invariant (Flynn ruling, 2026-07-25 — LAW, active after migration; amendment gate-cleared r3, 4→2→0)

**Parity on EVERYTHING between registered harnesses is an invariant of the system.**
Every capability the substrate offers is either (a) parity-complete across every
registered harness, or (b) carries a NAMED divergence row in `harness-support.md`
with the blocker stated and a NEGATIVE test proving the divergent behavior — silence
is never a legal third state. Everywhere code touches a harness it goes through the
polymorphic interface; the interface supports N harnesses, never two; and the
interfaces are BUNDLED so that adding harness #3 has exactly one satisfaction
surface (below). The smoke matrix (one full leg per registered harness) is this
invariant's end-to-end enforcement; the per-harness conformance suite (below) is
its unit-level enforcement.

**Migration gate (r2 F3 — the law ACTIVATES only when these complete; until then its
status is RATIFIED-PENDING-MIGRATION, because the current tree contains violations the
law must not bless):** (1) a CLOSED capability-ID census over `harness-support.md` —
every capability gets a stable ID, and every {capability × registered harness} cell
gets a status + proof reference; the matrix's current unverified-claim allowance is
REVOKED at census completion; (2) the known silent divergences are named and
negative-tested — model selection, claude compaction visibility (and codex's unknown
end-to-end status resolved), and auth-event classification (claude's always-:unknown
vs codex's terminal/transient — today an UNLISTED divergence); (3) the shipped
`tightbeam-harnesses` skill is reconciled with the canonical matrix (it currently
contradicts it on slash commands and compaction); (4) `feature_smoke` becomes
registry-driven — one leg per registered harness from `Harness.all/0`, not a
default-harness run.

## Adding a harness — the bundle

**Scope (r2 F1, closed per r3): this bundle is additive-complete for a harness
consuming an ALREADY-SUPPORTED credential provider.** A harness bringing a NEW
provider also requires the companion PROVIDER-INTEGRATION bundle, whose membership is
SCAN-CLOSED rather than hand-listed (the invariant-1 trick): a second checked-in scan
finds every provider-literal consumer (`:openai|:anthropic|"openai"|"anthropic"`)
outside the provider zone — today that includes `credentials.ex`, the gateway's
provider parser, the CLI provider surface (`args.rs`, ceremonies), store layout,
preflight rows, and `feature_smoke`'s provider list — and the bundle is defined as
"every site the scan reports, plus an ADDITIVITY TEST proving a fixture provider
onboards end-to-end with edits only inside the scan's reported sites." A consumer the
scan misses is a scan-pattern bug, not a spec gap.

The obligation set is enumerated in ONE checked-in MACHINE-READABLE manifest
(`priv/harness_bundle.json`, stable obligation IDs — r2 F4); this section and
`Tightbeam.Harness`'s moduledoc both RENDER that manifest, and a test asserts the
moduledoc's obligation-ID set equals the manifest's exactly (content equality on IDs,
not a count — the spec text stays review-enforced prose). A new harness ships:

1. **The behaviour module + conformance vectors** — every `Tightbeam.Harness`
   callback implemented, PLUS the standardized `conformance_vectors()` provider
   (r2 F2, contract pinned r3). The vector CONTRACT is part of the machine-readable
   manifest: for EVERY callback it names the required cases and the observable
   ORACLE the shared suite asserts — not return shapes:
   `prepare_launch` — local + remote × railed + lawless vectors; oracle = the
   rendered plan's env/argv/serialized command against the vector's expected form.
   `ensure_adapter` — present/absent × local/remote vectors with a fake bundle +
   anchors; oracle = refusal (local-absent), install-contribution string, patched
   bundle bytes + preserved mode.
   `session_config` — one session vector; oracle = the exact `_meta` map.
   `reconcile_home` — a sentinel-seeded home vector + desired set; oracle = observed
   write-set equals the vector's expected write-set, sentinels byte-identical
   outside it (the behavioral preservation oracle, §Home ownership).
   `materialize_skills` — snapshot vector; oracle = expected cwd entries under the
   reserved namespace.
   `credential_ready?`/`harvest_credential` — present/absent/rotated vectors;
   oracle = boolean + harvested bytes.
   `credential_live?(target, home_path, opts)` — AMENDMENT 2026-07-26 r2 (task #15;
   obligation ID **HB-08**, capability-matrix ID **CAP-018**; field evidence: sat-e2e
   lnx-0725b — present codex store, dead grant, login-status masquerade; SMOKE.md
   documents the claude twin). Target-shaped like the sibling credential callbacks
   (harness.ex typing conventions); transport and timeout are INJECTED via opts
   (`:transport`, `:timeout_ms` — bounded, default pinned by the manifest entry). A
   REAL liveness probe: the cheapest harness-native call requiring a VALID grant
   (never a status/presence read), returning
   {:live | {:dead, reason} | {:unknown, reason}}; timeout maps to
   {:unknown, :timeout}. Vectors take RAW injected-transport results (recorded real
   response shapes for the live/dead fixtures — not mock-invented replies, per the
   mock-divergence law): authenticated success → :live; explicit rejection/
   revocation → {:dead, reason}; timeout AND transient transport failure (DNS/TLS/
   5xx) → {:unknown, reason} with the timeout case asserting BOUNDED elapsed time +
   cleanup; a transport with no cheap authenticated probe → {:unknown, reason} as a
   named-divergence row. The permanent fixture harness implements the callback with
   vectors. CONSUMER MAPPING, pinned: :live → pass; :dead → fail; :unknown →
   INCOMPLETE/blocker — NEVER pass. V1 consumer scope: the three e2e preflight
   surfaces ONLY (SMOKE P1/P2, client-e2e P-rows, satellite-e2e S2 preflight);
   production readiness paths (spinup credential_ready?, gateway credential_status)
   deliberately keep presence semantics in v1 — their adoption is a named follow-up
   decision, not smuggled. This is the THIRD intentional behavior change under this
   spec's acceptance (amending the two-changes sentence accordingly).
   `probe_cli` — a fake CLI vector; oracle = pinned version/path decision.
   `containment_additions` — oracle = exact grant list.
   `classify_auth_event`/`classify_subagent_event` — positive AND negative envelope
   vectors; oracle = exact classification (a harness with no positive envelope
   ships the named-divergence row instead — the vector contract records that as an
   explicit `unsupported` case, never silence).
   `fetch_catalog` — valid + malformed + unavailable source vectors (injected
   transport); oracle = entries with provider stamps / exact error.
   `wire_projection` — oracle = decoded fields round-trip the manifest's field
   list.
   A harness supplies vectors for every case or a named divergence; the shared
   suite contains zero harness branches.
   **CLOSURE AMENDMENT 2026-07-26 (found live: install_cli_projection landed with
   zero conformance coverage and the suite stayed green):** the law is closed at
   BOTH ends — the manifest-equality test (moduledoc ↔ manifest IDs) AND a
   behaviour-closure test: `Tightbeam.Harness.behaviour_info(:callbacks)` minus a
   CONSTANT-ACCESSOR ALLOWLIST (declared IN the manifest — id, wire_name,
   credential_provider, install_package, conformance_vectors — reviewable, not
   hardcoded in the test) must be a subset of the vector_contract keys. A new
   behavioural callback without vectors fails the suite BY CONSTRUCTION.
   `install_cli_projection` itself joins the contract: required cases creates /
   already-exists-skip / self-resolved-skip; oracle = observed filesystem effect
   (shim present+executable / untouched); per-harness vectors incl the fixture
   harness (claude no-op is a named vector, not silence).
2. **One registry entry** (`Harness.all/0`) — and nothing else in Elixir (the seam
   test proves zero edits elsewhere).
3. **A vendored ACP adapter** (or upstream equivalent) plus its pinned-version
   patch set where the wire lacks required carriers (guidance `_meta`,
   auth events, subagent termination — the patch mechanism and anchors live in the
   harness module).
4. **A catalog source AND its bootstrap** (`fetch_catalog` stamping provider per
   entry, plus the provisioning path for cache-backed sources — codex's
   `:missing_cache` today requires manual seeding; a new harness names how its
   catalog becomes ready, and the doctor/preflight row that checks it).
5. **A `harness-support.md` row per capability** — parity claimed or divergence
   named with its negative test — AND the shipped `tightbeam-harnesses` skill
   updated in the same change (the skill mirrors the matrix; drift between them is
   a violation).
6. **Smoke-leg entry with provisioning** — the harness becomes a leg of the
   SMOKE.md matrix and the registry-driven feature-smoke run, including its
   credential preflight, catalog readiness, compatible default model, and any
   timing assumptions (horizon envs) the leg needs.
7. **The per-harness CONFORMANCE SUITE green** — one shared, parameterized test
   module that runs the same contract assertions against EVERY registered harness
   (the generalization of the fixture-harness acceptance): each callback exercised,
   parity tests executed per harness, divergences asserted negative. The fixture
   harness runs it too, permanently, as the additivity sentinel.

## Invariants

1. **No harness-specific literal in production implementation code outside
   `Tightbeam.Harness.*`** (and the Rust boundary, §Cross-language). Scope (r2 F6 —
   executable, with carve-outs): the prohibition covers hard-coded harness mechanics in
   `lib/` production modules. It does NOT cover: values flowing at runtime from the
   registry into logs/API payloads/persisted rows; test files asserting expected
   literals as parity oracles; fixtures; documentation. The greppable form: an
   allowlist-scoped scan of `lib/` excluding `lib/tightbeam/harness/` AND the
   provider-ceremony exemption zone (`credentials.ex` — store-layout AND
   ceremony-execution literals, r7 F2: running a provider's guided ceremony
   necessarily names the harness env/paths/binaries it onboards for, e.g. the codex
   device-code flow's `CODEX_HOME`/`auth.json` staging; these are ceremony mechanics,
   not call-site dispatch). The exemption does NOT cover home WRITES — `credentials.ex`
   home-side writes flow through `reconcile_home/3` and the scan still fails on any
   home-path write outside it. Scan patterns:
   `CODEX_HOME|CLAUDE_CONFIG_DIR|codex-acp|claude-agent-acp|auth\.json|oauth-token|
   settings\.json|hooks\.json` and kin; the exact pattern set is a checked-in script,
   not prose.
2. **No `if`/`case` on harness identity outside `Tightbeam.Harness.*`.** Dispatch is via
   the behaviour.
3. **Unknown harness raises** at the parse boundary.
4. **The harness list has one home** (`Harness.all/0`).
5. **Adding a harness is additive in Elixir**: one module plus one registry entry (Rust
   boundary: §Cross-language).
6. **One writer per home artifact**: all Tight-Beam-owned writes to a given file flow
   through `reconcile_home/3` with a declared merge order (r2 F3).

## Home ownership

Owned by r5 (`served-identity-home-projection-v1.md` §12): regeneration replaces only
Tight-Beam-owned paths; harness-owned durable state survives byte-identical. The owned
set, PER CURRENT MAIN (`homes.ex` moduledoc and projection; r3 F4 killed r2's stale
list): the credential entry (store-backed link; the BACKING content is durable and
harvested before replacement), the harness rails artifact, `.tightbeam/` (including
`.tightbeam/manifest`), and the substrate BASELINE skill links (projected separately
from org identity, never sourced from the org-editable library). NOT in the home and
NOT owned here: elected skills (session-cwd material via `materialize_skills`),
guidance (delivered via `session_config`, not a file), any model pin (none exists in
the current shared projection — rails is the only spec field). Anything not enumerated
is harness-owned and untouchable. **The preservation test is BEHAVIORAL, not
declaration-driven** (r4 F2 — a declaration would need a new queryable surface): seed
the home with sentinel files everywhere plausible, run `reconcile_home`, and assert
every sentinel survives byte-identical OUTSIDE the paths the reconcile observably
wrote; the observed write-set must equal this section's enumeration. No declaration
callback exists; the enumeration lives here and in the test's expectations. If a
future artifact joins the projection it joins this list and the test in the same
change.

## Cross-language seam — the Rust CLI (DECIDED: option a, offline-capable)

The CLI obtains everything harness-shaped **from the substrate**; Rust holds no harness
list (r2 F5 — option (b) required a Rust edit per harness, contradicting invariant 5).

**Transport preserves the offline doctor (r4 F6):** the gateway PERSISTS the projection
to `harnesses.json` beside `gateway.json` at every boot, and `GET /harnesses` serves the
same bytes live. The CLI reads the FILE first (works with no gateway running — today's
`tightbeam doctor` behavior), falling back to the route; when neither exists (gateway
never booted here) the doctor reports what it can and says exactly why the harness
checks are unavailable. Rust still embeds nothing.

**The projection surface (r3 F8, hardened per r4 F8, consumer inventory per r5 A3):**
each harness module implements `wire_projection() :: binary()` (normalized at the
boundary — r5 C1) returning **pre-encoded opaque bytes** carrying id, wire_name,
adapter install package, and adapter process markers (what `probe.rs` matches in
process listings). NOT ceremony descriptors — onboarding is provider-owned (§Callbacks;
r4 F7) and its CLI surface is untouched. The **sole Elixir consumers** are the boundary
serializer (the route + the boot-time file write); an enforcement test asserts, over
the codebase, that `wire_projection` has exactly those call sites and that no Elixir
module reads decoded projection keys (grep/AST-level, checked in beside the literal
scan). This is a wire projection a non-BEAM process consumes — never a descriptor table
an Elixir call site dispatches on; opacity plus the call-site test is what keeps r1's
rejected pattern closed (r4 F8).
**Rust consumers — the COMPLETE inventory (r5 A3 + r6 A2 + r7 F3):** `args.rs`
(harness argument validation, the `claude,codex` default list, AND the HELP TEXT —
three embedded-name sites: two list-bearing help strings plus the `codex` spawn
example), `probe.rs` (process markers), and `ceremonies.rs` **assimilation**
(closed-world harness validation + both adapter package literals — the
install-package field's named consumer). All replace their embedded lists/literals
with the fetched projection. Help text renders harness names and examples from the
projection when one is available and otherwise prints a neutral pointer to the
EXISTING surface — `tightbeam doctor`, which already reports harness/adapter state
and consumes the same persisted projection (r8 F1: no new command; the prior "see
tightbeam harnesses" named a command that does not exist) — it never embeds names. Acceptance is NEGATIVE as well as
positive (r7 F3): the fixture test asserts help output contains NO harness name
absent from the supplied projection (a grep over rendered help against the projection
set), in addition to the fixture name appearing, across argument validation,
defaulting, assimilation provisioning, and help rendering. A conformance test asserts
the projection round-trips every field Rust consumes.

## Sites requiring care — mechanical substitution is NOT behaviour-preserving

The care LIST below names site CLASSES; exact line anchors are RE-DERIVED from the
implementation base SHA as part of the §Coverage table (r3 F10: r2/r3 anchors drifted
across two merges; anchors in a spec rot, classes do not). Each class needs its
before/after stated explicitly and a parity test:

- Probe provisioning (placement) — probe-directory destruction, `CODEX_CONFIG` seeding,
  probe-model selection, ACP boot attestation. Not a boolean.
- Launch environment assembly (placement, local + remote arms) — folds into
  `prepare_launch` whole.
- Shared-home artifact write (placement/homes) — per-harness outcomes differ (rails
  merge vs standalone artifact vs NO file); a naive rewrite creates an empty rails file.
  Current shared projection carries RAILS ONLY (no model pin — r3 F10 corrected r2).
- Auth ordering (homes) — preserve `harvest_auth_back → wipe → write → relink`;
  boot-wide auth sweeps precede any adapter or home projection. Wipe-before-harvest has
  shipped once.
- Remote home reconciliation (placement) — current behavior ALREADY preserves and
  harvests (r3 F10 corrected r2's rm-rf claim); the refactor owes PARITY, not a new
  behavior. Remote-preservation parity test required.
- Harness switching (gateway) — preserve the validate → readiness → deliver home →
  persist → history-barrier order; persisting earlier strands a session on an
  unavailable harness.
- Model inference (gateway) — preserve zero/one/multiple-match semantics iterating the
  registry; provider comes from the selected catalog entry (F4).
- Startup (gateway) — the all-harness auth-sweep barrier completes before
  `AdapterCoordinator` starts; sweep order follows the registry.
- Remote spinup (spinup) — reinstall then re-check the REQUESTED adapter binary before
  reporting ready (now owned by `ensure_adapter`).
- **Credential-transition capture/publication (gateway — r9's addition, landed in
  `5ae730c`):** the two-stage park/re-onboard emission enumerates affected sessions by
  provider→harness mapping; under the seam this becomes registry enumeration on
  `credential_provider`, PRESERVING immutable pre-park/pre-resume capture and
  post-success publication exactly as landed. Parity test required.
- **ACP session lifecycle (adapter — r3 F10's addition):** the harness `_meta` preset
  divergence between session NEW and LOAD, strict effort application and its rollback
  on failure, contained-vs-uncontained failure handling, and the gate-attestation
  session path. All flow through `session_config`/adapter parity tests: new, load, gate
  attestation, effort apply/rollback, contained and uncontained.

## Coverage — the inventory is the checklist

First implementation deliverable: re-derive the site inventory from current main (the
r2 counts are stale) and check in a coverage table mapping every site to its seam
operation (or to "registry", "persisted enum", "test oracle", "docs" per the invariant-1
carve-outs). The table is the review artifact for the implementation PR; a site absent
from the table is a finding, not an oversight (r2 F1).

## Acceptance

- **The literal test** (scoped per invariant 1): the checked-in scan script passes on
  the refactored tree and fails when any listed literal is reintroduced into scoped
  production code.
- **The seam test**: a fixture third harness is added as one module plus one registry
  entry, with zero edits to `placement.ex`, `gateway.ex`, `homes.ex`, `spinup.ex`, the
  mix tasks, or the schema — it spawns, tunes, fetches a catalog, reconciles a home, and
  creates an ACP session — **and the FULL existing test suite passes with the fixture
  registered** (r2 F8). The three closed-world tests the gate identified
  (`archetypes_test.exs:562` exact two-name message, `gateway_test.exs:638` two-clause
  probe, `tightbeam_doctor_test.exs:29` two-inventory catalog) are refactored to
  registry-driven form as part of this spec's implementation. The fixture must be
  selectable through the runtime/default configuration path (r3 F9), not only via
  explicit spawn params.
- `Harness.parse!("opencode")` raises; nothing defaults to `:claude`.
- The fixture third harness also proves credential-transition scoping: sessions whose
  harness has `credential_provider == provider` are captured/published on terminal and
  re-onboard transitions; nonmatching sessions are excluded (r9 gate closure).
- Behaviour-parity tests: railed and lawless codex, railed and lawless claude, local and
  remote token injection, unchanged-home preservation, rotated-credential
  harvest-before-wipe, REMOTE home preservation (parity with current behavior),
  harness-switch ordering, model-inference match semantics, and the ACP lifecycle set
  (new, load, gate attestation, effort apply/rollback, contained/uncontained).
- Existing behaviour unchanged for both harnesses EXCEPT two named intentional changes:
  unknown harness raises (was: became claude); provider is read from catalog entries
  (same values today, different authority).

## Not blocking

The persisted enums (`org.ex` SQLite `CHECK`; `subagent_markers` DDL harness `CHECK`
added by the markers merge — r7 F4) are sites, not risks: greenfield, the
database may be deleted and recreated. **`config/runtime.exs` is NOT exempt** (r3 F9):
its harness parsing is a live closed-world parser — it hardcodes the two names and
cannot accept a third, so it goes through `Harness.parse!/1` like every other boundary,
and the fixture-harness seam test must select the fixture through the runtime/default
configuration path (not only via explicit spawn params) to prove the whole default
chain is registry-driven.
