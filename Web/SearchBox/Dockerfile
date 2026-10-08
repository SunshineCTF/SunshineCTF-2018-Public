# Pin the jessie-based image: its curl 7.38 ignores the host in file:// URLs,
# which the intended SSRF solve (file://www.google.com/etc/flag.txt?) relies on.
# The stretch image's curl 7.52 rejects file:// with a non-local host.
FROM php:7.0-apache-jessie
COPY index.php /var/www/html
COPY flag.txt /etc
