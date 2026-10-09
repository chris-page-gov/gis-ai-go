# These plans use a mock provider, never Google credentials or API calls.
mock_provider "google" {}

variables {
  project_number             = "123456789012"
  project_id                 = "synthetic-gcp-pilot"
  region                     = "europe-west2"
  profile                    = "personal-network-private"
  name_prefix                = "gis-ai-go-test"
  enable_apis                = false
  publisher_member           = "user:synthetic-owner@example.test"
  create_network             = true
  network_id                 = ""
  subnet_id                  = ""
  subnet_cidr                = "10.86.0.0/24"
  backup_bucket_name         = "synthetic-gis-ai-go-test-backups"
  database_id                = "gis-ai-go-test-evidence"
  create_access_vm           = true
  access_vm_zone             = "europe-west2-a"
  access_vm_image            = "projects/ubuntu-os-cloud/global/images/synthetic-pinned-image"
  access_vm_machine_type     = "e2-micro"
  access_principals          = ["user:synthetic-owner@example.test"]
  create_foundation          = true
  existing_runtime_email     = ""
  existing_invoker_email     = ""
  existing_invoker_unique_id = ""
  existing_image_repository  = ""
}

run "private_personal_foundation" {
  command = plan
  assert {
    condition     = google_compute_resource_policy.access_stop[0].instance_schedule_policy[0].vm_stop_schedule[0].schedule == "0 * * * *" && length(google_compute_resource_policy.access_stop[0].instance_schedule_policy[0].vm_start_schedule) == 0 && length(google_compute_instance.access[0].resource_policies) == 1
    error_message = "The on-demand bridge must have an hourly stop safeguard and no automatic start."
  }
  assert {
    condition     = google_compute_instance_iam_member.access_scheduler[0].instance_name == google_compute_instance.access[0].name && google_compute_instance_iam_member.access_scheduler[0].member == "serviceAccount:service-123456789012@compute-system.iam.gserviceaccount.com" && google_project_iam_custom_role.access_scheduler[0].permissions == toset(["compute.instances.start", "compute.instances.stop"])
    error_message = "Scheduler start/stop permissions must belong only to the managed service agent on the owned access VM."
  }
  assert {
    condition     = length(google_compute_instance.access[0].network_interface[0].access_config) == 0
    error_message = "The access VM must have no external IP."
  }
  assert {
    condition     = google_compute_subnetwork.pilot[0].private_ip_google_access
    error_message = "The private access subnet requires Private Google Access."
  }
  assert {
    condition     = google_compute_firewall.iap_ssh[0].source_ranges == toset(["35.235.240.0/20"]) && one(google_compute_firewall.iap_ssh[0].allow).ports == tolist(["22"])
    error_message = "SSH ingress must be restricted to IAP forwarding on port 22."
  }
  assert {
    condition     = google_storage_bucket.backup[0].public_access_prevention == "enforced" && google_storage_bucket.backup[0].uniform_bucket_level_access && !google_storage_bucket.backup[0].force_destroy
    error_message = "Private backup storage must prevent public access and destructive force removal."
  }
  assert {
    condition     = google_firestore_database.evidence[0].delete_protection_state == "DELETE_PROTECTION_ENABLED" && google_firestore_database.evidence[0].point_in_time_recovery_enablement == "POINT_IN_TIME_RECOVERY_ENABLED"
    error_message = "Evidence retention and recovery protection must remain enabled."
  }
}

run "bduk_consumes_platform_foundation" {
  command = plan
  variables {
    profile                    = "bduk-sandpit-network-private"
    create_foundation          = false
    create_network             = false
    create_access_vm           = false
    network_id                 = "projects/synthetic-host/global/networks/shared"
    subnet_id                  = "projects/synthetic-host/regions/europe-west2/subnetworks/approved"
    access_principals          = []
    existing_runtime_email     = "runtime@synthetic-gcp-pilot.iam.gserviceaccount.com"
    existing_invoker_email     = "transport@synthetic-gcp-pilot.iam.gserviceaccount.com"
    existing_invoker_unique_id = "100000000000000000001"
    existing_image_repository  = "europe-west2-docker.pkg.dev/synthetic-gcp-pilot/approved"
  }
  assert {
    condition     = length(google_service_account.runtime) == 0 && length(google_service_account.invoker) == 0 && length(google_compute_instance.access) == 0 && length(google_compute_network.pilot) == 0 && length(google_firestore_database.evidence) == 0 && length(google_storage_bucket.backup) == 0 && length(google_artifact_registry_repository.images) == 0 && length(google_project_service.required) == 0
    error_message = "The default sandpit profile must consume approved platform resources."
  }
}
