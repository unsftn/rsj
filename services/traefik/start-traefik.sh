#!/bin/bash

mkdir -p /var/services/traefik/log
mkdir -p /var/services/traefik/letsencrypt
mkdir -p /var/services/traefik/conf

docker run \
  --name traefik \
  --label traefik.http.middlewares.redirect-to-https.redirectscheme.scheme=https \
  --volume /var/services/traefik/conf/traefik.toml:/etc/traefik/traefik.toml \
  --volume /var/services/traefik/letsencrypt:/letsencrypt \
  --volume /var/services/traefik/log:/log \
  --volume /var/run/docker.sock:/var/run/docker.sock:ro \
  -p 80:80 \
  -p 443:443 \
  -p 8080:8080 \
  --rm \
  --detach \
  traefik:v2.2
