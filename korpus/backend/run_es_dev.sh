#!/bin/bash
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" --name elastic-korpus --detach docker.elastic.co/elasticsearch/elasticsearch:7.11.1
