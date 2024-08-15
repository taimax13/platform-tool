resource "aws_lambda_function" "telemetry_processor_lambda" {
  function_name = "${var.project_name}-${var.environment}-telemetryProcessor"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  role          = aws_iam_role.lambda_exec_role.arn
  source_code_hash = filebase64sha256("path_to_your_lambda_zip/telemetry_processor.zip")
  filename      = "path_to_your_lambda_zip/telemetry_processor.zip"

  environment {
    variables = {
      INPUT_QUEUE_URL  = module.input_queue.queue_url
      OUTPUT_QUEUE_URL = module.output_queue.queue_url
      DB_HOST          = aws_rds_instance.db_instance.endpoint
      DB_NAME          = var.db_name
      DB_USER          = var.db_username
      DB_PASSWORD      = var.db_password
    }
  }
}

resource "aws_lambda_function" "acknowledgment_handler_lambda" {
  function_name = "${var.project_name}-${var.environment}-acknowledgmentHandler"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.8"
  role          = aws_iam_role.lambda_exec_role.arn
  source_code_hash = filebase64sha256("path_to_your_lambda_zip/acknowledgment_handler.zip")
  filename      = "path_to_your_lambda_zip/acknowledgment_handler.zip"

  environment {
    variables = {
      OUTPUT_QUEUE_URL = module.output_queue.queue_url
    }
  }
}

resource "aws_iam_role" "lambda_exec_role" {
  name = "${var.project_name}-${var.environment}-lambda-exec-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_policy" {
  name        = "${var.project_name}-${var.environment}-lambda-policy"
  description = "IAM policy for Lambda to access SQS and RDS"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect   = "Allow",
        Action   = [
          "sqs:SendMessage",
          "sqs:ReceiveMessage",
          "sqs:DeleteMessage",
          "sqs:GetQueueAttributes"
        ],
        Resource = [
          module.input_queue.sqs_queue_arn,
          module.output_queue.sqs_queue_arn
        ]
      },
      {
        Effect   = "Allow",
        Action   = [
          "rds-data:ExecuteStatement",
          "rds-data:BatchExecuteStatement"
        ],
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}
