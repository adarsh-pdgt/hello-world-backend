#!/bin/bash

set -o errexit
set -o nounset

echo "Migrating database"
python manage.py migrate
