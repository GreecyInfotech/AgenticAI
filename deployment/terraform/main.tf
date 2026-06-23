terraform {
  required_version = ">= 1.5"
  required_providers {
    google = { source = "hashicorp/google", version = "~> 5.0" }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

variable "project_id" { type = string }
variable "region" { type = string default = "us-central1" }

resource "google_cloud_run_v2_service" "api_gateway" {
  name     = "eaap-api-gateway"
  location = var.region
  template {
    containers {
      image = "gcr.io/${var.project_id}/eaap-api-gateway"
      ports { container_port = 8000 }
      env { name = "AGENT_GATEWAY_URL" value = google_cloud_run_v2_service.agent_gateway.uri }
      env { name = "RAG_SERVICE_URL" value = google_cloud_run_v2_service.rag.uri }
    }
  }
}

resource "google_cloud_run_v2_service" "agent_gateway" {
  name     = "eaap-agent-gateway"
  location = var.region
  template {
    containers {
      image = "gcr.io/${var.project_id}/eaap-agent-gateway"
      ports { container_port = 8001 }
    }
  }
}

resource "google_cloud_run_v2_service" "rag" {
  name     = "eaap-rag"
  location = var.region
  template {
    containers {
      image = "gcr.io/${var.project_id}/eaap-rag"
      ports { container_port = 8002 }
    }
  }
}

output "api_gateway_url" { value = google_cloud_run_v2_service.api_gateway.uri }
