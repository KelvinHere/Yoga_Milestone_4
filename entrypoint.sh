#!/bin/sh

# Wait for postgres
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

# Script
echo -n "Start of script to setup django in entrypoint.sh"
python manage.py flush --no-input
python manage.py makemigrations --no-input
python manage.py migrate --no-input
python createsuperuser --no-input --username TEST --email e@e.com --password test999

exec "$@"