FROM python:3.11-slim

RUN mkdir /app \
	&& mkdir /log \
	&& mkdir /volume

RUN apt-get update && apt-get install -y curl vim
RUN apt-get clean

RUN pip install --upgrade pip

WORKDIR /
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:${PATH}"

COPY pyproject.toml /
COPY poetry.lock /
COPY ./app /app

RUN poetry install --without dev
RUN yes | poetry cache clear . --all

ENTRYPOINT ["poetry", "run"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
