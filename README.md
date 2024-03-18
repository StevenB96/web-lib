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

### Run tests:

- python manage.py test

### Start the Django development server:

- python manage.py runserver

## Login using default user

- Username: admin_user
- Email address: admin_user@example.com
- Password: adminpass

## Deployment

### Docker

- docker build -t web-lib .
- docker tag web-lib stevenb1996/web-lib:v[y].[z]
- docker push [x]/web-lib:v[y].[z]

### k8s

- minikube start
- kubectl apply -f web-lib.k8s.yaml
- minikube tunnel
- kubectl get pod -n web-lib-project
- kubectl logs [x] -c [y]
- kubectl exec -it [pod]-- bash
- kubectl get service -n web-lib-project
- kubectl get secret -n web-lib-project
- kubectl get all -n web-lib-project
- kubectl delete -f web-lib.k8s.yaml