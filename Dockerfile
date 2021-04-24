FROM python:3.8-alpine

RUN apk add --update --no-cache g++ gcc postgresql-dev libffi-dev

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

### Upgrade pip to prevent errors
RUN pip install setuptools --upgrade
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /cyclone
WORKDIR /cyclone
ADD . /cyclone

EXPOSE 7007