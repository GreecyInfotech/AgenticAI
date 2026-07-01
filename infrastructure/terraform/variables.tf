variable "project_name" {
  description = "Project name used for resource naming"
  type        = string
  default     = "distributor-platform"
}

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "tags" {
  description = "Common resource tags"
  type        = map(string)
  default     = {}
}

variable "aks_kubernetes_version" {
  description = "AKS Kubernetes version"
  type        = string
  default     = "1.30"
}

variable "aks_node_count" {
  description = "Default node pool VM count"
  type        = number
  default     = 2
}

variable "aks_vm_size" {
  description = "AKS node VM size"
  type        = string
  default     = "Standard_D4s_v5"
}

variable "postgres_sku" {
  description = "PostgreSQL Flexible Server SKU"
  type        = string
  default     = "GP_Standard_D2s_v3"
}

variable "postgres_storage_mb" {
  description = "PostgreSQL storage in MB"
  type        = number
  default     = 32768
}

variable "redis_sku" {
  description = "Redis cache SKU name"
  type        = string
  default     = "Standard"
}

variable "redis_capacity" {
  description = "Redis cache capacity"
  type        = number
  default     = 1
}

variable "enable_event_hubs" {
  description = "Provision Azure Event Hubs as Kafka-compatible endpoint"
  type        = bool
  default     = true
}

variable "allowed_ingress_cidrs" {
  description = "CIDR blocks allowed to reach ingress"
  type        = list(string)
  default     = ["0.0.0.0/0"]
}
