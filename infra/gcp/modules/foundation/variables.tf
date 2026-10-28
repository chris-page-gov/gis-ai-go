variable "project_id" { type = string }
variable "project_number" { type = string }
variable "region" { type = string }
variable "profile" { type = string }
variable "name_prefix" { type = string }
variable "enable_apis" { type = bool }
variable "publisher_member" { type = string }
variable "create_network" { type = bool }
variable "network_id" { type = string }
variable "subnet_id" { type = string }
variable "subnet_cidr" { type = string }
variable "backup_bucket_name" { type = string }
variable "database_id" { type = string }
variable "create_access_vm" { type = bool }
variable "access_vm_on_demand" {
  type    = bool
  default = true
  validation {
    condition     = !var.create_access_vm || var.access_vm_on_demand
    error_message = "A personal access VM must use on-demand start and scheduled stop safeguards."
  }
}
variable "access_vm_zone" { type = string }
variable "access_vm_image" { type = string }
variable "access_vm_machine_type" { type = string }
variable "access_principals" {
  type = list(string)
  validation {
    condition     = alltrue([for member in var.access_principals : can(regex("^(?:(?:user|group|serviceAccount):[^[:space:]@]+@[^[:space:]@]+|principal(Set)?://iam\\.googleapis\\.com/[^[:space:]*]+)$", member))])
    error_message = "Only explicit authenticated IAM principals are allowed; anonymous/wildcard members are forbidden."
  }
}
variable "create_foundation" { type = bool }
variable "existing_runtime_email" { type = string }
variable "existing_invoker_email" { type = string }
variable "existing_invoker_unique_id" { type = string }
variable "existing_image_repository" { type = string }
