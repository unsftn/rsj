#!/bin/bash

docker run \
  --name cmd-reindex \
  --rm \
  --network recnik \
  -v ./search_index:/app/search_index \
  rsj/search-engine \
  import-all --recnik-host recnik-mysql --korpus-host korpus-mysql --force --output-dir /app/search_index
