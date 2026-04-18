import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('users')

def lambda_handler(event, context):

    method = event.get('httpMethod')

    body = {}
    if event.get("body"):
        body = json.loads(event["body"])

    query = event.get("queryStringParameters") or {}

    # ---------- POST ----------
    if method == 'POST':

        table.put_item(Item=body)

        return {
            'statusCode': 200,
            'body': json.dumps('User created')
        }

    # ---------- GET ----------
    elif method == 'GET':

        user_id = query.get("id")

        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps("Missing id in query string")
            }

        response = table.get_item(Key={'id': user_id})

        return {
            'statusCode': 200,
            'body': json.dumps(response.get("Item", {}))
        }

    # ---------- PUT ----------
    elif method == 'PUT':

        user_id = body.get("id")

        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps("Missing id in body")
            }

        table.update_item(
            Key={'id': user_id},
            UpdateExpression="set info=:i",
            ExpressionAttributeValues={
                ':i': body.get("info")
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('User updated')
        }

    # ---------- DELETE ----------
    elif method == 'DELETE':

        user_id = query.get("id")

        if not user_id:
            return {
                'statusCode': 400,
                'body': json.dumps("Missing id in query string")
            }

        table.delete_item(Key={'id': user_id})

        return {
            'statusCode': 200,
            'body': json.dumps('User deleted')
        }

    # ---------- DEFAULT ----------
    else:
        return {
            'statusCode': 400,
            'body': json.dumps('Unsupported method')
        }
