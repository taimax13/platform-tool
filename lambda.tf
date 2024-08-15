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

# Define the IAM policy (same as before)
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

# Attach the policy to the role (same as before)
resource "aws_iam_role_policy_attachment" "lambda_policy_attachment" {
  role       = aws_iam_role.lambda_exec_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# Define the Lambda functions using a for_each loop
module "lambda_functions" {
  source  = "terraform-aws-modules/lambda/aws"
  version = "4.8.0"

  for_each        = { for lambda in var.lambda_functions : lambda.name => lambda }
  function_name   = each.value.name
  handler         = each.value.handler
  runtime         = "python3.8"
  role            = aws_iam_role.lambda_exec_role.arn
  filename        = each.value.filename
  source_code_hash = each.value.source_code_hash

  environment_variables = each.value.environment
}