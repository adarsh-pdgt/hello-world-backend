#!/bin/bash

set -o errexit
set -o nounset

echo "Checking nginx conf"
nginx -t

echo "Starting nginx"
service nginx restart
