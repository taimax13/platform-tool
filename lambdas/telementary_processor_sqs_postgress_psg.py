import os
import boto3
import json
import psycopg2


def lambda_handler(event, context):
    # Get environment variables
    db_host = os.environ['DB_HOST']
    db_name = os.environ['DB_NAME']
    db_user = os.environ['DB_USER']
    db_password = os.environ['DB_PASSWORD']
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )
    cursor = conn.cursor()

    sqs_client = boto3.client('sqs')

    try:
        for record in event['Records']:
            telemetry_data = json.loads(record['body'])
            insert_query = """
            INSERT INTO telemetry (id, data, received_at)
            VALUES (%s, %s, NOW())
            """
            cursor.execute(insert_query, (telemetry_data['id'], json.dumps(telemetry_data)))
            conn.commit()
            sqs_client.send_message(
                QueueUrl=os.environ['OUTPUT_QUEUE_URL'],
                MessageBody=json.dumps({'status': 'processed', 'id': telemetry_data['id']})
            )

    except Exception as e:
        conn.rollback()
        print(f"Error processing record: {e}")
        sqs_client.send_message(
            QueueUrl=os.environ['OUTPUT_QUEUE_URL'],
            MessageBody=json.dumps({'status': 'failed', 'id': telemetry_data['id'], 'error': str(e)})
        )

    finally:
        cursor.close()
        conn.close()

    return {'statusCode': 200}
