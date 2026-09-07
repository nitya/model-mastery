#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib/common.sh"

usage() {
  cat <<'EOF'
Usage: provision.sh [--env-file PATH] [--preview] [--apply] [--yes]

Runs online preflight first. Default is an Azure what-if preview. --apply
requires explicit confirmation and can create billable resources.
EOF
}

ENV_FILE="$WORKSHOP_ROOT/.env"
MODE=preview
ASSUME_YES=false
while (($#)); do
  case "$1" in
    --env-file) ENV_FILE="${2:?--env-file requires a path}"; shift 2 ;;
    --preview) MODE=preview; shift ;;
    --apply) MODE=apply; shift ;;
    --yes) ASSUME_YES=true; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown argument: $1" >&2; usage >&2; exit 2 ;;
  esac
done
[[ "$ENV_FILE" = /* ]] || ENV_FILE="$PWD/$ENV_FILE"
"$SCRIPT_DIR/preflight.sh" --env-file "$ENV_FILE" --online
cd "$WORKSHOP_SRC"
if [[ "$MODE" == "preview" ]]; then
  azd provision --preview --no-prompt
  echo '[OK] Preview complete; no resources were changed.'
  exit 0
fi
confirm_word PROVISION 'The reviewed plan can create chargeable Azure resources.' ||
  { echo 'Cancelled.'; exit 2; }
azd provision --no-prompt
echo '[OK] Provisioning completed. Review outputs with: azd env get-values'
