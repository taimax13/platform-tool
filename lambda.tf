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
          module.input_queue.queue_arn,
          module.output_queue.queue_arn
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

resource "aws_lambda_function" "lambda_functions" {
  for_each        = { for lambda in var.lambda_functions : lambda.name => lambda }

  function_name   = "${var.project_name}-${var.environment}-${each.value.name}"
  handler         = each.value.handler
  runtime         = "python3.8"
  role            = aws_iam_role.lambda_exec_role.arn
  filename        = each.value.filename
  source_code_hash = filebase64sha256(each.value.source_code_hash)

  environment {
    variables = each.value.environment
  }

  vpc_config {
    subnet_ids         = module.vpc.private_subnets
    security_group_ids = [aws_security_group.lambda_security_group.id]
  }
}

resource "aws_security_group" "lambda_security_group" {
  name_prefix = "${var.project_name}-${var.environment}-lambda-sg"
  vpc_id      = module.vpc.vpc_id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
