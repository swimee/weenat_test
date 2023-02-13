FROM node:lts-alpine3.14

WORKDIR /datalogger
ENV NODE_ENV development

COPY db.json ./
COPY package.json ./

RUN yarn install

EXPOSE 3000