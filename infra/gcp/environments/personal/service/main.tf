terraform {
  required_version = ">= 1.12.2, < 1.14.0"
  required_providers {
    google = { source = "hashicorp/google", version = "6.49.0" }
  }
}
provider "google" {
  project = var.project_id
  region  = var.region
}
module "pilot" {
  source                    = "../../../modules/service"
  project_id                = var.project_id
  region                    = var.region
  profile                   = var.profile
  name_prefix               = var.name_prefix
  runtime_email             = var.runtime_email
  invoker_unique_id         = var.invoker_unique_id
  network_id                = var.network_id
  subnet_id                 = var.subnet_id
  image_reference           = var.image_reference
  release_id                = var.release_id
  transport_principals      = var.transport_principals
  cpu                       = var.cpu
  memory                    = var.memory
  max_instances             = var.max_instances
  concurrency               = var.concurrency
  timeout_seconds           = var.timeout_seconds
  runtime_config_json       = var.runtime_config_json
  deletion_protection       = var.deletion_protection
  browser_secret_references = var.browser_secret_references
}

output "service_uri" { value = module.pilot.service_uri }
output "latest_revision" { value = module.pilot.latest_revision }
output "image_reference" { value = module.pilot.image_reference }
output "release_id" { value = module.pilot.release_id }
