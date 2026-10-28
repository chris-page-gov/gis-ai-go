output "service_uri" { value = google_cloud_run_v2_service.gateway.uri }
output "latest_revision" { value = google_cloud_run_v2_service.gateway.latest_ready_revision }
output "image_reference" { value = var.image_reference }
output "release_id" { value = var.release_id }
