#!/bin/sh
export DJANGO_SETTINGS=prod
touch /app/log/recnik.log
cd /app

if [ "$#" -ne 0 ]; then
  echo "python3 manage.py" "$@"
  python3 manage.py "$@"
else
  python3 manage.py migrate
  # python3 manage.py loaddata start_groups start_users kvalifikatori vrste_publikacija operacije-izmene renderi status_odrednice
  python3 manage.py copycoders
  # uwsgi --ini /app/config/uwsgi-prod.ini
  gunicorn -b 0.0.0.0:8000 -w 4 --access-logfile /app/log/gunicorn.log recnik.wsgi:application
fi
