import json
import boto3
import uuid




def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ItemsTable')
    http_method = event['httpMethod']

    if http_method == 'POST':
        return create_item(event, table)
    elif http_method == 'GET':
        return get_item(event)
    elif http_method == 'DELETE':
        return delete_item(event)
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'Message': 'Method not allowed'})
        }


def create_item(event, table):
    item_id = str(uuid.uuid4())
    item_name = json.loads(event['body'])['itemName']
    table.put_item(Item={'ItemId': item_id, 'ItemName': item_name})

    return {
        'statusCode': 200,
        'body': json.dumps({
            'ItemId': item_id,
            'Message': 'Item created successfully'
        })
    }


def get_item(event, table):
    item_id = event['pathParameters']['id']
    response = table.get_item(Key={'ItemId': item_id})

    item = response.get('Item')

    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'Message': 'Item not found'})
        }

    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }


def delete_item(event, table):
    item_id = event['pathParameters']['id']
    table.delete_item(Key={'ItemId': item_id})

    return {
        'statusCode': 200,
        'body': json.dumps({'Message': 'Item deleted successfully'})
    }
