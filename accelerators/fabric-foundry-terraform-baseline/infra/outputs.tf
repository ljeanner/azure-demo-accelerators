output "project_endpoint" {
  description = "AI Foundry project endpoint"
  value       = azapi_resource.ms_foundry_project.output.properties.endpoints["AI Foundry API"]
}

output "foundry_account_name" {
  description = "AI Foundry (Cognitive Services) account name"
  value       = azapi_resource.ms_foundry.name
}

output "chat_model_deployment" {
  description = "Chat model deployment name"
  value       = azurerm_cognitive_deployment.chat.name
}

output "embedding_deployment" {
  description = "Embedding model deployment name"
  value       = azurerm_cognitive_deployment.embedding.name
}

output "azure_resource_group" {
  description = "Azure resource group name"
  value       = local.resource_group_name
}

output "fabric_capacity_name" {
  description = "Fabric capacity name - attach your Fabric workspace to it"
  value       = azurerm_fabric_capacity.this.name
}

output "search_service_name" {
  description = "Azure AI Search service name"
  value       = azapi_resource.ai_search.name
}

output "search_service_endpoint" {
  description = "Azure AI Search service endpoint"
  value       = "https://${azapi_resource.ai_search.name}.search.windows.net"
}

output "search_system_identity_principal_id" {
  description = "Principal ID of the AI Search system-assigned identity. Grant it access to your Fabric workspace to index OneLake."
  value       = azapi_resource.ai_search.output.identity.principalId
}

output "storage_blob_endpoint" {
  description = "Primary blob endpoint of the storage account"
  value       = azurerm_storage_account.this.primary_blob_endpoint
}

output "user_assigned_identity_client_id" {
  description = "Client ID of the user-assigned identity used by the Foundry account and project"
  value       = azurerm_user_assigned_identity.this.client_id
}

output "application_insights_name" {
  description = "Application Insights instance connected to the Foundry project"
  value       = azurerm_application_insights.this.name
}

output "azure_tenant_id" {
  description = "Azure tenant ID"
  value       = data.azurerm_client_config.current.tenant_id
}
