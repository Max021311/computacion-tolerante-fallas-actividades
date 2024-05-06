FROM node:20-alpine
WORKDIR /usr/src/app

COPY package.json .
COPY src src/

RUN yarn install

CMD ["node", "src/server.js"]
