#!/bin/sh
export DJANGO_SETTINGS=prod
touch /app/log/korpus.log
touch /app/log/uwsgi.log
cd /app

if [ "$#" -ne 0 ]; then
  echo "python3 manage.py" "$@"
  python3 manage.py "$@"
else
  python3 manage.py migrate
  uwsgi --ini /app/config/uwsgi-prod.ini
fi
