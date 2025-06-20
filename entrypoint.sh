#!/bin/sh
# Wait for Postgres to be ready
/wait-for-postgres.sh postgresdb

# Perform database migration
python manage.py makemigrations
python manage.py migrate

# Start Django application 
python manage.py runserver 0.0.0.0:8000