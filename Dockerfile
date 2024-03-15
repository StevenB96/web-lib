FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get install -y gcc && \
    apt-get install -y libmariadb-dev-compat libmariadb-dev && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
# Set MySQLCLIENT_CFLAGS and MYSQLCLIENT_LDFLAGS
ENV MYSQLCLIENT_CFLAGS="-I/usr/include/mysql" MYSQLCLIENT_LDFLAGS="-L/usr/lib/x86_64-linux-gnu -lmysqlclient"
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy NGINX configuration
COPY nginx.conf /etc/nginx/sites-available/default

# Copy application code
COPY . /app/

# Expose ports
EXPOSE 8001

# Run migrations and seeding
RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py seed_permissions && \
    python manage.py seed_users && \
    python manage.py seed_books && \
    python manage.py collectstatic --noinput & \    
    python manage.py test && \
    chmod +x ./shell_scripts/entrypoint_docker.sh && \
    chmod +x ./shell_scripts/entrypoint_docker.sh

# Run application
CMD ["./shell_scripts/entrypoint_docker.sh"]
