output "input_queue_url" {
  value = module.input_queue.queue_url
}

output "output_queue_url" {
  value = module.output_queue.queue_url
}

output "lambda_telemetry_processor_arn" {
  value = aws_lambda_function.lambda_functions["telemetryProcessor"].arn
}

output "lambda_acknowledgment_handler_arn" {
  value = aws_lambda_function.lambda_functions["acknowledgmentHandler"].arn
}


output "db_endpoint" {
  value = module.rds_postgres.db_instance_endpoint
}