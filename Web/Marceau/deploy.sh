#!/bin/bash

docker build -t marceau .
docker rm -f marceau >/dev/null 2>&1 || true
docker run --name marceau -itd --restart=unless-stopped -v /etc/localtime:/etc/localtime:ro -p 127.0.0.1:50004:80 marceau
