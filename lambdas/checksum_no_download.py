import boto3
import logging

import botocore

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize S3 client
s3_client = boto3.client('s3')

###retrieving the ETag from the file metadata, which acts as the MD5 checksum.
def lambda_handler(event, context):
    try:
        # Extract bucket name and object key from the event triggered by S3
        bucket_name = event['Records'][0]['s3']['bucket']['name']
        object_key = event['Records'][0]['s3']['object']['key']

        logger.info(f"Processing file: {object_key} in bucket: {bucket_name}")

        # Get the object's metadata from S3
        response = s3_client.head_object(Bucket=bucket_name, Key=object_key)

        # Extract the ETag (this is the MD5 checksum for non-multipart uploads)
        etag = response['ETag'].strip('"')  # ETag is enclosed in quotes, so remove them
        logger.info(f"ETag (MD5 checksum) for {object_key}: {etag}")

        # Create the MD5 file with the same prefix but with .md5 extension
        checksum_key = f'{object_key}.md5'
        upload_checksum(bucket_name, checksum_key, etag)

        return {
            'statusCode': 200,
            'body': f'MD5 checksum {etag} stored as {checksum_key}'
        }
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        return {
            'statusCode': 500,
            'body': f'Error processing file: {str(e)}'
        }


def upload_checksum(bucket, key, checksum):
    """Upload the MD5 checksum to S3."""
    try:
        s3_client.put_object(Bucket=bucket, Key=key, Body=checksum)
        logger.info(f"MD5 checksum uploaded successfully: {key}")
    except botocore.exceptions.ClientError as e:
        logger.error(f"Error uploading MD5 checksum to S3: {str(e)}")
        raise
