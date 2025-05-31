# Authentication Service

![Coverage](https://codecov.io/github/bytesworm/ecommerce-ms/branch/main/graph/badge.svg?token=TCF23H716I&flag=auth-service)

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
