data "aws_region" "current" {}
data "aws_caller_identity" "current" {}

##########
# Lambda #
##########

# assume role policy
data "aws_iam_policy_document" "lambda_assume_role_policy" {
  statement {
    actions = [
      "sts:AssumeRole"
    ]

    principals {
      type = "Service"
      identifiers = [
        "lambda.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name = "backend-lambda-role"
  path = "/system/"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role_policy.json

  lifecycle {
    create_before_destroy = true
  }

  tags = merge(var.tags, {
    name = "backend-lambda-role"
  })
}

data "aws_iam_policy_document" "lambda_execution_policy_document" {
  // Logs
  statement {
    actions = [
      "logs:CreateLogStream",
      "logs:CreateLogGroup",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:*:*:*"]
  }
  // DynamoDB Scan
  statement {
    actions = [
      "dynamodb:Scan",
      "dynamodb:PutItem"
    ]
    resources = [
      "arn:aws:dynamodb:*:*:*"]
  }
}

resource "aws_iam_policy" "lambda_execution_policy" {
  name = "backend-lambda-execution-policy"
  path = "/"
  description = "IAM policy for backend lambda function"
  policy = data.aws_iam_policy_document.lambda_execution_policy_document.json
}

resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_execution_policy.arn
}

#############
# S3 Bucket #
#############

data "aws_iam_policy_document" "s3_bucket_policy_document" {
  // denies all s3 access without ssl
  // complies with s3-bucket-ssl-requests-only rule
  statement {
    effect = "Deny"
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::${aws_s3_bucket.static_files.bucket}/*"]

    # anonymous user
    principals {
      identifiers = [
        "*"
      ]
      type = "*"
    }

    condition {
      test = "Bool"
      values = [
        false
      ]
      variable = "aws:SecureTransport"
    }
  }
}

resource "aws_s3_bucket_policy" "static_files_policy" {
  bucket = aws_s3_bucket.static_files.bucket
  policy = data.aws_iam_policy_document.s3_bucket_policy_document.json
}