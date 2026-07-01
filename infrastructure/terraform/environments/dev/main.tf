terraform {
  required_version = ">= 1.6.0"
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy = false
    }
    resource_group {
      prevent_deletion_if_contains_resources = true
    }
  }
}

module "platform" {
  source = "../../"

  project_name = "distributor-platform"
  environment  = "dev"
  location     = "eastus"

  aks_node_count = 2
  aks_vm_size    = "Standard_D4s_v5"

  postgres_sku        = "B_Standard_B2s"
  postgres_storage_mb = 32768

  redis_sku      = "Basic"
  redis_capacity = 0

  tags = {
    cost_center = "engineering"
  }
}
