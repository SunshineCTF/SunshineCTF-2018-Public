#!/bin/bash

docker build -t workshop-helper .
docker rm -f workshop-helper >/dev/null 2>&1 || true
docker run --name workshop-helper -itd --restart=unless-stopped -v /etc/localtime:/etc/localtime:ro --read-only -p 127.0.0.1:50001:50001 workshop-helper
