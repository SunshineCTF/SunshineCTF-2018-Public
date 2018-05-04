#!/bin/bash

docker build -t home-sweet-home .
docker rm -f home-sweet-home >/dev/null 2>&1 || true
docker run --name home-sweet-home -itd --restart=unless-stopped -v /etc/localtime:/etc/localtime:ro -p 50005:80 home-sweet-home
