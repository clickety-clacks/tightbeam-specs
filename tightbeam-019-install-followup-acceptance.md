# 0.1.9 installer follow-up acceptance

8 September 2026. Backing requirements for existing work item `wi_0c8ebb58-ac04-4353-8ff9-d435e64c1e28` (key `mike-019-install-followup-seven-days`). Mike authorized this requirement in the ClipMesh discussion and transferred it to the stalls-and-churn lead. Main subsequently closed that coordination item and retained the unmet requirement in successor `wi_cb0a4962-9f07-420e-92eb-26686454d249`. Reuse the successor; preserve the original history.

## Purpose

Prompt an external forensic review seven days after verified Gibson 0.1.9 installation. Review the design decisions in `tightbeam-019-agent-judgment-plan.md` and the change ledger in `tightbeam-learning-loop-v1.md` against actual use. This is follow-up improvement of a release already required to meet its engineering acceptance; it is not the release's initial correctness check.

## Required installer behavior

1. After verifying the published, hash-verified 0.1.9 release is installed and running on Gibson, retain the verification evidence and timestamp. Schedule an absolute-time wake at that timestamp plus 604800000 milliseconds. Installation and service actions retain their existing authorization requirements.
2. Address the reminder to `--user mike`, with the purpose, backing documents and installation evidence. This destination is the stalls-and-churn lead's routing decision; ClipMesh's earlier release-owner recipient was an assumption. The installer owns scheduling, not the external assessment's conclusion.
3. Record the stable installation identity, immutable verification timestamp, recipient, due time and returned wake ID in durable linked records. Retry must not create duplicate follow-ups for the same installation. Reconcile an unknown scheduling outcome before issuing another request.
4. Keep scheduling failures visible and retryable. Successful installation does not imply successful scheduling, and a scheduling error does not falsify the installation verification. This requirement is fulfilled only when scheduling and its evidence are established.
5. The reminder asks for external evaluation of actual outcomes, contrary cases and actual exposure to the changed behavior. Insufficient exposure produces a scoped finding and next action; it does not postpone the authorized installation-based reminder.

## Acceptance cases

- Verified installation produces one recorded reminder due exactly seven days after its recorded verification time.
- Retrying the same installation or recovering an uncertain scheduling result preserves one reminder and the original time anchor.
- Scheduling failure is visible with an owned retry; neither a successful install nor a queued coordination message is reported as a completed follow-up requirement.
- The review can distinguish installation from actual loaded guidance/rule versions and relevant use. Unknown exposure remains unknown.

A direct installer-scheduled wake needs no new installation-fact watcher. A watch's fallback duration starts when the watch is created and would not implement this timing requirement.

## Delivery boundary and current status

A Tightbeam wake is a notification. It does not independently run an external forensic agent or guarantee delivery while the gateway is down. Keep the due obligation externally discoverable through retained records. An external patrol can adopt a due unassigned review item, but that independent engagement path still needs an owner and working trigger; this installer item does not silently claim to deliver it.

The PO's coordination assignment `asg_e07250bb-b653-4310-a6cb-ffd223b22e39` retained these requirements but surrendered after the existing CI owner found no authorized installer. Main turn 124270 then closed the original item and created iceboxed successor `wi_cb0a4962-9f07-420e-92eb-26686454d249`, currently without assignments, for attachment to future authorized installation work. The requirement remains unmet. This corrects the prior report that the original item was still open. No installation timestamp or actual seven-day wake exists in this handoff. Preserve that status until implementation and scheduling evidence change it.
