terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=5.3.0"
    }

    random = {
      source  = "hashicorp/random"
      version = "3.9.0"
    }

    azapi = {
      source  = "Azure/azapi"
      version = "2.10.0"
    }

    azuread = {
      source  = "hashicorp/azuread"
      version = "~> 3.0"
    }

    fabric = {
      source  = "microsoft/fabric"
      version = "~> 1.14"
    }
  }

  backend "local" {}
  # backend "azurerm" {}
}

provider "azurerm" {
  features {
    cognitive_account {
      purge_soft_delete_on_destroy = true
    }
  }
  storage_use_azuread = true
}

provider "azapi" {
  # Configuration options
}

provider "azuread" {
  # Configuration options
}

provider "fabric" {
  # Authenticates with the Azure CLI by default (az login).
  # Service principal / OIDC options are documented at
  # https://registry.terraform.io/providers/microsoft/fabric/latest/docs
}