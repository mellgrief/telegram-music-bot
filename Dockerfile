FROM python:3.11-slim-buster as builder
LABEL authors="mellgrief"


RUN pip install poetry

WORKDIR /app
COPY . /app

RUN poetry install --no-root --no-dev

CMD ["poetry", "run", "python", "main.py"]