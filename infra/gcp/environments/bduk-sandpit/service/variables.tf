variable "project_id" { type = string }
variable "region" { type = string }
variable "profile" { type = string }
variable "name_prefix" { type = string }
variable "runtime_email" { type = string }
variable "invoker_unique_id" { type = string }
variable "network_id" { type = string }
variable "subnet_id" { type = string }
variable "image_reference" { type = string }
variable "release_id" { type = string }
variable "transport_principals" {
  type = list(string)
  validation {
    condition     = alltrue([for member in var.transport_principals : can(regex("^(?:(?:user|group|serviceAccount):[^[:space:]@]+@[^[:space:]@]+|principal(Set)?://iam\\.googleapis\\.com/[^[:space:]*]+)$", member))])
    error_message = "Only explicit authenticated IAM principals are allowed; anonymous/wildcard members are forbidden."
  }
}
variable "cpu" { type = string }
variable "memory" { type = string }
variable "max_instances" { type = number }
variable "concurrency" { type = number }
variable "timeout_seconds" { type = number }
variable "runtime_config_json" { type = string }
variable "deletion_protection" { type = bool }
variable "browser_secret_references" {
  type    = map(object({ resource = string, version = string }))
  default = {}
  validation {
    condition     = alltrue([for name, reference in var.browser_secret_references : contains(["GCP_BROWSER_SESSION_KEY", "GCP_OIDC_CLIENT_SECRET"], name) && can(regex("^projects/[a-z0-9-]+/secrets/[A-Za-z0-9_-]+$", reference.resource)) && can(regex("^[1-9][0-9]*$", reference.version))])
    error_message = "Browser secrets require approved Secret Manager resource names and immutable numeric versions."
  }
}
