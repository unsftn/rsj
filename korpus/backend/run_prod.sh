#!/bin/sh
export DJANGO_SETTINGS=prod
touch /app/log/korpus.log
cd /app

if [ "$#" -ne 0 ]; then
  echo "python3 manage.py" "$@"
  python3 manage.py "$@"
else
  python3 manage.py migrate
  exec gunicorn -b 0.0.0.0:8000 -w 4 --access-logfile /app/log/gunicorn.log korpus.wsgi:application
fi
