terraform {
  required_version = ">= 1.3.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }

  backend "gcs" {
    
  }

}

# ------------------------------------------------------------------------------
# Variabili
# ------------------------------------------------------------------------------
variable "project_id" {
  type        = string
  description = "ID del progetto GCP"
}

variable "region" {
  type        = string
  description = "Regione di deployment (es. europe-west1)"
  default     = "europe-west1"
}

variable "service_name" {
  type        = string
  description = "Nome condiviso per Cloud Run, Service Account e Artifact Registry"
  default     = "Sage"
}

variable "resource_prefix" {
  type        = string
  description = "Prefisso da applicare ai nomi di tutte le risorse"
  default     = "its-ict-mario-mogavero"
}

# variable "container_image" {
#   type        = string
#   description = "URI dell'immagine Docker (es. europe-west1-docker.pkg.dev/PROJECT_ID/REPO_NAME/IMAGE:TAG)"
#   default     = "us-docker.pkg.dev/cloudrun/container/hello" # Immagine placeholder iniziale
# }

provider "google" {
  project = var.project_id
  region  = var.region
}

# ------------------------------------------------------------------------------
# 1. Abilitazione delle API di Google Cloud
# ------------------------------------------------------------------------------
# resource "google_project_service" "enabled_apis" {
#   for_each = toset([
#     "run.googleapis.com",             # API per Cloud Run
#     "artifactregistry.googleapis.com",# API per Artifact Registry (Container Registry)
#     "aiplatform.googleapis.com",      # API per Vertex AI
#     "iam.googleapis.com"              # API per IAM
#   ])
# 
#   project                    = var.project_id
#   service                    = each.key
#   disable_on_destroy         = false
#   disable_dependent_services = false
# }
# 
# # ------------------------------------------------------------------------------
# # 2. Artifact Registry (Equivalente ECR su GCP)
# # ------------------------------------------------------------------------------
# resource "google_artifact_registry_repository" "registry" {
#   location      = var.region
#   repository_id = var.service_name
#   description   = "Repository Docker per il servizio ${var.service_name}"
#   format        = "DOCKER"
# 
#   depends_on = [google_project_service.enabled_apis]
# }
# 
# # ------------------------------------------------------------------------------
# # 3. Service Account e Permessi Vertex AI
# # ------------------------------------------------------------------------------
# resource "google_service_account" "app_sa" {
#   account_id   = var.service_name
#   display_name = "Service Account per ${var.service_name}"
# 
#   depends_on = [google_project_service.enabled_apis]
# }
# 
# # Assegnazione del ruolo Vertex AI User al Service Account
# resource "google_project_iam_member" "vertex_user" {
#   project = var.project_id
#   role    = "roles/aiplatform.user"
#   member  = "serviceAccount:${google_service_account.app_sa.email}"
# }
# 
# # Permesso facoltativo per leggere le immagini da Artifact Registry
# resource "google_artifact_registry_repository_iam_member" "registry_reader" {
#   project    = var.project_id
#   location   = var.region
#   repository = google_artifact_registry_repository.registry.name
#   role       = "roles/artifactregistry.reader"
#   member     = "serviceAccount:${google_service_account.app_sa.email}"
# }
# 
# # ------------------------------------------------------------------------------
# # 4. Servizio Cloud Run (v2)
# # ------------------------------------------------------------------------------
# resource "google_cloud_run_v2_service" "sage_backend" {
#   name     = "${var.service_name}-sage_backend"
#   location = var.region
#   project = var.project_id
#   ingress  = "INGRESS_TRAFFIC_ALL"
# 
#   deletion_protection = false
# 
#   template {
#     service_account = google_service_account.app_sa.email
# 
#     scaling {
#       min_instance_count = 0
#       max_instance_count = 3
#     }
# 
#     
# 
#     containers {
#       image = var.container_image
# 
#       resources {
#         limits = {
#           cpu    = "1000m" # 1 vCPU
#           memory = "2Gi"   # 2 GB RAM
#         }
#       }
# 
#       ports {
#         container_port = 8000
#       }
#     }
#   }
# 
#   depends_on = [
#     google_project_service.enabled_apis,
#     google_project_iam_member.vertex_user
#   ]
# }

# ------------------------------------------------------------------------------
# Outputs
# ------------------------------------------------------------------------------
# output "cloud_run_url" {
#   value       = google_cloud_run_v2_service.default.uri
#   description = "URL del servizio Cloud Run"
# }
# 
# output "artifact_registry_url" {
#   value       = "${var.region}-docker.pkg.dev/${var.project_id}/${google_artifact_registry_repository.registry.name}"
#   description = "URI base dell'Artifact Registry per fare il push delle immagini Docker"
# }
# 
# output "service_account_email" {
#   value       = google_service_account.app_sa.email
#   description = "Email del Service Account creato"
# }