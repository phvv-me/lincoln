terraform {
  required_providers {
    aws = {
      # uses the latest provider from hashicorp registry
      source = "hashicorp/aws"
    }
  }
  backend "remote" {
    organization = "phvv"

    workspaces {
      // from terraform cloud
      name = "lincoln"
    }
  }
}

provider "aws" {
  # looks for credentials in ~/.aws/credentials
  profile = "default"
  # N. Virginia
  region  = "us-east-1"
}

module "bot" {
  source = "./services/bot/deploy"

  DISCORD_TOKEN         = var.DISCORD_TOKEN
  AWS_ACCESS_KEY_ID     = var.AWS_ACCESS_KEY_ID
  AWS_SECRET_ACCESS_KEY = var.AWS_SECRET_ACCESS_KEY

  tags = var.tags
}

module "backend" {
  source = "./services/backend/deploy"

  is_trigger_enabled = true

  DISCORD_WEBHOOK_URL = var.DISCORD_WEBHOOK_URL

  tags = var.tags
}

module "common" {
  source = "./services/common/deploy"

  tags = var.tags
}