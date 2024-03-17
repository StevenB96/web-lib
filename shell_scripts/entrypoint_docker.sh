#!/bin/bash

# Function to log errors
function log_error {
    local message="$1"
    echo "[ERROR] $message"
}

echo "Running Django tests..."
if ! python manage.py test; then
    log_error "Failed to run Django tests."
    exit 1
fi

echo "Starting NGINX service..."
if ! service nginx start; then
    log_error "Failed to start NGINX service."
    exit 1
fi

echo "Starting Gunicorn server..."
if ! gunicorn livi_assessment.wsgi:application --bind 0.0.0.0:8002; then
    log_error "Failed to start Gunicorn server."
    exit 1
fi
