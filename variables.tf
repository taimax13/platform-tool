variable "project_name" {
  description = "The name of the project."
  type        = string
}

variable "environment" {
  description = "The deployment environment (e.g., dev, prod)."
  type        = string
}

variable "db_username" {
  description = "The username for the database."
  type        = string
  sensitive   = true
}

variable "db_password" {
  description = "The password for the database."
  type        = string
  sensitive   = true
}

variable "db_name" {
  description = "The name of the database."
  type        = string
}

variable "aws_region" {
  description = "The AWS region to deploy to."
  type        = string
  default     = "us-west-2"
}

variable "lambda_functions" {
  description = "List of Lambda functions with their configurations"
  type = list(object({
    name           = string
    handler        = string
    filename       = string
    source_code_hash = string
    environment    = map(string)
  }))
}
