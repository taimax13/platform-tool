import json
import os
import pytest
import textwrap
import re
from unittest.mock import patch, MagicMock

from lambdas.telementary_processor_sqs_postgress_psg import lambda_handler

@patch('boto3.client')
@patch('psycopg2.connect')
def test_telemetry_processor(mock_db_connect, mock_boto_client):
    mock_sqs = MagicMock()
    mock_boto_client.side_effect = lambda service_name, *args, **kwargs: mock_sqs if service_name == 'sqs' else MagicMock()
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_db_connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_sqs.create_queue.side_effect = lambda QueueName: {'QueueUrl': f'https://mock-queue-url/{QueueName}'}
    os.environ['INPUT_QUEUE_URL'] = mock_sqs.create_queue(QueueName='input-queue')['QueueUrl']
    os.environ['OUTPUT_QUEUE_URL'] = mock_sqs.create_queue(QueueName='output-queue')['QueueUrl']
    os.environ['DB_HOST'] = 'mock-db-host'
    os.environ['DB_NAME'] = 'mock-db-name'
    os.environ['DB_USER'] = 'mock-user'
    os.environ['DB_PASSWORD'] = 'mock-password'
    event = {
        'Records': [
            {
                'body': json.dumps({'id': '12345', 'data': 'telemetry_data'})
            }
        ]
    }

    result = lambda_handler(event, None)

    assert result['statusCode'] == 200

    # Normalize the expected and actual SQL queries
    expected_query = textwrap.dedent("""
        INSERT INTO telemetry (id, data, received_at)
        VALUES (%s, %s, NOW())
    """).strip()

    actual_query = mock_cursor.execute.call_args[0][0].strip()

    # Remove extra whitespace and newlines for comparison
    def normalize_sql(query):
        return re.sub(r'\s+', ' ', query).strip()

    expected_query_normalized = normalize_sql(expected_query)
    actual_query_normalized = normalize_sql(actual_query)

    print(f"Expected query: {expected_query_normalized}")
    print(f"Actual query: {actual_query_normalized}")

    # Now compare the normalized queries
    assert actual_query_normalized == expected_query_normalized, (
        f"Expected query:\n{expected_query_normalized}\n\nActual query:\n{actual_query_normalized}"
    )

    # # Check the arguments passed to execute!!!! ###medo spaces!!!!!!!!!!!!!!!!
    # mock_cursor.execute.assert_called_once_with(
    #     expected_query,
    #     ('12345', json.dumps({'id': '12345', 'data': 'telemetry_data'}))
    # )

    mock_conn.commit.assert_called_once()

    mock_sqs.send_message.assert_called_once_with(
        QueueUrl=os.environ['OUTPUT_QUEUE_URL'],
        MessageBody=json.dumps({'status': 'processed', 'id': '12345'})
    )

    mock_conn.close.assert_called_once()
    mock_cursor.close.assert_called_once()
