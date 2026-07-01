output "resource_group_name" {
  value = module.resource_group.name
}

output "aks_cluster_name" {
  value = module.aks.cluster_name
}

output "aks_kube_config" {
  value     = module.aks.kube_config
  sensitive = true
}

output "acr_login_server" {
  value = module.container_registry.login_server
}

output "key_vault_name" {
  value = module.key_vault.name
}

output "key_vault_uri" {
  value = module.key_vault.uri
}

output "postgres_fqdn" {
  value = module.postgres.fqdn
}

output "postgres_database_name" {
  value = module.postgres.database_name
}

output "redis_hostname" {
  value = module.redis.hostname
}

output "event_hubs_bootstrap" {
  value = var.enable_event_hubs ? module.event_hubs[0].bootstrap_servers : ""
}

output "helm_external_services" {
  description = "Values to pass to Helm chart externalServices"
  value = {
    postgres = {
      host     = module.postgres.fqdn
      port     = 5432
      database = module.postgres.database_name
      user     = module.postgres.admin_username
    }
    redis = {
      host = module.redis.hostname
      port = module.redis.ssl_port
    }
    kafka = {
      bootstrapServers = var.enable_event_hubs ? module.event_hubs[0].bootstrap_servers : ""
    }
  }
  sensitive = true
}
