import json
import boto3
import os


sqs_client = boto3.client('sqs')

def lambda_handler(event, context):
    try:
        for record in event['Records']:
            message_body = json.loads(record['body'])
            if message_body['status'] == 'processed':
                print(f"Telemetry data with ID {message_body['id']} processed successfully.")
            else:
                print(f"Failed to process telemetry data with ID {message_body['id']}. Error: {message_body['error']}")

    except Exception as e:
        print(f"Error handling acknowledgment: {e}")

    return {'statusCode': 200}
