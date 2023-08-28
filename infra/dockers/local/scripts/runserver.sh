#!/bin/bash

set -o errexit
set -o nounset

echo "Starting server"
python manage.py migrate --settings settings.development
python manage.py runserver 0.0.0.0:8000 --settings settings.development
