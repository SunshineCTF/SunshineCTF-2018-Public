#!/bin/bash

docker build -t evaluation .
docker rm -f evaluation >/dev/null 2>&1 || true
docker run --name evaluation -itd --restart=unless-stopped -v /etc/localtime:/etc/localtime:ro --read-only -v /var/run -p 127.0.0.1:50002:80 evaluation
