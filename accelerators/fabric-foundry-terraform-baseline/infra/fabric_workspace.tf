# ---------------------------------------------------------------------------
# Fabric workspace + lakehouse, created with the microsoft/fabric provider.
#
# Optional: set create_fabric_workspace = false if your tenant blocks
# service-principal / user access to the Fabric APIs, and create the workspace
# by hand instead. Everything else in this stack works either way.
# ---------------------------------------------------------------------------

# Resolves the ARM capacity to the GUID the Fabric API expects.
data "fabric_capacity" "this" {
  count        = var.create_fabric_workspace ? 1 : 0
  display_name = azurerm_fabric_capacity.this.name

  depends_on = [azurerm_fabric_capacity.this]
}

resource "fabric_workspace" "this" {
  count        = var.create_fabric_workspace ? 1 : 0
  display_name = coalesce(var.fabric_workspace_name, format("ws-%s", local.resource_suffix_kebabcase))
  description  = "Demo workspace provisioned by Terraform"
  capacity_id  = data.fabric_capacity.this[0].id

  identity = {
    type = "SystemAssigned"
  }
}

resource "fabric_lakehouse" "this" {
  count        = var.create_fabric_workspace ? 1 : 0
  display_name = var.fabric_lakehouse_name
  description  = "Lakehouse holding the synthetic demo data"
  workspace_id = fabric_workspace.this[0].id
}

# Lets Azure AI Search index OneLake directly, with no data copy and no key.
# See the seed/ai-search-onelake/ scripts.
resource "fabric_workspace_role_assignment" "ai_search" {
  count        = var.create_fabric_workspace && var.grant_ai_search_on_workspace ? 1 : 0
  workspace_id = fabric_workspace.this[0].id
  role         = "Contributor"

  principal = {
    id   = azapi_resource.ai_search.output.identity.principalId
    type = "ServicePrincipal"
  }
}
