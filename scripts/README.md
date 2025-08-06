# MCP Time Service

A simple microservice that provides current time information in various formats and exposes metrics for monitoring.

## Features

- Returns current time in multiple formats (UTC, ISO 8601, Unix timestamp)
- Supports timezone parameter customization
- Provides Prometheus-compatible metrics endpoint
- Includes health check endpoint for monitoring
- Containerized for easy deployment

## API Endpoints

### 1. Time Information

```
GET /time
```

Returns current time in various formats.

**Optional Query Parameters:**
- `tz`: Timezone (default: UTC)
- `pretty`: Set to "true" for pretty-printed JSON (default: false)

**Sample Response:**
```json
{
  "unix_timestamp": 1754390178,
  "iso_8601": "2025-08-05T10:36:18.400581",
  "utc": "2025-08-05T10:36:18.400585", 
  "local_time": "2025-08-05 10:36:18",
  "timezone": "UTC",
  "hostname": "29f88f324a2f",
  "service_name": "mcp-time"
}
```

### 2. Health Check

```
GET /health
```

Returns the health status of the service.

**Sample Response:**
```json
{
  "status": "healthy"
}
```

### 3. Metrics

```
GET /metrics
```

Returns Prometheus-compatible metrics.

## Metrics

The following custom metrics are available:

- `time_service_requests_total`: Counter for total requests by endpoint and method
- `time_service_time_requests_total`: Counter specifically for /time endpoint requests
- `time_service_uptime_seconds`: Gauge for service uptime in seconds

## Docker Usage

The service is available as part of the dev-stack Docker Compose setup.

```bash
# Start the service
docker compose up mcp-time -d

# Stop the service
docker compose stop mcp-time

# View logs
docker compose logs mcp-time
```

## Configuration

The service uses environment variables for configuration:

- `PORT`: The port to listen on (default: 8080)
- `TZ`: Default timezone (default: UTC)