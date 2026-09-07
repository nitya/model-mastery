#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

usage() {
  cat <<'EOF'
Usage: cleanup.sh [--preview|--apply] [--yes]

Default: list the active azd environment and resources without deleting them.
--apply requires typing DELETE and runs azd down --purge --force.
EOF
}

MODE=preview
ASSUME_YES=false
while (($#)); do
  case "$1" in
    --preview) MODE=preview; shift ;;
    --apply) MODE=apply; shift ;;
    --yes) ASSUME_YES=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done
cd "$WORKSHOP_SRC"
echo 'Active azd environment:'
azd env get-values 2>/dev/null | sed -E 's/(KEY|TOKEN|SECRET|CONNECTION_STRING)=.*/\1=<redacted>/I' || true
echo 'Azure resources that match the azd environment tag:'
resource_group="$(azd env get-value AZURE_RESOURCE_GROUP 2>/dev/null || true)"
if [[ -n "$resource_group" ]]; then
  az resource list --resource-group "$resource_group" \
    --query "[].{name:name,type:type,location:location}" --output table
else
  echo '[WARN] AZURE_RESOURCE_GROUP is not set; nothing can be targeted safely.'
fi
[[ "$MODE" == "apply" ]] || { echo '[OK] Preview only; nothing deleted.'; exit 0; }
[[ -n "$resource_group" ]] || exit 1
confirm_word DELETE "This permanently deletes '$resource_group', deployments, and telemetry." ||
  { echo 'Cancelled.'; exit 2; }
azd down --purge --force
echo '[OK] azd-managed workshop resources deleted.'
