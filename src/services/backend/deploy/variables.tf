variable "tags" {}

variable "is_trigger_enabled" {
  type = bool
  default = false
}

# sensitive variables #
variable "DISCORD_WEBHOOK_URL" {}