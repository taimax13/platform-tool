module "input_queue" {
  source  = "terraform-aws-modules/sqs/aws"
  version = "4.0.0"

  name = "${var.project_name}-${var.environment}-input-queue"
}

module "output_queue" {
  source  = "terraform-aws-modules/sqs/aws"
  version = "4.0.0"

  name = "${var.project_name}-${var.environment}-output-queue"
}
