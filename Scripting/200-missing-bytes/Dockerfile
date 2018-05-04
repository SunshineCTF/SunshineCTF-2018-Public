FROM ubuntu:14.04

# Install server software
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y && \
    apt-get install -y --force-yes \
        python \
        socat

# Set a working direrctory
WORKDIR /app

COPY run.sh ./
COPY flag.txt ./
COPY server.py ./

# Expose the required port
EXPOSE 30001

# Start the application
CMD [ "bash", "run.sh"]