module "s3_bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "~> 3.0"

  bucket = "checksum-source-bucket"  # Replace with your desired bucket name
  versioning = {
    enabled = true
  }

  lifecycle_rule = [
    {
      id      = "clean-up"
      enabled = true
      expiration = {
        days = 365  # Optional: Expire objects after a year
      }
    }
  ]

  tags = {
    Name        = "checksum-source-bucket"
    Environment = "dev"
  }
}
