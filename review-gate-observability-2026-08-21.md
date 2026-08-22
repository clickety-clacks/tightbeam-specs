# Review gate — observability trio (Sol blind round, 2026-08-21)

Reviewer: GPT-5.6-Sol xhigh, blind, via the codex lane. Scope:
event-firehose-v1.md r5 + rest-state-api-v1.md r1 (r2 amendment's five
known corrections excluded from scope) + rest-vs-cli-adjudication.md r2,
reviewed as one design. VERDICT: BLOCKER, 24 findings. tb02 adjudication
of the findings follows separately; disposition: firehose-side folds are
tb02's, REST-side findings route to product-owner:rest-state-api
(wi_cb5734eb).



## tb02 re-adjudication of F20 (2026-08-21, after Mike's question)

Mike asked whether F20's connect-ticket fix was gymnastics forced by his
use-existing-credentials ruling. It was not — and the ruling contains the
fix: the existing chat socket authenticates IN-BAND (connect plain, auth
frame with the credential as the first message, auth_result; wire/socket.ex
— how Clawline connects from browsers today). The firehose socket
authenticates identically. F20 downgrades from design-hole to one missing
spec sentence, landing in firehose r6: auth is the chat socket's in-band
auth frame, same credential, same failure behavior. The ticket idea is
withdrawn.

## F23 resolution (Mike, 2026-08-22)

Overruled the accepted-risk drop: a sanity cap of 100 subscriptions per
connection lands in firehose S5 (typed refusal on the 101st). The
no-limits ruling stands for replay/admission.