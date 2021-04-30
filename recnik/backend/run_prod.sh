#!/bin/sh
export DJANGO_SETTINGS=prod
touch /app/log/recnik.log
touch /app/log/uwsgi.log
cd /app

if [ "$#" -ne 0 ]; then
  echo "python3 manage.py" "$@"
  python3 manage.py "$@"
else
  python3 manage.py migrate
  python3 manage.py loaddata start_groups start_users kvalifikatori vrste_publikacija operacije-izmene renderi
  uwsgi --ini /app/config/uwsgi-prod.ini
fi
