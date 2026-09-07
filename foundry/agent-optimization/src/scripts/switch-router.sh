#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

usage() {
  cat <<'EOF'
Usage: switch-router.sh --env-file PATH [--offline|--preview|--apply] [--yes]

Remaps the existing adaptive-copy deployment from fixed GPT-5.4-mini to the
verified Model Router catalog entry. Default is Azure what-if preview.
--offline prints the intended change without Azure calls. --apply requires
typing SWITCH unless --yes is supplied.
EOF
}

ENV_FILE=""
MODE=preview
ASSUME_YES=false
while (($#)); do
  case "$1" in
    --env-file) ENV_FILE="${2:?--env-file requires a path}"; shift 2 ;;
    --offline) MODE=offline; shift ;;
    --preview) MODE=preview; shift ;;
    --apply) MODE=apply; shift ;;
    --yes) ASSUME_YES=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done
[[ -n "$ENV_FILE" ]] || { usage >&2; exit 2; }
[[ "$ENV_FILE" = /* ]] || ENV_FILE="$PWD/$ENV_FILE"
load_env_file "$ENV_FILE"
for key in MODEL_ROUTER_MODEL_NAME MODEL_ROUTER_MODEL_VERSION MODEL_ROUTER_MODEL_FORMAT MODEL_ROUTER_MODEL_SKU; do
  require_value "$key"
done

cat <<EOF
Deployment: adaptive-copy
Current intent: ${ADAPTIVE_COPY_MODEL_FORMAT}/${ADAPTIVE_COPY_MODEL_NAME}/${ADAPTIVE_COPY_MODEL_VERSION}
New intent:     ${MODEL_ROUTER_MODEL_FORMAT}/${MODEL_ROUTER_MODEL_NAME}/${MODEL_ROUTER_MODEL_VERSION}
SKU:            ${MODEL_ROUTER_MODEL_SKU}
EOF
[[ "$MODE" != "offline" ]] || { echo '[OK] Offline preview only; no state changed.'; exit 0; }

"$SCRIPT_DIR/preflight.sh" --env-file "$ENV_FILE" --online
cd "$WORKSHOP_SRC"
if [[ "$MODE" == "preview" ]]; then
  ADAPTIVE_COPY_MODEL_NAME="$MODEL_ROUTER_MODEL_NAME" \
  ADAPTIVE_COPY_MODEL_VERSION="$MODEL_ROUTER_MODEL_VERSION" \
  ADAPTIVE_COPY_MODEL_FORMAT="$MODEL_ROUTER_MODEL_FORMAT" \
  ADAPTIVE_COPY_MODEL_SKU="$MODEL_ROUTER_MODEL_SKU" \
  COPYWRITER_DEPLOYMENT_MODE=routed \
    azd provision --preview --no-prompt
  echo '[OK] What-if complete; no deployment was changed.'
  exit 0
fi

confirm_word SWITCH 'This replaces the model behind adaptive-copy and can affect cost/latency.' ||
  { echo 'Cancelled.'; exit 2; }
azd env set ADAPTIVE_COPY_MODEL_NAME "$MODEL_ROUTER_MODEL_NAME"
azd env set ADAPTIVE_COPY_MODEL_VERSION "$MODEL_ROUTER_MODEL_VERSION"
azd env set ADAPTIVE_COPY_MODEL_FORMAT "$MODEL_ROUTER_MODEL_FORMAT"
azd env set ADAPTIVE_COPY_MODEL_SKU "$MODEL_ROUTER_MODEL_SKU"
azd env set COPYWRITER_DEPLOYMENT_MODE routed
azd provision --no-prompt
echo '[OK] adaptive-copy now maps to the configured Model Router deployment.'
