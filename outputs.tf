output "input_queue_url" {
  value = module.input_queue.sqs_queue_url
}

output "output_queue_url" {
  value = module.output_queue.sqs_queue_url
}

output "lambda_telemetry_processor_arn" {
  value = module.telemetry_processor_lambda.lambda_function_arn
}

output "lambda_acknowledgment_handler_arn" {
  value = module.acknowledgment_handler_lambda.lambda_function_arn
}

output "db_endpoint" {
  value = aws_rds_instance.db_instance.endpoint
}