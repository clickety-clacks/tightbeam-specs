# What the Surf Ace compositor is for

This is the spirit of the Surf Ace Linux compositor: the problem it answers, what it should
achieve, what it is not, and the stances that decide close calls inside it. The Surf Ace product
spirit ([surf-ace-spirit-v1.md](surf-ace-spirit-v1.md)) governs this document; where they
conflict, the product spirit wins.

The product spirit already says how the compositor behaves under faults: bad optional settings,
runtime or display loss, uncertain identity or layout, stale or ambiguous updates, and requests
for capabilities that are physically unavailable. This document does not repeat or narrow that.

## The problem

Surf Ace clients decide which panes exist, what they show, where they sit, and in what order
operations happen. On a Linux appliance, something has to make that real on the physical screen:
draw the panes, host the native applications that run inside them, route touch, pointer and
keyboard input to the right place, and capture what is shown. The compositor does that. It is an
appliance component, not a desktop environment.

## What the compositor owns

- **Clients own the meaning.** Pane identity, layout, geometry, content mode, history and the
  order of operations belong to the Surf Ace clients. The compositor does not reinterpret them
  and does not fill in intent a client did not send.
- **The compositor owns the physical side.** It chooses the display output and rendering device,
  follows connector changes, applies rotation, hosts native applications, keeps physical focus,
  routes input, and captures the screen and panes.
- **Physical focus is local.** Which surface has keyboard focus on an appliance is that
  appliance's short-lived state. Which pane a user has selected in Surf Ace stays the client's.

## Outcomes

1. **What the user sees, touches and captures agree.** After a scale, rotation, mode or output
   change, the user never sees one layout while input lands on another, never captures old pixels
   under new coordinates, and never gets healthy status for a presentation that did not happen.
   A change that cannot be presented leaves the previous presentation in place and is reported
   truthfully.
2. **Ordinary display changes recover by themselves.** Moving a display to another connector needs
   no operator action.
3. **Input goes where the screen says.** Input reaches only surfaces in what is actually on screen.
   A request aimed at an old pane or presentation is never redirected to another pane by its
   label, the current selection, proximity or the current layout.
4. **One pane has keyboard focus, and Surf Ace shows which.** A native application's dialogs and
   other secondary windows belong to its pane. They may float outside the pane, over other panes
   and over Surf Ace's own controls. Only the focused pane's secondary windows are visible; every
   pane's main content stays visible. Focusing a pane and focusing a surface are separate: Surf Ace
   can take keyboard input back without changing which pane is focused.
5. **Losing focus hides; it does not close.** When a pane loses focus, its secondary windows are
   hidden but keep existing, with their position, size, stacking order and application state.
   Focusing the pane again brings back every one that still exists. A window the application
   really closes while hidden stays closed and is reported as closed.
6. **Content that disappears ends the interaction safely.** If focused or grabbed native content
   really disappears, the compositor cancels that interaction and returns focus and input to Surf
   Ace. It never hands the interaction to another pane or application.
7. **Launched applications leave lasting diagnostics.** Output from native applications the
   compositor launches goes to the appliance's persistent system journal and can still be read
   after the compositor and the application restart. Values shaped like tokens or credentials are
   removed before anything is written. The journal's own retention applies; the compositor keeps
   no separate log store.
8. **Operators can tell what the compositor did.** Durable diagnostics show the chosen backend,
   devices, connector, mode, rotation, presentation, the life of each launched application, and
   any recovery in progress.

## What the compositor is not

- **Not a desktop environment or general window manager.** No multi-monitor desktop management,
  global task switching or independent workspaces.
- **Not the owner of panes.** It does not decide pane layout, pane meaning or operation order.
- **Not a clipping box for secondary windows.** Keeping only the focused pane's secondary windows
  visible is how they are contained, not clipping or clamping them to the pane's rectangle.
- **Not a lifecycle event on blur.** Hiding a window because its pane lost focus is never treated
  as the window or application closing.
- **Not cross-platform, and not a general compatibility layer** for arbitrary Linux applications.

## Quality stances

- **Supported appliances first.** The compositor targets Linux appliances that Surf Ace declares
  supported. Portability beyond Linux and those appliances is a low priority, and that low priority
  never weakens support on the supported ones.
- **Realize, never reinterpret.** When the compositor and a client could each answer a question
  about panes, the client's answer wins.

## Open product gaps

These are not yet decided. Nothing in this document settles them.

- **Multi-screen behavior.** How the compositor should behave across more than one screen has been
  deferred. It must not be settled by whatever an implementation happens to do.
