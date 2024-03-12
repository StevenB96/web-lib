# Livi assessment setup README

## Note: As of 9am on 12/03/2024 I have not developed / tested the Dockerfile. This is in part due to me working on a windows laptop which does not support virtualistation.

## Initiate a Virtual Environment

### Create a virtual environment using the following command:

- python -m venv ./venv

### Activate the virtual environment:

- venv\Scripts\Activate.ps1

## Setup Django Project

### Install requirements

- pip install -r requirements.txt

### Apply migrations

- python manage.py makemigrations
- python manage.py migrate

### Seed permissions, users, and books

- python manage.py seed_permissions
- python manage.py seed_users
- python manage.py seed_books

## Run Server

### Run tests:

- python manage.py test

### Start the Django development server:

- python manage.py runserver

## Login using default user

- Username: admin_user
- Email address: admin_user@example.com
- Password: adminpass
