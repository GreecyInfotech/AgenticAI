variable "name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "subnet_id" { type = string }
variable "private_dns_zone_id" { type = string }
variable "sku_name" { type = string }
variable "storage_mb" { type = number }
variable "database_name" { type = string }
variable "key_vault_id" { type = string }
variable "tags" { type = map(string) }

resource "random_password" "admin" {
  length  = 24
  special = true
}

resource "azurerm_postgresql_flexible_server" "this" {
  name                   = substr(var.name, 0, 63)
  resource_group_name    = var.resource_group_name
  location               = var.location
  version                = "16"
  administrator_login    = "distributor"
  administrator_password = random_password.admin.result
  storage_mb             = var.storage_mb
  sku_name               = var.sku_name
  zone                   = "1"
  backup_retention_days  = 14
  geo_redundant_backup_enabled = false
  tags                   = var.tags

  delegated_subnet_id          = var.subnet_id
  private_dns_zone_id          = var.private_dns_zone_id
  public_network_access_enabled = false
}

resource "azurerm_postgresql_flexible_server_database" "this" {
  name      = var.database_name
  server_id = azurerm_postgresql_flexible_server.this.id
  charset   = "UTF8"
  collation = "en_US.utf8"
}

resource "azurerm_key_vault_secret" "password" {
  name         = "postgres-admin-password"
  value        = random_password.admin.result
  key_vault_id = var.key_vault_id
}

output "fqdn" { value = azurerm_postgresql_flexible_server.this.fqdn }
output "database_name" { value = azurerm_postgresql_flexible_server_database.this.name }
output "admin_username" { value = azurerm_postgresql_flexible_server.this.administrator_login }
