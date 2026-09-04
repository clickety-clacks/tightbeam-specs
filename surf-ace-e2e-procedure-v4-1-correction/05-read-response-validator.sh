#!/usr/bin/env bash

# Source this file from a run-specific operator harness. Use the strict content
# validator immediately after a push. Use the joint current-state validator
# with the matching capture for a baseline, restoration, or later read with no
# new push.
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

surf_ace_current_read_capture_ok() {
  if [ "$#" -ne 7 ]; then
    return 64
  fi

  local read_exit_code="$1"
  local read_response_path="$2"
  local capture_exit_code="$3"
  local capture_response_path="$4"
  local expected_scope="$5"
  local expected_pane_id="$6"
  local expected_content_id="$7"

  [ "$read_exit_code" -eq 0 ] || return 1
  [ "$capture_exit_code" -eq 0 ] || return 1
  jq -e \
    --slurpfile capture "$capture_response_path" \
    --arg scope "$expected_scope" \
    --argjson paneId "$expected_pane_id" \
    --arg contentId "$expected_content_id" \
    '
      ($capture | length) == 1
      and (
        $capture[0] as $captureResponse
        | ([.result.records[]? | select(.recordClass == "content")]) as $contentRecords
        | .ok == true
        and .command == "read"
        and (.controllerInstanceId | type == "string" and length > 0)
        and .controllerInstanceId == $captureResponse.controllerInstanceId
        and $captureResponse.ok == true
        and $captureResponse.command == "capture-pane"
        and $captureResponse.result.ok == true
        and $captureResponse.result.op == "snapshot.get"
        and $captureResponse.result.payload.paneId == $paneId
        and $captureResponse.result.payload.contentId == $contentId
        and ($captureResponse.result.payload.contentType | type == "string" and length > 0)
        and ($captureResponse.result.payload.revision | type == "number")
        and ($captureResponse.result.payload.visibleText | type == "string")
        and ($captureResponse.result.payload.viewport | type == "object")
        and ($captureResponse.result.payload | has("selection"))
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
        and all(
          $contentRecords[];
          (.payload | type == "object")
          and (.payload.contentId | type == "string" and length > 0)
          and (.payload.revision | type == "number")
        )
        and (
          ($contentRecords | length) == 0
          or (
            ($contentRecords | max_by(.sequence) | .payload.contentId) == $captureResponse.result.payload.contentId
            and ($contentRecords | max_by(.sequence) | .payload.revision) == $captureResponse.result.payload.revision
          )
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
      )
    ' "$read_response_path" >/dev/null
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
  if [ "${1:-}" != "--self-test" ]; then
    printf 'usage: %s --self-test\n' "$0" >&2
    exit 64
  fi

  validator_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
  fixture="$validator_dir/fixtures/tick-0-read-success.json"
  current_empty_fixture="$validator_dir/fixtures/preflight-read-current-empty.json"
  current_capture_fixture="$validator_dir/fixtures/preflight-capture-current-semantic.json"
  expected_scope="pane:sf_0e2d0a73a98d:1"
  expected_content_id="soak-6fbbda0-linux-20260903-t0-sf_0e2d0a73a98d-pa"

  surf_ace_read_response_ok 0 "$fixture" "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 1 "$fixture" "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 <(jq '.ok = false' "$fixture") "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 <(jq '.result.cacheStatus = "stale"' "$fixture") "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 <(jq '.result.consumableLoss = {"generation":1}' "$fixture") "$expected_scope" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 "$fixture" "pane:wrong:1" "$expected_content_id" || exit 1
  ! surf_ace_read_response_ok 0 "$fixture" "$expected_scope" "wrong-content" || exit 1

  surf_ace_current_read_capture_ok 0 "$current_empty_fixture" 0 "$current_capture_fixture" "$expected_scope" 1 "$expected_content_id" || exit 1
  surf_ace_current_read_capture_ok 0 "$fixture" 0 <(jq '.controllerInstanceId = "ctl_79b1d809fab84b6badf8c0b43ff07cb2"' "$current_capture_fixture") "$expected_scope" 1 "$expected_content_id" || exit 1
  ! surf_ace_current_read_capture_ok 1 "$current_empty_fixture" 0 "$current_capture_fixture" "$expected_scope" 1 "$expected_content_id" || exit 1
  ! surf_ace_current_read_capture_ok 0 "$current_empty_fixture" 1 "$current_capture_fixture" "$expected_scope" 1 "$expected_content_id" || exit 1
  ! surf_ace_current_read_capture_ok 0 <(jq '.result.cacheStatus = "unsynchronized"' "$current_empty_fixture") 0 "$current_capture_fixture" "$expected_scope" 1 "$expected_content_id" || exit 1
  ! surf_ace_current_read_capture_ok 0 <(jq '.result.consumableLoss = {"generation":1}' "$current_empty_fixture") 0 "$current_capture_fixture" "$expected_scope" 1 "$expected_content_id" || exit 1
  ! surf_ace_current_read_capture_ok 0 <(jq '.result.records = [{"bytes":1,"payload":{"contentId":"wrong-content","revision":20},"recordClass":"content","recordId":"cr_wrong","sequence":20}] | .result.acknowledgement = {"scopeId":"pane:sf_0e2d0a73a98d:1"}' "$current_empty_fixture") 0 "$current_capture_fixture" "$expected_scope" 1 "$expected_content_id" || exit 1
  ! surf_ace_current_read_capture_ok 0 "$current_empty_fixture" 0 <(jq '.result.payload.contentId = "wrong-content"' "$current_capture_fixture") "$expected_scope" 1 "$expected_content_id" || exit 1
  ! surf_ace_current_read_capture_ok 0 "$fixture" 0 <(jq '.controllerInstanceId = "ctl_79b1d809fab84b6badf8c0b43ff07cb2" | .result.payload.revision = 19' "$current_capture_fixture") "$expected_scope" 1 "$expected_content_id" || exit 1
  ! surf_ace_current_read_capture_ok 0 "$current_empty_fixture" 0 <(jq '.controllerInstanceId = "ctl_wrong"' "$current_capture_fixture") "$expected_scope" 1 "$expected_content_id" || exit 1

  printf 'read-response validator self-test: PASS\n'
fi
