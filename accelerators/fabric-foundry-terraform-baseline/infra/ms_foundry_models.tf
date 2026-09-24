resource "azurerm_cognitive_deployment" "chat" {
  name                 = var.chat_model.name
  cognitive_account_id = azapi_resource.ms_foundry.id

  sku {
    name     = "GlobalStandard"
    capacity = var.chat_model.capacity
  }

  model {
    format  = "OpenAI"
    name    = var.chat_model.name
    version = var.chat_model.version
  }

  version_upgrade_option = "OnceNewDefaultVersionAvailable"
  rai_policy_name        = "Microsoft.DefaultV2"

  depends_on = [
    azapi_resource.ms_foundry
  ]
}

resource "azurerm_cognitive_deployment" "embedding" {
  name                 = var.embedding_model.name
  cognitive_account_id = azapi_resource.ms_foundry.id

  sku {
    name     = "GlobalStandard"
    capacity = var.embedding_model.capacity
  }

  model {
    format  = "OpenAI"
    name    = var.embedding_model.name
    version = var.embedding_model.version
  }

  version_upgrade_option = "OnceNewDefaultVersionAvailable"
  rai_policy_name        = "Microsoft.DefaultV2"

  depends_on = [
    azapi_resource.ms_foundry
  ]
}
