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

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw_logs.arn
    format          = jsonencode({
      requestId       = "$context.requestId"
      ip              = "$context.identity.sourceIp"
      caller          = "$context.identity.caller"
      user            = "$context.identity.user"
      requestTime     = "$context.requestTime"
      httpMethod      = "$context.httpMethod"
      resourcePath    = "$context.resourcePath"
      status          = "$context.status"
      protocol        = "$context.protocol"
      responseLength  = "$context.responseLength"
    })
  }

  xray_tracing_enabled = true
  tags = {
    Project     = var.project_name
    Environment = var.environment
  }

}


resource "aws_cloudwatch_log_group" "api_gw_logs" {
  name              = "/aws/api-gateway/example"
  retention_in_days = 14
}