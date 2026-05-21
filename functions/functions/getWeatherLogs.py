import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WeatherLogs')

def lambda_handler(event, context):
    params = event.get('queryStringParameters') or {}
    city = params.get('city')

    try:
        if city:
            response = table.query(
                KeyConditionExpression=Key('city').eq(city.lower())
            )
        else:
            response = table.scan()

        items = response.get('Items', [])
        items.sort(key=lambda x: x['timestamp'], reverse=True)

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(items)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
