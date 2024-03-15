#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py seed_permissions
python manage.py seed_users
python manage.py seed_books
python manage.py collectstatic --noinput
python manage.py test
chmod +x entrypoint.sh