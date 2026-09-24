variable "domain" {
  description = "Azure deployment domain (short code used in resource names)"
  type        = string
  default     = "dmo"
}

variable "workload" {
  description = "Azure deployment workload (short code used in resource names)"
  type        = string
  default     = "iq"
}

variable "environment" {
  description = "The environment deployed"
  type        = string
  default     = "dev"
  validation {
    condition     = can(regex("(dev|stg|pro)", var.environment))
    error_message = "The environment value must be a valid."
  }
}

variable "location" {
  description = "Azure deployment location"
  type        = string
  default     = "swedencentral"
}

variable "region" {
  description = "Short region code used in resource names"
  type        = string
  default     = "swc"
}

variable "tags" {
  type        = map(any)
  description = "The custom tags for all resources"
  default     = {}
}

variable "resource_group_name" {
  type        = string
  description = "Name of an existing resource group. Leave empty to create one."
  default     = ""
}

variable "project_name" {
  type        = string
  description = "Value of the ProjectName tag applied to every resource"
  default     = "demo-accelerator"
}

variable "fabric_capacity_sku" {
  type        = string
  description = "Fabric capacity SKU. F2 is the minimum required by Fabric data agents."
  default     = "F2"
}

variable "chat_model" {
  type = object({
    name     = string
    version  = string
    capacity = number
  })
  description = "Chat model deployed on the Foundry account"
  default = {
    name     = "gpt-4.1-mini"
    version  = "2025-04-14"
    capacity = 120
  }
}

variable "embedding_model" {
  type = object({
    name     = string
    version  = string
    capacity = number
  })
  description = "Embedding model deployed on the Foundry account"
  default = {
    name     = "text-embedding-3-large"
    version  = "1"
    capacity = 500
  }
}
