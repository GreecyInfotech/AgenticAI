locals {
  name_prefix = "${var.project_name}-${var.environment}"
  common_tags = merge(
    {
      project     = var.project_name
      environment = var.environment
      managed_by  = "terraform"
    },
    var.tags
  )
}

module "resource_group" {
  source   = "./modules/resource_group"
  name     = "rg-${local.name_prefix}"
  location = var.location
  tags     = local.common_tags
}

module "networking" {
  source                = "./modules/networking"
  name_prefix           = local.name_prefix
  location              = var.location
  resource_group_name   = module.resource_group.name
  tags                  = local.common_tags
  allowed_ingress_cidrs = var.allowed_ingress_cidrs
}

module "container_registry" {
  source              = "./modules/container_registry"
  name                = replace("acr${var.project_name}${var.environment}", "-", "")
  location            = var.location
  resource_group_name = module.resource_group.name
  tags                = local.common_tags
  sku                 = var.environment == "prod" ? "Premium" : "Standard"
}

module "aks" {
  source              = "./modules/aks"
  name                = "aks-${local.name_prefix}"
  location            = var.location
  resource_group_name = module.resource_group.name
  subnet_id           = module.networking.aks_subnet_id
  kubernetes_version  = var.aks_kubernetes_version
  node_count          = var.aks_node_count
  vm_size             = var.aks_vm_size
  acr_id              = module.container_registry.id
  tags                = local.common_tags
}

module "key_vault" {
  source                    = "./modules/key_vault"
  name                      = "kv-${local.name_prefix}"
  location                  = var.location
  resource_group_name       = module.resource_group.name
  tags                      = local.common_tags
  aks_identity_principal_id = module.aks.kubelet_identity_object_id
}

module "postgres" {
  source              = "./modules/postgres"
  name                = "psql-${local.name_prefix}"
  location            = var.location
  resource_group_name = module.resource_group.name
  subnet_id           = module.networking.data_subnet_id
  private_dns_zone_id = module.networking.postgres_private_dns_zone_id
  sku_name            = var.postgres_sku
  storage_mb          = var.postgres_storage_mb
  database_name       = "distributor_platform"
  key_vault_id        = module.key_vault.id
  tags                = local.common_tags

  depends_on = [module.networking]
}

module "redis" {
  source              = "./modules/redis"
  name                = "redis-${local.name_prefix}"
  location            = var.location
  resource_group_name = module.resource_group.name
  subnet_id           = module.networking.data_subnet_id
  sku_name            = var.redis_sku
  capacity            = var.redis_capacity
  key_vault_id        = module.key_vault.id
  tags                = local.common_tags
}

module "event_hubs" {
  source              = "./modules/event_hubs"
  count               = var.enable_event_hubs ? 1 : 0
  name                = "evh-${local.name_prefix}"
  location            = var.location
  resource_group_name = module.resource_group.name
  subnet_id           = module.networking.data_subnet_id
  tags                = local.common_tags
}
