FROM hello-world-backend-base:latest

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

# copy basic entrypoint.sh
COPY ./infra/dockers/local/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

RUN chmod +x /entrypoint

COPY ./infra/dockers/local/scripts/runserver.sh /scripts/runserver.sh
RUN sed -i 's/\r$//g' /scripts/runserver.sh
RUN chmod +x /scripts/runserver.sh

# copy application code to WORKDIR
COPY . ${APP_HOME}

RUN poetry install

ENTRYPOINT ["/entrypoint"]
