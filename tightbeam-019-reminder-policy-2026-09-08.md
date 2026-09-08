# 0.1.9 selected reminder policy

8 September 2026. Lead selection under Mike's instruction to direct the team and carry the agreed judgment-led reliability work through 0.1.9 release. This is the selected product behavior for existing R1 `wi_d884d359-d1f2-4a1a-94c3-a8dbb90279ce`, design owner `asg_0175504c-f4a2-4c3c-806b-9a5753d318f2`. It resolves the pending timing choice; implementation and verified acceptance remain owed.

Adopt Morrow's elapsed-time recommendation below: first notice under existing eligibility, then minimum unchanged-notice gaps of 5, 15 and 30 minutes, retaining 30 minutes thereafter, measured from successful delivery. The cap limits added backoff, not total silence under valid waiting or a later existing reassessment. Material relevant evidence or an attributed consequence change can renew attention at the next existing evaluation. A successful notice about that changed expectation starts the unchanged-reminder sequence again. Ordinary progress prose and unrelated activity do not reset it.

The responsible technical owner chooses the exact supported consequence-record contract and atomic persistent placement. These are engineering decisions to finish with a bounded design, not a request for Mike to select schema fields. If the existing record contract cannot express an attributed material consequence tied to the obligation, propose the smallest concrete addition and its acceptance behavior to the lead. Do not claim prose parsing or unimplemented fields provide a deterministic signal.

Preserve effort decision authority/deadlines, qualified waits, bounded checkpoints, truthful delivery and recovery of unknown effects. Coalesce healthy pending delivery while preserving changed relevant information for owned reconsideration. A duplicate completion notification cannot advance backoff twice. Do not use notification success as outcome fulfillment.

The internal Main-authored stop recorded in `att_b691cd15` and `att_6f4815eb` must receive an explicit owner disposition under this selected policy before internal design work resumes. Its attribution as a direct Mike instruction was not supported by the inspected transcript. This selection does not erase historical records or infer success of failed handoffs.

Record the actual deployed configuration and relevant exposure for later external forensics. Evaluate fewer unchanged notifications alongside response to material changes, maintained reassessment, missed obligations and recovery. These numbers are a reasoned release choice, not an empirically established optimum. Pre-release acceptance remains required.

## Selected recommendation and acceptance examples

The following is Morrow's submitted proposal, retained as rationale and examples. Its former pending-selection language is historical; the lead disposition above governs.

# R1 reminder treatment proposal

Morrow, 2026-09-08. Proposal for the existing R1 owner and lead. Not a numeric ruling, implementation, or replacement for independent design review. Based on recorded R1 findings att_b19acfdb, att_5b79dc1f and att_27365d9b. No new source inspection or schema placement claim.

## Proposed product choice

Keep existing obligation reassessment and effort deadlines. For a repeated reminder about the same unchanged expectation, propose minimum notification gaps of 5 minutes, 15 minutes, then 30 minutes, retaining 30 minutes thereafter. The first otherwise-eligible reminder remains eligible under existing policy. Measure subsequent gaps from successful delivery, not scans or attempted delivery. These are notification eligibility thresholds, not a guarantee to send at those times: notification still requires an unmet expectation and no valid suppression or healthy pending delivery.

The proposed 30-minute cap limits added backoff delay; it does not promise a notice every 30 minutes when the underlying obligation is not due or is validly waiting. Reassessment continues independently. An authoritative material evidence or consequence change makes attention eligible at the next existing evaluation without waiting out unchanged-notice backoff. Keep the approved dependency-verifier contract and existing bounded checkpoints.

Rationale: a five-minute initial gap removes second-scale repetition while allowing an early follow-up; fifteen then thirty minutes reduces long unchanged streams. This is a selected recommendation for review, not an empirically established optimum. Counter-risk: an approaching consequence needs faster attention even with unchanged blocker evidence. The implementation therefore needs a supported consequence input or explicit owner-directed attention; it must not infer a deadline from prose. No schedule makes an unrecorded consequence detectable.

## Required design boundary

Bind evidence and consequence identity to the particular obligation, never general holder activity. Use a supported attributed owner record with explicit obligation identity for consequence changes. The existing design owner must identify that exact record contract or propose the smallest missing contract; no claim that a suitable current field exists.

Keep last successfully delivered evidence/consequence identity, next notification eligibility, backoff step and pending delivery lineage durable on the existing obligation mechanism. Exact table/field placement remains engineering work. Existing effort multipliers and evaluation watermarks are not substitutes. Use the existing transactional wake delivery path rather than a second outbox.

Advance backoff only on confirmed successful delivery of the relevant reminder. A queued wake coalesces duplicates but proves neither delivery nor fulfillment. Failure preserves prior successful-notice state and invokes supported delivery recovery. Unknown outcome requires reconciliation before replay; it must not create another independent notice. Recovery backoff remains separate from unchanged-notification backoff.

Do not suppress a required effort decision merely because an ordinary reminder is throttled. Shared delivery may combine compatible content only if the required decision, actor attribution and deadline remain intact. Otherwise preserve its existing delivery semantics until a reviewed design explicitly resolves overlap.

## Acceptance examples

- With an unmet unchanged obligation evaluated each minute, first delivery at minute 0 permits repeated deliveries no earlier than 5, 20, 50 and 80. Evaluations still occur each minute. No extra worker timers are created.
- If the next legitimate assessment after minute 5 is minute 12, the reminder can deliver at 12; its next unchanged eligibility is 27. The policy does not create a notification at minute 5 merely to satisfy the example.
- A material recorded consequence change at minute 21 permits attention at the next existing evaluation, despite prior eligibility at 50. Activity on another obligation does not do so.
- A valid dependency wait remains suppressed under its existing coverage. Backoff expiry does not cancel coverage or manufacture work.
- A failed attempt at minute 5 does not advance the success watermark or backoff step. Existing recovery owns the original intent; a pending healthy successor is reused.
- Restart before or after enqueue/delivery preserves eligibility and wake identity. Reconciliation prevents the same successful notification from advancing the step twice.
- A required effort decision remains due and actionable even during ordinary reminder backoff.

Next owner action: lead/PO decides the timing treatment; existing R1 technical owner settles consequence contract and persisted placement, then the existing release path commissions implementation and independent acceptance. The stop on further internal source mapping is not silently overridden by this proposal.
