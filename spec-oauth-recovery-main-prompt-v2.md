# OAuth recovery sends one complete procedure prompt to Main

Status: READY TO BUILD

Authority: Mike, 2026-08-20

Work item: `wi_92bc2577-4050-4d8a-8f97-bcba65bcddd3`

Supersedes: `art_e06563b7` and `art_83c3b17c`

## Spirit

After a successful OAuth recovery, Tightbeam sends one real runnable wake to
the authenticated operator's Main. The wake prompt contains the complete
recovery procedure. Main follows that prompt to find the declared main
archetype for every installed or learned Kung Fu, notify the live agents that
use those archetypes, and require those agents to inspect and resume any
stalled agent graph.

Tightbeam stays neutral. It only sends this complete prompt to Main. It does not
read Kung Fu manifests, identify product owners, select product-specific
agents, inspect their work, or decide which graph should resume.

This procedure is an event instruction, not standing guidance. Do not add or
change an identity file, archetype, Kung Fu guide, skill, manual rule, or other
persistent guidance to implement it.

## Exact boundary

On successful OAuth finish, the substrate schedules exactly one ordinary,
immediate prompt wake to the authenticated operator's Main session. The wake
uses the existing scheduler and delivery path with:

- `origin = "process:tightbeam"`;
- `consumer = "prompt"`;
- `targetGate = 1`;
- no product, work-item, assignment, archetype, or product-agent target;
- the full procedure prompt below.

The prompt must communicate this complete instruction in one wake:

> The OAuth token for `<provider>` on `<host>` was refreshed. Read the manifests
> for every installed or learned Kung Fu. Read each manifest's declared main
> archetype. Find live agents with those archetypes. Notify each that the OAuth
> token was refreshed, and require each to inspect and resume any stalled agent
> graph.

The implementation may add neutral correlation facts, but it must not shorten,
move, or replace any procedure clause. A reference to standing guidance, a
procedure name, or a transcript notice does not satisfy this contract.

Main performs the prompt through inference and native Tightbeam inspection and
messaging surfaces. In the current manifest shape, `root_archetype` is the
declared main archetype and `tightbeam kungfu list` exposes it as
`rootArchetype`. Main de-duplicates matching live agents before notification.
The substrate does none of that selection.

If Main retires or becomes non-runnable before delivery, the ordinary
`targetGate = 1` check suppresses the turn. Tightbeam does not fall back to a
product agent and does not fan out the wake.

## Proposed seam

Use the successful `finish` branch of `Gateway.onboard_phase`, immediately after
`Credentials.finish_onboard/4` returns `:ok` and before the wire response reports
the ceremony complete.

This seam knows the neutral recovery facts: success, provider, host, and the
authenticated caller. Preserve that principal through `onboard_result`. Resolve
only the caller's personal Main through the existing native Main mapping. Insert
one wake with `Wakes.schedule_in_txn/2`.

Do not use `publish_credential_sessions/3` to select targets. It enumerates
provider sessions and would move product policy into the credential substrate.
Its transcript and stream notices may remain for visibility, but they do not
count as recovery.

Wake insertion must succeed before the finish response reports success. If the
credential recovered but the wake transaction failed, return a typed partial-
success error that separately states those two facts. Do not substitute a
transcript message.

## Test proof

Focused Gateway and wake-path tests must prove:

1. Successful OAuth finish inserts exactly one immediate prompt wake to the
   authenticated caller's Main.
2. The stored wake uses `origin = "process:tightbeam"`, `consumer = "prompt"`,
   and `targetGate = 1`.
3. The stored prompt names provider and host and contains every procedure
   clause: every installed or learned Kung Fu; each manifest's declared main
   archetype; live agents with those archetypes; token-refreshed notification;
   and the requirement to inspect and resume any stalled agent graph.
4. The real Scheduler and Gateway path delivers that complete prompt unchanged
   into a runnable Main turn.
5. Multiple Kung Fu bundles, product owners, assignments, and live agents still
   produce one substrate wake to Main and no direct product-agent wake.
6. Retiring Main after insertion and before delivery produces no turn and no
   fallback.
7. Failed OAuth finish, provider start, or provider resume creates no Main wake.
8. Forced wake-transaction failure cannot return the ordinary `onboarded`
   response and reports credential recovery separately from wake failure.
9. The change set contains no identity, archetype guidance, Kung Fu guidance,
   skill, or manual edit. A test or review that moves the procedure out of the
   event prompt fails this design.

One disposable-org proof must use a real runnable Main. Install or learn at
least two fixture Kung Fu bundles with different declared main archetypes.
Start matching live agents and one unrelated agent. Complete OAuth recovery,
capture the single Main wake and turn, and prove that Main reads the manifests
and live roster, notifies every matching agent with the recovery fact and resume
requirement, and does not notify the unrelated agent.

The proof must preserve the real wake, manifest, roster, and message shapes. A
transcript insertion, mocked direct fan-out, abbreviated prompt, or standing
guidance dependency is not valid proof.

Run the unmodified Elixir gate first. After implementation, run
`mix format --check-formatted` and `scripts/verify_mix.sh` exactly as CI does.
Record baseline and final counts plus the focused and disposable-org evidence.

## Acceptance

The repair is complete when successful OAuth recovery schedules one runnable
wake to Main whose prompt contains the whole recovery procedure, Main performs
that procedure, non-runnable safeguards remain intact, and the substrate makes
no Kung Fu or product-agent selection.

## Subtraction ruling

A transcript notice does not create a turn. Direct substrate fan-out imposes
product policy below Main. Standing guidance makes the recovery behavior a
second source of truth. The smallest valid addition is one native Main wake
whose event prompt is complete.
