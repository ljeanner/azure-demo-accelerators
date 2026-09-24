#!/usr/bin/env bash
# Create the Foundry project connection to a Fabric data agent.
#
# Requires Microsoft.CognitiveServices/accounts/projects/connections/write on the
# Foundry project. Reads its configuration from .env.
#
#   cp .env.template .env && vi .env
#   ./create_connection.sh

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/.env" ]; then
  set -a
  # shellcheck disable=SC1091
  . "$SCRIPT_DIR/.env"
  set +a
fi

: "${AZURE_SUBSCRIPTION_ID:?set it in .env}"
: "${AZURE_RESOURCE_GROUP:?set it in .env}"
: "${FOUNDRY_ACCOUNT_NAME:?set it in .env}"
: "${FOUNDRY_PROJECT_NAME:?set it in .env}"
: "${FABRIC_CONNECTION_NAME:?set it in .env}"
: "${FABRIC_WORKSPACE_ID:?set it in .env}"
: "${FABRIC_DATA_AGENT_ID:?set it in .env}"

API_VERSION="2025-04-01-preview"
URL="https://management.azure.com/subscriptions/${AZURE_SUBSCRIPTION_ID}"
URL="${URL}/resourceGroups/${AZURE_RESOURCE_GROUP}"
URL="${URL}/providers/Microsoft.CognitiveServices/accounts/${FOUNDRY_ACCOUNT_NAME}"
URL="${URL}/projects/${FOUNDRY_PROJECT_NAME}/connections/${FABRIC_CONNECTION_NAME}"
URL="${URL}?api-version=${API_VERSION}"

BODY=$(cat <<JSON
{
  "properties": {
    "category": "CustomKeys",
    "authType": "CustomKeys",
    "credentials": {
      "keys": {
        "workspace_id": "${FABRIC_WORKSPACE_ID}",
        "artifact_id": "${FABRIC_DATA_AGENT_ID}"
      }
    }
  }
}
JSON
)

echo "Creating connection '${FABRIC_CONNECTION_NAME}' on project '${FOUNDRY_PROJECT_NAME}'..."
az rest --method put --url "$URL" --headers "Content-Type=application/json" --body "$BODY" \
  --query id --output tsv

echo
echo "Done. Use FABRIC_CONNECTION_NAME=${FABRIC_CONNECTION_NAME} in the Python scripts."
