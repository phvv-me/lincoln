############################
# Lambda Scheduled Trigger #
############################

resource "aws_cloudwatch_event_rule" "every_half_hour" {
  is_enabled = var.is_trigger_enabled

  name                = "half-hour-trigger"
  description         = "Fires every 30 minutes between 8:00 - 20:30 BST from Monday to Friday"
  schedule_expression = "cron(0/30 11-21 ? * MON-FRI *)"

  tags = merge(var.tags, {
    name = "lambda function schedule rule"
  })
}

resource "aws_cloudwatch_event_target" "lambda_schedule_target" {
  target_id = "TriggerLambda"
  rule      = aws_cloudwatch_event_rule.every_half_hour.name
  arn       = aws_lambda_function.service_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_function" {
  statement_id = "AllowExecutionFromCloudWatch"
  action       = "lambda:InvokeFunction"
  principal    = "events.amazonaws.com"

  function_name = aws_lambda_function.service_lambda.function_name
  source_arn    = aws_cloudwatch_event_rule.every_half_hour.arn
}