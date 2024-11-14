all: test ruff build run

test:
	poetry run pytest

ruff:
	poetry run ruff check . --fix
	poetry run ruff format --preview

build:
	docker build -t simple-image-upload-api:latest .

run:
	docker-compose up -d
