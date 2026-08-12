# Tightbeam credential onboarding + lifecycle — v1

Status: DRAFT r3 (Opus-authored 2026-07-24). Greenfield — no production. Both architecture decisions
are Flynn-ratified (B2, B5). Pending: r3 Sol-high review, then Sol implementation.

`served-identity-home-projection-v1` is the authoritative statement of the home/identity model,
racelessness, onboarding mechanisms, and skill/guidance delivery — including the shared **Provenance
& rationale** for the OAuth race, per-machine boundary, and provider differences. This spec is the
credential-onboarding-and-lifecycle companion; where they overlap, the served-identity spec governs.

## Provenance & rationale (credential-specific; see the served-identity spec for the shared root cause)

- **Why `Tightbeam.Credentials` is NOT a refresher.** The OAuth race (rotating single-use refresh
  tokens with reuse-detection) means two refreshers on one credential can revoke the whole lineage.
  The Codex runtime already refreshes and owns `auth.json`; a second refresher in Tight Beam would
  re-create the exact race we are eliminating. So this component is deliberately confined to
  onboarding + lifecycle + health + re-onboarding, and owns no live token copy. (This corrects an
  earlier design where the broker was the sole refresher/writer with single-flight crash-safe
  refresh — that made Tight Beam the second refresher and is rejected.)
- **Why Claude has no API-key fallback and no rotating credential.** Claude's race is removed by the
  non-rotating `setup-token`; a rotating `/login` credential is the race path, and an API-key fallback
  is unnecessary given setup-token is the supported subscription path. (Earlier "OAuth primary +
  API-key secondary + anthropic-device-poll-or-API-key-fallback" framing is rejected.)
- **Why the dead-credential signal is the runtime's terminal event, not a broker refresh probe.** A
  bare 401 is not proof of death; and this component cannot itself refresh to classify (that would be
  a second refresher). So the classifier is the Codex runtime's own terminal auth signal (or, for
  Claude's non-rotating token, a plain rejection).
- **Why notification is channel-neutral.** Pushover is a deployment detail of one operator, not a
  product assumption; the baseline must work with a local status/CLI surface and zero external
  services.

## Ratified decisions

- **B2 — restart picks up the current credential; bounce on broken (Flynn FINAL 2026-07-24).** To get
  a new/refreshed credential into an agent, **reset/bounce/resume** it — on (re)start it reads the
  current credential. A **broken** credential (rejected and not silently recoverable) makes the
  bounce **required — and replacement-conditioned**: per the serialized lifecycle (Invariant 3b /
  served-identity §9b) the bounce happens only AFTER the replacement credential is written; a
  terminal mark parks sessions, it never restarts them against the revoked credential. In-flight
  swap is permitted but never a dependency. No continuous fan-out into running agents.
- **B5 — per-host credentials + tightbeam-guided onboarding (Flynn ratified 2026-07-24).** Each
  machine keeps its OWN local credential; secrets NEVER transit between machines. Tight Beam ITSELF
  walks a user through onboarding on each machine — a first-class product flow, per host.

## Problem

Tight Beam needs a provider credential per machine (OpenAI for codex, Anthropic for claude) so the
model catalog validates models and spawned agents can call their providers. The old design harvested
credentials from a USER's installed harness homes (`~/.codex`, `~/.claude`) — the prohibited
**onboarding-harvest**, distinct from the required **preservation harvest** of Tight Beam's OWN
rotated credential during gated home regeneration (served-identity §12) — and symlink-shared one across every per-archetype home;
because OAuth refresh tokens rotate and are single-use, concurrent refreshers raced → bricked login.
The served-identity model removes the many-home race structurally (one shared `{harness, machine}`
home, one Codex runtime). What remains for THIS spec: Tight Beam must **own** the machine credential
(never harvest it), **onboard** it via a guided flow, and **manage its lifecycle** (health, bounce,
re-onboarding) — WITHOUT becoming a second refresher.

## Invariants

1. **Tight Beam owns its credential; never onboarding-harvests from a user's harness home.** No NEW
   credential ever originates from a user's installed harness home. (The regeneration-time
   preservation harvest of Tight Beam's own rotated credential — projected home entry → Tight Beam
   store, runtime stopped — is a different operation and is required; served-identity §12.)
2. **Per-host ownership; one credential per `{harness, machine}`.** Each machine holds its own local
   credential; secrets never cross machines (B5).
3. **Single Codex authority, phased.** **Bootstrap phase** (no Codex runtime live for that home):
   `Tightbeam.Credentials` is the only writer and performs **exactly one** atomic write of the
   Tight-Beam STORE backing file (write-temp-rename, 0600), then links `CODEX_HOME/auth.json` to it
   (served-identity §12 link topology — the rename targets the store, never the link). **Steady state** (runtime live): the runtime is
   the **SOLE refresher and SOLE writer**; this component never writes it, never read-modify-writes
   it, and runs **no refresh loop**. `homes.ex` never writes the credential. Home regeneration
   touches the credential entry only GATED with the runtime stopped, preservation-harvest first
   (served-identity §12); the "exactly one write" of bootstrap is not violated by that harvest —
   the harvest copies the runtime's own rotation back to the store, it does not mint a credential.
   Re-onboarding follows the serialized order below.
3b. **Serialized re-onboarding; never bounce before the replacement exists.**
   `gate → stop runtime → obtain+write new credential (exactly one write) → mark metadata → start
   runtime → resume sessions`. Restarting a runtime against a known-revoked credential is forbidden
   (it loops); if onboarding cannot complete, the machine stays gated with a legible
   `needs_onboarding`. (Authoritative statement: served-identity spec §9b.)
4. **Claude auth is the non-rotating setup-token.** Captured from `claude setup-token` stdout (over a
   PTY), stored 0600, injected via `CLAUDE_CODE_OAUTH_TOKEN`. There is no Claude refresh loop and no
   rotating `~/.claude/.credentials.json`. No API-key fallback (setup-token/OAuth is the path).
5. **Credential canonical truth.** Codex: `CODEX_HOME/auth.json` is the sole LIVE truth after
   onboarding (runtime-owned; a link to the Tight-Beam store file until the runtime's first
   rotation replaces it with a regular file). The store copy is BACKING — reconciled only by the
   gated preservation harvest, never written while the runtime lives, never a competing writer.
   `Tightbeam.Credentials` persists only lifecycle/status **metadata** (onboarded?,
   last-known-health, provider, subscription-status, expires_at) — never a second live copy.
   Claude: the captured setup-token is the truth, injected as env; `Tightbeam.Credentials`
   holds it plus status metadata.
6. **Onboarding is a guided product flow, channel-neutral.** Tight Beam drives the provider-specific
   login (device-code for codex; setup-token-over-PTY for claude) and surfaces attention via a
   **local status + CLI baseline**; any external notification channel is optional integration, never
   required (no mandatory Pushover).
7. **Degraded state is a guided journey.** Missing/expired/`unsupported` credential on a model-needing
   call → legible `needs_onboarding` + the guided flow; calls needing no model keep working.
8. **Broken → park, then replacement-conditioned bounce (B2 + 3b).** A credential confirmed genuinely
   broken (per the §Dead-credential signal contract) gates and PARKS sessions; the bounce/resume runs
   only after the serialized re-onboarding (Invariant 3b) has written the replacement — never before.
   The resumed process reads the current (new) credential at start.
9. **Security: 0600, same-UID trust, minimal copies.** Credential/metadata files are 0600 under a
   same-UID trust model (portable to Linux/gibson). Keychain/secret-manager is a v1 non-goal.

## Architecture — `Tightbeam.Credentials` (per host)

One GenServer per host, owning that host's **onboarding + lifecycle**, NOT refresh. Contract:

- **`status(provider) :: :onboarded | {:needs_onboarding, reason}`** — the check every model-needing
  path consults (catalog refresh, spawn). Reads lifecycle metadata + the presence/health of the
  canonical credential (Codex `auth.json` present and not flagged terminal; Claude token present and
  not flagged revoked), and **compares `expires_at` against now at this read seam** — past the
  boundary returns `{:needs_onboarding, :expired}`. The comparison happens ONLY at read seams
  (status/spawn/catalog/credential-read); there is NO timer, sweep, or scheduled check (ratified
  event-driven invariant). Never refreshes. **Boundary tests (REQUIRED):** a token past `expires_at`
  yields `:expired` at the next read; one before it yields `:onboarded`; no process wakes to check.
- **`onboard(provider) :: :ok | {:error, reason}`** — runs the provider-specific guided flow (below),
  writes the canonical credential (Codex: `auth.json`; Claude: captured token + env wiring) and the
  lifecycle metadata. Per host.
- **`mark_terminal(provider, evidence)`** — records a terminal auth failure (from the §Dead-credential
  signal) → sets `{:needs_onboarding, :revoked}`, **gates new sessions and PARKS running ones**, and
  raises the guided flow. It never restarts anything. This is the ONLY path that declares a
  credential dead; a bare 401 does not reach it.
- **Bounce coordination (replacement-conditioned)** — after `onboard` writes the replacement per the
  serialized order (Invariant 3b: gate → stop → write → mark → start → resume), coordinate the
  reset/resume so the runtime (Codex) or adapter/subprocess (Claude) starts against the NEW
  credential, with the old process's exit confirmed before start.

There is deliberately **no `resolve`/`refresh`/`write_home`-of-live-token** in this component — the
Codex runtime refreshes and owns `auth.json`; Claude's token is non-rotating.

## Guided onboarding (provider-specific — the verified mechanisms)

`tightbeam onboard <provider>` — per-host, admin-tier, thin CLI. The verified mechanisms (full detail
in `served-identity-home-projection-v1` §5):

- **Codex / OpenAI — device-code (RFC 8628), verified live.** Present verification URL + one-time
  code (device `https://auth.openai.com/codex/device`; authorize
  `https://auth.openai.com/oauth/authorize`; client_id `app_EMoamEEZ73f0CkXaXp7hrann`; scopes
  `openid profile email offline_access api.connectors.read api.connectors.invoke`; PKCE S256).
  Approve on any device; Tight Beam **polls** the token endpoint; the flow writes
  `CODEX_HOME/auth.json`. After this, the runtime owns rotation.
- **Claude / Anthropic — setup-token capture over PTY, verified from binary+docs.** `claude
  setup-token` opens the browser authorization; the token returns via a **carry-back code**
  (`MANUAL_REDIRECT_URL: https://platform.claude.com/oauth/code/callback`) — approve on any device,
  carry the code back. Tight Beam drives it **over a PTY** (the CLI's `isTTY` gate requires an
  interactive terminal), **captures the token from stdout**, stores it 0600, and injects it via
  `CLAUDE_CODE_OAUTH_TOKEN`. Requires a **subscription**; a no-subscription account is
  `needs_onboarding: unsupported (no subscription)`, surfaced, not retried. Non-rotating (1 year).

When any model-needing call hits `needs_onboarding`, Tight Beam drives the same flow and surfaces the
URL+code via the **local status/CLI baseline** (and any configured optional channel), so a headless
host is legible rather than silently failing.

## Dead-credential signal contract

A bare request-level 401 is NOT proof a credential is dead, and this component may not refresh to
classify (that would be a second refresher — forbidden by Invariant 3).
- **Codex:** the **`account/updated` notification's `authMode` field** (nullable; `"chatgpt"` while
  logged in — verified in the pinned protocol schema) is the signal source the adapter surfaces to
  `mark_terminal` (authoritative contract: served-identity §10). The previously named candidates are
  confirmed WRONG and are retained only as NON-terminal fixtures: `reauthenticationRequired` is
  `McpServerStartupFailureReason` (MCP startup, unrelated to the account credential) and
  `unauthorized` is a `ChatgptAuthTokensRefreshReason` of the external-token auth mode Tight Beam
  does not use. The impl captures the real logged-out fixture once (revoke a throwaway token) and
  pins the exact shape against the generated schema (`codex app-server generate-json-schema --out`,
  version-checkable in CI).
- **Fail-safe default (REQUIRED):** anything not in the pinned terminal set — including unknown or
  newly-introduced variants — is **NON-terminal**. Unknown never escalates to re-onboarding
  (over-triggering revokes a working machine; under-triggering is recoverable).
- **Claude (non-rotating):** no refresh exists to consult — a provider rejection of the token itself
  (401/invalid-token on an authenticated request, persisting across a retry) is terminal.
- **Fixture-based tests (REQUIRED):** a transient 401 does NOT mark terminal; an **unknown** event
  does NOT mark terminal; `reauthenticationRequired` and refresh-reason `unauthorized` do NOT mark
  terminal (the excluded ex-candidates, kept as fixtures so they can never be reintroduced); the
  captured `account/updated` logged-out shape DOES; the Claude persisted-rejection case does.
  Fixtures are recorded payloads, so a protocol change breaks the test rather than silently changing
  classification.

## Credential + metadata layout, 0600

- **Codex canonical:** `CODEX_HOME/auth.json` (runtime-owned; `auth_mode`, `tokens{access_token,
  refresh_token,...}`). Tight Beam writes it ONCE at onboarding, then the runtime owns it.
- **Claude canonical:** the captured setup-token, stored 0600 and injected as `CLAUDE_CODE_OAUTH_TOKEN`
  at launch (non-rotating; re-onboard on 1-year expiry).
- **Lifecycle metadata** (Tight-Beam-owned, per host, 0600): `{provider, onboarded, last_health,
  subscription_status, terminal?, expires_at}`. `expires_at` is recorded at onboarding (Claude:
  the setup-token's ~1-year boundary; Codex: nil — the runtime rotates). This is NOT a copy of the
  live Codex token — it is status only.

## Discovery UX

`list`/org-options surfaces each provider's catalog `health` WITH reason (`unavailable — not
onboarded` / `unsupported (no subscription)` / `revoked`), never a silently empty model list.

## Migration — none (greenfield)

No production, no live deployment on the old harvest/per-archetype-home model to protect. Build the
target model directly; onboard shrdlu/eezo fresh. No add→onboard→retire cutover.

## Non-goals (v1)

- Keychain / OS secret-manager storage (0600 files stand).
- Per-agent distinct credentials (one per provider per host).
- A second refresher in Tight Beam (the Codex runtime refreshes; Claude is non-rotating).
- Proxying agent→provider HTTP.
- Cross-host credential sharing / a central broker (rejected — B5).
- API-key-primary auth; rotating Claude `/login` credential (rejected).

## Acceptance

- `tightbeam onboard openai` (device-code) writes a valid 0600 `CODEX_HOME/auth.json`; `tightbeam
  onboard anthropic` (setup-token over PTY, incl. carry-back code) captures + injects a valid token;
  the catalog validates models on the host where onboarding ran.
- Single Codex authority: a test proves `Tightbeam.Credentials` performs NO `auth.json` write while a
  Codex runtime is live, and runs no refresh loop.
- Claude non-rotating: a test proves the Claude path uses `CLAUDE_CODE_OAUTH_TOKEN` (no rotating
  `~/.claude/.credentials.json`); an N-session soak shows no `refresh_token_reused`/`invalid_grant`.
- Dead-credential contract: a test proves a single transient 401 does NOT mark a credential dead;
  only the runtime's terminal signal / a rejected non-rotating token does.
- Bounce (B2, replacement-conditioned): a test proves that on `mark_terminal` sessions PARK and NO
  restart occurs while the credential is still the revoked one; after `onboard` writes the
  replacement and metadata clears, the bounce runs and the resumed agent reads the NEW credential.
- No-subscription Claude surfaces `needs_onboarding: unsupported (no subscription)`, not a retry loop.
- Degraded journey: an un-onboarded provider shows `unavailable + reason` in `list`; a model-needing
  call raises `needs_onboarding` + the guided flow; an onboarded-provider spawn succeeds.
- Per-host: no credential transits between hosts; a satellite onboards independently.
- Notification is channel-neutral: the flow works with the local status/CLI baseline and no external
  service; any channel is optional.
- Security: every credential/metadata file is 0600.

## Implementation handoff

New per-host `Tightbeam.Credentials` (onboarding + lifecycle + status metadata; NO refresh/write of
live token) + `tightbeam onboard` (device-code for codex; setup-token-over-PTY for claude) + status
metadata store. Targeted edits: model_catalog (consult `status`, not a broker `resolve`); placement
(inject `CLAUDE_CODE_OAUTH_TOKEN`; Codex runtime launched against the onboarded `auth.json`);
adapter (surface the runtime's terminal auth signal to `mark_terminal`; bounce coordination);
gateway/org-options (surface health). Anti-stub: every invariant + acceptance item gets a
fail-on-revert test; genuinely-blocked items → HANDOFF with a named blocker.
