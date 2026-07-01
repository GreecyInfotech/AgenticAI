variable "name" { type = string }
variable "location" { type = string }
variable "resource_group_name" { type = string }
variable "subnet_id" { type = string }
variable "tags" { type = map(string) }

resource "azurerm_eventhub_namespace" "this" {
  name                = substr(replace(var.name, "-", ""), 0, 50)
  location            = var.location
  resource_group_name = var.resource_group_name
  sku                 = "Standard"
  capacity            = 1
  tags                = var.tags
}

locals {
  topics = [
    "order.created", "order.updated", "order.cancelled",
    "inventory.checked", "inventory.reserved",
    "promotion.applied", "credit.checked",
    "payment.completed", "shipment.created", "notification.sent",
  ]
}

resource "azurerm_eventhub" "topics" {
  for_each          = toset(local.topics)
  name              = each.key
  namespace_id      = azurerm_eventhub_namespace.this.id
  partition_count   = 4
  message_retention = 7
}

output "bootstrap_servers" {
  value = "${azurerm_eventhub_namespace.this.name}.servicebus.windows.net:9093"
}
