# Operator ruling provenance census — 2026-08-30

Status: immutable evidence capture for `wi_a8de6fe5-5450-41c8-ac9b-f623d349d0cc`.
This file contains no decision, rationale, question, message, session id, or private content.

## Source

- Store: live Gibson Tightbeam `state.db`, opened read-only.
- Live release: `0.1.8`, build `1337`, source stamp `fdb3db5`.
- Capture time: 2026-08-30 12:08:30 PT (`1788116910000`).
- Window start: 2026-08-20 00:00:00 PT.
- Window end: capture time.
- Population: `decision_requests.kind='operator'`, `ruledBy='user:mike'`, and a non-null
  `ruledAt` inside the window.

## Query

```sql
SELECT
  COUNT(*) AS total,
  SUM(ruledViaSessionKey IS NULL) AS no_via_session,
  SUM(ruledViaSessionKey IS NOT NULL) AS with_via_session,
  MIN(ruledAt),
  MAX(ruledAt)
FROM decision_requests
WHERE kind = 'operator'
  AND ruledBy = 'user:mike'
  AND ruledAt >= 1787209200000
  AND ruledAt <= 1788116910000;
```

## Result

| Measure | Count |
| --- | ---: |
| Mike-attributed operator rulings | 294 |
| `ruledViaSessionKey` absent | 291 |
| `ruledViaSessionKey` present | 3 |
| Distinct present session keys | 3 |
| Present keys resolving to a retained session row | 3 |
| Present keys resolving to a built-in personal session | 0 |

The first matching ruling is 2026-08-20 09:45:48 PT (`1787244348967`). The last is
2026-08-30 06:49:54 PT (`1788097794045`).

## Classification rule

- The 3 rows with a retained session key are **session-mediated legacy rulings**. The key proves
  a submitting session. The old row does not prove exact source bytes or actor principal.
- The 291 rows without a key are **legacy attribution unknown**. Absence does not prove direct
  user action. These rows may combine direct shell use, org-token use, lost transport
  attribution, or an intermediary path. This census does not choose among them.
- The census classifies 0 historical rows as **direct-user** because no retained field proves
  that class.

## Reproduction note

A rolling `capture_time - 10*24h` window returns 291 operator rows, not 294, because it excludes
three August 20 rows before 12:08:30 PT. The assignment's “in ten days” count uses the ten PT
calendar dates beginning at 00:00 PT on August 20. This file freezes that boundary explicitly.
