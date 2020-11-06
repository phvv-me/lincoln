#############################
# Dependencies Lambda Layer #
#############################

locals {
  name = "python-layer"
  description = "python dependencies from requirements.txt"

  source_dir = "${path.module}/lambda_layer/"
  filename = "lambda_layer.zip"
}

data "archive_file" "requirements_zip_package" {
  type = "zip"
  source_dir = local.source_dir
  output_path = local.filename
}

resource "aws_s3_bucket_object" "layer_package_s3_object" {
  bucket = aws_s3_bucket.static_files.id
  key = data.archive_file.requirements_zip_package.output_path
  source = data.archive_file.requirements_zip_package.output_path
  etag = data.archive_file.requirements_zip_package.output_md5
}

resource "aws_lambda_layer_version" "python_dependencies_layer" {
  layer_name = local.name
  description = local.description

  s3_bucket = aws_s3_bucket.static_files.bucket
  s3_key = aws_s3_bucket_object.layer_package_s3_object.key
  source_code_hash = aws_s3_bucket_object.layer_package_s3_object.content_base64

  compatible_runtimes = [
    "python3.8"
  ]
}