# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lambda_s3_access_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [{
      Action    = "sts:AssumeRole",
      Effect    = "Allow",
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# IAM Policy for Lambda S3 access
resource "aws_iam_policy" "lambda_s3_policy" {
  name = "lambda_s3_access_policy"
  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = ["s3:HeadBucket","s3:ListBucket", "s3:GetObject", "s3:PutObject"],
        Effect = "Allow",
        Resource = ["${module.s3_bucket.s3_bucket_arn}", "${module.s3_bucket.s3_bucket_arn}/*"]
      }
    ]
  })
}

# Attach IAM policy to role
resource "aws_iam_role_policy_attachment" "attach_policy" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_s3_policy.arn
}
