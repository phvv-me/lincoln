variable service {
  type = map(string)
  # service location
  default = {
    name        = "backend"
    description = "webhook discord"
    filename    = "lambda_backend.zip"
  }
}

data "archive_file" "service_zip_package" {
  type        = "zip"
  source_dir  = "${path.module}/../app"

  # forces file update and not just etag update
  output_path = "${timestamp()}-${var.service.filename}"
}

resource "aws_s3_bucket_object" "service_package_s3_object" {
  bucket = aws_s3_bucket.static_files.id
  key    = data.archive_file.service_zip_package.output_path
  source = data.archive_file.service_zip_package.output_path
  etag   = data.archive_file.service_zip_package.output_md5
}

resource "aws_lambda_function" "service_lambda" {
  depends_on = [
    aws_s3_bucket_object.service_package_s3_object,
    aws_iam_role_policy_attachment.lambda_policy,
  ]

  layers = [aws_lambda_layer_version.python_dependencies_layer.arn]

  # S3 bucket must exist with a packaged .zip before terraform apply
  s3_bucket        = aws_s3_bucket.static_files.bucket
  s3_key           = aws_s3_bucket_object.service_package_s3_object.key
  source_code_hash = aws_s3_bucket_object.service_package_s3_object.content_base64

  publish       = true
  function_name = var.service.name
  description   = var.service.description
  role          = aws_iam_role.lambda_role.arn
  handler       = "main.handler"
  memory_size   = 256
  timeout       = 6
  runtime       = "python3.8"

  environment {
    variables = {
      DISCORD_WEBHOOK_URL = var.DISCORD_WEBHOOK_URL
    }
  }

  tracing_config {
    # disables X-Ray
    mode = "PassThrough"
  }

  tags = merge(var.tags, {
    name = var.service.name
  })
}