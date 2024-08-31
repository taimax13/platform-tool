import psycopg2
import os, json


def lambda_handler(event, context):
    claims = event['requestContext']['authorizer']['claims']
    tenant_id = claims['custom:tenant_id']
    #tenant_id = event['headers']['tenant-id']  # Assume tenant ID is passed in headers

    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        database=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD']
    )

    conn.cursor().execute(f"SET app.current_tenant = '{tenant_id}';")

    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM tenants;")
        result = cursor.fetchall()

    return {
        'statusCode': 200,
        'body': json.dumps(result)
    }
