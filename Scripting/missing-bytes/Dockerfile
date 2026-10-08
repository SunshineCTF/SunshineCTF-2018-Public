# python2 service; python:2.7 provides python2 + a working apt for socat.
FROM python:2.7

RUN printf 'deb http://archive.debian.org/debian buster main\ndeb http://archive.debian.org/debian-security buster/updates main\n' > /etc/apt/sources.list && \
	apt-get -o Acquire::Check-Valid-Until=false update && \
	apt-get install -y socat && \
	rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY run.sh flag.txt server.py ./
RUN chmod +x server.py run.sh

EXPOSE 30001
CMD ["bash", "run.sh"]
