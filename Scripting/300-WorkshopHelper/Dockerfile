FROM ubuntu:14.04

# Install server software
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get dist-upgrade -y && \
    apt-get install -y --force-yes \
        build-essential \
        libgmp3-dev \
        curl \
        npm

# Make user
RUN useradd --no-log-init -r -m user

# Get nodejs
RUN curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash -

# Install nodejs
RUN apt-get install -y nodejs

# Make app directory
WORKDIR /usr/src/app

# Add package.json to the server
COPY package.json ./

# Install app dependencies
RUN npm install

# Add server files to the directory
COPY . ./

# Expose the http and https ports
EXPOSE 50001

# Start the application
CMD [ "node", "index.js" ]