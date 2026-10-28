resource "google_cloud_run_v2_service" "gateway" {
  project             = var.project_id
  location            = var.region
  name                = var.name_prefix
  ingress             = "INGRESS_TRAFFIC_INTERNAL_ONLY"
  deletion_protection = var.deletion_protection
  labels              = { application = "gis-ai-go", deployment = var.name_prefix, profile = var.profile }
  depends_on          = [google_secret_manager_secret_iam_member.browser]
  template {
    service_account                  = var.runtime_email
    timeout                          = "${var.timeout_seconds}s"
    max_instance_request_concurrency = var.concurrency
    scaling {
      min_instance_count = 0
      max_instance_count = var.max_instances
    }
    vpc_access {
      egress = "ALL_TRAFFIC"
      network_interfaces {
        network    = var.network_id
        subnetwork = var.subnet_id
        tags       = ["${var.name_prefix}-runtime"]
      }
    }
    containers {
      image = var.image_reference
      ports { container_port = 8080 }
      resources {
        limits   = { cpu = var.cpu, memory = var.memory }
        cpu_idle = true
      }
      env {
        name  = "GCP_FIRESTORE_PROJECT"
        value = var.project_id
      }
      env {
        name  = "GCP_TRANSPORT_SUBJECT"
        value = var.invoker_unique_id
      }
      env {
        name  = "GCP_RELEASE_ID"
        value = var.release_id
      }
      env {
        name  = "GCP_RUNTIME_CONFIG_JSON"
        value = var.runtime_config_json
      }
      dynamic "env" {
        for_each = var.browser_secret_references
        content {
          name = env.key
          value_source {
            secret_key_ref {
              secret  = env.value.resource
              version = env.value.version
            }
          }
        }
      }
      startup_probe {
        http_get {
          path = "/healthz"
          port = 8080
        }
        initial_delay_seconds = 1
        period_seconds        = 5
        failure_threshold     = 12
      }
    }
  }
  lifecycle {
    precondition {
      condition     = can(regex("@sha256:[0-9a-f]{64}$", var.image_reference))
      error_message = "Only an observed immutable image digest is accepted."
    }
  }
}
resource "google_cloud_run_v2_service_iam_member" "private_transport" {
  for_each = toset(var.transport_principals)
  project  = var.project_id
  location = var.region
  name     = google_cloud_run_v2_service.gateway.name
  role     = "roles/run.invoker"
  member   = each.value
}

# Existing approved secret versions only. No secret payload or version resource
# is read/created by Terraform, so credentials never enter Terraform state.
resource "google_secret_manager_secret_iam_member" "browser" {
  for_each  = toset([for reference in values(var.browser_secret_references) : reference.resource])
  project   = split("/", each.value)[1]
  secret_id = split("/", each.value)[3]
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.runtime_email}"
}
