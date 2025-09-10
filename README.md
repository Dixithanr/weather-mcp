# Weather API - Azure Functions

A simple Azure Functions API that receives a city name and returns sample weather data.

## Features

- Accepts city name via query parameter or request body
- Returns comprehensive sample weather data including:
  - Current weather conditions
  - 5-day forecast
  - Temperature, humidity, wind speed, pressure, and visibility
- Supports both GET and POST requests
- Proper error handling and validation

## Project Structure

```
weather/
├── host.json                 # Azure Functions host configuration
├── local.settings.json       # Local development settings
├── requirements.txt          # Python dependencies
├── weather_api/             # Function directory
│   ├── __init__.py          # Main function code
│   └── function.json        # Function configuration
└── README.md                # This file
```

## Local Development

### Prerequisites

- Python 3.8 or higher
- Azure Functions Core Tools v4
- Azure CLI (for deployment)

### Setup

1. Install Azure Functions Core Tools:
   ```bash
   npm install -g azure-functions-core-tools@4 --unsafe-perm true
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the local development server:
   ```bash
   func start
   ```

The API will be available at: `http://localhost:7071/api/weather_api`

## API Usage

### GET Request
```
GET /api/weather_api?city=London
```

### POST Request
```json
POST /api/weather_api
Content-Type: application/json

{
    "city": "New York"
}
```

### Sample Response
```json
{
  "city": "London",
  "country": "Sample Country",
  "current_weather": {
    "temperature": 22,
    "feels_like": 24,
    "condition": "Partly Cloudy",
    "humidity": "65%",
    "wind_speed": "12 km/h",
    "pressure": "1015 hPa",
    "visibility": "10 km",
    "last_updated": "2024-01-15 14:30:00"
  },
  "forecast": [
    {
      "date": "2024-01-15",
      "day": "Monday",
      "high_temp": 25,
      "low_temp": 18,
      "condition": "Sunny",
      "precipitation_chance": 10
    },
    {
      "date": "2024-01-16",
      "day": "Tuesday",
      "high_temp": 23,
      "low_temp": 16,
      "condition": "Cloudy",
      "precipitation_chance": 40
    }
  ],
  "data_source": "Sample Weather API",
  "note": "This is sample weather data for demonstration purposes"
}
```

## Deployment to Azure

### Method 1: Using Azure CLI

1. Create a resource group:
   ```bash
   az group create --name weather-api-rg --location "East US"
   ```

2. Create a storage account:
   ```bash
   az storage account create --name weatherstorageaccount --location "East US" --resource-group weather-api-rg --sku Standard_LRS
   ```

3. Create the function app:
   ```bash
   az functionapp create --resource-group weather-api-rg --consumption-plan-location "East US" --runtime python --runtime-version 3.9 --functions-version 4 --name weather-api-function --storage-account weatherstorageaccount
   ```

4. Deploy the function:
   ```bash
   func azure functionapp publish weather-api-function
   ```

### Method 2: Using Visual Studio Code

1. Install the Azure Functions extension
2. Sign in to Azure
3. Right-click on the function app folder
4. Select "Deploy to Function App"
5. Choose your subscription and function app

### Method 3: Using Azure Portal

1. Go to the Azure Portal
2. Create a new Function App
3. Choose Python 3.9 runtime
4. Use the deployment center to connect to your repository
5. Deploy from your Git repository

## Configuration

### Environment Variables

The function uses the following configuration (set in `local.settings.json` for local development):

- `AzureWebJobsStorage`: Storage account connection string
- `FUNCTIONS_WORKER_RUNTIME`: Set to "python"
- `AzureWebJobsFeatureFlags`: Set to "EnableWorkerIndexing"

### Authentication

The function is configured with `authLevel: "anonymous"`, which means the API can be called without any authentication keys:

```
https://your-function-app.azurewebsites.net/api/weather_api?city=London
```

If you need to add authentication later, you can change the `authLevel` in `function.json` to `"function"` or `"admin"`.

## Testing

### Using curl

```bash
# GET request
curl "https://your-function-app.azurewebsites.net/api/weather_api?city=Paris"

# POST request
curl -X POST "https://your-function-app.azurewebsites.net/api/weather_api" \
  -H "Content-Type: application/json" \
  -d '{"city": "Tokyo"}'
```

### Using Postman

1. Set method to GET or POST
2. Set URL to your function endpoint
3. Add city parameter in query string (GET) or request body (POST)
4. No authentication required

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: When city name is not provided
- **500 Internal Server Error**: For unexpected errors

## Customization

### Adding Real Weather Data

To integrate with a real weather service (like OpenWeatherMap), modify the `generate_sample_weather` function:

```python
import requests

def get_real_weather(city_name: str, api_key: str) -> dict:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}&units=metric"
    response = requests.get(url)
    return response.json()
```

### Adding More Cities

You can enhance the sample data by adding city-specific information or integrating with a geocoding service.

## Monitoring

Azure Functions provides built-in monitoring through:

- Application Insights (automatically configured)
- Azure Monitor
- Function execution logs

## Cost Considerations

This function uses the Consumption plan, which means you only pay for execution time. The function is designed to be lightweight and cost-effective.

## Security Notes

- The API is currently configured for anonymous access
- Consider implementing additional security measures for production use:
  - Change `authLevel` to `"function"` or `"admin"` for authentication
  - Implement API rate limiting
  - Add input validation and sanitization
  - Consider using Azure API Management for advanced security features
