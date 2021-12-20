#!/bin/bash
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --name elastic-recnik --detach docker.elastic.co/elasticsearch/elasticsearch:7.16.1
