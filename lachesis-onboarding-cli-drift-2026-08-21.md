# Lachesis onboarding CLI drift — 2026-08-21

Authority: Mike's live findings from 2026-08-21 18:33–18:40 UTC against the
Gibson service built from public `main` commit
`afd4948a374833228b1bf1fd8cc5147032ee439a`.

## Confirmed working

The provider-home busy check now scopes correctly. Both Codex and Claude login
jobs start even while unrelated organization adapter processes are running.

## Blocking gaps

1. Codex device authorization remains in `starting`. The current Codex CLI is
   version 0.149.0. It emits the official verification URL and one-time code as
   ANSI-colored, numbered prose. It offers no JSON output for this command.
   Lachesis must strip ANSI escapes and extract the URL and code by structural
   patterns, without matching surrounding sentence text. The API must publish
   `verification_url` and `user_code`, and normal cancellation, timeout, child
   exit, and credential-write completion must remain intact.

2. Claude paste-code authorization reaches `awaiting_user`, but the API has no
   operation that writes the submitted authorization code to the waiting CLI
   child's standard input. Lachesis must add the smallest code-submission API.
   The code must be accepted only for the matching active Claude job, written
   once to the live child, and never logged, stored, echoed, or returned. The
   existing cancellation, timeout, lock release, child exit, credential-write,
   and provider-home preservation rules remain binding.

## Acceptance

- One blocking-bar code review covers the combined repair.
- The verified commit fast-forwards public `main` and is rebuilt for
  Linux/amd64 with CGO disabled on Eezo.
- Only the Gibson systemd user service is restarted.
- Health and the loopback-only listener remain correct.
- A fresh Codex job publishes its official verification URL and one-time code
  through the API.
- A fresh Claude job accepts one pasted authorization code through the API and
  continues the existing job lifecycle.
- No password, MFA secret, token, authorization code, credential, live response
  body, account identifier, or private path enters public history or logs.

## Non-goals

- No broader onboarding redesign.
- No provider CLI pinning.
- No new UI.
- No unrelated account, service, unit, or credential change.
