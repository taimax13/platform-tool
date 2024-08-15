# platform-tool
this is demo example of tool, developed for platform -  AWS Lambda functions, SQS, and either RDS Postgres or DocumentDB. 

# Platform Application on AWS with Lambda, SQS, and RDS/Postgres

## Overview

This platform application handles incoming telemetry data, processes it, and provides asynchronous responses using AWS Lambda, SQS, and RDS Postgres (or DocumentDB). The architecture is designed to be modular, scalable, and reliable, emphasizing separation of concerns and robust error handling.

## Architecture

### Key Components:
- **Telemetry Processor Lambda**: 
  - Receives telemetry data from the input SQS queue.
  - Processes and stores the data in the database (RDS Postgres or DocumentDB).
  - Sends acknowledgment messages to the output SQS queue.

- **Acknowledgment Handler Lambda**: 
  - Handles acknowledgment messages from the Telemetry Processor Lambda.
  - Logs processing outcomes and manages errors.

- **SQS Queues**: 
  - **Input Queue**: Receives telemetry data and triggers the Telemetry Processor Lambda.
  - **Output Queue**: Collects acknowledgment messages from the Telemetry Processor Lambda.

- **RDS Postgres (or DocumentDB)**: 
  - Stores processed telemetry data.

## Resources

### Telemetry Processor Lambda
- **Purpose**: Processes telemetry data and manages storage and acknowledgment.
- **Environment Variables**:
  - `INPUT_QUEUE_URL`, `OUTPUT_QUEUE_URL`
  - `DB_HOST`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`

### Acknowledgment Handler Lambda
- **Purpose**: Processes and logs acknowledgment messages.
- **Environment Variables**:
  - `OUTPUT_QUEUE_URL`

### SQS Queues
- **Input Queue**: Triggers the Telemetry Processor Lambda with incoming data.
- **Output Queue**: Collects and manages acknowledgment messages.

### RDS Postgres (or DocumentDB)
- **Purpose**: Securely stores the telemetry data processed by the Telemetry Processor Lambda.

## Setup and Deployment

### Prerequisites
- Terraform installed and configured.
- AWS CLI configured with appropriate access.

### Steps to Deploy:
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/platform-application.git
   cd platform-application
### Plan and apply terraform 
```
 terraform plan -var-file="dev.tfvars"
 terraform apply -var-file="dev.tfvars"

```

the output 
```
db_endpoint = "localhost.localstack.cloud:4510"
input_queue_url = "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/platform-app-dev-input-queue"
lambda_acknowledgment_handler_arn = "arn:aws:lambda:us-east-1:000000000000:function:platform-app-dev-acknowledgmentHandler"
lambda_telemetry_processor_arn = "arn:aws:lambda:us-east-1:000000000000:function:platform-app-dev-telemetryProcessor"
output_queue_url = "http://sqs.us-east-1.localhost.localstack.cloud:4566/000000000000/platform-app-dev-output-queue"

```

### Please not for demo purpose I used https://app.localstack.cloud/getting-started