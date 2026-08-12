# Work plan: pre-Gibson blockers and the queue behind them

Status: ACTIVE. Decisions here were ruled by Flynn 2026-08-03 (in-session, recorded per
item). Mechanisms come from three Fable design reviews run the same day; every cause
below is LOCATED (file:line, verified against a live database or reproduced), not
inferred. Executors: follow your lane's brief exactly; where this plan and code comments
disagree, this plan is newer and wins, and say so in your report.

Standing discipline for every lane, no exceptions:
- Verify RED before claiming a fix: break the mechanism, watch your test fail for its
  stated reason, restore. State what you broke. A test whose reach you did not prove is
  a false receipt.
- ASSERT THE BREAK APPLIED. Three authors in one day produced the same failure: a patch
  or revert that silently no-ops leaves a green suite, and green is indistinguishable
  from covered (a commit claiming tests never added; a reviewer green over a live bug by
  seed luck; a RED check whose string-replace matched nothing). The form that works:
  re-run every RED check with the revert ASSERTED to have applied — check the diff is
  non-empty, check the count moved — before reading the suite's colour at all.
- Verify test COUNT, not suite colour — a patch that silently fails to apply leaves
  green, and green is indistinguishable from covered.
- Gates: `mix test` AND `cargo test`, zero failures, on eezo AND shrdlu (all platforms
  are the gate). Formatting by stash-and-compare parity, never by formatting files you
  did not touch.
- Review: distinct Codex GPT-5.6-SOL reviewer at high reasoning per lane. Author fixes
  findings, never reviews own work. No verdict = failed gate.
- DIFF SCOPE FOR REVIEW IS `git diff $(git merge-base main HEAD)..HEAD`, never
  `main..HEAD`. On a branch created before main's current tip, `main..HEAD` renders
  MAIN'S OWN later commits as apparent reversions by the branch, and a reviewer will
  correctly report them as blocking findings. Cost this once: G6's review BLOCKed on a
  doc "revert" the branch never made (it touched zero doc files). The reviewer was right
  given what it was shown; the brief was wrong.
- A WRITE AND ITS ACCOUNT OF ITSELF MUST NOT BE SEPARATED (lane G1, two findings one
  layer apart). Re-reading the world BEFORE acting on the read is a race
  (sample-then-act); re-reading the world AFTER acting, to describe what you did, is a
  lie waiting for a second actor (a sweep that ages twice re-reads its own error string
  and reports the first batch again). Neither survives the separation. The statement
  that does the work is the only honest source of what it did — fold the cause into the
  UPDATE's predicate, and take the account from UPDATE ... RETURNING.
- Commit messages carry authority: name the finding/ruling a change implements, so a
  diff-only reviewer does not re-raise it as unauthorized (this happened twice tonight).
- No push on a red or unrun gate. Stack, never amend, after anything is reviewed.

---

## PRE-GIBSON (blockers — deploy waits on these)

THE GATE (Flynn ruling 2026-08-03): anything that can make a core loop or core
operation of tightbeam FAIL is pre-Gibson. Not "painful", not "invisible" — FAIL.
Visibility work rides along only when it is cheap (G5 is).

### Lane G1 — turn-delivery integrity (task #15; the only work-loss defect)

Ruling (Flynn): deliver a substrate notice to the target session if it exists; if the
owner has no main session, LOG it — that is an edge case, logs are fine. Never create a
session on demand; never queue to an unverified address.

Mechanism (verified against ~/.tightbeam-soak/state.db — 6/6 orphans are
`process:tightbeam` adjudication notices addressed to `Org.personal_session_key` of a
user with zero sessions rows):
1. `supervision.ex:133` — `ladder_target` falls back to the personal key UNVERIFIED and
   its @spec is `String.t()`, so "nobody" is unrepresentable.
2. `gateway.ex:1032-1046` — `delivery_target` rejects the phantom, then the lineage
   branch re-resolves via the SAME resolver and accepts it unchecked (:1040). The
   `nil -> nil` arm (:1039) is dead code. Sibling `active_personal_target`
   (gateway.ex:1056) verifies correctly; propagate that lesson.
3. `ledger.ex:169-217` — `claim_next` returns `:none` for BOTH "queue empty" and "work
   exists that no one can ever claim".
4. `ledger.ex:384-390` — `pending_sessions` never joins sessions, so LaneManager nudges
   the phantom every 5s forever.

Build, in order:
(a) Guard `Ledger.enqueue_in_txn` (ledger.ex:85) — the single writer every turn passes
    through. Refuse AS A VALUE unless a sessions row EXISTS in the same transaction.
    CORRECTION 2026-08-03: this brief originally said "active sessions row". That was
    wrong and the lane was right to refuse it. escalation-delivery-v1 §targetGate (lines
    67-71) requires decision notifications to deliver UNCONDITIONALLY, "including when
    the target session is held or retired", and states that adding an active-session
    gate would change observable routing — with a proof asserting it. EXISTENCE is the
    correct guard: it closes 100% of the evidence orphans (phantom key, zero rows)
    without touching held/retired routing. The retired case is named after the fact by
    (c) as {:unclaimable, :session_retired}. A work plan is not authority over a live
    spec (a raise would roll back the wake's 'fired' mark). Closes every path
    including the unvalidated gate-less arm at gateway.ex:1017. Callers already carry
    refusal plumbing (`wake_delivery_failed` at wakes.ex:520-532; `:skipped`).
(b) Let `ladder_target` return nil; verify the personal-key fallback the way
    `active_personal_target` does. Undeliverable notice → Logger line naming what could
    not be delivered, to whom, and why (the ruling's log case).
(c) Split `claim_next`'s `:none` into empty vs unclaimable-with-reason; the EXISTING
    LaneManager scan ages unclaimable rows into `failed` with a named error, which rides
    the EXISTING `unpublished_terminals` publication (conspicuous for free). Backstop
    only — after (a) it should never fire. NEVER age `:held` turns; holds are designed
    waiting and healed correctly in the soak (~1.1s).

Do NOT: add a turn status, a process, auto-retry, a "queued-and-owned" split (a lane
owned this key the whole time — ownership was never the missing thing), or touch the
reconciler design (it is correct and not implicated).

Definition of done: 60-minute soak, A1 PASS with its own receipt, plus A2/A4/A5.
A3 SPLITS — its adapter_deaths half fails identically on the PARENT commit (measured:
baseline worktree at dd9cb0b, same {:adapter_deaths, expected: 1, observed: []}), and is
task #14, owned by G5. "VERDICT PASS with A3 unrelaxed" is the gate for the MERGED
G1+G5 result, run by the dispatcher after both land — not a gate G1 can meet alone.
Do not weaken A3. The
soak recipe (env, arena, credential source) is in scripts/soak.exs headers and
docs/smoke-runs/2026-08-03-3441879-post-model-identity.md.

### Lane G2 — placement refuses by name (task #18)

Ruling (Flynn): when NO host in an archetype's `where` can run the requested harness,
spawn REFUSES and names the true cause and remedy. No silent substitution, ever. (A
multi-host `where` picking its second entry is the list working, not substitution.)

Mechanism: `placement.ex:158` and `:211` — `hosts_for(config)[key] || %{ssh: nil, ...}`
turns a hosts-map MISS into "run locally on the gateway". Absence-as-success in the
host dimension. Lines 186, 240, 864, 1119 already use `Map.fetch!` — make 158/211 match.
Then the refusal: when every `where` host is ineligible, deny with cause per host
("eurisko cannot run codex: no credential in its store — run `tightbeam onboard openai`
there"). Reuse the readiness message voice; do not invent prose shape.

Definition of done: the T3a scenario reproduced tonight (eurisko registered, credential
absent) REFUSES with the eurisko-specific cause instead of landing on shrdlu. Red test
first against current behavior.

### Lane G3 — one owner for routability (tasks #12 + the spawn lie; enables G2's prose)

No Flynn ruling needed — this implements T-SOURCE structurally. Direction from the
design review, adopted:

- Lift `harness_for_ref` (gateway.ex:5466, a defp in a 5,813-line module — "THE ONE
  ANSWER", unreachable by its callers) and `unroutable/2` (5493-5516) onto
  `Tightbeam.ModelCatalog` as `route(host, selection)` / `route(host, harness,
  selection)` returning `{:ok, %{harness, provider, entry}} | {:error, %Unroutable{}}`.
  route/2 is a fold over route/3 — one derivation, two quantifiers, no mode flag.
- `%Unroutable{cause, host, harness, selection, health, offered}` with causes
  :no_catalog | :family_absent | :needs_effort | :effort_not_offered | :ambiguous, and
  `Unroutable.message/1` as the one honest sentence. Fold in the no-catalog
  classifications currently duplicated at readiness.ex:188-197 and gateway.ex:3835-3883
  (the client_version arm — "credential is not implicated; upgrade the binary" — exists
  in only one of four mechanisms today; centralizing is how the rest inherit it).
- `{:ok, ...}` carries provider+entry, which deletes `catalog_provider!/3`
  (gateway.ex:5540) and its "entry missing after validation" raise.
- Migrate: adjudication call sites (gateway.ex:4668, 4877), `validate_catalog_model`
  becomes a thin relay, readiness `model_state/3` pattern-matches the cause
  (health not_derived → :unknown row stays caller policy).
- THEN DELETE `ModelCatalog.member?/4` — the cause-eraser whose `present?: false` means
  three different things and which produced the fourth mechanism. Zero callers after
  migration; while it exists, route is advice.

Do NOT: unify readiness's credential/adapter columns (different owners), move
`compose_model_selection`'s pick-a-tier policy (policy, not fact), add a `routable?`
boolean, cache anything, or serialize anything (route is a read of the existing catalog
cache — verify no new process sits on the prompt path; T-CONCURRENCY).

Definition of done: fresh org booted with a tiered default model and no effort reports
"needs an effort (offers low|medium|high...)" — not "not in the live catalog". Verified
both directions on one org (the reproduction recipe is in task #12).

### Lane G4 — renewal under real expiry — DONE 2026-08-03 12:43

Verified against a GENUINELY expired token (2h past expiry, unfakeable): one
catalog-probe run renewed silently, returned HTTP 200 with 11 models, empty stderr, and
rotated .credentials.json in place (expiresAt 10:43 -> 20:43, mtime advanced). The
morning's install-killing scenario now self-heals. Original brief below for the record.

The token-renewal path (f3a00e4) is proven by unit tests and a live manual grant, but
the in-situ path has never fired against a genuinely expired token (needs ~8h idle).
Before Gibson: idle the eezo install past expiry once, run one probe, confirm the 401
never appears and the credential file rotates (mtime + expiresAt advance). If it fails,
the fallback is the stored token and the failure is on stderr — diagnose from there.
This is the difference between a Gibson install that survives its first night and one
that wakes up dead.

### Lane G5 — record-and-notify (P1+P2+#14, promoted because it is cheap)

Not a core-loop failure; promoted because the primitive it needs already exists
(`Projection.append_marker_in_txn` — how `[turn failed]` lands today) so the whole lane
is ~2 days touching files no other lane touches. Build: `EventLog.notice(kind, subject,
detail, audience:)` — always writes the row; audience `{:session, key}` appends the
marker if the session exists, else logs (Flynn's edge-case ruling). Audit all ~40
`EventLog.lifecycle` call sites for audience (the output IS task #20's misfiled list);
convert the important ones; move the adapter_down write outside the stale-:DOWN guard
(#14) so the record is unconditional and only the restart action stays gated. Double-posting guard: one
call owns both effects.

ATTENTION, not a new concept (Flynn rulings 2026-08-03): the noise problem is solved by
the client, not by withholding messages — and the vocabulary ALREADY EXISTS. The agent
elects an attention tier for its replies (`replyAttention`, gateway.ex:4156, tiers
normal|high, surfaced as `attention_tier`). Substrate notices elect attention the same
way — same concept, same author-elects shape, same client consumer. Do NOT invent a
parallel "priority" field; extend attention DOWNWARD with one tier: low|normal|high.
Substrate defaults per kind: ambient info low (clients hide by default), session-
affecting fault normal, needs-a-human high. Mechanically markers need a message-level
attention field (replyAttention lives on turns; markers are not turns) but it carries
the SAME tier vocabulary and surfaces through the SAME `attention_tier` payload key.
Elevation is a NEW higher-attention message referencing the event (records, not
mutations), which is how a hidden low-attention notice "shows up" when something raises
the stakes. Greenfield: no prod DB, column lands without migration. Keep it minimal —
one column, per-kind defaults, no policy engine.

### Lane G6 — unreadable credential store refuses loudly (#13, promoted by the gate)

An unreadable store makes catalog derivation FAIL — the core loop dies with zero
diagnostics (no catalog, no log line; measured symlink-vs-copy on one arena). The
trigger is unusual (normal onboarding writes real files) but Gibson provisioning is
exactly where unusual setups happen, and the failure is total when it fires. Fix:
widen `read_metadata`'s collapses (credentials.ex:677,681,690-694) — absent → empty is
fine; unreadable/corrupt/symlinked → loud refusal naming the path ("report dirt, never
accommodate it"). Then revert the satellite runbook's copy-not-symlink workaround and
re-verify against a symlinked store. Small; can ride with G5.

### Post-merge gate — AMENDED 2026-08-04 after the first combined run

The combined soak + T2b re-run against merged main produced two in-gate findings; the
gate now additionally requires:
3. Lane G7 (parked-adapter deaths recorded) merged and the soak's A3 green with kills
   landing on BOTH adapter states — 6 of 8 idle-adapter kills were unrecorded because
   parked processes die outside the coordinator's monitor; G5 sealed only the monitored
   door.
4. Lane G8 — AMENDED 2026-08-04: row 10's failure was measured and is a TEST defect, not
   a wire defect (oracle asserts B's reply precedes Main's; B's turn simply ran longer).
   Gate requirement is now: G8's repaired oracle merged and row 10 green on BOTH legs,
   with red-before-green proving the row still catches a reordered frame AND a withheld
   one. The ordering defect ConnRegistry documents is real but LATENT with no
   reproduction — post-Gibson, see ordered-publication-proposal-v1.md.
A1 is PROVEN in situ on the merged tree (259 turns, zero orphans) and stays green.

### Post-merge gate (added 2026-08-03, Flynn's question surfaced it)

The tier map's own rule applies to this work: G3 rewrote the readiness/boot prose and G6
rewrote credential-store reading, both "boot/readiness/credential" surfaces, so T0 is
REQUIRED, not optional. The full post-merge gate, run on quiet hardware after all lanes
land:
1. Combined 60-minute soak, VERDICT PASS, A1+A3 unrelaxed (G1+G5's joint oracle).
2. T0 V0 zero-credential half + V2 (harness present, no credential) walked on fresh base
   dirs — the boot prose is all new and T0 judges what a first-run user concludes from
   it. V1 skipped by name (adapter-missing detection untouched; N3 re-proven yesterday).
   V4 skipped by name (ceremony code untouched since yesterday's live exercise).

### Sequencing and independence

G1, G2, G4, G5, G6 are independent — parallel lanes, separate worktrees (shared checkout
collides at commit time even with disjoint edits). G3 touches gateway.ex broadly; run it
AFTER G2's two-line placement fix lands to avoid trampling, or in a worktree rebased
last. G2's refusal PROSE gets richer once G3 lands (route gives it the cause struct),
but do not couple them — G2 ships with hand-written cause text if it is ready first.

---

## POST-GIBSON (queued, decided, not blocking)

- **P1 conspicuousness sweep** (the half of P1 not consumed by G5) — promote the three
  private swallow-but-write copies (wakes.ex:534, supervision.ex:957, gateway.ex:395)
  into `EventLog.best_effort(result, kind, subject)`; sweep the 52 self-declared
  best-effort sites; delete the three privates. After the sweep a naked
  `{:error,_} -> :ok` is a review finding (one grep). Note for context: the Flynn
  rulings G5 implements — important events bubble up via clawline AND replay on
  reconnect (both mechanisms verified to exist); the lifecycle TABLE stays for
  dashboard-shaped observability.
- **#16 SATELLITE.md** — prohibition becomes a loud confirmation gate (what, from-host,
  to-host, why, explicit yes). Spec edit + ceremony support.
- **Doctor section** — lifecycle failure-kinds since last clean boot epoch (P4 from the
  design review; hours).
- **Events schema conversation** — `kind` is a deliberately open string set; fine for a
  log, fragments under a dashboard's GROUP BY. Decide BEFORE building the dashboard.
- **npm packaging** (task #7) — Flynn picks (a)/(b)/(c); recommendation (a) mix release
  via per-platform optionalDependencies. After packaging, tiers re-run against the
  packaged artifact (a release-mode gateway is a different runtime from `mix run`).
- **T3 completion** — S3 workspace motion, T3b fault+reinstall, T3c N1/N2, macOS
  pairing, MANUAL smoke rows. Preconditions now hold (shrdlu onboarded, ssh config in
  place, runbook updated with tonight's four precondition lessons).
- **Tier staleness visibility** — every tier records last-passed SHA; unrun-against-main
  reports as UNPROVEN. This is the meta-lesson of the night: T2a/T4 were broken for four
  days and a broken tier is indistinguishable from an unrun one.

## Explicitly NOT doing (decided against, do not resurrect)

- Undiscardable return types / banning `:ok` / Credo gate now (fights the language;
  post-sweep grep is the whole check).
- "Narrate everything onto clawline" firehose (ambient noise erodes the same trust).
- Recording successes for every best-effort op; retry/self-heal attached to records.
- New tenet text as a fix — T-SOURCE corollary not added; the structural moves (public
  owner, deleted affordances) are what would have prevented all four drifts.
- Kind registry for lifecycle events (until the dashboard is real).
- Reconciler rewrite or queued-and-owned state (design is correct; incident does not
  indict it).
