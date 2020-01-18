# Pull base image
FROM python:3.7-alpine

MAINTAINER Goutom Roy

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

# set work directory
WORKDIR /code/

# install psycopg2 dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# copy project files to container filesystem
COPY . /code/

# install dependencies
RUN pip3 install -r requirements.txt



