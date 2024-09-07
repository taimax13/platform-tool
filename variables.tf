variable "project_name" {
  description = "The name of the project."
  type        = string
}

variable "environment" {
  description = "The deployment environment (e.g., dev, prod)."
  type        = string
}

variable "aws_region" {
  description = "The AWS region to deploy to."
  type        = string
  default     = "us-west-2"
}

