import json
import boto3
import urllib.request
from datetime import datetime, timezone

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('WeatherLogs')

API_KEY = 'YOUR_API_KEY_HERE'

def lambda_handler(event, context):
    params = event.get('queryStringParameters') or {}
    city = params.get('city')

    if not city:
        return {
            'statusCode': 400,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': 'City parameter is required'})
        }

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())

        weather = {
            'city': data['name'],
            'country': data['sys']['country'],
            'temperature': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'humidity': data['main']['humidity'],
            'condition': data['weather'][0]['description'],
            'timestamp': datetime.now(timezone.utc).isoformat()
        }

        table.put_item(Item={
            'city': weather['city'].lower(),
            'timestamp': weather['timestamp'],
            'country': weather['country'],
            'temperature': str(weather['temperature']),
            'feels_like': str(weather['feels_like']),
            'humidity': str(weather['humidity']),
            'condition': weather['condition']
        })

        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(weather)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'error': str(e)})
        }
