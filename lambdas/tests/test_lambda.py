import moto
import unittest
import boto3
from unittest.mock import patch, mock_open
from lambdas.checksum import lambda_handler, calculate_md5  # Adjust the import based on your file structure


class TestLambdaHandler(unittest.TestCase):

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
    @patch('os.remove')
    def test_lambda_handler(self, mock_remove, mock_boto_client):
        # Arrange: Prepare a mock S3 event
        event = {
            'Records': [{
                's3': {
                    'bucket': {'name': self.bucket_name},
                    'object': {'key': self.file_key}
                }
            }]
        }

        # Mock the download_file method
        mock_s3_client = mock_boto_client.return_value
        mock_s3_client.download_file.side_effect = self.mock_download_file  # Simulate download

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

        # Assert: The checksum should be the MD5 of 'Hello, world!'
        expected_md5 = "6cd3556deb0da54bca060b4c39479839"  # The correct MD5 for 'Hello, world!'
        self.assertEqual(checksum_content, expected_md5)

        # Assert: Ensure the temporary file was cleaned up
        mock_remove.assert_called_once_with(f'/tmp/{self.file_key}')

    def mock_download_file(self, Bucket, Key, Filename):
        """Mock the S3 download_file method"""
        with open(Filename, 'w') as f:
            f.write(self.file_content)  # Simulate the file being downloaded

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
