
variable "tags" {
  description = "Tags to apply to all resources created by the modules"
  type = map(string)
  default = {
    "project" = "lincoln"
    "owner"   = "pedro valois"
  }
}

# sensitive variables #
variable "DISCORD_TOKEN" {}
variable "DISCORD_WEBHOOK_URL" {}

variable "AWS_ACCESS_KEY_ID" {}
variable "AWS_SECRET_ACCESS_KEY" {}