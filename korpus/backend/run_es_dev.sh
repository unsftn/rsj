#!/bin/bash
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" --name elastic-korpus --detach elasticsearch:8.4.1
