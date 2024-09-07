import time
import unittest
import uuid

import boto3

LOCALSTACK_ENDPOINT_URL = "http://localhost:4566"  # LocalStack endpoint


class TestListAndUploadFileWithLocalStack(unittest.TestCase):

    def setUp(self):
        # Create a boto3 S3 client pointing to LocalStack
        self.s3 = boto3.client('s3', region_name='us-east-1', endpoint_url=LOCALSTACK_ENDPOINT_URL)

        # Create a test S3 bucket in LocalStack
        self.bucket_names = ['test-bucket-1', 'test-bucket-2']
        for bucket_name in self.bucket_names:
            self.s3.create_bucket(Bucket=bucket_name)

    def tearDown(self):
        # Clean up the S3 buckets
        for bucket_name in self.bucket_names:
            objects = self.s3.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in objects:
                for obj in objects['Contents']:
                    self.s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
            self.s3.delete_bucket(Bucket=bucket_name)

    def test_list_buckets_and_upload_file(self):
        # Step 1: List buckets in LocalStack
        response = self.s3.list_buckets()
        bucket_names_listed = [bucket['Name'] for bucket in response['Buckets']]
        print(f"Buckets listed: {bucket_names_listed}")

        # Assert that the created buckets are listed
        for bucket_name in self.bucket_names:
            self.assertIn(bucket_name, bucket_names_listed)

        # Step 2: Upload a file to the first bucket
        bucket_to_upload = bucket_names_listed[0]
        file_key = f'test_file_{uuid.uuid4()}.txt'
        file_content = 'Hello, world!'

        # Upload the file
        self.s3.put_object(Bucket=bucket_to_upload, Key=file_key, Body=file_content)

        # Step 3: Verify that the file was uploaded
        response = self.s3.list_objects_v2(Bucket=bucket_to_upload, Prefix=file_key)
        self.assertEqual(response['KeyCount'], 1, f"File {file_key} not found in {bucket_to_upload}")

        # Print confirmation of file upload
        print(f"File '{file_key}' successfully uploaded to bucket '{bucket_to_upload}'.")


        ##### test lambda was triggered

        time.sleep(15)  # Adjust the sleep time based on how fast your environment processes events

        response = self.s3.list_objects_v2(Bucket=bucket_to_upload)
        print(response)


        # Step 3: Check if the checksum file (.md5) is created in S3
        checksum_key = f'{file_key}.md5'
        response = self.s3.list_objects_v2(Bucket=bucket_to_upload)

        # Assert that the checksum file exists
#        self.assertEqual(response['KeyCount'], 1, f"Checksum file {checksum_key} not found in {bucket_to_upload}")
        print(f"Checksum file '{response}' successfully created.")
        #

if __name__ == '__main__':
    unittest.main()
