resource "azapi_resource" "ms_foundry_project" {
  type                      = "Microsoft.CognitiveServices/accounts/projects@2025-06-01"
  name                      = format("prj-%s", local.resource_suffix_kebabcase)
  parent_id                 = azapi_resource.ms_foundry.id
  location                  = local.resource_group_location
  schema_validation_enabled = false
  tags                      = local.tags_azapi

  body = {
    sku = {
      name = "S0"
    }
    identity = {
      type = "UserAssigned"
      userAssignedIdentities = {
        (azurerm_user_assigned_identity.this.id) = {}
      }
    }

    properties = {
      displayName = "project"
      description = "A project for the AI Foundry account with network secured deployed Agent using User Assigned Identity"
    }
  }

  response_export_values = [
    "identity.principalId",
    "properties.internalId",
    "properties.endpoints"
  ]

  depends_on = [
    azapi_resource.ms_foundry,
  ]
}