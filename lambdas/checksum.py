import boto3
import botocore
import hashlib
import os
import logging

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
#s3_client = boto3.client('s3')



#####NOTE!!!! - THIS is only for texting in localstack
LOCALSTACK_ENDPOINT_URL = "http://localhost:4566"
s3_client = boto3.client('s3', region_name='us-east-1', endpoint_url=LOCALSTACK_ENDPOINT_URL)

# Configuration
CHUNK_SIZE = 8192  # Increased chunk size for potentially better performance

def lambda_handler(event, context):
    try:
        # Extract bucket name and object key from the event triggered by S3
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']

        logger.info(f"Processing file: {object_key} in bucket: {bucket_name}")

        # Download the object to the Lambda's local /tmp directory
        download_path = f'/tmp/{os.path.basename(object_key)}'
        download_file(bucket_name, object_key, download_path)

        # Calculate the MD5 checksum of the file
        checksum = calculate_md5(download_path)

        # Create the MD5 file with the same prefix but with .md5 extension
        checksum_key = f'{object_key}.md5'
        upload_checksum(bucket_name, checksum_key, checksum)

        # Clean up the temporary file
        os.remove(download_path)
        logger.info(f"Temporary file removed: {download_path}")

        return {
            'statusCode': 200,
            'body': f'MD5 checksum {checksum} stored as {checksum_key}'
        }
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error processing file: {str(e)}'
        }


def validate_bucket_access(bucket):
    """Check if the bucket exists and the client can access it."""
    try:
        s3_client.head_bucket(Bucket=bucket)
        logger.info(f"Bucket {bucket} exists and is accessible")
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 403:
            logger.error(f"Access to the bucket {bucket} is forbidden")
        elif error_code == 404:
            logger.error(f"Bucket {bucket} does not exist")
        raise e


def download_file(bucket, key, download_path):
    try:
        # Validate connection to the bucket
        validate_bucket_access(bucket)

        logger.info(f"Attempting to download file {key} from bucket {bucket} to {download_path}")
        response = s3_client.list_objects_v2(Bucket=bucket)
        print(response)  # Prints the response to ensure file is listed

        # Check if the file is listed before attempting to download
        if 'Contents' not in response or not any(item['Key'] == key for item in response['Contents']):
            logger.error(f"File {key} not found in S3 bucket {bucket}")
            raise FileNotFoundError(f"File {key} not found in bucket {bucket}")

        s3_client.download_file(bucket, key, download_path)
        logger.info(f"File downloaded successfully: {download_path}")
    except botocore.exceptions.ClientError as e:
        logger.error(f"Error downloading file from S3: {str(e)}")
        raise


def calculate_md5(file_path):
    """Calculate the MD5 checksum for the given file."""
    hash_md5 = hashlib.md5()
    try:
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(CHUNK_SIZE), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except IOError as e:
        logger.error(f"Error reading file for MD5 calculation: {str(e)}")
        raise


def upload_checksum(bucket, key, checksum):
    """Upload the MD5 checksum to S3."""
    try:
        # Validate connection to the bucket
        validate_bucket_access(bucket)

        s3_client.put_object(Bucket=bucket, Key=key, Body=checksum)
        logger.info(f"MD5 checksum uploaded successfully: {key}")
    except botocore.exceptions.ClientError as e:
        logger.error(f"Error uploading MD5 checksum to S3: {str(e)}")
        raise
