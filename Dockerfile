FROM python:3.8.2-slim as base

RUN apt-get update && apt-get install -y \
    libpq-dev \
    libmagic-dev \
    netcat \
    gcc

RUN pip install --upgrade pip
RUN pip install poetry

WORKDIR /app
COPY . .

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev --no-root

EXPOSE $PORT

CMD ["sh", "-c", "uvicorn --port $PORT --host 0.0.0.0 stocks.app:app --reload"]