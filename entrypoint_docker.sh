#!/bin/bash

python manage.py test
service nginx start
gunicorn livi_assessment.wsgi:application --bind 0.0.0.0:8002
