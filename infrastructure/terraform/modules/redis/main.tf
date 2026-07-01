variable "name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "subnet_id" { type = string }
variable "sku_name" { type = string }
variable "capacity" { type = number }
variable "key_vault_id" { type = string }
variable "tags" { type = map(string) }

resource "random_password" "access" {
  length  = 32
  special = false
}

resource "azurerm_redis_cache" "this" {
  name                  = substr(replace(var.name, "-", ""), 0, 63)
  location              = var.location
  resource_group_name   = var.resource_group_name
  capacity              = var.capacity
  family                = var.sku_name == "Premium" ? "P" : "C"
  sku_name              = var.sku_name
  minimum_tls_version   = "1.2"
  non_ssl_port_enabled  = false
  tags                  = var.tags

  redis_configuration {
    maxmemory_policy = "allkeys-lru"
  }

  subnet_id = var.sku_name == "Premium" ? var.subnet_id : null
}

resource "azurerm_key_vault_secret" "key" {
  name         = "redis-primary-key"
  value        = azurerm_redis_cache.this.primary_access_key
  key_vault_id = var.key_vault_id
}

output "hostname" { value = azurerm_redis_cache.this.hostname }
output "ssl_port" { value = azurerm_redis_cache.this.ssl_port }
