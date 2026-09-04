#!/usr/bin/env bash

# Source this file from the preflight harness. Pass a restoration summary that
# contains the baseline and restored semantic capture metadata plus both PNG hashes.
surf_ace_restoration_ok() {
  if [ "$#" -ne 1 ]; then
    return 64
  fi

  jq -e '
    def sha256:
      type == "string" and test("^[0-9a-f]{64}$");
    def complete_semantics:
      has("paneId")
      and has("contentId")
      and has("contentType")
      and has("revision")
      and has("visibleText")
      and has("selection")
      and has("viewport")
      and (.paneId | type == "number")
      and (.contentId | type == "string" and length > 0)
      and (.contentType | type == "string" and length > 0)
      and (.revision | type == "number")
      and (.visibleText | type == "string")
      and (.viewport | type == "object");
    def semantics:
      {paneId, contentId, contentType, revision, visibleText, selection, viewport};

    (.baselinePngSha256 | sha256)
    and (.afterRollbackPngSha256 | sha256)
    and (.baseline | complete_semantics)
    and (.afterRollback | complete_semantics)
    and ((.baseline | semantics) == (.afterRollback | semantics))
  ' "$1" >/dev/null
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  if [ "${1:-}" != "--self-test" ]; then
    printf 'usage: %s --self-test\n' "$0" >&2
    exit 64
  fi

  validator_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
  fixture="$validator_dir/fixtures/restoration-png-drift.json"

  surf_ace_restoration_ok "$fixture" || exit 1
  surf_ace_restoration_ok <(jq '.afterRollbackPngSha256 = .baselinePngSha256' "$fixture") || exit 1
  ! surf_ace_restoration_ok <(jq '.afterRollback.contentId = "wrong-content"' "$fixture") || exit 1
  ! surf_ace_restoration_ok <(jq '.afterRollback.visibleText = "stale visible text"' "$fixture") || exit 1
  ! surf_ace_restoration_ok <(jq '.afterRollback.revision -= 1' "$fixture") || exit 1
  ! surf_ace_restoration_ok <(jq 'del(.afterRollbackPngSha256)' "$fixture") || exit 1

  printf 'restoration oracle self-test: PASS\n'
fi
