#!/bin/bash

docker run -v $PWD/cayley.yml:/etc/cayley.yml \
           -v $PWD/data:/data \
           -p 64210:64210 \
           -d \
           --name pug-db \
           quay.io/cayleygraph/cayley \
           -c /etc/cayley.yml --init
