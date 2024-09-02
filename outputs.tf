output "input_queue_url" {
  value = module.input_queue.queue_url
}

output "output_queue_url" {
  value = module.output_queue.queue_url
}

output "lambda_function_arns" {
  value = {
    for name, lambda in aws_lambda_function.lambda_functions : name => lambda.arn
  }
}

output "db_endpoint" {
  value = module.rds_postgres.db_instance_endpoint
}