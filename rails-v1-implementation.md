# Rails v1 — implementation spec (gate tier ONLY; supersedes all prior versions)

This document REPLACES every earlier revision of itself. The previously
implemented "remind tier" (standing-law guidance sections, UserPromptSubmit
injection, Stop-hook bounces) violates the system's core invariant and MUST
BE REMOVED as part of this work.

THE INVARIANT (bible §rails, binding): **rails never add guidance.** A rail
contributes ZERO bytes to any model's context — no standing sections, no
reminders, no injected obligations. Rails create deterministic guardrails,
period. The ONLY text a rail ever emits is the refusal reason at the moment
it fires, delivered by the enforcing mechanism itself. Anything an agent is
meant to *read* belongs in guidance or a skill.

Repo: `~/src/tightbeam_ex` (Elixir). Gate: `mix compile --warnings-as-errors`
clean and `mix test` fully green. Follow the existing comment discipline:
moduledocs state invariants and WHY, never narrate code. Match the voice of
`lib/tightbeam/archetypes.ex`. Never touch code unrelated to this spec.

## Part 1 — REMOVE the remind tier (all of it)

From the current tree, delete entirely:

- `Rails.standing_law/0` and every call site (the guidance suffix in
  `Placement.deliver_home` — guidance goes back to EXACTLY
  `Archetypes.guidance(archetype)`, byte-identical, statutes or not).
- All `UserPromptSubmit` and `Stop` hook compilation, including the
  `stop_hook_active` machinery and `escape_double_quoted` if unused after.
- Statute events `work-received` and `turn-end`, and `mode = "remind"`.
- Every remind-related test and the remind examples in
  `docs/statutes.toml.example`.

A test must pin the invariant: projected guidance for an org WITH statutes
is byte-identical to guidance for an org WITHOUT them, for BOTH harnesses.

## Part 2 — the gate tier

A gate statute compiles to a Claude Code `PreToolUse` hook: the harness
presents every proposed tool call to the hook BEFORE execution; on match
the hook exits 2 and the call is REFUSED — the action never happens, no
inference in the loop. The refusal text reaches the model as the denial
reason (the one sanctioned emission: law learned by hitting it). State the
honest limit in the Rails moduledoc: pattern matching over command strings
is accident-grade enforcement — adversarial containment belongs to
sandboxes and credentials; gates stop mistakes deterministically.

### Schema

Location unchanged: `<base_dir>/identity/rails/*.toml`, filename order,
loaded fail-closed by `Rails.load!/1` from `Gateway.children/1`, stored in
`:persistent_term`. Missing dir / zero files → `[]` (valid).

```toml
[[statute]]
name = "no-history-rewrites"   # required; unique; ^[a-z0-9][a-z0-9-]*$
on   = "tool-call"             # required; the ONLY valid event in v1
mode = "gate"                  # optional; default AND only valid mode "gate"
tool = "Bash"                  # required; exact harness tool name
pattern = "git (reset|stash|rebase|checkout \\.|restore|clean)"
                               # required; POSIX ERE matched against the
                               # tool-call input
text = "History-rewriting git commands are forbidden here: other agents may have uncommitted work in this tree."
                               # required; the refusal reason
```

Validation table (each error raises `ArgumentError` at load; messages must
contain the quoted fragments verbatim):

| Input | Error must contain |
|---|---|
| `mode = "remind"` | `rails never add guidance; put prose in guidance or a skill` |
| `mode = "block"` | `mode "block" is reserved for a later stage` |
| `check = "..."` (key present) | `"check" (predicate statutes) is reserved for a later stage` |
| `mode = "nonsense"` | `unknown statute mode` |
| `on = "turn-end"` (or anything ≠ tool-call) | `unknown statute event` |
| missing `on` | `statute no-history-rewrites is missing "on"` |
| missing `tool` | `is missing "tool"` |
| missing `pattern` | `is missing "pattern"` |
| missing or blank `text` | `is missing "text"` |
| missing `name` | `statute is missing "name"` |
| `name = "Bad_Name"` | `invalid statute name` |
| duplicate names across files | `duplicate statute name: x` |
| unknown key (e.g. `sevrity`) | `unknown statute keys` and the key name |
| `pattern = "("` | `invalid gate pattern` (validate via `Regex.compile/1`) |

Persisted shape: ordered list of
`%{name: String.t(), on: :tool_call, mode: :gate, tool: String.t(),
pattern: String.t(), text: String.t()}`.

### Compilation — `Rails.claude_settings/0`

`nil` when no statutes; else a settings map delivered exactly as before via
`extra_files: %{"settings.json" => JSON.encode!(...)}` in
`Placement.deliver_home`, for `:claude` homes only. Codex homes get NOTHING
(no hook surface exists; per the invariant, no advisory text either — an
unenforceable rule on codex simply does not exist there, and the moduledoc
says so). No statutes → no key, no file: an org without law is byte-
identical to today (a test pins manifest-hash stability for both
harnesses).

Shape for the example statute:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "sh -c 'grep -qE \"git (reset|stash|rebase|checkout \\\\.|restore|clean)\" - || exit 0; echo \"[gate: no-history-rewrites] History-rewriting git commands are forbidden here: other agents may have uncommitted work in this tree.\" >&2; exit 2'"
          }
        ]
      }
    ]
  }
}
```

Mechanics (state in the moduledoc): the hook receives the tool-call JSON on
stdin; `grep -qE` runs the statute's pattern against it; no match → exit 0
(allow); match → statute text to stderr, exit 2 (harness refuses the call
and shows the model the reason). One `PreToolUse` entry per statute, load
order, `matcher` = the statute's `tool`. Commands are self-contained — no
file paths, no environment dependencies (homes live at different paths on
gateway, staging, and satellites). The pattern is matched against the RAW
JSON line (no jq dependency on satellites); document the caveat that
patterns should not rely on matching bare `"` characters.

Escaping: pattern and text are embedded in double quotes inside the
single-quoted `sh -c` payload. Apply, in order: BACKSLASH FIRST
(`\`→`\\` — a pattern's own backslash must never pair with a later escape
and un-escape it at hook runtime), then `"`→`\"`, `$`→`\$`,
backtick→backslash-backtick within the double-quoted strings; then the
whole payload single-quote-escaped by `'` → `'\''`. Pin a torture test:
pattern containing `.`, `|`, parentheses, and a `$`; text containing a
single quote (e.g. `Don't rewrite history.`) — assert the exact compiled
command string.

### `docs/statutes.toml.example`

Replace its contents with two gate statutes — `no-history-rewrites` (the
example above) and `no-push-main` (`pattern = "git push[^&|;]*\\b(main|master)\\b"`,
text naming the rule) — plus a 4-line header: copy into
`<base_dir>/identity/rails/`, restart to apply, gates are claude-only
today, a statute change regenerates homes (sessions lose model memory,
visibly).

### Tests

1. Every validation-table row.
2. Zero statutes: `[]`, `claude_settings/0` nil, no settings.json
   projected, manifest hash identical to a no-rails world (both harnesses).
3. Guidance byte-identity with statutes present (both harnesses) — the
   invariant test.
4. Byte-pinned settings for the example statute; the escaping torture case.
5. Ordering across two files.
6. Integration in `placement_test.exs`: gate statute present → local claude
   home has settings.json with the PreToolUse entry and CLAUDE.md WITHOUT
   any statute text; codex home has neither.

### Acceptance

- `mix compile --warnings-as-errors` clean; `mix test` fully green.
- Only these files change: `lib/tightbeam/rails.ex`,
  `lib/tightbeam/placement.ex`, `docs/statutes.toml.example`,
  `test/rails_test.exs`, `test/placement_test.exs`. (`gateway.ex` keeps its
  existing `Rails.load!` call — untouched.)
- Do not commit; leave the tree for review.
- If any instruction here conflicts with the tree or another spec, STOP
  and report instead of improvising.
