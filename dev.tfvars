project_name = "platform-app"
environment  = "dev"
db_username = "admin"
db_password = "password"
db_name     = "simpledb"
aws_region = "us-west-2"
lambda_functions = [
  {
    name           = "simple_lambda"
    handler        = "lambda_function.lambda_handler"
    filename       = "./lambdas/simple_lambda.zip"
    source_code_hash = "./lambdas/simple_lambda.zip"
    environment = {

    }
  },
  {
    name           = "lambda_rds"
    handler        = "lambda_function.lambda_handler"
    filename       = "./lambdas/lambda_rds.zip"
    source_code_hash = "./lambdas/lambda_rds.zip"
    environment = {
      DB_HOST          = "mydb.host.com"
      DB_NAME          = "mydb"
      DB_USER          = "admin"
      DB_PASSWORD      = "password"
    }
  }
]