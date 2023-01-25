#!/bin/bash
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e ES_JAVA_OPTS="-Xms4g -Xmx4g" --name elastic-korpus --detach elasticsearch:8.6.0
