import unittest
from unittest.mock import patch, MagicMock
import os
import json
from lambdas.simple_lambda import lambda_handler  # Adjust this import path to your project structure

class TestItemManager(unittest.TestCase):

    @patch('lambdas.simple_lambda.boto3.resource')  # Mock boto3.resource
    def test_create_item(self, mock_boto_resource):
        # Create a mock DynamoDB resource and table
        mock_dynamodb = MagicMock()
        mock_table = MagicMock()

        # Setup the mock to return the mock table when Table is called
        mock_boto_resource.return_value = mock_dynamodb
        mock_dynamodb.Table.return_value = mock_table

        # Example event to trigger the Lambda function
        event = {
            'httpMethod': 'POST',
            'body': json.dumps({'itemName': 'Test Item'})
        }

        # Call the Lambda function
        response = lambda_handler(event, None)

        # Decode the body from the response
        body_decoded = json.loads(response['body'])
        print(body_decoded)  # For debugging purposes

        # Assertions to verify the behavior
        mock_table.put_item.assert_called_once_with(
            Item={
                'ItemId': body_decoded['ItemId'],
                'ItemName': 'Test Item'
            }
        )
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('ItemId', body_decoded)
        self.assertEqual(body_decoded['Message'], 'Item created successfully')

if __name__ == '__main__':
    unittest.main()
