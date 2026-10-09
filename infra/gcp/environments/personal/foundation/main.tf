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
  source                     = "../../../modules/foundation"
  project_number             = var.project_number
  access_vm_on_demand        = var.access_vm_on_demand
  project_id                 = var.project_id
  region                     = var.region
  profile                    = var.profile
  name_prefix                = var.name_prefix
  enable_apis                = var.enable_apis
  publisher_member           = var.publisher_member
  create_network             = var.create_network
  network_id                 = var.network_id
  subnet_id                  = var.subnet_id
  subnet_cidr                = var.subnet_cidr
  backup_bucket_name         = var.backup_bucket_name
  database_id                = var.database_id
  create_access_vm           = var.create_access_vm
  access_vm_zone             = var.access_vm_zone
  access_vm_image            = var.access_vm_image
  access_vm_machine_type     = var.access_vm_machine_type
  access_principals          = var.access_principals
  create_foundation          = var.create_foundation
  existing_runtime_email     = var.existing_runtime_email
  existing_invoker_email     = var.existing_invoker_email
  existing_invoker_unique_id = var.existing_invoker_unique_id
  existing_image_repository  = var.existing_image_repository
}

output "runtime_email" { value = module.pilot.runtime_email }
output "invoker_email" { value = module.pilot.invoker_email }
output "invoker_unique_id" { value = module.pilot.invoker_unique_id }
output "network_id" { value = module.pilot.network_id }
output "subnet_id" { value = module.pilot.subnet_id }
output "image_repository" { value = module.pilot.image_repository }
output "backup_bucket" { value = module.pilot.backup_bucket }
output "database_id" { value = module.pilot.database_id }
output "access_vm" { value = module.pilot.access_vm }
