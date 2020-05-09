FROM python:3.8.2-slim as base

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /srv/app
COPY . .

RUN poetry config settings.virtualenvs.create false
RUN poetry install --no-dev --no-root

EXPOSE $PORT

CMD ["sh", "-c", "poetry run waitress-serve --port $PORT --call 'stocks:create_app'"]