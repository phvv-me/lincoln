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
  region = "us-east-1"
  version = "~> 3.6.0"
}

variable "tags" {
  type = map(string)
  default = {
    "project" = "lincoln"
    "owner"   = "pedro valois"
  }
}