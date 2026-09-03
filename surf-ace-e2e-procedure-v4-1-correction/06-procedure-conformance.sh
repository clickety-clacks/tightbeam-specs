#!/usr/bin/env bash

set -eu

bundle_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
fixture="$bundle_dir/fixtures/tick-0-read-success.json"
scope="pane:sf_0e2d0a73a98d:1"
content_id="soak-6fbbda0-linux-20260903-t0-sf_0e2d0a73a98d-pa"

# Rule 1: the captured successful local read has no result.ok and still passes.
. "$bundle_dir/05-read-response-validator.sh"
jq -e '(.result | has("ok")) | not' "$fixture" >/dev/null
surf_ace_read_response_ok 0 "$fixture" "$scope" "$content_id"

# Rule 2: read success alone cannot satisfy capture and render proof.
! surf_ace_render_proof_ok 0
! surf_ace_render_proof_ok 0 1 MATCH
! surf_ace_render_proof_ok 0 0 MISMATCH
surf_ace_render_proof_ok 0 0 MATCH
grep -Fq 'After a successful `read`, the harness must run `capture-pane` for the same surface and pane and must complete the render comparison. A successful `read` alone never produces a passing render result.' "$bundle_dir/01-gibson-cli-control-plane.md"

# Rule 3: this run uses one exact fact and scope, and fallback alone cannot advance it.
grep -Fq 'fact kind `surf-ace-capacity-6fbbda0-preflight-ready` with scope `wi_ef5e9b29-d440-4c39-b01b-58600569109b`' "$bundle_dir/01-gibson-cli-control-plane.md"
grep -Fq 'A fallback wake can report a missing fact. It never transfers custody and never advances the E2E operator.' "$bundle_dir/01-gibson-cli-control-plane.md"

# Rule 4: every operation revalidates the exact live binding or stops for preflight.
grep -Fq 'Immediately before each target operation, the operator verifies that the preflight row is unexpired and bound to the exact `controllerInstanceId`, state root, operator assignment, `surfaceId`, and `paneId`. If any field differs, the operator stops and obtains a fresh preflight before that operation.' "$bundle_dir/01-gibson-cli-control-plane.md"

printf 'procedure conformance: PASS\n'
