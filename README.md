# Livi assessment setup README

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

### Start the Django development server:

- python manage.py runserver

## Login using default user

- Username: admin_user
- Email address: admin_user@example.com
- Password: adminpass
