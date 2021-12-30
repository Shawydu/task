FROM node:14 AS builder

WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY . /app/

RUN npm run build

FROM nginx:1.15

COPY --from=builder /app/build/ /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
