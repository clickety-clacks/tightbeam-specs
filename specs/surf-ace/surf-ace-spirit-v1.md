# What Surf Ace is for

This is Surf Ace's product spirit: the problem it answers, what it should achieve, what it is not,
and the stances that decide close calls. It covers the whole product: the client apps, the
registry, the Linux compositor, the protocol that connects them, and the command-line tool that
speaks it. A component's own documents may say more about that component. Where one of them
conflicts with this document, this document wins.

## The problem

Surf Ace turns screens into surfaces that people, scripts and agents can address. A caller pushes
content to a pane, reads what a pane shows, captures it, and collects what users annotate on it.
Desktop clients run on Linux and macOS, and an iOS client runs on iPhone and iPad. A registry keeps track
of the clients and surfaces on a network. On Linux appliances, a compositor puts client panes and
native applications on the physical screen.

These pieces run on different machines, come from different releases, and meet real hardware.
Configuration is sometimes wrong. A peer is sometimes older or newer than the one it talks to. A
display can disappear, and a reply can arrive incomplete. Surf Ace has to meet all of that and keep
working.

The product standard is:

> "the job of the product is to function or do its best regardless of faults and
> incompatibilities. Just like the job of a web browser is to show something regardless of the
> correctness of the html."

## Outcomes

1. **Surf Ace keeps working through faults and incompatibilities.** This holds in the app, the
   registry, the compositor and the protocol. An unexpected, missing, renamed or inconsistent field,
   an older or newer peer, or a partial reply gets the best available behavior. It does not get a
   refusal of the whole operation.
2. **Every fallback is visible.** When Surf Ace works around a fault, a warning says what was wrong.
   Best effort is never silent, and a fallback is never presented as the thing that was asked for.
3. **Refusals are deliberate.** A whole-operation refusal stays only where the operator explicitly
   requested it. Keeping or adding any other whole-operation refusal needs the operator's explicit
   decision. It is not an implementation choice, and no component document can make it on the
   operator's behalf. Everything else gets the best available behavior.
4. **The screen keeps showing.** The compositor never stops all of its work because of a fault. It
   behaves as follows:
   - **Bad optional settings.** When an optional setting, mode or control feature is wrong or will
     not start, the compositor warns and uses the default. Every display and control capability
     the fault does not touch keeps running.
   - **Runtime loss.** When the display or rendering runtime fails, the compositor keeps the last
     good presentation and keeps its clients. It warns and recovers by itself. If a display is
     physically gone, it says so truthfully and comes back when the display returns. It never
     terminates the main app, and the rest of the product keeps running.
   - **Uncertain identity or layout.** When the compositor cannot be sure which pane a surface
     belongs to, it keeps the surface showing, warns, and marks the surface unresolved. It does not
     bind the surface to a pane it may not belong to, it does not redirect input on a guess, and it
     does not close the surface. It binds the surface once it is sure again.
   - **Stale or ambiguous updates.** The compositor never applies a stale or ambiguous display
     update to the wrong pane, and never sends input to the wrong pane. It keeps the last good
     state, warns and continues. It never rejects the update or closes anything over it.
5. **Missing capabilities are named, request by request.** A request for a capability that is
   physically unavailable gets an explicit error that names the reason. Per-request errors are
   reserved for that case. For example, a compositor screen capture or measurement with
   nothing to capture or measure gets an error, and the compositor stays up. An empty result is
   never passed off as success, because a fake empty capture misleads more than an error does. An
   error on one request is not a refusal of the whole operation.
6. **Requests and replies are salvaged, not thrown away.** This holds in the apps, the registry
   and the command-line tool.
   - **Per item, not all or nothing.** One bad item in a request or reply does not spoil the good
     ones. Surf Ace applies what is good, warns about the rest, and retries only the affected
     items.
   - **Local content and unaffected functions stay.** A fault never takes away content already on
     the device, or a function the fault does not touch.
   - **Nothing is made up.** Surf Ace never fabricates an identity, an endpoint lease or content.
     It never applies anything to the wrong client, pane or window.
   - **Uncertain saved state holds back one write, not all of them.** When Surf Ace cannot be sure
     what it has saved, it warns and keeps working. It holds back only the specific write that
     cannot be made safely.
7. **Old and new versions work together.** Already-shipped older and newer clients and servers
   interoperate in both directions. When a reply changes shape, for example to report results item
   by item, it still works with the versions already out there, and a mismatch gets a warning
   rather than a failure.

## What best effort is not

- **Not stopping on doubt.** Doubt is not a reason to stop.
- **Not stopping everything for one fault.** No component halts all of its work, or the product,
  because one setting, peer, field or device is faulty.
- **Not terminating the main app because the compositor lost its display or runtime.**
- **Not closing a surface only because its identity is uncertain.**
- **Not guessing.** Showing something never means putting content or input into a client, pane
  or window it may not belong to.
- **Not pretending.** A fallback, empty result or default is never reported as full success, and
  no identity, endpoint lease or content is made up to fill a gap.

## Quality stances

- **Function over strictness.** The product's job is to function or do its best regardless of
  faults and incompatibilities. Given a choice between strict refusal and the best
  available behavior with a warning, Surf Ace takes the best available behavior.
- **Honest degradation.** Best effort always says what it could not do. A visible warning goes with
  every fallback, and a physically unavailable request gets its reason.
- **Last good state over blank or wrong state.** When new state cannot be applied safely, Surf Ace
  keeps the last good state rather than showing nothing or showing the new state in the wrong place.
- **This document over component documents.** Where a component document says to reject, close or
  stop on a fault or on ambiguity, this document governs.

## Open product gaps

These are not yet decided. Nothing in this document settles them.

- **Where warnings appear.** This document requires that warnings be visible. It does not say who
  sees them or where: on the screen, to the caller, or in the product's diagnostics.
- **More than one compositor on a screen.** Whether a second compositor should ever run alongside
  one that is already running has not been decided.
