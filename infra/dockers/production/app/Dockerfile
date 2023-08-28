FROM hello-world-backend-base:latest


# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # aws-cli
  awscli

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Requirements are installed here to ensure they will be cached.
COPY ./requirements .
COPY pyproject.toml .

RUN pip install -U pip poetry
RUN poetry env use python3
RUN poetry config virtualenvs.create false
RUN poetry update
RUN python3 -m pip install --upgrade pip wheel

ARG APP_HOME=/app

WORKDIR ${APP_HOME}

RUN mkdir /scripts

# copy basic entypoint.sh
COPY ./infra/dockers/production/entrypoint /scripts/entrypoint
RUN sed -i 's/\r$//g' /scripts/entrypoint
RUN chmod +x /scripts/entrypoint

COPY ./infra/dockers/production/scripts/run-uwsgi.sh /scripts/run-uwsgi.sh
RUN sed -i 's/\r$//g' /scripts/run-uwsgi.sh
RUN chmod +x /scripts/run-uwsgi.sh

COPY ./infra/dockers/production/scripts/migrate.sh /scripts/migrate.sh
RUN sed -i 's/\r$//g' /scripts/migrate.sh
RUN chmod +x /scripts/migrate.sh

COPY ./infra/dockers/production/scripts/run-daphne.sh /scripts/run-daphne.sh
RUN sed -i 's/\r$//g' /scripts/run-daphne.sh
RUN chmod +x /scripts/run-daphne.sh

RUN rm /etc/nginx/nginx.conf
COPY ./infra/dockers/production/scripts/nginx/nginx.conf /etc/nginx/nginx.conf

RUN rm /etc/nginx/sites-enabled/default
COPY ./infra/dockers/production/scripts/nginx/nginx-site.conf /etc/nginx/sites-enabled/nginx-site.conf

COPY ./infra/dockers/production/scripts/uwsgi/uwsgi.ini /scripts/uwsgi.ini

# copy application code to WORKDIR
COPY .. ${APP_HOME}

# copy basic entypoint.sh
COPY ./infra/dockers/production/scripts/nginx/nginx.sh /scripts/nginx.sh
RUN sed -i 's/\r$//g' /scripts/nginx.sh
RUN chmod +x /scripts/nginx.sh

RUN poetry install

ENTRYPOINT ["/scripts/entrypoint"]
