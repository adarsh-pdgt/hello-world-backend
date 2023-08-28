#!/bin/bash

set -o errexit
set -o nounset

echo "Collecting static files"
date
python manage.py collectstatic --noinput

echo "Starting nginx"
date
service nginx restart

echo "Starting Asgi server"
date
daphne --verbosity 2 -u /tmp/hello_world-daphne.sock asgi:application
