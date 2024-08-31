module "api_gateway" {
  source  = "terraform-aws-modules/apigateway-v2/aws"
  name          = "${var.project_name}-${var.environment}-api"
  description   = "API Gateway for ${var.project_name} in ${var.environment}"
  protocol_type = "HTTP"

  cors_configuration = {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST", "OPTIONS"]
  }

  target = aws_lambda_function.lambda_functions.arn
  target_type = "lambda"

  security_group_ids = [aws_security_group.lambda_security_group.id]
  vpc_link_id = module.vpc.vpc_id

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
