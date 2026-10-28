locals {
  labels        = { application = "gis-ai-go", deployment = var.name_prefix, profile = var.profile }
  runtime_email = "${var.name_prefix}-runtime@${var.project_id}.iam.gserviceaccount.com"
  invoker_email = "${var.name_prefix}-invoker@${var.project_id}.iam.gserviceaccount.com"
  network_id    = var.create_network ? google_compute_network.pilot[0].id : var.network_id
  subnet_id     = var.create_network ? google_compute_subnetwork.pilot[0].id : var.subnet_id
  api_services  = toset(["run.googleapis.com", "artifactregistry.googleapis.com", "compute.googleapis.com", "iap.googleapis.com", "firestore.googleapis.com", "storage.googleapis.com", "iam.googleapis.com", "dns.googleapis.com"])
}

# API enablement is an explicit, reviewed resource change; never performed by preflight.
resource "google_project_service" "required" {
  for_each           = var.enable_apis ? local.api_services : toset([])
  project            = var.project_id
  service            = each.value
  disable_on_destroy = false
}
resource "google_service_account" "runtime" {
  count        = var.create_foundation ? 1 : 0
  project      = var.project_id
  account_id   = "${var.name_prefix}-runtime"
  display_name = "GIS AI GO runtime; no human identity"
  depends_on   = [google_project_service.required]
}
resource "google_service_account" "invoker" {
  count        = var.create_foundation ? 1 : 0
  project      = var.project_id
  account_id   = "${var.name_prefix}-invoker"
  display_name = "GIS AI GO private transport only"
  depends_on   = [google_project_service.required]
}
resource "google_artifact_registry_repository" "images" {
  count         = var.create_foundation ? 1 : 0
  project       = var.project_id
  location      = var.region
  repository_id = "${var.name_prefix}-images"
  format        = "DOCKER"
  labels        = local.labels
  depends_on    = [google_project_service.required]
}
resource "google_artifact_registry_repository_iam_member" "publisher" {
  count      = var.create_foundation ? 1 : 0
  project    = var.project_id
  location   = var.region
  repository = google_artifact_registry_repository.images[0].name
  role       = "roles/artifactregistry.writer"
  member     = var.publisher_member
}
resource "google_storage_bucket" "backup" {
  count                       = var.create_foundation ? 1 : 0
  project                     = var.project_id
  name                        = var.backup_bucket_name
  location                    = var.region
  uniform_bucket_level_access = true
  public_access_prevention    = "enforced"
  force_destroy               = false
  labels                      = local.labels
  versioning { enabled = true }
  lifecycle { prevent_destroy = true }
  depends_on = [google_project_service.required]
}
resource "google_firestore_database" "evidence" {
  count                             = var.create_foundation ? 1 : 0
  project                           = var.project_id
  name                              = var.database_id
  location_id                       = var.region
  type                              = "FIRESTORE_NATIVE"
  concurrency_mode                  = "PESSIMISTIC"
  delete_protection_state           = "DELETE_PROTECTION_ENABLED"
  point_in_time_recovery_enablement = "POINT_IN_TIME_RECOVERY_ENABLED"
  lifecycle { prevent_destroy = true }
  depends_on = [google_project_service.required]
}
# Additive binding; database condition protects other evidence databases.
resource "google_project_iam_member" "evidence" {
  count   = var.create_foundation ? 1 : 0
  project = var.project_id
  role    = "roles/datastore.user"
  member  = "serviceAccount:${google_service_account.runtime[0].email}"
  condition {
    title       = "gis-ai-go-owned-evidence-database"
    description = "Only the named pilot database; application enforces evidence ownership"
    expression  = "resource.name == 'projects/${var.project_id}/databases/${var.database_id}' || resource.name.startsWith('projects/${var.project_id}/databases/${var.database_id}/')"
  }
}
resource "google_compute_network" "pilot" {
  count                   = var.create_network ? 1 : 0
  project                 = var.project_id
  name                    = "${var.name_prefix}-private"
  auto_create_subnetworks = false
  depends_on              = [google_project_service.required]
}
resource "google_compute_subnetwork" "pilot" {
  count                    = var.create_network ? 1 : 0
  project                  = var.project_id
  region                   = var.region
  name                     = "${var.name_prefix}-private"
  network                  = google_compute_network.pilot[0].id
  ip_cidr_range            = var.subnet_cidr
  private_ip_google_access = true
}
resource "google_dns_managed_zone" "apis" {
  count      = var.create_network ? 1 : 0
  project    = var.project_id
  name       = "${var.name_prefix}-googleapis"
  dns_name   = "googleapis.com."
  visibility = "private"
  private_visibility_config {
    networks { network_url = local.network_id }
  }
}
resource "google_dns_record_set" "api_vip" {
  count        = var.create_network ? 1 : 0
  project      = var.project_id
  managed_zone = google_dns_managed_zone.apis[0].name
  name         = "private.googleapis.com."
  type         = "A"
  ttl          = 300
  rrdatas      = ["199.36.153.8", "199.36.153.9", "199.36.153.10", "199.36.153.11"]
}
resource "google_dns_record_set" "api_wildcard" {
  count        = var.create_network ? 1 : 0
  project      = var.project_id
  managed_zone = google_dns_managed_zone.apis[0].name
  name         = "*.googleapis.com."
  type         = "CNAME"
  ttl          = 300
  rrdatas      = ["private.googleapis.com."]
}
resource "google_dns_managed_zone" "run" {
  count      = var.create_network ? 1 : 0
  project    = var.project_id
  name       = "${var.name_prefix}-run"
  dns_name   = "run.app."
  visibility = "private"
  private_visibility_config {
    networks { network_url = local.network_id }
  }
}
resource "google_dns_record_set" "run" {
  count        = var.create_network ? 1 : 0
  project      = var.project_id
  managed_zone = google_dns_managed_zone.run[0].name
  name         = "*.run.app."
  type         = "CNAME"
  ttl          = 300
  rrdatas      = ["private.googleapis.com."]
}
resource "google_compute_firewall" "iap_ssh" {
  count         = var.create_access_vm ? 1 : 0
  project       = var.project_id
  name          = "${var.name_prefix}-iap-ssh"
  network       = local.network_id
  direction     = "INGRESS"
  source_ranges = ["35.235.240.0/20"]
  target_tags   = ["${var.name_prefix}-access"]
  allow {
    protocol = "tcp"
    ports    = ["22"]
  }
}
resource "google_compute_firewall" "private_api_egress" {
  count              = var.create_network ? 1 : 0
  project            = var.project_id
  name               = "${var.name_prefix}-private-api-egress"
  network            = local.network_id
  direction          = "EGRESS"
  priority           = 1000
  destination_ranges = ["199.36.153.8/30"]
  target_tags        = ["${var.name_prefix}-access", "${var.name_prefix}-runtime"]
  allow {
    protocol = "tcp"
    ports    = ["443"]
  }
}
resource "google_compute_firewall" "deny_egress" {
  count              = var.create_network ? 1 : 0
  project            = var.project_id
  name               = "${var.name_prefix}-deny-egress"
  network            = local.network_id
  direction          = "EGRESS"
  priority           = 2000
  destination_ranges = ["0.0.0.0/0"]
  target_tags        = ["${var.name_prefix}-access", "${var.name_prefix}-runtime"]
  deny {
    protocol = "all"
  }
}
resource "google_compute_instance" "access" {
  count             = var.create_access_vm ? 1 : 0
  project           = var.project_id
  zone              = var.access_vm_zone
  name              = "${var.name_prefix}-access"
  machine_type      = var.access_vm_machine_type
  resource_policies = var.access_vm_on_demand ? [google_compute_resource_policy.access_stop[0].id] : []
  labels            = local.labels
  tags              = ["${var.name_prefix}-access"]
  boot_disk {
    initialize_params {
      image = var.access_vm_image
      size  = 10
      type  = "pd-balanced"
    }
  }
  network_interface {
    subnetwork = local.subnet_id
  }
  service_account {
    email  = google_service_account.invoker[0].email
    scopes = ["cloud-platform"]
  }
  metadata = { enable-oslogin = "TRUE", block-project-ssh-keys = "TRUE" }
  shielded_instance_config {
    enable_secure_boot          = true
    enable_vtpm                 = true
    enable_integrity_monitoring = true
  }
}
resource "google_compute_resource_policy" "access_stop" {
  count   = var.create_access_vm && var.access_vm_on_demand ? 1 : 0
  project = var.project_id
  region  = var.region
  name    = "${var.name_prefix}-hourly-access-stop"
  instance_schedule_policy {
    vm_stop_schedule { schedule = "0 * * * *" }
    time_zone = "Etc/UTC"
  }
  depends_on = [google_project_service.required]
}
resource "google_project_iam_custom_role" "access_scheduler" {
  count       = var.create_access_vm && var.access_vm_on_demand ? 1 : 0
  project     = var.project_id
  role_id     = "${replace(var.name_prefix, "-", "_")}_access_scheduler"
  title       = "GIS AI GO instance schedule permission"
  description = "Scheduled access VM stop safeguard; binding is limited to the owned access instance"
  permissions = ["compute.instances.start", "compute.instances.stop"]
}
resource "google_compute_instance_iam_member" "access_scheduler" {
  count         = var.create_access_vm && var.access_vm_on_demand ? 1 : 0
  project       = var.project_id
  zone          = var.access_vm_zone
  instance_name = google_compute_instance.access[0].name
  role          = google_project_iam_custom_role.access_scheduler[0].name
  member        = "serviceAccount:service-${var.project_number}@compute-system.iam.gserviceaccount.com"
}
resource "google_iap_tunnel_instance_iam_member" "owner" {
  for_each = var.create_access_vm ? toset(var.access_principals) : toset([])
  project  = var.project_id
  zone     = var.access_vm_zone
  instance = google_compute_instance.access[0].name
  role     = "roles/iap.tunnelResourceAccessor"
  member   = each.value
  condition {
    title      = "ssh-only"
    expression = "destination.port == 22"
  }
}
resource "google_compute_instance_iam_member" "os_login" {
  for_each      = var.create_access_vm ? toset(var.access_principals) : toset([])
  project       = var.project_id
  zone          = var.access_vm_zone
  instance_name = google_compute_instance.access[0].name
  role          = "roles/compute.osAdminLogin"
  member        = each.value
}
resource "google_service_account_iam_member" "access_sa" {
  for_each           = var.create_access_vm ? toset(var.access_principals) : toset([])
  service_account_id = google_service_account.invoker[0].name
  role               = "roles/iam.serviceAccountUser"
  member             = each.value
}
