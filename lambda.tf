module "lambda_function" {
  source = "terraform-aws-modules/lambda/aws"

  function_name = "${var.environment}-checksum-calculation-lambda"
  description   = "Lambda function to calculate MD5 checksum for S3 objects"
  handler       = "lambda_function.lambda_handler"
  runtime       = "python3.12"
  publish       = true
  package_type = "Zip"
  source_path = "./lambdas/"
  create_role = false
  lambda_role = aws_iam_role.lambda_role.arn
  # IAM Policies to allow S3 read/write permissions for checksum calculation
  #attach_policy_json = true
  policies = [aws_iam_policy.lambda_s3_policy.arn]
  # Additional policies for required AWS services
  attach_policy = true
  policy        = "arn:aws:iam::aws:policy/AWSLambdaExecute"

  tags = {
    Environment = "dev"
    Module      = "checksum-lambda"
  }
}

resource "aws_s3_bucket_notification" "s3_event" {
  bucket = module.s3_bucket.s3_bucket_id

  lambda_function {
    lambda_function_arn = module.lambda_function.lambda_function_arn
    events              = ["s3:ObjectCreated:*"]
  }

  depends_on = [module.lambda_function]  # Ensure Lambda is created before setting notification
}

