# What the Surf Ace compositor is for

This is the spirit of the Surf Ace Linux compositor: what it owns, the problem it answers, what it
should achieve and what it is not. The Surf Ace product spirit
([surf-ace-spirit-v1.md](surf-ace-spirit-v1.md)) governs this document; where they conflict, the
product spirit wins.

The product spirit sets the compositor's behavior for bad optional settings, uncertain identity or
layout, stale or ambiguous updates, and capture or measurement that is physically unavailable. This
document does not repeat it.

## The problem

Surf Ace clients decide which panes exist, what they show, where they sit and in what order
operations happen. On a Linux appliance, something has to make that real on the physical screen:
draw the panes, host the native applications inside them, route input to them and capture what is
shown. The compositor does that.

## What the compositor owns

- **Clients own the meaning.** Pane identity, layout, geometry, content and the order of
  operations belong to the Surf Ace clients. The compositor does not reinterpret them or fill in
  intent a client did not send.
- **The compositor owns the physical side.** It owns the display output and rendering device,
  rotation, the native applications it hosts, input routing and capture.

## Outcomes

1. **The screen agrees with itself.** What the user sees, where input lands, what a capture returns
   and the status the compositor reports all describe the same presentation: the one actually on
   screen.
2. **A lost display leaves the last good state.** When the display or its runtime is lost, the
   compositor keeps showing the last good state, says truthfully when a display is gone, and comes
   back when it returns.

## What the compositor is not

- **Not a desktop environment or general window manager.** No multi-monitor desktop management,
  global task switching or independent workspaces.
- **Not cross-platform, and not a general compatibility layer** for arbitrary Linux applications.

## Quality stances

- **Warn truthfully.** When the compositor cannot do something, it says so truthfully. This
  document promises no persistent diagnostics store or surface.
- **Supported appliances first.** The compositor targets the Linux appliances Surf Ace declares
  supported. Portability beyond them is a low priority and never weakens support on them.

## Open product gaps

- **Multi-screen behavior.** How the compositor should behave across more than one screen has been
  deferred. Nothing here settles it.
