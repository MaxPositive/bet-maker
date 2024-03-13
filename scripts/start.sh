#!/usr/bin/env bash

set -e

poetry run alembic upgrade head

exec poetry run uvicorn src:init_app --host 0.0.0.0 --port 8000 --reload