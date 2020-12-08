#!/bin/bash

# this directory
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

cd "$DIR/../../recnik" || exit
docker build -t rsj/recnik .
