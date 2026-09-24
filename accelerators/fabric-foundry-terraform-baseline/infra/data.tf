data "azurerm_client_config" "current" {}

data "azuread_user" "current" {
  object_id = data.azurerm_client_config.current.object_id
}

data "azurerm_resource_group" "this" {
  count = var.resource_group_name != "" ? 1 : 0
  name  = var.resource_group_name
}