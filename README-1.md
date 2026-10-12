# Serverless Weather API

A serverless REST API built on AWS that fetches live weather data and logs it to a database. Built using AWS Lambda, API Gateway, and DynamoDB.

> **Status:** the original live deployment was taken down when my AWS free trial ended. The deployment steps below recreate it from this code.

---

## Architecture

- **AWS Lambda**: serverless functions that handle business logic
- **API Gateway**: exposes Lambda functions as public HTTP endpoints
- **DynamoDB**: NoSQL database that stores weather lookup history
- **OpenWeatherMap API**: provides live weather data

How a request moves through it:

- `GET /weather?city=Durban` goes to API Gateway, then the `fetchWeather` Lambda, which gets live weather from OpenWeatherMap and saves the lookup in DynamoDB.
- `GET /logs` goes to API Gateway, then the `getWeatherLogs` Lambda, which reads past lookups from DynamoDB.

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

## Setup

### Prerequisites
- AWS Account
- OpenWeatherMap API key (free tier)

### Deployment Steps

1. **DynamoDB**: Create a table named `WeatherLogs` with partition key `city` (String) and sort key `timestamp` (String)
2. **IAM**: Create a Lambda execution role with `AmazonDynamoDBFullAccess` and `AWSLambdaBasicExecutionRole`
3. **Lambda**: Create two functions (`fetchWeather`, `getWeatherLogs`) using Python 3.12, attach the IAM role, and deploy the code from the `/functions` folder
4. **API key**: In the `fetchWeather` function, go to Configuration, then Environment variables, and add `OPENWEATHER_API_KEY` with your OpenWeatherMap key. The key is never stored in this repo
5. **API Gateway**: Create an HTTP API, add a `GET /weather` route pointing to `fetchWeather` and a `GET /logs` route pointing to `getWeatherLogs`
6. **Test**: Open `<your-api-url>/weather?city=Durban` in a browser, then `<your-api-url>/logs`

---

## Tech Stack

- Python 3.12
- AWS Lambda
- AWS API Gateway (HTTP API)
- AWS DynamoDB
- OpenWeatherMap API

## Author
Nicholas Ntuli
