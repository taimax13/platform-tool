import json
import boto3
import os

from moto.backends import get_backend
from moto.sqs.models import SQSBackend
from moto.rds.models import RDSBackend
from unittest.mock import patch

# Manually register SQS and RDS backends to use them
sqs_backend = get_backend("sqs")
rds_backend = get_backend("rds")


from lambdas.acknoledgement import lambda_handler

@patch("boto3.client")
def test_acknowledgment_handler():
    sqs = boto3.client('sqs', region_name='us-west-2')
    output_queue = sqs.create_queue(QueueName='output-queue')
    os.environ['OUTPUT_QUEUE_URL'] = output_queue['QueueUrl']
    event = {
        'Records': [
            {
                'body': json.dumps({'status': 'processed', 'id': '12345'})
            }
        ]
    }
    result = lambda_handler(event, None)
    assert result['statusCode'] == 200

