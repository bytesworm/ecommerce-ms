#!/bin/sh

set -e
set -x

# check db connection
python app/prestart.py

# run migrations
alembic upgrade head
