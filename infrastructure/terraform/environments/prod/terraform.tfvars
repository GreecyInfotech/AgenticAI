environment = "prod"
location    = "eastus"

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
