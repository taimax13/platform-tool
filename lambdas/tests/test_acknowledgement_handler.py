import json
import boto3
import os
import pytest
from moto import mock_sqs

from lambdas.acknoledgement import lambda_handler

@mock_sqs
def test_acknowledgment_handler():
    # Set up mock SQS
    sqs = boto3.client('sqs', region_name='us-west-2')

    # Create mock SQS queue
    output_queue = sqs.create_queue(QueueName='output-queue')

    # Set environment variables
    os.environ['OUTPUT_QUEUE_URL'] = output_queue['QueueUrl']

    # Create a mock event
    event = {
        'Records': [
            {
                'body': json.dumps({'status': 'processed', 'id': '12345'})
            }
        ]
    }

    # Invoke the lambda function
    result = lambda_handler(event, None)

    # Assertions
    assert result['statusCode'] == 200
    # You can add more assertions to verify that the acknowledgment was handled correctly.
