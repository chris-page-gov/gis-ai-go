# These plans use a mock provider, never Google credentials or API calls.
mock_provider "google" {}

variables {
  project_id           = "synthetic-gcp-pilot"
  region               = "europe-west2"
  profile              = "personal-network-private"
  name_prefix          = "gis-ai-go-test"
  runtime_email        = "runtime@synthetic-gcp-pilot.iam.gserviceaccount.com"
  invoker_unique_id    = "100000000000000000001"
  network_id           = "projects/synthetic-gcp-pilot/global/networks/private"
  subnet_id            = "projects/synthetic-gcp-pilot/regions/europe-west2/subnetworks/private"
  image_reference      = "europe-west2-docker.pkg.dev/synthetic-gcp-pilot/images/gateway@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  release_id           = "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
  transport_principals = ["serviceAccount:invoker@synthetic-gcp-pilot.iam.gserviceaccount.com"]
  cpu                  = "1"
  memory               = "2Gi"
  max_instances        = 2
  concurrency          = 20
  timeout_seconds      = 120
  runtime_config_json  = "{}"
  deletion_protection  = true
}

run "private_service" {
  command = plan
  assert {
    condition     = google_cloud_run_v2_service.gateway.ingress == "INGRESS_TRAFFIC_INTERNAL_ONLY"
    error_message = "The pilot must have internal ingress."
  }
  assert {
    condition     = google_cloud_run_v2_service.gateway.template[0].vpc_access[0].egress == "ALL_TRAFFIC"
    error_message = "All runtime egress must traverse the approved VPC."
  }
  assert {
    condition     = google_cloud_run_v2_service.gateway.template[0].scaling[0].min_instance_count == 0 && google_cloud_run_v2_service.gateway.template[0].scaling[0].max_instance_count == 2
    error_message = "The approved instance bounds must be retained."
  }
  assert {
    condition     = alltrue([for binding in google_cloud_run_v2_service_iam_member.private_transport : binding.role == "roles/run.invoker" && startswith(binding.member, "serviceAccount:")])
    error_message = "Only the explicit transport identity receives invocation permission."
  }
  assert {
    condition     = google_cloud_run_v2_service.gateway.deletion_protection && endswith(google_cloud_run_v2_service.gateway.template[0].containers[0].image, "@sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
    error_message = "Deployment must retain deletion protection and the approved image digest."
  }
}

run "mutable_image_denied" {
  command = plan
  variables { image_reference = "europe-west2-docker.pkg.dev/synthetic-gcp-pilot/images/gateway:latest" }
  expect_failures = [google_cloud_run_v2_service.gateway]
}

run "approved_secret_references" {
  command = plan
  variables {
    browser_secret_references = {
      GCP_BROWSER_SESSION_KEY = { resource = "projects/synthetic-gcp-pilot/secrets/session-key", version = "3" }
      GCP_OIDC_CLIENT_SECRET  = { resource = "projects/synthetic-gcp-pilot/secrets/oidc-client", version = "2" }
    }
  }
  assert {
    condition     = length(google_secret_manager_secret_iam_member.browser) == 2 && alltrue([for binding in google_secret_manager_secret_iam_member.browser : binding.role == "roles/secretmanager.secretAccessor" && binding.member == "serviceAccount:runtime@synthetic-gcp-pilot.iam.gserviceaccount.com"])
    error_message = "Only the runtime identity can access exactly the approved existing secrets."
  }
  assert {
    condition     = alltrue([for environment in google_cloud_run_v2_service.gateway.template[0].containers[0].env : contains(["GCP_BROWSER_SESSION_KEY", "GCP_OIDC_CLIENT_SECRET"], environment.name) ? environment.value == null && length(environment.value_source) == 1 : true])
    error_message = "Secret values must use Secret Manager references, never literal Terraform environment values."
  }
}

run "anonymous_invoker_denied" {
  command = plan
  variables { transport_principals = ["allUsers"] }
  expect_failures = [var.transport_principals]
}

run "mutable_secret_version_denied" {
  command = plan
  variables { browser_secret_references = { GCP_BROWSER_SESSION_KEY = { resource = "projects/synthetic-gcp-pilot/secrets/session-key", version = "latest" } } }
  expect_failures = [var.browser_secret_references]
}
