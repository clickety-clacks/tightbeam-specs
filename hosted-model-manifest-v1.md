# Hosted model manifest v1 — curated model metadata served from tightbeam.ing

- Status: DRAFT r1 (mike, 2026-09-01). Filed for the Tightbeam product owner to assign and staff. Target lines: 0.1.9 and 0.2.0.
- Pattern: **t3code model manifest**, adopted as-is where it fits (pingdotgg/t3code `apps/server/src/provider/model-manifest.json`, `ModelManifest.ts`, `ClaudeModelCatalog.ts`, main @ 692eb1a5 2026-09-01).
- Related work items: `wi_3e1a8cf2-ddff-4885-b79e-32dd6d0ada27` (catalog withholds claude-fable-5-1), `wi_f331e232-90b8-48d5-a7f7-d1a3b7979ed5` (shipped kungfu names fable-5).
- Relation to prior specs: refines `derived-model-catalog-v1.md`, `per-host-catalogs-v1.md`, `model-identity-v1.md`. Where this spec and those disagree, see "Open decisions"; nothing here reintroduces an allowlist.

## Problem

`Tightbeam.Harness.Claude` (0.1.8) fetches the Anthropic `/v1/models` list and then withholds every model not in a compiled-in constant, `@adapter_selectable_models`, keyed to claude-agent-acp 0.66.0. The gateway logs: "model(s) the API offers are not selectable by claude-agent-acp 0.66.0 and were withheld". On 2026-09-01 all three hosts (gibson, eezo, racter) were re-onboarded for Anthropic; each catalog now shows exactly fable-5, opus-5, opus-4-8, sonnet-5, haiku-4-5 and nothing newer. `claude-fable-5-1` is withheld even though:

- the API offers it,
- the adapters on gibson were upgraded the same day to claude-agent-acp 0.73.0 / claude-agent-sdk 0.3.257, whose bundled Claude Code 2.1.257 selects it,
- the spec-writer and reviewer archetypes now default to it and fall through to gpt-5.6-sol xhigh.

The constant is a translation table (API id ↔ adapter picker string, e.g. `claude-fable-5` ↔ `claude-fable-5[1m]`) that was snapshotted into code. Every new Anthropic model therefore needs a gateway release. `derived-model-catalog-v1` already ruled "NO allowlist, NO sensible subset" for the substrate; the constant is a regression against that ruling that grew out of per-environment refusal measurements (see the comment trail in `lib/tightbeam/harness/claude.ex`).

## Goal

G1. Model metadata that changes between releases (which models exist, aliases, current/legacy status, capabilities, harness-version gates, adapter rendering rules) lives in one **data file**, not in compiled code.

- Acceptance: Given a new Anthropic model, when its row is added to the manifest and published, then `tightbeam list` on every host shows it within one manifest TTL with **no gateway release and no adapter reinstall**, provided the host's bundled Claude Code meets the row's `minVersion`.

G2. The gateway refreshes the manifest at runtime from `https://tightbeam.ing/model-manifest.json` and never fails a catalog read because the fetch failed.

- Acceptance: Given the droplet is unreachable, when the gateway boots or refreshes, then it serves the last on-disk copy, else the release-bundled copy, and logs one warning per retry window. `tightbeam list` returns promptly in every case.

G3. Offering is gated by the harness binary version the host actually runs, not by an adapter package version.

- Acceptance: Given a manifest row with `minVersion: 2.1.257` and a host whose bundled Claude Code is 2.1.220, when the catalog is derived for that host, then the row is absent for that host and the readiness report names the upgrade ("Claude Code v2.1.220 is too old for Fable 5.1; needs v2.1.257").

G4. An unknown slug passes through.

- Acceptance: Given an archetype default naming a model with no manifest row, when a spawn resolves it, then the structured identity is handed to the adapter unchanged; a vendor refusal advances the preference ladder exactly as today. Nothing is withheld for being unrecognized.

G5. No compiled-in model list remains as a source of truth in the Claude harness.

- Acceptance: `grep -n "claude-" lib/tightbeam/harness/claude.ex` matches only test fixtures and the package name.

## Design

### D1. The manifest file

One JSON document, schema versioned, additive. Shape follows t3code with Tightbeam's vocabulary (fields per `model-identity-v1`: family, effort, context — never a packed string).

```json
{
  "version": 1,
  "providers": {
    "claude": {
      "defaults": { "chat": "claude-sonnet-5" },
      "profiles": {
        "fable-5": {
          "efforts": ["low", "medium", "high", "xhigh", "max"],
          "defaultEffort": "high",
          "contexts": ["200k", "1m"],
          "defaultContext": "1m",
          "contextWindowTokens": { "200k": 200000, "1m": 1000000 },
          "adapter": { "claudeCode": { "contextSuffix": { "1m": "[1m]" } } }
        }
      },
      "models": [
        { "slug": "claude-fable-5-1", "name": "Fable 5.1", "aliases": ["fable", "fable-5.1"], "status": "current", "profile": "fable-5",
          "adapter": { "claudeCode": { "minVersion": "2.1.257" } }, "badge": "new" },
        { "slug": "claude-fable-5",   "name": "Fable 5",   "status": "legacy",  "profile": "fable-5",
          "adapter": { "claudeCode": { "minVersion": "2.1.169" } } },
        { "slug": "claude-opus-5",    "name": "Opus 5",    "aliases": ["opus", "opus-5"], "status": "current", "profile": "opus-5",
          "adapter": { "claudeCode": { "minVersion": "2.1.219" } } },
        { "slug": "claude-opus-4-8",  "name": "Opus 4.8",  "status": "legacy",  "profile": "opus-4-8" },
        { "slug": "claude-sonnet-5",  "name": "Sonnet 5",  "aliases": ["sonnet", "sonnet-5"], "status": "current", "profile": "sonnet-5" },
        { "slug": "claude-haiku-4-5-20251001", "name": "Haiku 4.5", "aliases": ["haiku"], "status": "legacy", "profile": "haiku-4-5" }
      ]
    },
    "codex": {
      "models": [
        { "slug": "gpt-5.6-sol",   "status": "current" },
        { "slug": "gpt-5.6-terra", "status": "current" },
        { "slug": "gpt-5.6-luna",  "status": "current" },
        { "slug": "gpt-5.5",       "status": "legacy" },
        { "slug": "gpt-5.4",       "status": "legacy" }
      ]
    }
  }
}
```

Rules:

- `slug` is the vendor's canonical id, opaque, and the only identity (`derived-model-catalog-v1` §Canonical ref). Aliases are convenience lookups that resolve to a slug at the CLI seam; stored selections (archetype defaults, preferences) always hold slugs.
- `profile` carries capabilities and the adapter rendering rule. Rendering `[1m]` happens only inside the Claude adapter from the structured `context` field (`model-identity-v1` §What moves). No `[…]` string exists outside the adapter.
- `adapter.claudeCode.minVersion` / `maxVersionExclusive` gate offering per host by the bundled Claude Code version (`node_modules/@anthropic-ai/claude-agent-sdk-linux-x64/claude --version` or the `CLAUDE_CODE_EXECUTABLE` override), probed on the owning host per `per-host-catalogs-v1` §Design 2.
- `status: legacy` is a presentation hint for clients and the kungfu tables; the substrate still offers legacy rows that pass the version gate.
- For codex the manifest is an overlay only (status, name). The live per-host codex derivation stays as is; codex already publishes `minimal_client_version` natively.
- Efforts are Tightbeam's vocabulary. t3code's `ultracode`/`ultrathink` are not adopted.

### D2. Precedence and freshness

Order: remote fetch → last successful on-disk copy (`~/.tightbeam/model-manifest.json`) → release-bundled copy (`priv/model-manifest.json`). Constants, matching t3code: TTL 1 h, retry gap after failure 5 min, fetch timeout 10 s. The fetch runs in a spawned task and never inside a call a reader awaits (`derived-model-catalog-v1` I4). The manifest's health state is reported alongside the catalog's existing `fresh | stale | unavailable(reason)` (§Freshness contract) as a separate `manifest:` field so a stale manifest is never mistaken for a stale credential.

A manifest that fails schema validation is rejected whole; the previous good copy stays in force and one warning names the failing field. Validation: unique slugs, every `profile` reference exists, every `defaults.chat` names a listed slug, every version string parses as semver, `minVersion < maxVersionExclusive`.

### D3. What the Claude harness does with it

Offered set for `{host, claude}` = manifest rows whose version gate passes on that host. The compiled `@adapter_selectable_models` constant and its withholding branch are deleted. See Open decision O1 for the fate of the `/v1/models` fetch.

Spawn / tune / set-model resolve alias → slug via the manifest, build the structured identity, and hand it to the adapter. A slug with no manifest row is passed through with the profile defaults of the nearest family match, else no capabilities (G4). Refusals keep the house style: harness, host, and the repair on that host, with the version-upgrade message from G3 when a gate is the cause.

### D4. Publishing

- Source of truth: `priv/model-manifest.json` in the tightbeam repo. Bundled into every release.
- Publish: a release step (or a `mix tightbeam.manifest.publish` task) copies the committed file to the droplet at `/var/www/tightbeam.ing/model-manifest.json` over the existing `tbing` ssh alias on gibson. Nginx serves it as `application/json` with `Cache-Control: public, max-age=300` and an ETag. No auth, no CORS needed.
- A manifest change is a data commit plus a publish. Adding a model is one row and a `minVersion`. The existing `model-release-intake` skill's step 4 ("sweep archetypes") now also says "add the manifest row".

### D5. Hosting facts (recon 2026-09-01)

| Item | Value |
|---|---|
| Droplet | `tightbeam-ing-sfo3`, DigitalOcean sfo3, IPv4 143.198.229.224, IPv6 2604:a880:4:1d0:0:3:5817:c000 |
| OS / web | Ubuntu, kernel 6.8, nginx 1.24.0, certbot present, ufw allows OpenSSH + Nginx Full |
| Access | root over ssh from gibson via alias `tbing` (key lives on gibson). No doctl anywhere. |
| Serving today | `blog.tightbeam.ing` only: root `/var/www/blog.tightbeam.ing`, Let's Encrypt cert for that one name (expires 2026-11-19), HTTP→HTTPS redirect. Static files, copied by hand; no git, no cron, no deploy script. |
| DNS | Nameservers are Porkbun's. `blog.tightbeam.ing` → A 143.198.229.224. The apex `tightbeam.ing` has **no A/AAAA record**. Nobody on gibson/eezo/racter/this machine holds Porkbun or DigitalOcean API credentials. |
| Disk | 24 GB, 11% used |

Consequences: serving `https://blog.tightbeam.ing/model-manifest.json` needs only a file copy and works today. Serving from the apex needs (a) an A and AAAA record at Porkbun, which only mike can add, then (b) a second nginx server block with `server_name tightbeam.ing` and `certbot --nginx -d tightbeam.ing`. Both are ten-minute jobs once DNS resolves.

## Non-goals

- No change to codex derivation, credentials, or the per-host probe seam.
- No admin refresh verb; TTL is enough (matches `derived-model-catalog-v1` §Hardening).
- No pricing, usage, or cost data in the manifest.
- No client-side curation rules beyond `status`; grouping and hiding stay with clients and kungfu tables.
- No rewrite of `preferred-models.md` capsules; that is `wi_f331e232` and the intake ceremony.

## Open decisions (owner)

O1. **Fate of the Claude `/v1/models` fetch.** Default (t3code-exact): retire it; the manifest is the offered set and the vendor's answer at turn time remains the authority (`per-host-catalogs-v1` §Design 7). Alternative: keep it and offer manifest ∩ API, so a host whose account lacks a model never sees it. The alternative preserves more of `per-host-catalogs-v1` but keeps a second fetch and its 401-masking failure mode alive.

O2. **Canonical URL.** Default: `https://tightbeam.ing/model-manifest.json`, with `https://blog.tightbeam.ing/model-manifest.json` served from the same file as the interim URL until the apex record exists. The gateway's fetch URL is a config value with the apex as its default.

O3. **Who runs the publish step.** Default: the release ceremony on gibson, since the ssh alias and key live there.

## Acceptance tests

- T1 Manifest schema: bundled file validates; a duplicate slug, a dangling profile, or `minVersion >= maxVersionExclusive` is rejected with the field named.
- T2 Precedence: remote 200 → cached copy written; remote 500/timeout → cached copy served, `manifest: stale`; no cache, no remote → bundled copy served, `manifest: unavailable(reason)`.
- T3 Version gate: host at 2.1.220 omits fable-5-1 and reports the upgrade string; host at 2.1.257 offers it.
- T4 Passthrough: spawn with `--model claude-not-in-manifest` reaches the adapter with that slug; adapter refusal advances the ladder.
- T5 Rendering: `--model claude-fable-5-1 --context 1m` renders `claude-fable-5-1[1m]` inside the adapter and nowhere else; `tightbeam list` output contains no `[`.
- T6 Reader latency: `tightbeam list` returns within its existing budget while a manifest fetch is hung.
- T7 End to end: with the manifest published on the droplet and gibson's adapters at 0.73.0 / SDK 0.3.257, `tightbeam spawn --archetype spec-writer` selects claude-fable-5-1 high, and `tightbeam list` shows it on gibson, eezo, and racter after their adapters are brought to the same versions.

## Handoff

Successor cards the owner should open: (1) manifest schema + loader + precedence (T1, T2, T6); (2) Claude harness migration off the constant, version gate, passthrough, rendering (T3, T4, T5); (3) droplet publish step + nginx block, plus a decision request to mike for the apex DNS record (O2); (4) adapter version bump to 0.73.0 / 0.3.257 in the release so every host meets fable-5-1's gate (T7). Card 2 supersedes `wi_3e1a8cf2`'s "extend the allowlist" reading; the allowlist is deleted, not extended.
