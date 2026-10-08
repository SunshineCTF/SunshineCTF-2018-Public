# node 8 to match the original toolchain (webpack 4 / babel 6-7 era).
FROM node:8

RUN useradd --no-log-init -r -m user

WORKDIR /usr/src/app
COPY package.json ./
RUN npm install

COPY . ./

EXPOSE 50001
CMD ["node", "index.js"]
