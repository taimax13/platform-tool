import json
import boto3
import os
import pytest
from moto import mock_sqs, mock_rds

import tes


@mock_sqs
@mock_rds
def test_telemetry_processor():
    # Set up mock SQS and RDS
    sqs = boto3.client('sqs', region_name='us-west-2')
    rds = boto3.client('rds', region_name='us-west-2')

    # Create mock SQS queues
    input_queue = sqs.create_queue(QueueName='input-queue')
    output_queue = sqs.create_queue(QueueName='output-queue')

    # Set environment variables
    os.environ['INPUT_QUEUE_URL'] = input_queue['QueueUrl']
    os.environ['OUTPUT_QUEUE_URL'] = output_queue['QueueUrl']
    os.environ['DB_HOST'] = 'mock-db-host'
    os.environ['DB_NAME'] = 'mock-db-name'
    os.environ['DB_USER'] = 'mock-user'
    os.environ['DB_PASSWORD'] = 'mock-password'

    # Create a mock event
    event = {
        'Records': [
            {
                'body': json.dumps({'id': '12345', 'data': 'telemetry_data'})
            }
        ]
    }

    # Invoke the lambda function
    result = lambda_handler(event, None)

    # Assertions
    assert result['statusCode'] == 200
    # Here you could add more assertions to check if the data was handled correctly,
    # such as verifying that the message was sent to the output queue or that data was correctly processed.
