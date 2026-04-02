#!/bin/sh
if [ $# -eq 0 ]; then
  exec search-api
else
  exec search-cli "$@"
fi
