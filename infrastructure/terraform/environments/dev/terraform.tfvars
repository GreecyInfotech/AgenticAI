environment = "dev"
location    = "eastus"

aks_node_count = 2
aks_vm_size    = "Standard_D4s_v5"

postgres_sku        = "B_Standard_B2s"
postgres_storage_mb = 32768

redis_sku      = "Basic"
redis_capacity = 0

tags = {
  cost_center = "engineering"
  owner       = "platform-team"
}
