module "lambda_iam_role" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-role"
  version = "5.0.0"

  name = "${var.project_name}-${var.environment}-lambda-exec-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })

  policies = [{
    name   = "lambda-policy"
    policy = jsonencode({
      Version = "2012-10-17",
      Statement = [
        {
          Effect   = "Allow"
          Action   = ["sqs:SendMessage", "sqs:ReceiveMessage", "sqs:DeleteMessage", "sqs:GetQueueAttributes"]
          Resource = [module.input_queue.sqs_queue_arn, module.output_queue.sqs_queue_arn]
        },
        {
          Effect   = "Allow"
          Action   = ["rds-data:ExecuteStatement", "rds-data:BatchExecuteStatement"]
          Resource = "*"
        }
      ]
    })
  }]
}

module "telemetry_processor_lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "4.8.0"

  function_name = "${var.project_name}-${var.environment}-telemetryProcessor"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  source_path   = "path_to_your_lambda_zip/telemetry_processor.zip"

  environment_variables = {
    INPUT_QUEUE_URL  = module.input_queue.sqs_queue_url
    OUTPUT_QUEUE_URL = module.output_queue.sqs_queue_url
    DB_HOST          = aws_rds_instance.db_instance.endpoint
    DB_NAME          = var.db_name
    DB_USER          = var.db_username
    DB_PASSWORD      = var.db_password
  }

  role = module.lambda_iam_role.iam_role_arn
}

module "acknowledgment_handler_lambda" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "4.8.0"

  function_name = "${var.project_name}-${var.environment}-acknowledgmentHandler"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  source_path   = "path_to_your_lambda_zip/acknowledgment_handler.zip"

  environment_variables = {
    OUTPUT_QUEUE_URL = module.output_queue.sqs_queue_url
  }

  role = module.lambda_iam_role.iam_role_arn
}
