resource "azurerm_fabric_capacity" "this" {
  name                = format("fc%s", local.resource_suffix_lowercase)
  resource_group_name = local.resource_group_name
  location            = local.resource_group_location

  # The signed-in deployer becomes a capacity admin, so they can immediately
  # create a Fabric workspace bound to this capacity.
  administration_members = [data.azuread_user.current.user_principal_name]

  sku {
    name = var.fabric_capacity_sku
    tier = "Fabric"
  }

  tags = local.tags
}
