project_name = "platform-app"
environment  = "dev"
db_username = "admin"
db_password = "password"
db_name     = "telemetrydb"
aws_region = "us-west-2"
lambda_functions = [
  {
    name           = "telemetryProcessor"
    handler        = "lambda_function.lambda_handler"
    filename       = "./lambda/telemetry_processor.zip"
    source_code_hash = filebase64sha256("./lambda/telemetry_processor.zip")
    environment = {
      INPUT_QUEUE_URL  = "https://sqs.us-west-2.amazonaws.com/123456789012/input-queue"
      OUTPUT_QUEUE_URL = "https://sqs.us-west-2.amazonaws.com/123456789012/output-queue"
      DB_HOST          = "mydb.host.com"
      DB_NAME          = "mydb"
      DB_USER          = "admin"
      DB_PASSWORD      = "password"
    }
  },
  {
    name           = "acknowledgmentHandler"
    handler        = "lambda_function.lambda_handler"
    filename       = "./lambda/acknowledgment_handler.zip"
    source_code_hash = filebase64sha256("./lambda/acknowledgment_handler.zip")
    environment = {
      OUTPUT_QUEUE_URL = "https://sqs.us-west-2.amazonaws.com/123456789012/output-queue" ##accound id NOT in demo can be replaced by placeholder
    }
  }
]