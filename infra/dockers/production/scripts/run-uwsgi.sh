#!/bin/bash

set -o errexit
set -o nounset

echo "Collecting static files"
date
python manage.py collectstatic --noinput

echo "Starting nginx"
date
service nginx restart

echo "Starting server"
date
uwsgi /scripts/uwsgi.ini
