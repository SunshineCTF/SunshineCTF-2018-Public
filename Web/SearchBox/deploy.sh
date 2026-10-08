#!/bin/bash

docker build -t searchbox .
docker rm -f searchbox >/dev/null 2>&1 || true
docker run --name searchbox -itd --restart=unless-stopped -v /etc/localtime:/etc/localtime:ro -p 127.0.0.1:50003:80 searchbox
