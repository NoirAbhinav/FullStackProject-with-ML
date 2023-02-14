FROM node:19-alpine3.16 as build-env

USER root

RUN mkdir /frontend
WORKDIR /frontend

COPY ./package.json /frontend/package.json
RUN npm install --force

COPY . /frontend/

CMD [ "npm", "start" ]
