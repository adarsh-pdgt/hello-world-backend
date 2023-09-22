ARG PYTHON_VERSION=3.9-slim-buster

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # git
  git \
  # gdal for postgis
  gdal-bin \
  libgdal-dev\
  # recognizing image files data
  libmagic-dev \
  # nginx
  nginx-full


# build uwsgi plugin for python 3.
# https://www.paulox.net/2017/04/04/how-to-use-uwsgi-with-python3-6-in-ubuntu/
RUN apt-get update && apt-get install -y uwsgi-emperor\
  uwsgi \
  uwsgi-src \
  uuid-dev \
  libcap-dev \
  libpcre3-dev
RUN cd ~
RUN export PYTHON=python3.9
RUN uwsgi --build-plugin "/usr/src/uwsgi/plugins/python python39"
RUN mv python39_plugin.so /usr/lib/uwsgi/plugins/python39_plugin.so
RUN chmod 644 /usr/lib/uwsgi/plugins/python39_plugin.so


# Install required system dependencies
RUN apt-get update && apt-get install --no-install-recommends -y \
  # psycopg2 dependencies
  libpq-dev \
  # Translations dependencies
  gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# install the basic requirements to cache in the base build
COPY ./requirements .
COPY pyproject.toml .
RUN pip install -U pip poetry
RUN poetry env use python3
RUN poetry config virtualenvs.create false
RUN poetry update
RUN python3 -m pip install --upgrade pip wheel
RUN poetry install
