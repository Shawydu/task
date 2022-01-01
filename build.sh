#!/bin/bash

curr_dir=$(pwd)

cd $curr_dir/server
docker build -t server:local .

cd $curr_dir/ui
docker build -t ui:local .

cd $curr_dir
docker-compose up -d
