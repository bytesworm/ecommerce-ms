# Authentication Service

A microservice that manages user authentication data, and handles generation and validation of JWT tokens.

## Quick start

### Development

> [!IMPORTANT]
> To use this project, you need to have [`uv`](https://github.com/astral-sh/uv) installed.

> [!NOTE]
> Don't forget to create and fill your `.env` file.

```bash
uv sync
uv run uvicorn app.main:app --reload
```
