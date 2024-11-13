all: test lint build run

test:
    poetry run pytest

lint:
    poetry run ruff format --preview
    poetry run ruff lint

build:
    docker build -t simple-image-upload-api:latest .

run:
    docker-compose up -d

