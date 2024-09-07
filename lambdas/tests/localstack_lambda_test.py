import unittest
import uuid

import boto3
import time
from unittest.mock import patch, mock_open
from lambdas.checksum import lambda_handler, calculate_md5  # Adjust the import based on your file structure

LOCALSTACK_ENDPOINT_URL = "http://localhost:4566"  # LocalStack endpoint for S3

class TestLambdaHandlerWithLocalStack(unittest.TestCase):

    def setUp(self):
        self.s3 = boto3.client('s3', region_name='us-east-1', endpoint_url=LOCALSTACK_ENDPOINT_URL)

        # Use an existing bucket in LocalStack instead of creating a new one
        self.bucket_name = 'checksum-source-bucket'
        self.file_key = f'test_file_{str(uuid.uuid4())[:4]}.txt'
        self.file_content = 'Hello, world!'

        # Upload a mock file to the S3 bucket
        self.s3.put_object(Bucket=self.bucket_name, Key=self.file_key, Body=self.file_content)
        #self.validate_file()

    def validate_file(self):
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        self.assertIn('Contents', response, f"File {self.file_key} not found in S3 during setup")
        print(f"Uploaded file details: {response}")

    def tearDown(self):
        # Cleanup: remove the uploaded file and its checksum from the bucket
        objects = self.s3.list_objects_v2(Bucket=self.bucket_name)
        if 'Contents' in objects:
            for obj in objects['Contents']:
                self.s3.delete_object(Bucket=self.bucket_name, Key=obj['Key'])

    @patch('os.remove')
    def test_lambda_handler_with_localstack(self, mock_remove):
        print("INTO lambda test")
        print(self.validate_file())
        event = {
            'Records': [{
                's3': {
                    'bucket': {'name': self.bucket_name},
                    'object': {'key': self.file_key}
                }
            }]
        }

        # Act: Call the lambda handler
        result = lambda_handler(event, None)

        # Print the result to inspect the outcome
        print(f"Lambda handler result: {result}")

        # Assert: Verify if the response and behavior are as expected
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('MD5 checksum', result['body'])

        # Verify that the MD5 checksum file was created in S3
        checksum_key = f'{self.file_key}.md5'
        response = self.s3.get_object(Bucket=self.bucket_name, Key=checksum_key)
        checksum_content = response['Body'].read().decode('utf-8')

        # Assert: The checksum should be the MD5 of 'Hello, world!'
        expected_md5 = "6cd3556deb0da54bca060b4c39479839"  # The correct MD5 for 'Hello, world!'
        self.assertEqual(checksum_content, expected_md5)

        # Assert: Ensure the temporary file was cleaned up
        mock_remove.assert_called_once_with(f'/tmp/{self.file_key}')

    def test_calculate_md5(self):
        # Test the MD5 calculation separately
        test_content = b"Hello, world!"
        expected_md5 = "6cd3556deb0da54bca060b4c39479839"

        with patch('builtins.open', mock_open(read_data=test_content)):
            result = calculate_md5('/fake/path')

        print(result)
        self.assertEqual(result, expected_md5)


if __name__ == '__main__':
    unittest.main()
