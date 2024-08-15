import json
import boto3
import os
from unittest.mock import patch, MagicMock
from moto.backends import get_backend
from moto.sqs.models import SQSBackend
from moto.rds.models import RDSBackend
from unittest.mock import patch

# Manually register SQS and RDS backends to use them
sqs_backend = get_backend("sqs")
rds_backend = get_backend("rds")


from lambdas.acknoledgement import lambda_handler

@patch('boto3.client')
def test_acknowledgment_handler(mock_boto_client):
    mock_sqs = MagicMock()
    mock_boto_client.return_value = mock_sqs

    # Define the mock event
    event = {
        'Records': [
            {
                'body': json.dumps({'status': 'processed', 'id': '12345'})
            }
        ]
    }

    # Call the lambda handler
    response = lambda_handler(event, None)

    # Assertions to verify behavior
    mock_sqs.send_message.assert_not_called()  # Adjust based on what your function should do
    assert response['statusCode'] == 200

