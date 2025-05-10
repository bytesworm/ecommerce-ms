FROM python:3.13.2-alpine AS dev
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install
COPY app ./app
ENTRYPOINT [ "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]


FROM python:3.13.2-alpine AS prod
WORKDIR /app
COPY pyproject.toml poetry.lock ./
RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --without dev
COPY app ./app
ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
