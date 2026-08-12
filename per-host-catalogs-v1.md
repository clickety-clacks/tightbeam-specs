# Per-host model catalogs — v1

Decided 2026-07-28 (Flynn). Supersedes the implicit design in which every
harness's catalog is derived once, on the gateway, from the gateway's own
credential.

## Problem

Credentials are host-local by design; catalogs were gateway-global. With mixed
accounts per satellite a SUPPORTED configuration (ruled 2026-07-28), spawn and
set_model validate a model ref against the GATEWAY account's catalog while the
turn executes under the TARGET host account's entitlements (#88). Both failure
directions exist: validated-then-fails-at-runtime (masquerading per #81), and
refused-though-runnable. Secondary artifacts of the same centralization: the
gateway must hold a credential for every harness even satellite-only ones
(SATELLITE.md), and a fresh org looks for codex's `models_cache.json` on a host
where codex has never run (#67, in part).

## Principle

Facts about a host are established on that host. Secrets never travel; answers
derived from them do. A model list is a fact, not credential material.

## Design

1. **`ModelCatalog` keyed by `{host, harness}`**, not `harness`. Existing
   freshness/degraded states carry over per entry unchanged.
2. **Claude probe runs on the owning host.** The fetch is a plain
   `GET /v1/models` with a bearer token read off local disk — not an ACP or
   harness surface. Local host: current behavior. Remote host: execute over
   placement's existing ssh seam with the token read remotely
   (`$(cat …/auth/claude/oauth-token)` evaluated by the remote shell — the same
   pattern turn launch uses; the token never transits, never appears in a
   command line). The JSON model list returns.
3. **Codex probe runs on the owning host, as a direct HTTPS fetch — the cache
   file is retired.** Established empirically 2026-07-28 (codex-cli 0.145.0):
   `GET https://chatgpt.com/backend-api/codex/models?client_version=<v>` with
   `Authorization: Bearer <tokens.access_token from auth.json>` returns the
   account's live catalog (200, `{"models": [...]}`), and
   `Codex.derive_catalog_entries/1` parses the payload unchanged. The platform
   route (`api.openai.com/v1/models`) is confirmed closed to this token —
   403, missing scope `api.model.read`. Two sharp edges, both mandatory:
   - `client_version` is a SILENT catalog filter: a too-low value returns 200
     with an empty models list (each model carries `minimal_client_version`).
     The probe MUST pass the version of the `codex` binary ON THAT HOST
     (`codex --version` — the binary is an operator prerequisite there), never
     a constant.
   - The access token is read from the owning host's `auth.json` by the
     remote shell (same no-transit pattern as claude); extraction of
     `tokens.access_token` runs on that host (node is a stated prerequisite).
   Codex rotates this token itself (~10-day lifetime, refreshed mid-life);
   the probe is a read-only second reader, which is acceptable — but see the
   symlink-vs-rename question under Open. `models_cache.json` is no longer
   read anywhere; #67 dissolves entirely.
4. **Validation consults the target host's entry.** spawn / set_model /
   set_harness / tune resolve placement first, then validate the ref against
   `{target_host, harness}`. Refusals keep the house style: name the harness,
   the HOST, and the repair on that host.
5. **Readiness reports per `{host, harness}`.** The boot summary names which
   hosts can run which harnesses instead of one global judgment.
6. **The gateway needs credentials only for harnesses it runs.** The
   SATELLITE.md rule requiring a gateway credential for satellite-only
   harnesses is retired; docs updated in the same change.
7. **Runtime remains the authority.** The catalog is the substrate's belief;
   the vendor's answer at turn time is final, and #81 covers making the gap
   legible when belief and reality drift between refreshes.

## Non-goals

- No credential movement of any kind, in either direction.
- No new token classes (that is #82, separately specced).
- No change to TIGHTBEAM_DEFAULT_MODEL being a single global (#48) beyond the
  fact that it is now judged against the target host's catalog at selection
  time rather than one central one.
- No cache generation for codex — superseded: the cache is retired outright
  by the direct probe (design point 3), and #67 closes with it.

## Open

- Codex writes `auth.json` refreshes by an unknown mechanism: in-place write
  (a symlink into our auth store stays coherent) or rename-to-replace (the
  rename would swap the symlink for a regular file and strand the store on a
  pre-refresh token). Homes links the credential with `ln -s`
  (`homes.ex:187`), so this determines whether store-token freshness can be
  relied on. Being settled empirically, read-only.

## Acceptance

1. With two hosts whose claude catalogs differ (injected fetches), a spawn
   targeting host B validates against B's catalog, not the gateway's — both
   failure directions covered by tests.
2. A satellite-only harness with no gateway credential: spawn onto the
   satellite succeeds; nothing demands a gateway grant.
3. An unreachable host degrades its `{host, harness}` entries only; local
   entries stay fresh; the refusal names the host.
4. The codex probe for a remote host targets that host's own `auth.json` and
   that host's own `codex --version` — never the gateway's. A refused grant
   degrades that `{host, harness}` entry carrying the vendor's own error
   sentence; an empty-list response names the client_version and the host and
   does NOT implicate the credential (upgrade codex there is the repair,
   re-onboarding is explicitly the wrong one).
5. No test or production path shells credentials between machines; the remote
   probe's command line carries no token bytes (asserted, per the eurisko
   method: the token is read by the remote shell, not interpolated).
