terraform {
  required_version = ">= 1.6.0"
  backend "azurerm" {
    resource_group_name  = "rg-terraform-state"
    storage_account_name = "tfstatedistributor"
    container_name       = "tfstate"
    key                  = "dev/distributor-platform.tfstate"
  }
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
  environment  = "prod"
  location     = "eastus"

  aks_node_count = 3
  aks_vm_size    = "Standard_D8s_v5"

  postgres_sku        = "GP_Standard_D4s_v3"
  postgres_storage_mb = 131072

  redis_sku      = "Standard"
  redis_capacity = 2

  allowed_ingress_cidrs = ["203.0.113.0/24"]

  tags = {
    cost_center = "production"
    compliance  = "soc2"
  }
}
