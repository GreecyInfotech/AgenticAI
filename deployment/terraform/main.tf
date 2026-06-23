terraform {
  required_version = ">= 1.5"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" {
  type        = string
  description = "GCP Project ID"
}

variable "region" {
  type    = string
  default = "us-central1"
}

variable "environment" {
  type    = string
  default = "production"
}

# GKE Cluster
resource "google_container_cluster" "smart_port" {
  name     = "smart-port-${var.environment}"
  location = var.region

  remove_default_node_pool = true
  initial_node_count       = 1

  networking_mode = "VPC_NATIVE"

  workload_identity_config {
    workload_pool = "${var.project_id}.svc.id.goog"
  }

  monitoring_config {
    enable_components = ["SYSTEM_COMPONENTS", "WORKLOADS"]
  }
}

resource "google_container_node_pool" "primary" {
  name       = "smart-port-pool"
  location   = var.region
  cluster    = google_container_cluster.smart_port.name
  node_count = 3

  node_config {
    machine_type = "e2-standard-4"
    disk_size_gb = 100
    oauth_scopes = ["https://www.googleapis.com/auth/cloud-platform"]

    labels = {
      environment = var.environment
      platform    = "smart-port"
    }
  }

  autoscaling {
    min_node_count = 2
    max_node_count = 10
  }
}

# Cloud SQL PostgreSQL with pgvector
resource "google_sql_database_instance" "postgres" {
  name             = "smart-port-postgres-${var.environment}"
  database_version = "POSTGRES_16"
  region           = var.region

  settings {
    tier = "db-custom-4-16384"
    database_flags {
      name  = "cloudsql.enable_pgvector"
      value = "on"
    }
    ip_configuration {
      ipv4_enabled = false
      private_network = google_compute_network.vpc.id
    }
    backup_configuration {
      enabled    = true
      start_time = "03:00"
    }
  }

  deletion_protection = true
}

resource "google_sql_database" "smartport" {
  name     = "smartport"
  instance = google_sql_database_instance.postgres.name
}

# Cloud Storage for documents
resource "google_storage_bucket" "documents" {
  name          = "${var.project_id}-smart-port-documents"
  location      = var.region
  force_destroy = false

  versioning { enabled = true }

  lifecycle_rule {
    condition { age = 365 }
    action { type = "SetStorageClass", storage_class = "COLDLINE" }
  }
}

# BigQuery dataset for analytics
resource "google_bigquery_dataset" "analytics" {
  dataset_id = "smart_port_analytics"
  location   = var.region

  labels = {
    environment = var.environment
    platform    = "smart-port"
  }
}

# VPC
resource "google_compute_network" "vpc" {
  name                    = "smart-port-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "subnet" {
  name          = "smart-port-subnet"
  ip_cidr_range = "10.0.0.0/16"
  region        = var.region
  network       = google_compute_network.vpc.id
}

# Memorystore Redis
resource "google_redis_instance" "cache" {
  name           = "smart-port-redis"
  tier           = "STANDARD_HA"
  memory_size_gb = 4
  region         = var.region
}

output "cluster_name" {
  value = google_container_cluster.smart_port.name
}

output "postgres_connection" {
  value     = google_sql_database_instance.postgres.connection_name
  sensitive = true
}

output "documents_bucket" {
  value = google_storage_bucket.documents.name
}

output "bigquery_dataset" {
  value = google_bigquery_dataset.analytics.dataset_id
}
