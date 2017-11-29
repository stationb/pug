#!/bin/bash

docker run -v $PWD/cayley.yml:/etc/cayley.yml \
           -p 64210:64210 \
           -d \
           --name pug-db \
           quay.io/cayleygraph/cayley \
           -c /etc/cayley.yml --init
