#!/usr/bin/env bash

# Source this file from a run-specific operator harness. Pass the CLI exit code,
# response file, expected scope, and expected content id to the function below.
surf_ace_read_response_ok() {
  if [ "$#" -ne 4 ]; then
    return 64
  fi

  local exit_code="$1"
  local response_path="$2"
  local expected_scope="$3"
  local expected_content_id="$4"

  [ "$exit_code" -eq 0 ] || return 1
  jq -e \
    --arg scope "$expected_scope" \
    --arg contentId "$expected_content_id" \
    '
      .ok == true
      and .command == "read"
      and .result.scopeId == $scope
      and .result.acknowledgement.scopeId == $scope
      and .result.cacheStatus == "current"
      and any(
        .result.records[]?;
        .recordClass == "content"
        and .payload.contentId == $contentId
      )
    ' "$response_path" >/dev/null
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  if [ "${1:-}" != "--self-test" ]; then
    printf 'usage: %s --self-test\n' "$0" >&2
    exit 64
  fi

  validator_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
  fixture="$validator_dir/fixtures/tick-0-read-success.json"
  expected_scope="pane:sf_0e2d0a73a98d:1"
  expected_content_id="soak-6fbbda0-linux-20260903-t0-sf_0e2d0a73a98d-pa"

  surf_ace_read_response_ok 0 "$fixture" "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 1 "$fixture" "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 <(jq '.ok = false' "$fixture") "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 <(jq '.result.cacheStatus = "stale"' "$fixture") "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 "$fixture" "pane:wrong:1" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 "$fixture" "$expected_scope" "wrong-content" || exit 1

  printf 'read-response validator self-test: PASS\n'
fi
