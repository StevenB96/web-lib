#!/bin/bash

# Timeout for waiting for MySQL service (in seconds)
TIMEOUT=300
START_TIME=$(date +%s)

# Function to calculate elapsed time
function elapsed_time {
    local now=$(date +%s)
    echo $(($now - $START_TIME))
}

# Function to log errors
function log_error {
    local message="$1"
    echo "[ERROR] $message"
}

echo "Starting database initialization..."

# Check if the database engine is not SQLite
if [ $DB_ENGINE != "sqlite" ]; then
    until nc -z $DB_HOST $DB_PORT; do
        if (( $(elapsed_time) >= TIMEOUT )); then
            log_error "Timeout reached while waiting for database service."
            exit 1
        fi
        echo "Database service is not available yet. Retrying in 5 seconds..."
        sleep 5
    done
    echo "MySQL service is available. Starting database initialization..."
fi

# Run 'makemigrations'
echo "Running 'makemigrations'..."
if ! python manage.py makemigrations; then
    log_error "Failed to run 'makemigrations'."
    exit 1
fi

# Run 'migrate'
echo "Running 'migrate'..."
if ! python manage.py migrate; then
    log_error "Failed to run 'migrate'."
    exit 1
fi

# Run 'seed_permissions'
echo "Running 'seed_permissions'..."
if ! python manage.py seed_permissions; then
    log_error "Failed to run 'seed_permissions'."
    exit 1
fi

# Run 'seed_users'
echo "Running 'seed_users'..."
if ! python manage.py seed_users; then
    log_error "Failed to run 'seed_users'."
    exit 1
fi

# Run 'seed_books'
echo "Running 'seed_books'..."
if ! python manage.py seed_books; then
    log_error "Failed to run 'seed_books'."
    exit 1
fi

# Run 'collectstatic'
echo "Running 'collectstatic'..."
if ! python manage.py collectstatic --noinput; then
    log_error "Failed to run 'collectstatic'."
    exit 1
fi

echo "Database initialization completed successfully."
