#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

usage() {
  cat <<'EOF'
Usage: configure-environment.sh --env-file PATH [--apply] [--yes]

Default: print the azd environment changes. --apply writes only local azd
environment state; it does not provision Azure resources.
EOF
}

ENV_FILE=""
APPLY=false
ASSUME_YES=false
while (($#)); do
  case "$1" in
    --env-file) ENV_FILE="${2:?--env-file requires a path}"; shift 2 ;;
    --apply) APPLY=true; shift ;;
    --yes) ASSUME_YES=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done
[[ -n "$ENV_FILE" ]] || { usage >&2; exit 2; }
[[ "$ENV_FILE" = /* ]] || ENV_FILE="$PWD/$ENV_FILE"
load_env_file "$ENV_FILE"

keys=(
  AZURE_SUBSCRIPTION_ID AZURE_LOCATION AZURE_AI_DEPLOYMENTS_LOCATION
  AZURE_RESOURCE_GROUP AZURE_AI_ACCOUNT_NAME AZURE_AI_PROJECT_NAME
  ENABLE_HOSTED_AGENTS ENABLE_CAPABILITY_HOST AZD_AGENT_SKIP_ACR ENABLE_MONITORING
  COPYWRITER_DEPLOYMENT_MODE
  CAMPAIGN_COORDINATOR_MODEL_NAME CAMPAIGN_COORDINATOR_MODEL_VERSION
  CAMPAIGN_COORDINATOR_MODEL_FORMAT CAMPAIGN_COORDINATOR_MODEL_SKU
  VISUAL_UNDERSTANDING_MODEL_NAME VISUAL_UNDERSTANDING_MODEL_VERSION
  VISUAL_UNDERSTANDING_MODEL_FORMAT VISUAL_UNDERSTANDING_MODEL_SKU
  CAMPAIGN_REASONING_MODEL_NAME CAMPAIGN_REASONING_MODEL_VERSION
  CAMPAIGN_REASONING_MODEL_FORMAT CAMPAIGN_REASONING_MODEL_SKU
  ADAPTIVE_COPY_MODEL_NAME ADAPTIVE_COPY_MODEL_VERSION
  ADAPTIVE_COPY_MODEL_FORMAT ADAPTIVE_COPY_MODEL_SKU
  MODEL_ROUTER_MODEL_NAME MODEL_ROUTER_MODEL_VERSION
  MODEL_ROUTER_MODEL_FORMAT MODEL_ROUTER_MODEL_SKU
  CREATIVE_IMAGE_MODEL_NAME CREATIVE_IMAGE_MODEL_VERSION
  CREATIVE_IMAGE_MODEL_FORMAT CREATIVE_IMAGE_MODEL_SKU
)
require_value AZURE_ENV_NAME
for key in "${keys[@]}"; do
  if [[ -n "${!key:-}" ]]; then
    printf 'azd env set %q %q\n' "$key" "${!key}"
  fi
done
[[ "$APPLY" == "true" ]] || { echo '[OK] Preview only; no local or Azure state changed.'; exit 0; }
confirm_word CONFIGURE "This will update local azd environment '$AZURE_ENV_NAME'." ||
  { echo 'Cancelled.'; exit 2; }

cd "$WORKSHOP_SRC"
azd env new "$AZURE_ENV_NAME" --no-prompt >/dev/null 2>&1 ||
  azd env select "$AZURE_ENV_NAME"
for key in "${keys[@]}"; do
  [[ -n "${!key:-}" ]] && azd env set "$key" "${!key}"
done
if [[ -z "${AZURE_PRINCIPAL_ID:-}" ]] && az account show >/dev/null 2>&1; then
  azd env set AZURE_PRINCIPAL_ID "$(az ad signed-in-user show --query id --output tsv)"
  azd env set AZURE_PRINCIPAL_TYPE User
fi
echo '[OK] Local azd environment configured. No Azure resources were provisioned.'
