# Operator ruling provenance migration fixture — 2026-08-30

This fixture is a privacy-safe, row-level evidence capture used by migration acceptance T3 in
\`operator-ruling-provenance-v1.md\`.

## Source and boundary

- Store: live Gibson Tightbeam \`state.db\`, opened read-only.
- Release: \`0.1.8\`, build \`1337\`, source stamp \`fdb3db5\`.
- Window: 2026-08-20 00:00:00 PT through 2026-08-30 12:08:30 PT, inclusive.
- Selection: operator decision requests ruled by \`user:mike\` in that window.

## Redaction transform

The capture reads only \`id\`, \`ruledAt\`, and \`ruledViaSessionKey\`. It reads no question,
option, context, decision, rationale, message, attachment, raw session key, or raw request id.

1. Sort selected rows by \`ruledAt,id\`.
2. Replace the raw row id and timestamp with one-based \`ordinal\`.
3. Map a null \`ruledViaSessionKey\` to \`sessionState:"legacy-unknown"\` and
   \`sessionSlot:null\`.
4. Sort distinct non-null raw session keys. Replace each with its one-based dense rank as
   \`retained-session-<two digits>\`, and emit \`sessionState:"known"\`.
5. Emit only \`ordinal\`, \`kind\`, \`authority\`, \`sessionState\`, and \`sessionSlot\`.

The transform preserves the observed legacy shape while removing identifiers and private content.
\`rows.jsonl\` contains 294 rows: 291 legacy-unknown rows and 3 known rows
with 3 distinct pseudonymized slots.

## Consumer contract

T3 reads \`rows.jsonl\` as JSON Lines. Each row has exactly this evidence schema:

| Key | Value |
| --- | --- |
| \`ordinal\` | one-based positive integer unique within this file |
| \`kind\` | literal \`operator\` |
| \`authority\` | literal \`user:mike\` |
| \`sessionState\` | \`legacy-unknown\` or \`known\` |
| \`sessionSlot\` | null for \`legacy-unknown\`; otherwise \`retained-session-01\`, \`retained-session-02\`, or \`retained-session-03\` |

The known labels are dense ranks of the three distinct retained raw session keys. They prove only
that the old row retained a key. A null slot proves only that the old row did not retain one. Neither
label proves direct-user authorship. The current migration projects each pre-epoch row as \`unknown\`;
it does not copy this evidence label into the product projection.

The row fixture remains immutable point-in-time evidence. A replacement capture uses this same
transform and becomes a separate dated artifact; it does not overwrite this file.
