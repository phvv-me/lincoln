resource "aws_s3_bucket" "static_files" {
  bucket = "backend-static-files"
  acl    = "private"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = merge(var.tags, {
    name = "backend-bucket"
  })
}