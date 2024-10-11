#!/bin/sh
echo '🟡 Performing Migrations'
python manage.py makemigrations --noinput
python manage.py migrate --noinput

echo '✅ Migrate realized!'