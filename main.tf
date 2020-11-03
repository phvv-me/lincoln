terraform {
  required_providers {
    aws = {
      # uses the latest provider from hashicorp registry
      source = "hashicorp/aws"
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

resource "aws_dynamodb_table" "input_dynamodb_table" {
  name             = "bot"
  billing_mode     = "PROVISIONED"
  stream_view_type = "KEYS_ONLY"
  stream_enabled   = true
  read_capacity    = 5
  write_capacity   = 5
  hash_key         = "symbol"

  attribute {
    name = "symbol"
    type = "S"
  }

  tags = merge(var.tags, {
    Name = "${var.tags.project}-dynamodb-table"
  })
}