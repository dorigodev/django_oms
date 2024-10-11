#!/bin/sh
echo '🟡 Performing Collect Static '

python manage.py collectstatic --noinput

echo "✅ Collect Static realized!"