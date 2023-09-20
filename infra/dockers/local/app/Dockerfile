# Stage 1: Build stage
FROM hello-world-backend-base:latest AS build

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1


ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache


ARG APP_HOME=/app
WORKDIR ${APP_HOME}

# Install project dependencies using poetry
COPY /requirements/development.txt /app
RUN pip install --no-cache-dir -r development.txt

# copy basic entrypoint.sh
COPY ./infra/dockers/local/entrypoint /app/entrypoint
RUN sed -i 's/\r$//g' /app/entrypoint
RUN chmod +x /app/entrypoint

COPY ./infra/dockers/local/scripts/runserver.sh /app/scripts/runserver.sh
RUN sed -i 's/\r$//g' /app/scripts/runserver.sh
RUN chmod +x /app/scripts/runserver.sh

# copy application code to WORKDIR
COPY . ${APP_HOME}

# Stage 2: Final stage
FROM gcr.io/distroless/python3-debian9
COPY --from=build /usr/local/lib/python3.9/site-packages/ /usr/local/lib/python3.9/site-packages/
COPY --from=build /usr/local/bin/python3.9 /usr/local/bin/python3.9

COPY --from=build /app /app
ENV PYTHONPATH "${PYTHONPATH}:/usr/local/lib/python3.9/site-packages"

WORKDIR /app

ENTRYPOINT ["python", "manage.py", "runserver"]
