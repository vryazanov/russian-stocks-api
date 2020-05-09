FROM python:3.8.2-slim as base

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /srv/app
COPY . .

RUN poetry install --no-dev --no-root

CMD ["sh", "-c", "poetry run waitress-serve --port $PORT --call 'stocks:create_app'"]