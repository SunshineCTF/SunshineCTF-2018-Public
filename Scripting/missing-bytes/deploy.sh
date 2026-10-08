#!/bin/bash

docker build -t missing-bytes .
docker rm -f missing-bytes >/dev/null 2>&1 || true
docker run --name missing-bytes -itd --restart=unless-stopped -v /etc/localtime:/etc/localtime:ro --read-only -p 30001:30001 missing-bytes
