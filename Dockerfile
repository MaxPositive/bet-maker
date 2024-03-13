FROM python:3.12-slim-bookworm as python

FROM python as python-build-stage

ENV POETRY_HOME="/opt/poetry"
ENV POETRY_VENV="/opt/poetry-venv"
ENV POETRY_CACHE_DIR="/opt/.cache"


RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry


FROM python as python-run-stage

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    POETRY_VENV="/opt/poetry-venv"

ARG APP_HOME=/app
WORKDIR $APP_HOME

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*


# Copy Poetry to app image
COPY --from=python-build-stage $POETRY_VENV $POETRY_VENV

# Add Poetry to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

COPY pyproject.toml poetry.lock ${APP_HOME}

RUN poetry check

RUN poetry install --no-interaction --no-cache

COPY . ${APP_HOME}



WORKDIR $APP_HOME

RUN chmod +x "./scripts/start.sh"

CMD ["./scripts/start.sh"]