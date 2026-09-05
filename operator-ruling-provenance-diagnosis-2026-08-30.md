# Operator ruling provenance diagnosis — 2026-08-30

Status: immutable, content-free source-path report for
`wi_a8de6fe5-5450-41c8-ac9b-f623d349d0cc`.

Source baseline: Tightbeam `ea3e9c1879978b9362d30eea8973352d9dce8c1b`. Live census
baseline: release `0.1.8`, build `1337`, source stamp `fdb3db5`.

## Finding

Mike rulings lose provenance because the system projects an asserted user identity into the
binding authority slot before it retains the authenticated submitting actor and exact source.
The terminal row then gives the intermediary's answer the durable label `user:mike`. The exact
Mike message, when one exists, remains in a separate conversation row with no typed edge to the
ruling. Downstream readers therefore see the weaker representation as the authoritative fact
and cannot recover whether Mike wrote, confirmed, delegated, or was paraphrased.

## Write path

1. The CLI converts `--as-user mike` to `asUser:"mike"` (`cli/src/dispatch.rs:56-62`). Its
   operator-rule payload carries the request, decision or response, and rationale, but no
   exact-source reference (`cli/src/dispatch.rs:453-470`).
2. A session credential with `asUser:"mike"` becomes origin `user:mike` and principal
   `{:user,"mike"}` (`lib/tightbeam/wire/router.ex:584-607`). This erases the distinction
   between “the authority is Mike” and “the authenticated actor is this session” unless the
   transport session is retained separately.
3. Current `main` builds the call without `transport_session_key`
   (`lib/tightbeam/wire/router.ex:503-517`). The `0.1.8` line retained
   `authenticated_session_key(auth)` beside projected identity
   (`origin/0.1.8:lib/tightbeam/wire/router.ex:129-148,568-569`). Current `main` therefore
   regressed the only transport carrier used by the operator writer.
4. The writer derives `ruledBy` from the request owner. It reads the submitting session only
   from `call.transport_session_key`, then stores authority, performer principal, and session
   state on the terminal row (`lib/tightbeam/escalation.ex:2462-2503`). With the current router,
   real HTTP calls reach that writer with no transport session.
5. Authorization accepts the owner user principal. It rejects the personal Main proxy only
   when `transport_session_key` equals that personal session
   (`lib/tightbeam/escalation.ex:3540-3552`). The router omission makes that refusal ineffective
   on the real HTTP path even though direct unit calls can inject the field.

## Relay and source path

An operator request schedules a process-authored wake to the owner's personal session with the
request question and option list (`lib/tightbeam/escalation.ex:2386-2392,3689-3691`). The
personal session or another agent can then submit an answer. The terminal mutation schedules a
second process wake to the raiser and may stamp its creator session
(`lib/tightbeam/escalation.ex:2471-2480`). Neither wake stores the id or digest of the
Mike-authored message that supports the answer. The row therefore proves delivery and
submission plumbing, not authorship of the decision text.

This is the **paraphrased-wake path**: Mike's exact words arrive in a message; an intermediary
forms an answer; `--as-user mike` makes that answer terminal; no typed edge distinguishes the
two texts.

## Read, UI, and event path

Current `main` projects terminal operator attribution through
`rulingAttribution.onBehalfOf`, performer principal state, and performer session state
(`lib/tightbeam/escalation.ex:3011-3064`). Missing performer fields project as
`legacy-unknown`; a retained old session key projects as known. This is correct legacy
presentation, but it cannot supply exact-source evidence that was never stored.

The shared decision-request serializer uses that terminal projection
(`lib/tightbeam/state_resources.ex:559-562`). Firehose maps `operator-rule` to the existing
`decision_request.ruled` class (`lib/tightbeam/firehose/publisher.ex:23-29`). Its refs carry
the projected call principal and ordinary ids (`lib/tightbeam/firehose/publisher.ex:484-494`),
not the exact source message. UI, REST, and Firehose therefore inherit the same evidence gap.

## Path classification

| Path | What retained rows prove | Safe label |
| --- | --- | --- |
| authenticated user device directly confirms | user credential plus exact submitted bytes, after the proposed seam exists | direct-user |
| authenticated session submits | submitting session key, when retained | session-mediated |
| old terminal row has no submitting session | only `ruledBy='user:mike'` | legacy attribution unknown |
| Mike message is relayed and an agent calls `operator-rule --as-user mike` | Mike message and terminal ruling exist without a typed source edge | paraphrased-wake |

The live 294-row census supplies 3 session-mediated legacy rows and 291 legacy-unknown rows. It
supplies no proven direct-user row.

## Authority inversion

The evidence order is backward. A direct Mike message has authenticated authorship and exact
bytes, but it is not joined to the ruling. An agent paraphrase has neither property, yet the
terminal row labels it `user:mike`, and the row is what agents are instructed to obey. The
system promotes the weaker representation over the stronger source.

The proposed repair restores the order:

1. retain the exact source and its digest;
2. retain the authenticated submitting actor, session, and transport;
3. store the authority principal separately;
4. keep recommendations non-binding unless policy grants explicit typed delegation;
5. let only a binding confirmation terminalize the request.

## Why the proposal adds one carrier

Deleting session impersonation closes the unsafe binding surface, but it does not preserve
recommendations or exact user evidence. Accepting terminal text without a source keeps the
known defect. One immutable submission carrier is the smallest mechanism that retains both
non-binding agent work and the evidence for a binding confirmation. It adds no decision state
machine: the existing decision-request row remains the sole open/ruled outcome.
