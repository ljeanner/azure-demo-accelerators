#!/usr/bin/env bash
# Pause or resume the Fabric capacity created by this stack.
#
# A running F-SKU capacity bills by the hour whether or not anyone uses it.
# Pause it the moment the demo is over.
#
#   ./scripts/capacity.sh pause
#   ./scripts/capacity.sh resume
#   ./scripts/capacity.sh status
#
# Reads the capacity and resource group from the Terraform outputs, so there is
# nothing to hardcode.

set -euo pipefail

ACTION="${1:-status}"
INFRA_DIR="${INFRA_DIR:-$(cd "$(dirname "${BASH_SOURCE[0]}")/../infra" && pwd)}"

if ! az extension show --name microsoft-fabric >/dev/null 2>&1; then
  echo "Installing the 'microsoft-fabric' Azure CLI extension..."
  az extension add --name microsoft-fabric --only-show-errors
fi

RESOURCE_GROUP="${RESOURCE_GROUP:-$(terraform -chdir="$INFRA_DIR" output -raw azure_resource_group)}"
CAPACITY="${CAPACITY:-$(terraform -chdir="$INFRA_DIR" output -raw fabric_capacity_name)}"

case "$ACTION" in
  pause)
    echo "Pausing capacity '$CAPACITY'..."
    az fabric capacity suspend --capacity-name "$CAPACITY" --resource-group "$RESOURCE_GROUP"
    echo "Paused. Fabric content on this capacity is unavailable until you resume."
    ;;
  resume)
    echo "Resuming capacity '$CAPACITY'..."
    az fabric capacity resume --capacity-name "$CAPACITY" --resource-group "$RESOURCE_GROUP"
    echo "Resumed. Billing has restarted."
    ;;
  status)
    az fabric capacity show --capacity-name "$CAPACITY" --resource-group "$RESOURCE_GROUP" \
      --query "{name:name, state:properties.state, sku:sku.name}" -o table
    ;;
  *)
    echo "Usage: $0 {pause|resume|status}" >&2
    exit 1
    ;;
esac
