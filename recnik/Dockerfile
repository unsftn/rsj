FROM node:15.3.0-alpine AS angular
RUN npm update -g
RUN mkdir /app
WORKDIR /app
COPY frontend/package.json frontend/package-lock.json /app/
RUN npm install
COPY frontend /app
RUN npm run build -- --output-path=/app/frontend/dist/

FROM alpine:3.12
MAINTAINER Branko Milosavljevic <mbranko@uns.ac.rs>
RUN set -x \
    && deps=' \
    python3 \
    python3-dev \
    py3-wheel \
    py3-pip \
    uwsgi \
    uwsgi-python3 \
    uwsgi-http \
    uwsgi-router_static \
    uwsgi-logfile \
    mariadb-dev \
    gcc \
    musl-dev \
    jpeg-dev \
    zlib-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tiff-dev \
    libffi-dev \
    graphviz-dev \
    libmagic \
    ' \
        && apk --no-cache add --update $deps

RUN pip3 install --upgrade pip setuptools
COPY backend/requirements.txt /app/requirements.txt
RUN pip3 install -r /app/requirements.txt
COPY backend /app
RUN mkdir -p /app/static
COPY --from=angular /app/frontend/dist /app/static
WORKDIR /app
RUN mkdir /private
RUN echo "SECRET_KEY=XYZ" > /private/secrets
RUN rm -rf /app/log
RUN mkdir /app/log
ARG django_settings=prod
ENV DJANGO_SETTINGS=$django_settings
RUN python3 /app/manage.py collectstatic --noinput
RUN rm -rf /app/log/*
RUN rm /private/secrets
RUN chmod +x /app/run_prod.sh
EXPOSE 8000
CMD ["/app/run_prod.sh"]
