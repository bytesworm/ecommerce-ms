FROM python:3.13.3-slim-bookworm

# install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# install curl
RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY . .

RUN uv sync --locked

ENV PATH="/app/.venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
