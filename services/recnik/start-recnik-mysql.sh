#!/bin/bash

mkdir -p /var/services/recnik/data
mkdir -p /var/services/recnik/init

docker run \
  --name recnik-mysql \
  --restart always \
  -v /var/services/recnik/data:/var/lib/mysql \
  -v /var/services/recnik/init:/docker-entrypoint-initdb.d \
  -e MYSQL_ROOT_PASSWORD=recnik \
  -e MYSQL_PASSWORD=recnik \
  -e MYSQL_USER=recnik \
  -e MYSQL_DATABASE=recnik \
  -d mariadb:latest
