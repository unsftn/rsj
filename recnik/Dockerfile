FROM python:3.11-slim-bookworm
LABEL maintainer="Branko Milosavljevic <mbranko@uns.ac.rs>"
RUN apt-get -y update
RUN apt-get -y install pkg-config gcc default-libmysqlclient-dev graphviz-dev libffi-dev libmagic1 libtiff-dev libopenjp2-7-dev liblcms-dev zlib1g-dev libjpeg-dev musl-dev wget gdebi
RUN wget https://www.princexml.com/download/prince_16-1_debian12_amd64.deb
RUN gdebi -n prince_16-1_debian12_amd64.deb
RUN /usr/local/bin/python3 -m pip install --upgrade pip
RUN pip3 install -U setuptools
COPY backend/requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY backend /app
RUN mkdir -p /app/staticfiles
WORKDIR /app
RUN mkdir /private
RUN touch /private/secrets
RUN rm -rf /app/log
RUN mkdir /app/log
ARG django_settings=prod
ENV DJANGO_SETTINGS=$django_settings
RUN python3 /app/manage.py collectstatic --noinput
RUN rm -rf /app/log/*
RUN rm -rf /private
RUN chmod +x /app/run_prod.sh
EXPOSE 8000
ENTRYPOINT ["/app/run_prod.sh"]
