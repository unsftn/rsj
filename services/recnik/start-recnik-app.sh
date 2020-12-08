#!/bin/bash

# za produkciju u private dir treba staviti fajl secrets koji sadrzi red
# SECRET_KEY=......
mkdir -p /var/services/recnik/private
mkdir -p /var/services/recnik/log

docker run \
  --name recnik \
  --detach \
  --link recnik-mysql \
  -v /var/services/recnik/private:/private \
  -v /var/services/recnik/log:/app/log \
  -p 8000:8000 \
  --label "traefik.http.routers.recnik.rule=Host(\`recnik.rsj.rs\`)" \
  --label traefik.http.routers.recnik.entrypoints=web \
  --label traefik.http.routers.recnik.middlewares=redirect-to-https@docker \
  --label "traefik.http.routers.recnik-secured.rule=Host(\`recnik.rsj.rs\`)" \
  --label traefik.http.routers.recnik-secured.entrypoints=websecure \
  --label traefik.http.routers.recnik-secured.tls.certresolver=letsencrypt \
  --label traefik.http.routers.recnik-secured.tls=true \
  rsj/recnik
