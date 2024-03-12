FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy application code
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Run migrations and seeding
RUN python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py seed_permissions && \
    python manage.py seed_users && \
    python manage.py seed_books && \
    python manage.py test && \
    python manage.py collectstatic --noinput

# Run the Django application with Gunicorn
CMD gunicorn livi_assessment.wsgi:application --bind 0.0.0.0:8000
