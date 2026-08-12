# Home projection: shared {harness,machine} home + per-session cwd identity — v1

Status: DRAFT r4 (Opus-authored 2026-07-24). Greenfield — no production. The design was hardened
through independent adversarial review rounds and the live harness spikes cited below. Pending:
Sol-high review, then implementation.

## Provenance & rationale (why this architecture — do not lose this)

Each decision below is stated with the finding that forced it and the evidence, so a future reader
sees the reasoning, not just the mechanics.

1. **Root cause — the OAuth refresh-token race.** Both providers issue rotating, single-use refresh
   tokens with reuse-detection: refreshing in one process rotates the token and can revoke the whole
   lineage if another process later replays the spent one. Evidence: openai/codex#14144,
   anthropics/claude-code#25609, observed `refresh_token_reused` / `invalid_grant`. **Any design with
   N independent refreshers sharing one credential is racy by construction.** This finding drives
   everything else.
2. **The race was CREATED by binding identity to the home.** The prior model gave each archetype its
   own home (to hold that archetype's guidance/skills), and auth lived in the home too → per-archetype
   homes ⇒ per-archetype harness processes ⇒ N refreshers on the shared credential ⇒ the race.
   Decoupling identity from the home (deliver it per-session; keep ONE shared home for auth) removes
   the structural cause. → **shared `{harness, machine}` home + per-session cwd.** (Rejected:
   per-archetype homes — they are the race source.)
3. **Racelessness is asymmetric because the harnesses' process models differ.** Codex multiplexes all
   sessions on ONE runtime → one refresher → safe. Claude's ACP adapter spawns a SEPARATE Claude Code
   subprocess per session (evidence: claude-agent-acp calls SDK `query()` per session; SDK `close()`
   kills the CLI subprocess) → "one process" is impossible for Claude, so its race is removed **at the
   credential** by choosing the **non-rotating `setup-token`**. Two different fixes for two different
   process models. (Rejected: "one process per host eliminates the race" as a universal rule — true
   only for Codex; and Claude `/login`'s rotating credential — it is the race path.)
4. **Per-machine credential boundary.** Each machine keeps its own local credential and self-refreshes
   locally; secrets never transit between machines (preserves the placement boundary — a compromised
   transport cannot move a credential; a satellite onboards independently). (Rejected: a
   cross-host / central credential broker — it moves secrets and widens blast radius. Rejected:
   harvesting credentials from installed harness homes — racy and account-fragile.)
5. **Provider onboarding differs because the providers differ.** Codex has a real RFC-8628 device-code
   flow (headless-safe; verified live). Claude has NO device-code (open request #22992); its supported
   non-interactive path is `setup-token`, which returns a **carry-back code** and needs a **PTY**. We
   use each provider's actual supported mechanism, not a uniform wrapper. (Rejected: assuming a
   Codex-style device poll for Claude; API-key-primary auth — OAuth is the primary path.)
6. **Guidance is a string, skills are files — forced by what each harness consumes.** Both harnesses
   accept a per-session developer/system instruction string, so archetype guidance rides that (no
   file, no repo pollution, per-session, and — verified — outranks `AGENTS.md`). Codex discovers
   skills ONLY as files at the exact cwd (verified: no walk-up), so archetype skills must be
   materialized into the worktree and git-excluded. The asymmetry is imposed by the harnesses, not
   chosen. (Rejected: a `tightbeam agent-guidance` serve-verb + fetch library — an activation-tax
   apparatus made unnecessary by the injected instruction channel. Rejected: guidance-based skill "selection" —
   it is not segregation; isolation must be filesystem-scoped, proven live.)
7. **The kungfu is git-layered because git already solves learn/customize/re-learn.** Treating the
   shipped bundle as an upstream and local customizations as commits yields provenance, rollback, and
   conflict detection for free; re-learn = merge. (Rejected: seed-once copy with no merge — it loses
   customizations on a source update, which is exactly why the current seed-once `init_identity!` is
   insufficient for re-learn.)

**Evidence base (all 2026-07-24; live against real harnesses unless noted).** Skill segregation proven
against a running codex app-server (two sessions, different cwds, each saw ONLY its own skill, never
the other's). `.git/info/exclude` proven to hide materialized skills from `git status`/`git add -A`
while leaving a repo's own tracked `.codex/skills` untouched. Codex exact-cwd skill resolution (no
walk-up) proven. Codex `AGENTS.md` cwd→root composition and developer>`AGENTS.md` precedence read from
the binary's own bundled spec. Claude setup-token carry-back (`MANUAL_REDIRECT_URL:
platform.claude.com/oauth/code/callback`) + PTY (`isTTY`) gate + non-rotating 1-year token read from
the claude binary. Codex device-code verified live end-to-end. Codex home-skills emptying verified to
leave only ~16 binary built-ins (a capability floor).

## 1. The settled model — two scopes

- **Home** — one **generic, shared home per `{harness, machine}`** (process-level: `CODEX_HOME` /
  `CLAUDE_CONFIG_DIR`). Holds ONLY what is genuinely org-wide-and-machine-wide: the shared machine
  **auth credential** and the org-wide **Rails hooks**. No archetype identity, no archetype skills.
- **Per-session identity (the `cwd` = the session workdir)** — session-level. Each Tight Beam
  session runs a distinct harness session (`thread/start` for codex, `query()` for claude) whose
  `cwd` is that session's own workdir (a dumb path; §2). Archetype identity is delivered **into
  that session**, two ways depending on what the harness can consume.

**Delivery — the load-bearing table (each row verified):**

| Identity element | Source (kungfu / identity tree) | Delivered as | Why there |
|---|---|---|---|
| Auth credential | shared home | file/env at process level | one per machine → one refresher → no race |
| Rails hooks | shared home | org-wide hook map | hooks are org-wide (`Rails.hook_settings()` takes no archetype arg) |
| **Archetype guidance** | archetype TOML `[guidance]` (composed `#include` fragments) | **injected as the harness instruction channel** (Codex = developer message; Claude = appended system prompt — Claude has NO developer message) — on the wire: ACP `session/new` `_meta.systemPrompt` (claude, VERIFIED working in claude-agent-acp today) / `_meta.developerInstructions` → `thread/start.developerInstructions` (codex — **PREREQUISITE: a small codex-acp patch**; the underlying protocol field is verified in the pinned schema, but codex-acp newSession currently sends only `{config, modelProvider, cwd}`; patch it to pass the `_meta` field through, mirroring the claude adapter pattern) | a string needs no file; per-session; outranks `AGENTS.md`; no repo pollution |
| **Archetype skills** | `identity/skills/<elected>/SKILL.md` | **materialized at the SESSION CWD: `<session-cwd>/.codex/skills/tightbeam__<name>/` (claude: `.claude/skills/...`)**; the reserved `info/exclude` pattern applies ONLY when the session cwd is itself a repo checkout (a plain workdir has no git status to pollute) | skills are discovered only as files at the exact cwd (no walk-up, no walk-down) |
| **Product guidance** | the user's repo | read natively from the worktree (`AGENTS.md`/`CLAUDE.md`, cwd→root) | it's the product's, repo-scoped |
| **Product skills** | the user's repo | native `<repo>/.codex/skills` | the product's own |
| **Substrate skills** | `priv/skills/` (substrate-owned) | projected by the SUBSTRATE (baseline), never via the org library | substrate law must survive when inference cannot; names remain RESERVED — an org-library copy of a substrate skill name is refused at load, and the baseline list must not be emptied to defeat that guard. Substrate skills are not editable through the identity seam. |

### cwd vs home/auth — verified distinction
- **Codex.** `thread/start` carries a per-session `cwd`; `skills/list` resolves relative to the
  session cwd (`SkillsListParams.cwds`: *"When empty, defaults to the current session working
  directory"*). `AGENTS.md` is read from cwd up to the root and composed. `CODEX_HOME` is separate
  and process-level (`codex.mjs:654`) — auth + hooks live there.
- **Claude.** `query()` takes a per-session `cwd` (`sdk.d.ts:514`) and loads `CLAUDE.md` + project
  `.claude/skills` from it **only if `settingSources` includes `'project'`** (`sdk.d.ts:794`). Auth
  is the process-level `CLAUDE_CODE_OAUTH_TOKEN` env, not read from `cwd`.
- **Therefore:** guidance and skills are per-session; auth, hooks, and containment (Seatbelt,
  process-wide) are process/home-level. The split is not a preference — it's what each harness reads
  from where.

## 2. Identity topology (B1 resolution) — cwd is the session workdir

The session `cwd` **is the session workdir** — NOT a synthetic identity dir, and it is NOT
repointed. Identity layers onto it. Whether product conventions load natively depends on what
the workflow puts at the cwd: when a dispatch points the cwd at a repo checkout, the product's
`AGENTS.md`/skills load natively (cwd→root); under the engineering kungfu's own convention the
agent creates its worktree **inside** the workdir (`worktree-session` skill) — an assignment's
workdir holds everything the assignment produces — and reads the repo's conventions explicitly
on entry, because discovery is exact-cwd and does not walk down. The substrate treats the cwd
as a dumb path either way; where worktrees live is workflow, not substrate. Layout:

```
$CODEX_HOME  (shared per {harness, machine})          ← process-level
  ├── auth.json          ← the ONE shared credential (Codex runtime is its sole refresher)
  ├── hooks/ (Rails)     ← org-wide gate statutes
  └── skills/            ← EMPTY of archetype skills

Session A (reviewer)                       Session B (coder)
  cwd = <workdirA>/  (repo-checkout case)    cwd = <workdirB>/
  ├── AGENTS.md   ◄ PRODUCT guidance         ├── AGENTS.md   ◄ product guidance (native)
  ├── src/ …      ◄ the product's code        ├── src/ …
  └── .codex/skills/                          └── .codex/skills/
      ├── <product's own skills>                  ├── <product's own skills>
      └── tightbeam__review-* ◄ ARCHETYPE          └── tightbeam__coder-* ◄ archetype
          (materialized; info/exclude                 (materialized; info/exclude
           because this cwd is a repo)                 because this cwd is a repo)

(Non-repo-workdir case — the kungfu convention: same layout minus AGENTS.md/src at the
cwd; the worktree is a SUBFOLDER; no exclusion file exists or is needed; §8.11 proves it.)

  Archetype GUIDANCE is NOT a file here — it is INJECTED per session as the harness's
  instruction channel: Codex = developer message (thread/start.developerInstructions);
  Claude = appended system prompt. Precedence: injected identity > AGENTS.md/CLAUDE.md.
```

**Why this composition is correct and verified:**
- **Guidance composes; product guidance is NOT lost.** Codex's own `AGENTS.md` spec (from the
  binary): *"The contents of the AGENTS.md file at the root of the repo and any directories from the
  CWD up to the root are included… More-deeply-nested AGENTS.md files take precedence… Direct
  system/developer/user instructions take precedence over AGENTS.md."* So the product's `AGENTS.md`
  applies, and the archetype's injected identity applies and **outranks it** on conflict — archetype
  role/policy governs behavior; the product's file governs its own conventions.
- **Guidance rides a string, not a file** → no worktree file, no git-exclude needed for guidance,
  segregated by construction (each `thread/start` carries its own archetype's text).
- **Skills must be files** (Codex discovers skills only from the exact cwd — LIVE-VERIFIED: a
  child-repo cwd saw only the child's `.codex/skills`, never a parent's). So archetype skills are
  **materialized at the session cwd**; when that cwd is a repo checkout they are hidden from git
  via **`.git/info/exclude`** (LIVE-VERIFIED:
  the materialized skill was invisible to `git status`, unstageable by `git add -A`, and the repo's
  own tracked `.codex/skills` were untouched). Never the tracked `.gitignore`; never committed.

### Materialized-skill ownership — structural, via a reserved namespace (REQUIRED)

Materialization writes into a directory a product may also own, so ownership must be unambiguous.
It is established **structurally, by path**, not by recorded state:

- **Reserved namespace, unconditionally.** Every archetype skill is materialized at
  `.codex/skills/tightbeam__<name>/` (claude: `.claude/skills/tightbeam__<name>/`) — **always**, not
  only on collision. The `tightbeam__` prefix is reserved: a product skill using it is a naming
  violation, not a collision to arbitrate.
- **Therefore collision is impossible and ownership needs no manifest.** Tight Beam owns exactly the
  `tightbeam__*` entries and nothing else; a product's own `.codex/skills` entries are untouched by
  construction. There is deliberately NO ownership manifest: a recorded ownership list is state that
  can drift from the filesystem (a product file replacing a materialized one, a changed collision
  mapping, or the product owning the manifest file itself), and every such drift is a defect class
  the reserved prefix does not have.
- **Reconciliation on every provisioning.** Materialize the currently-elected skills, then remove any
  `tightbeam__*` entry that is no longer elected (de-election, re-election, or a re-learn that
  dropped a skill). Non-prefixed entries are never read, written, or removed. This prevents stale
  archetype skills from remaining visible.
- **Git exclusion is one reserved pattern.** The single exclusion `.codex/skills/tightbeam__*` (and
  the claude equivalent) is written to the repository's `info/exclude`. Because git resolves that
  file from the **common** git dir, the entry is shared by every linked worktree — which is safe
  here, and *only* because the pattern is a reserved prefix no product owns. A per-path exclusion
  scheme would be unsafe for exactly that reason: an exclusion added for worktree A would hide a
  product-owned file at the same path in worktree B.
- These behaviors are tested (§8.9), including against a real linked worktree.
- **Segregation is filesystem-scoped, not advisory** (LIVE-VERIFIED: two sessions with different
  cwds each saw ONLY their own archetype skill and never the other's).

## 3. The kungfu / identity tree — learn, customize, re-learn

**"Learning a kungfu" = seeding the git-versioned identity tree** at `<base_dir>/identity/`
(`Archetypes.init_identity!`). It installs the bundle: archetype definitions
(`archetypes/<name>.toml` — name + elected skills + `[guidance]` that `#include`s fragments),
guidance fragments (`guidance/*.md`), skill bodies (`skills/<name>/SKILL.md`), org-wide rails
(`rails/engineering.toml`), and kungfu metadata. It is a git repo — the source of truth, editable,
with provenance and rollback for free.

Two layers, managed exactly like a vendored dependency with an upstream:
- **Source kungfu** — the shipped bundle in `priv/kungfu/agentic-engineering/` (ships with the
  release; the upstream/vendor copy).
- **Learned kungfu** — the `identity/` git repo, seeded from source, then **locally editable**.

### Git model (exact — this is a merge, not a rebase)

The identity tree is a git repo with **three refs**:
- **`tightbeam/upstream`** — a branch holding **source snapshots**. Each learn/re-learn imports the
  current `priv/kungfu/<bundle>/` contents as **one commit on this branch, parented on the previous
  upstream commit** (so successive source versions form a related history — never unrelated roots).
  The import is a **full-tree replace** of the bundle's subtree, so **source deletions propagate** as
  deletions in that commit.
- **`main`** — the working branch. It starts at the first `tightbeam/upstream` commit; **local
  customizations are commits on `main`**.

Lifecycle (REQUIRED behavior):
1. **Learn (first time)** — import the source bundle as the initial `tightbeam/upstream` commit and
   set `main` to it. This is today's `init_identity!` seed.
2. **Customize** — edits (a new skill, a tweaked fragment, "coder talks like a pirate" →
   `identity/guidance/coder.md`) are **commits on `main`**. Local, versioned, effective immediately,
   and they **never touch the source `priv/` bundle**.
3. **Re-learn (source update)** — REQUIRED sequence, and it is a **merge**:
   1. **Precondition: clean working tree** on `main`. A dirty tree aborts re-learn with a legible
      error (never auto-stash — stashing is forbidden).
   2. Import the new source snapshot as a **new commit on `tightbeam/upstream`**, parented on the
      prior upstream commit (full-tree replace of the bundle subtree).
   3. **`git merge tightbeam/upstream` into `main`.** Local customizations are preserved because they
      are ancestors of `main`; git performs a three-way merge against the shared upstream base.
   4. **Success** = a merge commit on `main`, **then** `tightbeam/live` is fast-forwarded to `main`
      (below). **Conflict** = the repo is left in git's normal conflicted state on `main`, surfaced
      to the operator with the conflicting paths; re-learn reports `conflict`, does NOT auto-resolve,
      and **`tightbeam/live` does not move**. A conflict arises only where a customization touches
      something the source also changed.

- **`tightbeam/live`** — the third ref, and **the only ref sessions read**. `main` is the working and
  merge branch; `live` is the publication pointer, advanced by fast-forward only after a successful
  learn, customize, or re-learn. Because a conflicted or mid-merge `main` never advances `live`, a
  conflicted identity tree is never a live identity tree and conflict markers can never reach a
  delivered archetype identity (Codex developer message / Claude appended system prompt).

Re-learn is NOT the current seed-once `init_identity!` (which no-ops when `identity/.git` exists) —
it is a new operation. It MUST preserve local customizations, never clobber them, never silently drop
a source update (including deletions), and never produce an unrelated history.

### The identity seam — one write path, four verbs

All identity mutation goes through ONE seam operating the git model above; nothing else writes
`identity/`. Raw `git` in the tree and hand-edits of `priv/` are outside the model. The seam is
four verbs:

- **`tightbeam identity edit <archetype>`** — customize. Commits on `main`, then fast-forwards
  `tightbeam/live`. Never touches `priv/`.
- **`tightbeam identity relearn`** — the §3 upstream-import-and-merge sequence, publishing `live`
  only on success. `relearn --abort` discards a conflicted attempt (`git merge --abort`);
  `relearn --resolve` completes one after the operator resolves it, then publishes.
- **`tightbeam identity status`** — report only: the `live` revision, per-session revisions,
  staleness, and conflict state (`relearn-conflicted` with the conflicting paths). It never repairs
  and never mutates.
- **`tightbeam identity apply [<session>|--all]`** — move sessions onto the current `live` revision
  via the §9 bounce-and-resume. There is no in-place patch of a running session.

§6 teaches these verbs to the agent; the verb named there is `tightbeam identity edit`.

### Sessions stamp the revision they materialized from

Provisioning resolves `tightbeam/live` **once** and reads every artifact — composed guidance and all
elected skill bodies — through that single immutable commit, so guidance and skills can never
straddle a publication. Each session records that revision. A session whose stamp is behind `live`
is reported `identity-stale` by `identity status`; `identity apply` refreshes it through the §9
bounce. Customizations therefore reach NEW sessions at their next start and existing sessions when
applied.

## 4. Racelessness — asymmetric (Codex runtime vs Claude setup-token)

OAuth refresh tokens for both providers are single-use and rotate with reuse-detection
(openai/codex#14144, anthropics/claude-code#25609). The fix differs by harness:
- **Codex — one shared runtime, ONE refresher.** All co-located Codex sessions multiplex on a single
  Codex runtime (one `CODEX_HOME`, one auth). **The shared Codex runtime is the SOLE refresher and
  SOLE writer of that home's `auth.json`.**
- **Claude — non-rotating setup-token.** The Claude ACP adapter spawns a **separate subprocess per
  session** (N subprocesses, one credential) — "one process" is NOT available. Claude's race is
  removed at the credential: `claude setup-token` is a **non-rotating 1-year token**; N subprocesses
  reading a token that never rotates cannot collide. Setup-token is the REQUIRED Claude auth path.

## 5. Onboarding (VERIFIED mechanisms)

Shape is identical (**detect → loudly name harness+machine → launch that provider's login → observe
success → store → resume**); mechanism is provider-specific. Attention is **channel-neutral**:
baseline is a **local status + CLI** surface; any external channel is optional integration, never
required flow (Pushover is a deployment detail, not a product assumption).

- **Codex / OpenAI — device-code (RFC 8628), VERIFIED LIVE.** `codex login --device-auth`: present
  the verification URL + one-time code (`https://auth.openai.com/codex/device`; authorize
  `https://auth.openai.com/oauth/authorize`; client_id `app_EMoamEEZ73f0CkXaXp7hrann`). Approve on
  **any device**, no local browser/callback. Tight Beam **polls** the token endpoint; writes
  `auth.json` (0600) as the canonical `{harness, machine}` credential.
- **Claude / Anthropic — setup-token capture (NO device-code), VERIFIED from binary + docs.**
  `claude setup-token`: opens the browser authorization; the token returns via a **carry-back code**
  (the binary carries `MANUAL_REDIRECT_URL: https://platform.claude.com/oauth/code/callback`
  alongside a localhost server), so the user can **approve on a different machine and carry the code
  back** to a headless box. **Requires a PTY** to type the code into (an `isTTY` gate; non-TTY stdin
  aborts) — Tight Beam drives `setup-token` over a PTY. Requires a **subscription**. Tight Beam
  **captures the token from stdout**, stores it (0600), injects it via **`CLAUDE_CODE_OAUTH_TOKEN`**.
  Non-rotating (1 year) — the race fix. The rotating `/login` credential is NOT used.
- **Blocker status:** Codex — none. Claude — supported via setup-token; a **no-subscription** Claude
  account is genuinely `needs_onboarding: unsupported (no subscription)`, not silently retried.

## 6. Runtime operating guidance (REQUIRED — the agent must be taught to operate the model)

The impl MUST author and deliver **ample runtime guidance** (a kungfu operating-manual fragment,
composed into every archetype's injected identity) that teaches the agent how to operate WITHIN this
model. Without it, an agent will do the familiar-but-wrong thing (e.g. write archetype customization
into a repo's `AGENTS.md`). The guidance MUST cover, at minimum:

1. **Your identity arrives as your session instructions** (rendered per harness: the developer
   message on Codex, the system prompt on Claude — the composer emits the harness-accurate term)
   and is authoritative; your archetype skills are in this session's workdir and are yours to
   invoke.
2. **Two different "AGENTS" scopes — do not confuse them.**
   - *"In THIS repo, always X"* (build/test/convention for the product) → the **repo's own
     `AGENTS.md`** (repo-scoped, committed). Correct to edit for the product.
   - *"I, as the coder archetype, should always X"* (role/personal, every repo) → the **archetype's
     guidance fragment in the kungfu identity tree**, NOT any repo file. Use the verb below. Never
     write archetype-personal customization into a product repo's `AGENTS.md` (wrong scope, gets
     committed, applies to all archetypes).
3. **Do not commit the materialized `.codex/skills`/`.claude/skills` archetype entries** — they are
   git-excluded and are not part of the product.
4. **How to edit your own archetype guidance/skills** — via the §3 identity seam verbs; such edits
   are local customizations (commits on `identity/` `main`, published via `tightbeam/live`) layered
   over the source kungfu.

**The verbs are the §3 seam — the ONLY mutation surface (no second command family).**
Content input is non-interactive: `identity edit` takes `--file <path>` or reads stdin (agents pipe;
no editor is spawned). The edit target is selected by flag: the default (no flag) writes the
archetype's guidance fragment (`identity/guidance/<archetype>.md`); `--manifest` writes the
archetype's manifest (`identity/archetypes/<archetype>.toml`) — elections, `where`, defaults — and
is validated exactly as at boot (a manifest that would fail `load!` is refused, not committed);
`--skill <name>` writes the SHARED skill body (`identity/skills/<name>/SKILL.md` — library CRUD).
De-election is therefore `edit <archetype> --manifest` removing the name from `skills = [...]`,
after which `--skill <name> --rm` succeeds if no other archetype still elects it. `--skill <name> --rm` removes the shared body and
REFUSES while any archetype still elects it, naming the electors — de-elect first. Conflict
resolution after a conflicted `relearn` is the one sanctioned direct-edit window: the operator/agent
edits the conflicted files in the `identity/` working tree, then `relearn --resolve` stages, commits
the merge on `main`, and publishes `live`; `--abort` discards the merge state. Outside that window,
direct writes to `identity/` remain outside the model.

| Verb | Covers | Behavior |
|---|---|---|
| `tightbeam identity edit <archetype> [--manifest \| --skill <name> [--rm]]` | default: `identity/guidance/<archetype>.md`; `--manifest`: `identity/archetypes/<archetype>.toml` (elections, `where`, defaults — boot-equivalent validation; a manifest that would fail `load!` is REFUSED without commit); `--skill`: `identity/skills/<name>/SKILL.md` (add/update; `--rm` removes, refusing while any archetype elects it) | writes the target, commits on `main` (author recorded), fast-forwards `tightbeam/live` |
| `tightbeam identity status [<archetype>]` | live revision, per-session revisions, staleness, conflict state; with an archetype, also prints its composed guidance as delivered | report-only; never mutates |
| `tightbeam identity relearn [--abort\|--resolve]` | §3 re-learn | clean-tree precondition → upstream import → merge into `main`; publishes `live` only on success; `conflict` leaves `live` unmoved |
| `tightbeam identity apply [<session>\|--all]` | session refresh | moves sessions onto current `live` via the §9 bounce |

Path resolution is against the Tight-Beam-owned `identity/` tree (never a repo path). Only a
SUCCESSFUL identity-content mutation (`edit`; a `relearn` that merges cleanly or is `--resolve`d)
commits and publishes `tightbeam/live`; a conflicted or `--abort`ed `relearn` leaves `live` unmoved,
and `apply` consumes `live` but never changes it. No verb writes into a product repo.

**Harness-accurate wording (REQUIRED).** The guidance and the impl MUST NOT conflate the two
channels: on **Codex**, archetype guidance is the **developer message**
(`thread/start.developerInstructions`), which per Codex's spec outranks `AGENTS.md`. On **Claude**, it
is the **system prompt** (`query()` `systemPrompt`, append form) — Claude has no "developer message";
do not describe it as one.

This guidance is itself part of the kungfu, delivered per §1 — it is not documentation on the side;
it is in the agent's context every session.

## 7. Invariants

1. **No archetype identity in the home.** A home is per `{harness, machine}`; no per-archetype
   guidance, no archetype skills. Identity is delivered per session.
2. **Guidance is the injected instruction channel; skills are worktree files (git-excluded).**
   Archetype guidance → the harness's per-session instruction channel: Codex `developerInstructions`,
   Claude appended `systemPrompt` (Claude has NO developer message — never describe it as one). No
   worktree file for guidance. Archetype skills → materialized
   at the session cwd under the reserved `tightbeam__*` namespace; when the cwd is a repo checkout
   they are hidden by one reserved `info/exclude` pattern — never the tracked `.gitignore`, never
   committed. Ownership is structural (prefix), never a recorded manifest. Claude MUST keep `settingSources ⊇ 'project'`.
3. **cwd is the session workdir, not repointed.** The ACP `cwd` remains Tight Beam's existing
   durable session workdir — a dumb path (§2). When the workflow points it at a repo checkout,
   product `AGENTS.md`/`CLAUDE.md` and product skills apply natively; under the kungfu
   worktree-in-workdir convention the agent reads the repo's conventions on entry. The product
   repo is never polluted by materialized identity in either case.
4. **Filesystem-scoped skill segregation.** A reviewer session's skills are physically absent from a
   coder session (different session cwds). The home skill dir holds no archetype skills.
5. **Single Codex authority, phased (§9b).** While a Codex runtime is live it is the **SOLE refresher
   and SOLE writer** of the home's `auth.json`; `Tightbeam.Credentials` never writes it and never runs
   a refresh loop. Only in the **bootstrap phase** (no runtime live) does `Tightbeam.Credentials`
   perform exactly one atomic credential write. `homes.ex` never writes the credential. Re-onboarding
   follows the serialized order in §9b, and a bounce never precedes obtaining the replacement
   credential.
6. **Claude racelessness = non-rotating setup-token.** N subprocesses per session share one
   credential; it MUST be the non-rotating setup-token.
7. **One shared credential per `{harness, machine}`, real file/env, never harvested, never crosses
   machines.**
8. **Customizations are identity-tree git commits; re-learn is a merge that preserves them.** No
   customization touches the source `priv/` bundle; re-learn never clobbers local customizations and
   never silently drops a source update.
9. **The agent is taught to operate the model** (§6): the runtime operating guidance is delivered
   every session.

## 8. Isolation guarantees + REQUIRED proofs (tests MUST prove every isolation the model promises)

Each isolation below is a promise of the model; the spec REQUIRES a real, fail-on-revert test that
proves it (the automated form of the 2026-07-24 spikes). No isolation is asserted without a test.

**The expected visible-skill set (the precise predicate every skill test asserts).** For a session of
archetype **A** with session cwd **C** (which may be a repo checkout OR a plain workdir):

```
Let E(X) = the set of skills archetype X elects.

visible(A, C)  ==  built-in floor  ∪  product skills committed at C (∅ when C is not a repo)
                   ∪  E(A)  (materialized at C under the tightbeam__* namespace)

Segregation clause:   visible(A, C)  ∩  ( E(B) − E(A) )  ==  ∅   for every archetype B ≠ A
```

**The exclusion is `E(B) − E(A)`, NOT `E(B)`.** A skill elected by BOTH archetypes (a shared
election, e.g. a common `editing-and-viewing-files`) is legitimately visible to both — it is in
`E(A)`, so it is not a leak. Asserting `visible(A) ∩ E(B) == ∅` would be **unsatisfiable** for any
shared election. Only skills unique to another archetype must be absent.

Likewise a **product** skill that happens to share a name with an archetype skill is not a
violation: entries are distinguished by provenance — product entries at their own path, Tight Beam
entries under the reserved `tightbeam__*` namespace (per §2's ownership rules) — so the predicate is
evaluated over **provenance-qualified** entries, not bare names.

"Segregated" means **excludes other archetypes' exclusive skills** — it does NOT mean "only A's
skills"; the built-in floor, the product's own skills, and shared elections are expected and
required to be present.

1. **Skill segregation — BOTH harnesses.** Spawn a reviewer archetype and a coder archetype on one
   host; assert the `visible(A, C)` predicate above holds for each session: each sees the built-in floor +
   its worktree's product skills + its own elected skills, and **no skill in `E(B) − E(A)`** (the
   other archetype's EXCLUSIVE skills; a skill both elect is legitimately visible to both). Assert
   the shared home skill dir contains no archetype skills. Run for **Codex** (via
   `skills/list`) **and Claude** (via the session's available-skills listing, with
   `settingSources ⊇ 'project'`). (Automates the live segregation spike, extended to Claude.)
1b. **Positive product-skill visibility.** Assert a product-owned skill in the worktree IS visible to
   the session (proving materialization does not mask or displace product skills) — both harnesses.
1c. **Cross-session guidance non-leakage — sentinel-based (composition-aware).** Archetype guidance
   is deliberately **shared fragments + archetype-specific fragments**: the §6 operating-model
   fragment and common fragments (`wisdom.md`, `engineering-tenets.md`, …) are included in EVERY
   archetype by design. A naive "none of A's guidance appears in B" assertion is therefore
   **unsatisfiable** — it would fail on the shared fragments — while a loose assertion would miss
   genuine leakage. The test MUST distinguish the two classes:
   - Place a unique sentinel in an **A-only** fragment and another in a **B-only** fragment, plus a
     sentinel in a **shared** fragment.
   - Assert: the shared sentinel appears in **both** sessions (composition works); the A-only
     sentinel appears in A and **never** in B; the B-only sentinel appears in B and **never** in A.
   - Run for two concurrent sessions on **both** harnesses — Codex (`developerInstructions`) and
     Claude (appended `systemPrompt`).
2. **No repo pollution.** After materializing archetype skills into a real git worktree, assert
   `git status` is clean, `git add -A` stages nothing of the materialized skills, and the repo's own
   tracked `.codex/skills` (if any) are untouched. (Automates the `.git/info/exclude` spike.)
3. **Guidance scoping + precedence — BOTH harnesses.** With a repo-checkout cwd carrying a product
   conventions file AND archetype guidance delivered: on **Codex** (product `AGENTS.md` + developer
   message) and on **Claude** (product `CLAUDE.md` + system prompt, `settingSources ⊇ 'project'`),
   assert both layers are in effect and that on a deliberate conflict the archetype instruction wins
   (Codex per its documented developer>AGENTS.md precedence; Claude asserted empirically and the
   observed precedence recorded as the fixture). Assert a product repo containing no archetype still
   gets correct archetype identity (identity comes from the kungfu, not the repo).
4. **Customization does not touch source; re-learn preserves it.** Assert a customization commit lands
   in `identity/` and leaves `priv/` byte-identical; then re-learn against a changed source and assert
   the local customization remains present in the three-way merge result and a genuine conflict is surfaced, not silently
   dropped.
5. **Personal skills are out of scope.** Assert a user's personal `~/.codex/skills` are NOT visible to
   a Tight Beam agent (Tight Beam uses its own `{harness,machine}` home), and agent skills never write
   into a user's personal codex.
6. **Codex no-race / single authority.** Spawn N concurrent Codex archetype sessions; assert ONE Codex
   runtime process and ONE credential, and that `Tightbeam.Credentials` performs no `auth.json` write
   while the runtime is live.
7. **Claude non-rotating auth / no-race.** Assert the Claude path uses `CLAUDE_CODE_OAUTH_TOKEN` (not
   a rotating `~/.claude/.credentials.json`); an N-session soak shows no `refresh_token_reused` /
   `invalid_grant`.
8. **Runtime operating guidance is present.** Assert every archetype's delivered archetype guidance
   (Codex developer message / Claude system prompt) contains the operating-model guidance (§6),
   including the named verbs — the agent is actually taught, every session.
9. **Materialized-skill ownership, collision, and reconciliation.** Assert: (a) a product-owned skill
   path (tracked or untracked) sharing a name with an elected archetype skill is **never
   overwritten** — the product file is byte-identical after provisioning, because the archetype skill
   only ever occupies `tightbeam__<name>`; (b) after **de-election** (or a re-learn that drops a
   skill), the stale `tightbeam__*` entry is **removed**, and non-prefixed entries are **never**
   removed — after removal, a NON-prefixed product entry sharing the same base name is untouched
   (a product file can never legitimately occupy a `tightbeam__*` path — that prefix is reserved);
   (c) in a **real linked worktree** whose product owns a colliding skill name, that product file
   stays visible to `git status`/`git add -A` while the `tightbeam__*` entries stay hidden, proving
   the shared `info/exclude` pattern is safe across worktrees.
10. **Re-learn git model.** Assert `tightbeam identity relearn` aborts on a dirty tree; that a source
   update produces a commit on `tightbeam/upstream` parented on the prior upstream commit (related
   history, not an unrelated root); that a **source deletion propagates**; that a non-conflicting
   customization survives the merge; and that a genuine conflict leaves a legible conflicted state
   rather than auto-resolving or dropping either side.
11. **Non-repo workdir topology (the kungfu convention).** With a session cwd that is a PLAIN
   workdir containing a nested engineering worktree: assert archetype skills materialized at the
   cwd are visible via `visible(A, C)`; the nested repo's committed skills are NOT auto-visible
   (exact-cwd, no walk-down); no exclusion file is written anywhere (nothing to exclude); and
   nothing Tight Beam writes lands inside the nested worktree. Run BOTH harnesses. Companion case:
   a session cwd that IS a repo checkout exercises tests 2 and 9 unchanged.
12. **Ownership-scoped home regeneration (local AND remote).** Plant harness durable state in both
   homes (Codex: a `sessions/` rollout, `history.jsonl`; Claude: a `projects/<slug>/` transcript
   and `memory/` file); change the projection manifest; regenerate. Assert: owned paths (credential
   entry, rails artifact, `.tightbeam/`) are replaced; every planted file survives byte-identical;
   the **preservation harvest** ordering held — regeneration runs only gated with the runtime
   STOPPED (no live writer), and a home credential entry that the runtime had rotated into a
   regular file is copied back to the Tight-Beam-owned store BEFORE the entry is replaced with a
   fresh link (never clobbered); and no whole-home removal occurred — locally and over the
   `placement.ex` remote path.
13. **Publication isolation (`tightbeam/live`).** Assert: a conflicted or aborted re-learn leaves
   `live` unmoved and running/starting sessions still provision from the last-good revision;
   provisioning while `main` ≠ `live` delivers `live` content only (never `main`, never conflict
   markers); and a `live` fast-forward DURING provisioning cannot mix revisions — the session's
   guidance, skills, and revision stamp all come from the single OID resolved at provisioning
   start. Additionally: a SUCCESSFUL `live` advance causes NO automatic refresh — an open session's
   materialized skills, delivered guidance, and stamp are byte-identical before and after the
   publication until `identity apply` runs; and `apply` itself is proven to close/reopen only the
   harness session (same workdir, same history pointer), recompose guidance AND skills from one
   resolved OID, update the stamp, and leave the shared Codex runtime process untouched (same OS
   pid before and after).
14. **Per-machine credential isolation.** With two machine contexts, assert each onboards
   independently, each runtime is launched with only its local credential, and no credential bytes
   traverse the placement/control channel between them (fail-on-revert against the transport
   layer).

## 9. Lifecycle: credential/home change → bounce-and-resume (B2, decided)

No non-destructive/drain/rollback machinery is required (greenfield; killing/bouncing agents is
acceptable; sessions are durable and resume). The rule is the ratified B2 model:
- **Guidance/skill changes** touch **session workdirs / the injected identity on next session**, not
  the shared home → nothing bounces AUTOMATICALLY; new sessions pick the changes up at start.
  **`identity apply [<session>|--all]` is the explicit per-session refresh**: at a turn boundary,
  close the harness session, re-materialize skills and recompose guidance from ONE resolved
  `tightbeam/live` OID, re-open the harness session on the same workdir and history pointer, and
  update the session's revision stamp. For Codex this closes/reopens the THREAD only — the shared
  runtime process is not restarted. §8.13's single-OID rule applies to the re-provision.
- **Codex auth / hook change in the shared home** → written atomically (write-temp-rename onto the
  store backing file for the credential, per §9b link topology; direct for hook artifacts); when a
  running runtime must pick it up, the runtime/adapter is **bounced and resumed** (reads fresh state
  at start). No live in-flight patch.
- **Claude token change** → bounce the adapter/subprocess; the resumed process reads the fresh
  `CLAUDE_CODE_OAUTH_TOKEN`.

## 9b. Credential writer authority — ONE serialized lifecycle (resolves the writer contradiction)

"The runtime is sole writer" and "Tight Beam writes the credential at onboarding" are both true only
if phased. The phases are normative:

- **Bootstrap phase — no Codex runtime is live for that home.** `Tightbeam.Credentials` is the
  **only** writer: onboarding performs **exactly one** atomic write of the Tight-Beam STORE backing
  file (`<base_dir>/auth/codex/…`, write-temp-rename, 0600), then links the home entry
  (`CODEX_HOME/auth.json` → store) and updates lifecycle metadata. The atomic write targets the
  store, never `auth.json` directly — renaming onto `auth.json` would replace the link itself.
- **Steady state — a Codex runtime is live.** The **runtime is the sole writer and sole refresher**
  of `auth.json`. `Tightbeam.Credentials` MUST NOT write it, and MUST NOT read-modify-write it.
- **`homes.ex` never writes the Codex credential.** It provisions the generic home (org-wide hooks,
  directory layout) only. Credential writes belong exclusively to `Tightbeam.Credentials`' bootstrap
  phase. (This removes the r4 contradiction.)

**Re-onboarding is serialized and ordered so a bounce can never reload a revoked credential:**

```
1. gate  — stop admitting new sessions for that {harness, machine}
2. stop  — stop the Codex runtime (no live writer remains)
3. write — obtain the NEW credential (guided onboarding), write it atomically to the STORE backing
   file, and replace the home entry — which the old runtime may have left as a regular rotated
   file — with a fresh link to the store  ← exactly one credential write
4. mark  — update lifecycle metadata (onboarded, cleared terminal flag)
5. start — start the runtime against the new credential
6. resume— resume sessions
```

**The bounce never precedes step 3.** A terminal credential parks sessions (`needs_onboarding`) and
waits for a replacement; restarting the runtime against the same revoked credential — the
reload-revoked-and-loop failure — is forbidden. If onboarding cannot complete (e.g. no human), the
machine stays gated with a legible `needs_onboarding`, not in a restart loop.

## 10. Dead-credential signal contract (concrete)

A bare request-level 401 is NOT proof a credential is dead, and `Tightbeam.Credentials` may not
refresh to classify (that would be a second refresher — forbidden by Invariant 5). The contract:

- **Signal source (Codex):** the **`account/updated` notification's `authMode` field** (nullable;
  `"chatgpt"` while logged in — VERIFIED in the pinned schema). The prior candidates are confirmed
  WRONG and must not be used: `reauthenticationRequired` is `McpServerStartupFailureReason` (MCP
  server startup, unrelated to the account credential), and `unauthorized` is a
  `ChatgptAuthTokensRefreshReason` belonging to the external-token auth mode Tight Beam does not
  use. The impl MUST capture the real logged-out fixture once (revoke a throwaway token, record the
  notification) and pin the exact shape against the generated protocol schema
  (`codex app-server generate-json-schema --out <dir>`, version-checkable).
- **Fail-safe default (REQUIRED):** any event/error that is **not** in the pinned terminal set —
  including unknown or newly-introduced variants — is classified **NON-terminal**. Unknown never
  escalates to re-onboarding. (Under-triggering is recoverable; over-triggering revokes a working
  machine.)
- **Signal source (Claude):** the setup-token is non-rotating, so there is no refresh to consult — a
  provider rejection of the token itself (401/invalid-token on an authenticated request, persisting
  across a retry) is terminal.
- **Mapping:** a terminal signal → `Tightbeam.Credentials.mark_terminal/2` → `needs_onboarding` +
  the guided flow + the §9b serialized re-onboarding. Nothing else may declare a credential dead.
- **Tests (fixture-based, REQUIRED):** a transient 401 does NOT mark terminal; an **unknown** event
  does NOT mark terminal; each pinned terminal shape DOES; and the Claude persisted-rejection case
  does. Fixtures are the recorded event/error payloads, so a protocol change breaks the test rather
  than silently changing classification.

## 11. Migration — none (greenfield)

There is no production and no live deployment on the old per-archetype-home model to protect. Build
the target model directly; stand up shrdlu/eezo fresh on it. No add→onboard→collapse→retire cutover,
no per-machine migration state machine. (This deletes r3's B5/B6.)

## 12. Component-by-component changes

- **`lib/tightbeam/homes.ex`** — home keyed `{harness, machine}`, generic. **Ownership-scoped
  regeneration (REQUIRED):** Tight Beam owns exactly its credential entry, its rails artifact, and
  `.tightbeam/` (the projection manifest moves to `.tightbeam/manifest`); regeneration replaces ONLY
  those paths — never `File.rm_rf!` of the home, local or remote (`placement.ex:953` has the same
  defect on the remote path). Everything else in the home is harness-owned durable state (Codex
  `sessions/` rollouts, `history.jsonl`, automation memory; Claude `projects/<slug>/` transcripts and
  memory) and MUST survive regeneration byte-identical — VERIFIED: even a failed claude run creates
  `projects/<slug>/memory/` and a transcript inside `CLAUDE_CONFIG_DIR`. The r4 rationale ("an
  identity change is a new agent body") is void under r5: identity is not in the home. **Credential
  link topology (normative):** the Tight-Beam-owned store (`<base_dir>/auth/<harness>/…`) is the
  backing file; onboarding writes it once and links the home entry (`auth.json`) to it. In steady
  state the RUNTIME may replace that link with a regular file when it rotates — expected, and the
  store copy is then stale backing, never a competing writer. Regeneration is gated: stop the
  runtime first, then the **preservation harvest** (copy a rotated regular-file entry back over its
  store source — this preserves Tight Beam's OWN credential and is REQUIRED; it is distinct from
  the PROHIBITED onboarding-harvest of a user's installed harness home), then replace + relink. A fail-on-revert test
  plants harness state, changes the manifest, regenerates, and asserts survival (§8). Remove
  per-archetype home projection
- **Per-session provisioning** — materialize the archetype's elected skills at the SESSION CWD
  under `.codex/skills/tightbeam__<name>/` (claude equivalent); when and only when that cwd is a
  repo checkout, ensure the single reserved `info/exclude` pattern is present (a non-repo workdir
  needs no exclusion). Do NOT write a guidance file, and do NOT write an
  ownership manifest.
- **Guidance delivery** — ONE composer. Resolve `tightbeam/live` once, read the archetype's composed
  `[guidance]` (fragments) and the elected skill bodies through that single commit, and pass the
  composed string as `thread/start.developerInstructions` (codex) / `query()` systemPrompt (claude).
  Compose in the §6 operating-model guidance. Both harness adapters consume the composer's output;
  neither composes its own.
- **`Archetypes` — re-learn as merge** — add the source-as-upstream merge operation (§3); keep
  `init_identity!` as the first-time seed.
- **`placement.ex` / `acp/adapter.ex` / `adapter_coordinator.ex`** — launch the generic home + shared
  credential; each session is a distinct harness session with `cwd` = its session workdir (a dumb path); Codex multiplexes
  on one runtime (sole refresher); Claude opens its per-session subprocess with
  `settingSources ⊇ 'project'`.
- **`Tightbeam.Credentials`** (companion spec) — onboarding + lifecycle + health + re-onboarding,
  per host; NOT a Codex refresher; drives device-code (codex) and setup-token-over-PTY (claude).

## 13. Rejected / superseded alternatives (do not reintroduce)

- Per-archetype home projection (the race source).
- Served guidance via a `tightbeam agent-guidance` verb + a fetch library (r1) — superseded by
  per-session injected guidance via the harness instruction channel (no serve verb, no fetch, no
  activation tax).
- "One process per host eliminates the race" universally — true only for Codex.
- **Guidance-based skill selection** ("all skills available; guidance says which to use") — REJECTED
  as non-segregation. Isolation is filesystem-scoped, proven live.
- A second Codex refresher / broker refresh loop — REJECTED (Invariant 5).
- Writing archetype identity into a product repo's `AGENTS.md`; harvesting credentials; per-archetype
  OAuth login; cross-host / central credential broker; API-key-primary; Claude `/login` rotating
  credential — all rejected.

## 14. Acceptance

- Every isolation in §8 (1-14, including non-repo-workdir topology, ownership-scoped home
  regeneration local+remote, publication isolation, and per-machine credential isolation) has a
  real, fail-on-revert test that passes; each proves the promised
  isolation (segregation, no pollution, scoping/precedence, customization-vs-source, personal-skills
  out, Codex no-race/single-authority, Claude non-rotating, operating-guidance-present).
- Guidance delivered via the harness instruction channel (Codex developer message / Claude appended
  system prompt); skills materialized + git-excluded; product guidance/skills
  apply natively WHEN the session cwd is a repo checkout (under the kungfu worktree-in-workdir
  convention the agent reads the nested repo's conventions explicitly on entry, per §6); no
  archetype identity in the home.
- Learn / customize / re-learn lifecycle works: customizations are `identity/` commits, re-learn
  merges the source upstream without clobbering, conflicts surface.
- Onboarding: Codex device-code and Claude setup-token-over-PTY each produce a valid credential; the
  catalog validates models; no-subscription Claude surfaces `unsupported`.
- Anti-stub: every invariant + isolation test is real; genuinely-blocked items → HANDOFF with a named
  blocker.
