# Credential kinds — v1

Decided 2026-07-28 (Flynn). Ruled as an INVARIANT, not a feature: Tight Beam
supports BOTH credential kinds — API key and subscription token — for BOTH
harnesses, and reports which kind is active to the client over the clawline
protocol.

## Problem

Today the product supports exactly one kind per harness: claude's subscription
setup-token, codex's ChatGPT OAuth. No API-key handling exists anywhere
(verified 2026-07-28 — no ANTHROPIC_API_KEY / OPENAI_API_KEY path in lib/).
Both harnesses natively support API keys; the product just never wires them.
Flynn ruled the gap a deficit.

## Invariants

1. **Both kinds, both harnesses, per host.** Each host's auth store holds one
   ACTIVE credential per provider, of either kind. Kind is host-local config —
   satellite A may run claude on an API key while satellite B runs it on a
   subscription token. No global assumption anywhere.
2. **The active kind is reported to the client over clawline.** Per SESSION —
   a session's kind is the kind active for {its host, its harness's provider}
   at read time. Wire: camelCase like everything else on the clawline wire
   (`credentialKind: "apiKey" | "subscription"`), surfaced wherever the
   session's display/status shape already reports harness and model, and in
   session-status reads. Absence of a credential reports as its own state,
   not as a missing field.
3. **Every credential-consuming seam dispatches on kind.** Known seams and
   their per-kind shapes (verified where noted):
   - claude env injection: subscription → `CLAUDE_CODE_OAUTH_TOKEN`;
     api key → `ANTHROPIC_API_KEY`.
   - codex auth.json: subscription → `tokens.{...}` (ChatGPT mode);
     api key → the `OPENAI_API_KEY` field (native codex mode, field exists
     today, null under subscription).
   - claude catalog probe: subscription → bearer token (works today, 28
     models observed); api key → `x-api-key` header on the same
     `/v1/models` route.
   - codex catalog probe: subscription → `chatgpt.com/backend-api/codex/models`
     (verified 200); api key → `api.openai.com/v1/models` (API keys carry
     `api.model.read`, the scope the subscription token was refused for —
     verify empirically before relying on it).
   - preflight liveness probes (#15/#81 territory): per-kind endpoints as
     above.
4. **Onboarding gains a key path.** API-key onboarding is non-interactive:
   the operator supplies the key, the ceremony validates it live (one
   authenticated models call), banks it with metadata recording the kind.
   No browser, no device code, no TUI — which also means none of #80's
   machinery is on this path. The interactive subscription ceremonies are
   unchanged.
5. **Kind is recorded in credential metadata** (`credential.json` gains
   `"kind"`), and everything that reads the store dispatches on it rather
   than sniffing file shape. One authority.
6. **Rotation posture differs by kind and the code must know it.** API keys
   are static — no rotation, no refresh, no single-writer constraint.
   Subscription: claude static (year-long setup-token), codex self-rotating
   (in-place, single writer — the shared-runtime constraint). Liveness and
   expiry reporting (#81) dispatch on kind.

## Non-goals

- No changing the default or recommending a kind; both are first-class.
- No credential transit between machines, ever, either kind.
- No auto-conversion between kinds.

## Acceptance

1. Per harness: an org whose host holds ONLY an API key runs a real turn and
   derives a live catalog; same for subscription-only. All four cells.
2. Mixed fleet: gateway on subscription, satellite on API key (or reverse) —
   catalogs per host reflect each host's own kind; spawns validate correctly
   (per-host-catalogs already keys this).
3. A client reading session status sees `credentialKind` for its session's
   host, and the value flips when the host's active credential changes kind.
4. API-key onboarding: non-interactive, validates live before banking,
   failure names the provider/host/kind.
5. Metadata records kind; nothing sniffs file shape to infer it.
