#!/usr/bin/env python3
"""
MCP Time Service
A simple service that provides current time information in various formats
and exposes metrics for monitoring.
"""

import os
import time
import datetime
import json
import socket
from flask import Flask, jsonify, request, Response
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST

# Initialize Flask app
app = Flask(__name__)

# Initialize Prometheus metrics
REQUEST_COUNT = Counter('time_service_requests_total', 'Total request count', ['endpoint', 'method'])
TIME_REQUESTS = Counter('time_service_time_requests_total', 'Time endpoint request count')
UPTIME_GAUGE = Gauge('time_service_uptime_seconds', 'Service uptime in seconds')

# Store start time for uptime calculation
START_TIME = time.time()

@app.route('/health')
def health():
    """Health check endpoint"""
    REQUEST_COUNT.labels(endpoint='/health', method='GET').inc()
    return jsonify({"status": "healthy"})

@app.route('/time')
def get_time():
    """Return current time in various formats"""
    REQUEST_COUNT.labels(endpoint='/time', method='GET').inc()
    TIME_REQUESTS.inc()

    # Get timezone from request parameter or use UTC as default
    timezone = request.args.get('tz', 'UTC')
    try:
        os.environ['TZ'] = timezone
        time.tzset()
    except (AttributeError, ValueError):
        # tzset not available on all platforms or invalid timezone
        pass

    now = datetime.datetime.now()
    utc_now = datetime.datetime.utcnow()

    response = {
        "unix_timestamp": int(time.time()),
        "iso_8601": now.isoformat(),
        "utc": utc_now.isoformat(),
        "local_time": now.strftime("%Y-%m-%d %H:%M:%S %Z"),
        "timezone": timezone,
        "hostname": socket.gethostname(),
        "service_name": "mcp-time"
    }

    # Check if client wants pretty-printed JSON
    pretty = request.args.get('pretty', 'false').lower() == 'true'
    if pretty:
        return jsonify(response)
    else:
        return Response(json.dumps(response), mimetype='application/json')

@app.route('/metrics')
def metrics():
    """Expose Prometheus metrics"""
    REQUEST_COUNT.labels(endpoint='/metrics', method='GET').inc()

    # Update uptime metric
    UPTIME_GAUGE.set(time.time() - START_TIME)

    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

@app.route('/')
def index():
    """Root endpoint with basic information"""
    REQUEST_COUNT.labels(endpoint='/', method='GET').inc()
    return jsonify({
        "service": "mcp-time",
        "version": "1.0.0",
        "description": "Time service for MCP stack",
        "endpoints": [
            {"path": "/time", "description": "Get current time information"},
            {"path": "/metrics", "description": "Prometheus metrics"},
            {"path": "/health", "description": "Health check"}
        ]
    })

if __name__ == '__main__':
    # Use PORT environment variable if defined, otherwise default to 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
