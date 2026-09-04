#!/usr/bin/env bash

# Source this file from a run-specific operator harness. Use the strict content
# validator immediately after a push. Use the current-state validator for a
# baseline, restoration, or later read with no new push.
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
      and .result.consumableLoss == null
      and any(
        .result.records[]?;
        .recordClass == "content"
        and .payload.contentId == $contentId
      )
  ' "$response_path" >/dev/null
}

surf_ace_current_read_response_ok() {
  if [ "$#" -ne 3 ]; then
    return 64
  fi

  local exit_code="$1"
  local response_path="$2"
  local expected_scope="$3"

  [ "$exit_code" -eq 0 ] || return 1
  jq -e \
    --arg scope "$expected_scope" \
    '
      .ok == true
      and .command == "read"
      and .result.scopeId == $scope
      and .result.cacheStatus == "current"
      and (.result | has("acknowledgement") and has("consumableLoss") and has("records"))
      and .result.consumableLoss == null
      and (.result.records | type == "array")
      and all(
        .result.records[];
        type == "object"
        and (.bytes | type == "number")
        and has("payload")
        and (.recordClass | type == "string" and length > 0)
        and (.recordId | type == "string" and length > 0)
        and (.sequence | type == "number")
      )
      and (
        (
          (.result.records | length) == 0
          and .result.acknowledgement == null
        )
        or (
          (.result.records | length) > 0
          and .result.acknowledgement.scopeId == $scope
        )
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
  current_empty_fixture="$validator_dir/fixtures/preflight-read-current-empty.json"
  expected_scope="pane:sf_0e2d0a73a98d:1"
  expected_content_id="soak-6fbbda0-linux-20260903-t0-sf_0e2d0a73a98d-pa"

  surf_ace_read_response_ok 0 "$fixture" "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 1 "$fixture" "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 <(jq '.ok = false' "$fixture") "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 <(jq '.result.cacheStatus = "stale"' "$fixture") "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 <(jq '.result.consumableLoss = {"generation":1}' "$fixture") "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 "$fixture" "pane:wrong:1" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 "$fixture" "$expected_scope" "wrong-content" || exit 1

  surf_ace_current_read_response_ok 0 "$current_empty_fixture" "$expected_scope" || exit 1
  surf_ace_current_read_response_ok 0 "$fixture" "$expected_scope" || exit 1
  ! surf_ace_current_read_response_ok 1 "$current_empty_fixture" "$expected_scope" || exit 1
  ! surf_ace_current_read_response_ok 0 <(jq '.result.cacheStatus = "unsynchronized"' "$current_empty_fixture") "$expected_scope" || exit 1
  ! surf_ace_current_read_response_ok 0 <(jq '.result.consumableLoss = {"generation":1}' "$current_empty_fixture") "$expected_scope" || exit 1
  ! surf_ace_current_read_response_ok 0 <(jq '.result.acknowledgement = {"scopeId":"pane:wrong:1"}' "$current_empty_fixture") "$expected_scope" || exit 1
  ! surf_ace_current_read_response_ok 0 <(jq '.result.records = [{"recordClass":"content"}] | .result.acknowledgement = {"scopeId":"pane:sf_0e2d0a73a98d:1"}' "$current_empty_fixture") "$expected_scope" || exit 1

  printf 'read-response validator self-test: PASS\n'
fi
