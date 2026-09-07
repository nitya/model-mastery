#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib/common.sh
source "$SCRIPT_DIR/lib/common.sh"

usage() {
  cat <<'EOF'
Usage: preflight.sh [--env-file PATH] [--online]

Validates local files and model parameters without changing Azure. --online
also performs read-only authentication, catalog, SKU, and quota checks.
EOF
}

ENV_FILE="$WORKSHOP_ROOT/sample.env"
ONLINE=false
while (($#)); do
  case "$1" in
    --env-file) ENV_FILE="${2:?--env-file requires a path}"; shift 2 ;;
    --online) ONLINE=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done
[[ "$ENV_FILE" = /* ]] || ENV_FILE="$PWD/$ENV_FILE"
load_env_file "$ENV_FILE"

failures=0
for command in python3 az azd; do
  if command -v "$command" >/dev/null 2>&1; then
    printf '[OK] %s is installed.\n' "$command"
  else
    printf '[ACTION] Install %s.\n' "$command"
    failures=$((failures + 1))
  fi
done

required=(
  AZURE_SUBSCRIPTION_ID AZURE_LOCATION AZURE_AI_DEPLOYMENTS_LOCATION
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
for name in "${required[@]}"; do
  require_value "$name" || failures=$((failures + 1))
done

python3 "$SCRIPT_DIR/validate-assets.py" --root "$WORKSHOP_SRC" ||
  failures=$((failures + 1))

if [[ "$ONLINE" == "true" && "$failures" -eq 0 ]]; then
  az account show --subscription "$AZURE_SUBSCRIPTION_ID" --output none ||
    { echo '[ACTION] Authenticate with Azure CLI and select the intended subscription.'; exit 1; }
  azd auth login --check-status >/dev/null ||
    { echo '[ACTION] Authenticate azd with: azd auth login'; exit 1; }

  catalog="$(
    az cognitiveservices model list \
      --subscription "$AZURE_SUBSCRIPTION_ID" \
      --location "$AZURE_AI_DEPLOYMENTS_LOCATION" \
      --output json
  )"
  CATALOG_JSON="$catalog" python3 "$SCRIPT_DIR/verify-model-catalog.py"

  echo '[INFO] Quota is subscription-, region-, model-, and SKU-specific:'
  az cognitiveservices usage list \
    --subscription "$AZURE_SUBSCRIPTION_ID" \
    --location "$AZURE_AI_DEPLOYMENTS_LOCATION" \
    --query "[?currentValue < limit].{name:name.localizedValue,used:currentValue,limit:limit}" \
    --output table
  echo '[ACTION] Instructor: verify displayed quota covers every deployment capacity in src/azure.yaml.'
  echo '[ACTION] For partner models, verify Marketplace offer acceptance and purchasing permissions.'
fi

if ((failures)); then
  printf '[ACTION] Preflight found %d blocking local issue(s).\n' "$failures" >&2
  exit 1
fi
echo '[OK] Preflight completed without making changes.'
