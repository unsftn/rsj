#!/bin/sh
export DJANGO_SETTINGS=prod
touch /app/log/recnik.log
touch /app/log/uwsgi.log
cd /app
python3 manage.py migrate
# echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@rsj.rs', 'changeme')" | python3 manage.py shell > /dev/null 2>&1
python3 manage.py loaddata start_groups start_users
uwsgi --ini /app/config/uwsgi-prod.ini
