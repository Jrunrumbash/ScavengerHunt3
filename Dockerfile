FROM python:3.6.5-slim
MAINTAINER James Runswick <jrunswick@gmail.com>

RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main' >> /etc/apt/sources.list.d/pgdg.list
RUN apt-get update && apt-get install -qq -y build-essential libpq-dev postgresql-client-10 --fix-missing --no-install-recommends --allow-unauthenticated

ENV INSTALL_PATH /hunt_app
RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

VOLUME /hunt_app


CMD gunicorn -b 0.0.0.0:8000 "app:create_app()"
