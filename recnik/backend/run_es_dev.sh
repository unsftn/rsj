#!/bin/bash
docker run -p 9201:9200 -p 9301:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" -e ES_JAVA_OPTS="-Xms4g -Xmx4g" --name elastic-recnik --detach docker.elastic.co/elasticsearch/elasticsearch:7.16.1
