#############################
# Lambda Scheduled Triggers #
#############################

variable "scheduled_tasks" {
  type = list(map(string))
  default = [
    {
      function: "app.handlers.watch.watch_handler",
      description: "Fires every 30 minutes between 8:00 - 20:30 BST from Monday to Friday",
      expression: "cron(0/30 11-21 ? * MON-FRI *)"
    },
    {
      function: "app.handlers.evaluate.evaluation_handler",
      description: "Fires every 4 hours between 8:00 - 20:30 BST from Monday to Friday",
      expression: "cron(0 11-21/4 ? * MON-FRI *)"
    }
  ]
}

resource "aws_cloudwatch_event_rule" "scheduled_tasks_rules" {
  is_enabled = var.is_trigger_enabled

  count = length(var.scheduled_tasks)

  name = var.scheduled_tasks[count.index].function
  description = var.scheduled_tasks[count.index].description
  schedule_expression = var.scheduled_tasks[count.index].expression

  tags = merge(var.tags, {
    name = "trigger-${var.scheduled_tasks[count.index].function}"
  })
}

resource "aws_cloudwatch_event_target" "lambda_schedule_target" {
  count = length(var.scheduled_tasks)

  rule = aws_cloudwatch_event_rule.scheduled_tasks_rules[count.index].name
  target_id = "TriggerLambda-${count.index}"
  arn = aws_lambda_function.service_lambda.arn
}

resource "aws_lambda_permission" "allow_cloudwatch_to_call_function" {
  statement_id = "AllowExecutionFromCloudWatch-${count.index}"
  action = "lambda:InvokeFunction"
  principal = "events.amazonaws.com"

  function_name = aws_lambda_function.service_lambda.function_name
  source_arn = aws_cloudwatch_event_rule.scheduled_tasks_rules[count.index].arn
}