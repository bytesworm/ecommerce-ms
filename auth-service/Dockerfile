FROM python:3.13.2-alpine

WORKDIR /auth-service

COPY ./pyproject.toml ./poetry.lock ./alembic.ini /auth-service/
COPY scripts /auth-service/scripts
COPY app /auth-service/app

ENV PYTHONPATH=/auth-service

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

CMD [ "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]
