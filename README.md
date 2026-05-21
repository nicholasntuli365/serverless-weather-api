# Serverless Weather API

A serverless REST API built on AWS that fetches live weather data and logs it to a database. Built using AWS Lambda, API Gateway, and DynamoDB.

---

## Architecture

- **AWS Lambda** — serverless functions that handle business logic
- **API Gateway** — exposes Lambda functions as public HTTP endpoints
- **DynamoDB** — NoSQL database that stores weather lookup history
- **OpenWeatherMap API** — provides live weather data

---

## Endpoints

### Get Live Weather
GET /weather?city={cityname}

Fetches current weather for a city and logs it to DynamoDB.

Example response:
{
  "city": "Ladysmith",
  "country": "ZA",
  "temperature": 18.5,
  "feels_like": 17.2,
  "humidity": 74,
  "condition": "few clouds",
  "timestamp": "2026-05-21T11:06:24Z"
}

### Get Weather Logs
GET /logs
GET /logs?city={cityname}

Returns all previously logged weather lookups, optionally filtered by city.

---

## Live API

Base URL: https://lk5tzd9nbl.execute-api.af-south-1.amazonaws.com

Test it:
- https://lk5tzd9nbl.execute-api.af-south-1.amazonaws.com/weather?city=Durban
- https://lk5tzd9nbl.execute-api.af-south-1.amazonaws.com/logs

---

## Setup

### Prerequisites
- AWS Account (free tier)
- OpenWeatherMap API key (free tier)

### Deployment Steps

1. **DynamoDB** — Create a table named `WeatherLogs` with partition key `city` (String) and sort key `timestamp` (String)
2. **IAM** — Create a Lambda execution role with `AmazonDynamoDBFullAccess` and `AWSLambdaBasicExecutionRole`
3. **Lambda** — Create two functions (`fetchWeather`, `getWeatherLogs`) using Python 3.12, attach the IAM role, and deploy the code from the `/functions` folder
4. **API Gateway** — Create an HTTP API, add `GET /weather` route pointing to `fetchWeather` and `GET /logs` route pointing to `getWeatherLogs`

---

## Tech Stack

- Python 3.12
- AWS Lambda
- AWS API Gateway (HTTP API)
- AWS DynamoDB
- OpenWeatherMap API
  
## Author
Nicholas Ntuli
