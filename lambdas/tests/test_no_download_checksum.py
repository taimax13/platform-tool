import moto
import unittest
import boto3
from unittest.mock import patch
from lambdas.checksum_no_download import lambda_handler  # Adjust the import based on your file structure


class TestLambdaHandlerETag(unittest.TestCase):

    def setUp(self):
        # Start Moto's AWS mock (using mock_aws for newer versions)
        self.mock_aws = moto.mock_aws()  # This mocks all AWS services, including S3
        self.mock_aws.start()

        # Create a boto3 S3 client and create a mock S3 bucket
        self.s3 = boto3.client('s3', region_name='us-east-1')
        self.bucket_name = 'test-bucket'
        self.s3.create_bucket(Bucket=self.bucket_name)

        # Upload a mock file to the S3 bucket
        self.file_key = 'test_file.txt'
        self.file_content = 'Hello, world!'
        self.s3.put_object(Bucket=self.bucket_name, Key=self.file_key, Body=self.file_content)

        # Validate that the file has been uploaded
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=self.file_key)
        print(response)
        self.assertEqual(response['KeyCount'], 1, f"File {self.file_key} not found in S3 during setup")

    def tearDown(self):
        # Stop Moto's AWS mock
        self.mock_aws.stop()

    @patch('boto3.client')  # Mock the entire S3 client
    def test_lambda_handler(self, mock_boto_client):
        # Arrange: Prepare a mock S3 event
        event = {
            'Records': [{
                's3': {
                    'bucket': {'name': self.bucket_name},
                    'object': {'key': self.file_key}
                }
            }]
        }

        # Mock the head_object method to return an ETag
        mock_s3_client = mock_boto_client.return_value
        mock_s3_client.head_object.return_value = {
            'ETag': '"6cd3556deb0da54bca060b4c39479839"'  # Simulating the ETag (MD5 checksum)
        }

        # Act: Call the lambda handler
        result = lambda_handler(event, None)

        # Print the result to inspect the error
        print(f"Lambda handler result: {result}")

        # Assert: Verify if the response and behavior are as expected
        self.assertEqual(result['statusCode'], 200)
        self.assertIn('MD5 checksum', result['body'])

        # Verify that the MD5 checksum file was created in S3
        checksum_key = f'{self.file_key}.md5'
        response = self.s3.get_object(Bucket=self.bucket_name, Key=checksum_key)
        checksum_content = response['Body'].read().decode('utf-8')

        # Assert: The checksum should be the MD5 of 'Hello, world!' (ETag)
        expected_md5 = "6cd3556deb0da54bca060b4c39479839"  # The correct MD5 for 'Hello, world!'
        self.assertEqual(checksum_content, expected_md5)

    def test_calculate_md5(self):
        # This method can remain unchanged for now, but it can be omitted in this version of the test if needed
        pass


if __name__ == '__main__':
    unittest.main()
