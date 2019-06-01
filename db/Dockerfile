FROM postgres:alpine
LABEL app=db
ARG POSTGRESQL_USER=vagrant
ARG POSTGRESQL_PASSWORD=vagrant
ARG POSTGRESQL_DATABASE=news
COPY ./data .
RUN apk update; apk add unzip; unzip newsdata.zip